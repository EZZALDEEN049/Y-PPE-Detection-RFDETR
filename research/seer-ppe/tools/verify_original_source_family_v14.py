#!/usr/bin/env python3
"""SEER-PPE V14: original Train-Valid 99-source evidence coverage.
For original Valid review queue only: union of all existing V13 50
cross-split source-pairs plus Top-3 Train candidate edges (230 new = 280).
No protected Test media, training, model predictions, or human signoffs.
"""
from __future__ import annotations
import argparse,hashlib,io,json,os,sys
from concurrent.futures import ThreadPoolExecutor,as_completed
from pathlib import Path
from collections import Counter
sys.path.insert(0,str(Path(__file__).parent))
from source_original_acquire_pilot import download
from verify_valid_original_to_clean17_pixels_v13 import analyze,selftest as image_selftest

def gate(x,m):
 if not x:raise ValueError("V14_SOURCE_SCOPE_GATE_BLOCKED:"+m)

def scope(q,prev,manifest,fps,clean):
 gate(q['queue_valid_total']==99 and len(q['review_queue'])==99,"MISSING_REVIEW_QUEUE")
 gate(prev['cross_split_pairs_compared']==50 and len(prev['pairs'])==50,"OLD_50_PAIR_EVIDENCE_CHANGED")
 gate(manifest['image_count']==2093 and manifest['project']=='softyyemen/altayyar-0oflt-lafos-qqauz',"SOURCE_MANIFEST_INVALID")
 gate(len(fps['source_fingerprints'])==2093 and fps.get('test_sources_queried')==0,"SOURCE_HASH_SCOPE_INVALID")
 f=dict((x['source_id'],x) for x in fps['source_fingerprints'])
 m=dict((x['image_id'],x) for x in manifest['images'])
 gate(len(f)==len(m)==2093,"DUPLICATE_SOURCE_IDS")
 retained={x['original_source_id'] for x in clean['valid_rows'] if x['clean17_export_candidate'] is not None}
 gate(len(retained)==459,"FROZEN_CLEAN17_COHORT_CHANGED")
 byvalid={x['valid_source_id']:x for x in q['review_queue']}
 gate(len(byvalid)==99,"REPEATED_VALID_REVIEW_IDS")
 edges={}
 for x in prev['pairs']:
  k=(x['valid_id'],x['train_id'])
  gate(k not in edges,"DUPLICATE_PRIOR_PAIR")
  edges[k]={'valid_id':k[0],'train_id':k[1],
    'original_valid_filename':x['valid_filename'],
    'original_train_filename':x['train_filename'],
    'candidate_bases':['V13_PREVIOUSLY_DIRECT_VERIFIED_PAIR'],
    'previous_v13_ssim':x['gray_ssim'],
    'previous_v13_same_frame_candidate':x['automated_same_frame_candidate']}
 for qrow in q['review_queue']:
  for tr in qrow.get('top_three_train_candidates') or []:
   k=(qrow['valid_source_id'],tr['train_id'])
   if k in edges:
    edges[k]['candidate_bases'].append('V06_TOP_THREE_SIMILARITY_NEIGHBOR')
    edges[k]['original_embedding_cosine']=tr['cosine_similarity']
   else:
    edges[k]={'valid_id':k[0],'train_id':k[1],
      'original_valid_filename':qrow['valid_filename'],
      'original_train_filename':tr['train_filename'],
      'candidate_bases':['V06_TOP_THREE_SIMILARITY_NEIGHBOR'],
      'original_embedding_cosine':tr['cosine_similarity'],
      'previous_v13_ssim':None,
      'previous_v13_same_frame_candidate':None}
 gate(len(edges)==280,"UNEXPECTED_CROSS_SPLIT_EDGES_NOT_280")
 gate(sum(x['previous_v13_ssim'] is None for x in edges.values())==230,"NEW_EDGE_COUNT_NOT_230")
 unique_valid={x[0] for x in edges}
 unique_train={x[1] for x in edges}
 gate(len(unique_valid)==99 and len(unique_train)==205,"UNIQUE_SOURCE_SCOPE_CHANGED")
 gate(all(x in unique_valid for x in byvalid),"INCOMPLETE_REVIEW_QUEUE_COVERAGE")
 gate(len(unique_valid&retained)==92 and len(unique_valid-retained)==7,"CLEAN17_SOURCE_MEMBERSHIP_DRIFT")
 for (v,t),e in edges.items():
  gate(m[v]['split']=='valid' and f[v]['split']=='valid',"NON_VALID_SOURCE_REJECTED")
  gate(m[t]['split']=='train' and f[t]['split']=='train',"NON_TRAIN_SOURCE_REJECTED")
  gate(f[v]['filename']==m[v]['filename']==e['original_valid_filename'],"VALID_NAME_CHANGED")
  gate(f[t]['filename']==m[t]['filename']==e['original_train_filename'],"TRAIN_NAME_CHANGED")
  e['clean17_valid_candidate_retained']=v in retained
  e['prior_specific_valid_hold']=bool(byvalid[v]['prior_hold'])
  e['source_family_signed_by_human']=False
  e['scoring_eligible']=False
 return edges,f,byvalid,retained

def run(args):
 q=json.loads(args.review_queue.read_text())
 prev=json.loads(args.prior_direct_pairs.read_text())
 manifest=json.loads(args.original_index.read_text())
 fp=json.loads(args.original_fingerprints.read_text())
 cw=json.loads(args.clean17_candidate_map.read_text())
 edges,fingerprints,review,retained=scope(q,prev,manifest,fp,cw)
 ids={v for v,t in edges}|{t for v,t in edges}
 gate(os.environ.get('ROBOFLOW_API_KEY'),"MISSING_ACCESS_KEY")
 from roboflow import Roboflow
 project=Roboflow(api_key=os.environ['ROBOFLOW_API_KEY']).workspace('softyyemen').project('altayyar-0oflt-lafos-qqauz')
 images={};failures=[]
 def retrieve(sid):
  raw=download(project,sid)
  gate(hashlib.sha256(raw).hexdigest()==fingerprints[sid]['bytes_sha256'],"ORIGINAL_SOURCE_SHA_CHANGED")
  return sid,raw
 with ThreadPoolExecutor(max_workers=6) as ex:
  fut={ex.submit(retrieve,sid):sid for sid in sorted(ids)}
  for future in as_completed(fut):
   try:
    sid,raw=future.result()
    images[sid]=raw
   except Exception:
    failures.append({'source_id':fut[future],'error':'ORIGINAL_FETCH_OR_SHA_FAILED'})
 records=[]
 for key,e in sorted(edges.items()):
  v,t=key
  if v not in images or t not in images:
   records.append({**e,'error':'SOURCE_NOT_REACQUIRED_VERIFIED'})
   continue
  metric=analyze(images[v],io.BytesIO(images[t]))
  high=metric['gray_ssim']>=0.90 and metric['rgb_mean_absolute_error']<=0.05
  same_bytes=hashlib.sha256(images[v]).digest()==hashlib.sha256(images[t]).digest()
  record={**e,'original_source_bytes_sha_verified':True,
    'technical_high_same_frame_candidate':bool(high),
    'raw_source_bytes_identical':same_bytes,
    'source_acquisition_independence_certified':False,
    'human_source_family_verdict':None,
    **metric}
  if e['previous_v13_ssim'] is not None:
   gate(abs(e['previous_v13_ssim']-metric['gray_ssim'])<=0.0002,"PRIOR_V13_SCORE_REGRESSION")
   gate(e['previous_v13_same_frame_candidate']==high,"V13_OVERLAP_FLAG_CHANGED")
  records.append(record)
 gate(len(records)==280,"PAIR_OUTPUT_MISSING")
 source_evidence={}
 for sid,qrow in sorted(review.items()):
  neighbors=[x for x in records if x['valid_id']==sid]
  good=[x for x in neighbors if 'error' not in x]
  ranked=sorted(good,key=lambda x:(-x['gray_ssim'],x['rgb_mean_absolute_error']))
  highlist=[x for x in ranked if x['technical_high_same_frame_candidate']]
  source_evidence[sid]={
    'valid_id':sid,'valid_filename':qrow['valid_filename'],
    'retained_in_clean17':sid in retained,
    'prior_existing_research_hold':qrow['prior_hold'],
    'technical_high_same_frame_pairs':len(highlist),
    'direct_cross_split_pairs_examined':len(good),
    'strongest_train_source_id':ranked[0]['train_id'] if ranked else None,
    'strongest_train_filename':ranked[0]['original_train_filename'] if ranked else None,
    'strongest_train_ssim':ranked[0]['gray_ssim'] if ranked else None,
    'strongest_train_rgb_mae':ranked[0]['rgb_mean_absolute_error'] if ranked else None,
    'technical_disposition':'HIGH_OVERLAP_RESEARCH_QUARANTINE_CANDIDATE' if highlist else
      'CANDIDATES_INSPECTED_SITE_FAMILY_UNRESOLVED',
    'human_family_signoff':None,'independent_source_scoring_authorized':False
  }
 valid_rows=list(source_evidence.values())
 high_source=[x for x in valid_rows if x['technical_high_same_frame_pairs']>0]
 score_count=Counter({'high_pairs':sum(x.get('technical_high_same_frame_candidate',False) for x in records),
   'high_sources':len(high_source)})
 out={
  'schema_version':'seer-ppe/99-source-original-train-valid-direct-comparison/v0.14',
  'date':'2026-11-21',
  'original_review_valid_sources':99,
  'original_valid_sources_with_direct_cross_split_pairs':len(source_evidence),
  'source_ids_original_bytes_fetched':len(ids),
  'source_ids_original_bytes_sha_verified':len(images),
  'source_fetch_failures':len(failures),
  'train_valid_direct_pairs_total':280,
  'prior_direct_pair_regressions_checked':50,
  'new_direct_pair_measurements':230,
  'original_valid_retained_clean17_under_review':92,
  'original_valid_historically_excluded_under_review':7,
  'high_same_frame_candidate_pairs':score_count['high_pairs'],
  'distinct_valid_sources_with_high_same_frame_candidate':score_count['high_sources'],
  'retained_clean17_valid_sources_with_high_same_frame_candidate':sum(x['retained_in_clean17'] for x in high_source),
  'retained_clean17_high_overlap_not_previously_held':sum(x['retained_in_clean17'] and not x['prior_existing_research_hold'] for x in high_source),
  'high_overlap_already_historically_excluded':sum(not x['retained_in_clean17'] for x in high_source),
  'raw_byte_identical_cross_split_pairs':sum(x.get('raw_source_bytes_identical',False) for x in records),
  'original_source_hold_count_unchanged':5,
  'new_formal_holds_added':0,'signed_independence_decisions_added':0,
  'technical_unflagged_sources_are_not_proven_independent':True,
  'known_shared_school_site_independence_remains_restricted':True,
  'scope':'ORIGINAL_TRAIN_VALID_ONLY','test_source_ids_accessed':0,'test_images_decoded':0,
  'model_inference':False,'original_model_retrained':False,
  'dataset_splits_annotations_modified':False,'roboflow_eval_case_modified':False,
  'raw_image_bytes_uploaded':False,'private_image_urls_saved':False,
  'scientific_scoring_ready':False,
  'safe_fetch_failures':sorted(failures,key=lambda x:x['source_id']),
  'source_rows':valid_rows,'pair_rows':records
 }
 args.report.parent.mkdir(parents=True,exist_ok=True)
 args.report.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(json.dumps({k:v for k,v in out.items() if k not in ('safe_fetch_failures','source_rows','pair_rows')},indent=2))
 print('SEER_V14_ORIGINAL_99_VALID_SOURCES_280_PAIR_DIAGNOSTIC_NOT_SCIENTIFIC_SCORING')
 return 0 if len(images)==len(ids) and len(failures)==0 and len([r for r in records if 'error' not in r])==280 else 3

def selftest():
 image_selftest()
 print('SEER_V14_SOURCE_REVIEW_COMPARISON_SYNTHETIC_NO_TEST_PASS')

if __name__=='__main__':
 p=argparse.ArgumentParser()
 p.add_argument('--self-test',action='store_true')
 for n in ('review-queue','prior-direct-pairs','original-index',
  'original-fingerprints','clean17-candidate-map','report'):
  p.add_argument('--'+n,type=Path)
 args=p.parse_args()
 try:
  if args.self_test:selftest();sys.exit(0)
  gate(all(getattr(args,k) is not None for k in
   ('review_queue','prior_direct_pairs','original_index','original_fingerprints',
    'clean17_candidate_map','report')),"MISSING_REQUIRED_ARGUMENT")
  sys.exit(run(args))
 except Exception as e:
  print(str(e) if isinstance(e,ValueError) and str(e).startswith('V14_SOURCE_SCOPE_GATE_BLOCKED') else 'SEER_V14_SAFE_READ_ONLY_FAILURE',file=sys.stderr)
  sys.exit(2)
