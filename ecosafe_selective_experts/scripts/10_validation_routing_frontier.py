#!/usr/bin/env python3
"""Validation-only descriptive frontier for actual primary-first joint NMS escalation.

NO router training, NO threshold selection, NO heldout TEST access, NO energy
measurement. Score uses ONLY primary predictions, never GT/secondary predictions.
"""
from __future__ import annotations
import argparse
import json
from collections import Counter
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

from object_level_safety_oracle import matched_gt_indices, SAFETY

spec=spec_from_file_location("fusion_aggregate",Path(__file__).with_name("09_validation_fusion_report.py"))
fusion=module_from_spec(spec)
spec.loader.exec_module(fusion)

SCORES=("all_confidence_uncertainty","safety_confidence_uncertainty")
THRESHOLDS=(0.0,0.25,0.5,0.75,1.0)


def primary_score(primary_predictions, rule):
    """[0,1] confidence-based uncertainty; no GT or secondary access."""
    if rule not in SCORES:
        raise ValueError("Routing signal not predeclared.")
    if rule=="all_confidence_uncertainty":
        vals=[p["confidence"] for p in primary_predictions]
    else:
        vals=[p["confidence"] for p in primary_predictions if p["class_id"] in SAFETY]
    if any(not 0<=x<=1 for x in vals):
        raise ValueError("Invalid primary confidence.")
    return 1.0-max(vals) if vals else 1.0


def metrics(total_gt,tp,fp,escalated,frames):
    if total_gt<=0 or frames<=0:
        raise ValueError("Insufficient annotated safety ground truth.")
    return {
        "tp":tp, "fn":total_gt-tp,"fp":fp,
        "critical_recall":tp/total_gt,
        "precision":tp/(tp+fp) if tp+fp else None,
        "escalated_frames":escalated,
        "escalation_rate":escalated/frames,
        "expert_executions_proxy_per_image":1.0+escalated/frames,
    }


def calculate_frontier(gt_by_image, primary_by_image, secondary_by_image):
    if not gt_by_image or set(gt_by_image)!=set(primary_by_image) or set(gt_by_image)!=set(secondary_by_image):
        raise ValueError("Primary, secondary and ground-truth frames differ.")
    scored=[]
    total_gt=0
    for name in sorted(gt_by_image):
        gt=gt_by_image[name]
        if any(g["class_id"] not in SAFETY for g in gt):
            raise ValueError("Non-safety GT supplied.")
        total_gt+=len(gt)
        p=[x for x in primary_by_image[name] if x["class_id"] in SAFETY and x["confidence"]>=0.25]
        s=[x for x in secondary_by_image[name] if x["class_id"] in SAFETY and x["confidence"]>=0.25]
        both=fusion.class_nms(p+s,0.70)
        pm=matched_gt_indices(gt,[{"class_id":x["class_id"],"box":x["box"]} for x in p],0.50)
        jm=matched_gt_indices(gt,[{"class_id":x["class_id"],"box":x["box"]} for x in both],0.50)
        scored.append({
            "ptp":len(pm),"jtp":len(jm),
            "pfp":len(p)-len(pm),"jfp":len(both)-len(jm),
            "score_all":primary_score(primary_by_image[name],SCORES[0]),
            "score_safety":primary_score(primary_by_image[name],SCORES[1]),
        })
    n=len(scored)
    reference_tp=sum(x["jtp"] for x in scored)
    reference_fp=sum(x["jfp"] for x in scored)
    base_tp=sum(x["ptp"] for x in scored)
    base_fp=sum(x["pfp"] for x in scored)
    output={
        "type":"development_only_exploratory_not_threshold_selection",
        "policy":"primary_plus_secondary_when_escalated_class_aware_joint_NMS_0.70",
        "validation_frames":n,"critical_gt_objects":total_gt,
        "heldout_test_used":False,"router_trained":False,
        "inference_energy_measured":False,
        "primary_alone":metrics(total_gt,base_tp,base_fp,0,n),
        "always_run_both":metrics(total_gt,reference_tp,reference_fp,n,n),
        "frontiers":{},
        "limitations":[
            "Exploratory thresholds are not a prespecified final router policy.",
            "No statistical safety non-inferiority conclusion or operational minimum recall is established.",
            "Invocation count is a compute proxy, not measured latency, power or carbon.",
            "False-positive counts depend on class-aware maximum-cardinality GT matching."
        ]
    }
    for signal,field in ((SCORES[0],"score_all"),(SCORES[1],"score_safety")):
        rows=[]
        for t in THRESHOLDS:
            esc=[x[field]>=t for x in scored]
            tp=sum(x["jtp"] if choose else x["ptp"] for choose,x in zip(esc,scored))
            fp=sum(x["jfp"] if choose else x["pfp"] for choose,x in zip(esc,scored))
            observed=metrics(total_gt,tp,fp,sum(esc),n)
            r=observed["escalation_rate"]
            expected_random_tp=(1-r)*base_tp+r*reference_tp
            observed.update({
                "uncertainty_threshold":t,
                "expected_random_routing_recall_at_same_rate":expected_random_tp/total_gt,
                "recall_gap_vs_always_both":output["always_run_both"]["critical_recall"]-observed["critical_recall"],
            })
            rows.append(observed)
        output["frontiers"][signal]=rows
    return output


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--validation-root",required=True,type=Path)
    p.add_argument("--private-chunks",required=True,type=Path)
    p.add_argument("--domain",choices=("y","c"),required=True)
    p.add_argument("--seed",choices=(17,42,2026),type=int,required=True)
    p.add_argument("--out",type=Path,required=True)
    args=p.parse_args()
    try:
        d,n,digest=fusion.DOMAINS[args.domain]
        root=args.validation_root/d
        if fusion._locked.sha256(root/"manifest.jsonl")!=digest:
            raise ValueError("Frozen validation manifest failed.")
        images=sorted([q for q in (root/"images"/"val").iterdir() if q.is_file()
                       and q.suffix.lower() in (".jpg",".jpeg",".png")],key=lambda p:p.name)
        if len(images)!=n:
            raise ValueError("Unexpected development image count.")
        names=[p.name for p in images]
        y=fusion.read_complete_chunks(args.private_chunks,f"Y_YOLO_s{args.seed}",args.domain,names)
        c=fusion.read_complete_chunks(args.private_chunks,f"C_YOLO_s{args.seed}",args.domain,names)
        gt={p.name:fusion.read_labels(root/"labels"/"val"/(p.stem+".txt")) for p in images}
        reports={
            "Y_primary":calculate_frontier(gt,y,c),
            "Construction_primary":calculate_frontier(gt,c,y),
        }
        report={"domain":args.domain,"seed":args.seed,"frozen_manifest_sha256":digest,
                "exploratory_frontiers":reports}
    except (OSError,ValueError,TypeError,KeyError) as exc:
        raise SystemExit("ROUTING_FRONTIER_BLOCKED: "+type(exc).__name__)
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"domain":args.domain,"seed":args.seed,
                     "development_only":True,"router_trained":False,
                     "test_used":False,"energy_measured":False}))


if __name__=="__main__":main()
