#!/usr/bin/env python3
"""Privacy-safe GT-privileged secondary-expert opportunity audit.

DEVELOPMENT/VALIDATION ONLY. The oracle consults GT after prediction and is
NOT a deployable routing method. AUC is descriptive, not calibrated safety,
held-out performance, causal evidence, energy or an optimal threshold.

The input reader is the locked 12_best_validation_fusion_report.py preflight;
only anonymized per-domain/seed/direction aggregate counts leave this process.
"""
from __future__ import annotations
import argparse
import json
import math
from pathlib import Path
from importlib.util import module_from_spec, spec_from_file_location


def import_best_report():
    spec = spec_from_file_location(
        "locked_best_report", Path(__file__).with_name("12_best_validation_fusion_report.py"))
    mod = module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def auc_rank(labels, scores):
    """Tied-rank Mann-Whitney AUC, or None when a class is absent."""
    if not labels or len(labels) != len(scores):
        raise ValueError("AUC sample malformed.")
    if any(type(x) is not bool for x in labels):
        raise ValueError("AUC labels must be Boolean.")
    if any(not math.isfinite(s) or not 0 <= s <= 1 for s in scores):
        raise ValueError("Non-finite or invalid confidence score.")
    npos=sum(labels)
    nneg=len(labels)-npos
    if not npos or not nneg:
        return None
    ranked=sorted(zip(scores,labels),key=lambda x:x[0])
    score_sum=0.0
    pos=0
    while pos<len(ranked):
        end=pos+1
        while end<len(ranked) and ranked[end][0]==ranked[pos][0]:
            end+=1
        score_sum+=((pos+1+end)/2.0)*sum(x for _,x in ranked[pos:end])
        pos=end
    return (score_sum-npos*(npos+1)/2)/(npos*nneg)


def score_frame(gt, primary, secondary, matcher, nms, cutoff=0.25):
    """GT only scores retrospectively; decisions never feed a real model."""
    if not 0<cutoff<=1:
        raise ValueError("Invalid fixed operating confidence.")
    if any(g["class_id"] not in (6,7,8) for g in gt):
        raise ValueError("Unexpected non-safety GT.")
    if any(not math.isfinite(p["confidence"]) or not 0<=p["confidence"]<=1
           for p in primary+secondary):
        raise ValueError("Invalid prediction confidence.")
    safe=(6,7,8)
    p=[x for x in primary if x["class_id"] in safe and x["confidence"]>=cutoff]
    s=[x for x in secondary if x["class_id"] in safe and x["confidence"]>=cutoff]
    both=nms(p+s,0.70)
    # Match only anonymized class-aware prediction boxes, never identifiers.
    matching=lambda preds:len(matcher(gt,[{"class_id":d["class_id"],"box":d["box"]}
                                       for d in preds],threshold=0.50))
    p_tp=matching(p)
    joint_tp=matching(both)
    concat_tp=matching(p+s)
    if concat_tp < max(p_tp,joint_tp):
        raise ValueError("Union upper-bound consistency failure.")
    return {
        "gt":len(gt), "primary_tp":p_tp, "joint_tp":joint_tp,
        "concat_upper_tp":concat_tp,
        "primary_fp":len(p)-p_tp,"joint_fp":len(both)-joint_tp,
        "uncertainty_all":1.0-max((x["confidence"] for x in primary),default=0.0),
        "uncertainty_safety":1.0-max((x["confidence"] for x in primary
                                     if x["class_id"] in safe),default=0.0),
    }


def summarise(frames):
    """Bound required escalations with an explicitly GT-privileged oracle."""
    if not frames:
        raise ValueError("No frames.")
    total_gt=sum(f["gt"] for f in frames)
    if not total_gt:
        raise ValueError("No critical GT denominator.")
    primary=sum(f["primary_tp"] for f in frames)
    joint=sum(f["joint_tp"] for f in frames)
    ceiling=sum(f["concat_upper_tp"] for f in frames)
    pfp=sum(f["primary_fp"] for f in frames)
    jfp=sum(f["joint_fp"] for f in frames)
    gains=[f["joint_tp"]-f["primary_tp"] for f in frames]
    useful=[i for i,g in enumerate(gains) if g>0]
    harmful=[i for i,g in enumerate(gains) if g<0]
    gain=sum(gains[i] for i in useful)
    loss=-sum(gains[i] for i in harmful)
    if joint-primary!=gain-loss:
        raise ValueError("Inconsistent frame scoring.")
    privileged_tp=primary+gain
    privileged_fp=pfp+sum(frames[i]["joint_fp"]-frames[i]["primary_fp"] for i in useful)
    if not primary<=privileged_tp<=ceiling:
        raise ValueError("Privileged bound invalid.")
    minimal_calls=0
    needed=max(0,joint-primary)
    for v in sorted((gains[i] for i in useful),reverse=True):
        if needed<=0:
            break
        needed-=v
        minimal_calls+=1
    if needed>0:
        raise ValueError("Unachievable always-joint TP.")
    n=len(frames)
    rate=len(useful)/n
    labels=[g>0 for g in gains]
    useful_set=set(useful)
    return {
        "validation_frames":n, "critical_gt_objects":total_gt,
        "primary_tp":primary,"primary_fp":pfp,
        "always_joint_tp":joint,"always_joint_fp":jfp,
        "concat_recall_ceiling_tp":ceiling,
        "net_joint_minus_primary_tp":joint-primary,
        "positive_delta_frames":len(useful),
        "negative_delta_frames":len(harmful),
        "positive_delta_objects":gain,
        "negative_delta_objects":loss,
        "positive_frame_fraction":rate,
        "joint_fp_change_outside_positive_delta_frames":sum(
            f["joint_fp"]-f["primary_fp"] for i,f in enumerate(frames) if i not in useful_set),
        "privileged_gt_oracle":{
            "secondary_calls_to_score_every_positive_gain_frame":len(useful),
            "minimal_calls_to_match_total_always_joint_tp":minimal_calls,
            "total_tp_by_only_escalating_positive_gain_frames":privileged_tp,
            "total_fp_by_only_escalating_positive_gain_frames":privileged_fp,
            "theoretical_calls_per_frame_proxy":1+rate,
            "not_deployable":True,
        },
        "same_rate_random_routing_expected_tp":(1-rate)*primary+rate*joint,
        "primary_uncertainty_auc_for_positive_delta_frames":{
            "all_detection_confidence":auc_rank(labels,[f["uncertainty_all"] for f in frames]),
            "safety_only_confidence":auc_rank(labels,[f["uncertainty_safety"] for f in frames]),
        },
        "roc_auc_has_no_final_calibration_or_test_generalization":True,
    }


def evaluate_domain(best, validation_root, private_chunks, domain):
    dataset,n,fingerprint=best.DOMAINS[domain]
    root=validation_root/dataset
    if best._locked.sha256(root/"manifest.jsonl")!=fingerprint:
        raise ValueError("Frozen validation manifest mismatch.")
    image_paths=sorted((q for q in (root/"images"/"val").iterdir()
                       if q.is_file() and q.suffix.lower() in (".jpg",".jpeg",".png")),
                       key=lambda p:p.name)
    if len(image_paths)!=n or len({q.stem for q in image_paths})!=n:
        raise ValueError("Frozen image coverage mismatch.")
    names=[q.name for q in image_paths]
    gt={q.name:best.read_labels(root/"labels"/"val"/(q.stem+".txt")) for q in image_paths}
    result={"source_manifest_sha256":fingerprint,"validation_frames":n,"seeds":{}}
    for seed in (17,42,2026):
        y=best.read_complete_chunks(private_chunks,f"Y_YOLO_s{seed}",domain,names)
        c=best.read_complete_chunks(private_chunks,f"C_YOLO_s{seed}",domain,names)
        by_direction={}
        for label,p,s in (("Y_primary",y,c),("Construction_primary",c,y)):
            scored=[score_frame(gt[nm],p[nm],s[nm],best.matched_gt_indices,best.class_nms)
                    for nm in names]
            by_direction[label]=summarise(scored)
        result["seeds"][str(seed)]=by_direction
    return result


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--validation-root",type=Path,required=True)
    parser.add_argument("--private-chunks",type=Path,required=True)
    parser.add_argument("--out",type=Path,required=True)
    args=parser.parse_args()
    try:
        best=import_best_report()
        result={
            "scope":"best.pt six-expert development-only nondeployable oracle",
            "heldout_test_accessed":False,"router_training":False,
            "threshold_selected":False,"energy_measured":False,
            "source_group_independence_established":False,
            "operating_confidence":0.25,
            "gt_matching_iou":0.50,
            "joint_nms_iou":0.70,
            "domains":{d:evaluate_domain(best,args.validation_root,args.private_chunks,d)
                       for d in ("y","c")},
        }
        args.out.parent.mkdir(parents=True,exist_ok=True)
        if args.out.exists():
            raise ValueError("Do not overwrite existing scientific aggregate.")
        args.out.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
        print(json.dumps({"valid":True,"validation_only":True,
             "domain_count":2,"seeds_per_domain":3,
             "source_group_independence_established":False,
             "energy_measured":False}))
    except (ValueError, OSError, TypeError, KeyError) as exc:
        # Never disclose user-private frame/image identifiers or paths.
        raise SystemExit("ECO_SAFE_PRIVILEGED_GATE_BLOCKED: "+type(exc).__name__)


if __name__=="__main__":
    main()
