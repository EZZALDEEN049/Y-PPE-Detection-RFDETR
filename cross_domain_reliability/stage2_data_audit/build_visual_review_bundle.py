#!/usr/bin/env python3
"""Build a manual-review bundle for Stage 2 Y-PPE/YOLO audits.

The bundle is read-only with respect to the dataset. It creates:
- CSV manifest for cross-split near-duplicate candidates;
- contact-sheet JPGs with each candidate pair shown side-by-side;
- annotation duplicate provenance CSV that distinguishes exact repeated source
  rows from collisions that appear only after polygon->box normalization;
- CSV for near-identical same-class boxes reported by the auditor;
- compact JSON summary.

This is intended for human adjudication before a dataset split is frozen.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Iterable, Optional

from PIL import Image, ImageDraw, ImageFont

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".webp", ".tif", ".tiff"}


def find_image_dir(root: Path, split: str) -> Optional[Path]:
    candidates = [
        root / "images" / split,
        root / split / "images",
        root / split,
        root / "Images" / split,
        root / split / "Images",
    ]
    return next((p for p in candidates if p.is_dir()), None)


def find_label_dir(root: Path, split: str) -> Optional[Path]:
    candidates = [
        root / "labels" / split,
        root / split / "labels",
        root / "Labels" / split,
        root / split / "Labels",
    ]
    return next((p for p in candidates if p.is_dir()), None)


def index_images(root: Path, splits: Iterable[str]):
    out = {}
    for split in splits:
        d = find_image_dir(root, split)
        if d is None:
            continue
        for p in d.rglob("*"):
            if p.is_file() and p.suffix.lower() in IMAGE_EXTS:
                out[(split, p.name)] = p
    return out


def normalize_row(parts):
    """Return canonical detection row or None, plus source row kind."""
    if len(parts) == 5:
        try:
            vals = [float(x) for x in parts]
        except ValueError:
            return None, "non_numeric"
        cls, x, y, w, h = vals
        return f"{cls:g} {x:.12g} {y:.12g} {w:.12g} {h:.12g}", "bbox"
    if len(parts) >= 7 and len(parts) % 2 == 1:
        try:
            vals = [float(x) for x in parts]
        except ValueError:
            return None, "non_numeric"
        cls = vals[0]
        coords = vals[1:]
        xs = coords[0::2]
        ys = coords[1::2]
        if len(xs) < 3 or len(xs) != len(ys):
            return None, "malformed"
        x1, x2 = min(xs), max(xs)
        y1, y2 = min(ys), max(ys)
        return f"{cls:g} {(x1+x2)/2:.12g} {(y1+y2)/2:.12g} {x2-x1:.12g} {y2-y1:.12g}", "polygon"
    return None, "malformed"


def parse_near_issue(issue: dict):
    split_a, split_b = issue["split"].split("|", 1)
    left, right = issue["file"].split(" <> ", 1)
    distance_match = re.search(r"distance=(\d+)", issue.get("detail", ""))
    distance = int(distance_match.group(1)) if distance_match else None
    return split_a, Path(left).name, split_b, Path(right).name, distance


def exact_pair_names(issues):
    pairs = set()
    for issue in issues:
        if issue.get("issue_type") not in {"cross_split_exact_byte_duplicate", "cross_split_exact_pixel_duplicate"}:
            continue
        names = re.findall(r"(?:train|valid|val|test):([^;]+)", issue.get("detail", ""))
        if len(names) >= 2:
            pair = tuple(sorted(Path(x.strip()).name for x in names[:2]))
            pairs.add(pair)
    return pairs


def fit_image(path: Path, box_w: int, box_h: int):
    with Image.open(path) as im:
        im = im.convert("RGB")
        im.thumbnail((box_w, box_h))
        canvas = Image.new("RGB", (box_w, box_h), "white")
        x = (box_w - im.width) // 2
        y = (box_h - im.height) // 2
        canvas.paste(im, (x, y))
    return canvas


def short(text: str, n: int = 68):
    return text if len(text) <= n else text[: n - 3] + "..."


def make_contact_sheets(rows, image_index, out_dir: Path, per_page: int = 4):
    out_dir.mkdir(parents=True, exist_ok=True)
    font = ImageFont.load_default()
    page_paths = []
    cell_w, img_h, label_h = 520, 300, 62
    margin, gap = 18, 12
    pair_h = label_h + img_h + 24
    width = margin * 2 + cell_w * 2 + gap

    for page_idx in range(0, len(rows), per_page):
        chunk = rows[page_idx : page_idx + per_page]
        height = margin * 2 + pair_h * len(chunk)
        sheet = Image.new("RGB", (width, height), "white")
        draw = ImageDraw.Draw(sheet)
        y = margin
        for row in chunk:
            title = f"Pair {row['pair_id']} | {row['split_a']} <-> {row['split_b']} | dHash={row['dhash_distance']} | exact={row['exact_confirmed']}"
            draw.text((margin, y), title, fill="black", font=font)
            draw.text((margin, y + 18), short(row['file_a']), fill="black", font=font)
            draw.text((margin + cell_w + gap, y + 18), short(row['file_b']), fill="black", font=font)
            pa = image_index.get((row['split_a'], row['file_a']))
            pb = image_index.get((row['split_b'], row['file_b']))
            if pa and pa.exists():
                sheet.paste(fit_image(pa, cell_w, img_h), (margin, y + label_h))
            else:
                draw.rectangle((margin, y + label_h, margin + cell_w, y + label_h + img_h), outline="black")
                draw.text((margin + 12, y + label_h + 20), "IMAGE A NOT FOUND", fill="black", font=font)
            if pb and pb.exists():
                sheet.paste(fit_image(pb, cell_w, img_h), (margin + cell_w + gap, y + label_h))
            else:
                x0 = margin + cell_w + gap
                draw.rectangle((x0, y + label_h, x0 + cell_w, y + label_h + img_h), outline="black")
                draw.text((x0 + 12, y + label_h + 20), "IMAGE B NOT FOUND", fill="black", font=font)
            y += pair_h
        page = out_dir / f"near_duplicate_contact_sheet_{page_idx // per_page + 1:02d}.jpg"
        sheet.save(page, quality=90)
        page_paths.append(page)
    return page_paths


def build_annotation_duplicate_provenance(root: Path, splits, out_csv: Path):
    records = []
    aggregate = Counter()
    for split in splits:
        label_dir = find_label_dir(root, split)
        if label_dir is None:
            continue
        for lab in label_dir.rglob("*.txt"):
            text = lab.read_text(encoding="utf-8", errors="replace")
            raw_rows = []
            canonical_groups = defaultdict(list)
            raw_groups = defaultdict(list)
            for line_no, line in enumerate(text.splitlines(), 1):
                stripped = " ".join(line.split())
                if not stripped:
                    continue
                canonical, kind = normalize_row(stripped.split())
                raw_groups[stripped].append((line_no, kind, canonical))
                if canonical is not None:
                    canonical_groups[canonical].append((line_no, kind, stripped))
                raw_rows.append((line_no, stripped, kind, canonical))

            for raw, entries in raw_groups.items():
                if len(entries) > 1:
                    aggregate[(split, "raw_exact_duplicate")] += len(entries) - 1
                    records.append({
                        "split": split,
                        "label_file": lab.name,
                        "duplicate_type": "raw_exact_duplicate",
                        "occurrences": len(entries),
                        "line_numbers": ";".join(str(x[0]) for x in entries),
                        "source_kinds": ";".join(sorted({x[1] for x in entries})),
                        "canonical_row": entries[0][2] or "",
                        "raw_forms": raw,
                        "decision": "",
                        "notes": "",
                    })

            for canonical, entries in canonical_groups.items():
                raw_forms = sorted({x[2] for x in entries})
                if len(entries) > 1 and len(raw_forms) > 1:
                    aggregate[(split, "canonical_collision_after_normalization")] += len(entries) - 1
                    records.append({
                        "split": split,
                        "label_file": lab.name,
                        "duplicate_type": "canonical_collision_after_normalization",
                        "occurrences": len(entries),
                        "line_numbers": ";".join(str(x[0]) for x in entries),
                        "source_kinds": ";".join(sorted({x[1] for x in entries})),
                        "canonical_row": canonical,
                        "raw_forms": " || ".join(raw_forms),
                        "decision": "",
                        "notes": "",
                    })

    fields = ["split", "label_file", "duplicate_type", "occurrences", "line_numbers", "source_kinds", "canonical_row", "raw_forms", "decision", "notes"]
    with out_csv.open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(records)
    return records, aggregate


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dataset-root", required=True, type=Path)
    ap.add_argument("--issues", required=True, type=Path)
    ap.add_argument("--splits", default="train,valid,test")
    ap.add_argument("--out", required=True, type=Path)
    args = ap.parse_args()

    args.out.mkdir(parents=True, exist_ok=True)
    splits = [x.strip() for x in args.splits.split(",") if x.strip()]
    issues = json.loads(args.issues.read_text(encoding="utf-8"))
    images = index_images(args.dataset_root, splits)
    exact_pairs = exact_pair_names(issues)

    near_rows = []
    for idx, issue in enumerate((x for x in issues if x.get("issue_type") == "cross_split_near_duplicate_candidate"), 1):
        sa, fa, sb, fb, dist = parse_near_issue(issue)
        pair_names = tuple(sorted((fa, fb)))
        near_rows.append({
            "pair_id": f"ND{idx:03d}",
            "split_a": sa,
            "file_a": fa,
            "split_b": sb,
            "file_b": fb,
            "dhash_distance": dist,
            "exact_confirmed": "yes" if pair_names in exact_pairs else "no",
            "decision": "",
            "notes": "",
        })

    manifest = args.out / "near_duplicate_review_manifest.csv"
    fields = ["pair_id", "split_a", "file_a", "split_b", "file_b", "dhash_distance", "exact_confirmed", "decision", "notes"]
    with manifest.open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(near_rows)

    sheets = make_contact_sheets(near_rows, images, args.out / "contact_sheets")

    ann_records, ann_aggregate = build_annotation_duplicate_provenance(
        args.dataset_root,
        splits,
        args.out / "annotation_duplicate_provenance.csv",
    )

    near_box_rows = [x for x in issues if x.get("issue_type") == "near_duplicate_boxes"]
    nb_fields = ["dataset", "split", "file", "issue_type", "detail"]
    with (args.out / "near_identical_boxes.csv").open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=nb_fields)
        w.writeheader()
        for r in near_box_rows:
            w.writerow({k: r.get(k, "") for k in nb_fields})

    split_pair_counts = Counter(f"{r['split_a']}<->{r['split_b']}" for r in near_rows)
    dhash_counts = Counter(str(r["dhash_distance"]) for r in near_rows)
    summary = {
        "near_duplicate_candidates": len(near_rows),
        "confirmed_exact_pairs_in_near_manifest": sum(r["exact_confirmed"] == "yes" for r in near_rows),
        "near_duplicate_counts_by_split_pair": dict(split_pair_counts),
        "dhash_distance_counts": dict(dhash_counts),
        "contact_sheet_pages": len(sheets),
        "annotation_duplicate_provenance_groups": len(ann_records),
        "annotation_duplicate_extra_rows_by_type": {
            f"{split}:{kind}": count for (split, kind), count in sorted(ann_aggregate.items())
        },
        "near_identical_box_issues": len(near_box_rows),
        "manual_review_rule": "Do not delete dHash candidates automatically. Review each pair visually and record leakage / not-leakage / uncertain.",
    }
    (args.out / "visual_review_summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
