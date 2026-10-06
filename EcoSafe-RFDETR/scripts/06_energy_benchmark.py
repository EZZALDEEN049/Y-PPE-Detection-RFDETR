"""Measure model inference energy on a fixed NVIDIA GPU using NVML.
Run only on the dedicated experiment machine after warm-up.
"""
import argparse
import json
import time
from pathlib import Path

import numpy as np
import pynvml


def sample_power(handle):
    return pynvml.nvmlDeviceGetPowerUsage(handle) / 1000.0


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--out', required=True)
    p.add_argument('--frames', type=int, required=True)
    p.add_argument('--start-time', type=float, required=True)
    p.add_argument('--end-time', type=float, required=True)
    p.add_argument('--power-log', required=True, help='CSV/JSONL power samples generated during inference')
    a = p.parse_args()

    samples = []
    for line in Path(a.power_log).read_text().splitlines():
        if not line.strip():
            continue
        t, w = line.split(',')[:2]
        samples.append((float(t), float(w)))
    samples = [(t, w) for t, w in samples if a.start_time <= t <= a.end_time]
    if len(samples) < 2:
        raise SystemExit('Insufficient power samples inside inference interval')
    ts = np.array([x[0] for x in samples])
    pw = np.array([x[1] for x in samples])
    energy_j = float(np.trapz(pw, ts))
    result = {
        'frames': a.frames,
        'duration_s': a.end_time - a.start_time,
        'energy_j': energy_j,
        'j_per_frame': energy_j / a.frames,
        'avg_power_w': float(pw.mean()),
    }
    Path(a.out).write_text(json.dumps(result, indent=2))
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
