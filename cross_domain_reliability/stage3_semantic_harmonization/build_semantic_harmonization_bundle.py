#!/usr/bin/env python3
from __future__ import annotations
import argparse, csv, hashlib, json, math
from collections import Counter, defaultdict
from pathlib import Path
from statistics import median
from typing import List

import yaml
from PIL import Image, ImageDraw

IMAGE_EXTS={'.jpg','.jpeg','.png','.bmp','.webp','.tif','.tiff'}

def load_yaml(path: Path):
    return yaml.safe_load(path.read_text(encoding='utf-8'))

def class_names_from_yaml(path: Path) -> List[str]:
    data=load_yaml(path); names=data.get('names')
    if isinstance(names,list): return [str(x) for x in names]
    if isinstance(names,dict): return [str(names[i] if i in names else names[str(i)]) for i in range(len(names))]
    raise ValueError(f'No class names in {path}')

def find_dirs(root: Path, split: str):
    for img,lbl in [(root/split/'images',root/split/'labels'),(root/'images'/split,root/'labels'/split),(root/split,root/'labels'/split)]:
        if img.is_dir() and lbl.is_dir(): return img,lbl
    raise FileNotFoundError(f'Cannot locate image/label dirs root={root} split={split}')

def find_image(img_dir: Path, stem: str):
    for ext in IMAGE_EXTS:
        p=img_dir/(stem+ext)
        if p.exists(): return p
    m=[p for p in img_dir.glob(stem+'.*') if p.suffix.lower() in IMAGE_EXTS]
    return m[0] if m else None

def parse_label(path: Path):
    rows=[]
    if not path.exists(): return rows
    for line_no,line in enumerate(path.read_text(encoding='utf-8',errors='replace').splitlines(),1):
        parts=line.split()
        if not parts: continue
        try: cls=int(float(parts[0]))
        except Exception: continue
        fmt='unknown'; bbox=None
        if len(parts)==5:
            try:
                x,y,w,h=map(float,parts[1:]); bbox=(x,y,w,h); fmt='bbox'
            except Exception: pass
        elif len(parts)>=7 and len(parts)%2==1:
            try:
                coords=list(map(float,parts[1:])); xs=coords[0::2]; ys=coords[1::2]
                x1,x2=min(xs),max(xs); y1,y2=min(ys),max(ys)
                bbox=((x1+x2)/2,(y1+y2)/2,x2-x1,y2-y1); fmt='polygon'
            except Exception: pass
        if bbox is not None: rows.append({'cls':cls,'bbox':bbox,'format':fmt,'line_no':line_no,'raw':line.strip()})
    return rows

def box_xyxy(b):
    x,y,w,h=b; return (x-w/2,y-h/2,x+w/2,y+h/2)

def intersect_area(a,b):
    ax1,ay1,ax2,ay2=box_xyxy(a); bx1,by1,bx2,by2=box_xyxy(b)
    return max(0,min(ax2,bx2)-max(ax1,bx1))*max(0,min(ay2,by2)-max(ay1,by1))

def center_inside(inner,outer):
    x,y,_,_=inner; x1,y1,x2,y2=box_xyxy(outer); return x1<=x<=x2 and y1<=y<=y2

def quantile(vals,q):
    if not vals: return None
    vals=sorted(vals); pos=(len(vals)-1)*q; lo=int(math.floor(pos)); hi=int(math.ceil(pos))
    if lo==hi: return vals[lo]
    return vals[lo]*(hi-pos)+vals[hi]*(pos-lo)

def stable_key(seed,text): return hashlib.sha256((seed+'|'+text).encode()).hexdigest()

def pick_samples(items,split_order,n,seed):
    by=defaultdict(list)
    for item in items: by[item['split']].append(item)
    chosen=[]
    if len(split_order)>=2:
        val_n=max(1,round(n/3)); quotas={split_order[0]:n-val_n,split_order[1]:val_n}
    else: quotas={split_order[0]:n}
    for sp in split_order:
        arr=sorted(by.get(sp,[]),key=lambda x:stable_key(seed,x['image_rel'])); chosen.extend(arr[:quotas.get(sp,0)])
    if len(chosen)<n:
        used={x['image_rel'] for x in chosen}; rest=sorted([x for x in items if x['image_rel'] not in used],key=lambda x:stable_key(seed,'rest|'+x['image_rel']))
        chosen.extend(rest[:n-len(chosen)])
    return chosen[:n]

def draw_box(draw,bbox,W,H,color,width=3):
    x1,y1,x2,y2=box_xyxy(bbox); draw.rectangle([x1*W,y1*H,x2*W,y2*H],outline=color,width=width)

def crop_around(im,bbox,margin=1.8):
    W,H=im.size; x,y,w,h=bbox; cw=min(1.0,max(w*margin,0.20)); ch=min(1.0,max(h*margin,0.20))
    x1=max(0,x-cw/2); y1=max(0,y-ch/2); x2=min(1,x+cw/2); y2=min(1,y+ch/2)
    return im.crop((int(x1*W),int(y1*H),int(x2*W),int(y2*H)))

def panel_for_sample(item,target_cls,person_cls,target_name,panel_w=360,panel_h=250):
    im=Image.open(item['image_path']).convert('RGB'); W,H=im.size; full=im.copy(); d=ImageDraw.Draw(full)
    persons=[r for r in item['rows'] if r['cls']==person_cls]; targets=[r for r in item['rows'] if r['cls']==target_cls]
    for r in persons: draw_box(d,r['bbox'],W,H,(0,100,255),max(2,W//300))
    for r in targets: draw_box(d,r['bbox'],W,H,(255,0,0),max(3,W//250))
    zoom=crop_around(im,targets[0]['bbox']) if targets else im.copy(); full.thumbnail((215,180)); zoom.thumbnail((130,180))
    panel=Image.new('RGB',(panel_w,panel_h),'white'); panel.paste(full,(5,42)); panel.paste(zoom,(225,42)); pd=ImageDraw.Draw(panel)
    pd.rectangle([224,41,359,223],outline=(255,0,0),width=2)
    fmt=','.join(sorted(set(r['format'] for r in targets)))
    pd.text((5,5),f"{item['dataset']} | {target_name} | {item['split']}",fill='black'); pd.text((5,20),Path(item['image_path']).name[:44],fill='black')
    pd.text((5,225),f"target={len(targets)} person={len(persons)} fmt={fmt}",fill='black')
    return panel

def build_dataset_index(dataset,root,yaml_path,splits,mapping_native_names,person_native):
    names=class_names_from_yaml(yaml_path); name_to_id={n:i for i,n in enumerate(names)}
    missing=[n for n in mapping_native_names+[person_native] if n not in name_to_id]
    if missing: raise ValueError(f'{dataset}: missing classes {missing}; found={names}')
    target_ids={n:name_to_id[n] for n in mapping_native_names}; person_id=name_to_id[person_native]; items=[]
    for split in splits:
        img_dir,lbl_dir=find_dirs(root,split)
        for lp in sorted(lbl_dir.glob('*.txt')):
            ip=find_image(img_dir,lp.stem)
            if ip is None: continue
            rows=parse_label(lp); present={r['cls'] for r in rows}
            if any(cid in present for cid in target_ids.values()): items.append({'dataset':dataset,'split':split,'image_path':str(ip),'image_rel':f'{split}/{ip.name}','label_path':str(lp),'rows':rows})
    return target_ids,person_id,items

def summarize_class(items,cls_id,person_id):
    areas=[]; aspects=[]; fmts=Counter(); pair_ratios=[]; center_rates=[]; containment=[]; image_count=0; instance_count=0
    for item in items:
        targets=[r for r in item['rows'] if r['cls']==cls_id]
        if not targets: continue
        image_count+=1; persons=[r for r in item['rows'] if r['cls']==person_id]
        for t in targets:
            instance_count+=1; fmts[t['format']]+=1; x,y,w,h=t['bbox']; area=w*h; areas.append(area); aspects.append(w/h if h>0 else None)
            if cls_id!=person_id and persons:
                scored=[]
                for p in persons:
                    ratio=intersect_area(t['bbox'],p['bbox'])/area if area>0 else 0; scored.append(((1 if center_inside(t['bbox'],p['bbox']) else 0,ratio),p))
                score,p=max(scored,key=lambda z:z[0]); center_rates.append(score[0]); containment.append(score[1]); parea=p['bbox'][2]*p['bbox'][3]
                if parea>0: pair_ratios.append(area/parea)
    def stats(v):
        v=[x for x in v if x is not None]; return {'q25':quantile(v,.25),'median':quantile(v,.5),'q75':quantile(v,.75)} if v else {'q25':None,'median':None,'q75':None}
    return {'images_with_class':image_count,'instances':instance_count,'annotation_formats':dict(fmts),'box_area':stats(areas),'aspect_ratio':stats(aspects),'person_relation':{'paired_instances':len(center_rates),'target_center_inside_person_rate':sum(center_rates)/len(center_rates) if center_rates else None,'median_target_area_over_person_area':median(pair_ratios) if pair_ratios else None,'median_target_area_contained_by_person':median(containment) if containment else None}}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--y-root',required=True); ap.add_argument('--y-yaml',required=True); ap.add_argument('--c-root',required=True); ap.add_argument('--c-yaml',required=True); ap.add_argument('--ontology',required=True); ap.add_argument('--out',required=True); ap.add_argument('--samples-per-dataset-class',type=int,default=6); ap.add_argument('--seed',default='stage3-v1'); args=ap.parse_args()
    out=Path(args.out); out.mkdir(parents=True,exist_ok=True); (out/'contact_sheets').mkdir(exist_ok=True)
    ont=load_yaml(Path(args.ontology)); classes=ont['shared_classes']; y_names=[x['y_name'] for x in classes]; c_names=[x['c_name'] for x in classes]
    y_splits=ont['datasets']['Y-PPE']['visual_audit_splits']; c_splits=ont['datasets']['Construction-PPE']['visual_audit_splits']
    ytarget,yperson,yitems=build_dataset_index('Y-PPE',Path(args.y_root),Path(args.y_yaml),y_splits,y_names,ont['datasets']['Y-PPE']['person_class'])
    ctarget,cperson,citems=build_dataset_index('Construction-PPE',Path(args.c_root),Path(args.c_yaml),c_splits,c_names,ont['datasets']['Construction-PPE']['person_class'])
    geometry={'policy':{'visual_test_split_used':False,'polygon_handling':'Y-PPE polygon rows summarized and visualized using enclosing axis-aligned box only; source annotation remains unchanged.'},'classes':{}}; manifest=[]
    for idx,e in enumerate(classes,1):
        canon=e['canonical']; yname=e['y_name']; cname=e['c_name']; geometry['classes'][canon]={'Y-PPE':summarize_class(yitems,ytarget[yname],yperson),'Construction-PPE':summarize_class(citems,ctarget[cname],cperson)}
        ys=[x for x in yitems if any(r['cls']==ytarget[yname] for r in x['rows'])]; cs=[x for x in citems if any(r['cls']==ctarget[cname] for r in x['rows'])]
        ychosen=pick_samples(ys,y_splits,args.samples_per_dataset_class,args.seed+'|Y|'+canon); cchosen=pick_samples(cs,c_splits,args.samples_per_dataset_class,args.seed+'|C|'+canon); panels=[]
        for ds,chosen,clsid,pid,native in [('Y-PPE',ychosen,ytarget[yname],yperson,yname),('Construction-PPE',cchosen,ctarget[cname],cperson,cname)]:
            for item in chosen:
                panels.append(panel_for_sample(item,clsid,pid,native)); manifest.append({'canonical':canon,'dataset':ds,'native_class':native,'split':item['split'],'image':Path(item['image_path']).name,'label':Path(item['label_path']).name})
        cols=3; rows=math.ceil(len(panels)/cols); pw,ph=360,250; sheet=Image.new('RGB',(cols*pw,rows*ph+35),'white'); sd=ImageDraw.Draw(sheet); sd.text((8,8),f"Stage 3 semantic audit | {canon} | blue=person, red=target | TEST SPLIT NOT USED",fill='black')
        for j,p in enumerate(panels): sheet.paste(p,((j%cols)*pw,35+(j//cols)*ph))
        sheet.save(out/'contact_sheets'/f'{idx:02d}_{canon}.jpg',quality=90)
    (out/'geometry_summary.json').write_text(json.dumps(geometry,indent=2,ensure_ascii=False),encoding='utf-8')
    fields=['canonical','dataset','instances','images_with_class','bbox_rows','polygon_rows','area_q25','area_median','area_q75','aspect_median','paired_instances','center_inside_person_rate','median_target_area_over_person_area','median_target_contained_rate']
    with (out/'geometry_summary.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=fields); w.writeheader()
        for canon,d in geometry['classes'].items():
            for ds,s in d.items():
                w.writerow({'canonical':canon,'dataset':ds,'instances':s['instances'],'images_with_class':s['images_with_class'],'bbox_rows':s['annotation_formats'].get('bbox',0),'polygon_rows':s['annotation_formats'].get('polygon',0),'area_q25':s['box_area']['q25'],'area_median':s['box_area']['median'],'area_q75':s['box_area']['q75'],'aspect_median':s['aspect_ratio']['median'],'paired_instances':s['person_relation']['paired_instances'],'center_inside_person_rate':s['person_relation']['target_center_inside_person_rate'],'median_target_area_over_person_area':s['person_relation']['median_target_area_over_person_area'],'median_target_contained_rate':s['person_relation']['median_target_area_contained_by_person']})
    with (out/'sample_manifest.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=['canonical','dataset','native_class','split','image','label']); w.writeheader(); w.writerows(manifest)
    review=[{'canonical':e['canonical'],'y_class':e['y_name'],'construction_class':e['c_name'],'object_definition_match':'','box_extent_match':'','annotation_context_match':'','final_status':'PENDING_VISUAL_AUDIT','notes':''} for e in classes]
    with (out/'semantic_review_template.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=review[0].keys()); w.writeheader(); w.writerows(review)
    meta={'shared_class_count':len(classes),'samples_per_dataset_class':args.samples_per_dataset_class,'total_sample_panels':len(manifest),'test_split_visuals_included':False,'seed':args.seed,'contact_sheets':len(classes)}; (out/'bundle_summary.json').write_text(json.dumps(meta,indent=2),encoding='utf-8'); print(json.dumps(meta,indent=2))
if __name__=='__main__': main()
