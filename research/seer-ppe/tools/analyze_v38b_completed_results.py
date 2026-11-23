#!/usr/bin/env python3
"""V38-B: independent, read-only final evidence audit from archived large JSON/JSONL.

Runs on GitHub Actions checkout and writes only a short numerical summary.
No model calls, no image access, no Test access and no changes to original artifacts.
"""
import hashlib
import json
import math
import random
import statistics
from collections import Counter, defaultdict
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"outputs/v38b_authorized_2026-11-23"
RESULT=OUT/"V38_B_ACTUAL_XAI_RESULTS_2026-11-23.json"
LEDGER=OUT/"V38_B_ACTUAL_XAI_RESULTS_2026-11-23.json.attempts.jsonl"
CLOSURE=OUT/"V38_B_ONE_TIME_EXECUTION_CLOSURE_2026-11-23.json"
MANIFEST=ROOT/"V38_B_FROZEN_CANDIDATE_SAMPLE_2026-11-23.json"
SUMMARY=OUT/"V38_B_FINAL_NUMERICAL_RESULTS_SUMMARY_2026-11-23.json"

def require(ok,msg):
    if not ok:raise ValueError(msg)

def mean(values):
    return statistics.mean(values) if values else None

def median(values):
    return statistics.median(values) if values else None

def descr(values):
    v=[float(x) for x in values if isinstance(x,(int,float)) and math.isfinite(float(x))]
    return {"n":len(v),"mean":mean(v),"median":median(v),"min":min(v) if v else None,
            "max":max(v) if v else None,"std_sample":statistics.stdev(v) if len(v)>1 else None}

def bootstrap_image_mean(image_values,n=5000):
    # Purely descriptive interval for purposively selected development-exposed images,
    # NOT a source-population confidence interval.
    if len(image_values)<2:
        return None
    rng=random.Random("seer-ppe/v38b-image-block-bootstrap-2026-11-23")
    k=len(image_values)
    means=[]
    for _ in range(n):
        means.append(mean([image_values[rng.randrange(k)] for j in range(k)]))
    ordered=sorted(means)
    return {"method":"fixed_seed_resample_images_with_replacement_exploratory",
            "replicates":n,"lower_2p5_percentile":ordered[int(.025*(n-1))],
            "upper_97p5_percentile":ordered[int(.975*(n-1))],
            "not_population_inference":True}

def main():
    result=json.loads(RESULT.read_text(encoding="utf8"))
    closure=json.loads(CLOSURE.read_text(encoding="utf8"))
    plan=json.loads(MANIFEST.read_text(encoding="utf8"))
    require(result["status"]=="COMPLETED","result not complete")
    require(closure["status"]=="COMPLETED","closure not complete")
    require(result["model_id"]==plan["model"]["id"],"model mismatch")
    require(result["images_processed"]==24 and len(result["per_image"])==24,"image count not 24")
    require(result["targets_total"]==48,"target count not 48")
    require(result["calls_attempted"]==result["calls_succeeded"],"unsuccessful model calls")
    require(result["calls_attempted"]==closure["calls_attempted"],"closure count mismatch")
    require(closure["calls_succeeded"]==result["calls_succeeded"],"closure success mismatch")
    require(result["calls_attempted"]<=6000,"hard limit violated")
    require(result["no_test_accessed"] is True and result["retrained"] is False,"no Test/training condition failed")
    require(result["wire_encoding"]=="JPEG_quality_95_chroma_444_fixed_all_requests","wire setup mismatch")
    require(result["frozen_plan_sha256"]==hashlib.sha256(MANIFEST.read_bytes()).hexdigest(),"frozen plan changed")

    target_rows=[]
    image_summary=[]
    all_ids=[]
    for item in result["per_image"]:
        sid=item["source_id"]
        require(item["image_key"]=="valid:"+sid,"unexpected source split")
        require(len(item["targets"])==2,"not two targets per image")
        for t in item["targets"]:
            all_ids.append(t["target_id"])
            cr=t["cross_resolution"]
            require(cr["status"] in ("AVAILABLE","AMBIGUOUS_REGION","CONSTANT_RANKS"),
                    "unknown map status")
            require(len(t["gray_map_8x8"])==64 and len(t["gray_map_4x4"])==16,
                    "incomplete map trials")
            row={"source_id":sid,"target_id":t["target_id"],
                 "class_name":t["class_name"],
                 "cross_resolution_status":cr["status"],
                 "rho":cr.get("spearman_rho"),
                 "tau":cr.get("kendall_tau_b"),
                 "top_four_overlap":cr.get("top_four_overlap_fraction"),
                 "top_four_count":cr.get("top_four_overlap_regions"),
                 "mean_abs_density_difference":cr.get("mean_absolute_density_difference"),
                 "ambiguous_8x8_trials":sum(x["status"]=="AMBIGUOUS" for x in t["gray_map_8x8"]),
                 "ambiguous_4x4_trials":sum(x["status"]=="AMBIGUOUS" for x in t["gray_map_4x4"]),
                 "lost_8x8_trials":sum(x["status"]=="LOST" for x in t["gray_map_8x8"]),
                 "lost_4x4_trials":sum(x["status"]=="LOST" for x in t["gray_map_4x4"])}
            curve=t.get("curves",{})
            row["curve_status"]=curve.get("status","NOT_SELECTED")
            if curve.get("status")=="EXECUTED":
                curves=curve["values"]
                require(len(curves)==24,"Expected 24 curves: 11 x 2 + 1 x 2")
                row["curves_available"]=sum(x["auc"] is not None for x in curves.values())
                row["curves_total"]=len(curves)
                row["curve_auc"]={key:value.get("auc") for key,value in curves.items()}
            else:
                row["curves_available"]=0
                row["curves_total"]=0
                row["curve_auc"]={}
                if curve.get("status")=="NOT_RUN":
                    row["curve_block_reasons"]=curve.get("reasons",[])
            if t.get("operator_ablation"):
                op=t["operator_ablation"].get("blur_fill",{})
                row["blur_fill_rho"]=op.get("spearman_rho")
                row["blur_fill_top_four_overlap"]=op.get("top_four_overlap_fraction")
                row["blur_fill_status"]=op.get("status")
            target_rows.append(row)
        image_summary.append({"source_id":sid,"targets":len(item["targets"])})
    require(len(target_rows)==48 and len(set(all_ids))==48,"unique target count mismatch")
    require(set(all_ids)=={x["target_id"] for x in plan["targets"]},"frozen target IDs mismatch")
    require({x["source_id"] for x in image_summary}=={x["source_id"] for x in plan["images"]},"image ID mismatch")

    # The ledger is append-only and persisted before each remote POST.
    count_by_event=Counter()
    attempt_ids=[]
    success_ids=[]
    failed_ids=[]
    with LEDGER.open(encoding="utf8") as stream:
        for line in stream:
            if not line.strip(): continue
            e=json.loads(line)
            count_by_event[e["event"]]+=1
            if e["event"]=="ATTEMPT_RESERVED":attempt_ids.append(e["call_index"])
            if e["event"]=="ATTEMPT_SUCCEEDED":success_ids.append(e["call_index"])
            if e["event"]=="ATTEMPT_FAILED":failed_ids.append(e["call_index"])
    require(attempt_ids==list(range(1,result["calls_attempted"]+1)),"ledger attempted index missing/duplicate")
    require(success_ids==attempt_ids,"success events not one-to-one")
    require(not failed_ids,"failed calls unexpectedly present")
    require(sum(count_by_event.values())==2*result["calls_attempted"],"ledger events mismatch")

    valid=[r for r in target_rows if r["cross_resolution_status"]=="AVAILABLE"]
    per_class=defaultdict(list)
    by_image=defaultdict(list)
    for r in target_rows:
        per_class[r["class_name"]].append(r)
        by_image[r["source_id"]].append(r)

    metrics={"spearman_rho":"rho","kendall_tau_b":"tau",
             "top_four_overlap_fraction":"top_four_overlap",
             "mean_absolute_density_difference":"mean_abs_density_difference"}
    rows_by_endpoint={}
    for label,field in metrics.items():
        v=[r[field] for r in target_rows if r[field] is not None]
        equal_image=[]
        for source_id,records in by_image.items():
            matched=[r[field] for r in records if r[field] is not None]
            if matched:equal_image.append(mean(matched))
        rows_by_endpoint[label]={"target_weighted":descr(v),"image_balanced":descr(equal_image),
                                 "image_bootstrap_exploratory_interval":bootstrap_image_mean(equal_image)}
    zero_overlap=sum(r.get("top_four_count")==0 for r in target_rows)
    random_results=[]
    for r in target_rows:
        if r["curve_status"]!="EXECUTED":continue
        auc=r["curve_auc"]
        for direction in ("deletion","insertion"):
            salient=auc.get(f"8x8_saliency_{direction}")
            random_vals=[auc.get(f"8x8_random_seed_{i}_{direction}") for i in range(10)]
            good=[x for x in random_vals if x is not None]
            diff=None if salient is None or not good else (salient-mean(good))
            random_results.append({"target_id":r["target_id"],"direction":direction,
                                   "saliency_auc":salient,"random_valid":len(good),
                                   "random_auc_mean":mean(good),"saliency_minus_random_mean_auc":diff,
                                   "four_by_four_saliency_auc":auc.get(f"4x4_saliency_{direction}")})
    class_summary={}
    for cls,rr in sorted(per_class.items()):
        class_summary[cls]={"targets":len(rr),
                            "rho":descr([r["rho"] for r in rr]),
                            "top_four_overlap":descr([r["top_four_overlap"] for r in rr]),
                            "ambiguous_map_trials":sum(r["ambiguous_8x8_trials"]+r["ambiguous_4x4_trials"] for r in rr)}
    ablations=[r for r in target_rows if "blur_fill_rho" in r]
    summary={
        "schema_version":"seer-ppe/v38b-independent-actual-numeric-summary/v1",
        "status":"AUDITED_COMPLETE_REAL_INFERENCE",
        "source":"Original complete numeric evidence from frozen V38-B actual one-time GitHub Actions execution",
        "source_run_url":"https://github.com/EZZALDEEN049/Y-PPE-Detection-RFDETR/actions/runs/45085935253",
        "source_result_git_blob_sha":"aff9f7dc6c754e79d0af75a071a94bbba4338b6e",
        "model_id":result["model_id"],"study":"development_exposed_Validation_diagnostic",
        "images_processed":result["images_processed"],"targets_processed":len(target_rows),
        "target_status_counts":dict(Counter(x["cross_resolution_status"] for x in target_rows)),
        "attempted_model_calls":result["calls_attempted"],
        "succeeded_model_calls":result["calls_succeeded"],
        "hard_cap":6000,"planned_cap":5200,
        "calls_remaining_below_hard_cap":6000-result["calls_attempted"],
        "ledger_event_counts":dict(count_by_event),
        "all_attempts_contiguous":True,
        "endpoint_metrics":rows_by_endpoint,
        "zero_top_four_overlap_targets":zero_overlap,
        "class_metrics":class_summary,
        "ablation":{"targets_with_blur_fill_measurement":len(ablations),
                    "blur_fill_rho":descr([r["blur_fill_rho"] for r in ablations]),
                    "blur_fill_overlap":descr([r["blur_fill_top_four_overlap"] for r in ablations])},
        "progressive_curves":{"targets_executed":sum(r["curve_status"]=="EXECUTED" for r in target_rows),
                              "targets_blocked":sum(r["curve_status"]=="NOT_RUN" for r in target_rows),
                              "auc_curves_total":sum(r["curves_total"] for r in target_rows),
                              "auc_curves_available":sum(r["curves_available"] for r in target_rows),
                              "random_baseline_target_direction_results":random_results},
        "individual_target_numeric_rows":target_rows,
        "scientific_limits":["Historical V26 baseline and V38B use previously development-exposed Validation images; not independent external field sites.",
                             "Spearman and Kendall rank agreement do not prove causal explanation fidelity or PPE safety compliance.",
                             "Descriptive bootstrap of 24 selected images does not establish population coverage.",
                             "Different grid-cell occlusions have nonlinear interactions; area normalization does not remove confounding.",
                             "JPEG 95 4:4:4 wire encoding may affect sensitivity; older PNG-based V30/V33 results are not directly pooled."]
    }
    SUMMARY.write_text(json.dumps(summary,ensure_ascii=False,indent=2,allow_nan=False)+"\n",encoding="utf8")
    compact={k:summary[k] for k in ["status","images_processed","targets_processed","target_status_counts",
                                    "attempted_model_calls","succeeded_model_calls",
                                    "calls_remaining_below_hard_cap","endpoint_metrics",
                                    "zero_top_four_overlap_targets","ablation"]}
    compact["progressive_curves"]={k:v for k,v in summary["progressive_curves"].items() if k!="random_baseline_target_direction_results"}
    print(json.dumps(compact,ensure_ascii=False,indent=2,allow_nan=False))
if __name__=="__main__":
    main()
