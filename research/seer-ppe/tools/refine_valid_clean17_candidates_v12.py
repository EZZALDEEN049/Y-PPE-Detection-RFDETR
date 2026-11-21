#!/usr/bin/env python3
"""V12 ranked VALID-only metadata candidates, no photo proof, no Test bytes."""
from __future__ import annotations
import argparse,csv,io,json,re
from collections import Counter,defaultdict
from pathlib import Path

HOLD_IDS={"0De0PEUDyeg9v1J3T6zr","jeB2NmucImurFBeFkyIz",
          "NZu6Faj6evgINF1qFE0V","qBtfzUgi6Mpg3A5TE0ln","yeEvdkqXtNgsj7PZFDvI"}

def norm(s):
 s=Path(s).name.lower()
 s=re.sub(r'_([a-z0-9]+)\.rf\.[a-f0-9]{32}\.[a-z0-9]+$',r'.\1',s)
 return re.sub('[^a-z0-9]+','',s).replace('jpeg','jpg')
def hd(a,b):
 assert re.fullmatch('[0-9a-f]{16}',a) and re.fullmatch('[0-9a-f]{16}',b)
 return (int(a,16)^int(b,16)).bit_count()
def fail(m):raise ValueError("V12_RANKED_VALID_GATE_BLOCKED:"+m)

def derive(source,clean,prior):
 if source.get('test_sources_queried')!=0:fail('TEST_SOURCE_FLAG')
 if prior.get('not_read_test_image_bytes') is not True:fail('UNSAFE_PRIOR_RECONCILIATION')
 if len(source.get('source_fingerprints',[]))!=2093:fail('WRONG_FINGERPRINT_COUNT')
 if prior.get('source_original_count')!=2093 or prior.get('clean17_train_valid_count')!=2054:fail('WRONG_PRIOR_SCOPE')
 valid={x['source_id']:x for x in source['source_fingerprints'] if x['split']=='valid'}
 old={x['source_id']:x for x in prior['rows'] if x['split']=='valid'}
 if len(valid)!=len(old)!=468:fail('WRONG_VALID_COUNT')
 if len(valid)!=468 or len(old)!=468:fail('WRONG_VALID_COVERAGE')
 clean_valid=[c for c in clean if c['split']=='valid']
 if len(clean_valid)!=459:fail('WRONG_CLEAN_VALID_COUNT')
 byname=defaultdict(list)
 for c in clean_valid:byname[norm(c['file'])].append(c)
 rows=[]
 for source_id,s in sorted(valid.items()):
  priorrow=old.get(source_id)
  if priorrow is None or priorrow['source_filename']!=s['filename']:
   fail('ORIGINAL_SOURCE_ID_PROVENANCE_MISMATCH')
  matches=byname[norm(s['filename'])]
  if not matches:
   if not priorrow['listed_in_historical_exclusion_manifest_by_split_and_normalized_name']:
    fail('UNEXPLAINED_ABSENT_ORIGINAL_VALID_SOURCE')
   result={'original_source_id':source_id,'original_filename':s['filename'],'split':'valid',
     'clean17_export_candidate':None,'classification':'HISTORICAL_EXCLUSION_NO_CLEAN_NAME_MATCH',
     'dhash_best':None,'dhash_second':None,'dhash_rank_margin':None,'candidate_count':0}
  else:
   rank=sorted((hd(s['dhash64'],c['dhash64']),c['file']) for c in matches)
   best,filename=rank[0]
   second=rank[1][0] if len(rank)>1 else None
   if second is not None and second<=best:fail('AMBIGUOUS_DHASH_TIE')
   result={'original_source_id':source_id,'original_filename':s['filename'],'split':'valid',
     'clean17_export_candidate':filename,
     'classification':'UNIQUE_NORMALIZED_NAME_CANDIDATE' if len(matches)==1 else 'RANKED_DHASH_CANDIDATE',
     'dhash_best':best,'dhash_second':second,'dhash_rank_margin':second-best if second is not None else None,
     'candidate_count':len(matches)}
  result.update({'preexisting_research_hold':source_id in HOLD_IDS,
    'source_to_clean17_pixel_identity_verified':False,
    'source_family_independence_signed':False,
    'confirmed_clean17_membership':False,
    'eligible_for_scientific_scoring':False})
  rows.append(result)
 ct=Counter(x['classification'] for x in rows)
 if ct!=Counter({'UNIQUE_NORMALIZED_NAME_CANDIDATE':426,'RANKED_DHASH_CANDIDATE':33,
                  'HISTORICAL_EXCLUSION_NO_CLEAN_NAME_MATCH':9}):
  fail('UNEXPECTED_VALID_NAME_RANK_COUNTS')
 candidates=[r['clean17_export_candidate'] for r in rows if r['clean17_export_candidate']]
 if len(set(candidates))!=459 or set(candidates)!={c['file'] for c in clean_valid}:
  fail('NOT_BIJECTIVE_CANDIDATES_FOR_CLEAN_VALID')
 ranked=[x for x in rows if x['classification']=='RANKED_DHASH_CANDIDATE']
 if min(x['dhash_rank_margin'] for x in ranked)<15 or max(x['dhash_best'] for x in ranked)>6:
  fail('WEAK_AMBIGUOUS_NAME_DHASH_SEPARATION')
 if sum(x['preexisting_research_hold'] for x in rows)!=5:
  fail('PREVIOUS_VALID_RESEARCH_HOLDS_NOT_PRESERVED')
 if any(x['eligible_for_scientific_scoring'] or x['confirmed_clean17_membership'] for x in rows):
  fail('INVALID_EVALUATION_PERMISSION')
 return {'schema_version':'seer-ppe/provisional-valid-to-clean17-candidate-join/v0.12.1',
   'date':'2026-11-21','basis':'EXISTING_VERIFIED_GITHUB_ACTIONS_SOURCE_AND_CLEAN17_METADATA_ARTIFACTS',
   'original_valid_sources':468,'clean17_valid_export_files':459,
   'unique_name_candidates':426,'ranked_dhash_candidates':33,
   'prior_historical_exclusions_without_clean_match':9,
   'clean_valid_export_files_covered_by_distinct_candidates':459,
   'duplicate_clean_export_assignments':0,
   'minimum_dhash_rank_margin_among_ambiguous':15,
   'maximum_best_dhash_distance_among_ambiguous':6,
   'existing_source_holds_preserved':5,
   'source_to_clean17_pixel_identity_verified_count':0,
   'independent_source_human_signoffs':0,
   'scientifically_eligible_images_created':0,
   'protected_test_images_read':0,
   'model_or_source_splits_modified':False,
   'scientific_scoring_ready':False,
   'limitations':['Filename/dHash rankings are provisional metadata evidence, not cryptographic photo identity.',
      'Original-source to Clean17 exact pixel identity remains unverified.',
      'Five source holds and individual source-family independence signoff remain separate.'],
   'valid_rows':rows}

def report_text():
 return """# SEER-PPE V12 — Verified provisional Valid-to-Clean17 candidate mapping

**21 November 2026; real metadata-only execution, not model scoring.**

The exact original-Source and Clean17 historical metadata artifacts were downloaded into a temporary GitHub Actions runner, and 468 original Valid Source IDs were compared to 459 Clean17 Valid export filenames (no Test photo bytes). The result contains **426 distinct normalized-name candidates**, **33 previously ambiguous names with an unambiguous closest dHash candidate**, and **9 historically excluded images without a Clean17 name match**. The 459 candidate assignments cover exactly 459 distinct Clean17 Valid export filenames.

For all 33 ambiguous cases, nearest-vs-second-nearest dHash margin was at least **15**, and maximum nearest dHash distance was **6**. Such metadata evidence is **not a verified source image identity or an independently signed Clean17 membership**. The original/export image bytes did not match as raw SHA, and the source/clean pixel-hash conventions and resize/encoding paths differ. The only authorized classification here is *candidate*, never *verified*.

All five previous Valid research holds remain in place; 0 per-image source-independence human signoffs were added; no Test photo, original dataset, annotation, split or RF-DETR model was touched. **Scientific scoring remains blocked**. Future exact identity confirmation requires a documented image-content or acquisition-lineage check, without rewriting the protected Test.

[JSON source-ID ledger](SEER_PPE_VALID_TO_CLEAN17_PROVISIONAL_V12.json) · [CSV overview](SEER_PPE_VALID_TO_CLEAN17_PROVISIONAL_V12.csv) · [Reproducible ranking code](tools/refine_valid_clean17_candidates_v12.py) · [V12 initial hash/name run](https://github.com/EZZALDEEN049/Y-PPE-Detection-RFDETR/actions/runs/44842423862).
"""

def main():
 p=argparse.ArgumentParser()
 for key in ['source_report','clean_manifest','prior_report','out_dir']:p.add_argument('--'+key.replace('_','-'),type=Path,required=True)
 a=p.parse_args()
 source=json.loads(a.source_report.read_text(encoding='utf8'))
 prior=json.loads(a.prior_report.read_text(encoding='utf8'))
 with a.clean_manifest.open(encoding='utf8',newline='') as f:
  clean=[c for c in csv.DictReader(f) if c['split']=='valid']
 x=derive(source,clean,prior)
 a.out_dir.mkdir(parents=True,exist_ok=True)
 j=a.out_dir/'SEER_PPE_VALID_TO_CLEAN17_PROVISIONAL_V12.json'
 j.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
 flds=['original_source_id','original_filename','clean17_export_candidate','classification',
       'dhash_best','dhash_second','dhash_rank_margin','candidate_count','preexisting_research_hold',
       'source_to_clean17_pixel_identity_verified','eligible_for_scientific_scoring']
 with (a.out_dir/'SEER_PPE_VALID_TO_CLEAN17_PROVISIONAL_V12.csv').open('w',encoding='utf8',newline='') as f:
  writer=csv.DictWriter(f,fieldnames=flds);writer.writeheader()
  for r in x['valid_rows']:writer.writerow({k:r[k] for k in flds})
 (a.out_dir/'SEER_PPE_VALID_TO_CLEAN17_PROVISIONAL_V12.md').write_text(report_text(),encoding='utf8')
 print('SEER_V12_VALID_459_ONE_TO_ONE_METADATA_CANDIDATES_WITH_NO_SCIENTIFIC_SCORING_PASS')

if __name__=='__main__':
 try:main()
 except Exception as e:
  print(str(e),file=__import__('sys').stderr);raise SystemExit(2)
