#!/usr/bin/env python3
"""Stage 4.5 label-completeness/background-policy audit.

Parses annotation metadata for all splits, but opens image pixels only for
train/validation visual review. Test image pixels are never opened.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
from collections import Counter, defaultdict
from pathlib import Path
from typing import Iterable

import yaml
from PIL import Image, ImageDraw, ImageFont

Y_EXPECTED_NAMES = [
    "Persons", "Hard Hat", "Safety Boots", "Safety Vests", "No Gloves",
    "Gloves", "No Face Mask", "Pants", "No Safety Vest", "Goggles",
    "No Safety Boots", "No Safety Attire", "Animal", "Child", "Face Masks",
    "No Hard Hat", "Soft Hat",
]
C_EXPECTED_NAMES = [
    "helmet", "gloves", "vest", "boots", "goggles", "none", "Person",
    "no_helmet", "no_goggle", "no_gloves", "no_boots",
]

RETAINED = {
    "Y-PPE": {
        "Persons": "person", "Hard Hat": "helmet", "Gloves": "gloves",
        "Safety Vests": "vest", "Safety Boots": "boots", "Goggles": "goggles",
        "No Hard Hat": "no_helmet", "No Gloves": "no_gloves",
        "No Safety Boots": "no_boots",
    },
    "Construction-PPE": {
        "Person": "person", "helmet": "helmet", "gloves": "gloves",
        "vest": "vest", "boots": "boots", "goggles": "goggles",
        "no_helmet": "no_helmet", "no_gloves": "no_gloves",
        "no_boots": "no_boots",
    },
}

CRITICAL_PAIRS = {
    "Y-PPE": {
        "Child": ["Persons"],
        "No Safety Attire": ["Persons"],
        "Soft Hat": ["Hard Hat", "No Hard Hat"],
    },
    "Construction-PPE": {"none": ["Person"]},
}
INFORMATIONAL_PAIRS = {
    "Y-PPE": {"No Safety Vest": ["Safety Vests"]},
    "Construction-PPE": {"no_goggle": ["goggles"]},
}
IMG_EXTS = [".jpg", ".jpeg", ".png", ".webp", ".bmp"]


def parse_split_map(text: str) -> dict[str, str]:
    out = {}
    for item in text.split(","):
        left, right = item.split(":", 1)
        out[left.strip()] = right.strip()
    return out


def load_names(path: Path | None, expected: list[str]) -> list[str]:
    if path is None:
        return expected
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    names = data.get("names")
    if isinstance(names, dict):
        names = [names[i] if i in names else names[str(i)] for i in range(len(names))]
    names = [str(x) for x in names]
    if names != expected:
        raise SystemExit(f"Source class-order mismatch. Observed={names}; expected={expected}")
    return names


def resolve_split_dirs(root: Path, physical_split: str) -> tuple[Path, Path]:
    for images, labels in [
        (root / physical_split / "images", root / physical_split / "labels"),
        (root / "images" / physical_split, root / "labels" / physical_split),
    ]:
        if images.is_dir() and labels.is_dir():
            return images, labels
    raise SystemExit(f"Could not resolve split={physical_split} under {root}")


def bbox_from_yolo(tokens: list[str]) -> tuple[float, float, float, float]:
    vals = [float(x) for x in tokens[1:]]
    if len(vals) == 4:
        xc, yc, w, h = vals
        return (xc - w / 2, yc - h / 2, xc + w / 2, yc + h / 2)
    if len(vals) >= 6 and len(vals) % 2 == 0:
        xs, ys = vals[0::2], vals[1::2]
        return (min(xs), min(ys), max(xs), max(ys))
    raise ValueError(f"Unsupported YOLO row with {len(vals)} coordinates")


def area(b):
    return max(0.0, b[2] - b[0]) * max(0.0, b[3] - b[1])


def iou(a, b) -> float:
    ix1, iy1, ix2, iy2 = max(a[0], b[0]), max(a[1], b[1]), min(a[2], b[2]), min(a[3], b[3])
    inter = max(0.0, ix2 - ix1) * max(0.0, iy2 - iy1)
    union = area(a) + area(b) - inter
    return inter / union if union > 0 else 0.0


def containment(a, b) -> float:
    ix1, iy1, ix2, iy2 = max(a[0], b[0]), max(a[1], b[1]), min(a[2], b[2]), min(a[3], b[3])
    inter = max(0.0, ix2 - ix1) * max(0.0, iy2 - iy1)
    aa = area(a)
    return inter / aa if aa > 0 else 0.0


def image_for_label(images_dir: Path, label: Path) -> Path | None:
    for ext in IMG_EXTS:
        for candidate in [images_dir / f"{label.stem}{ext}", images_dir / f"{label.stem}{ext.upper()}"]:
            if candidate.exists():
                return candidate
    matches = list(images_dir.glob(label.stem + ".*"))
    return matches[0] if matches else None


def iter_label_files(labels_dir: Path) -> Iterable[Path]:
    yield from sorted(labels_dir.glob("*.txt"))


def read_objects(label: Path, names: list[str]) -> list[dict]:
    out = []
    text = label.read_text(encoding="utf-8").strip()
    if not text:
        return out
    for line_no, line in enumerate(text.splitlines(), 1):
        toks = line.split()
        if len(toks) < 5:
            raise SystemExit(f"Malformed label row {label}:{line_no}: {line}")
        cid = int(float(toks[0]))
        if not 0 <= cid < len(names):
            raise SystemExit(f"Class id {cid} outside names in {label}:{line_no}")
        out.append({"class_id": cid, "class_name": names[cid], "bbox": bbox_from_yolo(toks)})
    return out


def risk_analysis(objects: list[dict], dataset: str):
    by_name = defaultdict(list)
    for o in objects:
        by_name[o["class_name"]].append(o)
    reasons, overlap_rows = [], []
    for severity, pairs in [("critical", CRITICAL_PAIRS[dataset]), ("informational", INFORMATIONAL_PAIRS[dataset])]:
        for excluded_name, shared_names in pairs.items():
            for idx, ex in enumerate(by_name.get(excluded_name, [])):
                candidates = [o for s in shared_names for o in by_name.get(s, [])]
                best_iou = max([iou(ex["bbox"], c["bbox"]) for c in candidates], default=0.0)
                best_contain = max([containment(ex["bbox"], c["bbox"]) for c in candidates], default=0.0)
                matched = best_iou >= 0.50 or best_contain >= 0.80
                overlap_rows.append({
                    "severity": severity,
                    "excluded_class": excluded_name,
                    "candidate_shared_classes": "|".join(shared_names),
                    "excluded_index": idx,
                    "best_iou": round(best_iou, 6),
                    "best_containment": round(best_contain, 6),
                    "structurally_matched": matched,
                })
                if severity == "critical" and not matched:
                    reasons.append(f"critical_unmatched:{excluded_name}")
    return sorted(set(reasons)), overlap_rows


def draw_review_image(image_path: Path, objects: list[dict], retained_names: set[str], title: str) -> Image.Image:
    im = Image.open(image_path).convert("RGB")
    w, h = im.size
    draw = ImageDraw.Draw(im)
    font = ImageFont.load_default()
    for o in objects:
        x1, y1, x2, y2 = o["bbox"]
        box = (int(x1 * w), int(y1 * h), int(x2 * w), int(y2 * h))
        retained = o["class_name"] in retained_names
        color = (0, 180, 0) if retained else (220, 80, 0)
        draw.rectangle(box, outline=color, width=max(2, int(min(w, h) / 300)))
        draw.text((box[0] + 2, max(0, box[1] - 12)), o["class_name"], fill=color, font=font)
    canvas = Image.new("RGB", (w, h + 34), "white")
    canvas.paste(im, (0, 34))
    ImageDraw.Draw(canvas).text((6, 6), title[:180], fill="black", font=font)
    return canvas


def make_contact_sheets(rendered, out_dir: Path, prefix: str):
    out_dir.mkdir(parents=True, exist_ok=True)
    per_page, thumb_w, thumb_h, cols = 12, 360, 270, 3
    outputs = []
    for page_idx in range(math.ceil(len(rendered) / per_page)):
        items = rendered[page_idx * per_page:(page_idx + 1) * per_page]
        sheet = Image.new("RGB", (cols * thumb_w, 4 * thumb_h), "white")
        draw, font = ImageDraw.Draw(sheet), ImageFont.load_default()
        for slot, (caption, p) in enumerate(items):
            im = Image.open(p).convert("RGB")
            im.thumbnail((thumb_w - 8, thumb_h - 28))
            x, y = (slot % cols) * thumb_w, (slot // cols) * thumb_h
            sheet.paste(im, (x + 4, y + 22))
            draw.text((x + 4, y + 4), caption[:55], fill="black", font=font)
        out = out_dir / f"{prefix}_{page_idx + 1:03d}.jpg"
        sheet.save(out, quality=90)
        outputs.append(str(out))
    return outputs


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dataset", required=True, choices=["Y-PPE", "Construction-PPE"])
    ap.add_argument("--root", required=True)
    ap.add_argument("--names-yaml")
    ap.add_argument("--splits", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    dataset, root, out = args.dataset, Path(args.root).resolve(), Path(args.out).resolve()
    out.mkdir(parents=True, exist_ok=True)
    expected_names = Y_EXPECTED_NAMES if dataset == "Y-PPE" else C_EXPECTED_NAMES
    names = load_names(Path(args.names_yaml) if args.names_yaml else None, expected_names)
    retained_map, retained_names = RETAINED[dataset], set(RETAINED[dataset])
    excluded_names = set(names) - retained_names
    split_map = parse_split_map(args.splits)

    image_rows, overlap_table, rendered, split_summary = [], [], [], {}
    for logical, physical in split_map.items():
        images_dir, labels_dir = resolve_split_dirs(root, physical)
        counts = Counter()
        for label in iter_label_files(labels_dir):
            objects = read_objects(label, names)
            shared = [o for o in objects if o["class_name"] in retained_names]
            excluded = [o for o in objects if o["class_name"] in excluded_names]
            reasons, overlaps = risk_analysis(objects, dataset)
            if not shared:
                reasons.append("harmonized_empty")
            reasons = sorted(set(reasons))
            row = {
                "dataset": dataset, "logical_split": logical, "physical_split": physical,
                "file_stem": label.stem, "native_object_count": len(objects),
                "retained_object_count": len(shared), "excluded_object_count": len(excluded),
                "excluded_classes": "|".join(sorted({o["class_name"] for o in excluded})),
                "risk_reasons": "|".join(reasons),
                "visual_review_required": logical != "test" and bool(reasons),
                "test_pixel_opened": False,
            }
            image_rows.append(row)
            for ov in overlaps:
                overlap_table.append({"dataset": dataset, "logical_split": logical, "file_stem": label.stem, **ov})

            counts["images"] += 1
            counts["native_objects"] += len(objects)
            counts["retained_objects"] += len(shared)
            counts["excluded_objects"] += len(excluded)
            if not shared: counts["harmonized_empty_images"] += 1
            if any(r.startswith("critical_unmatched:") for r in reasons): counts["critical_unmatched_images"] += 1
            if logical != "test" and reasons: counts["visual_review_images"] += 1
            if logical == "test" and reasons: counts["test_structural_risk_images"] += 1

            if logical != "test" and reasons:
                image_path = image_for_label(images_dir, label)
                if image_path is None:
                    row["visual_review_error"] = "image_not_found"
                else:
                    review_dir = out / "rendered" / logical
                    review_dir.mkdir(parents=True, exist_ok=True)
                    rendered_path = review_dir / f"{label.stem}.jpg"
                    title = f"{dataset} | {logical} | {label.stem} | {','.join(reasons)}"
                    review = draw_review_image(image_path, objects, retained_names, title)
                    review.thumbnail((1200, 1200))
                    review.save(rendered_path, quality=90)
                    rendered.append((f"{logical}:{label.stem}", rendered_path))
        split_summary[logical] = dict(counts)

    image_csv = out / "image_risk_table.csv"
    fields = ["dataset", "logical_split", "physical_split", "file_stem", "native_object_count",
              "retained_object_count", "excluded_object_count", "excluded_classes", "risk_reasons",
              "visual_review_required", "test_pixel_opened", "visual_review_error"]
    with image_csv.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore"); w.writeheader()
        for r in image_rows: w.writerow(r)

    overlap_csv = out / "excluded_shared_overlap_table.csv"
    ov_fields = ["dataset", "logical_split", "file_stem", "severity", "excluded_class",
                 "candidate_shared_classes", "excluded_index", "best_iou", "best_containment",
                 "structurally_matched"]
    with overlap_csv.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=ov_fields); w.writeheader(); w.writerows(overlap_table)

    sheets = make_contact_sheets(rendered, out / "contact_sheets", dataset.replace("-", "_"))
    critical_unmatched = sum(1 for r in image_rows if any(x.startswith("critical_unmatched:") for x in r["risk_reasons"].split("|") if x))
    trainval_review = sum(1 for r in image_rows if r["visual_review_required"])
    test_risk = sum(1 for r in image_rows if r["logical_split"] == "test" and r["risk_reasons"])

    summary = {
        "stage": "4.5", "dataset": dataset,
        "status": "REQUIRES_MANUAL_REVIEW" if trainval_review or test_risk else "STRUCTURAL_PASS",
        "scientific_rule": {"label_metadata_all_splits": True, "train_val_pixels_may_be_opened": True,
                            "test_pixels_opened": False, "dataset_modified": False},
        "source_class_order": names, "retained_source_classes": retained_map,
        "excluded_source_classes": sorted(excluded_names), "critical_pairs": CRITICAL_PAIRS[dataset],
        "informational_pairs": INFORMATIONAL_PAIRS[dataset],
        "match_rule": "IoU>=0.50 OR excluded-box containment>=0.80",
        "split_summary": split_summary, "critical_unmatched_images_all_splits": critical_unmatched,
        "train_val_visual_review_images": trainval_review, "test_structural_risk_images": test_risk,
        "contact_sheet_count": len(sheets),
        "outputs": {"image_risk_table": str(image_csv), "excluded_shared_overlap_table": str(overlap_csv), "contact_sheets": sheets},
        "closure_allowed": False,
        "next_action": "Manual adjudication of train/val visual panels plus a predeclared annotation-only test policy. If membership/labels change, build a new harmonized derivative/fingerprint before Stage 5.",
    }
    (out / "structural_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
