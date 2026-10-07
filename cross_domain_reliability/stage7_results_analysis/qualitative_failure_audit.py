#!/usr/bin/env python3
"""Stage 7B: deterministic qualitative audit of safety-class cross-domain failures.

Analysis only. Uses the frozen Stage 6 operating point:
imgsz=640, conf=0.25, NMS IoU=0.70, class-matched IoU=0.50.
No training, adaptation, checkpoint selection, or threshold tuning.
"""
from __future__ import annotations
import argparse, csv, hashlib, json, gc
from pathlib import Path
from collections import defaultdict
import numpy as np
import torch, yaml
from PIL import Image, ImageDraw
from ultralytics import YOLO

CLASSES=["person","helmet","gloves","vest","boots","goggles","no_helmet","no_gloves","no_boots"]
SAFETY=["no_helmet","no_gloves","no_boots"]
SEEDS=[17,42,2026]
EXTS={".jpg",".jpeg",".png",".bmp",".tif",".tiff",".webp"}

def parse_args():
    p=argparse.ArgumentParser()
    p.add_argument("--stage5-root",required=True,type=Path)
    p.add_argument("--y-data",required=True,type=Path)
    p.add_argument("--c-data",required=True,type=Path)
    p.add_argument("--out",required=True,type=Path)
    p.add_argument("--device",default="0")
    p.add_argument("--batch",type=int,default=8)
    p.add_argument("--imgsz",type=int,default=640)
    p.add_argument("--conf",type=float,default=0.25)
    p.add_argument("--nms-iou",type=float,default=0.70)
    p.add_argument("--match-iou",type=float,default=0.50)
    p.add_argument("--examples-per-class",type=int,default=8)
    return p.parse_args()

def read_yaml(path):
    d=yaml.safe_load(path.read_text(encoding="utf-8"))
    names=d.get("names")
    if isinstance(names,dict): names=[names[k] for k in sorted(names,key=lambda x:int(x))]
    if list(names or [])!=CLASSES: raise RuntimeError(f"Class order mismatch in {path}")
    root=Path(d.get("path","."))
    if not root.is_absolute(): root=(path.parent/root).resolve()
    return d,root

def test_images(path):
    d,root=read_yaml(path)
    p=Path(d["test"])
    if not p.is_absolute(): p=(root/p).resolve()
    return sorted(x.resolve() for x in p.rglob("*") if x.is_file() and x.suffix.lower() in EXTS)

def label_path(img):
    parts=list(img.parts)
    ids=[i for i,v in enumerate(parts) if v=="images"]
    if not ids: raise RuntimeError(f"No images path segment: {img}")
    parts[ids[-1]]="labels"
    return Path(*parts).with_suffix(".txt")

def gt_objects(img,w,h):
    out=[]; lp=label_path(img)
    if not lp.exists(): return out
    for idx,line in enumerate(lp.read_text(encoding="utf-8").splitlines()):
        vals=line.split()
        if len(vals)<5: continue
        c=int(float(vals[0])); cx,cy,bw,bh=map(float,vals[1:5])
        box=np.array([(cx-bw/2)*w,(cy-bh/2)*h,(cx+bw/2)*w,(cy+bh/2)*h],float)
        out.append({"gt_index":idx,"class_id":c,"class":CLASSES[c],"box":box,"area_fraction":bw*bh})
    return out

def iou(a,b):
    x1=max(a[0],b[0]); y1=max(a[1],b[1]); x2=min(a[2],b[2]); y2=min(a[3],b[3])
    inter=max(0.0,x2-x1)*max(0.0,y2-y1)
    aa=max(0.0,a[2]-a[0])*max(0.0,a[3]-a[1]); bb=max(0.0,b[2]-b[0])*max(0.0,b[3]-b[1])
    u=aa+bb-inter
    return inter/u if u>0 else 0.0

def size_bin(area):
    return "small" if area<0.01 else ("medium" if area<0.10 else "large")

def run_model(weights,images,a):
    model=YOLO(str(weights)); out={}
    for start in range(0,len(images),a.batch):
        chunk=images[start:start+a.batch]
        rs=model.predict(source=[str(p) for p in chunk],conf=a.conf,iou=a.nms_iou,
                         imgsz=a.imgsz,device=a.device,augment=False,verbose=False)
        for r in rs:
            preds=[]
            if r.boxes is not None and len(r.boxes):
                boxes=r.boxes.xyxy.detach().cpu().numpy().astype(float)
                cls=r.boxes.cls.detach().cpu().numpy().astype(int)
                conf=r.boxes.conf.detach().cpu().numpy().astype(float)
                preds=[(int(c),b,float(s)) for c,b,s in zip(cls,boxes,conf)]
            out[str(Path(r.path).resolve())]=preds
        del rs; gc.collect()
        if torch.cuda.is_available(): torch.cuda.empty_cache()
    del model; gc.collect()
    if torch.cuda.is_available(): torch.cuda.empty_cache()
    return out

def detected(gt,preds,thr):
    return any(c==gt["class_id"] and iou(gt["box"],b)>=thr for c,b,_ in preds)

def render(img_path,gt,out_path,title):
    im=Image.open(img_path).convert("RGB"); d=ImageDraw.Draw(im)
    x1,y1,x2,y2=[int(v) for v in gt["box"]]
    d.rectangle((x1,y1,x2,y2),outline="red",width=4)
    d.rectangle((4,4,min(im.width-4,620),32),fill="black")
    d.text((8,8),title,fill="white")
    im.save(out_path,quality=92)

def main():
    a=parse_args(); a.out.mkdir(parents=True,exist_ok=True)
    directions=[("Y_to_C","Y",a.c_data.resolve()),("C_to_Y","C",a.y_data.resolve())]
    rows=[]
    for direction,src,target_yaml in directions:
        images=test_images(target_yaml)
        pred={}
        for seed in SEEDS:
            weights=(a.stage5_root/f"{src}_YOLO_s{seed}"/"train"/"weights"/"last.pt").resolve()
            if not weights.is_file(): raise FileNotFoundError(weights)
            pred[seed]=run_model(weights,images,a)
        consensus=defaultdict(list)
        for img in images:
            with Image.open(img) as im: w,h=im.size
            for gt in gt_objects(img,w,h):
                if gt["class"] not in SAFETY: continue
                outcomes={s:detected(gt,pred[s][str(img)],a.match_iou) for s in SEEDS}
                row={"direction":direction,"image":str(img),"class":gt["class"],"gt_index":gt["gt_index"],
                     "area_fraction":gt["area_fraction"],"size_bin":size_bin(gt["area_fraction"]),
                     **{f"detected_seed_{s}":outcomes[s] for s in SEEDS},
                     "consensus_fn":not any(outcomes.values())}
                rows.append(row)
                if row["consensus_fn"]: consensus[gt["class"]].append((img,gt))
        ddir=a.out/direction; ddir.mkdir(exist_ok=True)
        for cls,items in consensus.items():
            items=sorted(items,key=lambda z:hashlib.sha256(f"{z[0]}|{cls}|{z[1]['gt_index']}".encode()).hexdigest())
            for j,(img,gt) in enumerate(items[:a.examples_per_class],1):
                render(img,gt,ddir/f"{cls}_{j:02d}.jpg",f"{direction} | {cls} | consensus FN {j}")
    with (a.out/"stage7_consensus_fn_records.csv").open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    summary={}
    for direction in ["Y_to_C","C_to_Y"]:
        summary[direction]={}
        dr=[r for r in rows if r["direction"]==direction]
        for cls in SAFETY:
            rr=[r for r in dr if r["class"]==cls]; fn=[r for r in rr if r["consensus_fn"]]
            summary[direction][cls]={"gt_objects":len(rr),"consensus_fn_objects":len(fn),
                "consensus_fn_rate":len(fn)/len(rr) if rr else None,
                "consensus_fn_size_bins":{k:sum(1 for r in fn if r["size_bin"]==k) for k in ["small","medium","large"]}}
    (a.out/"stage7_consensus_fn_summary.json").write_text(json.dumps(summary,indent=2),encoding="utf-8")
    print("STAGE7_QUALITATIVE_FAILURE_AUDIT: PASS")

if __name__=="__main__": main()
