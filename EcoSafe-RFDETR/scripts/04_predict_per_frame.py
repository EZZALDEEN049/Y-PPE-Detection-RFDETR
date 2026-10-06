import argparse, json, time
from pathlib import Path
import numpy as np
ap=argparse.ArgumentParser(); ap.add_argument("--variant",choices=["nano","small","medium","large"],required=True); ap.add_argument("--checkpoint",required=True); ap.add_argument("--coco",required=True); ap.add_argument("--images",required=True); ap.add_argument("--out",required=True); ap.add_argument("--threshold",type=float,default=.01); a=ap.parse_args()
from rfdetr import RFDETRNano, RFDETRSmall, RFDETRMedium, RFDETRLarge
cls={"nano":RFDETRNano,"small":RFDETRSmall,"medium":RFDETRMedium,"large":RFDETRLarge}[a.variant]; m=cls(pretrain_weights=a.checkpoint); coco=json.loads(Path(a.coco).read_text()); rows=[]
for im in coco["images"]:
 p=Path(a.images)/im["file_name"]; t=time.perf_counter(); d=m.predict(str(p),threshold=a.threshold); dt=(time.perf_counter()-t)*1000; dets=[]
 for b,s,c in zip(np.asarray(d.xyxy).tolist(),np.asarray(d.confidence).tolist(),np.asarray(d.class_id).tolist()): dets.append({"xyxy":b,"confidence":float(s),"class_id":int(c)})
 rows.append({"image_id":im["id"],"file_name":im["file_name"],"latency_ms":dt,"detections":dets})
Path(a.out).write_text("\n".join(json.dumps(x) for x in rows)+"\n",encoding="utf-8"); print("wrote",len(rows))
