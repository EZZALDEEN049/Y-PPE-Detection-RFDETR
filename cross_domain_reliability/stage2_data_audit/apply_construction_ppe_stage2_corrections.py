#!/usr/bin/env python3
import argparse, csv, json, shutil
from pathlib import Path

IMAGE_EXTS={'.jpg','.jpeg','.png','.bmp','.tif','.tiff','.webp'}

def split_dirs(root: Path, split: str):
    candidates=[
        (root/'images'/split, root/'labels'/split),
        (root/split/'images', root/split/'labels'),
    ]
    for img_dir,lbl_dir in candidates:
        if img_dir.is_dir() and lbl_dir.is_dir():
            return img_dir,lbl_dir
    raise FileNotFoundError(f'Could not locate image/label directories for split={split}')

def dedupe_exact_rows(root: Path):
    removed=0; files_changed=0; details=[]
    for p in sorted((root/'labels').rglob('*.txt')):
        raw=p.read_text(encoding='utf-8').splitlines()
        seen=set(); out=[]; local=[]
        for idx,line in enumerate(raw,1):
            key=line.strip()
            if key and key in seen:
                removed+=1; local.append({'line_1based':idx,'row':key}); continue
            if key: seen.add(key)
            out.append(line)
        if local:
            p.write_text('\n'.join(out)+'\n',encoding='utf-8')
            files_changed+=1
            details.append({'label_file':str(p.relative_to(root)),'removed':local})
    return removed,files_changed,details

def remove_orphan_manifest(root: Path, manifest: Path):
    removed=[]
    with manifest.open(newline='',encoding='utf-8') as f:
        for row in csv.DictReader(f):
            split=row['split'].strip(); fn=row['label_file'].strip()
            _,lbl_dir=split_dirs(root,split)
            p=lbl_dir/fn
            if not p.exists(): raise FileNotFoundError(f'Orphan label listed but not found: {p}')
            p.unlink(); removed.append({'split':split,'label_file':fn,'reason':row.get('reason','')})
    return removed

def apply_file_manifest(root: Path, manifest: Path):
    excluded=[]
    with manifest.open(newline='',encoding='utf-8') as f:
        for row in csv.DictReader(f):
            if row['action'].strip().lower()!='exclude':
                raise ValueError(f"Only exclude actions are supported, got {row['action']}")
            split=row['split'].strip(); fn=row['file'].strip()
            img_dir,lbl_dir=split_dirs(root,split)
            img=img_dir/fn
            if not img.exists(): raise FileNotFoundError(f'Image listed for exclusion not found: {img}')
            lab=lbl_dir/(img.stem+'.txt')
            if not lab.exists(): raise FileNotFoundError(f'Paired label missing for exclusion image: {lab}')
            img.unlink(); lab.unlink()
            excluded.append({'split':split,'image':fn,'label':lab.name,'reason':row.get('reason',''),'evidence_pairs':row.get('evidence_pairs','')})
    return excluded

def count_split(root: Path, split: str):
    img_dir,lbl_dir=split_dirs(root,split)
    images=sum(1 for p in img_dir.iterdir() if p.is_file() and p.suffix.lower() in IMAGE_EXTS)
    labels=sum(1 for p in lbl_dir.glob('*.txt'))
    return {'images':images,'labels':labels}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--root',required=True)
    ap.add_argument('--out',required=True)
    ap.add_argument('--file-manifest',required=True)
    ap.add_argument('--orphan-label-manifest',required=True)
    ap.add_argument('--expected-exclusions',type=int,default=64)
    ap.add_argument('--expected-orphan-removals',type=int,default=10)
    ap.add_argument('--expected-exact-row-removals',type=int,default=1)
    ap.add_argument('--summary-out',required=True)
    args=ap.parse_args()

    src=Path(args.root).resolve(); out=Path(args.out).resolve()
    if out.exists(): shutil.rmtree(out)
    shutil.copytree(src,out)

    orphan_details=remove_orphan_manifest(out,Path(args.orphan_label_manifest))
    exact_removed, exact_files_changed, exact_details=dedupe_exact_rows(out)
    excluded_details=apply_file_manifest(out,Path(args.file_manifest))

    if len(orphan_details)!=args.expected_orphan_removals:
        raise RuntimeError(f'Orphan removal count mismatch: expected {args.expected_orphan_removals}, got {len(orphan_details)}')
    if exact_removed!=args.expected_exact_row_removals:
        raise RuntimeError(f'Exact duplicate row removal mismatch: expected {args.expected_exact_row_removals}, got {exact_removed}')
    if len(excluded_details)!=args.expected_exclusions:
        raise RuntimeError(f'Image exclusion count mismatch: expected {args.expected_exclusions}, got {len(excluded_details)}')

    summary={
        'source_root':str(src),'clean_root':str(out),
        'orphan_labels_removed':len(orphan_details),
        'exact_duplicate_rows_removed':exact_removed,
        'exact_duplicate_label_files_changed':exact_files_changed,
        'source_images_excluded':len(excluded_details),
        'splits':{s:count_split(out,s) for s in ('train','val','test')},
        'orphan_label_details':orphan_details,
        'exact_duplicate_details':exact_details,
        'excluded_files':excluded_details,
    }
    sp=Path(args.summary_out); sp.parent.mkdir(parents=True,exist_ok=True)
    sp.write_text(json.dumps(summary,indent=2,ensure_ascii=False),encoding='utf-8')
    print(json.dumps(summary,indent=2,ensure_ascii=False))

if __name__=='__main__': main()
