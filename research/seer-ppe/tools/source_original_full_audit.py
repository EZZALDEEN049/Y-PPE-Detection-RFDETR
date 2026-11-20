#!/usr/bin/env python3
"""Read-only original Source audit: 1625 Train + 468 Valid, never Test.

All original images are temporary in RUNNER_TEMP; only Source-ID keyed
fingerprints / cross-split match metadata are reported (no URLs or bytes).
"""
import argparse, json, os, re, sys, time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from source_original_acquire_pilot import download
from source_pixel_hash_audit import audit, _fingerprint

SOURCE_ID = re.compile(r"[A-Za-z0-9_-]{10,128}\Z")


def validate(m):
    rows=m.get('images',[])
    if m.get('project')!='softyyemen/altayyar-0oflt-lafos-qqauz' or len(rows)!=2093 or m.get('image_count')!=2093:
        raise ValueError('WRONG_FROZEN_MANIFEST')
    if Counter(x.get('split') for x in rows)!=Counter({'train':1625,'valid':468}):
        raise ValueError('WRONG_TRAIN_VALID_COUNTS')
    if len({x.get('image_id') for x in rows})!=2093 or any(not SOURCE_ID.fullmatch(x['image_id']) for x in rows):
        raise ValueError('INVALID_SOURCE_IDS')
    if any(not isinstance(x.get('width'),int) or not isinstance(x.get('height'),int)
           or x['width']<=0 or x['height']<=0 for x in rows):
        raise ValueError('INVALID_MANIFEST_DIMENSIONS')
    return rows


def do_one(project, row, root):
    error='ORIGINAL_FETCH_OR_DECODE_FAILED'
    for attempt in range(3):
        try:
            data=download(project,row['image_id'])
            path=root/row['split']/(row['image_id']+'.jpg')
            path.parent.mkdir(parents=True,exist_ok=True)
            path.write_bytes(data)
            f=_fingerprint(path)
            if (f['width'],f['height'])!=(row['width'],row['height']):
                path.unlink(missing_ok=True)
                error='SOURCE_IMAGE_DIMENSIONS_MISMATCH'
                break
            return {'source_id':row['image_id'],'split':row['split'],
                    'filename':row['filename'],**f},None
        except Exception as exc:
            # Exceptions from SDK/network may include credentials or signed URLs.
            error='ORIGINAL_FETCH_OR_DECODE_FAILED'
            if isinstance(exc,ValueError) and str(exc) in {
                'ORIGINAL_URL_UNAVAILABLE','ORIGINAL_URL_HOST_UNTRUSTED',
                'ORIGINAL_HTTP_NOT_200','ORIGINAL_CONTENT_TYPE_INVALID','ORIGINAL_FILE_TOO_LARGE'}:
                error=str(exc)
                if error in ('ORIGINAL_URL_UNAVAILABLE','ORIGINAL_URL_HOST_UNTRUSTED'):
                    break
            if attempt<2:
                time.sleep(1+attempt*2)
    return None,{'source_id':row['image_id'],'split':row['split'],'error_code':error}


def main():
    pa=argparse.ArgumentParser()
    pa.add_argument('--manifest',type=Path,required=True)
    pa.add_argument('--temp-root',type=Path,required=True)
    pa.add_argument('--report',type=Path,required=True)
    pa.add_argument('--workers',type=int,default=4)
    a=pa.parse_args()
    if a.workers<1 or a.workers>6: raise SystemExit('WORKERS_OUT_OF_BOUNDS')
    m=json.loads(a.manifest.read_text(encoding='utf-8'))
    rows=validate(m)
    if not os.getenv('ROBOFLOW_API_KEY'):raise SystemExit('ROBOFLOW_API_KEY_NOT_CONFIGURED')
    from roboflow import Roboflow
    project=Roboflow(api_key=os.environ['ROBOFLOW_API_KEY']).workspace('softyyemen').project('altayyar-0oflt-lafos-qqauz')
    success=[];errors=[]
    # Four workers avoid overwhelming the project/Source API with 2,093 calls.
    with ThreadPoolExecutor(max_workers=a.workers) as ex:
        futures=[ex.submit(do_one,project,row,a.temp_root) for row in rows]
        for f in as_completed(futures):
            item,error=f.result()
            if item:success.append(item)
            else:errors.append(error)
    result=audit(m,a.temp_root)
    result['source_fingerprints']=sorted(success,key=lambda x:(x['split'],x['source_id']))
    result['acquisition_errors']=sorted(errors,key=lambda x:(x['split'],x['source_id']))
    result['original_source_decoded_count']=len(success)
    result['original_source_requested_count']=len(rows)
    result['original_source_audit_status']='FULL_COVERAGE' if result['full_2093_coverage'] and not errors else 'PARTIAL_OR_BLOCKED'
    result['image_bytes_uploaded']=False
    result['original_source_urls_persisted']=False
    result['test_sources_queried']=0
    result['human_source_family_adjudication_complete']=False
    result['scoring_ready']=False
    a.report.parent.mkdir(parents=True,exist_ok=True)
    a.report.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'original_sources_hashed':len(success),'missing':result['missing_count'],
                      'decode_errors':result['decode_error_count'],
                      'acquisition_errors':len(errors),
                      'exact_byte_pairs':len(result['exact_byte_matches']),
                      'exact_rgb_pairs':len(result['exact_decoded_pixel_matches_different_bytes']),
                      'near_dhash_pairs':len(result['dhash_review_candidates']),
                      'complete':result['full_2093_coverage'],'scoring_ready':False}))
    return 0 if result['full_2093_coverage'] and not errors else 2

if __name__=='__main__':sys.exit(main())
