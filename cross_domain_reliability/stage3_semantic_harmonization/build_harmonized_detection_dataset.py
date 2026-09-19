#!/usr/bin/env python3
"""Build a deterministic 9-class bounding-box derivative from a cleaned source dataset.

The script never edits the source dataset. It:
- reads native class order from data.yaml,
- keeps only classes frozen in ontology_frozen_v1.yaml,
- remaps them to canonical IDs 0..8,
- converts retained YOLO polygon rows to enclosing axis-aligned YOLO boxes,
- copies every cleaned source image into standardized train/val/test layout,
- writes empty label files when an image has no retained shared-class instance,
- records counts and SHA256 fingerprints for reproducibility.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from collections import Counter
from pathlib import Path

import yaml

IMAGE_EXTS={'.jpg','.jpeg','.png','.bmp','.tif','.tiff','.webp'}


def sha256_file(path: Path, chunk_size: int=1024*1024) -> str:
    h=hashlib.sha256()
    with path.open('rb') as f:
        while True:
            b=f.read(chunk_size)
            if not b: break
            h.update(b)
    return h.hexdigest()


def load_names(path: Path):
    data=yaml.safe_load(path.read_text(encoding='utf-8'))
    names=data.get('names')
    if isinstance(names,list): return [str(x) for x in names]
    if isinstance(names,dict):
        out=[]
        for i in range(len(names)):
            out.append(str(names[i] if i in names else names[str(i)]))
        return out
    raise RuntimeError(f'Could not read ordered names from {path}')


def split_dirs(root: Path, split: str):
    candidates=[
        (root/split/'images', root/split/'labels'),
        (root/'images'/split, root/'labels'/split),
    ]
    for img,lbl in candidates:
        if img.is_dir() and lbl.is_dir(): return img,lbl
    raise FileNotFoundError(f'Could not locate split {split} under {root}')


def parse_to_bbox(parts, line_desc: str):
    if len(parts)==5:
        cls=float(parts[0]); x,y,w,h=map(float,parts[1:])
        if not cls.is_integer(): raise RuntimeError(f'Non-integer class id: {line_desc}')
        return int(cls),x,y,w,h,'bbox'
    if len(parts)>=7 and (len(parts)-1)%2==0:
        cls=float(parts[0])
        if not cls.is_integer(): raise RuntimeError(f'Non-integer class id: {line_desc}')
        coords=list(map(float,parts[1:]))
        xs=coords[0::2]; ys=coords[1::2]
        if len(xs)<3: raise RuntimeError(f'Polygon has fewer than 3 points: {line_desc}')
        if any(v<0 or v>1 for v in coords): raise RuntimeError(f'Polygon coordinate outside [0,1]: {line_desc}')
        x1,x2=min(xs),max(xs); y1,y2=min(ys),max(ys)
        w=x2-x1; h=y2-y1; x=(x1+x2)/2; y=(y1+y2)/2
        if w<=0 or h<=0: raise RuntimeError(f'Degenerate polygon envelope: {line_desc}')
        return int(cls),x,y,w,h,'polygon'
    raise RuntimeError(f'Unsupported YOLO row with {len(parts)} fields: {line_desc}')


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--root',required=True)
    ap.add_argument('--data-yaml',required=True)
    ap.add_argument('--ontology',required=True)
    ap.add_argument('--dataset-key',required=True,choices=['Y-PPE','Construction-PPE'])
    ap.add_argument('--splits',required=True,help='Comma list of source_split:output_split, e.g. train:train,valid:val,test:test')
    ap.add_argument('--out',required=True)
    ap.add_argument('--summary-out',required=True)
    args=ap.parse_args()

    src=Path(args.root).resolve(); out=Path(args.out).resolve()
    if out.exists(): shutil.rmtree(out)
    out.mkdir(parents=True)

    native_names=load_names(Path(args.data_yaml))
    onto=yaml.safe_load(Path(args.ontology).read_text(encoding='utf-8'))
    shared=onto['shared_classes']
    canonical=[x['canonical'] for x in shared]
    if [x['id'] for x in shared] != list(range(len(shared))):
        raise RuntimeError('Ontology canonical IDs must be contiguous 0..N-1')

    native_field='y_name' if args.dataset_key=='Y-PPE' else 'c_name'
    name_to_new={x[native_field]:int(x['id']) for x in shared}
    native_id_to_new={i:name_to_new[n] for i,n in enumerate(native_names) if n in name_to_new}
    split_map=[]
    for spec in args.splits.split(','):
        a,b=spec.split(':',1); split_map.append((a.strip(),b.strip()))

    totals=Counter(); retained_by_class=Counter(); dropped_by_native=Counter(); split_summary={}; manifest=[]

    for source_split,target_split in split_map:
        src_img,src_lbl=split_dirs(src,source_split)
        dst_img=out/'images'/target_split; dst_lbl=out/'labels'/target_split
        dst_img.mkdir(parents=True,exist_ok=True); dst_lbl.mkdir(parents=True,exist_ok=True)
        images=sorted(p for p in src_img.iterdir() if p.is_file() and p.suffix.lower() in IMAGE_EXTS)
        split_counts=Counter(images=len(images))
        for img in images:
            lab=src_lbl/(img.stem+'.txt')
            if not lab.exists(): raise FileNotFoundError(f'Missing source label: {lab}')
            out_rows=[]
            text=lab.read_text(encoding='utf-8',errors='strict').strip()
            if text:
                for line_no,line in enumerate(text.splitlines(),1):
                    stripped=' '.join(line.split())
                    if not stripped: continue
                    parts=stripped.split()
                    old_cls,x,y,w,h,fmt=parse_to_bbox(parts,f'{lab}:{line_no}')
                    if not 0<=old_cls<len(native_names):
                        raise RuntimeError(f'Class id out of range at {lab}:{line_no}: {old_cls}')
                    totals['source_rows']+=1
                    if fmt=='polygon': totals['polygon_rows_seen']+=1
                    if old_cls not in native_id_to_new:
                        totals['dropped_nonshared_rows']+=1
                        if fmt=='polygon': totals['polygon_rows_dropped_nonshared']+=1
                        dropped_by_native[native_names[old_cls]]+=1
                        continue
                    new_cls=native_id_to_new[old_cls]
                    if not (0<=x<=1 and 0<=y<=1 and 0<w<=1 and 0<h<=1):
                        raise RuntimeError(f'Invalid normalized bbox after conversion at {lab}:{line_no}')
                    x1,y1,x2,y2=x-w/2,y-h/2,x+w/2,y+h/2
                    if x1 < -1e-6 or y1 < -1e-6 or x2 > 1+1e-6 or y2 > 1+1e-6:
                        raise RuntimeError(f'BBox outside image after conversion at {lab}:{line_no}')
                    out_rows.append(f'{new_cls} {x:.9f} {y:.9f} {w:.9f} {h:.9f}')
                    totals['retained_rows']+=1
                    if fmt=='polygon': totals['polygon_rows_converted']+=1
                    retained_by_class[canonical[new_cls]]+=1
            if not out_rows: split_counts['empty_label_images']+=1
            split_counts['retained_instances']+=len(out_rows)
            dst_i=dst_img/img.name; dst_l=dst_lbl/(img.stem+'.txt')
            shutil.copy2(img,dst_i)
            dst_l.write_text(('\n'.join(out_rows)+'\n') if out_rows else '',encoding='utf-8')
            manifest.append({
                'split':target_split,'image':img.name,'label':dst_l.name,
                'image_sha256':sha256_file(dst_i),'label_sha256':sha256_file(dst_l),
                'retained_instances':len(out_rows)
            })
        split_summary[target_split]=dict(split_counts)

    data_yaml={
        'path':'.','train':'images/train','val':'images/val','test':'images/test',
        'names':canonical,'nc':len(canonical)
    }
    (out/'data.yaml').write_text(yaml.safe_dump(data_yaml,sort_keys=False),encoding='utf-8')
    with (out/'manifest.jsonl').open('w',encoding='utf-8') as f:
        for row in manifest: f.write(json.dumps(row,sort_keys=True)+'\n')
    dataset_fingerprint=hashlib.sha256((out/'manifest.jsonl').read_bytes()).hexdigest()

    summary={
        'dataset':args.dataset_key,
        'source_root':str(src),'output_root':str(out),
        'canonical_names':canonical,
        'source_class_names':native_names,
        'native_to_canonical_id':{native_names[k]:v for k,v in sorted(native_id_to_new.items())},
        'splits':split_summary,
        'totals':dict(totals),
        'retained_instances_by_canonical':dict(retained_by_class),
        'dropped_instances_by_native_class':dict(dropped_by_native),
        'dataset_fingerprint_sha256':dataset_fingerprint,
        'policy':{
            'keep_all_clean_source_images':True,
            'drop_nonshared_annotation_rows':True,
            'polygon_to_bbox':'enclosing_axis_aligned_bbox',
            'test_images_visually_opened':False
        }
    }
    sp=Path(args.summary_out); sp.parent.mkdir(parents=True,exist_ok=True)
    sp.write_text(json.dumps(summary,indent=2,ensure_ascii=False),encoding='utf-8')
    print(json.dumps(summary,indent=2,ensure_ascii=False))

if __name__=='__main__': main()
