#!/usr/bin/env python3
"""V38-C scientific Figures 2 and 3 from V38-B audited numeric summary only.

No photographs, model inference, dataset modification or Test access. Figures
are 300 dpi PNG, one individual file per numbered journal figure.
"""
from pathlib import Path
import json
import statistics
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/"outputs/v38b_authorized_2026-11-23/V38_B_FINAL_NUMERICAL_RESULTS_SUMMARY_2026-11-23.json"
DIR=ROOT/"figures/V38C_2026-11-23"
ART=ROOT/"submissions/results-in-engineering/artwork"

def setup():
    plt.rcParams.update({
        "font.family":"DejaVu Sans","font.size":9.2,"axes.titlesize":10,
        "axes.labelsize":9,"axes.spines.top":False,"axes.spines.right":False,
        "savefig.facecolor":"white","figure.facecolor":"white",
        "axes.edgecolor":"#777777","xtick.labelsize":8,"ytick.labelsize":8
    })

def save(fig,name,number):
    DIR.mkdir(parents=True,exist_ok=True)
    ART.mkdir(parents=True,exist_ok=True)
    path=DIR/name
    fig.savefig(path,dpi=300,bbox_inches="tight")
    dest=ART/("Figure_"+str(number)+".png")
    dest.write_bytes(path.read_bytes())
    plt.close(fig)
    return {"file":str(path.relative_to(ROOT)),"artwork":str(dest.relative_to(ROOT)),
            "bytes":path.stat().st_size}

def make_agreement(d):
    rows=d["individual_target_numeric_rows"]
    valid=[(i+1,r) for i,r in enumerate(rows) if r["rho"] is not None]
    missing=[(i+1,r) for i,r in enumerate(rows) if r["rho"] is None]
    assert len(valid)==45 and len(missing)==3
    fig,axs=plt.subplots(1,2,figsize=(12.5,5.1),layout="constrained")
    ax=axs[0]
    ax.scatter([i for i,_ in valid],[r["rho"] for _,r in valid],s=33,
               facecolor="#285E86",linewidth=0)
    for i,_ in missing:
        ax.plot(i,-.16,marker="x",markersize=6,color="#A34842",markeredgewidth=1.6)
    ax.axhline(d["endpoint_metrics"]["spearman_rho"]["target_weighted"]["mean"],
               color="#B1732E",linestyle="--",linewidth=1.4,
               label="Available target mean: 0.649")
    ax.axhline(0,color="#777777",linewidth=.8)
    ax.set(xlim=(0,49),ylim=(-.24,1.0),xticks=[1,8,16,24,32,40,48],
           xlabel="Preselected target index (1–48)",ylabel="Spearman rho",
           title="A. Individual target rank agreement")
    ax.text(2,-.215,"x: non-estimable map due to ambiguous matching",fontsize=8,color="#A34842")
    ax.legend(frameon=False,loc="lower right",fontsize=8)
    ax.grid(axis="y",alpha=.13)
    ax=axs[1]
    cl=sorted(d["class_metrics"].items())
    names=[k for k,_ in cl]
    means=[v["rho"]["mean"] for _,v in cl]
    lo=[v["rho"]["min"] for _,v in cl]
    hi=[v["rho"]["max"] for _,v in cl]
    ns=[v["rho"]["n"] for _,v in cl]
    ax.errorbar(means,range(len(cl)),xerr=[
        [m-a for m,a in zip(means,lo)],[b-m for m,b in zip(means,hi)]],
        fmt="o",color="#285E86",ecolor="#9EA7AF",capsize=2,elinewidth=1.2,markersize=4)
    for j,n in enumerate(ns):
        ax.text(.985,j,"n="+str(n),fontsize=7.2,color="#747474",
                va="center",ha="right")
    ax.axvline(.6489788814589973,color="#B1732E",linestyle="--",linewidth=1.4)
    ax.set(xlim=(-.12,1.02),yticks=list(range(len(cl))),yticklabels=names,
           xlabel="Class-mean rho; bars show observed range",
           title="B. Descriptive within-class spread")
    ax.invert_yaxis()
    ax.grid(axis="x",alpha=.14)
    fig.suptitle("V38-B: signed sensitivity consistency across grid resolutions",
                 fontweight="bold",fontsize=12.5)
    return save(fig,"Figure_2_V38C_Target_Consistency.png",2)

def make_controls(d):
    rows=d["individual_target_numeric_rows"]
    paired=[r for r in rows if r["rho"] is not None and r.get("blur_fill_rho") is not None]
    assert len(paired)==14
    curves=d["progressive_curves"]["random_baseline_target_direction_results"]
    assert len(curves)==22
    deletes=[x["saliency_minus_random_mean_auc"] for x in curves if x["direction"]=="deletion"]
    inserts=[x["saliency_minus_random_mean_auc"] for x in curves if x["direction"]=="insertion"]
    assert len(deletes)==len(inserts)==11
    fig,axs=plt.subplots(1,2,figsize=(12.5,4.8),layout="constrained")
    ax=axs[0]
    gray=[x["rho"] for x in paired]
    blur=[x["blur_fill_rho"] for x in paired]
    ax.plot([-.16,1.03],[-.16,1.03],"--",linewidth=1,color="#8D8D8D")
    ax.scatter(gray,blur,s=42,facecolor="#285E86",edgecolor="white",linewidth=.4)
    ax.text(-.09,.96,"Paired mean rho: gray %.3f / blur %.3f"%(statistics.mean(gray),statistics.mean(blur)),
            va="top",fontsize=8)
    ax.text(-.09,.87,"Mean blur-minus-gray: %.3f"%(statistics.mean([b-a for a,b in zip(gray,blur)])),
            va="top",fontsize=8)
    ax.set(xlim=(-.15,1.01),ylim=(-.15,1.01),
           xlabel="Gray-fill cross-grid rho",ylabel="Blur-fill cross-grid rho",
           title="A. Same-target operator control (n=14)")
    ax.grid(alpha=.12)
    ax=axs[1]
    for group,vals,color in [(0,deletes,"#B1732E"),(1,inserts,"#285E86")]:
        for index,value in enumerate(vals):
            jitter=((index*7)%11-5)/40
            ax.scatter(group+jitter,value,s=32,color=color,alpha=.88)
        m=statistics.mean(vals)
        ax.plot([group-.17,group+.17],[m,m],color="#151515",linewidth=2)
        ax.text(group+.2,m,"%+.3f"%m,fontsize=8,va="center")
    ax.axhline(0,color="#777777",linewidth=1)
    ax.set(xlim=(-.5,1.65),ylim=(-.83,.85),xticks=[0,1],
           xticklabels=["Deletion (lower better)","Insertion (higher better)"],
           ylabel="Saliency AUC minus target mean random AUC",
           title="B. Ten-random-order controls (n=11 targets)")
    ax.grid(axis="y",alpha=.14)
    fig.suptitle("V38-B: operator and random-order response sensitivity",
                 fontweight="bold",fontsize=12.5)
    return save(fig,"Figure_3_V38C_Operator_and_Random_Controls.png",3)

def main():
    setup()
    d=json.loads(SRC.read_text(encoding="utf8"))
    assert d["status"]=="AUDITED_COMPLETE_REAL_INFERENCE"
    assert d["targets_processed"]==48 and d["attempted_model_calls"]==4984
    out=[make_agreement(d),make_controls(d)]
    # Protect against low-quality or accidentally empty artwork.
    from PIL import Image
    for row in out:
        path=ROOT/row["artwork"]
        with Image.open(path) as img:
            w,h=img.size
            assert w>=2500 and h>=850,(w,h)
        row["dimensions_pixels"]=[w,h]
    print(json.dumps({"status":"V38C_FIGURES_2_3_QA_PASS",
                      "numerical_sources":"V38B_audited_48_target_summary",
                      "hosted_model_calls":0,
                      "figures":out},indent=2))
if __name__=="__main__":
    main()
