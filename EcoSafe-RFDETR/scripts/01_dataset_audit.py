import argparse, hashlib, json, csv
from pathlib import Path
from collections import Counter, defaultdict
from PIL import Image
import imagehash, yaml
IMG_EXT={".jpg",".jpeg",".png",".bmp",".webp",".tif",".tiff"}
def sha256(p):
 h=hashlib.sha256()
 with open(p,"rb") as f:
  for b in iter(lambda:f.read(1048576),b""): h.update(b)
 return h.hexdigest()
def find_images(root): return sorted(p for p in Path(root).rglob("*") if p.suffix.lower() in IMG_EXT)
def parse_names(root):
 for n in ["data.yaml","dataset.yaml"]:
  p=Path(root)/n
  if p.exists():
   y=yaml.safe_load(p.read_text(encoding="utf-8")); names=y.get("names",[])
   if isinstance(names,dict): return [names[k] for k in sorted(names,key=lambda x:int(x))]
   return list(names)
 return []
ap=argparse.ArgumentParser(); ap.add_argument("--root",required=True); ap.add_argument("--format",choices=["yolo","images"],default="yolo"); ap.add_argument("--out",required=True); a=ap.parse_args()
root=Path(a.root); out=Path(a.out); out.mkdir(parents=True,exist_ok=True); imgs=find_images(root); names=parse_names(root)
class_counts=Counter(); bad=[]; records=[]; sha_groups=defaultdict(list); ph_groups=defaultdict(list)
for p in imgs:
 rel=str(p.relative_to(root))
 try:
  with Image.open(p) as im: im.verify()
  with Image.open(p) as im: ph=str(imagehash.phash(im.convert("RGB"))); W,H=im.size
  s=sha256(p); sha_groups[s].append(rel); ph_groups[ph].append(rel); records.append([rel,W,H,s,ph])
 except Exception as e: bad.append([rel,repr(e)]); continue
 if a.format=="yolo":
  parts=list(p.parts); lab=None
  if "images" in parts:
   j=parts.index("images"); q=Path(*parts[:j],"labels",*parts[j+1:]).with_suffix(".txt")
   if q.exists(): lab=q
  if lab:
   for line in lab.read_text(encoding="utf-8",errors="ignore").splitlines():
    z=line.split()
    if z:
     try: class_counts[int(float(z[0]))]+=1
     except: pass
exact=[v for v in sha_groups.values() if len(v)>1]; sameph=[v for v in ph_groups.values() if len(v)>1]
report={"root":str(root),"images":len(imgs),"bad_images":len(bad),"class_names":names,"class_counts":{(names[k] if k<len(names) else str(k)):v for k,v in sorted(class_counts.items())},"exact_duplicate_groups":len(exact),"same_phash_groups":len(sameph)}
(out/"audit.json").write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding="utf-8")
with open(out/"image_manifest.csv","w",newline="",encoding="utf-8") as f: w=csv.writer(f); w.writerow(["relative_path","width","height","sha256","phash"]); w.writerows(records)
(out/"exact_duplicates.json").write_text(json.dumps(exact,indent=2),encoding="utf-8"); (out/"same_phash_groups.json").write_text(json.dumps(sameph,indent=2),encoding="utf-8")
print(json.dumps(report,indent=2,ensure_ascii=False))
