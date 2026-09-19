#!/usr/bin/env python3
"""Download the official Ultralytics Construction-PPE archive and record provenance."""
from __future__ import annotations
import argparse, hashlib, json, shutil, urllib.request, zipfile
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_URL = "https://github.com/ultralytics/assets/releases/download/v0.0.0/construction-ppe.zip"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def safe_extract(zf: zipfile.ZipFile, dest: Path) -> None:
    root = dest.resolve()
    for member in zf.infolist():
        target = (dest / member.filename).resolve()
        if root not in target.parents and target != root:
            raise RuntimeError(f"Unsafe ZIP member path: {member.filename}")
    zf.extractall(dest)


def find_dataset_root(root: Path) -> Path:
    candidates = [root] + [p for p in root.rglob("*") if p.is_dir()]
    for p in candidates:
        if all((p / "images" / s).is_dir() for s in ("train", "val", "test")) and all(
            (p / "labels" / s).is_dir() for s in ("train", "val", "test")
        ):
            return p
    raise RuntimeError("Could not locate a YOLO dataset root with images/{train,val,test} and labels/{train,val,test}.")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", default=DEFAULT_URL)
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--metadata-out", required=True, type=Path)
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    archive = args.out / "construction-ppe.zip"
    req = urllib.request.Request(args.url, headers={"User-Agent": "Stage2-Audit/1.0"})
    with urllib.request.urlopen(req, timeout=120) as r, archive.open("wb") as f:
        shutil.copyfileobj(r, f)
    extract_dir = args.out / "extracted"
    extract_dir.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(archive) as zf:
        safe_extract(zf, extract_dir)
    dataset_root = find_dataset_root(extract_dir)
    meta = {
        "dataset": "Construction-PPE",
        "source_url": args.url,
        "downloaded_at_utc": datetime.now(timezone.utc).isoformat(),
        "archive_sha256": sha256_file(archive),
        "archive_size_bytes": archive.stat().st_size,
        "dataset_root": str(dataset_root.resolve()),
    }
    args.metadata_out.parent.mkdir(parents=True, exist_ok=True)
    args.metadata_out.write_text(json.dumps(meta, indent=2), encoding="utf-8")
    print(json.dumps(meta, indent=2))


if __name__ == "__main__":
    main()
