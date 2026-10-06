import argparse, json, shutil
from pathlib import Path
from PIL import Image
import yaml
EXT={".jpg",".jpeg",".png",".bmp",".webp"}
def names(root):
 y=yaml.safe_load((Path(root)/"data.yaml").read_text(encoding="utf-8")); n=y.get("names",[])
 if isinstance(n,dict): n=[n[k] for k in sorted(n,key=lambda x:int(x))]
 return list(n)
def locate(root,split):
 aliases=[split]+(["val","validation"] if split=="valid" else [])
 for s in aliases:
  i=Path(root)/s/"images"; l=Path(root)/s/"labels"
  if i.exists() and l.exists(): return i,l
 raise FileNotFoundError(split)
def convert(root,out,split,nms):
 imdir,labdir=locate(root,split); dest=Path(out)/split; dest.mkdir(parents=True,exist_ok=True); ims=[]; anns=[]; aid=1
 files=sorted(p for p in imdir.iterdir() if p.suffix.lower() in EXT)
 for iid,p in enumerate(files,1):
  with Image.open(p) as im: W,H=im.size
  shutil.copy2(p,dest/p.name); ims.append({"id":iid,"file_name":p.name,"width":W,"height":H}); lab=labdir/(p.stem+".txt")
  if not lab.exists(): continue
  for line in lab.read_text(encoding="utf-8",errors="ignore").splitlines():
   z=line.split()
   if len(z)<5: continue
   c=int(float(z[0])); xc,yc,w,h=map(float,z[1:5]); bw=w*W; bh=h*H; x=max(0,(xc-w/2)*W); y=max(0,(yc-h/2)*H); bw=min(bw,W-x); bh=min(bh,H-y)
   anns.append({"id":aid,"image_id":iid,"category_id":c+1,"bbox":[x,y,bw,bh],"area":bw*bh,"iscrowd":0}); aid+=1
 cats=[{"id":i+1,"name":n,"supercategory":"ppe"} for i,n in enumerate(nms)]
 (dest/"_annotations.coco.json").write_text(json.dumps({"images":ims,"annotations":anns,"categories":cats},indent=2),encoding="utf-8"); print(split,len(ims),len(anns))
ap=argparse.ArgumentParser(); ap.add_argument("--root",required=True); ap.add_argument("--out",required=True); ap.add_argument("--splits",nargs="+",default=["train","valid"]); a=ap.parse_args(); n=names(a.root)
for s in a.splits: convert(a.root,a.out,s,n)
