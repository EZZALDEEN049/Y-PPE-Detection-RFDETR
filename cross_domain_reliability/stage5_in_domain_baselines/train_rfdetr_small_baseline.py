#!/usr/bin/env python3
"""Controlled Stage 5 RF-DETR Small trainer.

Training only: held-out test evaluation is intentionally disabled.
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
import rfdetr
from rfdetr import RFDETRSmall

EXPECTED = {
    "Y-PPE-h9": "db49295a0ef2c9eec73b14c620966ed00bf12dac253866b65bab9b50af9db896",
    "Construction-PPE-h9": "bd706ae34aa77507f119a9a4d5cd443d4cb84ee6cd2020b9b8ee6e086350880e",
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
    ap.add_argument("--grad-accum-steps", required=True, type=int)
    ap.add_argument("--device", default="cuda")
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--epochs", type=int, default=100)
    ap.add_argument("--resolution", type=int, default=640)
    ap.add_argument("--output-root", required=True)
    args = ap.parse_args()

    if args.epochs != 100 or args.resolution != 640:
        raise SystemExit("Stage 5 v1 primary protocol requires epochs=100 and resolution=640")
    if args.batch_size < 1 or args.grad_accum_steps < 1:
        raise SystemExit("batch-size and grad-accum-steps must be positive frozen integers")
    if 640 % 32 != 0:
        raise SystemExit("RF-DETR Small controlled resolution must be divisible by its 32-pixel block size")

    root = Path(args.dataset_root).resolve()
    manifest = root / "manifest.jsonl"
    data_yaml = root / "data.yaml"
    if not manifest.is_file() or not data_yaml.is_file():
        raise SystemExit("dataset-root must contain manifest.jsonl and data.yaml from Stage 4")
    fp = sha256_file(manifest)
    if fp != EXPECTED[args.dataset]:
        raise SystemExit(f"Frozen dataset fingerprint mismatch: got {fp}, expected {EXPECTED[args.dataset]}")

    random.seed(args.seed)
    np.random.seed(args.seed)
    torch.manual_seed(args.seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(args.seed)

    run_id = f"{args.dataset.replace('-h9','').replace('-','_')}_RFDETR_s{args.seed}"
    out_root = Path(args.output_root).resolve()
    out_root.mkdir(parents=True, exist_ok=True)
    run_dir = out_root / run_id
    if run_dir.exists():
        raise SystemExit(f"Refusing to overwrite existing run directory: {run_dir}")
    run_dir.mkdir(parents=True)

    meta = {
        "stage": 5,
        "status": "training_started",
        "run_id": run_id,
        "dataset": args.dataset,
        "dataset_fingerprint_sha256": fp,
        "model": "RF-DETR Small",
        "seed": args.seed,
        "epochs": 100,
        "resolution": 640,
        "batch_size": args.batch_size,
        "grad_accum_steps": args.grad_accum_steps,
        "effective_batch_size_single_gpu": args.batch_size * args.grad_accum_steps,
        "device_requested": args.device,
        "workers": args.workers,
        "primary_checkpoint_policy": "final_epoch_weight_policy_to_be_locked_before_first_full_run",
        "test_evaluation_performed": False,
        "stochastic_online_augmentation": False,
        "scale_jitter": False,
        "early_stopping": False,
        "use_ema": True,
        "optimizer_policy": "rfdetr_native_finetuning_recipe_record_from_checkpoint_and_logs",
        "started_at_utc": datetime.now(timezone.utc).isoformat(),
        "git_sha": git_sha(),
        "python": platform.python_version(),
        "torch": torch.__version__,
        "cuda_runtime": torch.version.cuda,
        "cuda_available": torch.cuda.is_available(),
        "gpu": torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,
        "rfdetr": getattr(rfdetr, "__version__", "unknown"),
    }
    (run_dir / "run_manifest_pre.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")

    model = RFDETRSmall()
    model.train(
        dataset_dir=str(root),
        epochs=100,
        batch_size=args.batch_size,
        grad_accum_steps=args.grad_accum_steps,
        resolution=640,
        device=args.device,
        num_workers=args.workers,
        seed=args.seed,
        output_dir=str(run_dir / "train"),
        aug_config={},
        scale_jitter=False,
        early_stopping=False,
        use_ema=True,
        run_test=False,
        tensorboard=True,
    )

    meta["status"] = "training_completed"
    meta["completed_at_utc"] = datetime.now(timezone.utc).isoformat()
    meta["test_evaluation_performed"] = False
    (run_dir / "run_manifest_post.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    print(json.dumps(meta, indent=2))


if __name__ == "__main__":
    main()
