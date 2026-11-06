#!/usr/bin/env python3
"""Read-only SEER-PPE clean-17 archive audit; no image upload or modification.

The CLEAN directory is the output of the historically archived deterministic
copy-then-correct script, NOT the augmented ALTAYYAR V2 training export.
This program does not assert site-level independence, copyright clearance,
or independent human annotations.
"""
import argparse, csv, hashlib, json, re
from collections import Counter, defaultdict
from pathlib import Path
from PIL import Image, ImageOps

EXTENSIONS={'.jpg','.jpeg','.png','.webp','.bmp','.tif','.tiff'}
EXPECTED={'train':1595,'valid':459,'test':234}
KNOWN_VIDEO=(re.compile(r'^(sapi-7_mp4|rpreplay_final1667001201_mp4|43_mov)[-_]',re.I),)

def normalized_name(name):
    """Name-only candidate matching, never pixel/identity proof."""
    s=Path(name).name.lower()
    s=re.sub(r'_([a-z0-9]+)\.rf\.[a-f0-9]{32}\.[a-z0-9]+$',r'.\1',s)
    return re.sub(r'[^a-z0-9]+','',s).replace('jpeg','jpg')

def d_hash(im):
    gray=ImageOps.exif_transpose(im).convert('L').resize((9,8))
    p=list(gray.getdata()); num=0
    for y in range(8):
        for x in range(8):num=(num<<1) | (p[y*9+x]>p[y*9+x+1])
    return num

def known_family(name):
    for regex in KNOWN_VIDEO:
        m=regex.match(name)
        if m:return m.group(1).lower()
    return ''

def locate(root,split):
    for a,b in [(root/split/'images',root/split/'labels'),(root/'images'/split,root/'labels'/split)]:
        if a.is_dir() and b.is_dir():return a,b
    raise FileNotFoundError(f'missing image/labels for {split}')

def audit(root,out, strict=True):
    root=Path(root).resolve();out=Path(out).resolve();out.mkdir(parents=True,exist_ok=True)
    stats={}; rows=[]; issues=[]; names={}; bbox_total=0; label_geometry=Counter()
    for split in EXPECTED:
        idir,ldir=locate(root,split)
        imgs=sorted(p for p in idir.iterdir() if p.is_file() and p.suffix.lower() in EXTENSIONS)
        lbls={p.stem:p for p in ldir.glob('*.txt')}
        if len(imgs)!=EXPECTED[split]:issues.append({'type':'unexpected_split_count','split':split,'actual':len(imgs),'expected':EXPECTED[split]})
        all_stems={p.stem for p in imgs}
        for stem in sorted(set(lbls)-all_stems):issues.append({'type':'orphan_label','split':split,'stem':stem})
        for img in imgs:
            lbl=lbls.get(img.stem)
            if not lbl:issues.append({'type':'missing_label','split':split,'file':img.name});continue
            lines=[z.strip() for z in lbl.read_text(encoding='utf8').splitlines() if z.strip()]
            for line in lines:
                t=line.split()
                try:
                    cid=int(t[0]); v=[float(x) for x in t[1:]]
                    if cid not in range(17) or not all(-1e-8 <= z <= 1+1e-8 for z in v):raise ValueError()
                    if len(v)==4:
                        if v[2]<=0 or v[3]<=0:raise ValueError()
                        label_geometry['bbox_xywh']+=1
                    elif len(v)>=6 and len(v)%2==0:
                        # Roboflow's YOLOv11 export mixes boxes with polygon vertex
                        # sequences for segmentation-shaped annotations (not errors).
                        # Preserve the polygons; do NOT silently convert to boxes.
                        xs=v[::2];ys=v[1::2]
                        if max(xs)-min(xs)<=0 or max(ys)-min(ys)<=0:raise ValueError()
                        label_geometry['polygon_xy']+=1
                    else:raise ValueError()
                except (ValueError,IndexError):issues.append({'type':'bad_label','split':split,'file':lbl.name,'raw':line[:100]})
            bbox_total+=len(lines)
            data=img.read_bytes();sh=hashlib.sha256(data).hexdigest()
            try:
                with Image.open(img) as im:
                    rgb=ImageOps.exif_transpose(im).convert('RGB')
                    pix=hashlib.sha256(f'{rgb.width}:{rgb.height}:'.encode()+rgb.tobytes()).hexdigest()
                    dh=d_hash(im)
            except Exception as e:
                issues.append({'type':'unreadable_image','split':split,'file':img.name,'error':str(e)[:160]});continue
            rows.append({'split':split,'file':img.name,'source_file_sha256':sh,'pixels_sha256':pix,'dhash64':f'{dh:016x}', 'width':rgb.width,'height':rgb.height,'labels':len(lines), 'known_video_family':known_family(img.name),'normalized_filename':normalized_name(img.name)})
        stats[split]={'images':len(imgs),'labels':sum(z['labels'] for z in rows if z['split']==split)}
    if bbox_total !=16300:issues.append({'type':'unexpected_bbox_count','actual':bbox_total,'expected':16300})
    for key in ['source_file_sha256','pixels_sha256']:
        d=defaultdict(list)
        for r in rows:d[r[key]].append(r)
        for val,rset in d.items():
            if len({r['split'] for r in rset})>1:issues.append({'type':'cross_split_'+key,'images':[{'split':r['split'],'file':r['file']} for r in rset]})
    families=defaultdict(set)
    for r in rows:
        if r['known_video_family']:families[r['known_video_family']].add(r['split'])
    known_violations={k:sorted(v) for k,v in families.items() if len(v)>1}
    for k,v in known_violations.items():issues.append({'type':'known_video_family_cross_split','family':k,'splits':v})
    # dHash flags must be visually adjudicated, and can include benign lookalikes.
    candidates=[]; seen=set(); x=list(rows)
    for i in range(len(x)):
        a=x[i]; ha=int(a['dhash64'],16)
        for j in range(i+1,len(x)):
            b=x[j]
            if a['split']==b['split']:continue
            distance=(ha^int(b['dhash64'],16)).bit_count()
            if distance<=4:candidates.append({'a_split':a['split'],'a_file':a['file'],'b_split':b['split'],'b_file':b['file'],'dhash_distance':distance,'status':'CANDIDATE_REQUIRES_VISUAL_REVIEW'})
    with (out/'clean17_file_manifest.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]) if rows else ['split','file']);w.writeheader();w.writerows(rows)
    with (out/'cross_split_dhash_review.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=['a_split','a_file','b_split','b_file','dhash_distance','status']);w.writeheader();w.writerows(candidates)
    status='PASS_FILE_INTEGRITY_ONLY' if not issues else 'FAIL_OR_REVIEW_REQUIRED'
    summary={'project':'SEER-PPE','source':'master-fylfq/altayyar-0oflt-lafos-qqauz-ty5nh version 2 via historical correction script','status':status,'counts':stats,'objects':bbox_total,'annotation_geometry_types':dict(label_geometry),'independent_acquisition_groups':'NOT_ESTABLISHED','rights':'NOT_ESTABLISHED','human_double_review':'NOT_STARTED','known_video_groups_cross_split':known_violations,'cross_split_dhash_candidates':len(candidates),'issues':issues,'critical_problem_count':len(issues),'file_manifest_sha256':hashlib.sha256((out/'clean17_file_manifest.csv').read_bytes()).hexdigest(),'raw_images_not_committed':True}
    (out/'freeze_summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf8')
    return summary

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('clean_root');p.add_argument('--out',required=True);a=p.parse_args()
    r=audit(a.clean_root,a.out);print(json.dumps({k:v for k,v in r.items() if k not in {'issues'}},indent=2));raise SystemExit(0 if r['status']=='PASS_FILE_INTEGRITY_ONLY' else 3)
