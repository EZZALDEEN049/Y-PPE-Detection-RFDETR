#!/usr/bin/env python3
"""Train simple routing baselines with out-of-fold probabilities.

This script is intended for development/calibration data only. It produces
out-of-fold probabilities and a frozen logistic model specification. It does not
inspect or consume held-out test data.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score, roc_auc_score
from sklearn.model_selection import StratifiedKFold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

DEFAULT_FEATURES = [
    "n_detections",
    "max_confidence",
    "mean_confidence",
    "min_confidence",
    "p10_confidence",
    "safety_max_confidence",
    "safety_detection_count",
]


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--input", required=True)
    p.add_argument("--out-dir", required=True)
    p.add_argument("--features", nargs="+", default=DEFAULT_FEATURES)
    p.add_argument("--folds", type=int, default=5)
    p.add_argument("--seed", type=int, default=20261016)
    args = p.parse_args()

    rows = list(csv.DictReader(open(args.input, newline="", encoding="utf-8")))
    if not rows:
        raise SystemExit("empty input")

    X = np.array([[float(r[c]) for c in args.features] for r in rows], dtype=float)
    y = np.array([int(r["second_expert_recovers_primary_safety_fn"]) for r in rows], dtype=int)

    if len(np.unique(y)) < 2:
        raise SystemExit("router target has one class only; selective learning is not identifiable")
    min_class = int(np.bincount(y).min())
    n_splits = min(args.folds, min_class)
    if n_splits < 2:
        raise SystemExit("insufficient positive/negative examples for cross-fitting")

    skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=args.seed)
    oof = np.full(len(y), np.nan, dtype=float)

    for tr, va in skf.split(X, y):
        pipe = Pipeline([
            ("scale", StandardScaler()),
            ("clf", LogisticRegression(
                class_weight="balanced",
                max_iter=2000,
                random_state=args.seed,
            )),
        ])
        pipe.fit(X[tr], y[tr])
        oof[va] = pipe.predict_proba(X[va])[:, 1]

    if np.isnan(oof).any():
        raise SystemExit("incomplete out-of-fold predictions")

    full = Pipeline([
        ("scale", StandardScaler()),
        ("clf", LogisticRegression(
            class_weight="balanced",
            max_iter=2000,
            random_state=args.seed,
        )),
    ])
    full.fit(X, y)

    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)

    pred_path = out / "router_oof_predictions.csv"
    with pred_path.open("w", newline="", encoding="utf-8") as f:
        fields = list(rows[0].keys()) + ["router_score_oof"]
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r, score in zip(rows, oof):
            rr = dict(r)
            rr["router_score_oof"] = float(score)
            w.writerow(rr)

    scaler = full.named_steps["scale"]
    clf = full.named_steps["clf"]
    model_spec = {
        "features": args.features,
        "seed": args.seed,
        "folds_used": n_splits,
        "scaler_mean": scaler.mean_.tolist(),
        "scaler_scale": scaler.scale_.tolist(),
        "coef": clf.coef_[0].tolist(),
        "intercept": float(clf.intercept_[0]),
        "target": "second_expert_recovers_primary_safety_fn",
        "development_only": True,
    }
    (out / "router_logistic_spec.json").write_text(
        json.dumps(model_spec, indent=2), encoding="utf-8"
    )

    metrics = {
        "n": int(len(y)),
        "positive_n": int(y.sum()),
        "positive_rate": float(y.mean()),
        "oof_auroc": float(roc_auc_score(y, oof)),
        "oof_aupr": float(average_precision_score(y, oof)),
    }
    (out / "router_oof_metrics.json").write_text(
        json.dumps(metrics, indent=2), encoding="utf-8"
    )
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()
