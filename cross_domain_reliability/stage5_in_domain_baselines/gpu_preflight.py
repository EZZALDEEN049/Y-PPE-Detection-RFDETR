#!/usr/bin/env python3
"""Stage 5 NVIDIA GPU preflight.

Runs no training and touches no dataset/test image. It records the execution
hardware/software environment that must be frozen before the first full
harmonized in-domain baseline run.
"""

from __future__ import annotations

import argparse
import json
import os
import platform
import subprocess
from pathlib import Path

import torch


def cmd_text(args: list[str]) -> str | None:
    try:
        p = subprocess.run(args, check=True, capture_output=True, text=True)
        return p.stdout.strip()
    except Exception:
        return None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True, help="Output JSON path")
    args = ap.parse_args()

    report: dict[str, object] = {
        "status": "PASS" if torch.cuda.is_available() else "FAIL_NO_CUDA",
        "python": platform.python_version(),
        "platform": platform.platform(),
        "torch": torch.__version__,
        "torch_cuda_runtime": torch.version.cuda,
        "cuda_available": torch.cuda.is_available(),
        "cudnn_version": torch.backends.cudnn.version(),
        "git_sha": cmd_text(["git", "rev-parse", "HEAD"]),
        "nvidia_smi": cmd_text([
            "nvidia-smi",
            "--query-gpu=name,uuid,driver_version,memory.total,compute_cap",
            "--format=csv,noheader,nounits",
        ]),
        "environment": {
            "CUDA_VISIBLE_DEVICES": os.environ.get("CUDA_VISIBLE_DEVICES"),
        },
        "gpus": [],
        "note": "No model training and no held-out test evaluation are performed by this preflight.",
    }

    if torch.cuda.is_available():
        gpus = []
        for idx in range(torch.cuda.device_count()):
            prop = torch.cuda.get_device_properties(idx)
            torch.cuda.set_device(idx)
            total = int(prop.total_memory)
            free, total_runtime = torch.cuda.mem_get_info(idx)
            gpu = {
                "index": idx,
                "name": prop.name,
                "total_memory_bytes": total,
                "free_memory_bytes_at_preflight": int(free),
                "runtime_total_memory_bytes": int(total_runtime),
                "compute_capability": f"{prop.major}.{prop.minor}",
                "bf16_supported": bool(torch.cuda.is_bf16_supported()),
                "tf32_matmul_allowed": bool(torch.backends.cuda.matmul.allow_tf32),
            }
            # Small allocation/compute sanity check only; not a model benchmark.
            x = torch.randn((1024, 1024), device=f"cuda:{idx}", dtype=torch.float32)
            y = x @ x
            torch.cuda.synchronize(idx)
            gpu["basic_cuda_compute_ok"] = bool(torch.isfinite(y).all().item())
            del x, y
            torch.cuda.empty_cache()
            gpus.append(gpu)
        report["gpus"] = gpus

    # Record package versions from import metadata, including RF-DETR whose module
    # namespace may not expose __version__.
    try:
        from importlib.metadata import version
        report["packages"] = {
            "rfdetr": version("rfdetr"),
            "ultralytics": version("ultralytics"),
            "torch": version("torch"),
            "torchvision": version("torchvision"),
            "numpy": version("numpy"),
            "PyYAML": version("PyYAML"),
        }
    except Exception as e:
        report["package_version_error"] = repr(e)

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if torch.cuda.is_available() else 2


if __name__ == "__main__":
    raise SystemExit(main())
