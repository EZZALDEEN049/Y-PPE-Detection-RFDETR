#!/usr/bin/env python3
import argparse, csv, json, shutil
from pathlib import Path

IMAGE_EXTS={'.jpg','.jpeg','.png','.bmp','.tif','.tiff','.webp'}

def split_dirs(root: Path, split: str):
    candidates=[
        (root/split/'images', root/split/'labels'),
        (root/'images'/split, root/'labels'/split),
    ]
    for img_dir,lbl_dir in candidates:
        if img_dir.is_dir() and lbl_dir.is_dir():
            return img_dir,lbl_dir
    raise FileNotFoundError(f'Could not locate image/label directories for split={split}')

def dedupe_exact_rows(labels_root: Path):
    removed=0; files_changed=0
    for p in sorted(labels_root.rglob('*.txt')):
        raw=p.read_text(encoding='utf-8').splitlines()
        seen=set(); out=[]; local=0
        for line in raw:
            key=line.strip()
            if key and key in seen:
                removed+=1; local+=1
                continue
            if key:
                seen.add(key)
            out.append(line)
        if local:
            p.write_text('\n'.join(out)+'\n',encoding='utf-8')
            files_changed+=1
    return removed,files_changed

def remove_near_box_rows(root: Path, manifest: Path):
    removed=0; details=[]
    with manifest.open(newline='',encoding='utf-8') as f:
        for row in csv.DictReader(f):
            split=row['split']; label_file=row['label_file']; target=row['raw_row_to_remove'].strip()
            _,lbl_dir=split_dirs(root,split)
            p=lbl_dir/label_file
            if not p.exists():
                raise FileNotFoundError(f'Near-box target label missing: {p}')
            lines=p.read_text(encoding='utf-8').splitlines()
            matched=[i for i,x in enumerate(lines) if x.strip()==target]
            if len(matched)!=1:
                raise RuntimeError(f'Expected exactly one near-box row in {p}, found {len(matched)}')
            idx=matched[0]
            lines.pop(idx)
            p.write_text('\n'.join(lines)+'\n',encoding='utf-8')
            removed+=1
            details.append({'split':split,'label_file':label_file,'removed_line_1based':idx+1,'raw_row':target})
    return removed,details

def apply_file_manifest(root: Path, manifest: Path):
    excluded=0; retained=0; details=[]
    with manifest.open(newline='',encoding='utf-8') as f:
        for row in csv.DictReader(f):
            action=row['action'].strip().lower(); split=row['split']; fn=row['file']
            if action=='retain':
                retained+=1
                continue
            if action!='exclude':
                raise ValueError(f'Unexpected action={action}')
            img_dir,lbl_dir=split_dirs(root,split)
            img=img_dir/fn
            if not img.exists():
                raise FileNotFoundError(f'Image listed for exclusion not found: {img}')
            label=lbl_dir/(img.stem+'.txt')
            if not label.exists():
                raise FileNotFoundError(f'Label paired with exclusion image not found: {label}')
            img.unlink(); label.unlink(); excluded+=1
            details.append({'split':split,'image':fn,'label':label.name,'reason':row.get('reason','')})
    return excluded,retained,details

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
    ap.add_argument('--near-box-manifest',required=True)
    ap.add_argument('--expected-exclusions',type=int,default=39)
    ap.add_argument('--expected-exact-row-removals',type=int,default=68)
    ap.add_argument('--expected-near-box-removals',type=int,default=1)
    ap.add_argument('--summary-out',required=True)
    args=ap.parse_args()
    src=Path(args.root).resolve(); out=Path(args.out).resolve()
    if out.exists(): shutil.rmtree(out)
    shutil.copytree(src,out)

    exact_removed, exact_files_changed=dedupe_exact_rows(out)
    near_removed, near_details=remove_near_box_rows(out,Path(args.near_box_manifest))
    excluded, retained, excluded_details=apply_file_manifest(out,Path(args.file_manifest))

    if exact_removed!=args.expected_exact_row_removals:
        raise RuntimeError(f'Exact duplicate removal count mismatch: expected {args.expected_exact_row_removals}, got {exact_removed}')
    if near_removed!=args.expected_near_box_removals:
        raise RuntimeError(f'Near-box removal count mismatch: expected {args.expected_near_box_removals}, got {near_removed}')
    if excluded!=args.expected_exclusions:
        raise RuntimeError(f'File exclusion count mismatch: expected {args.expected_exclusions}, got {excluded}')

    summary={
        'source_root':str(src), 'clean_root':str(out),
        'exact_duplicate_rows_removed':exact_removed,
        'exact_duplicate_label_files_changed':exact_files_changed,
        'near_identical_rows_removed':near_removed,
        'source_images_excluded':excluded,
        'manifest_retain_rows':retained,
        'splits':{s:count_split(out,s) for s in ('train','valid','test')},
        'near_box_details':near_details,
        'excluded_files':excluded_details,
    }
    sp=Path(args.summary_out); sp.parent.mkdir(parents=True,exist_ok=True)
    sp.write_text(json.dumps(summary,indent=2,ensure_ascii=False),encoding='utf-8')
    print(json.dumps(summary,indent=2,ensure_ascii=False))

if __name__=='__main__': main()
