import argparse, json, shutil, xml.etree.ElementTree as ET
from pathlib import Path
ap=argparse.ArgumentParser(); ap.add_argument("--images",required=True); ap.add_argument("--annotations",required=True); ap.add_argument("--out",required=True); ap.add_argument("--list"); a=ap.parse_args()
imgdir=Path(a.images); anndir=Path(a.annotations); out=Path(a.out); out.mkdir(parents=True,exist_ok=True); allow=None
if a.list: allow=set(x.strip() for x in Path(a.list).read_text().splitlines() if x.strip())
xmls=sorted(anndir.glob("*.xml")); xmls=[x for x in xmls if allow is None or x.stem in allow]; classes=set(); parsed=[]
for x in xmls:
 r=ET.parse(x).getroot(); fn=r.findtext("filename") or x.stem+".jpg"; size=r.find("size"); W=int(size.findtext("width")); H=int(size.findtext("height")); objs=[]
 for o in r.findall("object"):
  n=o.findtext("name"); classes.add(n); b=o.find("bndbox"); xmin=float(b.findtext("xmin")); ymin=float(b.findtext("ymin")); xmax=float(b.findtext("xmax")); ymax=float(b.findtext("ymax")); objs.append((n,[xmin,ymin,xmax-xmin,ymax-ymin]))
 parsed.append((fn,W,H,objs))
classes=sorted(classes); cid={n:i+1 for i,n in enumerate(classes)}; ims=[]; anns=[]; aid=1
for iid,(fn,W,H,objs) in enumerate(parsed,1):
 src=imgdir/fn
 if not src.exists():
  m=list(imgdir.glob(Path(fn).stem+".*"))
  if not m: continue
  src=m[0]; fn=src.name
 shutil.copy2(src,out/fn); ims.append({"id":iid,"file_name":fn,"width":W,"height":H})
 for n,b in objs: anns.append({"id":aid,"image_id":iid,"category_id":cid[n],"bbox":b,"area":b[2]*b[3],"iscrowd":0}); aid+=1
cats=[{"id":cid[n],"name":n,"supercategory":"ppe"} for n in classes]; (out/"_annotations.coco.json").write_text(json.dumps({"images":ims,"annotations":anns,"categories":cats},indent=2),encoding="utf-8"); print(classes,len(ims),len(anns))
