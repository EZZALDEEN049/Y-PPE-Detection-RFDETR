#!/usr/bin/env python3
"""Select a routing threshold on development data under a safety constraint.

No default non-inferiority margin is imposed. The user must explicitly provide
an allowable absolute violation-recall loss, delta, before selection.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

import numpy as np


def recall(gt, fn):
    return 1.0 - fn / gt if gt else float("nan")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--input", required=True)
    p.add_argument("--score-column", default="router_score_oof")
    p.add_argument("--delta", type=float, required=True,
                   help="Maximum absolute violation-recall loss versus always-secondary reference")
    p.add_argument("--out", required=True)
    args = p.parse_args()

    if args.delta < 0:
        raise SystemExit("delta must be non-negative and pre-specified")

    rows = list(csv.DictReader(open(args.input, newline="", encoding="utf-8")))
    scores = np.array([float(r[args.score_column]) for r in rows])
    gt = np.array([int(r["gt_safety_objects"]) for r in rows])
    pfn = np.array([int(r["primary_safety_fn"]) for r in rows])
    sfn = np.array([int(r["secondary_safety_fn"]) for r in rows])
    total_gt = int(gt.sum())

    secondary_recall = recall(total_gt, int(sfn.sum()))
    thresholds = np.unique(np.concatenate(([-np.inf], scores, [np.inf])))
    candidates = []

    for t in thresholds:
        esc = scores >= t
        final_fn = np.where(esc, sfn, pfn)
        r = recall(total_gt, int(final_fn.sum()))
        loss = secondary_recall - r
        candidates.append({
            "threshold": float(t),
            "escalation_rate": float(esc.mean()),
            "expert_executions_per_image": float(1.0 + esc.mean()),
            "violation_recall": float(r),
            "loss_vs_always_secondary": float(loss),
            "safety_false_negatives": int(final_fn.sum()),
            "feasible": bool(loss <= args.delta + 1e-12),
        })

    feasible = [x for x in candidates if x["feasible"]]
    if not feasible:
        raise SystemExit("no threshold satisfies the pre-specified safety constraint")

    # Lowest escalation rate; break ties by higher recall.
    chosen = sorted(feasible, key=lambda x: (x["escalation_rate"], -x["violation_recall"]))[0]
    payload = {
        "selection_split": "development_only",
        "delta": args.delta,
        "reference": "always_secondary",
        "always_secondary_violation_recall": secondary_recall,
        "chosen": chosen,
    }
    Path(args.out).write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
