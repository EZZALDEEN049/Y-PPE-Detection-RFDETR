#!/usr/bin/env python3
"""SEER-PPE V13: SHA-pinned direct image-content corroboration, Valid only.
Only the selected original Valid Source IDs and clone Valid export images are decoded.
Media remains private in temporary CI; output is evidence metadata, not human signoff.
"""
import argparse,csv,hashlib,io,json,os,re,sys
from concurrent.futures import ThreadPoolExecutor,as_completed
from pathlib import Path
import numpy as np
import cv2
from PIL import Image,ImageOps
from skimage.metrics import structural_similarity
sys.path.insert(0,str(Path(__file__).parent))
from source_original_acquire_pilot import download

def require(cond,msg):
 if not cond:raise ValueError("V13_FAIL_CLOSED:"+msg)
def load_rgb(file):
 with Image.open(file) as f:return ImageOps.exif_transpose(f).convert("RGB").copy()
def hashfile(path):
 h=hashlib.sha256()
 with open(path,'rb') as f:
  for chunk in iter(lambda:f.read(262144),b''):h.update(chunk)
 return h.hexdigest()
def analyze(src,out):
 orig=load_rgb(io.BytesIO(src))
 exported=load_rgb(out)
 b=np.asarray(exported)
 rgb_b=cv2.cvtColor(b,cv2.COLOR_RGB2GRAY)
 trials=[]
 for method,im in [('lanczos',np.asarray(orig.resize(exported.size,Image.Resampling.LANCZOS))),
                   ('bicubic',np.asarray(orig.resize(exported.size,Image.Resampling.BICUBIC))),
                   ('bilinear',np.asarray(orig.resize(exported.size,Image.Resampling.BILINEAR))),
                   ('opencv_area',cv2.resize(np.asarray(orig),exported.size,interpolation=cv2.INTER_AREA))]:
  s=float(structural_similarity(cv2.cvtColor(im,cv2.COLOR_RGB2GRAY),rgb_b,data_range=255))
  mae=float(np.mean(cv2.absdiff(im,b))/255)
  trials.append((s,-mae,method,im))
 best=max(trials,key=lambda x:(x[0],x[1]))
 orb=cv2.ORB_create(nfeatures=850)
 a=cv2.cvtColor(best[3],cv2.COLOR_RGB2GRAY)
 kp1,d1=orb.detectAndCompute(a,None)
 kp2,d2=orb.detectAndCompute(rgb_b,None)
 good=[]
 if d1 is not None and d2 is not None and len(d1)>=8 and len(d2)>=8:
  for pair in cv2.BFMatcher(cv2.NORM_HAMMING).knnMatch(d1,d2,k=2):
   if len(pair)==2 and pair[0].distance<.75*pair[1].distance:good.append(pair[0])
 inliers=0
 if len(good)>=8:
  q=np.float32([kp1[x.queryIdx].pt for x in good]).reshape(-1,1,2)
  t=np.float32([kp2[x.trainIdx].pt for x in good]).reshape(-1,1,2)
  _,mask=cv2.findHomography(q,t,cv2.RANSAC,3)
  inliers=int(mask.sum()) if mask is not None else 0
 s,neg_mae,method,_=best
 high=(s>=.94 and -neg_mae<=.075) or (s>=.88 and -neg_mae<=.11 and inliers>=24)
 return {'gray_ssim':round(s,5),'rgb_mean_absolute_error':round(-neg_mae,5),'resize_method':method,
         'orb_good_matches':len(good),'orb_inliers':inliers,'technical_content_consistency':
         'HIGH_AUTOMATED_EVIDENCE_NOT_FINAL_PHOTO_IDENTITY' if high else 'FURTHER_REVIEW_NEEDED',
         'original_dimensions':list(orig.size),'export_dimensions':list(exported.size)}
def selftest():
 rng=np.random.default_rng(13)
 o=Image.fromarray(rng.integers(0,256,size=(190,310,3),dtype=np.uint8))
 b=io.BytesIO();o.resize((640,640),Image.Resampling.LANCZOS).save(b,format='JPEG',quality=90)
 r=analyze(io_bytes(o),io.BytesIO(b.getvalue()))
 require(r['gray_ssim']>.8,'SYNTHETIC_MATCH')
 other=Image.fromarray(rng.integers(0,256,size=(640,640,3),dtype=np.uint8))
 require(analyze(io_bytes(o),io.BytesIO(io_bytes(other)))['gray_ssim']<.4,'NEGATIVE_CONTROL')
 print('V13_SYNTHETIC_PICTURE_COMPARISON_AND_NEGATIVE_CONTROL_PASS')
def io_bytes(img):
 b=io.BytesIO();img.save(b,format='PNG');return b.getvalue()
def main(a):
 cross=json.loads(a.crosswalk.read_text())
 original=json.loads(a.original_report.read_text())
 idx=json.loads(a.original_index.read_text())
 require(cross['original_valid_sources']==468 and cross['clean17_valid_export_files']==459,'WRONG_CROSSWALK')
 require(original.get('test_sources_queried')==0,'TEST_SOURCE_USED')
 osrc={x['source_id']:x for x in original['source_fingerprints'] if x['split']=='valid'}
 need={x['image_id']:x for x in idx['images'] if x['split']=='valid'}
 require(len(osrc)==len(need)==468,'FROZEN_VALID_SOURCE_SET_CHANGED')
 with open(a.clean_manifest,newline='',encoding='utf-8') as f:
  clean={x['file']:x for x in csv.DictReader(f) if x['split']=='valid'}
 require(len(clean)==459,'FROZEN_CLEAN_VALID_COUNT_CHANGED')
 items=[r for r in cross['valid_rows'] if r['clean17_export_candidate']]
 require(len(items)==459,'CROSSWALK_HAS_MISSING_VALID')
 if a.mode=='pilot':
  held=[x for x in items if x['preexisting_research_hold']]
  ranked=[x for x in items if x['classification']=='RANKED_DHASH_CANDIDATE'][:7]
  ordinary=[x for x in items if x['classification']=='UNIQUE_NORMALIZED_NAME_CANDIDATE' and not x['preexisting_research_hold']][:4]
  items=held+ranked+ordinary
  require(len(items)==16,'PILOT_CASE_SELECTION')
 require(os.environ.get('ROBOFLOW_API_KEY'),'MISSING_API_KEY')
 from roboflow import Roboflow
 project=Roboflow(api_key=os.environ['ROBOFLOW_API_KEY']).workspace('softyyemen').project('altayyar-0oflt-lafos-qqauz')
 valid_dir=(a.clean_root/'valid'/'images').resolve()
 require(valid_dir.is_dir(),'VALID_EXPORT_FOLDER_MISSING')
 def one(row):
  sid=row['original_source_id'];filename=row['clean17_export_candidate']
  require(osrc[sid]['filename']==row['original_filename'] and need[sid]['filename']==row['original_filename'],'ORIGINAL_SOURCE_ID_CHANGED')
  require(osrc[sid]['split']=='valid','NON_VALID_SOURCE_FORBIDDEN')
  require(Path(filename).name==filename,'UNSAFE_EXPORT_FILENAME')
  path=(valid_dir/filename).resolve()
  require(path.is_relative_to(valid_dir) and path.is_file() and not path.is_symlink(),'NON_VALID_EXPORT_PATH')
  if hashfile(path)!=clean[filename]['source_file_sha256']:return {'source_id':sid,'error':'CLEAN17_EXPORT_SHA_CHANGED'}
  raw=download(project,sid)
  if hashlib.sha256(raw).hexdigest()!=osrc[sid]['bytes_sha256']:return {'source_id':sid,'error':'ORIGINAL_SOURCE_SHA_CHANGED'}
  score=analyze(raw,path)
  require(score['original_dimensions']==[need[sid]['width'],need[sid]['height']],'ORIGINAL_DIMENSIONS_CHANGED')
  return {'source_id':sid,'export_filename':filename,'previous_hold':row['preexisting_research_hold'],
    'candidate_classification':row['classification'],'original_sha_verified':True,'export_sha_verified':True,**score,
    'final_photo_identity_human_signed':False,'source_family_independence_human_signed':False,'scoring_eligible':False}
 records=[]
 with ThreadPoolExecutor(max_workers=4) as pool:
  future={pool.submit(one,r):r for r in items}
  for f in as_completed(future):
   try:records.append(f.result())
   except Exception:records.append({'source_id':future[f]['original_source_id'],'error':'READ_OR_COMPARISON_FAILED_NO_PRIVATE_URL_IN_REPORT'})
 records.sort(key=lambda x:x['source_id'])
 good=[r for r in records if 'error' not in r]
 result={'schema_version':'seer-ppe/source-clean17-valid-photo-corroboration/v0.13','mode':a.mode,
  'requested':len(items),'source_and_export_sha_verified':len(good),
  'high_content_consistency':sum(x['technical_content_consistency'].startswith('HIGH') for x in good),
  'needs_further_review':sum(x['technical_content_consistency']=='FURTHER_REVIEW_NEEDED' for x in good),
  'errors':len(records)-len(good),'previous_held_valid_sample_count':sum(x.get('previous_hold',False) for x in records),
  'data_scope':'ORIGINAL_VALID_TO_CLONE_VALID_ONLY','test_images_decoded':0,
  'test_image_inference':0,'source_family_signoffs_added':0,'person_ppe_decisions_added':0,
  'model_retrained':False,'roboflow_evals_changed':False,'images_uploaded':False,
  'source_urls_or_secrets_persisted':False,'scientific_scoring_ready':False,
  'results':records}
 a.report.parent.mkdir(parents=True,exist_ok=True)
 a.report.write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps({k:v for k,v in result.items() if k!='results'},indent=2))
 print('SEER_V13_REAL_VALID_PHOTO_CONTENT_EVIDENCE_RECORDED_NO_SCORING')
 return 0 if len(good)==len(items) else 3
if __name__=='__main__':
 p=argparse.ArgumentParser()
 p.add_argument('--self-test',action='store_true')
 for name in ('crosswalk','original-report','original-index','clean-manifest','clean-root','report'):
  p.add_argument('--'+name,type=Path)
 p.add_argument('--mode',choices=['pilot','full'],default='pilot')
 a=p.parse_args()
 try:
  if a.self_test:selftest();sys.exit(0)
  require(all(getattr(a,k) is not None for k in ('crosswalk','original_report','original_index','clean_manifest','clean_root','report')),'MISSING_CLI_INPUT')
  sys.exit(main(a))
 except Exception as e:
  msg=str(e) if isinstance(e,ValueError) and str(e).startswith('V13_FAIL_CLOSED') else 'V13_READ_ONLY_MEDIA_AUDIT_FAILED'
  print(msg,file=sys.stderr);sys.exit(2)
