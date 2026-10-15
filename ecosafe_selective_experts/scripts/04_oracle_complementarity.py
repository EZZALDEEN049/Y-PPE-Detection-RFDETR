#!/usr/bin/env python3
"""Quantify whether two frozen experts are complementary enough to justify routing.

This is the first scientific GO/NO-GO gate for the selective-expert extension.
It consumes a per-image table produced by 02_build_router_dataset.py.
"""

from __future__ import annotations

import argparse
import csv
import math


def recall(total_gt, total_fn):
    return 1.0 - total_fn / total_gt if total_gt else math.nan


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--input", required=True)
    args = p.parse_args()

    rows = list(csv.DictReader(open(args.input, newline="", encoding="utf-8")))
    if not rows:
        raise SystemExit("empty input")

    gt = [int(r["gt_safety_objects"]) for r in rows]
    pfn = [int(r["primary_safety_fn"]) for r in rows]
    sfn = [int(r["secondary_safety_fn"]) for r in rows]

    total_gt = sum(gt)
    p_total = sum(pfn)
    s_total = sum(sfn)
    oracle_total = sum(min(a, b) for a, b in zip(pfn, sfn))

    secondary_better = sum(b < a for a, b in zip(pfn, sfn))
    primary_better = sum(a < b for a, b in zip(pfn, sfn))
    tied = len(rows) - secondary_better - primary_better

    primary_recall = recall(total_gt, p_total)
    secondary_recall = recall(total_gt, s_total)
    oracle_recall = recall(total_gt, oracle_total)
    best_single = max(primary_recall, secondary_recall)
    oracle_gain = oracle_recall - best_single

    print("COMPLEMENTARITY_GATE")
    print(f"frames={len(rows)}")
    print(f"gt_safety_objects={total_gt}")
    print(f"primary_recall={primary_recall:.6f}")
    print(f"secondary_recall={secondary_recall:.6f}")
    print(f"oracle_per_image_recall={oracle_recall:.6f}")
    print(f"oracle_gain_over_best_single={oracle_gain:.6f}")
    print(f"secondary_better_frames={secondary_better}")
    print(f"primary_better_frames={primary_better}")
    print(f"tied_frames={tied}")
    print("Interpretation: routing is only worth pursuing if the oracle gain and recovery-positive support are materially non-zero.")


if __name__ == "__main__":
    main()
