#!/usr/bin/env python3
"""Normalize mixed YOLO box/polygon labels to temporary detection boxes, then run Stage 2 audit.

Why this wrapper exists
-----------------------
Roboflow YOLO exports can contain standard detection rows (5 fields) and
polygon/segmentation rows (class id + x/y coordinate pairs). The original
Stage 2 auditor is intentionally strict for 5-field detection labels, so it
would otherwise misclassify valid polygon rows as malformed.

This wrapper is read-only with respect to the downloaded dataset. It builds a
temporary normalized detection view, converts valid polygons to their enclosing
axis-aligned boxes, records conversion statistics, and then invokes the original
auditor on that temporary view.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from collections import Counter
from pathlib import Path


def find_image_dir(root: Path, split: str):
    candidates = [
        root / "images" / split,
        root / split / "images",
        root / split,
        root / "Images" / split,
        root / split / "Images",
    ]
    return next((p for p in candidates if p.is_dir()), None)


def find_label_dir(root: Path, split: str):
    candidates = [
        root / "labels" / split,
        root / split / "labels",
        root / "Labels" / split,
        root / split / "Labels",
    ]
    return next((p for p in candidates if p.is_dir()), None)


def normalize_row(parts):
    """Return (normalized_detection_row, kind).

    kind is one of: bbox, polygon, malformed, non_numeric.
    Polygon syntax is class + at least 3 x/y pairs => odd number of fields >= 7.
    """
    if len(parts) == 5:
        try:
            vals = [float(x) for x in parts]
        except ValueError:
            return None, "non_numeric"
        return " ".join(parts), "bbox"

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
        xc = (x1 + x2) / 2.0
        yc = (y1 + y2) / 2.0
        w = x2 - x1
        h = y2 - y1
        return f"{cls:g} {xc:.12g} {yc:.12g} {w:.12g} {h:.12g}", "polygon"

    return None, "malformed"


def mirror_images(source: Path, target: Path):
    target.parent.mkdir(parents=True, exist_ok=True)
    try:
        os.symlink(source, target, target_is_directory=True)
    except OSError:
        shutil.copytree(source, target)


def convert_labels(source_dir: Path, target_dir: Path, stats: Counter):
    target_dir.mkdir(parents=True, exist_ok=True)
    for src in source_dir.rglob("*.txt"):
        rel = src.relative_to(source_dir)
        dst = target_dir / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        out_lines = []
        text = src.read_text(encoding="utf-8", errors="replace")
        for line in text.splitlines():
            stripped = " ".join(line.split())
            if not stripped:
                continue
            norm, kind = normalize_row(stripped.split())
            stats[kind] += 1
            if norm is not None:
                out_lines.append(norm)
            else:
                # Preserve truly unrecognized rows so the strict auditor can flag them.
                out_lines.append(stripped)
        dst.write_text("\n".join(out_lines) + ("\n" if out_lines else ""), encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dataset-name", required=True)
    ap.add_argument("--root", required=True, type=Path)
    ap.add_argument("--data-yaml", required=True, type=Path)
    ap.add_argument("--splits", default="train,val,test")
    ap.add_argument("--near-hash-distance", type=int, default=4)
    ap.add_argument("--skip-near-duplicates", action="store_true")
    ap.add_argument("--out", required=True, type=Path)
    args = ap.parse_args()

    args.out.mkdir(parents=True, exist_ok=True)
    splits = [s.strip() for s in args.splits.split(",") if s.strip()]
    stats = Counter()
    split_stats = {}

    auditor = Path(__file__).with_name("stage2_dataset_audit.py")

    with tempfile.TemporaryDirectory(prefix="stage2_normalized_") as td:
        temp_root = Path(td)
        for split in splits:
            img_dir = find_image_dir(args.root, split)
            lab_dir = find_label_dir(args.root, split)
            local = Counter()
            if img_dir is not None:
                mirror_images(img_dir, temp_root / split / "images")
            if lab_dir is not None:
                convert_labels(lab_dir, temp_root / split / "labels", local)
            stats.update(local)
            split_stats[split] = dict(local)

        report = {
            "source_root": str(args.root),
            "normalization": "YOLO polygons converted to enclosing axis-aligned detection boxes in a temporary read-only view",
            "row_counts": dict(stats),
            "row_counts_by_split": split_stats,
            "polygon_rule": "class + >=3 normalized x/y pairs (odd field count >=7)",
        }
        (args.out / "annotation_format_report.json").write_text(
            json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8"
        )

        cmd = [
            sys.executable,
            str(auditor),
            "--dataset-name", args.dataset_name,
            "--root", str(temp_root),
            "--data-yaml", str(args.data_yaml),
            "--splits", ",".join(splits),
            "--near-hash-distance", str(args.near_hash_distance),
            "--out", str(args.out),
        ]
        if args.skip_near_duplicates:
            cmd.append("--skip-near-duplicates")
        completed = subprocess.run(cmd)
        raise SystemExit(completed.returncode)


if __name__ == "__main__":
    main()
