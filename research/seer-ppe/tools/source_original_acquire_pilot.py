#!/usr/bin/env python3
"""SEER-PPE read-only six-Source Train/Valid pilot. Images never leave runner.

Roboflow project.image(Source ID) provides original URL at runtime. No URL,
secret, raw media or image base64 is committed or included in report/logs.
"""
import argparse
import json
import os
import re
import sys
from pathlib import Path
from urllib.parse import urlsplit

from source_pixel_hash_audit import _fingerprint

SOURCE_ID = re.compile(r"[A-Za-z0-9_-]{10,128}\Z")
MAX_BYTES = 25 * 1024 * 1024


def scope(manifest, checkpoint):
    if manifest.get('project') != 'softyyemen/altayyar-0oflt-lafos-qqauz':
        raise ValueError('wrong project')
    rows = manifest.get('images', [])
    if len(rows) != 2093 or manifest.get('image_count') != 2093:
        raise ValueError('wrong manifest count')
    if sum(x['split']=='train' for x in rows)!=1625 or sum(x['split']=='valid' for x in rows)!=468:
        raise ValueError('wrong split counts')
    if len({x['image_id'] for x in rows})!=2093:
        raise ValueError('repeated Source ID')
    by_id={x['image_id']:x for x in rows}
    if any(x['split'] not in ('train','valid') or not SOURCE_ID.fullmatch(x['image_id']) for x in rows):
        raise ValueError('unsafe Source ID or split')
    pairs=checkpoint['live_source_verification']['pairs']
    if len(pairs)!=3 or len({p[s]['id'] for p in pairs for s in ('train','valid')})!=6:
        raise ValueError('pilot expected 3 pairs/6 unique Source IDs')
    for p in pairs:
        for split in ('train','valid'):
            x=p[split]; m=by_id.get(x['id'])
            if not m or (m['split'],m['filename'],m['width'],m['height']) != (split,x['filename'],*x['size']):
                raise ValueError('Source ID/filename/dimensions mismatch')
    return pairs,by_id


def download(project, image_id):
    import requests
    details=project.image(image_id)
    urls=details.get('urls',{}) if isinstance(details,dict) else {}
    link=urls.get('original') if isinstance(urls,dict) else None
    if not link:
        raise ValueError('ORIGINAL_URL_UNAVAILABLE')
    parsed=urlsplit(link)
    if parsed.scheme!='https' or parsed.hostname!='source.roboflow.com' or parsed.username or parsed.password:
        raise ValueError('ORIGINAL_URL_HOST_UNTRUSTED')
    with requests.get(link,timeout=(10,55),stream=True,allow_redirects=False) as r:
        if r.status_code!=200: raise ValueError('ORIGINAL_HTTP_NOT_200')
        mime=r.headers.get('content-type','').lower()
        if mime and not (mime.startswith('image/') or mime.startswith('application/octet-stream')):
            raise ValueError('ORIGINAL_CONTENT_TYPE_INVALID')
        blocks=[]; count=0
        for chunk in r.iter_content(262144):
            count+=len(chunk)
            if count>MAX_BYTES:raise ValueError('ORIGINAL_FILE_TOO_LARGE')
            blocks.append(chunk)
    return b''.join(blocks)


def run(pairs,by_id,retrieve,root):
    root.mkdir(parents=True,exist_ok=True)
    rows=[];issues=[]
    safe_errors={'ORIGINAL_URL_UNAVAILABLE','ORIGINAL_URL_HOST_UNTRUSTED','ORIGINAL_HTTP_NOT_200',
                 'ORIGINAL_CONTENT_TYPE_INVALID','ORIGINAL_FILE_TOO_LARGE'}
    for p in pairs:
        for split in ('valid','train'):
            x=p[split]
            try:
                data=retrieve(x['id'])
                path=root / split / (x['id']+'.jpg')
                path.parent.mkdir(parents=True,exist_ok=True)
                path.write_bytes(data)
                fp=_fingerprint(path)
                if (fp['width'],fp['height'])!=(by_id[x['id']]['width'],by_id[x['id']]['height']):
                    raise ValueError('PIXEL_DIMENSION_MISMATCH')
                rows.append({'split':split,'id':x['id'],'filename':x['filename'],**fp})
            except Exception as e:
                # SDK/network exceptions can contain signed URLs: never print them.
                msg=str(e) if isinstance(e,ValueError) else ''
                reason=msg if msg in safe_errors|{'PIXEL_DIMENSION_MISMATCH'} else 'ORIGINAL_FETCH_OR_DECODE_ERROR'
                issues.append({'source_id':x['id'],'split':split,'error_code':reason})
    found={x['id']:x for x in rows}
    pair_out=[]
    for p in pairs:
        a=found.get(p['valid']['id']);b=found.get(p['train']['id'])
        one={'valid_id':p['valid']['id'],'train_id':p['train']['id'],
             'valid_filename':p['valid']['filename'],'train_filename':p['train']['filename'],
             'embedding_cosine_from_prior_triage':p['cosine']}
        if a and b:
            distance=(int(a['dhash64'],16)^int(b['dhash64'],16)).bit_count()
            byte_equal=a['bytes_sha256']==b['bytes_sha256']
            rgb_equal=a['rgb_pixel_sha256']==b['rgb_pixel_sha256']
            one.update({'raw_byte_equal':byte_equal,'decoded_rgb_equal':rgb_equal,'dhash_hamming':distance,
                        'valid_raw_sha256':a['bytes_sha256'],'train_raw_sha256':b['bytes_sha256'],
                        'valid_rgb_sha256':a['rgb_pixel_sha256'],'train_rgb_sha256':b['rgb_pixel_sha256'],
                        'status':'BYTE_IDENTICAL' if byte_equal else 'RGB_IDENTICAL' if rgb_equal
                        else 'DHASH_NEAR_REVIEW' if distance<=8 else 'PIXELS_DIFFER_SOURCE_UNDECIDED'})
        else:one['status']='UNTESTED_INPUT_INCOMPLETE'
        pair_out.append(one)
    return {'schema_version':'seer-ppe/original-source-pilot/v0.1','scope':'TRAIN_VALID_SIX_SOURCE_IDS_NO_TEST',
            'expected_images':6,'acquired_and_decoded_images':len(rows),
            'complete':len(rows)==6 and not issues,'pairs':pair_out,'errors':issues,
            'image_bytes_uploaded':False,'original_urls_exposed':False,
            'human_source_signoff':False,'scoring_ready':False}


def main():
    pa=argparse.ArgumentParser()
    pa.add_argument('--manifest',type=Path,required=True)
    pa.add_argument('--checkpoint',type=Path,required=True)
    pa.add_argument('--temp-root',type=Path,required=True)
    pa.add_argument('--report',type=Path,required=True)
    args=pa.parse_args()
    manifest=json.loads(args.manifest.read_text(encoding='utf-8'))
    checkpoint=json.loads(args.checkpoint.read_text(encoding='utf-8'))
    pairs,by_id=scope(manifest,checkpoint)
    if not os.environ.get('ROBOFLOW_API_KEY'):raise SystemExit('ROBOFLOW_API_KEY_NOT_CONFIGURED')
    from roboflow import Roboflow
    project=Roboflow(api_key=os.environ['ROBOFLOW_API_KEY']).workspace('softyyemen').project('altayyar-0oflt-lafos-qqauz')
    output=run(pairs,by_id,lambda source_id:download(project,source_id),args.temp_root)
    args.report.parent.mkdir(parents=True,exist_ok=True)
    args.report.write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'originals_decoded':output['acquired_and_decoded_images'],
                      'complete':output['complete'],'errors':len(output['errors']),
                      'scientific_scoring_ready':False}))
    return 0 if output['complete'] else 2

if __name__=='__main__':sys.exit(main())
