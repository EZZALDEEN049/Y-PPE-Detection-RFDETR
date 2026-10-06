import argparse, hashlib, csv
from pathlib import Path
from collections import defaultdict
from PIL import Image
import imagehash
EXT={".jpg",".jpeg",".png",".bmp",".webp",".tif",".tiff"}
def files(r): return [p for p in Path(r).rglob("*") if p.suffix.lower() in EXT]
def sh(p):
 h=hashlib.sha256()
 with open(p,"rb") as f:
  for b in iter(lambda:f.read(1048576),b""): h.update(b)
 return h.hexdigest()
ap=argparse.ArgumentParser(); ap.add_argument("--a",required=True); ap.add_argument("--b",required=True); ap.add_argument("--out",required=True); a=ap.parse_args(); shaA=defaultdict(list); phA=defaultdict(list)
for p in files(a.a):
 s=sh(p)
 with Image.open(p) as im: ph=str(imagehash.phash(im.convert("RGB")))
 shaA[s].append(p); phA[ph].append(p)
rows=[]
for p in files(a.b):
 s=sh(p)
 with Image.open(p) as im: ph=str(imagehash.phash(im.convert("RGB")))
 if s in shaA:
  for q in shaA[s]: rows.append(["exact",str(q),str(p)])
 elif ph in phA:
  for q in phA[ph]: rows.append(["same_phash",str(q),str(p)])
with open(a.out,"w",newline="",encoding="utf-8") as f: w=csv.writer(f); w.writerow(["type","dataset_a","dataset_b"]); w.writerows(rows)
print("candidate overlaps",len(rows))
