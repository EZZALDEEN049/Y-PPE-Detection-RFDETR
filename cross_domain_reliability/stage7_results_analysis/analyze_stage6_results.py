#!/usr/bin/env python3
"""Stage 7 publication-oriented analysis of frozen Stage 6 outputs.

This script is analysis-only. It does not load model checkpoints and does not
run inference or training.
"""
from __future__ import annotations
import argparse
from pathlib import Path
import json
import pandas as pd

def parse_args():
    p=argparse.ArgumentParser()
    p.add_argument("--stage6-dir", required=True, type=Path)
    p.add_argument("--out", required=True, type=Path)
    return p.parse_args()

def main():
    a=parse_args()
    a.out.mkdir(parents=True, exist_ok=True)
    raw=pd.read_csv(a.stage6_dir/"stage6_12cell_summary.csv")
    group=pd.read_csv(a.stage6_dir/"stage6_group_summary.csv")
    gaps=pd.read_csv(a.stage6_dir/"stage6_seed_domain_gaps.csv")
    gap_summary=pd.read_csv(a.stage6_dir/"stage6_domain_gap_summary.csv")
    metrics=json.loads((a.stage6_dir/"stage6_all_metrics.json").read_text())

    if len(raw) != 12:
        raise RuntimeError(f"Expected 12 Stage 6 rows, got {len(raw)}")
    if set(raw["seed"]) != {17,42,2026}:
        raise RuntimeError("Unexpected seed set in Stage 6 summary")

    primary=[]
    for tr in ("Y","C"):
        ind=group[(group.train_domain==tr)&(group.domain_type=="in_domain")].iloc[0]
        cross=group[(group.train_domain==tr)&(group.domain_type=="cross_domain")].iloc[0]
        primary.append({
            "train_domain":tr,
            "in_test_domain":ind.test_domain,
            "cross_test_domain":cross.test_domain,
            "map50_95_in_mean":ind.map50_95_mean,
            "map50_95_in_sd":ind.map50_95_sd,
            "map50_95_cross_mean":cross.map50_95_mean,
            "map50_95_cross_sd":cross.map50_95_sd,
            "map50_95_gap_abs":ind.map50_95_mean-cross.map50_95_mean,
            "map50_95_relative_drop_pct":
                100*(ind.map50_95_mean-cross.map50_95_mean)/ind.map50_95_mean,
            "precision_in_mean":ind.precision_fixed_mean,
            "precision_cross_mean":cross.precision_fixed_mean,
            "recall_in_mean":ind.recall_fixed_mean,
            "recall_cross_mean":cross.recall_fixed_mean,
            "f1_in_mean":ind.f1_fixed_mean,
            "f1_cross_mean":cross.f1_fixed_mean,
        })
    pd.DataFrame(primary).to_csv(a.out/"stage7_primary_domain_results.csv",index=False)

    safety_cols=[
        "train_domain","domain_type","test_domain","n_seeds",
        "no_helmet_recall_mean","no_helmet_recall_sd",
        "no_gloves_recall_mean","no_gloves_recall_sd",
        "no_boots_recall_mean","no_boots_recall_sd",
        "no_helmet_fnr_mean","no_gloves_fnr_mean","no_boots_fnr_mean",
    ]
    group[safety_cols].to_csv(a.out/"stage7_safety_violation_summary.csv",index=False)

    per_class=[]
    for _,rec in metrics.items():
        for cls,ap in rec["ap_metrics"]["per_class_ap50_95"].items():
            per_class.append({
                "train_domain":rec["train_domain"],
                "test_domain":rec["test_domain"],
                "domain_type":rec["domain_type"],
                "seed":rec["seed"],
                "class":cls,
                "ap50_95":ap,
            })
    pc=pd.DataFrame(per_class)
    pc.groupby(["train_domain","domain_type","test_domain","class"])["ap50_95"]\
      .agg(["mean","std"]).reset_index()\
      .to_csv(a.out/"stage7_per_class_ap50_95_summary.csv",index=False)

    gap_summary.to_csv(a.out/"stage7_domain_gap_summary.csv",index=False)
    gaps.to_csv(a.out/"stage7_seed_level_gaps.csv",index=False)
    print("STAGE7_PRIMARY_ANALYSIS: PASS")

if __name__=="__main__":
    main()
