#!/usr/bin/env python3
"""Stage 11A sensitivity evaluation after dependence audit.

Evaluation only. No training, fine-tuning, checkpoint reselection, or threshold
tuning is performed. Two prespecified sensitivity subsets are evaluated:
(1) strict near-duplicate exclusion and
(2) conservative direct train-scene exclusion.
"""
from __future__ import annotations

import argparse
import csv
import gc
import hashlib
import importlib.util
import json
import shutil
from pathlib import Path

import numpy as np
import pandas as pd
import torch
import yaml
from ultralytics import YOLO

RUNS = [
    ("Y_YOLO_s17", "Y", 17),
    ("Y_YOLO_s42", "Y", 42),
    ("Y_YOLO_s2026", "Y", 2026),
    ("C_YOLO_s17", "C", 17),
    ("C_YOLO_s42", "C", 42),
    ("C_YOLO_s2026", "C", 2026),
]

SCENARIOS = {
    "strict_near_duplicate_exclusion": "strict_near_duplicate_test_exclusions.json",
    "conservative_train_scene_exclusion": "conservative_train_scene_test_exclusions.json",
}

def parse_args():
    p=argparse.ArgumentParser()
    p.add_argument("--repo",required=True,type=Path)
    p.add_argument("--stage5-root",required=True,type=Path)
    p.add_argument("--y-data",required=True,type=Path)
    p.add_argument("--c-data",required=True,type=Path)
    p.add_argument("--out",required=True,type=Path)
    p.add_argument("--original-group-summary",type=Path,default=None)
    p.add_argument("--device",default="0")
    p.add_argument("--batch",type=int,default=8)
    p.add_argument("--imgsz",type=int,default=640)
    p.add_argument("--ap-conf",type=float,default=0.001)
    p.add_argument("--operating-conf",type=float,default=0.25)
    p.add_argument("--nms-iou",type=float,default=0.70)
    p.add_argument("--match-iou",type=float,default=0.50)
    return p.parse_args()

def sha256(path):
    h=hashlib.sha256()
    with path.open("rb") as f:
        for ch in iter(lambda:f.read(1024*1024),b""):
            h.update(ch)
    return h.hexdigest()

def load_stage6(repo:Path):
    p=repo/"cross_domain_reliability/stage6_heldout_evaluation/evaluate_yolo_cross_domain.py"
    spec=importlib.util.spec_from_file_location("stage6_eval",p)
    m=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m

def source_root(data_yaml:Path):
    d=yaml.safe_load(data_yaml.read_text(encoding="utf-8"))
    root=Path(d.get("path","."))
    if not root.is_absolute():
        root=(data_yaml.parent/root).resolve()
    return d,root

def resolve_entry(data_yaml:Path,key:str):
    d,root=source_root(data_yaml)
    p=Path(d[key])
    return p if p.is_absolute() else (root/p).resolve()

def label_for(img:Path):
    parts=list(img.parts)
    ids=[i for i,v in enumerate(parts) if v=="images"]
    if not ids:
        raise RuntimeError(f"No images segment: {img}")
    parts[ids[-1]]="labels"
    return Path(*parts).with_suffix(".txt")

def build_filtered_yaml(data_yaml:Path,dataset_name:str,excluded:set[str],dest:Path,classes:list[str]):
    d,_=source_root(data_yaml)
    src_test=resolve_entry(data_yaml,"test")
    out_root=dest/dataset_name
    img_dir=out_root/"images"/"test"
    lab_dir=out_root/"labels"/"test"
    img_dir.mkdir(parents=True,exist_ok=True)
    lab_dir.mkdir(parents=True,exist_ok=True)
    exts={".jpg",".jpeg",".png",".bmp",".tif",".tiff",".webp"}
    imgs=sorted(p for p in src_test.rglob("*") if p.is_file() and p.suffix.lower() in exts)
    kept=[]
    for img in imgs:
        if img.name in excluded:
            continue
        dst=img_dir/img.name
        if not dst.exists():
            dst.symlink_to(img)
        lp=label_for(img)
        if lp.exists():
            ldst=lab_dir/lp.name
            if not ldst.exists():
                ldst.symlink_to(lp)
        kept.append(dst.resolve())
    runtime={
        "path":str(out_root.resolve()),
        "train":str(resolve_entry(data_yaml,"train")),
        "val":str(resolve_entry(data_yaml,"val")),
        "test":str(img_dir.resolve()),
        "names":classes,
        "nc":len(classes),
    }
    yp=out_root/"data.yaml"
    yp.write_text(yaml.safe_dump(runtime,sort_keys=False),encoding="utf-8")
    return yp, kept

def aggregate(rows):
    df=pd.DataFrame(rows)
    metrics=["map50_95","map50","map75","precision_fixed","recall_fixed","f1_fixed",
             "no_helmet_recall","no_gloves_recall","no_boots_recall"]
    out=[]
    for (tr,te,dt),g in df.groupby(["train_domain","test_domain","domain_type"]):
        r={"train_domain":tr,"test_domain":te,"domain_type":dt,"n_seeds":len(g)}
        for m in metrics:
            r[m+"_mean"]=float(g[m].mean())
            r[m+"_sd"]=float(g[m].std(ddof=1))
        out.append(r)
    return pd.DataFrame(out)

def domain_gaps(rows):
    df=pd.DataFrame(rows)
    out=[]
    for (tr,seed),g in df.groupby(["train_domain","seed"]):
        ind=g[g.domain_type=="in_domain"].iloc[0]
        cr=g[g.domain_type=="cross_domain"].iloc[0]
        out.append({
            "train_domain":tr,"seed":int(seed),
            "map50_95_gap_in_minus_cross":float(ind.map50_95-cr.map50_95),
            "f1_gap_in_minus_cross":float(ind.f1_fixed-cr.f1_fixed),
        })
    return pd.DataFrame(out)

def run_scenario(a,s6,scenario,exclusion_path):
    scenario_out=a.out/scenario
    scenario_out.mkdir(parents=True,exist_ok=True)
    exclusions=json.loads(exclusion_path.read_text(encoding="utf-8"))
    data_dir=scenario_out/"_filtered_data"
    if data_dir.exists():
        shutil.rmtree(data_dir)
    y_yaml,y_imgs=build_filtered_yaml(a.y_data.resolve(),"Y-PPE-h9-v2",
                                      set(exclusions["Y-PPE-h9-v2"]),data_dir,s6.CLASSES)
    c_yaml,c_imgs=build_filtered_yaml(a.c_data.resolve(),"Construction-PPE-h9-v2",
                                      set(exclusions["Construction-PPE-h9-v2"]),data_dir,s6.CLASSES)
    tests={"Y":(y_yaml,y_imgs,"Y-PPE-h9-v2"),"C":(c_yaml,c_imgs,"Construction-PPE-h9-v2")}
    preflight={
        "status":"STAGE11A_SENSITIVITY_PREFLIGHT_PASS",
        "scenario":scenario,
        "exclusion_file":str(exclusion_path),
        "exclusion_sha256":sha256(exclusion_path),
        "y_test_images":len(y_imgs),"c_test_images":len(c_imgs),
        "settings":{"imgsz":a.imgsz,"ap_conf":a.ap_conf,"operating_conf":a.operating_conf,
                    "nms_iou":a.nms_iou,"match_iou":a.match_iou,"augmentation":False},
        "training_performed":False,
        "checkpoint_policy":"final_epoch_last.pt",
    }
    (scenario_out/"preflight.json").write_text(json.dumps(preflight,indent=2),encoding="utf-8")
    print(f"{scenario}: preflight Y={len(y_imgs)} C={len(c_imgs)}",flush=True)
    rows=[]
    for run_id,train_domain,seed in RUNS:
        weights=(a.stage5_root/run_id/"train"/"weights"/"last.pt").resolve()
        if not weights.is_file():
            raise FileNotFoundError(weights)
        model=YOLO(str(weights))
        for test_domain in ("Y","C"):
            data_yaml,imgs,test_name=tests[test_domain]
            eval_id=f"{run_id}__TEST_{test_domain}"
            dt="in_domain" if train_domain==test_domain else "cross_domain"
            print(f"[{scenario}] START {eval_id}",flush=True)
            metrics=model.val(
                data=str(data_yaml),split="test",imgsz=a.imgsz,batch=a.batch,
                device=a.device,conf=a.ap_conf,iou=a.nms_iou,augment=False,
                plots=False,save_json=False,verbose=False,
                project=str(scenario_out/"ultralytics"),name=eval_id,exist_ok=True,
            )
            ap=s6.metrics_to_dict(metrics)
            del metrics; gc.collect()
            if torch.cuda.is_available(): torch.cuda.empty_cache()
            fixed=s6.fixed_operating_point(
                model,imgs,a.device,a.imgsz,a.operating_conf,a.nms_iou,a.match_iou,a.batch
            )
            rows.append({
                "scenario":scenario,"eval_id":eval_id,"run_id":run_id,
                "train_domain":train_domain,"test_domain":test_domain,"domain_type":dt,"seed":seed,
                "n_test_images":len(imgs),
                "map50_95":ap["map50_95"],"map50":ap["map50"],"map75":ap["map75"],
                "precision_fixed":fixed["micro"]["precision"],
                "recall_fixed":fixed["micro"]["recall"],"f1_fixed":fixed["micro"]["f1"],
                "no_helmet_recall":fixed["per_class"]["no_helmet"]["recall"],
                "no_gloves_recall":fixed["per_class"]["no_gloves"]["recall"],
                "no_boots_recall":fixed["per_class"]["no_boots"]["recall"],
            })
            print(f"[{scenario}] COMPLETE {eval_id}",flush=True)
        del model; gc.collect()
        if torch.cuda.is_available(): torch.cuda.empty_cache()
    raw=pd.DataFrame(rows)
    raw.to_csv(scenario_out/"stage11_12cell_summary.csv",index=False)
    group=aggregate(rows); group.to_csv(scenario_out/"stage11_group_summary.csv",index=False)
    gaps=domain_gaps(rows); gaps.to_csv(scenario_out/"stage11_seed_domain_gaps.csv",index=False)
    return group

def comparison_table(original,scenario_groups):
    keys=["train_domain","test_domain","domain_type"]
    metrics=["map50_95_mean","recall_fixed_mean","f1_fixed_mean",
             "no_helmet_recall_mean","no_gloves_recall_mean","no_boots_recall_mean"]
    rows=[]
    for scenario,g in scenario_groups.items():
        m=original.merge(g,on=keys,suffixes=("_orig","_sens"))
        for _,r in m.iterrows():
            row={"scenario":scenario,**{k:r[k] for k in keys}}
            for met in metrics:
                if met+"_orig" in r:
                    row[met+"_original"]=r[met+"_orig"]
                    row[met+"_sensitivity"]=r[met+"_sens"]
                    row[met+"_delta"]=r[met+"_sens"]-r[met+"_orig"]
            rows.append(row)
    return pd.DataFrame(rows)

def main():
    a=parse_args()
    a.repo=a.repo.resolve(); a.stage5_root=a.stage5_root.resolve()
    a.y_data=a.y_data.resolve(); a.c_data=a.c_data.resolve(); a.out=a.out.resolve()
    a.out.mkdir(parents=True,exist_ok=True)
    s6=load_stage6(a.repo)
    # Verify the six completed frozen runs before sensitivity evaluation.
    s6.validate_stage5_inputs(a.stage5_root)
    scenario_groups={}
    exdir=a.repo/"cross_domain_reliability/stage11_major_revision"
    for scenario,fn in SCENARIOS.items():
        scenario_groups[scenario]=run_scenario(a,s6,scenario,exdir/fn)
    if a.original_group_summary and a.original_group_summary.is_file():
        orig=pd.read_csv(a.original_group_summary)
        comp=comparison_table(orig,scenario_groups)
        comp.to_csv(a.out/"stage11_sensitivity_comparison.csv",index=False)
        print(comp.to_string(index=False))
    status={
        "status":"STAGE11A_SENSITIVITY_EVALUATION_COMPLETE",
        "training_performed":False,
        "test_informed_tuning":False,
        "scenarios":list(SCENARIOS),
    }
    (a.out/"stage11_status.json").write_text(json.dumps(status,indent=2),encoding="utf-8")
    print("STAGE11A_SENSITIVITY_EVALUATION: PASS")

if __name__=="__main__":
    main()
