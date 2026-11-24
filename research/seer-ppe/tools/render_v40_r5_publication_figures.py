#!/usr/bin/env python3
"""V40-R5 offline publication artwork QA. No inference, images or data changes."""
from pathlib import Path
from copy import deepcopy
import argparse, json, hashlib, statistics, re, sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm
from matplotlib.patches import Rectangle
import fitz
import cairosvg
from PIL import Image, ImageOps, ImageDraw
import render_v34b_scientific_figures as historical
import render_v38c_figures as extension

ROOT = Path(__file__).resolve().parents[1]
SUB = ROOT / "submissions/results-in-engineering"
W = 180 / 25.4
BLUE="#285E86"; GOLD="#B1732E"; GRAY="#777777"
plt.rcParams.update({"font.family":"DejaVu Sans","font.size":8.5,"axes.labelsize":8.5,
 "axes.titlesize":9,"xtick.labelsize":8,"ytick.labelsize":8,"legend.fontsize":8,
 "pdf.fonttype":42,"ps.fonttype":42,"savefig.facecolor":"white","axes.spines.top":False,
 "axes.spines.right":False,"figure.facecolor":"white"})

def save(fig, path):
    fig.savefig(path, format="pdf", dpi=500, metadata={"Title":path.stem,"Author":"SEER-PPE research project","Subject":"Data-derived publication artwork candidate"})
    plt.close(fig)

def alias(meta, i):
    return ["Train A","Train B","Train C","Train C","Train D",
            "Validation V01","Validation V02","Validation V03","Validation V03","Validation V04"][i]

def historical_figures(items, out):
    assert len(items)==10
    # The existing validator reconstructs every cell and recomputes all ranks.
    displayed=np.concatenate([np.concatenate([x["fine"].ravel(),x["direct"].ravel()]) for x in items])
    scale=float(np.percentile(np.abs(displayed),historical.SCALE_PERCENTILE,method="linear"))
    assert abs(scale-15.470900859749108)<1e-9
    assert np.count_nonzero(np.abs(displayed)>scale)==17
    labels=[f'H{i+1:02d}  {x["meta"]["target_class"]}' for i,x in enumerate(items)]
    rho=np.array([x["rho_recomputed"] for x in items])
    tau=np.array([x["tau_recomputed"] for x in items])
    ov=np.array([x["overlap"] for x in items])
    fig,ax=plt.subplots(figsize=(W,3.9))
    fig.subplots_adjust(left=.27,right=.86,bottom=.15,top=.88)
    order=np.argsort(rho); y=np.arange(10)
    ax.barh(y-.18,rho[order],height=.32,color=BLUE,label="Spearman ρ")
    ax.barh(y+.18,tau[order],height=.32,color=GOLD,label="Kendall τ-b")
    ax.set(yticks=y,yticklabels=np.array(labels)[order],xlim=(0,1),xlabel="Rank correlation")
    ax.grid(axis="x",alpha=.2);ax.set_axisbelow(True)
    ax.legend(loc="lower right",bbox_to_anchor=(1,1.005),ncol=2,frameon=False)
    for yi,i in enumerate(order):ax.text(1.025,yi,f"{ov[i]}/4",va="center",fontsize=8,clip_on=False)
    ax.text(1.025,1.035,"Top 4",transform=ax.transAxes,fontsize=8,ha="left")
    fig.text(.02,.965,"Historical ten-target spatial agreement",weight="bold",va="top",fontsize=10)
    save(fig,out/"Figure_1.pdf")
    for i,x in enumerate(items):
        fig,axes=plt.subplots(1,2,figsize=(W,5.0))
        fig.subplots_adjust(left=.095,right=.965,top=.85,bottom=.36,wspace=.28)
        fig.text(.5,.95,f'H{i+1:02d} • {alias(x["meta"],i)} • {x["meta"]["target_class"]}',ha="center",weight="bold",fontsize=11)
        norm=TwoSlopeNorm(vmin=-scale,vcenter=0,vmax=scale)
        for ax,n,values,title in [(axes[0],8,x["fine"],"A. Native 8×8"),(axes[1],4,x["direct"],"B. Direct 4×4")]:
            # pcolormesh uses vector cells; no source photo or raster embedding.
            mesh=ax.pcolormesh(np.arange(n+1),np.arange(n+1),values,cmap="RdBu_r",norm=norm,
                shading="flat",edgecolors="#b0b0b0",linewidth=.25)
            ax.set(xlim=(0,n),ylim=(n,0),xticks=np.arange(n)+.5,yticks=np.arange(n)+.5,
                   xticklabels=np.arange(1,n+1),yticklabels=np.arange(1,n+1),xlabel="Grid column",ylabel="Grid row",title=title)
            ax.set_aspect("equal");ax.tick_params(length=0)
        for j in x["top_pooled"]:
            row,col=divmod(j,4);axes[0].add_patch(Rectangle((2*col,2*row),2,2,fill=False,edgecolor="#CF8E00",linewidth=1.6))
        for j in x["top_direct"]:
            row,col=divmod(j,4);axes[1].add_patch(Rectangle((col,row),1,1,fill=False,edgecolor="#CF8E00",linewidth=1.6))
        cbax=fig.add_axes([.20,.235,.60,.035]);cb=fig.colorbar(mesh,cax=cbax,orientation="horizontal",extend="both")
        cb.solids.set_rasterized(False)
        cb.set_label("Signed score-drop density (drop / exact area fraction)")
        fig.text(.5,.110,f'Spearman ρ = {x["rho_recomputed"]:.4f}    Kendall τ-b = {x["tau_recomputed"]:.4f}    Top-four = {x["overlap"]}/4',ha="center",fontsize=9,weight="bold")
        fig.text(.5,.060,"Gold outlines: four highest-ranked aligned regions. Shared color scale;",ha="center",fontsize=8)
        fig.text(.5,.032,"clipping is display-only; all metrics use original numeric values.",ha="center",fontsize=8)
        save(fig,out/f"Figure_S{i+1}.pdf")
    return {"historical_targets":10,"historical_images":8,"scale":scale,"display_saturated":17,
            "rho_mean":float(rho.mean()),"tau_mean":float(tau.mean()),"top_four_mean":float(ov.mean()/4)}

def extension_figures(d,out):
    rows=d["individual_target_numeric_rows"];valid=[(i+1,r) for i,r in enumerate(rows) if r["rho"] is not None]
    missing=[i+1 for i,r in enumerate(rows) if r["rho"] is None]
    assert len(rows)==48 and len(valid)==45 and missing==[5,30,47]
    mean=statistics.mean(r["rho"] for _,r in valid)
    assert abs(mean-.6489788814589973)<1e-12
    fig=plt.figure(figsize=(W,6.8))
    gs=fig.add_gridspec(3,1,height_ratios=[2.0,.32,3.0],left=.22,right=.94,bottom=.085,top=.95,hspace=.45)
    ax=fig.add_subplot(gs[0]);ax.scatter([i for i,_ in valid],[r["rho"] for _,r in valid],s=17,c=BLUE)
    ax.axhline(mean,color=GOLD,ls="--",lw=1.1,label=f"Available target mean: {mean:.3f}")
    ax.axhline(0,color=GRAY,lw=.6);ax.set(xlim=(0,49),ylim=(-.10,1),ylabel="Spearman ρ",xticks=[1,8,16,24,32,40,48],title="A. Individual target rank agreement")
    ax.grid(axis="y",alpha=.18);ax.tick_params(labelbottom=False)
    ax.set_title(f"A. Individual target rank agreement (dashed: mean {mean:.3f})")
    strip=fig.add_subplot(gs[1]);strip.set(xlim=(0,49),ylim=(0,1),xticks=[1,8,16,24,32,40,48],yticks=[])
    strip.scatter(missing,[.55]*3,marker="x",s=26,color="#A34842");strip.set_ylabel("Undefined",rotation=0,labelpad=26,va="center")
    strip.set_xlabel("Preselected target index (1–48)");strip.spines["left"].set_visible(False)
    ax=fig.add_subplot(gs[2]);cl=sorted(d["class_metrics"].items())
    means=np.array([v["rho"]["mean"] for _,v in cl]);lo=np.array([v["rho"]["min"] for _,v in cl]);hi=np.array([v["rho"]["max"] for _,v in cl])
    ax.errorbar(means,np.arange(len(cl)),xerr=[means-lo,hi-means],fmt="o",markersize=4,color=BLUE,ecolor="#808990",capsize=2)
    ax.axvline(mean,color=GOLD,ls="--",lw=1.1)
    ax.set(xlim=(-.1,1.03),yticks=np.arange(len(cl)),yticklabels=[f'{k} (n={v["rho"]["n"]})' for k,v in cl],xlabel="Class-mean ρ; bars show observed range",title="B. Descriptive class-level spread")
    ax.invert_yaxis();ax.grid(axis="x",alpha=.18)
    save(fig,out/"Figure_2.pdf")
    paired=[r for r in rows if r["rho"] is not None and r.get("blur_fill_rho") is not None];assert len(paired)==14
    gray=[r["rho"] for r in paired];blur=[r["blur_fill_rho"] for r in paired]
    curves=d["progressive_curves"]["random_baseline_target_direction_results"]
    delete=[r["saliency_minus_random_mean_auc"] for r in curves if r["direction"]=="deletion"];insert=[r["saliency_minus_random_mean_auc"] for r in curves if r["direction"]=="insertion"]
    assert len(delete)==len(insert)==11 and max(delete)<0 and min(insert)>0
    fig,axes=plt.subplots(1,2,figsize=(W,3.9));fig.subplots_adjust(left=.10,right=.97,top=.88,bottom=.24,wspace=.4)
    ax=axes[0];ax.plot([-.1,1],[-.1,1],ls="--",color=GRAY,lw=.8);ax.scatter(gray,blur,s=27,c=BLUE,edgecolor="white",lw=.3)
    ax.set(xlim=(-.1,1),ylim=(-.1,1),xlabel="Gray-fill ρ",ylabel="Blur-fill ρ",title="A. Paired fill control (n=14)")
    ax.set_aspect("equal");ax.grid(alpha=.15)
    ax.text(.02,.97,f"Gray mean: {statistics.mean(gray):.3f}\nBlur mean: {statistics.mean(blur):.3f}",transform=ax.transAxes,va="top",fontsize=8)
    ax=axes[1]
    for g,vals,color in [(0,delete,GOLD),(1,insert,BLUE)]:
        jitter=np.array([((i*7)%11-5)/45 for i in range(11)])
        ax.scatter(g+jitter,vals,s=23,c=color);v=statistics.mean(vals);ax.hlines(v,g-.18,g+.18,color="#222",lw=1.7)
    ax.axhline(0,lw=.7,color=GRAY);ax.set(xlim=(-.45,1.45),ylim=(-.72,.72),xticks=[0,1],xticklabels=["Deletion\n(lower better)","Insertion\n(higher better)"],ylabel="Ranked AUC − mean random AUC",title="B. Internal order control (n=11)")
    ax.grid(axis="y",alpha=.15)
    ax.text(.025,.97,f"Mean deletion: {statistics.mean(delete):+.3f}\nMean insertion: {statistics.mean(insert):+.3f}",transform=ax.transAxes,va="top",fontsize=8)
    fig.text(.5,.04,"Random-order comparison is an internal response diagnostic, not independent fidelity.",ha="center",fontsize=8)
    save(fig,out/"Figure_3.pdf")
    return {"extension_targets":48,"estimable":45,"undefined_indices":missing,"mean_rho":mean,"paired":14,
            "gray_mean":statistics.mean(gray),"blur_mean":statistics.mean(blur),"deletion_delta_mean":statistics.mean(delete),"insertion_delta_mean":statistics.mean(insert)}

def qa(out, private_tokens):
    pdfs=[out/f"Figure_{i}.pdf" for i in range(1,5)]+[out/f"Figure_S{i}.pdf" for i in range(1,11)]
    rows=[]
    thumbnails=[]
    for p in pdfs:
        with fitz.open(p) as d:
            assert len(d)==1;pg=d[0];txt=pg.get_text()
            assert len(txt)>40 and not any(v in txt for v in private_tokens if len(v)>7),p.name
            assert not re.search(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b",txt,re.I),p.name
            assert len(pg.get_images(full=True))==0,(p.name,"unexpected raster image")
            spans=[s for b in pg.get_text("dict")["blocks"] for l in b.get("lines",[]) for s in l["spans"] if s["text"].strip()]
            minpt=min(s["size"] for s in spans)
            assert minpt>=6.5,(p.name,minpt)
            assert all(fitz.Rect(s["bbox"]) in pg.rect+(-.5,-.5,.5,.5) for s in spans),p.name
            pix=pg.get_pixmap(matrix=fitz.Matrix(1.6,1.6),alpha=False)
            im=Image.frombytes("RGB",(pix.width,pix.height),pix.samples);thumbnails.append((p.stem,im))
            rows.append({"file":p.name,"width_mm":round(pg.rect.width*25.4/72,2),"height_mm":round(pg.rect.height*25.4/72,2),
                         "text_min_pt":round(minpt,2),"vector_only":True,"sha256":hashlib.sha256(p.read_bytes()).hexdigest(),"privacy_text_scan":"PASS"})
    # Rendered contact sheets for internal human visual inspection, not journal figures.
    qa_dir=out/"qa";qa_dir.mkdir(exist_ok=True)
    for start in range(0,len(thumbnails),4):
        sheet=Image.new("RGB",(1600,1800),"#e8ebee");draw=ImageDraw.Draw(sheet)
        for j,(name,img) in enumerate(thumbnails[start:start+4]):
            x=(j%2)*800;y=(j//2)*900
            draw.text((x+15,y+10),name,fill="#111111")
            img.thumbnail((770,860),Image.Resampling.LANCZOS)
            sheet.paste(img,(x+(800-img.width)//2,y+28+(860-img.height)//2))
        sheet.save(qa_dir/f"Contact_{start//4+1}.jpg",quality=88)
    return rows

def main():
    ap=argparse.ArgumentParser();ap.add_argument("--output-dir",type=Path,required=True);args=ap.parse_args()
    out=args.output_dir.resolve();out.mkdir(parents=True,exist_ok=True)
    old=json.loads(historical.SOURCE_DEFAULT.read_text(encoding="utf8"))
    items=historical.validate_and_prepare(old)
    d=json.loads(extension.SRC.read_text(encoding="utf8"))
    assert d["status"]=="AUDITED_COMPLETE_REAL_INFERENCE" and d["attempted_model_calls"]==4984
    private_tokens=[]
    for x in items:
        private_tokens += [x["meta"]["target_id"],x["meta"]["image_key"].split(":",1)[-1]]
    private_tokens += [str(r.get("source_id","")) for r in d["individual_target_numeric_rows"]]
    summary={"historical":historical_figures(items,out),"extension":extension_figures(d,out)}
    # CairoSVG preserves vector paths and text; 180 mm final page width.
    cairosvg.svg2pdf(url=str(SUB/"artwork-publication/Figure_4_Proposed_Workflow.svg"),write_to=str(out/"Figure_4.pdf"),output_width=180/25.4*96,output_height=180/25.4*96*.92)
    summary.update({"status":"R5_STRUCTURAL_QA_PASS_VISUAL_AND_AUTHOR_REVIEW_PENDING","figures":qa(out,private_tokens),
        "source_sha256":{"historical":hashlib.sha256(historical.SOURCE_DEFAULT.read_bytes()).hexdigest(),"extension":hashlib.sha256(extension.SRC.read_bytes()).hexdigest()},
        "new_model_calls":0,"source_data_modified":False})
    (out/"R5_ARTWORK_QA.json").write_text(json.dumps(summary,indent=2,ensure_ascii=False)+"\n",encoding="utf8")
    print(json.dumps(summary,indent=2,ensure_ascii=False))
if __name__=="__main__":
    main()
