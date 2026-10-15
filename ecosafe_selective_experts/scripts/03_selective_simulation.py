#!/usr/bin/env python3
"""Sweep a routing score and report safety/compute trade-offs.

Input is a CSV containing per-image primary and secondary safety FN counts plus a
continuous routing score. The score must be produced using development/calibration
data only when thresholds are selected.
"""

from __future__ import annotations

import argparse
import csv
import numpy as np


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--input", required=True)
    p.add_argument("--score-column", required=True)
    p.add_argument("--out", required=True)
    p.add_argument("--steps", type=int, default=101)
    args = p.parse_args()

    rows = list(csv.DictReader(open(args.input, newline="", encoding="utf-8")))
    if not rows:
        raise SystemExit("empty input")

    scores = np.array([float(r[args.score_column]) for r in rows], dtype=float)
    gt = np.array([int(r["gt_safety_objects"]) for r in rows], dtype=int)
    pfn = np.array([int(r["primary_safety_fn"]) for r in rows], dtype=int)
    sfn = np.array([int(r["secondary_safety_fn"]) for r in rows], dtype=int)

    lo, hi = float(scores.min()), float(scores.max())
    thresholds = np.linspace(lo, hi, args.steps)
    out_rows = []

    for t in thresholds:
        escalate = scores >= t
        final_fn = np.where(escalate, sfn, pfn)
        total_gt = int(gt.sum())
        recall = 1.0 - float(final_fn.sum()) / total_gt if total_gt else float("nan")
        rate = float(escalate.mean())
        out_rows.append({
            "threshold": float(t),
            "escalation_rate": rate,
            "expert_executions_per_image": 1.0 + rate,
            "safety_false_negatives": int(final_fn.sum()),
            "violation_recall": recall,
        })

    fields = list(out_rows[0])
    with open(args.out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(out_rows)

    print(f"SIMULATION_COMPLETE thresholds={len(out_rows)}")
    print(args.out)


if __name__ == "__main__":
    main()
