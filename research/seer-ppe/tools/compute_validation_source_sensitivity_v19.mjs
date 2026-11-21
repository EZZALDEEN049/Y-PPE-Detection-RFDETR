#!/usr/bin/env node
/**
 * V19: deterministic numerical source-overlap sensitivity screen.
 * NEVER edits original splits, infers independence or requests image reinspection.
 * Reads pre-existing 459 Valid technical crosswalk + 280 direct original
 * Train↔Valid pair comparisons. All retained images remain uncertified.
 */
import assert from 'node:assert/strict';
import {readFileSync,writeFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import {resolve} from 'node:path';
import {fileURLToPath} from 'node:url';
const ROOT=resolve(fileURLToPath(new URL('..',import.meta.url)));
const files={
 crosswalk:'VALIDATION_TECHNICAL_QUARANTINE_V14.json',
 directPairs:'ORIGINAL_99_VALID_SOURCE_FAMILY_PAIRS_2026-11-21_V14.json',
 readiness:'VALIDATION_459_SIGNED_SOURCE_COHORT_READINESS_V15.json'
};
const read=n=>JSON.parse(readFileSync(resolve(ROOT,n),'utf8'));
const sha=n=>createHash('sha256').update(readFileSync(resolve(ROOT,n))).digest('hex');
const need=(ok,why)=>{if(!ok)throw Error('SEER_V19_SOURCE_SENSITIVITY_BLOCKED:'+why)};
const categories=[
 'RETAIN_PREEXISTING_RESEARCH_HOLD',
 'TECHNICAL_OVERLAP_QUARANTINE_PENDING_REVIEW',
 'SOURCE_FAMILY_REVIEW_PENDING',
 'NO_SCREEN_FLAG_INDEPENDENCE_UNCERTIFIED'
];
const STATUS={
 RETAIN_PREEXISTING_RESEARCH_HOLD:'HISTORICAL_HOLD',
 TECHNICAL_OVERLAP_QUARANTINE_PENDING_REVIEW:'HIGH_OVERLAP_TECHNICAL_QUARANTINE',
 SOURCE_FAMILY_REVIEW_PENDING:'POTENTIAL_SOURCE_FAMILY_LINK_PENDING',
 NO_SCREEN_FLAG_INDEPENDENCE_UNCERTIFIED:'UNFLAGGED_NOT_PROVEN_INDEPENDENT'
};
function run(quarantine,pairs,readiness){
 need(quarantine.schema_version==='seer-ppe/clean17-valid-research-quarantine/v0.14' &&
  quarantine.clean17_valid_files===459 && quarantine.technical_direct_clean17_matches===459 &&
  quarantine.previous_signed_research_holds===5 &&
  quarantine.additional_technical_quarantine_unsigned===6 &&
  quarantine.other_flagged_source_family_unsigned===81 &&
  quarantine.unflagged_independence_uncertified===367 &&
  quarantine.source_splits_unchanged===true &&
  quarantine.test_opened===false && quarantine.model_original_unchanged===true &&
  quarantine.scoring_ready===false,'v14 technical Valid map changed');
 need(pairs.schema_version==='seer-ppe/99-source-original-train-valid-direct-comparison/v0.14' &&
  pairs.train_valid_direct_pairs_total===280 &&
  pairs.original_review_valid_sources===99 &&
  pairs.high_same_frame_candidate_pairs===12 &&
  pairs.signed_independence_decisions_added===0 &&
  pairs.test_source_ids_accessed===0 && pairs.model_inference===false &&
  pairs.scientific_scoring_ready===false,
  'v14 original source pair status changed');
 need(readiness.schema_version==='seer-ppe/validation-evidence-qualification-audit/v0.15'&&
  readiness.original_valid_count===468&&readiness.clean17_valid_count===459&&
  readiness.per_image_source_family_human_decisions_signed===0&&
  readiness.human_independence_attestations===0&&
  readiness.scoring_ready===false&&readiness.image_rows.length===459,
  'readiness claims unexpected independent validation');
 const cross=new Map();
 for(const q of quarantine.rows){
  need(q.original_to_clean17_direct_media_sha_verified===true &&
   q.high_source_export_content_consistency===true &&
   q.retained_in_clean17_valid===true &&
   categories.includes(q.eligibility_disposition),
   'image alignment or V14 technical disposition changed');
  need(typeof q.original_valid_source_id==='string'&&!cross.has(q.original_valid_source_id),
   'duplicate or invalid Valid source ID');
  cross.set(q.original_valid_source_id,q);
 }
 need(cross.size===459,'corrected 459 image mapping changed');
 const signed=new Map(readiness.image_rows.map(x=>[x.source_id,x]));
 need(signed.size===459,'readiness source ID duplicate');
 for(const [id,q] of cross){
  const s=signed.get(id);
  need(s&&s.clean17_valid_export_filename===q.clean17_valid_filename &&
   s.eligible_for_scientific_scoring===false &&
   s.signed_source_family_verdict===null &&
   s.source_reviewer_signoff_missing===true,
   'unsigned source appeared independent or original mapping mismatch');
 }
 const count=Object.fromEntries(categories.map(x=>[x,0]));
 for(const q of cross.values())count[q.eligibility_disposition]++;
 need(count[categories[0]]===5&&count[categories[1]]===6&&
  count[categories[2]]===81&&count[categories[3]]===367,
  'source risk bucket count drift');
 const directPairIDs=new Set(),high=[];
 const perValid=new Map();
 for(const p of pairs.pair_rows){
  need(typeof p.valid_id==='string'&&typeof p.train_id==='string' &&
   p.valid_id!==p.train_id && p.original_source_bytes_sha_verified===true &&
   p.raw_source_bytes_identical===false &&
   p.source_acquisition_independence_certified===false &&
   p.scoring_eligible===false,
   'old pair evidence corrupted or independence improperly asserted');
  const k=p.valid_id+'|'+p.train_id;
  need(!directPairIDs.has(k),'duplicate cross-split pair');
  directPairIDs.add(k);
  if(!perValid.has(p.valid_id))perValid.set(p.valid_id,[]);
  perValid.get(p.valid_id).push(p);
  if(p.technical_high_same_frame_candidate===true)high.push(p);
 }
 need(directPairIDs.size===280&&high.length===12,'direct pair/high-sim count drift');
 // Union-find on HYPOTHESIS edges only; no independent-acquisition inference.
 const parent=new Map(),size=new Map();
 function find(x){
  if(!parent.has(x)){parent.set(x,x);size.set(x,1);}
  if(parent.get(x)!==x)parent.set(x,find(parent.get(x)));
  return parent.get(x);
 }
 function union(a,b){
  a=find(a);b=find(b);if(a===b)return;
  if(size.get(a)<size.get(b)){const t=a;a=b;b=t;}
  parent.set(b,a);size.set(a,size.get(a)+size.get(b));
 }
 for(const p of high)union('valid:'+p.valid_id,'train:'+p.train_id);
 const components=new Map();
 for(const id of parent.keys()){
  const root=find(id);
  if(!components.has(root))components.set(root,[]);
  components.get(root).push(id);
 }
 const highSummary=[...components.values()].map(nodes=>({
  valid_source_ids:nodes.filter(x=>x.startsWith('valid:')).map(x=>x.slice(6)).sort(),
  train_source_ids:nodes.filter(x=>x.startsWith('train:')).map(x=>x.slice(6)).sort(),
  status:'HIGH_SIMILARITY_CONNECTED_COMPONENT_HYPOTHESIS_ONLY'
 })).sort((a,b)=>a.valid_source_ids[0].localeCompare(b.valid_source_ids[0]));
 const highValid=new Set(high.map(x=>x.valid_id));
 need(highValid.size===9&&[...highValid].filter(x=>cross.has(x)).length===8,
   'v14 high-overlap source counts drift');
 const outputRows=[...cross.values()].map(q=>{
  const source=q.original_valid_source_id,linked=(perValid.get(source)??[]);
  return {
   original_valid_source_id:source,
   clean17_valid_export_filename:q.clean17_valid_filename,
   risk_bucket:STATUS[q.eligibility_disposition],
   direct_train_pair_candidates_checked:linked.length,
   technical_high_same_frame_pair_candidates:linked.filter(p=>p.technical_high_same_frame_candidate===true).length,
   high_similarity_component_id:highValid.has(source)?highSummary.findIndex(g=>g.valid_source_ids.includes(source))+1:null,
   retained_in_full_descriptive_cohort:true,
   retained_in_conservative_448_sensitivity:![categories[0],categories[1]].includes(q.eligibility_disposition),
   retained_in_unflagged_367_sensitivity:q.eligibility_disposition===categories[3],
   source_acquisition_independence_proven:false,
   independent_scientific_scoring_authorized:false
  };
 }).sort((a,b)=>a.original_valid_source_id.localeCompare(b.original_valid_source_id));
 const ids=criterion=>outputRows.filter(criterion).map(x=>x.original_valid_source_id);
 const full=ids(x=>x.retained_in_full_descriptive_cohort);
 const restricted=ids(x=>x.retained_in_conservative_448_sensitivity);
 const unflagged=ids(x=>x.retained_in_unflagged_367_sensitivity);
 need(full.length===459&&restricted.length===448&&unflagged.length===367,
  'sensitivity scenario cohorts not exhaustive or inconsistent');
 need(highSummary.reduce((s,x)=>s+x.valid_source_ids.length,0)===highValid.size,
  'technical high similarity component assignment inconsistent');
 return {
  schema_version:'seer-ppe/validation-source-computational-sensitivity-screen/v0.19',
  date:'2026-11-21',
  scope:'METADATA_ONLY_EXISTING_TRAIN_VALID_DIRECT_PAIRS_NO_IMAGE_REINSPECTION',
  source_file_sha256:Object.fromEntries(Object.entries(files).map(([k,v])=>[k,sha(v)])),
  input_original_valid_count:468,input_clean17_valid_count:459,
  source_family_groups_are_hypotheses_not_confirmed_acquisition_ids:true,
  no_new_human_or_second_review_required:true,
  original_model_retrained:false,
  source_splits_or_labels_modified:false,
  valid_predictions_scored:false,test_sources_or_images_accessed:false,
  scoring_ready:false,independent_valid_scientific_cohort_size:0,
  risk_bucket_counts:{
   historical_holds:count[categories[0]],
   high_overlap_technical_quarantines:count[categories[1]],
   other_flagged_possible_source_families:count[categories[2]],
   unflagged_but_not_independently_certified:count[categories[3]]
  },
  original_direct_pairs_examined:280,
  high_similarity_pair_edges:high.length,
  high_similarity_distinct_valid_ids_in_99_review:highValid.size,
  high_similarity_distinct_valid_ids_retained_in_clean17:[...highValid].filter(x=>cross.has(x)).length,
  high_similarity_connected_components:highSummary,
  descriptive_sensitivity_scenarios:{
   ALL_MATCHED_VALID_459:{source_ids:full,count:full.length,scientifically_independent:false},
   EXCLUDE_HISTORICAL_HOLDS_AND_TECHNICAL_QUARANTINES_448:{source_ids:restricted,count:restricted.length,scientifically_independent:false},
   UNFLAGGED_ONLY_BUT_UNCERTIFIED_367:{source_ids:unflagged,count:unflagged.length,scientifically_independent:false}
  },
  per_image_technical_flags:outputRows
 };
}
function tests(){
 const q=read(files.crosswalk),p=read(files.directPairs),r=read(files.readiness);
 const x=run(q,p,r);
 assert.equal(x.descriptive_sensitivity_scenarios.ALL_MATCHED_VALID_459.count,459);
 assert.equal(x.descriptive_sensitivity_scenarios.EXCLUDE_HISTORICAL_HOLDS_AND_TECHNICAL_QUARANTINES_448.count,448);
 assert.equal(x.descriptive_sensitivity_scenarios.UNFLAGGED_ONLY_BUT_UNCERTIFIED_367.count,367);
 assert.equal(x.high_similarity_pair_edges,12);
 assert.equal(x.independent_valid_scientific_cohort_size,0);
 const q2=structuredClone(q);q2.rows[0].eligibility_disposition='MADE_UP_INDEPENDENT';
 assert.throws(()=>run(q2,p,r));
 const p2=structuredClone(p);p2.pair_rows[0].source_acquisition_independence_certified=true;
 assert.throws(()=>run(q,p2,r));
 const r2=structuredClone(r);r2.per_image_source_family_human_decisions_signed=1;
 assert.throws(()=>run(q,p,r2));
 const q3=structuredClone(q);q3.test_opened=true;
 assert.throws(()=>run(q3,p,r));
 console.log('SEER_V19_AUTOMATED_SOURCE_SENSITIVITY_459_448_367_AND_FAIL_CLOSED_TESTS_PASS');
}
try{
 const mode=process.argv[2]??'--audit';
 if(mode==='--self-test')tests();
 else if(mode==='--audit'){
  const out=run(read(files.crosswalk),read(files.directPairs),read(files.readiness));
  if(process.argv[3])writeFileSync(process.argv[3],JSON.stringify(out,null,2)+'\n');
  console.log(JSON.stringify({buckets:out.risk_bucket_counts,
   high_similarity_pair_edges:out.high_similarity_pair_edges,
   components:out.high_similarity_connected_components.length,
   descriptive_cohorts:Object.fromEntries(Object.entries(out.descriptive_sensitivity_scenarios).map(([k,v])=>[k,v.count])),
   scientific_scoring_ready:out.scoring_ready},null,2));
  console.log('SEER_V19_SOURCE_METADATA_ONLY_STRATIFICATION_NOT_INDEPENDENT_PASS');
 }else throw Error('Usage: --self-test | --audit [file]');
}catch(e){console.error(String(e));process.exitCode=2;}
