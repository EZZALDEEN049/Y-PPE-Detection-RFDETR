#!/usr/bin/env python3
"""Freeze Stage 5 Colab execution parameters before any model training.

The policy is intentionally conservative and performance-independent. It uses the
actual attached GPU only as a feasibility gate, not to tune scientific outcomes.
No dataset image, prediction, validation score, or held-out test metric is read.
"""
from __future__ import annotations

import argparse
import importlib.metadata as md
import json
import platform
import subprocess
from datetime import datetime, timezone
from pathlib import Path

import torch

EXPECTED_FINGERPRINTS = {
    "Y-PPE-h9-v2": "82c08766d5c5e50e93d41d21c4751fd686a3932ea6a8cb24ffd2838d9e30fba8",
    "Construction-PPE-h9-v2": "59469299ba67355dbcb0e725851f73d244a7ad6e93522d44601be3c8323d3c14",
}


def pkg(name: str) -> str | None:
    try:
        return md.version(name)
    except md.PackageNotFoundError:
        return None


def git_sha(repo: Path) -> str | None:
    try:
        return subprocess.check_output(["git", "-C", str(repo), "rev-parse", "HEAD"], text=True).strip()
    except Exception:
        return None


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--materialization-summary", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    if not torch.cuda.is_available():
        raise SystemExit("CUDA GPU required for Stage 5 resource freeze")
    if torch.cuda.device_count() != 1:
        raise SystemExit(f"Stage 5 Colab policy requires exactly one GPU; found {torch.cuda.device_count()}")

    props = torch.cuda.get_device_properties(0)
    vram_gib = props.total_memory / 1024**3
    if vram_gib < 14.0:
        raise SystemExit(f"GPU VRAM {vram_gib:.2f} GiB is below conservative Stage 5 minimum 14 GiB")

    summary = json.loads(Path(args.materialization_summary).read_text(encoding="utf-8"))
    if summary.get("status") != "PASS":
        raise SystemExit("Frozen dataset materialization did not PASS")
    if summary.get("frozen_fingerprints") != EXPECTED_FINGERPRINTS:
        raise SystemExit("Frozen dataset fingerprints do not match Stage 5 policy")

    # Fixed values: these do not depend on model accuracy, validation behavior, or test results.
    # They are intentionally conservative for the common free-Colab single-GPU envelope.
    policy = {
        "status": "FROZEN_BEFORE_TRAINING",
        "frozen_at_utc": datetime.now(timezone.utc).isoformat(),
        "selection_basis": "hardware feasibility only; no model or test performance inspected",
        "repo_git_sha": git_sha(Path(args.repo)),
        "hardware": {
            "gpu": torch.cuda.get_device_name(0),
            "gpu_count": 1,
            "vram_gib": round(vram_gib, 3),
            "compute_capability": f"{props.major}.{props.minor}",
            "cuda_runtime": torch.version.cuda,
            "cudnn": torch.backends.cudnn.version(),
        },
        "software": {
            "python": platform.python_version(),
            "torch": torch.__version__,
            "torchvision": pkg("torchvision"),
            "ultralytics": pkg("ultralytics"),
            "rfdetr": pkg("rfdetr"),
            "roboflow": pkg("roboflow"),
            "PyYAML": pkg("PyYAML"),
        },
        "datasets": {
            "fingerprints": EXPECTED_FINGERPRINTS,
            "counts": summary.get("frozen_counts"),
        },
        "yolo11m": {
            "physical_batch_size": 8,
            "grad_accum_steps": None,
            "workers": 2,
            "amp": True,
            "resolution": 640,
            "epochs": 100,
            "checkpoint_policy": "final_epoch_ema_last_pt",
        },
        "rfdetr_small": {
            "physical_batch_size": 1,
            "grad_accum_steps": 16,
            "effective_batch_size": 16,
            "workers": 2,
            "amp_dtype": "fp16",
            "resolution": 640,
            "epochs": 100,
            "checkpoint_policy": "final_epoch_ema_last_ema_pth",
        },
        "held_out_test_evaluation_performed": False,
        "model_training_performed_before_freeze": False,
    }

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(policy, indent=2), encoding="utf-8")
    print(json.dumps(policy, indent=2))
    print("RESOURCE_PARAMETER_FREEZE_COMPLETE")


if __name__ == "__main__":
    main()
