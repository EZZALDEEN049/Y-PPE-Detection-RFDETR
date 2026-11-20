#!/usr/bin/env python3
"""SEER-PPE read-only source-image duplicate audit.

Dependencies: Pillow. Input must contain unique Roboflow Source image IDs and
explicit local paths (or uniquely matching <root>/<split>/<image_id>.* files).
Only Train/Valid are accepted. Test is intentionally excluded to keep it sealed.
Local paths must be under their declared split folder. No symlinks or traversal.
Results are research triage, NEVER authorization to score or modify images.
"""
import argparse
import hashlib
import json
import platform
import re
import shutil
import sys
import tempfile
from collections import Counter, defaultdict
from pathlib import Path

from PIL import Image, ImageOps, __version__ as pillow_version


def _sha(data):
    return hashlib.sha256(data).hexdigest()


def _resolve(root, item):
    """Resolve ONLY the declared Train/Valid Source ID, never arbitrary or Test paths.

    Local paths must start with the declared split directory. Symlinks and path
    traversal are forbidden to prevent accidental reads of protected Test bytes.
    """
    root = root.resolve()
    split = item["split"]
    folder = root / split
    if folder.is_symlink() or not folder.resolve().is_relative_to(root):
        raise ValueError("Split directory symlink or root escape forbidden")

    if item.get("local_path"):
        relative = Path(item["local_path"])
        if (relative.is_absolute() or ".." in relative.parts
                or not relative.parts or relative.parts[0] != split
                or any(part.lower() in {"test", "testing"} for part in relative.parts[:-1])):
            raise ValueError("Local path must remain under the declared Train/Valid split")
        candidate = root / relative
        cursor = root
        for part in relative.parts:
            cursor = cursor / part
            if cursor.is_symlink():
                raise ValueError("Symlink in Source path forbidden")
        path = candidate.resolve()
        if not path.is_relative_to(folder.resolve()):
            raise ValueError("Path escapes declared Train/Valid split")
        return path if path.is_file() else None

    # Never guess by original filename: different Sources may share filenames.
    # Search Source-ID-prefixed files only, rejecting symlinks and ambiguities.
    paths = []
    for candidate in folder.glob(item["image_id"] + ".*"):
        if candidate.is_symlink():
            raise ValueError("Symlink in Source path forbidden")
        path = candidate.resolve()
        if not path.is_relative_to(folder.resolve()):
            raise ValueError("Path escapes declared Train/Valid split")
        if path.is_file():
            paths.append(path)
    if len(paths) > 1:
        raise ValueError("Ambiguous Source ID in local files: " + item["image_id"])
    return paths[0] if paths else None


def _fingerprint(path):
    sha256 = _sha(path.read_bytes())
    with Image.open(path) as raw:
        rgb = ImageOps.exif_transpose(raw).convert("RGB")
        width, height = rgb.size
        pix_sha256 = _sha(f"RGB:{width}x{height}:".encode() + rgb.tobytes())
        reduced = rgb.convert("L").resize((9, 8), Image.Resampling.LANCZOS)
        values = list(reduced.tobytes())
        bits = 0
        for y in range(8):
            for x in range(8):
                bits = (bits << 1) | int(values[y * 9 + x] > values[y * 9 + x + 1])
    return {"bytes_sha256": sha256, "rgb_pixel_sha256": pix_sha256,
            "dhash64": f"{bits:016x}", "width": width, "height": height}


def audit(manifest, root):
    if not isinstance(manifest, dict) or not isinstance(manifest.get("images"), list):
        raise ValueError("Expected manifest object with images array")
    items = manifest["images"]
    if any(x.get("split") not in ("train", "valid") for x in items):
        raise ValueError("Test or unknown split is forbidden in this audit")
    if any(not isinstance(x.get("image_id"), str)
           or not re.fullmatch(r"[A-Za-z0-9_-]+", x["image_id"]) for x in items):
        raise ValueError("All Source image_id values must be safe alphanumeric IDs")
    if len({x["image_id"] for x in items}) != len(items):
        raise ValueError("Duplicate Source ID in manifest")
    counts = Counter(x["split"] for x in items)
    scanned, missing, failures = [], [], []
    for item in items:
        path = _resolve(root, item)
        if path is None:
            missing.append({"image_id": item["image_id"], "split": item["split"]})
            continue
        try:
            fp = _fingerprint(path)
            scanned.append({"image_id": item["image_id"], "filename": item.get("filename"),
                            "split": item["split"], **fp})
        except (OSError, ValueError) as ex:
            failures.append({"image_id": item["image_id"], "split": item["split"],
                             "error": str(ex)[:200]})
    by_split = {k: [x for x in scanned if x["split"] == k] for k in ("train", "valid")}
    exact_bytes, exact_pixels, near, closest = [], [], [], []
    train_by_bytes = defaultdict(list)
    train_by_pixels = defaultdict(list)
    for tr in by_split["train"]:
        train_by_bytes[tr["bytes_sha256"]].append(tr)
        train_by_pixels[tr["rgb_pixel_sha256"]].append(tr)
    for va in by_split["valid"]:
        for tr in train_by_bytes[va["bytes_sha256"]]:
            exact_bytes.append({"valid_id": va["image_id"], "train_id": tr["image_id"],
                                "evidence": "IDENTICAL_SHA256_RAW_BYTES"})
        for tr in train_by_pixels[va["rgb_pixel_sha256"]]:
            if tr["bytes_sha256"] != va["bytes_sha256"]:
                exact_pixels.append({"valid_id": va["image_id"], "train_id": tr["image_id"],
                                     "evidence": "IDENTICAL_RGB_PIXELS_AFTER_EXIF_ORIENTATION"})
        best = []
        for tr in by_split["train"]:
            dist = (int(va["dhash64"], 16) ^ int(tr["dhash64"], 16)).bit_count()
            candidate = {"valid_id": va["image_id"], "train_id": tr["image_id"],
                         "dhash_hamming": dist}
            if dist <= 8 and tr["rgb_pixel_sha256"] != va["rgb_pixel_sha256"]:
                near.append({**candidate, "status": "VISUAL_REVIEW_REQUIRED_NOT_PROVEN_DUPLICATE"})
            if len(best) < 3 or dist < best[-1]["dhash_hamming"]:
                best.append(candidate)
                best.sort(key=lambda x: (x["dhash_hamming"], x["train_id"]))
                best = best[:3]
        closest.append({"valid_id": va["image_id"], "top3_train": best})
    complete = not missing and not failures and counts == Counter({"train": 1625, "valid": 468})
    return {
        "schema_version": "seer-ppe/source-pixel-hash-audit/v0.1",
        "scope": "TRAIN_VALID_ONLY_TEST_NEVER_READ",
        "project": manifest.get("project"), "manifest_rows": len(items),
        "manifest_split_counts": dict(counts), "scanned_split_counts": {k: len(v) for k, v in by_split.items()},
        "missing_count": len(missing), "missing": missing,
        "decode_error_count": len(failures), "decode_errors": failures,
        "full_2093_coverage": complete,
        "method": {"bytes": "SHA-256 file bytes", "pixels": "SHA-256 over EXIF-oriented RGB size + bytes",
                   "near": "64-bit horizontal dHash, threshold <=8 for review queue only",
                   "pillow_version": pillow_version, "python_version": platform.python_version()},
        "exact_byte_matches": exact_bytes, "exact_decoded_pixel_matches_different_bytes": exact_pixels,
        "dhash_review_candidates": near, "nearest_train_for_each_scanned_valid": closest,
        "scoring_ready": False,
        "warnings": ["No Test data accessed", "dHash collisions and crops may yield false positives or negatives",
                     "Only source originals should be used, not derived augmented tiles",
                     "No independent human source-family adjudication or Person–PPE gold reference"],
    }


def self_test():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        for split in ("train", "valid"):
            (root / split).mkdir()
        original = Image.new("RGB", (32, 24))
        for y in range(24):
            for x in range(32):
                original.putpixel((x, y), ((x * 7 + y) % 256, (x * 2 + y * 3) % 256, (x * 5) % 256))
        original.save(root / "train" / "T.png")
        shutil.copyfile(root / "train" / "T.png", root / "valid" / "V1.png")
        original.save(root / "valid" / "V2.bmp")
        Image.new("RGB", (32, 24), (255, 0, 0)).save(root / "valid" / "V3.png")
        manifest = {"images": [{"image_id": "T", "split": "train"},
                               {"image_id": "V1", "split": "valid"},
                               {"image_id": "V2", "split": "valid"},
                               {"image_id": "V3", "split": "valid"}]}
        result = audit(manifest, root)
        assert len(result["exact_byte_matches"]) == 1
        assert len(result["exact_decoded_pixel_matches_different_bytes"]) == 1
        assert result["full_2093_coverage"] is False
        assert result["scoring_ready"] is False
        assert result["scope"] == "TRAIN_VALID_ONLY_TEST_NEVER_READ"
        try:
            audit({"images": [{"image_id": "bad", "split": "test"}]}, root)
            raise AssertionError("Test guard failed")
        except ValueError as exc:
            assert "forbidden" in str(exc)
        # Reject malformed IDs before any file access.
        try:
            audit({"images": [{"image_id": "../test/secret", "split": "train"}]}, root)
            raise AssertionError("Unsafe image ID guard failed")
        except ValueError as exc:
            assert "alphanumeric" in str(exc)
        # Reject a declared Train Source pointing to Valid or Test image bytes.
        for wrong_path in ("valid/V1.png", "test/secret.png"):
            try:
                audit({"images": [{"image_id": "T", "split": "train",
                                   "local_path": wrong_path}]}, root)
                raise AssertionError("Cross-split path guard failed")
            except ValueError as exc:
                assert "split" in str(exc)
        # Reject file symlinks which could silently cross split boundaries.
        (root / "train" / "LINK.png").symlink_to(root / "valid" / "V1.png")
        try:
            audit({"images": [{"image_id": "LINK", "split": "train"}]}, root)
            raise AssertionError("Symlink guard failed")
        except ValueError as exc:
            assert "Symlink" in str(exc)
    print("SOURCE_PIXEL_HASH_AUDIT_SELF_TEST_PASS")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--manifest", type=Path, help="JSON Source-ID image manifest")
    ap.add_argument("--root", type=Path, help="Root containing split/Source-ID.ext or explicit relative local_path")
    ap.add_argument("--output", type=Path, help="Write a JSON audit record")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        self_test()
        return 0
    if not (args.manifest and args.root and args.output):
        ap.error("--manifest, --root and --output are all required")
    result = audit(json.loads(args.manifest.read_text(encoding="utf-8")), args.root.resolve())
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"full_2093_coverage": result["full_2093_coverage"],
                      "exact_byte_matches": len(result["exact_byte_matches"]),
                      "exact_pixel_matches": len(result["exact_decoded_pixel_matches_different_bytes"]),
                      "dhash_review_candidates": len(result["dhash_review_candidates"]),
                      "missing": result["missing_count"], "decode_errors": result["decode_error_count"],
                      "scoring_ready": False}))
    return 0 if result["full_2093_coverage"] else 2


if __name__ == "__main__":
    sys.exit(main())
