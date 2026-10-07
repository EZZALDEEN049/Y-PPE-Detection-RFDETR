#!/usr/bin/env python3
"""Stage 7 dataset diagnostic audit for the frozen h9-v2 datasets.

Analysis only: no model loading, inference, training, adaptation, or threshold tuning.
"""
from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd
import yaml
from PIL import Image

CLASSES = [
    "person", "helmet", "gloves", "vest", "boots", "goggles",
    "no_helmet", "no_gloves", "no_boots",
]
SAFETY = {"no_helmet", "no_gloves", "no_boots"}
EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff", ".webp"}


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--y-data", required=True, type=Path)
    p.add_argument("--c-data", required=True, type=Path)
    p.add_argument("--out", required=True, type=Path)
    return p.parse_args()


def read_yaml(path: Path):
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    names = data.get("names")
    if isinstance(names, dict):
        names = [names[k] for k in sorted(names, key=lambda x: int(x))]
    if list(names or []) != CLASSES:
        raise RuntimeError(f"Class order mismatch in {path}: {names}")
    root = Path(data.get("path", "."))
    if not root.is_absolute():
        root = (path.parent / root).resolve()
    return data, root


def resolve_split(yaml_path: Path, split: str):
    data, root = read_yaml(yaml_path)
    target = Path(data[split])
    return target if target.is_absolute() else (root / target).resolve()


def images_in(path: Path):
    return sorted(p for p in path.rglob("*") if p.is_file() and p.suffix.lower() in EXTS)


def label_for_image(image_path: Path):
    parts = list(image_path.parts)
    ids = [i for i, v in enumerate(parts) if v == "images"]
    if not ids:
        raise RuntimeError(f"No images path segment: {image_path}")
    parts[ids[-1]] = "labels"
    return Path(*parts).with_suffix(".txt")


def parse_label(path: Path):
    rows = []
    if not path.exists():
        return rows
    for ln in path.read_text(encoding="utf-8").splitlines():
        if not ln.strip():
            continue
        v = ln.split()
        if len(v) < 5:
            continue
        c = int(float(v[0]))
        x, y, w, h = map(float, v[1:5])
        rows.append((c, x, y, w, h))
    return rows


def summarize_dataset(name: str, yaml_path: Path):
    image_rows = []
    box_rows = []
    class_rows = []
    for split in ("train", "val", "test"):
        split_path = resolve_split(yaml_path, split)
        imgs = images_in(split_path)
        counts = Counter()
        for img in imgs:
            try:
                with Image.open(img) as im:
                    width, height = im.size
            except Exception as e:
                raise RuntimeError(f"Cannot read image {img}: {e}")
            image_rows.append({
                "dataset": name,
                "split": split,
                "image": str(img),
                "width": width,
                "height": height,
                "aspect_ratio": width / height if height else np.nan,
            })
            for c, x, y, w, h in parse_label(label_for_image(img)):
                if c < 0 or c >= len(CLASSES):
                    raise RuntimeError(f"Invalid class id {c} in {label_for_image(img)}")
                cls = CLASSES[c]
                counts[cls] += 1
                area = w * h
                box_rows.append({
                    "dataset": name,
                    "split": split,
                    "class": cls,
                    "image": str(img),
                    "w_norm": w,
                    "h_norm": h,
                    "area_fraction": area,
                    "size_bin": (
                        "small" if area < 0.01 else
                        "medium" if area < 0.10 else
                        "large"
                    ),
                })
        for cls in CLASSES:
            class_rows.append({
                "dataset": name,
                "split": split,
                "class": cls,
                "instances": counts.get(cls, 0),
                "images": len(imgs),
                "instances_per_image": counts.get(cls, 0) / len(imgs) if imgs else np.nan,
            })
    return pd.DataFrame(image_rows), pd.DataFrame(box_rows), pd.DataFrame(class_rows)


def main():
    a = parse_args()
    a.out.mkdir(parents=True, exist_ok=True)
    chunks = []
    boxes = []
    counts = []
    for name, data in [("Y-PPE-h9-v2", a.y_data.resolve()),
                       ("Construction-PPE-h9-v2", a.c_data.resolve())]:
        i, b, c = summarize_dataset(name, data)
        chunks.append(i); boxes.append(b); counts.append(c)

    images = pd.concat(chunks, ignore_index=True)
    bbox = pd.concat(boxes, ignore_index=True)
    cls = pd.concat(counts, ignore_index=True)

    image_summary = (
        images.groupby(["dataset", "split"])
        .agg(
            n_images=("image", "count"),
            width_median=("width", "median"),
            height_median=("height", "median"),
            aspect_ratio_median=("aspect_ratio", "median"),
            aspect_ratio_q25=("aspect_ratio", lambda s: s.quantile(0.25)),
            aspect_ratio_q75=("aspect_ratio", lambda s: s.quantile(0.75)),
        ).reset_index()
    )

    bbox_summary = (
        bbox.groupby(["dataset", "split", "class"])
        .agg(
            n_instances=("area_fraction", "count"),
            area_median=("area_fraction", "median"),
            area_q25=("area_fraction", lambda s: s.quantile(0.25)),
            area_q75=("area_fraction", lambda s: s.quantile(0.75)),
            width_norm_median=("w_norm", "median"),
            height_norm_median=("h_norm", "median"),
        ).reset_index()
    )

    size_counts = (
        bbox.groupby(["dataset", "split", "class", "size_bin"])
        .size().rename("count").reset_index()
    )

    safety = cls[cls["class"].isin(SAFETY)].copy()

    # Dataset-level imbalance summary by split.
    imbalance_rows = []
    for (dataset, split), g in cls.groupby(["dataset", "split"]):
        vals = g["instances"].to_numpy()
        positive = vals[vals > 0]
        imbalance_rows.append({
            "dataset": dataset,
            "split": split,
            "total_instances": int(vals.sum()),
            "min_nonzero_class_instances": int(positive.min()) if len(positive) else 0,
            "max_class_instances": int(vals.max()) if len(vals) else 0,
            "max_to_min_nonzero_ratio": float(vals.max()/positive.min()) if len(positive) else np.nan,
        })
    imbalance = pd.DataFrame(imbalance_rows)

    images.to_csv(a.out/"stage7_image_level_metadata.csv", index=False)
    image_summary.to_csv(a.out/"stage7_image_summary.csv", index=False)
    cls.to_csv(a.out/"stage7_class_instance_counts.csv", index=False)
    bbox_summary.to_csv(a.out/"stage7_bbox_area_summary.csv", index=False)
    size_counts.to_csv(a.out/"stage7_bbox_size_bins.csv", index=False)
    safety.to_csv(a.out/"stage7_safety_class_support.csv", index=False)
    imbalance.to_csv(a.out/"stage7_class_imbalance_summary.csv", index=False)

    summary = {
        "status": "STAGE7_DATASET_DIAGNOSTIC_AUDIT_COMPLETE",
        "analysis_only": True,
        "training_performed": False,
        "inference_performed": False,
        "datasets": ["Y-PPE-h9-v2", "Construction-PPE-h9-v2"],
        "classes": CLASSES,
        "outputs": [
            "stage7_image_summary.csv",
            "stage7_class_instance_counts.csv",
            "stage7_bbox_area_summary.csv",
            "stage7_bbox_size_bins.csv",
            "stage7_safety_class_support.csv",
            "stage7_class_imbalance_summary.csv",
        ],
    }
    (a.out/"stage7_dataset_audit_status.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )
    print("STAGE7_DATASET_DIAGNOSTIC_AUDIT: PASS")


if __name__ == "__main__":
    main()
