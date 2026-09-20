#!/usr/bin/env python3
"""Freeze Stage 5 execution parameters from an actual Colab GPU report.

This script does not train a model and does not read held-out test images or metrics.
The selection rule is deterministic and depends only on GPU VRAM and BF16 support.
It exists to prevent performance-driven batch/precision changes after experiments start.
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
    if data.get("frozen_fingerprints") != EXPECTED_FINGERPRINTS:
        raise SystemExit("Corrected Stage 4.5 dataset fingerprints do not match the frozen Stage 5 identity")

    vram = float(gpu["vram_gib"])
    if vram < 10.0:
        raise SystemExit(f"GPU VRAM {vram:.2f} GiB is below the conservative Stage 5 minimum (10 GiB)")

    # Deterministic conservative policy. No model metric or validation/test outcome is consulted.
    # RF-DETR effective batch is fixed to 8 via gradient accumulation across all tiers.
    if vram < 20.0:
        yolo_batch = 4
        rf_batch, rf_grad_accum = 1, 8
    elif vram < 35.0:
        yolo_batch = 8
        rf_batch, rf_grad_accum = 2, 4
    else:
        yolo_batch = 16
        rf_batch, rf_grad_accum = 4, 2

    rf_amp_dtype = "bf16" if bool(gpu.get("bf16_supported")) else "fp16"

    report = {
        "status": "RESOURCE_PARAMETERS_FROZEN",
        "frozen_at_utc": datetime.now(timezone.utc).isoformat(),
        "selection_policy": "stage5_colab_resource_policy_v1_vram_only_no_performance_tuning",
        "selection_inputs": {
            "gpu_model": gpu.get("gpu"),
            "vram_gib": vram,
            "compute_capability": gpu.get("compute_capability"),
            "bf16_supported": bool(gpu.get("bf16_supported")),
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
            "physical_batch_size": yolo_batch,
            "workers": 2,
            "amp": True,
            "precision_policy": "explicit Ultralytics CUDA AMP enabled",
            "gradient_accumulation_control": "framework-native optimizer accumulation; do not change after first run",
        },
        "rfdetr_small": {
            "physical_batch_size": rf_batch,
            "grad_accum_steps": rf_grad_accum,
            "effective_batch_size_single_gpu": rf_batch * rf_grad_accum,
            "workers": 2,
            "amp_dtype": rf_amp_dtype,
            "use_ema": True,
            "primary_checkpoint": "last_ema.pth",
        },
        "scientific_guards": {
            "model_training_performed_by_this_script": False,
            "held_out_test_evaluation_performed_by_this_script": False,
            "parameters_selected_from_model_performance": False,
            "same_parameters_per_architecture_across_both_datasets": True,
        },
    }

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    print("\nRESOURCE_PARAMETER_FREEZE_COMPLETE")


if __name__ == "__main__":
    main()
