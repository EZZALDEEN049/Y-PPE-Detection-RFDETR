#!/usr/bin/env python3
"""Freeze Stage 5 execution parameters from an actual Colab GPU report.

This script does not train a model and does not read held-out test images or metrics.
The execution parameters are fixed in advance and the actual GPU is used only as a
feasibility/identity gate. This prevents performance-driven resource changes after
experiments start.
"""
from __future__ import annotations

import argparse
import importlib.metadata as md
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

EXPECTED_FINGERPRINTS = {
    "Y-PPE-h9-v2": "82c08766d5c5e50e93d41d21c4751fd686a3932ea6a8cb24ffd2838d9e30fba8",
    "Construction-PPE-h9-v2": "59469299ba67355dbcb0e725851f73d244a7ad6e93522d44601be3c8323d3c14",
}


def version(name: str) -> str | None:
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
    ap.add_argument("--gpu-report", required=True)
    ap.add_argument("--materialization-summary", required=True)
    ap.add_argument("--repo", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    gpu = json.loads(Path(args.gpu_report).read_text(encoding="utf-8"))
    data = json.loads(Path(args.materialization_summary).read_text(encoding="utf-8"))
    repo = Path(args.repo).resolve()

    if not gpu.get("cuda_available"):
        raise SystemExit("CUDA is not available; resource parameters cannot be frozen")
    if int(gpu.get("gpu_count", 0)) != 1:
        raise SystemExit(f"Exactly one GPU is required; found {gpu.get('gpu_count')}")
    if data.get("frozen_fingerprints") != EXPECTED_FINGERPRINTS:
        raise SystemExit("Corrected Stage 4.5 dataset fingerprints do not match the frozen Stage 5 identity")

    vram = float(gpu["vram_gib"])
    if vram < 14.0:
        raise SystemExit(f"GPU VRAM {vram:.2f} GiB is below the conservative Stage 5 minimum (14 GiB)")

    report = {
        "status": "FROZEN_BEFORE_TRAINING",
        "frozen_at_utc": datetime.now(timezone.utc).isoformat(),
        "selection_policy": "stage5_colab_resource_policy_v2_fixed_before_training_no_performance_tuning",
        "selection_basis": "hardware feasibility and identity only; no model, validation, or held-out test performance inspected",
        "selection_inputs": {
            "gpu_model": gpu.get("gpu"),
            "gpu_count": gpu.get("gpu_count"),
            "vram_gib": vram,
            "compute_capability": gpu.get("compute_capability"),
            "bf16_supported": bool(gpu.get("bf16_supported")),
            "cuda_runtime": gpu.get("cuda_runtime"),
            "cudnn": gpu.get("cudnn"),
        },
        "git_sha": git_sha(repo),
        "software": {
            "torch": version("torch"),
            "torchvision": version("torchvision"),
            "ultralytics": version("ultralytics"),
            "rfdetr": version("rfdetr"),
            "roboflow": version("roboflow"),
            "PyYAML": version("PyYAML"),
        },
        "datasets": {
            "fingerprints": data["frozen_fingerprints"],
            "counts": data.get("frozen_counts"),
        },
        "yolo11m": {
            "physical_batch_size": 8,
            "grad_accum_steps": None,
            "workers": 2,
            "amp": True,
            "precision_policy": "explicit Ultralytics CUDA AMP enabled",
            "resolution": 640,
            "epochs": 100,
            "checkpoint_policy": "final_epoch_ema_last_pt",
        },
        "rfdetr_small": {
            "physical_batch_size": 1,
            "grad_accum_steps": 16,
            "effective_batch_size_single_gpu": 16,
            "workers": 2,
            "amp_dtype": "fp16",
            "use_ema": True,
            "resolution": 640,
            "epochs": 100,
            "primary_checkpoint": "last_ema.pth",
        },
        "scientific_guards": {
            "model_training_performed_by_this_script": False,
            "held_out_test_evaluation_performed_by_this_script": False,
            "parameters_selected_from_model_performance": False,
            "same_parameters_per_architecture_across_both_datasets": True,
        },
        "model_training_performed_before_freeze": False,
        "held_out_test_evaluation_performed": False,
    }

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    print("\nRESOURCE_PARAMETER_FREEZE_COMPLETE")


if __name__ == "__main__":
    main()
