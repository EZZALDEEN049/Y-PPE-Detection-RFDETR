#!/usr/bin/env python3
"""Controlled Stage 5 YOLO11m trainer.

This script trains only. It intentionally does not evaluate the held-out test split.
The common test evaluator is a separate later gate.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import platform
import random
import subprocess
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import torch
from ultralytics import YOLO, __version__ as ultralytics_version

EXPECTED = {
    "Y-PPE-h9-v2": "82669459c4c8b53535ee765321fa22277a1ef8d43695409ebb0d212764eb8b89",
    "Construction-PPE-h9-v2": "59469299ba67355dbcb0e725851f73d244a7ad6e93522d44601be3c8323d3c14",
}
RUN_PREFIX = {
    "Y-PPE-h9-v2": "Y",
    "Construction-PPE-h9-v2": "C",
}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def git_sha() -> str | None:
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
    except Exception:
        return None


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dataset", required=True, choices=sorted(EXPECTED))
    ap.add_argument("--dataset-root", required=True)
    ap.add_argument("--seed", required=True, type=int, choices=[17, 42, 2026])
    ap.add_argument("--batch-size", required=True, type=int)
    ap.add_argument("--device", default="0")
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--epochs", type=int, default=100)
    ap.add_argument("--imgsz", type=int, default=640)
    ap.add_argument("--output-root", required=True)
    args = ap.parse_args()

    if args.epochs != 100 or args.imgsz != 640:
        raise SystemExit("Stage 5 v1 primary protocol requires epochs=100 and imgsz=640")
    if args.batch_size < 1:
        raise SystemExit("batch-size must be a positive frozen integer")

    root = Path(args.dataset_root).resolve()
    manifest = root / "manifest.jsonl"
    data_yaml = root / "data.yaml"
    if not manifest.is_file() or not data_yaml.is_file():
        raise SystemExit("dataset-root must contain corrected Stage 4.5 manifest.jsonl and data.yaml")
    fp = sha256_file(manifest)
    if fp != EXPECTED[args.dataset]:
        raise SystemExit(f"Frozen dataset fingerprint mismatch: got {fp}, expected {EXPECTED[args.dataset]}")

    random.seed(args.seed)
    np.random.seed(args.seed)
    torch.manual_seed(args.seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(args.seed)

    run_id = f"{RUN_PREFIX[args.dataset]}_YOLO_s{args.seed}"
    out_root = Path(args.output_root).resolve()
    out_root.mkdir(parents=True, exist_ok=True)
    run_dir = out_root / run_id
    if run_dir.exists():
        raise SystemExit(f"Refusing to overwrite existing run directory: {run_dir}")

    meta = {
        "stage": 5,
        "status": "training_started",
        "run_id": run_id,
        "dataset": args.dataset,
        "dataset_fingerprint_sha256": fp,
        "model": "YOLO11m",
        "pretrained_checkpoint": "yolo11m.pt",
        "seed": args.seed,
        "epochs": 100,
        "resolution": 640,
        "batch_size": args.batch_size,
        "grad_accum_steps": None,
        "device_requested": args.device,
        "workers": args.workers,
        "primary_checkpoint_policy": "final_epoch",
        "test_evaluation_performed": False,
        "stochastic_online_augmentation": False,
        "early_stopping": False,
        "early_stopping_control": "patience=0; verified by Stage 5 preflight to map to infinity in installed Ultralytics",
        "optimizer_policy": "ultralytics_auto_record_from_logs",
        "started_at_utc": datetime.now(timezone.utc).isoformat(),
        "git_sha": git_sha(),
        "python": platform.python_version(),
        "torch": torch.__version__,
        "cuda_runtime": torch.version.cuda,
        "cuda_available": torch.cuda.is_available(),
        "gpu": torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,
        "ultralytics": ultralytics_version,
    }
    run_dir.mkdir(parents=True)
    (run_dir / "run_manifest_pre.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")

    model = YOLO("yolo11m.pt")
    model.train(
        data=str(data_yaml),
        epochs=100,
        imgsz=640,
        batch=args.batch_size,
        device=args.device,
        workers=args.workers,
        seed=args.seed,
        deterministic=True,
        pretrained=True,
        patience=0,
        val=True,
        optimizer="auto",
        project=str(run_dir),
        name="train",
        exist_ok=False,
        save=True,
        save_period=10,
        plots=True,
        cache=False,
        hsv_h=0.0,
        hsv_s=0.0,
        hsv_v=0.0,
        degrees=0.0,
        translate=0.0,
        scale=0.0,
        shear=0.0,
        perspective=0.0,
        flipud=0.0,
        fliplr=0.0,
        bgr=0.0,
        mosaic=0.0,
        mixup=0.0,
        cutmix=0.0,
        augmentations=[],
    )

    meta["status"] = "training_completed"
    meta["completed_at_utc"] = datetime.now(timezone.utc).isoformat()
    meta["test_evaluation_performed"] = False
    (run_dir / "run_manifest_post.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    print(json.dumps(meta, indent=2))


if __name__ == "__main__":
    main()
