#!/usr/bin/env python3
"""Stage 8 publication-figure generator.

Reads frozen Stage 6/7 outputs from Google Drive-exported CSV/JSON files.
No training or inference is performed.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def parse_args():
    p=argparse.ArgumentParser()
    p.add_argument("--stage6-dir",required=True,type=Path)
    p.add_argument("--stage7b-dir",required=True,type=Path)
    p.add_argument("--out",required=True,type=Path)
    return p.parse_args()


def save(fig,path):
    fig.tight_layout()
    fig.savefig(path,dpi=600,bbox_inches="tight")
    fig.savefig(path.with_suffix(".pdf"),bbox_inches="tight")
    plt.close(fig)


def fig1_domain_map(group,out):
    fig,ax=plt.subplots(figsize=(7.0,4.6))
    x=np.arange(2)
    width=0.34
    train_domains=["Y","C"]
    labels=["Y-PPE trained","Construction-PPE trained"]
    in_means=[]; in_sds=[]; cross_means=[]; cross_sds=[]
    for tr in train_domains:
        ind=group[(group.train_domain==tr)&(group.domain_type=="in_domain")].iloc[0]
        cr=group[(group.train_domain==tr)&(group.domain_type=="cross_domain")].iloc[0]
        in_means.append(ind.map50_95_mean); in_sds.append(ind.map50_95_sd)
        cross_means.append(cr.map50_95_mean); cross_sds.append(cr.map50_95_sd)
    ax.bar(x-width/2,in_means,width,yerr=in_sds,capsize=4,label="In-domain")
    ax.bar(x+width/2,cross_means,width,yerr=cross_sds,capsize=4,label="Cross-domain")
    ax.set_xticks(x,labels)
    ax.set_ylabel("mAP50:95")
    ax.set_ylim(0,0.34)
    ax.set_title("Cross-domain degradation across three seeds")
    ax.legend(frameon=False)
    ax.grid(axis="y",alpha=0.25)
    save(fig,out/"Fig3_cross_domain_map5095.png")


def fig2_seed_gaps(gaps,out):
    fig,ax=plt.subplots(figsize=(7.0,4.6))
    for tr,label in [("Y","Y-PPE → Construction-PPE"),("C","Construction-PPE → Y-PPE")]:
        g=gaps[gaps.train_domain==tr].sort_values("seed")
        ax.plot(g.seed.astype(str),g.map50_95_gap_in_minus_cross,marker="o",label=label)
    ax.set_xlabel("Random seed")
    ax.set_ylabel("mAP50:95 domain gap (in − cross)")
    ax.set_title("Seed-level domain-generalization gaps")
    ax.grid(axis="y",alpha=0.25)
    ax.legend(frameon=False)
    save(fig,out/"Fig4_seed_level_domain_gaps.png")


def fig3_safety_recall(group,out):
    rows=[
        ("Y in-domain","Y","in_domain"),
        ("Y → C","Y","cross_domain"),
        ("C in-domain","C","in_domain"),
        ("C → Y","C","cross_domain"),
    ]
    classes=["no_helmet","no_gloves","no_boots"]
    vals=[]
    for label,tr,dt in rows:
        r=group[(group.train_domain==tr)&(group.domain_type==dt)].iloc[0]
        vals.append([r[f"{c}_recall_mean"] for c in classes])
    vals=np.asarray(vals,float)
    fig,ax=plt.subplots(figsize=(7.2,4.7))
    im=ax.imshow(vals,aspect="auto",vmin=0,vmax=max(0.4,float(vals.max())))
    ax.set_yticks(range(len(rows)),[r[0] for r in rows])
    ax.set_xticks(range(len(classes)),["no_helmet","no_gloves","no_boots"])
    ax.set_title("PPE-negative-state recall at the frozen operating point")
    for i in range(vals.shape[0]):
        for j in range(vals.shape[1]):
            ax.text(j,i,f"{vals[i,j]:.3f}",ha="center",va="center")
    fig.colorbar(im,ax=ax,label="Recall")
    save(fig,out/"Fig5_ppe_negative_state_recall.png")


def fig4_consensus(summary,out):
    classes=["no_helmet","no_gloves","no_boots"]
    y=[summary["Y_to_C"][c]["consensus_fn_rate"] for c in classes]
    c=[summary["C_to_Y"][c]["consensus_fn_rate"] for c in classes]
    x=np.arange(len(classes)); width=0.34
    fig,ax=plt.subplots(figsize=(7.0,4.6))
    ax.bar(x-width/2,y,width,label="Y-PPE → Construction-PPE")
    ax.bar(x+width/2,c,width,label="Construction-PPE → Y-PPE")
    ax.set_xticks(x,classes)
    ax.set_ylim(0,1.08)
    ax.set_ylabel("Consensus false-negative rate")
    ax.set_title("Persistence of PPE-negative-state false negatives across seeds")
    ax.legend(frameon=False)
    ax.grid(axis="y",alpha=0.25)
    save(fig,out/"Fig6_consensus_false_negative_rate.png")


def main():
    a=parse_args(); a.out.mkdir(parents=True,exist_ok=True)
    group=pd.read_csv(a.stage6_dir/"stage6_group_summary.csv")
    gaps=pd.read_csv(a.stage6_dir/"stage6_seed_domain_gaps.csv")
    summary=json.loads((a.stage7b_dir/"stage7_consensus_fn_summary.json").read_text(encoding="utf-8"))
    fig1_domain_map(group,a.out)
    fig2_seed_gaps(gaps,a.out)
    fig3_safety_recall(group,a.out)
    fig4_consensus(summary,a.out)
    print("STAGE8_PUBLICATION_FIGURES: PASS")


if __name__=="__main__":
    main()
