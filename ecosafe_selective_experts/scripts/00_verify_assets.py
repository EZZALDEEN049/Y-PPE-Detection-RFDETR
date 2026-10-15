#!/usr/bin/env python3
"""Verify the six frozen primary checkpoints before any EcoSafe execution."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

EXPECTED = {
    "Y_YOLO_s17": ("b5c54704553a6bbc900b8ac37735ee1040025a3c685dcd3717c4490d107bbee5", 40534380),
    "Y_YOLO_s42": ("3ec0b396ae344361a9e000683891aa88dd92ef9a6edff07829243f95bf6eaf64", 40534380),
    "Y_YOLO_s2026": ("c1ab6209e26aa461ef2833889c85d8edb8ffac6de70348117b0923b80939c23e", 40534572),
    "C_YOLO_s17": ("daef1d3841af76e0d3c801f8fd7a41d4713e465617b09b2e18d5fe67e5eb46c4", 40515820),
    "C_YOLO_s42": ("868b533722848a6885909391daabf52d7bd189cca4fc1e8d82fbe0f4c03869a1", 40515820),
    "C_YOLO_s2026": ("f1f160d2f1e84b8641872adb01d10b6c9d3b736a53b7ec5775333eef30f88bb1", 40515884),
}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--stage5-root", required=True)
    args = p.parse_args()

    root = Path(args.stage5_root)
    failures = []
    for run_id, (expected_hash, expected_size) in EXPECTED.items():
        path = root / run_id / "train" / "weights" / "last.pt"
        if not path.exists():
            failures.append(f"{run_id}: missing {path}")
            continue
        size = path.stat().st_size
        digest = sha256(path)
        ok = size == expected_size and digest == expected_hash
        print(f"{run_id}: size={size} sha256={digest} status={'PASS' if ok else 'FAIL'}")
        if not ok:
            failures.append(run_id)

    if failures:
        raise SystemExit("CHECKPOINT_LOCK_FAILED: " + "; ".join(failures))
    print("CHECKPOINT_LOCK_PASS")


if __name__ == "__main__":
    main()
