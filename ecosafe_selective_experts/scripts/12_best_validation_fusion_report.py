#!/usr/bin/env python3
"""Development-only EcoSafe validation fusion report; requires COMPLETE chunk exports.

Uses six separately SHA-locked validation-selected best.pt checkpoint IDs, paired per seed and no held-out TEST data.
Only aggregate, nonidentifying counts are written. No router tuning or training.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
import math
from collections import Counter, defaultdict
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

from object_level_safety_oracle import matched_gt_indices, iou, SAFETY

SRC = Path(__file__).with_name("11_export_best_validation_chunks.py")
_spec = spec_from_file_location("validation_chunks_spec", SRC)
_locked = module_from_spec(_spec)
_spec.loader.exec_module(_locked)
DOMAINS = _locked.DOMAINS
CHECKPOINTS = _locked.CHECKPOINTS


def read_labels(path: Path):
    if not path.is_file():
        raise ValueError("Missing validation ground-truth label file.")
    gt = []
    for line in path.read_text(encoding="utf-8").splitlines():
        parts = line.split()
        if not parts:
            continue
        if len(parts) != 5 or not parts[0].isdigit():
            raise ValueError("Unsupported label row.")
        cid = int(parts[0])
        if cid not in range(9):
            raise ValueError("Unknown class ID.")
        try:
            cx,cy,w,h = map(float, parts[1:])
        except ValueError as exc:
            raise ValueError("Non-numeric GT box.") from exc
        if not all(math.isfinite(x) for x in (cx,cy,w,h)):
            raise ValueError("Non-finite GT box.")
        coords=(cx-w/2,cy-h/2,cx+w/2,cy+h/2)
        if not (0 <= coords[0] < coords[2] <= 1 and
                0 <= coords[1] < coords[3] <= 1):
            raise ValueError("Invalid GT box geometry.")
        if cid in SAFETY:
            gt.append({"class_id":cid,"box":coords})
    return gt


def _rows(path: Path):
    with path.open(newline="",encoding="utf-8") as handle:
        reader=csv.DictReader(handle)
        if reader.fieldnames is None:
            raise ValueError("Missing CSV header.")
        return list(reader)


def read_complete_chunks(outdir: Path, model_id: str, domain: str, image_names: list[str]):
    ds, n, manifest_sha = DOMAINS[domain]
    if len(image_names) != n or len(set(image_names)) != n:
        raise ValueError("Invalid frozen validation image list.")
    prefix=f"{model_id}__BEST_VAL_{domain.upper()}__chunk_"
    files=sorted(outdir.glob(prefix+"*_manifest.json"))
    if not files:
        raise ValueError("No validation chunk manifests available.")
    cursor=0
    detections=defaultdict(list)
    frozen_chunk_size=None
    for manifest_path in files:
        meta=json.loads(manifest_path.read_text(encoding="utf-8"))
        checks={
            "model_id": model_id, "domain": domain,
            "expected_total_validation_images": n,
            "expected_checkpoint_sha256": CHECKPOINTS[model_id][0],
            "frozen_manifest_sha256": manifest_sha,
            "split":"validation_only",
            "imgsz":640,"inference_confidence":0.001,"nms_iou":0.70,
            "runtime_ultralytics_version":"8.4.156",
            "model_retraining":False, "heldout_test_accessed":False, "checkpoint_variant":"best.pt",
            "latency_or_energy_benchmark":False,
        }
        if any(meta.get(k)!=v for k,v in checks.items()):
            raise ValueError("Frozen provenance or inference configuration mismatch.")
        idx=meta.get("chunk_index")
        chunk_size=meta.get("chunk_size")
        start=meta.get("start")
        stop=meta.get("end_exclusive")
        if (type(idx) is not int or type(chunk_size) is not int
            or type(start) is not int or type(stop) is not int
            or not 1<=chunk_size<=32 or idx < 0):
            raise ValueError("Bad chunk metadata.")
        if frozen_chunk_size is None:frozen_chunk_size=chunk_size
        if chunk_size!=frozen_chunk_size or start!=cursor or idx*chunk_size!=start:
            raise ValueError("Missing, duplicate or nonconsecutive chunk.")
        if not cursor < stop <= min(n,cursor+chunk_size):
            raise ValueError("Invalid chunk boundaries.")
        stem=manifest_path.name[:-len("_manifest.json")]
        if stem!=prefix+f"{idx:03d}":
            raise ValueError("Chunk filename/index mismatch.")
        frame_file=outdir/(stem+"_frames.csv")
        det_file=outdir/(stem+"_detections.csv")
        frames=_rows(frame_file)
        raw=_rows(det_file)
        expected=image_names[cursor:stop]
        if [r.get("image_name") for r in frames]!=expected:
            raise ValueError("Unexpected, duplicate or missing inference frames.")
        if meta.get("frames_exported")!=len(expected) or meta.get("raw_detections_exported")!=len(raw):
            raise ValueError("Manifest counters disagree with CSV.")
        counts=Counter()
        for rec in raw:
            name=rec.get("image_name")
            if name not in expected:
                raise ValueError("Prediction for an unknown image.")
            detection={"class_id":int(rec["class_id"]),
                       "confidence":float(rec["confidence"]),
                       "box":tuple(float(rec[k]) for k in ("x1n","y1n","x2n","y2n"))}
            _locked.validate_detections([{"class_id":detection["class_id"],
                "confidence":detection["confidence"],
                **{k:v for k,v in zip(("x1n","y1n","x2n","y2n"),detection["box"])}}])
            counts[name]+=1
            detections[name].append(detection)
        if any(int(row["n_detections"])!=counts[row["image_name"]] for row in frames):
            raise ValueError("Zero-detection / per-frame count integrity mismatch.")
        cursor=stop
    if cursor != n:
        raise ValueError("Incomplete validation dataset coverage: STOP.")
    return {name:detections[name] for name in image_names}


def class_nms(preds, threshold:float):
    if not 0<threshold<=1:raise ValueError("NMS threshold outside (0,1].")
    candidates=sorted(enumerate(preds),key=lambda pair:(-pair[1]["confidence"],pair[0]))
    kept=[]
    for _,p in candidates:
        if not any(p["class_id"]==k["class_id"] and
                   iou(p["box"],k["box"])>threshold for k in kept):
            kept.append(p)
    return kept


def evaluate_validation(gt_by_image, predictions_y, predictions_c,
                        conf=0.25, gt_iou=0.50, fusion_nms_iou=0.70):
    if not 0<conf<=1 or not 0<gt_iou<=1 or not 0<fusion_nms_iou<=1:
        raise ValueError("Invalid operating thresholds.")
    if not gt_by_image or set(gt_by_image)!=set(predictions_y) or set(gt_by_image)!=set(predictions_c):
        raise ValueError("Image coverage differs between GT and both experts.")
    policies=("Y","C","joint_nms","concat_oracle")
    stats={k:{"tp":0,"fn":0,"fp":0,"preds":0,"gt":0,
              "tp_by_class":Counter()} for k in policies}
    gains={"Y":0,"C":0}
    old_proxy={"Y":0,"C":0}
    frames_improved={"Y":0,"C":0}
    frames_missed_by_legacy={"Y":0,"C":0}
    class_gt=Counter()
    safety_positive_frames=0
    for name in sorted(gt_by_image):
        gt=gt_by_image[name]
        for g in gt:
            if g["class_id"] not in SAFETY:raise ValueError("Non-safety GT passed to report.")
            class_gt[g["class_id"]]+=1
        safety_positive_frames+=bool(gt)
        y=[p for p in predictions_y[name] if p["class_id"] in SAFETY and p["confidence"]>=conf]
        c=[p for p in predictions_c[name] if p["class_id"] in SAFETY and p["confidence"]>=conf]
        candidate={"Y":y,"C":c,"joint_nms":class_nms(y+c,fusion_nms_iou),
                   "concat_oracle":y+c}
        matches={}
        for policy,pred in candidate.items():
            m=matched_gt_indices(gt,[{"class_id":p["class_id"],"box":p["box"]} for p in pred],
                                 threshold=gt_iou)
            matches[policy]=len(m)
            info=stats[policy]
            info["gt"]+=len(gt)
            info["preds"]+=len(pred)
            info["tp"]+=len(m)
            info["fn"]+=len(gt)-len(m)
            info["fp"]+=len(pred)-len(m)
            for idx in m:info["tp_by_class"][gt[idx]["class_id"]]+=1
        if matches["concat_oracle"] < max(matches["Y"],matches["C"]):
            raise ValueError("Oracle cardinality is not monotone: matching bug.")
        for primary,secondary in (("Y","C"),("C","Y")):
            improvement=matches["concat_oracle"]-matches[primary]
            legacy=max(0,matches[secondary]-matches[primary])
            gains[primary]+=improvement
            old_proxy[primary]+=legacy
            frames_improved[primary]+=int(improvement>0)
            frames_missed_by_legacy[primary]+=int(improvement>0 and legacy==0)
    if not sum(class_gt.values()):
        raise ValueError("No critical-class ground truth: recall undefined.")
    report={
        "phase":"validation_only_single_seed",
        "heldout_test_accessed":False,
        "router_trained":False, "energy_measured":False,
        "inference_cost_is_not_energy":True,
        "frames":len(gt_by_image), "safety_positive_frames":safety_positive_frames,
        "critical_gt_objects":sum(class_gt.values()),
        "critical_gt_class_counts":{_locked.CLASSES[k]:class_gt[k] for k in sorted(SAFETY)},
        "thresholds":{"operating_confidence":conf,
                      "gt_matching_iou":gt_iou,"joint_class_nms_iou":fusion_nms_iou},
        "policy_result":{},
        "oracle_additional_objects_vs_primary":gains,
        "legacy_fn_difference_additional_objects_proxy":old_proxy,
        "oracle_improvement_frames":frames_improved,
        "improvement_frames_missed_by_legacy":frames_missed_by_legacy,
        "limitations":[
            "Single development domain and one seed are not an external held-out estimate.",
            "Class-aware maximum-cardinality fixed-IoU matching is not COCO AP.",
            "Concat oracle is GT-scored upper bound, not a valid operational fusion.",
            "NMS may add false alarms; safety precision and recall must both be reported.",
            "No energy/latency/power measurement or selective router evaluation was performed."
        ]
    }
    for policy,data in stats.items():
        tp,fp,fn=data["tp"],data["fp"],data["fn"]
        rec=tp/(tp+fn)
        prec=tp/(tp+fp) if tp+fp else None
        report["policy_result"][policy]={
            "tp":tp,"fn":fn,"fp":fp if policy!="concat_oracle" else None,
            "predictions":data["preds"],
            "recall":rec,
            "precision":prec if policy!="concat_oracle" else None,
            "tp_by_class":{_locked.CLASSES[k]:data["tp_by_class"][k] for k in sorted(SAFETY)}
        }
    return report


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--validation-root",required=True,type=Path)
    p.add_argument("--private-chunks",required=True,type=Path)
    p.add_argument("--domain",required=True,choices=tuple(DOMAINS))
    p.add_argument("--seed",required=True,type=int,choices=(17,42,2026))
    p.add_argument("--out",required=True,type=Path)
    args=p.parse_args()
    try:
        ds,n,manifest=DOMAINS[args.domain]
        root=args.validation_root/ds
        if _locked.sha256(root/"manifest.jsonl")!=manifest:
            raise ValueError("Frozen validation manifest fingerprint failed.")
        imgdir=root/"images"/"val"
        files=sorted((q for q in imgdir.iterdir() if q.is_file()
                      and q.suffix.lower() in (".jpg",".jpeg",".png")),key=lambda x:x.name)
        if len(files)!=n:raise ValueError("Wrong validation image count.")
        names=[q.name for q in files]
        y=read_complete_chunks(args.private_chunks,f"Y_YOLO_s{args.seed}",args.domain,names)
        c=read_complete_chunks(args.private_chunks,f"C_YOLO_s{args.seed}",args.domain,names)
        gt={q.name:read_labels(root/"labels"/"val"/(q.stem+".txt")) for q in files}
        report=evaluate_validation(gt,y,c)
        report.update({
            "frozen_validation_manifest_sha256":manifest,
            "seed":args.seed,"domain":args.domain,
            "checkpoints_sha256":{
                f"Y_YOLO_s{args.seed}":CHECKPOINTS[f"Y_YOLO_s{args.seed}"][0],
                f"C_YOLO_s{args.seed}":CHECKPOINTS[f"C_YOLO_s{args.seed}"][0],
            }
        })
    except (OSError,ValueError,KeyError,TypeError) as exc:
        # Never print private image filenames/paths/raw annotations to stdout.
        raise SystemExit("ECO_SAFE_REPORT_BLOCKED: "+type(exc).__name__)
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps({"frames":report["frames"],
                      "gt_safety_objects":report["critical_gt_objects"],
                      "joint_nms_recall":report["policy_result"]["joint_nms"]["recall"],
                      "oracle_recall":report["policy_result"]["concat_oracle"]["recall"],
                      "validation_only":True,
                      "energy_measured":False}))


if __name__=="__main__":
    main()
