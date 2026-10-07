#!/usr/bin/env python3
"""Summarize Stage 6 frozen held-out evaluation results.

Consumes stage6_12cell_summary.csv and writes:
- stage6_group_summary.csv
- stage6_seed_domain_gaps.csv
- stage6_domain_gap_summary.csv
"""
from __future__ import annotations

import argparse
import csv
from pathlib import Path

import numpy as np
import pandas as pd

HIGHER_BETTER = [
    "map50_95", "map50", "map75",
    "precision_fixed", "recall_fixed", "f1_fixed",
    "no_helmet_recall", "no_gloves_recall", "no_boots_recall",
]
FNR_METRICS = ["no_helmet_fnr", "no_gloves_fnr", "no_boots_fnr"]


def parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True, type=Path)
    ap.add_argument("--out-dir", required=True, type=Path)
    return ap.parse_args()


def main():
    a = parse_args()
    a.out_dir.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(a.input)
    if len(df) != 12:
        raise RuntimeError(f"Expected 12 evaluation rows, got {len(df)}")

    # Aggregate seed stability within each train-domain × evaluation-domain condition.
    rows = []
    for (train_domain, domain_type, test_domain), g in df.groupby(
        ["train_domain", "domain_type", "test_domain"], sort=True
    ):
        row = {
            "train_domain": train_domain,
            "domain_type": domain_type,
            "test_domain": test_domain,
            "n_seeds": len(g),
        }
        for m in HIGHER_BETTER + FNR_METRICS:
            row[f"{m}_mean"] = float(g[m].mean())
            row[f"{m}_sd"] = float(g[m].std(ddof=1))
        rows.append(row)
    group = pd.DataFrame(rows)
    group.to_csv(a.out_dir / "stage6_group_summary.csv", index=False)

    # Paired seed-level generalization gaps.
    gaps = []
    for train_domain in ("Y", "C"):
        sub = df[df["train_domain"] == train_domain]
        for seed in sorted(sub["seed"].unique()):
            s = sub[sub["seed"] == seed]
            if len(s) != 2:
                raise RuntimeError(f"Expected 2 rows for {train_domain} seed {seed}, got {len(s)}")
            ind = s[s["domain_type"] == "in_domain"].iloc[0]
            cross = s[s["domain_type"] == "cross_domain"].iloc[0]
            row = {
                "train_domain": train_domain,
                "seed": int(seed),
                "in_test_domain": ind["test_domain"],
                "cross_test_domain": cross["test_domain"],
            }
            for m in HIGHER_BETTER:
                row[f"{m}_gap_in_minus_cross"] = float(ind[m] - cross[m])
            for m in FNR_METRICS:
                row[f"{m}_shift_cross_minus_in"] = float(cross[m] - ind[m])
            gaps.append(row)
    gaps = pd.DataFrame(gaps)
    gaps.to_csv(a.out_dir / "stage6_seed_domain_gaps.csv", index=False)

    # Mean/SD of paired gaps across the three seeds for each training direction.
    agg_rows = []
    gap_cols = [c for c in gaps.columns if c.endswith("_gap_in_minus_cross") or c.endswith("_shift_cross_minus_in")]
    for train_domain, g in gaps.groupby("train_domain", sort=True):
        row = {"train_domain": train_domain, "n_seeds": len(g)}
        for col in gap_cols:
            row[f"{col}_mean"] = float(g[col].mean())
            row[f"{col}_sd"] = float(g[col].std(ddof=1))
        agg_rows.append(row)
    pd.DataFrame(agg_rows).to_csv(a.out_dir / "stage6_domain_gap_summary.csv", index=False)

    print("PASS: Stage 6 statistical summaries written")
    print(a.out_dir / "stage6_group_summary.csv")
    print(a.out_dir / "stage6_seed_domain_gaps.csv")
    print(a.out_dir / "stage6_domain_gap_summary.csv")


if __name__ == "__main__":
    main()
