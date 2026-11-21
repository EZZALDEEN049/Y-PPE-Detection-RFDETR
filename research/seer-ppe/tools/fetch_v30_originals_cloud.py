#!/usr/bin/env python3
"""Fetch the eight frozen V30 original Roboflow sources on a cloud runner.

Read-only download from the source.roboflow.com original-image URLs archived by
the completed baseline preflight. Does not access Test, modify the Roboflow
dataset, upload source image bytes to GitHub, or print image URLs.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from pathlib import Path
from urllib.parse import urlsplit
from urllib.request import Request, urlopen

from PIL import Image

RESEARCH = Path(__file__).resolve().parents[1]
MAX_DOWNLOAD_BYTES = 40 * 1024 * 1024


def validate_download_url(url: str, asset_id: str):
    p = urlsplit(url)
    if p.scheme != "https" or p.hostname != "source.roboflow.com":
        raise ValueError("Only HTTPS Roboflow original-image sources are permitted")
    if p.username is not None or p.password is not None or p.query or p.fragment:
        raise ValueError("Unexpected credential, query, or fragment in original-image URL")
    parts = p.path.strip("/").split("/")
    if len(parts) != 3 or parts[1] != asset_id or parts[2] != "original.jpg":
        raise ValueError("Original-image URL does not match frozen Asset Library ID")


def retrieve(url: str):
    request = Request(url, headers={"User-Agent": "SEER-PPE-V30-research/1.0"})
    with urlopen(request, timeout=60) as response:
        if getattr(response, "status", 200) != 200:
            raise RuntimeError("Roboflow original-image HTTP response was not 200")
        if response.headers.get("Content-Length"):
            if int(response.headers.get("Content-Length")) > MAX_DOWNLOAD_BYTES:
                raise RuntimeError("Original image exceeds configured safety limit")
        data = response.read(MAX_DOWNLOAD_BYTES + 1)
    if not data or len(data) > MAX_DOWNLOAD_BYTES:
        raise RuntimeError("Original-image bytes are missing or exceed safety limit")
    return data


def fetch_images(manifest: dict, preflight: dict, destination: Path):
    if manifest.get("schema_version") != "seer-ppe/v30-frozen-progressive-xai-targets/v0.30":
        raise ValueError("Unexpected V30 manifest")
    if preflight.get("status") != "PASSED":
        raise ValueError("Actual V30 baseline preflight must have passed")
    if preflight.get("model", {}).get("model_id") != manifest.get("model_id"):
        raise ValueError("Model mismatch in baseline record")
    images = manifest.get("source_images", [])
    if len(images) != 8 or len(manifest.get("targets", [])) != 10:
        raise ValueError("Only the frozen eight images and ten targets may be fetched")
    records = preflight.get("source_images", [])
    by_key = {record["image_key"]: record for record in records}
    if len(records) != 8 or len(by_key) != 8:
        raise ValueError("Baseline preflight does not contain eight unique image records")
    destination.mkdir(parents=True, exist_ok=True)
    hashes = {}
    for image in images:
        key = image["image_key"]
        record = by_key.get(key)
        if record is None:
            raise ValueError("Missing frozen image from baseline record")
        if any(record.get(k) != image.get(v) for k, v in (
            ("filename", "filename"), ("asset_id", "asset_id"), ("split", "split"))):
            raise ValueError("Frozen image identifiers do not agree")
        if (record.get("width"), record.get("height")) != (
            image["image_width"], image["image_height"]):
            raise ValueError("Frozen image dimensions disagree")
        filename = image["filename"]
        if Path(filename).name != filename or filename in (".", ".."):
            raise ValueError("Invalid image filename")
        asset_id = image["asset_id"]
        url = record.get("source_url", "")
        validate_download_url(url, asset_id)
        data = retrieve(url)
        # Image.verify() checks file structure and does not modify original bytes.
        import io
        with Image.open(io.BytesIO(data)) as decoded:
            decoded.verify()
        with Image.open(io.BytesIO(data)) as decoded:
            if decoded.size != (image["image_width"], image["image_height"]):
                raise RuntimeError("Downloaded image dimensions differ from frozen source")
        target = destination / filename
        if target.exists():
            raise RuntimeError("Refusing to overwrite an existing V30 source-image file")
        target.write_bytes(data)
        digest = hashlib.sha256(data).hexdigest()
        hashes[key] = {"filename": filename, "asset_id": asset_id,
                       "split": image["split"], "sha256": digest,
                       "size_bytes": len(data)}
        print(f"Fetched {filename}: {len(data)} bytes (sha256 {digest})", flush=True)
    return hashes


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--destination", type=Path, required=True)
    p.add_argument("--manifest", type=Path,
                   default=RESEARCH / "V30_FROZEN_TARGETS_2026-11-22.json")
    p.add_argument("--baseline", type=Path,
                   default=RESEARCH / "V30_BASELINE_PREFLIGHT_ACTUAL_2026-11-22.json")
    p.add_argument("--hashes-output", type=Path, required=True)
    args = p.parse_args()
    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    preflight = json.loads(args.baseline.read_text(encoding="utf-8"))
    hashes = fetch_images(manifest, preflight, args.destination)
    args.hashes_output.parent.mkdir(parents=True, exist_ok=True)
    args.hashes_output.write_text(json.dumps({
        "schema_version": "seer-ppe/v30-cloud-download-hashes/v0.30",
        "source_images": hashes,
        "source_hashes_independently_available": False,
        "no_test_accessed": True
    }, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
