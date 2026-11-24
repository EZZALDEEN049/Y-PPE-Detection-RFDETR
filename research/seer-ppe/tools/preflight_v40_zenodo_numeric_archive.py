#!/usr/bin/env python3
"""Build a temporary rights-pending numerical archive preview; never upload or call a model.
Run on an existing research checkout. Outputs are not release-cleared.
"""
import argparse, csv, hashlib, json, math, random, re, statistics as st
from collections import defaultdict, Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"outputs/v38b_authorized_2026-11-23"
SUB=ROOT/"submissions/results-in-engineering"
def load(p): return json.loads(p.read_text(encoding="utf8"))
def near(a,b):
    assert a is not None and b is not None and math.isclose(a,b,abs_tol=1e-12,rel_tol=1e-12),(a,b)
def csvfile(p, rows):
    assert rows and all(set(r)==set(rows[0]) for r in rows),p.name
    with p.open("w",encoding="utf8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def ranks(xs):
    order=sorted(range(len(xs)),key=lambda i:(xs[i],i));r=[0.]*len(xs);i=0
    while i<len(xs):
        j=i+1
        while j<len(xs) and xs[order[j]]==xs[order[i]]:j+=1
        for k in order[i:j]:r[k]=(i+1+j)/2
        i=j
    return r
def rho(xs,ys):
    a,b=ranks(xs),ranks(ys);am,bm=st.mean(a),st.mean(b)
    den=math.sqrt(sum((v-am)**2 for v in a)*sum((v-bm)**2 for v in b))
    return sum((x-am)*(y-bm) for x,y in zip(a,b))/den if den else None
def tau(xs,ys):
    c=d=t=u=0
    for i in range(len(xs)):
        for j in range(i+1,len(xs)):
            x=(xs[i]>xs[j])-(xs[i]<xs[j]);y=(ys[i]>ys[j])-(ys[i]<ys[j])
            if x==y==0:continue
            if x==0:t+=1
            elif y==0:u+=1
            elif x==y:c+=1
            else:d+=1
    den=math.sqrt((c+d+t)*(c+d+u));return (c-d)/den if den else None
def overlap(a,b):
    return len(set(sorted(range(16),key=lambda i:(-a[i],i))[:4])&set(sorted(range(16),key=lambda i:(-b[i],i))[:4]))/4
def aligned(fine,coarse):
    if any(x["score_drop"] is None for x in fine+coarse):return None
    f={(x["row"],x["col"]):x for x in fine};g={(x["row"],x["col"]):x for x in coarse}
    a=[];b=[]
    for r in range(4):
        for c in range(4):
            area=g[r,c]["area_fraction"];children=[f[2*r+i,2*c+j] for i in range(2) for j in range(2)]
            near(sum(x["area_fraction"] for x in children),area)
            a.append(sum(x["score_drop"] for x in children)/area);b.append(g[r,c]["score_drop"]/area)
    return a,b
def main():
    p=argparse.ArgumentParser();p.add_argument("--output-dir",required=True,type=Path);a=p.parse_args();dest=a.output_dir.resolve()
    assert not dest.exists(),"use a fresh, temporary output directory"
    dest.mkdir(parents=True)
    plan=load(ROOT/"V38_B_FROZEN_CANDIDATE_SAMPLE_2026-11-23.json")
    summary=load(OUT/"V38_B_FINAL_NUMERICAL_RESULTS_SUMMARY_2026-11-23.json")
    raw=load(OUT/"V38_B_ACTUAL_XAI_RESULTS_2026-11-23.json")
    v26=load(ROOT/"ACTUAL_CURRENT_SOURCE_ORIGINAL_VALID_459_CLASS_BBOX_METRICS_V26.json")
    v26s=load(ROOT/"V26_VALID_CURRENT_SOURCE_459_NUMERIC_SUMMARY.json")
    history=load(ROOT/"V34A_SPATIAL_MAP_ALIGNMENT_RANK_CORRELATION_2026-11-22.json")
    assert len(v26["per_source"])==459
    vrows=[]
    for i,r in enumerate(v26["per_source"],1):
        assert r["tp"]+r["fn"]==r["reference_boxes"] and r["tp"]+r["fp"]==r["model_boxes"]
        vrows.append(dict(validation_image=f"V{i:03}",gt=r["reference_boxes"],predictions=r["model_boxes"],tp=r["tp"],fp=r["fp"],fn=r["fn"]))
    assert [sum(r[k] for r in vrows) for k in ("gt","predictions","tp","fp","fn")]==[3471,4103,3297,806,174]
    csvfile(dest/"validation_metrics.csv",vrows)
    vc=[]
    for cohort,d in v26s["cohorts"].items():
        for r in d["per_class"]:
            vc.append(dict(cohort=cohort,category=r["class_name"],gt=r["GT"],predictions=r["pred"],tp=r["TP"],fp=r["FP"],fn=r["FN"]))
    csvfile(dest/"validation_class_metrics.csv",vc)
    # Only summary-order pseudonyms; no source IDs, hashes of individual images, boxes or original filenames.
    sources={}; targets={}; pm={r["target_id"]:r for r in plan["targets"]}
    for i,r in enumerate(summary["individual_target_numeric_rows"],1):
        sources.setdefault(r["source_id"],f"I{len(sources)+1:02}")
        targets[r["target_id"]]=f"T{i:02}"
    assert len(sources)==24 and len(targets)==48
    sm={r["target_id"]:r for r in summary["individual_target_numeric_rows"]}
    manifest=[];maps=[];spatial=[];aucs=[];points=[];ops=[];densities=[]
    for im in raw["per_image"]:
        sid=im["source_id"];alias=sources[sid]
        for t in im["targets"]:
            tid=t["target_id"];tag=targets[tid];r=sm[tid];f=pm[tid]
            manifest.append(dict(target=tag,image_cluster=alias,category=t["class_name"],
                archived_baseline=f["baseline_confidence_from_v26"],reference_iou=f["baseline_author_reference_iou"],
                actual_baseline=t["baseline"]["confidence"],baseline_status=t["baseline"]["status"],
                blurred_endpoint=t["blurred_endpoint"]["score"],blurred_endpoint_status=t["blurred_endpoint"]["status"],
                curve_status=r["curve_status"],gray_status=r["cross_resolution_status"]))
            for fill,keys in (("gray",("gray_map_8x8","gray_map_4x4")),("blur",("blur_fill_map_8x8","blur_fill_map_4x4"))):
                fine,coarse=(t[k] for k in keys)
                if fine is None:assert coarse is None;continue
                assert len(fine)==64 and len(coarse)==16
                for g,rs in ((8,fine),(4,coarse)):
                    for x in rs:
                        maps.append(dict(target=tag,image_cluster=alias,fill=fill,grid=g,row=x["row"],col=x["col"],
                            area_fraction=x["area_fraction"],status=x["status"],score_after=x["score_after"],
                            score_drop=x["score_drop"],matched_iou=x["matched_iou"]))
                cr=t["cross_resolution"] if fill=="gray" else t["operator_ablation"]["blur_fill"]
                pair=aligned(fine,coarse)
                if pair is None:assert cr["status"]=="AMBIGUOUS_REGION"
                else:
                    x,y=pair
                    near(rho(x,y),cr["spearman_rho"]);near(tau(x,y),cr["kendall_tau_b"]);near(overlap(x,y),cr["top_four_overlap_fraction"])
                    for k,(v,w) in enumerate(zip(x,y)):densities.append(dict(target=tag,fill=fill,region=k,pooled_fine=v,direct_coarse=w))
            spatial.append(dict(target=tag,image_cluster=alias,category=r["class_name"],status=r["cross_resolution_status"],
                rho=r["rho"],tau_b=r["tau"],top_four_overlap=r["top_four_overlap"],mean_abs_density_difference=r["mean_abs_density_difference"]))
            if "blur_fill_status" in r:ops.append(dict(target=tag,image_cluster=alias,gray_status=r["cross_resolution_status"],
                blur_status=r["blur_fill_status"],gray_rho=r["rho"],blur_rho=r["blur_fill_rho"],
                paired_delta=None if r["rho"] is None or r["blur_fill_rho"] is None else r["blur_fill_rho"]-r["rho"]))
            if t["curves"].get("status")=="EXECUTED":
                for label,curve in t["curves"]["values"].items():
                    q=curve["points"];assert len(q)==11
                    z=sum((b["modified_fraction"]-a["modified_fraction"])*(a["normalized_score"]+b["normalized_score"])/2 for a,b in zip(q,q[1:]))
                    near(z,curve["auc"]);near(z,r["curve_auc"][label])
                    aucs.append(dict(target=tag,curve=label,auc=curve["auc"],status=curve["status"]))
                    for i,x in enumerate(q):
                        points.append(dict(target=tag,curve=label,point_index=i,direction=x["direction"],ordering=x["ordering"],
                            requested_fraction=x["requested_fraction"],modified_fraction=x["modified_fraction"],
                            target_confidence=x["target_confidence"],normalized_score=x["normalized_score"],match_status=x["match_status"],matched_iou=x["matched_iou"]))
    assert [len(manifest),len(maps),len(spatial),len(aucs),len(points),len(ops)]==[48,5120,48,264,2904,16]
    valid=[r for r in spatial if r["rho"] is not None];assert len(valid)==45
    near(st.mean(r["rho"] for r in valid),.6489788814589973)
    groups=defaultdict(list)
    for r in valid:groups[r["image_cluster"]].append(r["rho"])
    im=[st.mean(groups[f"I{i:02}"]) for i in range(1,25)]
    near(st.mean(im),.6507583876423197)
    rng=random.Random("seer-ppe/v38b-image-block-bootstrap-2026-11-23")
    boot=sorted(st.mean(im[rng.randrange(24)] for _ in im) for _ in range(5000))
    near(boot[int(.025*4999)],.5949574145556713);near(boot[int(.975*4999)],.7043504901960784)
    paired=[r for r in ops if r["paired_delta"] is not None];assert len(paired)==14
    near(st.mean(r["gray_rho"] for r in paired),.6942587984819544);near(st.mean(r["blur_rho"] for r in paired),.4810924369747899)
    for fname,rs in (("target_manifest.csv",manifest),("perturbation_scores.csv",maps),("spatial_agreement.csv",spatial),
            ("aligned_density.csv",densities),("auc_results.csv",aucs),("curve_points.csv",points),("operator_comparison.csv",ops)):
        csvfile(dest/fname,rs)
    # Historical aligned data kept separate, not pooled with extension.
    order=[4,2,3,8,6,9,1,5,0,7];hist=[];hr=[]
    by={r["target_id"]:r for r in history["per_target_aligned_maps"]};hg={}
    for i,j in enumerate(order,1):
        t=history["per_target"][j];h=by[t["target_id"]];tag=f"H{i:02}"
        hg.setdefault(t["image_key"],f"HI{len(hg)+1:02}")
        x=h["pooled_8x8_signed_drop_per_area_row_major"];y=h["direct_4x4_signed_drop_per_area_row_major"]
        near(rho(x,y),t["spearman_rho_signed_area_normalized"]);near(tau(x,y),t["kendall_tau_b_signed_area_normalized"])
        near(overlap(x,y),t["top4_signed_region_overlap_fraction"])
        hr.append(dict(target=tag,image_cluster=hg[t["image_key"]],split=t["split"],category=t["target_class"],rho=rho(x,y),tau_b=tau(x,y),top_four_overlap=overlap(x,y)))
        for k,(v,w) in enumerate(zip(x,y)):hist.append(dict(target=tag,region=k,pooled_fine=v,direct_coarse=w))
    near(st.mean(r["rho"] for r in hr),.5415659018474591)
    csvfile(dest/"historical_spatial_agreement.csv",hr);csvfile(dest/"historical_aligned_density.csv",hist)
    # Explicit field allowlist; never copy arbitrary payloads, paths, timestamps, credentials or IDs.
    ledger=OUT/"V38_B_ACTUAL_XAI_RESULTS_2026-11-23.json.attempts.jsonl"
    reserved=[];succeeded=[];counts=Counter()
    with ledger.open(encoding="utf8") as f,(dest/"inference_ledger.jsonl").open("w",encoding="utf8") as o:
        for line in f:
            if not line.strip():continue
            e=json.loads(line);event=e["event"];idx=e["call_index"];counts[event]+=1
            rec={"event":event,"call_index":idx}
            if event=="ATTEMPT_RESERVED":
                reserved.append(idx)
                assert e["phase"] in ("map","curve","original_baseline","blurred_endpoint")
                rec["phase"]=e["phase"]
                if "source_id" in e:rec["image_cluster"]=sources[e["source_id"]]
                if "target_id" in e:rec["target"]=targets[e["target_id"]]
                for k in ("grid","fill","row","col","ordering","direction"):
                    if k in e:rec[k]=e[k]
            elif event=="ATTEMPT_SUCCEEDED":
                succeeded.append(idx);rec["detection_count"]=int(e["detection_count"])
            else:raise AssertionError("unexpected ledger event")
            o.write(json.dumps(rec,ensure_ascii=False,allow_nan=False)+"\n")
    assert reserved==succeeded==list(range(1,4985))
    tokens=set(sources)|set(targets)|{r["source_id"] for r in v26["per_source"]}|set(hg)|set(by)
    for file in dest.iterdir():
        s=file.read_text(encoding="utf8")
        assert not any(t in s for t in tokens if len(t)>9),file.name
        assert not re.search(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b",s,re.I),file.name
    files={p.name:{"sha256":hashlib.sha256(p.read_bytes()).hexdigest(),"rows":sum(1 for _ in p.open(encoding="utf8"))-(p.suffix==".csv")} for p in sorted(dest.iterdir())}
    (dest/"SHA256SUMS.txt").write_text("".join(f'{v["sha256"]}  {k}\n' for k,v in files.items()),encoding="utf8")
    print(json.dumps({"status":"INTERNAL_NUMERIC_PREFLIGHT_PASS_NOT_RELEASE_CLEARED","files":files,
        "validation_images":459,"extension_targets":48,"image_clusters":24,"valid_rho":45,"paired_operator":14,
        "curve_auc":264,"curve_points":2904,"map_cells":5120,"ledger_events":dict(counts),"historical_targets":10,
        "numeric_reproduction":"PASS","new_model_calls":0,"public_release":False},indent=2))
if __name__=="__main__":main()
