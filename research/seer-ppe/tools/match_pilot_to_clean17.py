#!/usr/bin/env python3
"""Read-only name-and-label-count candidate alignment; no identity assertion."""
from __future__ import annotations
import argparse,csv,json,sys
from collections import defaultdict,Counter
from pathlib import Path
from freeze_clean17 import normalized_name

def main():
 p=argparse.ArgumentParser();p.add_argument('--sample',required=True);p.add_argument('--clean-manifest',required=True);p.add_argument('--counts-json',required=True);p.add_argument('--out',required=True);a=p.parse_args()
 sample=list(csv.DictReader(open(a.sample,encoding='utf-8-sig',newline='')))
 files=list(csv.DictReader(open(a.clean_manifest,encoding='utf-8',newline='')))
 counts=json.load(open(a.counts_json,encoding='utf-8'))
 index=defaultdict(list)
 for x in files:index[(x['split'],normalized_name(x['file']))].append(x)
 res=[]
 for x in sample:
  allname=index[(x['split'],normalized_name(x['filename']))]
  count=counts.get(x['image_id'])
  count_aligned=[z for z in allname if count is not None and int(z['labels'])==int(count)]
  if len(count_aligned)==1:chosen=count_aligned[0];status='UNIQUE_NAME_AND_COUNT_CANDIDATE'
  elif len(count_aligned)>1:chosen=None;status='AMBIGUOUS_NAME_AND_COUNT'
  elif len(allname)==1:chosen=allname[0];status='NAME_ONLY_COUNT_CONFLICT'
  elif not allname:chosen=None;status='UNMATCHED'
  else:chosen=None;status='AMBIGUOUS_NAME'
  res.append({'image_id':x['image_id'],'split':x['split'],'original_name':x['filename'],'original_boxes':count if count is not None else '', 'name_matches':len(allname),'name_count_matches':len(count_aligned),'matched_export_name':chosen['file'] if chosen else '', 'matched_sha256':chosen['source_file_sha256'] if chosen else '', 'image_alignment_status':status,'pixel_identity_verification':'NOT_PERFORMED','acquisition_group_verified':'NO','rights_clearance':'UNKNOWN','human_A_status':'NOT_STARTED','human_B_status':'NOT_STARTED'})
 out=Path(a.out);out.parent.mkdir(parents=True,exist_ok=True)
 with out.open('w',newline='',encoding='utf-8-sig') as f:
  w=csv.DictWriter(f,fieldnames=list(res[0]));w.writeheader();w.writerows(res)
 print(json.dumps({'images':len(res),'statuses':dict(Counter(x['image_alignment_status'] for x in res)),'output':str(out)},indent=2))
if __name__=='__main__':main()
