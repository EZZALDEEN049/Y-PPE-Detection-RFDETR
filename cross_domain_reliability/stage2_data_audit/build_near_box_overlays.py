#!/usr/bin/env python3
"""Build visual overlays for near-identical same-class bbox audit findings.

Reads the original exported image/label files plus the Stage 2
`near_identical_boxes.csv`. For each reported pair, it reconstructs the
corresponding rows (supporting both YOLO bbox and polygon rows), draws the two
candidate boxes, and writes an adjudication CSV plus JPG overlays.

The dataset is never modified.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path
from typing import Optional

import yaml
from PIL import Image, ImageDraw, ImageFont

IMAGE_EXTS = {'.jpg','.jpeg','.png','.bmp','.webp','.tif','.tiff'}


def find_image_dir(root: Path, split: str) -> Optional[Path]:
    for p in [root/'images'/split, root/split/'images', root/split, root/'Images'/split, root/split/'Images']:
        if p.is_dir():
            return p
    return None


def find_label_dir(root: Path, split: str) -> Optional[Path]:
    for p in [root/'labels'/split, root/split/'labels', root/'Labels'/split, root/split/'Labels']:
        if p.is_dir():
            return p
    return None


def class_names(data_yaml: Path):
    data = yaml.safe_load(data_yaml.read_text(encoding='utf-8'))
    names = data.get('names')
    if isinstance(names, list):
        return [str(x) for x in names]
    if isinstance(names, dict):
        return [str(names[i] if i in names else names[str(i)]) for i in range(len(names))]
    return []


def normalize_row(line: str):
    parts = line.split()
    if len(parts) == 5:
        vals = [float(x) for x in parts]
        cls, x, y, w, h = vals
        return int(cls), x, y, w, h, 'bbox'
    if len(parts) >= 7 and len(parts) % 2 == 1:
        vals = [float(x) for x in parts]
        cls = int(vals[0]); coords = vals[1:]
        xs, ys = coords[0::2], coords[1::2]
        if len(xs) < 3 or len(xs) != len(ys):
            raise ValueError('invalid polygon')
        x1,x2=min(xs),max(xs); y1,y2=min(ys),max(ys)
        return cls, (x1+x2)/2, (y1+y2)/2, x2-x1, y2-y1, 'polygon'
    raise ValueError('unsupported row')


def find_image(image_dir: Path, stem: str):
    for ext in IMAGE_EXTS:
        p=image_dir/(stem+ext)
        if p.exists(): return p
    for p in image_dir.rglob('*'):
        if p.is_file() and p.suffix.lower() in IMAGE_EXTS and p.stem==stem:
            return p
    return None


def yolo_xyxy(row, width, height):
    _,x,y,w,h,_=row
    return ((x-w/2)*width,(y-h/2)*height,(x+w/2)*width,(y+h/2)*height)


def load_nonempty_rows(label_path: Path):
    rows=[]
    for physical_no,line in enumerate(label_path.read_text(encoding='utf-8', errors='replace').splitlines(),1):
        s=' '.join(line.split())
        if not s: continue
        try:
            norm=normalize_row(s)
        except Exception:
            norm=None
        rows.append((physical_no,s,norm))
    return rows


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--dataset-root',required=True,type=Path)
    ap.add_argument('--near-box-csv',required=True,type=Path)
    ap.add_argument('--data-yaml',required=True,type=Path)
    ap.add_argument('--out',required=True,type=Path)
    args=ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    overlays=args.out/'overlays'; overlays.mkdir(exist_ok=True)
    names=class_names(args.data_yaml)
    findings=list(csv.DictReader(args.near_box_csv.open(encoding='utf-8-sig')))
    output=[]
    font=ImageFont.load_default()

    for idx,f in enumerate(findings,1):
        split=f['split']
        label_name=Path(f['file']).name
        m=re.search(r'rows\s+(\d+),(\d+);\s*IoU=([0-9.]+)',f.get('detail',''))
        if not m:
            continue
        r1,r2,iou=int(m.group(1)),int(m.group(2)),float(m.group(3))
        ld=find_label_dir(args.dataset_root,split); imd=find_image_dir(args.dataset_root,split)
        label_path=ld/label_name if ld else None
        image_path=find_image(imd, Path(label_name).stem) if imd else None
        status='ok'; note=''
        row1=row2=None
        if not label_path or not label_path.exists() or not image_path:
            status='missing_source_file'; note='label or image not found'
        else:
            rows=load_nonempty_rows(label_path)
            if not (1 <= r1 <= len(rows) and 1 <= r2 <= len(rows)):
                status='row_index_out_of_range'; note=f'nonempty_rows={len(rows)}'
            else:
                row1=rows[r1-1]; row2=rows[r2-1]
                if row1[2] is None or row2[2] is None:
                    status='unparseable_row'; note='one or both rows could not be normalized'

        out_name=f'NB{idx:03d}_{Path(label_name).stem}.jpg'
        out_path=overlays/out_name
        if status=='ok':
            with Image.open(image_path) as im:
                im=im.convert('RGB'); draw=ImageDraw.Draw(im)
                for tag,entry,width_line in [('A',row1,5),('B',row2,2)]:
                    row=entry[2]; box=yolo_xyxy(row,im.width,im.height)
                    shade='black' if tag=='A' else 'white'
                    draw.rectangle(box, outline=shade, width=width_line)
                    cls=row[0]; cname=names[cls] if 0 <= cls < len(names) else f'class_{cls}'
                    x1,y1,_,_=box
                    draw.text((max(0,x1+3),max(0,y1+3)),f'{tag}: {cname} row {r1 if tag=="A" else r2}',fill=shade,font=font)
                footer=f'IoU={iou:.6f} | A={row1[2][5]} | B={row2[2][5]}'
                draw.rectangle((0,max(0,im.height-22),im.width,im.height),fill='white')
                draw.text((5,max(0,im.height-18)),footer,fill='black',font=font)
                im.save(out_path,quality=92)
        output.append({
            'case_id':f'NB{idx:03d}','split':split,'image_file':image_path.name if image_path else '',
            'label_file':label_name,'reported_row_a':r1,'reported_row_b':r2,'iou':iou,
            'class_a': (names[row1[2][0]] if status=='ok' and 0 <= row1[2][0] < len(names) else ''),
            'class_b': (names[row2[2][0]] if status=='ok' and 0 <= row2[2][0] < len(names) else ''),
            'source_kind_a': row1[2][5] if status=='ok' else '',
            'source_kind_b': row2[2][5] if status=='ok' else '',
            'raw_row_a': row1[1] if row1 else '', 'raw_row_b': row2[1] if row2 else '',
            'overlay_file': out_name if status=='ok' else '',
            'status':status,'decision':'','notes':note,
        })

    csv_path=args.out/'near_identical_box_review.csv'
    fields=list(output[0].keys()) if output else ['case_id']
    with csv_path.open('w',newline='',encoding='utf-8-sig') as f:
        w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(output)
    from collections import Counter
    summary={'reported_cases':len(findings),'overlay_cases':sum(r['status']=='ok' for r in output),'statuses':dict(Counter(r['status'] for r in output))}
    (args.out/'near_identical_box_review_summary.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False),encoding='utf-8')
    print(json.dumps(summary,indent=2,ensure_ascii=False))

if __name__=='__main__':
    main()
