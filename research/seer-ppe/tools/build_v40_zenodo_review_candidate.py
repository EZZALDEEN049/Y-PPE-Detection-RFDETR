#!/usr/bin/env python3
"""Create a REVIEW-ONLY Zenodo candidate, never deposit. Run from research checkout."""
import argparse,csv,hashlib,json,math,random,re,shutil,statistics as st,subprocess,sys,zipfile
from pathlib import Path
from collections import defaultdict
ROOT=Path(__file__).resolve().parents[1]
SUB=ROOT/"submissions/results-in-engineering"
def main():
    ap=argparse.ArgumentParser();ap.add_argument("--output-dir",type=Path,required=True);a=ap.parse_args()
    out=a.output_dir.resolve();out.mkdir(parents=True,exist_ok=True)
    dest=out/"PPE_Cross_Resolution_Reproducibility_Archive"
    subprocess.run([sys.executable,str(ROOT/"tools/preflight_v40_zenodo_numeric_archive.py"),"--output-dir",str(dest)],check=True)
    (dest/"analysis").mkdir();(dest/"figures").mkdir()
    # All archive-only calculations use the same tested numerical definitions, but only read CSV/JSONL.
    src=(ROOT/"tools/preflight_v40_zenodo_numeric_archive.py").read_text()
    helpers=src[src.index("def near("):src.index("def main():")]
    verifier='''"""Recalculate archived score statistics without original images, hosted model or repository."""
import csv,hashlib,json,math,random,statistics as st
from pathlib import Path
from collections import defaultdict,Counter
ROOT=Path(__file__).resolve().parents[1]
def read(name):
    with (ROOT/name).open(encoding="utf8",newline="") as f:return list(csv.DictReader(f))
def num(s):return float(s) if s!="" else None
'''+helpers+'''
def main():
    for line in (ROOT/"SHA256SUMS.txt").read_text().splitlines():
        digest,name=line.split("  ",1)
        assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest,name
    v=read("validation_metrics.csv")
    assert len(v)==459
    gt,pred,tp,fp,fn=[sum(int(r[k]) for r in v) for k in ("gt","predictions","tp","fp","fn")]
    assert (gt,pred,tp,fp,fn)==(3471,4103,3297,806,174)
    cl=read("validation_class_metrics.csv");assert len(cl)==51
    c0=[r for r in cl if r["cohort"]=="M0"];assert len(c0)==17
    assert [sum(int(r[k]) for r in c0) for k in ("gt","predictions","tp","fp","fn")]==[gt,pred,tp,fp,fn]
    manifest=read("target_manifest.csv");assert len(manifest)==48 and len({r["image_cluster"] for r in manifest})==24
    maps=defaultdict(list)
    for r in read("perturbation_scores.csv"):
        for k in ("row","col"):r[k]=int(r[k])
        for k in ("area_fraction","score_drop","score_after"):r[k]=num(r[k])
        maps[r["target"],r["fill"],int(r["grid"])].append(r)
    assert sum(map(len,maps.values()))==5120
    spatial=read("spatial_agreement.csv");ops=read("operator_comparison.csv")
    by=defaultdict(list);vals=[]
    for r in spatial:
        pair=aligned(maps[r["target"],"gray",8],maps[r["target"],"gray",4])
        if pair is None:assert r["rho"]==""
        else:
            x,y=pair;v=rho(x,y)
            near(v,num(r["rho"]));near(tau(x,y),num(r["tau_b"]));near(overlap(x,y),num(r["top_four_overlap"]))
            vals.append(v);by[r["image_cluster"]].append(v)
    assert len(vals)==45
    means=[st.mean(by[f"I{i:02}"]) for i in range(1,25)]
    rng=random.Random("seer-ppe/v38b-image-block-bootstrap-2026-11-23")
    boot=sorted(st.mean(means[rng.randrange(24)] for _ in means) for _ in range(5000))
    near(st.mean(vals),.6489788814589973);near(st.mean(means),.6507583876423197)
    near(boot[int(.025*4999)],.5949574145556713);near(boot[int(.975*4999)],.7043504901960784)
    loo=[st.mean([v for k,g in by.items() if k!=drop for v in g]) for drop in by]
    bounds=[(sum(vals)-3)/48,(sum(vals)+3)/48]
    pairs=[]
    for r in ops:
        p=aligned(maps[r["target"],"blur",8],maps[r["target"],"blur",4])
        if p is None:assert r["blur_rho"]==""
        else:near(rho(*p),num(r["blur_rho"]))
        if r["paired_delta"]!="":pairs.append((num(r["gray_rho"]),num(r["blur_rho"])))
    assert len(pairs)==14
    gray,blur=[st.mean(x[i] for x in pairs) for i in (0,1)]
    near(gray,.6942587984819544);near(blur,.4810924369747899)
    points=defaultdict(list)
    for r in read("curve_points.csv"):points[r["target"],r["curve"]].append(r)
    aucs=defaultdict(dict)
    for r in read("auc_results.csv"):
        p=sorted(points[r["target"],r["curve"]],key=lambda x:int(x["point_index"]))
        assert len(p)==11
        x=[num(v["modified_fraction"]) for v in p];y=[num(v["normalized_score"]) for v in p]
        near(x[0],0);near(x[-1],1);assert all(a<b for a,b in zip(x,x[1:]))
        v=sum((b-a)*(c+d)/2 for a,b,c,d in zip(x,x[1:],y,y[1:]))
        near(v,num(r["auc"]));aucs[r["target"]][r["curve"]]=v
    assert len(points)==264 and len(aucs)==11
    delta={direction:[v[f"8x8_saliency_{direction}"]-st.mean(v[f"8x8_random_seed_{i}_{direction}"] for i in range(10)) for v in aucs.values()] for direction in ("deletion","insertion")}
    assert max(delta["deletion"])<0 and min(delta["insertion"])>0
    h=defaultdict(list)
    for r in read("historical_aligned_density.csv"):h[r["target"]].append(r)
    hs=read("historical_spatial_agreement.csv")
    for r in hs:
        p=sorted(h[r["target"]],key=lambda x:int(x["region"]))
        x=[num(z["pooled_fine"]) for z in p];y=[num(z["direct_coarse"]) for z in p]
        near(rho(x,y),num(r["rho"]));near(tau(x,y),num(r["tau_b"]));near(overlap(x,y),num(r["top_four_overlap"]))
    events=[json.loads(l) for l in (ROOT/"inference_ledger.jsonl").read_text().splitlines()]
    for typ in ("ATTEMPT_RESERVED","ATTEMPT_SUCCEEDED"):
        assert [e["call_index"] for e in events if e["event"]==typ]==list(range(1,4985))
    assert len(events)==9968
    print(json.dumps({"status":"PASS","validation":{"TP":tp,"FP":fp,"FN":fn,"precision":tp/pred,"recall":tp/gt,"micro_f1":2*tp/(2*tp+fp+fn)},"target_mean":st.mean(vals),"image_mean":st.mean(means),"bootstrap":[boot[int(.025*4999)],boot[int(.975*4999)]],"leave_one_image_out":[min(loo),max(loo)],"missing_bounds":bounds,"gray_mean":gray,"blur_mean":blur,"auc_count":264,"mean_auc_differences":{k:st.mean(v) for k,v in delta.items()},"historical_mean":st.mean(num(r["rho"]) for r in hs),"successful_calls":4984},indent=2))
if __name__=="__main__":main()
'''
    (dest/"analysis/reproduce.py").write_text(verifier,encoding="utf8")
    # Native historical density values required by the published heatmaps.
    h=json.loads((ROOT/"V34A_SPATIAL_MAP_ALIGNMENT_RANK_CORRELATION_2026-11-22.json").read_text())
    hm={r["target_id"]:r for r in h["per_target_aligned_maps"]};rows=[]
    for i,j in enumerate([4,2,3,8,6,9,1,5,0,7],1):
        r=hm[h["per_target"][j]["target_id"]]
        for c in r["aligned_cells"]:
            for x in c["fine_children"]:
                rows.append(dict(target=f"H{i:02}",grid=8,row=x["row_8x8"],col=x["col_8x8"],area_fraction=x["area_fraction"],score_drop=x["score_drop"],density=x["score_drop"]/x["area_fraction"]))
        for k,c in enumerate(r["aligned_cells"]):
            rows.append(dict(target=f"H{i:02}",grid=4,row=k//4,col=k%4,area_fraction=c["area_fraction"],score_drop=c["direct_4x4_score_drop"],density=c["direct_4x4_signed_drop_per_area"]))
    assert len(rows)==800
    with (dest/"historical_native_cells.csv").open("w",newline="",encoding="utf8") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    for i in range(1,5):shutil.copyfile(SUB/f"artwork-publication/r5/Figure_{i}.pdf",dest/f"figures/Figure_{i}.pdf")
    for i in range(1,11):shutil.copyfile(SUB/f"artwork-publication/r5/Figure_S{i}.pdf",dest/f"figures/Figure_S{i}.pdf")
    shutil.copyfile(SUB/"artwork-publication/Figure_4_Proposed_Workflow.svg",dest/"figures/Figure_4.svg")
    # Adapt the already reviewed R5 functions to archive-only inputs.
    render=(ROOT/"tools/render_v40_r5_publication_figures.py").read_text()
    funcs=render[render.index("W = 180"):render.index("def qa(")].replace("historical.SCALE_PERCENTILE","98")
    # Match the original percentile value from its source, not a guessed default.
    orig=(ROOT/"tools/render_v34b_scientific_figures.py").read_text()
    match=re.search(r"^SCALE_PERCENTILE\s*=\s*([0-9.]+)",orig,re.M);assert match
    funcs=funcs.replace("np.percentile(np.abs(displayed),98,","np.percentile(np.abs(displayed),"+match.group(1)+",")
    header='''"""Recreate R5 figure content from this candidate archive; no repository or images needed."""
import csv,statistics
from pathlib import Path
from collections import defaultdict
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm
from matplotlib.patches import Rectangle
import cairosvg
ROOT=Path(__file__).resolve().parents[1]
def read(n):
    with (ROOT/n).open(encoding="utf8",newline="") as f:return list(csv.DictReader(f))
def num(x):return float(x) if x!="" else None
'''
    tail='''
def main():
    out=ROOT/"regenerated_figures";out.mkdir(exist_ok=True)
    native=defaultdict(list);aligned_rows=defaultdict(list)
    for r in read("historical_native_cells.csv"):native[r["target"],int(r["grid"])].append(r)
    for r in read("historical_aligned_density.csv"):aligned_rows[r["target"]].append(r)
    items=[]
    for r in read("historical_spatial_agreement.csv"):
        tag=r["target"];a=sorted(aligned_rows[tag],key=lambda z:int(z["region"]))
        def grid(n):
            return np.array([float(z["density"]) for z in sorted(native[tag,n],key=lambda z:(int(z["row"]),int(z["col"])))]).reshape(n,n)
        items.append({"meta":{"target_class":r["category"]},"fine":grid(8),"direct":grid(4),"rho_recomputed":float(r["rho"]),"tau_recomputed":float(r["tau_b"]),"overlap":round(float(r["top_four_overlap"])*4),"top_pooled":sorted(range(16),key=lambda j:(-float(a[j]["pooled_fine"]),j))[:4],"top_direct":sorted(range(16),key=lambda j:(-float(a[j]["direct_coarse"]),j))[:4]})
    historical_figures(items,out)
    ops={r["target"]:r for r in read("operator_comparison.csv")};rows=[];cl=defaultdict(list)
    for r in read("spatial_agreement.csv"):
        v=num(r["rho"]);rows.append({"rho":v,"blur_fill_rho":num(ops.get(r["target"],{}).get("blur_rho",""))})
        if v is not None:cl[r["category"]].append(v)
    au=defaultdict(dict)
    for r in read("auc_results.csv"):au[r["target"]][r["curve"]]=float(r["auc"])
    c=[{"direction":direction,"saliency_minus_random_mean_auc":v[f"8x8_saliency_{direction}"]-statistics.mean(v[f"8x8_random_seed_{i}_{direction}"] for i in range(10))} for v in au.values() for direction in ("deletion","insertion")]
    extension_figures({"individual_target_numeric_rows":rows,"class_metrics":{k:{"rho":{"n":len(v),"mean":statistics.mean(v),"min":min(v),"max":max(v)}} for k,v in cl.items()},"progressive_curves":{"random_baseline_target_direction_results":c}},out)
    cairosvg.svg2pdf(url=str(ROOT/"figures/Figure_4.svg"),write_to=str(out/"Figure_4.pdf"),output_width=180/25.4*96,output_height=180/25.4*96*.92)
    assert len(list(out.glob("*.pdf")))==14
    print("14 figures regenerated; visual content reproduction, not byte-identical PDF guarantee.")
if __name__=="__main__":main()
'''
    (dest/"analysis/render_figures.py").write_text(header+funcs+tail,encoding="utf8")
    (dest/"README.md").write_text("""# PPE Cross-Resolution Reproducibility Archive — REVIEW CANDIDATE
**Not cleared for public deposit.** Prepared 2026-11-24. Associated manuscript: Cross-Resolution Consistency of Target-Matched Perturbation Sensitivity Maps for Personal Protective Equipment Detection. Author: Ezzaldeen Al-Tayar, Taiz University.

## Recalculate
Python 3.11. From the archive root run:
    python analysis/reproduce.py
No external packages, image files, weights, credentials, network or inference are needed for the numerical checks. For the figures, install requirements.txt, then run python analysis/render_figures.py. The separate Figure 4 SVG is a conceptual schematic, not validated operational evidence; ChatGPT GPT-6.2 assisted its preparation. Original R5 PDFs are included. Recreated PDFs need not be byte-identical.

## Scope
459 development-exposed internal validation images; fixed RF-DETR Small checkpoint accessed through Roboflow. Validation counts reproduce aggregate metrics, not object-level matching. Historical ten-target PNG experiment remains separate from 48 eligible reference-matched targets in 24 JPEG-95 4:4:4 validation images. Map scores are conditional on target matching and output thresholds (confidence 0.20, IoU 0.50, ambiguity margin 0.03). LOST denotes operational zero; AMBIGUOUS is missing, not zero. Signed area-normalized drops compare pooled fine cells with direct coarse cells. Bootstrap resamples 24 image clusters, 5000 fixed-seed replicates; it is descriptive only. Ten random-order AUCs per scorable target and direction are an internal diagnostic, not independent attribution fidelity. The ledger contains 4984 reservations and 4984 successes, not independent statistical observations. Numerical recomputation does not guarantee future hosted model replay, model weight access/identity, independent-site generalization, worker compliance, or causal explanations. Historical secondary progressive curves and A5/A6 target selection inputs are not included in this candidate.

## Privacy and rights
Only selected derived numerical records and vector figures, no original photographs, source identifiers, raw boxes, original weights, provider credentials or consent documents. Pseudonyms preserve study groups but do not guarantee anonymity. Institutional determination, rights/privacy review, and final author sign-off remain pending. No DOI has been assigned and this candidate has not been deposited. Do not publish until cleared. See LICENSE.md and DATA_DICTIONARY.md.
""",encoding="utf8")
    (dest/"LICENSE.md").write_text("""# Proposed licensing scope — review candidate only
Author approved MIT for code the author is entitled to license and CC BY 4.0 for eligible derived numerical data. No blanket repository license, third-party rights grant or license to the original photographs or detector weights. Before public release confirm provenance, rights and privacy, attach the full MIT license to eligible code and identify the exact data and artwork covered by CC BY 4.0. This review candidate does not itself assert that all material is cleared.
MIT: https://opensource.org/license/mit
CC BY 4.0: https://creativecommons.org/licenses/by/4.0/
""",encoding="utf8")
    (dest/"DATA_DICTIONARY.md").write_text("""# Data dictionary
CSV headers are field names. Empty cells are missing, not zero. IDs V001–V459 refer only to validation counts; I01–I24 and T01–T48 group extension targets; H01–H10 and HI01–HI08 group historical targets. No crosswalk is included.
- validation_metrics.csv: counts per image (gt, predictions, tp, fp, fn). Class-exact IoU >=0.50 matching; single-curator reference.
- validation_class_metrics.csv: counts by cohort and category; M0 459, M1 448, M2 367 images. Cohorts overlap.
- target_manifest.csv: reference IoU and confidence, actual baseline confidence, blurred endpoint score, curve and map status.
- perturbation_scores.csv: target/fill/grid/zero-based row/col; exact fraction of image area; score_after, signed score_drop, matched_iou and status.
- spatial_agreement.csv: rank rho, tau-b, top-four overlap fraction, mean absolute density difference; undefined entries empty.
- aligned_density.csv: zero-based coarse row-major region, sum of fine signed drops divided by coarse area, direct coarse drop divided by coarse area.
- operator_comparison.csv: gray/blur coefficient and status; paired_delta = blur minus gray.
- auc_results.csv: target and curve key; normalized-score trapezoidal AUC, status. Each curve has 11 points in curve_points.csv; modified_fraction is actual pixel area, requested_fraction is nominal. Ordering labels preserve ten random rankings without revealing original seed inputs.
- historical_spatial_agreement.csv and historical_aligned_density.csv: historical target agreement and aligned 4x4 region densities, not pooled with extension. historical_native_cells.csv: 8x8 and 4x4 native signed drops, areas and densities for heatmaps.
- inference_ledger.jsonl: explicit allowlisted reservation/success event types, contiguous call_index, phase, pseudonymous image/target and mask metadata when present; detection_count for successes. No original payloads or timestamps.
- figures/: 14 checked R5 vector PDFs plus conceptual schematic SVG. analysis/: scripts for archived numerical statistics and plot regeneration.
""",encoding="utf8")
    # Dependency pins for this reproduction environment, not original hosted inference.
    import importlib.metadata as md
    from packaging.requirements import Requirement
    names=set()
    todo=["numpy","matplotlib","cairosvg"]
    while todo:
        name=todo.pop()
        if name.lower() in names:continue
        names.add(name.lower())
        for spec in md.requires(name) or []:
            req=Requirement(spec)
            if req.marker is None or req.marker.evaluate({"extra":""}):todo.append(req.name)
    names=sorted(names)
    (dest/"requirements.txt").write_text("# Tested offline figure recreation dependencies; not historical hosted environment\n"+"".join(f"{k}=={md.version(k)}\n" for k in names),encoding="utf8")
    def hashes():
        fs=sorted(p for p in dest.rglob("*") if p.is_file() and p.name!="SHA256SUMS.txt")
        (dest/"SHA256SUMS.txt").write_text("".join(f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(dest).as_posix()}\n" for p in fs),encoding="utf8")
    hashes()
    result=subprocess.check_output([sys.executable,str(dest/"analysis/reproduce.py")],text=True)
    (dest/"RECOMPUTED_RESULTS.json").write_text(result,encoding="utf8")
    subprocess.run([sys.executable,str(dest/"analysis/render_figures.py")],check=True)
    shutil.rmtree(dest/"regenerated_figures")
    hashes()
    subprocess.run([sys.executable,str(dest/"analysis/reproduce.py")],check=True)
    zipname=out/"PPE_Cross_Resolution_Zenodo_REVIEW_CANDIDATE.zip"
    with zipfile.ZipFile(zipname,"w",compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for p in sorted(dest.rglob("*")):
            if p.is_file():z.write(p,p.relative_to(dest))
    with zipfile.ZipFile(zipname) as z:assert z.testzip() is None;print("ZIP_FILES",len(z.namelist()))
    print("ZIP_SHA256",hashlib.sha256(zipname.read_bytes()).hexdigest(),"BYTES",zipname.stat().st_size)
if __name__=="__main__":main()
