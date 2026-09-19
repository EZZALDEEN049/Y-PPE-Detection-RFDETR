#!/usr/bin/env python3
"""Create an RF-DETR-compatible YOLO directory view from a Stage 4 frozen derivative.

Stage 4 stores Ultralytics-style directories as images/{train,val,test} and
labels/{train,val,test}. RF-DETR's YOLO detector expects train/images and a
validation split addressable as valid/images (or an equivalent YAML-resolved
layout in supported versions). This adapter changes directory layout only.
Image bytes, label bytes, class order, split membership, and manifest bytes are
preserved exactly.
"""
from __future__ import annotations

import argparse
import hashlib
import os
import shutil
from pathlib import Path

import yaml

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff", ".webp"}
SPLITS = (("train", "train"), ("val", "valid"), ("test", "test"))


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def link_or_copy(src: Path, dst: Path) -> None:
    try:
        os.link(src, dst)
    except OSError:
        shutil.copy2(src, dst)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source-root", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--expected-fingerprint", required=True)
    args = ap.parse_args()

    src = Path(args.source_root).resolve()
    out = Path(args.out).resolve()
    manifest = src / "manifest.jsonl"
    data_yaml = src / "data.yaml"
    if not manifest.is_file() or not data_yaml.is_file():
        raise SystemExit("Stage 4 source must contain manifest.jsonl and data.yaml")
    fp = sha256_file(manifest)
    if fp != args.expected_fingerprint:
        raise SystemExit(f"Source fingerprint mismatch: {fp} != {args.expected_fingerprint}")

    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)

    data = yaml.safe_load(data_yaml.read_text(encoding="utf-8"))
    names = data.get("names")
    if not names or len(names) != 9:
        raise SystemExit("Expected frozen nine-class data.yaml")

    counts = {}
    for source_split, target_split in SPLITS:
        src_images = src / "images" / source_split
        src_labels = src / "labels" / source_split
        if not src_images.is_dir() or not src_labels.is_dir():
            raise SystemExit(f"Missing Stage 4 split directories for {source_split}")
        dst_images = out / target_split / "images"
        dst_labels = out / target_split / "labels"
        dst_images.mkdir(parents=True)
        dst_labels.mkdir(parents=True)

        images = sorted(p for p in src_images.iterdir() if p.is_file() and p.suffix.lower() in IMAGE_EXTS)
        labels = sorted(p for p in src_labels.iterdir() if p.is_file() and p.suffix.lower() == ".txt")
        for p in images:
            link_or_copy(p, dst_images / p.name)
        for p in labels:
            link_or_copy(p, dst_labels / p.name)
        counts[target_split] = {"images": len(images), "labels": len(labels)}
        if len(images) != len(labels):
            raise SystemExit(f"Image/label count mismatch after layout adaptation for {target_split}")

    adapted_yaml = {
        "path": ".",
        "train": "train/images",
        "val": "valid/images",
        "test": "test/images",
        "names": names,
        "nc": 9,
    }
    (out / "data.yaml").write_text(yaml.safe_dump(adapted_yaml, sort_keys=False), encoding="utf-8")
    shutil.copy2(manifest, out / "manifest.jsonl")

    adapted_fp = sha256_file(out / "manifest.jsonl")
    if adapted_fp != fp:
        raise SystemExit("Manifest bytes changed during RF-DETR layout adaptation")

    print({
        "source_fingerprint": fp,
        "adapted_fingerprint": adapted_fp,
        "counts": counts,
        "content_changed": False,
        "split_membership_changed": False,
    })


if __name__ == "__main__":
    main()
