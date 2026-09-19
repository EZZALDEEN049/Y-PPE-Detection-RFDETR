#!/usr/bin/env python3
"""
Stage 2 read-only audit for YOLO-format object-detection datasets.

Checks
------
- image/label pairing and orphan labels
- malformed YOLO rows
- class-ID and normalized-coordinate validity
- duplicate annotation rows
- near-identical same-class boxes within a label file
- split image / instance / class counts
- cross-split filename and stem overlap
- SHA-256 exact-byte duplicates across splits
- decoded-pixel exact duplicates across splits
- perceptual dHash near-duplicate candidates across splits (BK-tree indexed)

Important
---------
The script never modifies source dataset files. Class-name order is read from the
actual dataset data.yaml when supplied. If the numeric class order has not yet
been verified, use --num-classes only; the report will use class_0, class_1, ...
and will not invent semantic ID mappings.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

from PIL import Image

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".webp", ".tif", ".tiff"}


@dataclass
class Issue:
    dataset: str
    split: str
    file: str
    issue_type: str
    detail: str


def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while True:
            block = f.read(chunk_size)
            if not block:
                break
            h.update(block)
    return h.hexdigest()


def pixel_hash(path: Path) -> str:
    with Image.open(path) as im:
        im = im.convert("RGB")
        payload = im.tobytes()
        meta = f"{im.width}x{im.height}|RGB|".encode()
    return hashlib.sha256(meta + payload).hexdigest()


def dhash(path: Path, hash_size: int = 8) -> int:
    with Image.open(path) as im:
        im = im.convert("L").resize((hash_size + 1, hash_size))
        px = list(im.getdata())
    bits = 0
    idx = 0
    for y in range(hash_size):
        row = y * (hash_size + 1)
        for x in range(hash_size):
            bits |= (1 if px[row + x] > px[row + x + 1] else 0) << idx
            idx += 1
    return bits


def hamming(a: int, b: int) -> int:
    return (a ^ b).bit_count()


class BKTree:
    """Minimal BK-tree for exact-radius search over 64-bit perceptual hashes."""

    def __init__(self):
        self.root = None

    def add(self, key: int, payload: dict) -> None:
        if self.root is None:
            self.root = [key, [payload], {}]
            return
        node = self.root
        while True:
            d = hamming(key, node[0])
            if d == 0:
                node[1].append(payload)
                return
            child = node[2].get(d)
            if child is None:
                node[2][d] = [key, [payload], {}]
                return
            node = child

    def query(self, key: int, radius: int) -> Iterable[Tuple[int, dict]]:
        if self.root is None:
            return
        stack = [self.root]
        while stack:
            node = stack.pop()
            d = hamming(key, node[0])
            if d <= radius:
                for payload in node[1]:
                    yield d, payload
            low, high = d - radius, d + radius
            for edge, child in node[2].items():
                if low <= edge <= high:
                    stack.append(child)


def box_iou_yolo(a: Sequence[float], b: Sequence[float]) -> float:
    _, ax, ay, aw, ah = a
    _, bx, by, bw, bh = b
    ax1, ay1, ax2, ay2 = ax - aw / 2, ay - ah / 2, ax + aw / 2, ay + ah / 2
    bx1, by1, bx2, by2 = bx - bw / 2, by - bh / 2, bx + bw / 2, by + bh / 2
    ix1, iy1 = max(ax1, bx1), max(ay1, by1)
    ix2, iy2 = min(ax2, bx2), min(ay2, by2)
    iw, ih = max(0.0, ix2 - ix1), max(0.0, iy2 - iy1)
    inter = iw * ih
    union = aw * ah + bw * bh - inter
    return inter / union if union > 0 else 0.0


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


def collect_images(root: Path, split: str) -> List[Path]:
    image_dir = find_image_dir(root, split)
    if image_dir is None:
        return []
    return sorted(p for p in image_dir.rglob("*") if p.is_file() and p.suffix.lower() in IMAGE_EXTS)


def parse_label(
    label_path: Path,
    nclasses: int,
    dataset: str,
    split: str,
    issues: List[Issue],
    near_box_iou: float = 0.995,
):
    rows = []
    raw_seen = set()
    if not label_path.exists():
        return rows
    text = label_path.read_text(encoding="utf-8", errors="replace").strip()
    if not text:
        return rows

    for line_no, line in enumerate(text.splitlines(), 1):
        stripped = " ".join(line.split())
        if stripped in raw_seen:
            issues.append(
                Issue(dataset, split, str(label_path), "duplicate_annotation_row", f"line {line_no}: {stripped}")
            )
        raw_seen.add(stripped)
        parts = stripped.split()
        if len(parts) != 5:
            issues.append(
                Issue(dataset, split, str(label_path), "malformed_label_row", f"line {line_no}: expected 5 fields, got {len(parts)}")
            )
            continue
        try:
            cls_f, x, y, w, h = map(float, parts)
        except ValueError:
            issues.append(Issue(dataset, split, str(label_path), "non_numeric_label", f"line {line_no}: {stripped}"))
            continue
        if not cls_f.is_integer():
            issues.append(Issue(dataset, split, str(label_path), "non_integer_class_id", f"line {line_no}: {cls_f}"))
            continue
        cls = int(cls_f)
        if not 0 <= cls < nclasses:
            issues.append(Issue(dataset, split, str(label_path), "class_id_out_of_range", f"line {line_no}: {cls}"))
        if not (0 <= x <= 1 and 0 <= y <= 1 and 0 < w <= 1 and 0 < h <= 1):
            issues.append(
                Issue(dataset, split, str(label_path), "normalized_coordinate_invalid", f"line {line_no}: {x} {y} {w} {h}")
            )
        x1, y1, x2, y2 = x - w / 2, y - h / 2, x + w / 2, y + h / 2
        tol = 1e-6
        if x1 < -tol or y1 < -tol or x2 > 1 + tol or y2 > 1 + tol:
            issues.append(
                Issue(
                    dataset,
                    split,
                    str(label_path),
                    "box_outside_image",
                    f"line {line_no}: bounds=({x1:.6f},{y1:.6f},{x2:.6f},{y2:.6f})",
                )
            )
        if w * h < 1e-6:
            issues.append(
                Issue(dataset, split, str(label_path), "extremely_tiny_box", f"line {line_no}: normalized_area={w*h:.3e}")
            )
        rows.append((cls, x, y, w, h))

    for i in range(len(rows)):
        for j in range(i + 1, len(rows)):
            if rows[i][0] == rows[j][0]:
                iou = box_iou_yolo(rows[i], rows[j])
                if iou >= near_box_iou and rows[i] != rows[j]:
                    issues.append(
                        Issue(dataset, split, str(label_path), "near_duplicate_boxes", f"rows {i+1},{j+1}; IoU={iou:.6f}")
                    )
    return rows


def load_class_names(args) -> List[str]:
    if args.data_yaml:
        try:
            import yaml
        except ImportError as exc:
            raise SystemExit("PyYAML is required when --data-yaml is used: pip install pyyaml") from exc
        data = yaml.safe_load(args.data_yaml.read_text(encoding="utf-8"))
        names = data.get("names")
        if isinstance(names, dict):
            ordered = [names[i] if i in names else names[str(i)] for i in range(len(names))]
            return [str(x) for x in ordered]
        if isinstance(names, list):
            return [str(x) for x in names]
        raise SystemExit("Could not read ordered class names from data.yaml 'names'.")

    if args.classes_json:
        source = args.classes_json
        if source.strip().startswith("["):
            names = json.loads(source)
        else:
            names = json.loads(Path(source).read_text(encoding="utf-8"))
        if not isinstance(names, list) or not names:
            raise SystemExit("--classes-json must resolve to a non-empty JSON list.")
        return [str(x) for x in names]

    if args.num_classes is not None:
        if args.num_classes <= 0:
            raise SystemExit("--num-classes must be > 0")
        return [f"class_{i}" for i in range(args.num_classes)]

    raise SystemExit("Provide one of --data-yaml, --classes-json, or --num-classes.")


def cross_split_overlap_issues(name: str, records: List[dict], issues: List[Issue]) -> None:
    for key in ["name", "stem", "sha256", "pixel_sha256"]:
        bucket = defaultdict(list)
        for rec in records:
            val = rec.get(key)
            if val:
                bucket[val].append(rec)
        for val, recs in bucket.items():
            splitset = {r["split"] for r in recs}
            if len(splitset) > 1:
                issue_type = {
                    "name": "cross_split_filename_overlap",
                    "stem": "cross_split_stem_overlap",
                    "sha256": "cross_split_exact_byte_duplicate",
                    "pixel_sha256": "cross_split_exact_pixel_duplicate",
                }[key]
                issues.append(
                    Issue(
                        name,
                        "|".join(sorted(splitset)),
                        val,
                        issue_type,
                        "; ".join(f'{r["split"]}:{r["path"]}' for r in recs),
                    )
                )


def cross_split_near_duplicate_issues(
    name: str, records: List[dict], splits: List[str], radius: int, issues: List[Issue]
) -> None:
    by_split = defaultdict(list)
    for rec in records:
        if rec.get("dhash") is not None:
            by_split[rec["split"]].append((int(rec["dhash"], 16), rec))

    for i, split_a in enumerate(splits):
        for split_b in splits[i + 1 :]:
            a = by_split.get(split_a, [])
            b = by_split.get(split_b, [])
            if not a or not b:
                continue
            indexed, queried = (a, b) if len(a) <= len(b) else (b, a)
            tree = BKTree()
            for h, rec in indexed:
                tree.add(h, rec)
            emitted = set()
            for h, rec in queried:
                for d, match in tree.query(h, radius):
                    pair = tuple(sorted((rec["path"], match["path"])))
                    if pair in emitted:
                        continue
                    emitted.add(pair)
                    issues.append(
                        Issue(
                            name,
                            f'{rec["split"]}|{match["split"]}',
                            f'{rec["path"]} <> {match["path"]}',
                            "cross_split_near_duplicate_candidate",
                            f"dHash Hamming distance={d}; manual visual adjudication required",
                        )
                    )


def audit_dataset(
    name: str,
    root: Path,
    class_names: List[str],
    splits: List[str],
    near_hash_distance: int,
    skip_near_duplicates: bool,
):
    nclasses = len(class_names)
    issues: List[Issue] = []
    summary: Dict[str, dict] = {}
    all_images: Dict[str, List[Path]] = {}
    records: List[dict] = []

    for split in splits:
        images = collect_images(root, split)
        label_dir = find_label_dir(root, split)
        all_images[split] = images
        cls_counts = Counter()
        total_instances = 0
        labeled_images = 0
        missing_labels = 0

        if not images:
            issues.append(Issue(name, split, str(root), "split_images_not_found", "No conventional image directory found or split is empty"))
        if label_dir is None:
            issues.append(Issue(name, split, str(root), "split_labels_not_found", "No conventional label directory found"))

        for img in images:
            label_path = label_dir / (img.stem + ".txt") if label_dir else Path("__missing__")
            if not label_dir or not label_path.exists():
                missing_labels += 1
                issues.append(Issue(name, split, str(img), "missing_label_file", "No matching YOLO txt label"))
                rows = []
            else:
                rows = parse_label(label_path, nclasses, name, split, issues)
                labeled_images += 1
            for row in rows:
                cls_counts[row[0]] += 1
            total_instances += len(rows)

            try:
                with Image.open(img) as im:
                    width, height = im.size
            except Exception as exc:
                width = height = None
                issues.append(Issue(name, split, str(img), "image_decode_error", repr(exc)))
            try:
                file_hash = sha256_file(img)
            except Exception as exc:
                file_hash = None
                issues.append(Issue(name, split, str(img), "sha256_error", repr(exc)))
            try:
                decoded_hash = pixel_hash(img)
            except Exception as exc:
                decoded_hash = None
                issues.append(Issue(name, split, str(img), "pixel_hash_error", repr(exc)))
            try:
                perceptual_hash = dhash(img)
            except Exception as exc:
                perceptual_hash = None
                issues.append(Issue(name, split, str(img), "dhash_error", repr(exc)))

            records.append(
                {
                    "dataset": name,
                    "split": split,
                    "path": str(img),
                    "name": img.name,
                    "stem": img.stem,
                    "width": width,
                    "height": height,
                    "sha256": file_hash,
                    "pixel_sha256": decoded_hash,
                    "dhash": format(perceptual_hash, "016x") if perceptual_hash is not None else None,
                }
            )

        summary[split] = {
            "images": len(images),
            "labeled_images": labeled_images,
            "missing_label_files": missing_labels,
            "instances": total_instances,
            "class_instances": {class_names[k]: v for k, v in sorted(cls_counts.items())},
        }

    for split in splits:
        label_dir = find_label_dir(root, split)
        if label_dir:
            image_stems = {p.stem for p in all_images.get(split, [])}
            for lab in label_dir.rglob("*.txt"):
                if lab.stem not in image_stems:
                    issues.append(Issue(name, split, str(lab), "orphan_label_file", "No matching image stem in split"))

    cross_split_overlap_issues(name, records, issues)
    if not skip_near_duplicates:
        cross_split_near_duplicate_issues(name, records, splits, near_hash_distance, issues)

    return summary, records, [asdict(x) for x in issues]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dataset-name", required=True)
    ap.add_argument("--root", required=True, type=Path)
    group = ap.add_mutually_exclusive_group(required=True)
    group.add_argument("--data-yaml", type=Path, help="Actual dataset data.yaml; preferred because it preserves numeric class order")
    group.add_argument("--classes-json", help="JSON list or path to JSON file containing ordered class names")
    group.add_argument("--num-classes", type=int, help="Use only when semantic class-ID order is not yet verified")
    ap.add_argument("--splits", default="train,val,test")
    ap.add_argument("--near-hash-distance", type=int, default=4)
    ap.add_argument("--skip-near-duplicates", action="store_true", help="Skip perceptual near-duplicate screening")
    ap.add_argument("--out", required=True, type=Path)
    args = ap.parse_args()

    class_names = load_class_names(args)
    splits = [s.strip() for s in args.splits.split(",") if s.strip()]
    args.out.mkdir(parents=True, exist_ok=True)

    summary, records, issues = audit_dataset(
        args.dataset_name,
        args.root,
        class_names,
        splits,
        args.near_hash_distance,
        args.skip_near_duplicates,
    )
    (args.out / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    (args.out / "image_manifest.json").write_text(json.dumps(records, indent=2, ensure_ascii=False), encoding="utf-8")
    (args.out / "issues.json").write_text(json.dumps(issues, indent=2, ensure_ascii=False), encoding="utf-8")

    critical_types = {
        "split_images_not_found",
        "split_labels_not_found",
        "malformed_label_row",
        "non_numeric_label",
        "non_integer_class_id",
        "class_id_out_of_range",
        "normalized_coordinate_invalid",
        "box_outside_image",
        "missing_label_file",
        "orphan_label_file",
        "cross_split_exact_byte_duplicate",
        "cross_split_exact_pixel_duplicate",
    }
    critical = [x for x in issues if x["issue_type"] in critical_types]
    print(
        json.dumps(
            {
                "dataset": args.dataset_name,
                "root": str(args.root),
                "summary": summary,
                "issue_count": len(issues),
                "critical_issue_count": len(critical),
                "output_dir": str(args.out),
                "class_order_source": "data.yaml" if args.data_yaml else ("explicit JSON" if args.classes_json else "numeric IDs only"),
            },
            indent=2,
            ensure_ascii=False,
        )
    )
    sys.exit(2 if critical else 0)


if __name__ == "__main__":
    main()
