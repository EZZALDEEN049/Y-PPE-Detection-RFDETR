#!/usr/bin/env python3
"""Paired image-level bootstrap for frozen selective-policy evaluation."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

import numpy as np


def pct(a):
    return [float(np.quantile(a, 0.025)), float(np.quantile(a, 0.975))]


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--input", required=True,
                   help="Held-out table containing gt_safety_objects, primary_safety_fn, secondary_safety_fn, router_score")
    p.add_argument("--threshold-json", required=True)
    p.add_argument("--score-column", default="router_score")
    p.add_argument("--reps", type=int, default=2000)
    p.add_argument("--seed", type=int, default=20261016)
    p.add_argument("--out", required=True)
    args = p.parse_args()

    rows = list(csv.DictReader(open(args.input, newline="", encoding="utf-8")))
    lock = json.loads(Path(args.threshold_json).read_text(encoding="utf-8"))
    threshold = float(lock["chosen"]["threshold"])

    gt = np.array([int(r["gt_safety_objects"]) for r in rows], dtype=int)
    pfn = np.array([int(r["primary_safety_fn"]) for r in rows], dtype=int)
    sfn = np.array([int(r["secondary_safety_fn"]) for r in rows], dtype=int)
    score = np.array([float(r[args.score_column]) for r in rows], dtype=float)
    esc = score >= threshold
    final_fn = np.where(esc, sfn, pfn)

    rng = np.random.default_rng(args.seed)
    n = len(rows)
    recalls = []
    esc_rates = []
    fn_diffs = []

    for _ in range(args.reps):
        idx = rng.integers(0, n, n)
        g = int(gt[idx].sum())
        f = int(final_fn[idx].sum())
        sf = int(sfn[idx].sum())
        if g == 0:
            continue
        recalls.append(1.0 - f / g)
        esc_rates.append(float(esc[idx].mean()))
        fn_diffs.append(f - sf)

    payload = {
        "n_images": n,
        "bootstrap_reps_requested": args.reps,
        "bootstrap_reps_used": len(recalls),
        "threshold": threshold,
        "selective_violation_recall": float(1.0 - final_fn.sum() / gt.sum()) if gt.sum() else None,
        "selective_violation_recall_ci95": pct(recalls),
        "escalation_rate": float(esc.mean()),
        "escalation_rate_ci95": pct(esc_rates),
        "safety_fn_difference_vs_always_secondary": int(final_fn.sum() - sfn.sum()),
        "safety_fn_difference_ci95": pct(fn_diffs),
        "note": "Image-level paired bootstrap. Use cluster bootstrap instead if repeated frames/sites create dependence.",
    }
    Path(args.out).write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
