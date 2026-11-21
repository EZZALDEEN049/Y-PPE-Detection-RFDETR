#!/usr/bin/env python3
"""SEER-PPE V13 direct original Train↔Valid overlap characterization.
No Test source IDs, no model inference, no automatic source-family human verdict.
Images remain in memory/private runner and never enter evidence report or repository.
"""
import argparse,hashlib,io,json,os,sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor,as_completed
sys.path.insert(0,str(Path(__file__).parent))
from source_original_acquire_pilot import download
from verify_valid_original_to_clean17_pixels_v13 import analyze,selftest as image_selftest

def need(ok,msg):
 if not ok:raise ValueError('SOURCE_FAMILY_V13_FAIL_CLOSED:'+msg)
def prepare(q,manifest,fp):
 need(len(q['original_near_hash_pairs'])==46,'ORIGINAL_46_PAIRS_CHANGED')
 need(manifest['image_count']==2093 and manifest['project']=='softyyemen/altayyar-0oflt-lafos-qqauz','WRONG_FROZEN_MANIFEST')
 frozen={x['image_id']:x for x in manifest['images']}
 fingerprints={x['source_id']:x for x in fp['source_fingerprints']}
 need(len(frozen)==len(fingerprints)==2093,'ORIGINAL_SOURCE_HASH_COVERAGE_CHANGED')
 need(fp.get('test_sources_queried')==0 and fp.get('image_bytes_uploaded') is False,'ORIGINAL_TEST_OR_UPLOAD_SCOPE_BAD')
 edges=[]
 for p in q['original_near_hash_pairs']:
  edges.append({'valid_id':p['valid_id'],'train_id':p['train_id'],
   'valid_filename':p['valid_filename'],'train_filename':p['train_filename'],
   'evidence_origin':'V06_ORIGINAL_DHASH_LE8','legacy_dhash_hamming':p['dhash_hamming']})
 school_valid=['0De0PEUDyeg9v1J3T6zr','NZu6Faj6evgINF1qFE0V']
 school_train=['KrfW3xD7Vvxy6r6wISkv','H1KOFc0NQZnWRHJNcHPc']
 for v in school_valid:
  for tr in school_train:
   edges.append({'valid_id':v,'train_id':tr,'valid_filename':frozen[v]['filename'],
    'train_filename':frozen[tr]['filename'],'evidence_origin':'PREVIOUSLY_DOCUMENTED_SHARED_NAMED_SITE_22_MAY_SCHOOL',
    'legacy_dhash_hamming':None})
 keys=set()
 for e in edges:
  v,tr=e['valid_id'],e['train_id']
  need((v,tr) not in keys,'DUPLICATE_PAIR')
  keys.add((v,tr))
  need(frozen.get(v,{}).get('split')=='valid' and frozen.get(tr,{}).get('split')=='train','TRAIN_VALID_ONLY')
  need(e['valid_filename']==frozen[v]['filename'] and e['train_filename']==frozen[tr]['filename'],'FILENAME_MISMATCH')
  need(fingerprints[v]['split']=='valid' and fingerprints[tr]['split']=='train','FINGERPRINT_SPLIT_MISMATCH')
 need(len(edges)==50,'EXPECTED_50_EDGES')
 return edges,fingerprints

def main(args):
 q=json.loads(args.queue.read_text())
 m=json.loads(args.manifest.read_text())
 f=json.loads(args.fingerprints.read_text())
 edges,fps=prepare(q,m,f)
 require=set(e['valid_id'] for e in edges)|set(e['train_id'] for e in edges)
 need(os.environ.get('ROBOFLOW_API_KEY'),'MISSING_SECRET')
 from roboflow import Roboflow
 p=Roboflow(api_key=os.environ['ROBOFLOW_API_KEY']).workspace('softyyemen').project('altayyar-0oflt-lafos-qqauz')
 def fetch(sid):
  data=download(p,sid)
  need(hashlib.sha256(data).hexdigest()==fps[sid]['bytes_sha256'],'ORIGINAL_SHA_MISMATCH')
  return sid,data
 original={}
 errors=[]
 with ThreadPoolExecutor(max_workers=4) as pool:
  jobs={pool.submit(fetch,sid):sid for sid in sorted(require)}
  for fut in as_completed(jobs):
   try:
    sid,raw=fut.result()
    original[sid]=raw
   except Exception:errors.append({'source_id':jobs[fut],'safe_reason':'ORIGINAL_FETCH_OR_SHA_FAILED'})
 pair_rows=[]
 for e in edges:
  valid=e['valid_id'];train=e['train_id']
  if valid not in original or train not in original:
   pair_rows.append({**e,'error':'SOURCE_BYTES_NOT_VERIFIED'})
   continue
  x=analyze(original[valid],io.BytesIO(original[train]))
  same=hashlib.sha256(original[valid]).digest()==hashlib.sha256(original[train]).digest()
  likely=x['gray_ssim']>=.9 and x['rgb_mean_absolute_error']<=.05
  pair_rows.append({**e,'raw_bytes_equal':same,'source_hashes_both_verified':True,
   **x,'automated_same_frame_candidate':bool(likely),
   'source_independence_established':False,'human_family_verdict_signed':False,
   'scientific_scoring_eligible':False})
 report={'schema_version':'seer-ppe/direct-original-cross-split-media-candidates/v0.13',
  'date':'2026-11-21','target_source_ids':len(require),
  'originals_sha_verified':len(original),
  'original_fetch_or_hash_errors':len(errors),
  'previous_dhash_close_edges':46,
  'additional_previously_named_site_edges':4,
  'cross_split_pairs_compared':len(pair_rows)-sum('error' in x for x in pair_rows),
  'automated_same_frame_candidates':sum(x.get('automated_same_frame_candidate',False) for x in pair_rows),
  'nonhigh_pixel_pairs_remain_independence_unresolved':sum(not x.get('automated_same_frame_candidate') and 'error' not in x for x in pair_rows),
  'raw_byte_identical_cross_split_pairs':sum(x.get('raw_bytes_equal',False) for x in pair_rows),
  'known_named_school_22may_site_pairs':4,
  'human_source_family_verdicts_added':0,
  'photographic_source_independence_verified':False,
  'test_image_bytes_opened':0,'test_inferences':0,'original_model_modified':False,
  'roboflow_images_or_annotations_modified':False,'image_binary_uploaded':False,
  'scoring_ready':False,
  'source_errors':errors,'pairs':pair_rows}
 args.report.parent.mkdir(parents=True,exist_ok=True)
 args.report.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items() if k not in ('source_errors','pairs')},indent=2))
 print('SEER_V13_DIRECT_TRAIN_VALID_EVIDENCE_NOT_HUMAN_SOURCE_FAMILY_SIGNOFF')
 return 0 if not errors and report['cross_split_pairs_compared']==50 else 3

if __name__=='__main__':
 a=argparse.ArgumentParser()
 a.add_argument('--self-test',action='store_true')
 for k in ('queue','manifest','fingerprints','report'):a.add_argument('--'+k,type=Path)
 args=a.parse_args()
 try:
  if args.self_test:image_selftest();print('SEER_V13_CROSS_SPLIT_SCENE_COMPARISON_SYNTHETIC_PASS');sys.exit(0)
  need(all(getattr(args,k) is not None for k in ('queue','manifest','fingerprints','report')),'MISSING_ARGUMENT')
  sys.exit(main(args))
 except Exception as e:
  print(str(e) if isinstance(e,ValueError) and str(e).startswith('SOURCE_FAMILY_V13_FAIL_CLOSED') else 'SOURCE_FAMILY_V13_SAFE_ERROR',file=sys.stderr)
  sys.exit(2)
