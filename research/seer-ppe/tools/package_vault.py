#!/usr/bin/env python3
"""Produce a deterministic segmented internal-research backup; no web, no training.

The archive is not approved for public redistribution; store parts in a restricted
Drive folder. Metadata excludes raw images.
"""
import argparse,csv,hashlib,json,zipfile
from pathlib import Path

def digest(path, block=2**20):
    h=hashlib.sha256()
    with Path(path).open('rb') as fh:
        for b in iter(lambda:fh.read(block),b''):h.update(b)
    return h.hexdigest()

def package(root:Path, out:Path, part_bytes:int=48*1024*1024):
    root=root.resolve();out=out.resolve();out.mkdir(parents=True,exist_ok=True)
    assert part_bytes > 1024
    dataset_paths=[p for p in root.rglob('*') if p.is_file()]
    images=[p for p in dataset_paths if p.suffix.lower() in ('.jpg','.jpeg','.png','.bmp','.tif','.tiff','.webp') and p.parent.name=='images']
    assert len(images)==2288, f'Expected 2288 images, got {len(images)}'
    zip_path=out/'Y-PPE-v2-Clean17-INTERNAL-RESEARCH.zip'
    # ZIP_STORED avoids recompressing JPEGs and prevents compression-version drift.
    with zipfile.ZipFile(zip_path,'w',compression=zipfile.ZIP_STORED,allowZip64=True) as z:
        for p in sorted(dataset_paths):
            arc=p.relative_to(root).as_posix()
            info=zipfile.ZipInfo(arc, date_time=(2026,9,20,0,0,0))
            info.compress_type=zipfile.ZIP_STORED
            z.writestr(info,p.read_bytes())
    # Confirm archive round-trip and declared number of paths
    with zipfile.ZipFile(zip_path) as z:
        bad=z.testzip()
        assert not bad, f'bad ZIP member: {bad}'
        assert len(z.namelist())==len(dataset_paths)
    parts=[]
    with zip_path.open('rb') as fh:
        i=0
        while True:
            data=fh.read(part_bytes)
            if not data:break
            name=f'Y-PPE-v2-Clean17-INTERNAL-RESEARCH.zip.part_{i:02d}'
            p=out/name
            p.write_bytes(data)
            parts.append({'name':name,'size_bytes':p.stat().st_size,'sha256':digest(p)})
            i+=1
    assert len(parts)<=12, f'{len(parts)} chunks exceeds upload steps; abort incomplete backup'
    summary={'archive_file':zip_path.name,'archive_size_bytes':zip_path.stat().st_size,
             'archive_sha256':digest(zip_path),'image_count':len(images),'all_file_count':len(dataset_paths),
             'part_size_bytes':part_bytes,'parts':parts,
             'redistribution_rights':'NOT_CLEARED','storage_rule':'RESTRICTED_INTERNAL_RESEARCH_ONLY',
             'reassembly':'cat part_00 part_01 ... > Y-PPE-v2-Clean17-INTERNAL-RESEARCH.zip; sha256sum -c archive-sha256.txt'}
    (out/'vault_manifest.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    (out/'archive-sha256.txt').write_text(summary['archive_sha256']+'  '+zip_path.name+'\n',encoding='ascii')
    zip_path.unlink() # no redundant full copy left on runner
    print(json.dumps({k:v for k,v in summary.items() if k!='parts'}|{'part_count':len(parts)}))
    return summary

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--clean-root',type=Path,required=True)
    parser.add_argument('--out',type=Path,required=True)
    parser.add_argument('--chunk-mib',type=int,default=48)
    a=parser.parse_args()
    package(a.clean_root,a.out,a.chunk_mib*1024**2)
