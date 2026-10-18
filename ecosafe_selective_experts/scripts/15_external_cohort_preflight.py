#!/usr/bin/env python3
"""Metadata-only external PPE cohort preflight: NO image or model evaluation.

PRIVATE JSON input files contain source group IDs and hashes; NEVER publish.
This tests asserted capture provenance and ontology, not empirical safety.
"""
from __future__ import annotations
import argparse
import json
import re
from collections import Counter
from pathlib import Path

CLASSES=("no_helmet","no_gloves","no_boots")
HEX=re.compile(r"^[0-9a-f]{64}$")
GROUPS=("original_family_key","site_key","camera_key","session_key")


def evaluate(candidate,historical):
    if not isinstance(candidate,dict) or not isinstance(historical,dict):
        raise ValueError("Missing source manifest")
    if not candidate.get("source_origin") or candidate["source_origin"]==historical.get("source_origin"):
        raise ValueError("New source identity unverified")
    requirements={
      "rights_review":"research_use_documented",
      "object_geometry_review":"confirmed_comparable_no_helmet_no_gloves_no_boots",
      "annotation_quality_review":"completed_before_inference",
      "policy_lock":"independent_external_confirmatory_not_used_for_model_selection",
      "historical_stage6_excluded":True,
      "original_capture_attestation":"verified_with_dataset_steward",
    }
    if any(candidate.get(k)!=v for k,v in requirements.items()):
        raise ValueError("Research/ontology/steward gate blocked")
    namespace=candidate.get("source_group_namespace")
    if not isinstance(namespace,str) or len(namespace)<4 or namespace!=historical.get("source_group_namespace"):
        raise ValueError("Capture group namespaces not comparable")
    current=candidate.get("records")
    old=historical.get("records")
    if not isinstance(current,list) or not current or not isinstance(old,list) or not old:
        raise ValueError("Missing original capture registry")
    seen_old,seen_new=set(),set()
    groups_old={k:set() for k in GROUPS}
    groups_new={k:set() for k in GROUPS}
    class_total=Counter()
    class_sites={k:set() for k in CLASSES}
    for kind,rows,seen,groups in (("old",old,seen_old,groups_old),("new",current,seen_new,groups_new)):
        for row in rows:
            if not isinstance(row,dict):
                raise ValueError("Malformed registry record")
            digest=row.get("sha256")
            if not isinstance(digest,str) or HEX.fullmatch(digest) is None or digest in seen:
                raise ValueError("Invalid/repeated image hash")
            seen.add(digest)
            for k in GROUPS:
                value=row.get(k)
                if not isinstance(value,str) or not value.strip() or value.strip().upper()=="UNKNOWN":
                    raise ValueError("Original capture metadata unknown")
                groups[k].add(value)
            if kind=="new":
                counts=row.get("gt_critical_count")
                if not isinstance(counts,dict) or set(counts)!=set(CLASSES):
                    raise ValueError("Three critical class box ontologies not equivalent")
                for cls in CLASSES:
                    v=counts[cls]
                    if type(v) is not int or v<0:
                        raise ValueError("Invalid GT count")
                    class_total[cls]+=v
                    if v:
                        class_sites[cls].add(row["site_key"])
    if seen_old.intersection(seen_new):
        raise ValueError("Original study image hash overlap")
    if any(groups_old[k].intersection(groups_new[k]) for k in GROUPS):
        raise ValueError("Previously scored capture group overlap")
    if len(groups_new["site_key"])<2 or any(not class_total[k] or len(class_sites[k])<2 for k in CLASSES):
        raise ValueError("Too few independent site groups or critical examples")
    return {
      "status":"metadata_preflight_pass_not_test_authorization",
      "no_model_inference":True,"images":len(current),
      "verified_site_group_count":len(groups_new["site_key"]),
      "critical_gt_counts":{k:class_total[k] for k in CLASSES},
      "critical_positive_site_counts":{k:len(class_sites[k]) for k in CLASSES},
      "same_image_sha_overlap":0,"previous_source_group_overlap":0,
      "power_measured":False,"operational_safety_target_approved":False,
      "claim_is_independently_validated":False,
      "limitation":"Steward original metadata is a declaration requiring independent review."
    }


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--candidate-private",required=True,type=Path)
    ap.add_argument("--historical-private",required=True,type=Path)
    ap.add_argument("--aggregate-out",required=True,type=Path)
    args=ap.parse_args()
    try:
        if args.aggregate_out.exists():
            raise ValueError("Cannot overwrite prior audit")
        candidate=json.loads(args.candidate_private.read_text(encoding="utf-8"))
        historical=json.loads(args.historical_private.read_text(encoding="utf-8"))
        result=evaluate(candidate,historical)
        args.aggregate_out.parent.mkdir(parents=True,exist_ok=True)
        args.aggregate_out.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
        print(json.dumps({"status":result["status"],"frames":result["images"],"model_test_run":False}))
    except (OSError,ValueError,KeyError,TypeError) as exc:
        # Never leak private image hashes, source IDs, image names or site values.
        raise SystemExit("EXTERNAL_COHORT_GATE_BLOCKED: "+type(exc).__name__)

if __name__=="__main__":
    main()
