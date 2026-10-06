import argparse, json, csv
from pathlib import Path
from collections import defaultdict
def iou(a,b):
 x1=max(a[0],b[0]); y1=max(a[1],b[1]); x2=min(a[2],b[2]); y2=min(a[3],b[3]); inter=max(0,x2-x1)*max(0,y2-y1); aa=max(0,a[2]-a[0])*max(0,a[3]-a[1]); bb=max(0,b[2]-b[0])*max(0,b[3]-b[1]); return inter/(aa+bb-inter+1e-12)
ap=argparse.ArgumentParser(); ap.add_argument("--coco",required=True); ap.add_argument("--pred",required=True); ap.add_argument("--out",required=True); ap.add_argument("--iou",type=float,default=.5); ap.add_argument("--conf",type=float,default=.05); a=ap.parse_args(); c=json.loads(Path(a.coco).read_text()); cats={x["id"]:x["name"] for x in c["categories"]}; ordered=[x["id"] for x in sorted(c["categories"],key=lambda z:z["id"])]; gt=defaultdict(list)
for x in c["annotations"]:
 b=x["bbox"]; gt[x["image_id"]].append((x["category_id"],[b[0],b[1],b[0]+b[2],b[1]+b[3]]))
preds={}
for line in Path(a.pred).read_text().splitlines():
 x=json.loads(line); preds[x["image_id"]]=x
rows=[]
for im in c["images"]:
 iid=im["id"]; G=gt[iid]; P=[]
 for d in preds.get(iid,{}).get("detections",[]):
  if d["confidence"]<a.conf: continue
  j=d["class_id"]
  if 0<=j<len(ordered): P.append((ordered[j],d["xyxy"],d["confidence"]))
 for cid in sorted(set([x[0] for x in G]+[x[0] for x in P])):
  gg=[x[1] for x in G if x[0]==cid]; pp=sorted([x for x in P if x[0]==cid],key=lambda z:z[2],reverse=True); used=set(); tp=0
  for _,box,score in pp:
   best=(-1,None)
   for k,g in enumerate(gg):
    if k in used: continue
    v=iou(box,g)
    if v>best[0]: best=(v,k)
   if best[0]>=a.iou: tp+=1; used.add(best[1])
  rows.append([iid,im["file_name"],cats[cid],len(gg),len(pp),tp,len(pp)-tp,len(gg)-tp,preds.get(iid,{}).get("latency_ms","")])
with open(a.out,"w",newline="",encoding="utf-8") as f: w=csv.writer(f); w.writerow(["image_id","file_name","class","gt","pred","tp","fp","fn","latency_ms"]); w.writerows(rows)
print("wrote",len(rows))
