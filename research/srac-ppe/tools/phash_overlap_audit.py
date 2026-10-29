#!/usr/bin/env python3
"""Read-only pHash cross-split screening for a YOLO-style ZIP.

This script emits only *candidate counts* by default. pHash distance does NOT
prove duplication; visually adjudicate individual candidates offline.
Never call its output a validated leakage count without provenance review.

Requirements: pillow, numpy, scipy.
"""
import argparse
import json
from io import BytesIO
from itertools import combinations
from pathlib import Path
from zipfile import ZipFile

import numpy as np
from PIL import Image
from scipy.fftpack import dct


def phash64(data: bytes) -> int:
    im = Image.open(BytesIO(data)).convert("L")
    ar = np.array(im.resize((32, 32), Image.Resampling.LANCZOS), dtype=np.float32)
    lo = dct(dct(ar, axis=0, norm="ortho"), axis=1, norm="ortho")[:8, :8]
    median = float(np.median(lo.ravel()[1:]))
    bits = np.packbits((lo > median).ravel().astype(np.uint8))
    return int.from_bytes(bits.tobytes(), "big")


def audit(zip_path, cutoffs=(4, 6, 8, 10, 12), show_pairs=False):
    hashes = {"train": [], "valid": [], "test": []}
    with ZipFile(zip_path) as archive:
        for name in archive.namelist():
            seg = name.split("/")
            if len(seg) != 3 or seg[0] not in hashes or seg[1] != "images":
                continue
            if Path(name).suffix.lower() not in (".jpg", ".jpeg", ".png", ".webp"):
                continue
            hashes[seg[0]].append((name, phash64(archive.read(name))))
    result = {"method": "32x32 grayscale LANCZOS, orthonormal DCT, 8x8 median pHash",
              "limitations": "Candidate screening only; no validated scene leakage inference",
              "image_counts": {k: len(v) for k, v in hashes.items()},
              "pair_counts": {}}
    if show_pairs:
        result["candidates_at_max_cutoff"] = {}
    for a, b in combinations(("train", "valid", "test"), 2):
        name = a + "-" + b
        thresholds = {str(t): 0 for t in cutoffs}
        candidates = []
        for path_a, hash_a in hashes[a]:
            for path_b, hash_b in hashes[b]:
                hamming = (hash_a ^ hash_b).bit_count()
                for threshold in cutoffs:
                    if hamming <= threshold:
                        thresholds[str(threshold)] += 1
                if show_pairs and hamming <= max(cutoffs):
                    candidates.append({"distance": hamming, "image_a": path_a, "image_b": path_b})
        result["pair_counts"][name] = thresholds
        if show_pairs:
            result["candidates_at_max_cutoff"][name] = sorted(candidates, key=lambda x: x["distance"])
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("archive", type=Path)
    parser.add_argument("--show-pairs", action="store_true",
                        help="Print image filenames for manual adjudication; may contain sensitive metadata")
    args = parser.parse_args()
    print(json.dumps(audit(args.archive, show_pairs=args.show_pairs), indent=2))


if __name__ == "__main__":
    main()
