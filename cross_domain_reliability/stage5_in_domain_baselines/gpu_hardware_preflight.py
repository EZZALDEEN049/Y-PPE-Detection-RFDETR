#!/usr/bin/env python3
"""Stage 5 hardware-only GPU preflight.

This script performs no model training and does not access any dataset image or label.
It records the GPU/driver/CUDA-visible hardware state for the self-hosted runner.
"""
from __future__ import annotations

import json
import os
import platform
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path


def cmd(args: list[str]) -> str:
    return subprocess.check_output(args, text=True, stderr=subprocess.STDOUT).strip()


def main() -> None:
    out_dir = Path(os.environ.get("STAGE5_PREFLIGHT_OUT", "stage5_gpu_hardware_preflight"))
    out_dir.mkdir(parents=True, exist_ok=True)

    if shutil.which("nvidia-smi") is None:
        raise SystemExit("nvidia-smi not found: the runner is not ready for Stage 5 GPU execution")

    query = cmd([
        "nvidia-smi",
        "--query-gpu=index,name,uuid,memory.total,driver_version,pstate,temperature.gpu",
        "--format=csv,noheader,nounits",
    ])
    rows = []
    for line in query.splitlines():
        parts = [x.strip() for x in line.split(",")]
        if len(parts) != 7:
            raise SystemExit(f"Unexpected nvidia-smi query row: {line}")
        rows.append({
            "index": int(parts[0]),
            "name": parts[1],
            "uuid": parts[2],
            "memory_total_mib": int(parts[3]),
            "driver_version": parts[4],
            "pstate": parts[5],
            "temperature_c": int(parts[6]),
        })

    if len(rows) != 1:
        raise SystemExit(f"Stage 5 v1 expects exactly one visible GPU; found {len(rows)}")

    gpu = rows[0]
    if gpu["memory_total_mib"] < 15000:
        raise SystemExit(
            f"GPU VRAM is below the Stage 5 minimum preflight gate: {gpu['memory_total_mib']} MiB < 15000 MiB"
        )

    report = {
        "stage": 5,
        "preflight": "self_hosted_gpu_hardware",
        "status": "PASS",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "hostname": platform.node(),
        "platform": platform.platform(),
        "python": platform.python_version(),
        "runner_name": os.environ.get("RUNNER_NAME"),
        "runner_os": os.environ.get("RUNNER_OS"),
        "runner_arch": os.environ.get("RUNNER_ARCH"),
        "gpu_count": 1,
        "gpu": gpu,
        "minimum_vram_gate_mib": 15000,
        "nvidia_smi_full": cmd(["nvidia-smi"]),
        "note": "Hardware-only gate. No package installation, dataset access, training, validation, or test evaluation was performed.",
    }

    (out_dir / "gpu_hardware_preflight.json").write_text(
        json.dumps(report, indent=2), encoding="utf-8"
    )
    (out_dir / "nvidia_smi.txt").write_text(report["nvidia_smi_full"] + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
