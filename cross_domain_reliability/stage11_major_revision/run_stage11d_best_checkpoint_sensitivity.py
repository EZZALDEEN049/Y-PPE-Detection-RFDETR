#!/usr/bin/env python3
"""Stage 11D: best.pt checkpoint sensitivity evaluation.

Evaluation only. Uses the six already-completed Stage 5 runs and evaluates the
validation-selected best.pt checkpoint under the exact Stage 6 held-out settings.
No training, fine-tuning, adaptation, threshold tuning, or test-informed model
selection is performed.
"""
from __future__ import annotations
import argparse, gc, importlib.util, json
from pathlib import Path
import pandas as pd
import torch
from ultralytics import YOLO

RUNS=[
("Y_YOLO_s17","Y",17),("Y_YOLO_s42","Y",42),("Y_YOLO_s2026","Y",2026),
("C_YOLO_s17","C",17),("C_YOLO_s42","C",42),("C_YOLO_s2026","C",2026),
]

def args():
    p=argparse.ArgumentParser()
    p.add_argument("--repo",required=True,type=Path)
    p.add_argument("--stage5-root",required=True,type=Path)
    p.add_argument("--y-data",required=True,type=Path)
    p.add_argument("--c-data",required=True,type=Path)
    p.add_argument("--out",required=True,type=Path)
    p.add_argument("--original-group-summary",required=True,type=Path)
    p.add_argument("--device",default="0")
    p.add_argument("--batch",type=int,default=8)
    p.add_argument("--imgsz",type=int,default=640)
    p.add_argument("--ap-conf",type=float,default=0.001)
    p.add_argument("--operating-conf",type=float,default=0.25)
    p.add_argument("--nms-iou",type=float,default=0.70)
    p.add_argument("--match-iou",type=float,default=0.50)
    return p.parse_args()

def load_stage6(repo):
    p=repo/"cross_domain_reliability/stage6_heldout_evaluation/evaluate_yolo_cross_domain.py"
    spec=importlib.util.spec_from_file_location("s6",p)
    m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

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

def gaps(df):
    out=[]
    for (tr,seed),g in df.groupby(["train_domain","seed"]):
        ind=g[g.domain_type=="in_domain"].iloc[0]; cr=g[g.domain_type=="cross_domain"].iloc[0]
        out.append({"train_domain":tr,"seed":int(seed),
                    "map50_95_gap_in_minus_cross":float(ind.map50_95-cr.map50_95),
                    "f1_gap_in_minus_cross":float(ind.f1_fixed-cr.f1_fixed)})
    return pd.DataFrame(out)

def main():
    a=args(); a.repo=a.repo.resolve(); a.stage5_root=a.stage5_root.resolve()
    a.y_data=a.y_data.resolve(); a.c_data=a.c_data.resolve(); a.out=a.out.resolve()
    a.out.mkdir(parents=True,exist_ok=True)
    s6=load_stage6(a.repo)

    # Verify primary run manifests and both checkpoint files.
    s6.validate_stage5_inputs(a.stage5_root)
    ckpt_meta=[]
    for run_id,tr,seed in RUNS:
        p=(a.stage5_root/run_id/"train"/"weights"/"best.pt").resolve()
        if not p.is_file(): raise FileNotFoundError(p)
        ckpt_meta.append({"run_id":run_id,"train_domain":tr,"seed":seed,
                          "checkpoint":str(p),"size_bytes":p.stat().st_size})

    runtime=a.out/"_runtime_yaml"; runtime.mkdir(exist_ok=True)
    y_runtime=s6.write_runtime_yaml(a.y_data,runtime/"Y.yaml")
    c_runtime=s6.write_runtime_yaml(a.c_data,runtime/"C.yaml")
    y_imgs=s6.image_files(s6.resolve_split(y_runtime)); c_imgs=s6.image_files(s6.resolve_split(c_runtime))
    if len(y_imgs)!=186 or len(c_imgs)!=138:
        raise RuntimeError(f"Frozen test counts changed: Y={len(y_imgs)} C={len(c_imgs)}")

    preflight={"status":"STAGE11D_PREFLIGHT_PASS","training_performed":False,
               "checkpoint_policy":"validation_selected_best.pt",
               "checkpoints":ckpt_meta,
               "y_test_images":len(y_imgs),"c_test_images":len(c_imgs),
               "settings":{"imgsz":a.imgsz,"ap_conf":a.ap_conf,"operating_conf":a.operating_conf,
                           "nms_iou":a.nms_iou,"match_iou":a.match_iou,"augmentation":False}}
    (a.out/"stage11d_preflight.json").write_text(json.dumps(preflight,indent=2),encoding="utf-8")
    print("STAGE11D_PREFLIGHT_PASS",flush=True)

    tests={"Y":(y_runtime,y_imgs,"Y-PPE-h9-v2"),"C":(c_runtime,c_imgs,"Construction-PPE-h9-v2")}
    rows=[]
    for run_id,tr,seed in RUNS:
        weights=(a.stage5_root/run_id/"train"/"weights"/"best.pt").resolve()
        model=YOLO(str(weights))
        for te in ("Y","C"):
            data_yaml,imgs,test_name=tests[te]
            eval_id=f"{run_id}__BEST__TEST_{te}"
            dt="in_domain" if tr==te else "cross_domain"
            print(f"[Stage11D] START {eval_id}",flush=True)
            metrics=model.val(data=str(data_yaml),split="test",imgsz=a.imgsz,batch=a.batch,
                              device=a.device,conf=a.ap_conf,iou=a.nms_iou,augment=False,
                              plots=False,save_json=False,verbose=False,
                              project=str(a.out/"ultralytics"),name=eval_id,exist_ok=True)
            ap=s6.metrics_to_dict(metrics)
            del metrics; gc.collect()
            if torch.cuda.is_available(): torch.cuda.empty_cache()
            fixed=s6.fixed_operating_point(model,imgs,a.device,a.imgsz,a.operating_conf,
                                           a.nms_iou,a.match_iou,a.batch)
            rows.append({"eval_id":eval_id,"run_id":run_id,"train_domain":tr,
                         "test_domain":te,"domain_type":dt,"seed":seed,
                         "checkpoint":"best.pt","n_test_images":len(imgs),
                         "map50_95":ap["map50_95"],"map50":ap["map50"],"map75":ap["map75"],
                         "precision_fixed":fixed["micro"]["precision"],
                         "recall_fixed":fixed["micro"]["recall"],
                         "f1_fixed":fixed["micro"]["f1"],
                         "no_helmet_recall":fixed["per_class"]["no_helmet"]["recall"],
                         "no_gloves_recall":fixed["per_class"]["no_gloves"]["recall"],
                         "no_boots_recall":fixed["per_class"]["no_boots"]["recall"]})
            print(f"[Stage11D] COMPLETE {eval_id}",flush=True)
        del model; gc.collect()
        if torch.cuda.is_available(): torch.cuda.empty_cache()

    raw=pd.DataFrame(rows); raw.to_csv(a.out/"stage11d_best_12cell_summary.csv",index=False)
    grp=aggregate(rows); grp.to_csv(a.out/"stage11d_best_group_summary.csv",index=False)
    gp=gaps(raw); gp.to_csv(a.out/"stage11d_best_seed_gaps.csv",index=False)

    orig=pd.read_csv(a.original_group_summary)
    keys=["train_domain","test_domain","domain_type"]
    m=orig.merge(grp,on=keys,suffixes=("_last","_best"))
    metrics=["map50_95_mean","recall_fixed_mean","f1_fixed_mean",
             "no_helmet_recall_mean","no_gloves_recall_mean","no_boots_recall_mean"]
    out=[]
    for _,r in m.iterrows():
        row={k:r[k] for k in keys}
        for x in metrics:
            row[x+"_last"]=r[x+"_last"]; row[x+"_best"]=r[x+"_best"]
            row[x+"_delta_best_minus_last"]=r[x+"_best"]-r[x+"_last"]
        out.append(row)
    pd.DataFrame(out).to_csv(a.out/"stage11d_best_vs_last_comparison.csv",index=False)

    status={"status":"STAGE11D_BEST_CHECKPOINT_SENSITIVITY_COMPLETE",
            "training_performed":False,"test_informed_tuning":False,
            "checkpoint_policy":"best.pt","n_eval_cells":len(rows)}
    (a.out/"stage11d_status.json").write_text(json.dumps(status,indent=2),encoding="utf-8")
    print("STAGE11D_BEST_CHECKPOINT_SENSITIVITY: PASS")

if __name__=="__main__": main()
