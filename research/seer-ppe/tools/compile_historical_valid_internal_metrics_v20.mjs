#!/usr/bin/env node
/**
 * SEER-PPE V20: reproducible HISTORICAL Roboflow model Eval v2, Valid-only
 * per-image counter aggregation across three preselected source-risk cohorts.
 *
 * No new inference, image reading, Test access, model retraining, source labels
 * modification, independent source assertions or worker safety claims.
 * Historical Eval GT and CURRENT Source annotations do NOT match on all images.
 */
import assert from 'node:assert/strict';
import {readFileSync,writeFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import {fileURLToPath} from 'node:url';
import {resolve} from 'node:path';
const ROOT=resolve(fileURLToPath(new URL('..',import.meta.url)));
const paths={
 historic:'HISTORICAL_V2_VALID_PER_IMAGE_COUNTERS_V20.json',
 part1:'V20_VALID_SOURCE_ANNOTATION_COUNTS_PART1_PRIVATE_WORKING.json',
 part2:'V20_VALID_SOURCE_ANNOTATION_COUNTS_PART2_PRIVATE_WORKING.json',
 risk:'VALIDATION_SOURCE_OVERLAP_NUMERIC_SENSITIVITY_V19.json',
 protocol:'VALID_HISTORICAL_INTERNAL_OBJECT_EVAL_PROTOCOL_FROZEN_V20.md'
};
const read=(name)=>JSON.parse(readFileSync(resolve(ROOT,name),'utf8'));
const digest=(name)=>createHash('sha256').update(readFileSync(resolve(ROOT,name))).digest('hex');
const ck=(cond,msg)=>{if(!cond)throw Error('SEER_V20_FROZEN_VALID_INTERNAL_GATE_BLOCKED:'+msg)};
const k0='ALL_MATCHED_VALID_459';
const k1='EXCLUDE_HISTORICAL_HOLDS_AND_TECHNICAL_QUARANTINES_448';
const k2='UNFLAGGED_ONLY_BUT_UNCERTIFIED_367';
const asInt=x=>Number.isInteger(x)&&x>=0;
const six=x=>x===null?null:Number(x.toFixed(6));
function compile(e,pt1,pt2,risks){
 ck(e.schema_version==='seer-ppe/historical-original-model-valid-per-source-saved-counters/v0.20' &&
 e.eval_id==='KyzP9neuyNTN5eQpGCAY' &&
 e.original_model_id==='altayyar-0oflt-lafos-qqauz/2' &&
 e.dataset_version_number===2 &&
 e.scored_split==='valid' &&
 e.confidence_threshold===0.2 &&
 e.pages_retrieved===3 && e.historical_valid_image_rows===468 &&
 e.clean17_retained_original_source_rows===459 &&
 e.excluded_old_valid_ids_not_in_clean17===9 &&
 e.direct_exact_source_id_join_reconciled===true &&
 e.this_is_new_model_inference===false &&
 e.this_is_independent_SEER_validation===false &&
 e.test_results_accessed===false &&
 e.original_annotations_or_splits_modified===false,
 'wrong historical Eval provenance, confidence, version or split');
 ck(pt1.schema_version==='seer-ppe/read-only-valid-source-annotation-counts-part/v0.20' &&
 pt2.schema_version===pt1.schema_version &&
 pt1.part===1&&pt2.part===2&&pt1.total_parts===2&&pt2.total_parts===2 &&
 pt1.read_only===true&&pt2.read_only===true &&
 pt1.source_annotations_modified===false&&pt2.source_annotations_modified===false &&
 pt1.split==='valid'&&pt2.split==='valid'&&
 pt1.rows.length===250&&pt2.rows.length===209,
 'read-only source label metadata missing or malformed');
 ck(risks.schema_version==='seer-ppe/validation-source-computational-sensitivity-screen/v0.19' &&
 risks.input_original_valid_count===468&&risks.input_clean17_valid_count===459 &&
 risks.independent_valid_scientific_cohort_size===0 &&
 risks.source_family_groups_are_hypotheses_not_confirmed_acquisition_ids===true &&
 risks.scoring_ready===false && risks.test_sources_or_images_accessed===false &&
 risks.per_image_technical_flags.length===459,
 'source risk configuration is not frozen');
 const evalByID=new Map();
 for(const r of e.rows){
  ck(r.source_split==='valid'&&r.historical_saved_eval_image_id===r.source_id&&
   asInt(r.tp)&&asInt(r.fp)&&asInt(r.fn)&&
   typeof r.included_in_clean17_valid_459==='boolean' &&
   typeof r.source_id==='string'&&r.source_id.length>10&&!evalByID.has(r.source_id),
   'duplicate, wrong-split or invalid historical eval counter');
  evalByID.set(r.source_id,r);
 }
 ck(evalByID.size===468,'historical original Valid source coverage must be complete');
 const annotation=new Map();
 for(const a of [...pt1.rows,...pt2.rows]){
  ck(typeof a.source_id==='string'&&!annotation.has(a.source_id)&&
   asInt(a.saved_object_count)&&asInt(a.model_assisted_marker_count)&&
   asInt(a.polygon_count)&&a.model_assisted_marker_count<=a.saved_object_count&&
   a.polygon_count<=a.saved_object_count&&
   asInt(a.width)&&a.width>0&&asInt(a.height)&&a.height>0&&
   Object.values(a.class_counts).every(asInt)&&
   Object.values(a.class_counts).reduce((x,y)=>x+y,0)===a.saved_object_count,
   'original single-curator annotation counts duplicate/invalid');
  annotation.set(a.source_id,a);
 }
 ck(annotation.size===459,'current source annotation coverage drift');
 const s0=risks.descriptive_sensitivity_scenarios[k0],
 s1=risks.descriptive_sensitivity_scenarios[k1],
 s2=risks.descriptive_sensitivity_scenarios[k2];
 ck(s0.count===459&&s1.count===448&&s2.count===367,'prespecified cohort counts changed');
 const groupSets=new Map([[k0,new Set(s0.source_ids)],[k1,new Set(s1.source_ids)],[k2,new Set(s2.source_ids)]]);
 ck([...groupSets].every(([k,set])=>set.size===({[k0]:459,[k1]:448,[k2]:367})[k]) &&
 [...groupSets.get(k2)].every(x=>groupSets.get(k1).has(x)) &&
 [...groupSets.get(k1)].every(x=>groupSets.get(k0).has(x)),
 'source-risk cohorts not consistent nested sets');
 const kept=new Set(e.rows.filter(x=>x.included_in_clean17_valid_459).map(x=>x.source_id));
 ck(kept.size===459 && [...kept].every(x=>groupSets.get(k0).has(x)) &&
 [...groupSets.get(k0)].every(x=>annotation.has(x)),
 'original source IDs not exact-matched 459/459 or mismatch with current labels');
 const flagged=new Map(risks.per_image_technical_flags.map(x=>[x.original_valid_source_id,x]));
 ck(flagged.size===459&&[...kept].every(x=>flagged.has(x)),
 'source technical risk flags incomplete');
 const seenEntries=[];
 for(const id of [...kept].sort()){
  const saved=evalByID.get(id),source=annotation.get(id),screen=flagged.get(id);
  ck(saved && screen && source.source_original_filename===saved.source_original_filename &&
   screen.clean17_valid_export_filename &&
   screen.source_acquisition_independence_proven===false &&
   screen.independent_scientific_scoring_authorized===false,
   'source ID, original filename or family interpretation drift');
  const evaluatedReference=saved.tp+saved.fn;
  seenEntries.push({
   source_id:id,
   risk_bucket:screen.risk_bucket,
   historical_eval_tp:saved.tp,
   historical_eval_fp:saved.fp,
   historical_eval_fn:saved.fn,
   historical_eval_reference_object_count:evaluatedReference,
   current_saved_original_source_label_count:source.saved_object_count,
   current_source_model_assisted_label_marker_count:source.model_assisted_marker_count,
   source_label_count_matches_historical_eval:evaluatedReference===source.saved_object_count,
   historical_reference_count_minus_current_label_count:evaluatedReference-source.saved_object_count,
   in_448:groupSets.get(k1).has(id),
   in_367:groupSets.get(k2).has(id)
  });
 }
 function summarize(ids){
  const selected=seenEntries.filter(x=>ids.has(x.source_id));
  const sum=(name)=>selected.reduce((v,x)=>v+x[name],0);
  const tp=sum('historical_eval_tp'),fp=sum('historical_eval_fp'),fn=sum('historical_eval_fn');
  const ground=tp+fn,returned=tp+fp;
  const mismatch=selected.filter(x=>!x.source_label_count_matches_historical_eval);
  const P=returned?tp/returned:null,R=ground?tp/ground:null,F=2*tp+fp+fn?2*tp/(2*tp+fp+fn):null;
  return {
   images:selected.length,historical_tp:tp,historical_fp:fp,historical_fn:fn,
   historical_eval_reference_objects:ground,
   historical_eval_predicted_objects:returned,
   current_source_saved_annotation_boxes:sum('current_saved_original_source_label_count'),
   current_source_model_assisted_annotation_markers:sum('current_source_model_assisted_label_marker_count'),
   exact_label_count_agreement_images:selected.length-mismatch.length,
   label_count_mismatch_images:mismatch.length,
   total_current_minus_historical_reference_boxes:sum('current_saved_original_source_label_count')-ground,
   precision_micro_historical_valid:six(P),
   recall_micro_historical_valid:six(R),
   f1_micro_historical_valid:six(F),
   false_clearance_or_ppe_compliance_estimable:false,
   independent_source_generalization_supported:false
  };
 }
 const results=Object.fromEntries([...groupSets].map(([k,s])=>[k,summarize(s)]));
 ck(results[k0].images===459 && results[k1].images===448 && results[k2].images===367 &&
  results[k0].current_source_saved_annotation_boxes===3471 &&
  results[k0].exact_label_count_agreement_images===446 &&
  results[k0].label_count_mismatch_images===13 &&
  results[k0].total_current_minus_historical_reference_boxes===16,
  'original current source / historical eval divergence no longer matches V20 fetch');
 const counts={
  exact_matching_source_ids_to_historical_eval:468,
  original_valid_excluded_from_clean17:9,
  current_valid_original_source_annotations:459,
  original_current_labels_459:results[k0].current_source_saved_annotation_boxes,
  model_assisted_markers_459:results[k0].current_source_model_assisted_annotation_markers,
  historical_current_reference_agreement_459:446,
  historical_current_reference_mismatch_459:13,
  reference_object_count_difference_current_minus_historical:16
 };
 return {
  schema_version:'seer-ppe/historical-internal-valid-model-eval-three-risk-cohorts/v0.20',
  date:'2026-11-21',evaluation_basis:'SAVED_2025_ROBOFLOW_VERSION2_VALID_ONLY_PER_SOURCE_COUNTERS_REAGGREGATED_2026',
  model:'altayyar-0oflt-lafos-qqauz/2',existing_evaluation_id:e.eval_id,
  confidence_threshold:e.confidence_threshold,split:'valid',
  source_inputs_sha256:Object.fromEntries(Object.entries(paths).map(([k,v])=>[k,digest(v)])),
  exact_original_source_id_join:true,
  historical_source_annotation_geometry_available_from_platform_eval:false,
  historical_counters_not_recomputed_against_current_source_box_geometry:true,
  reference_drift_between_historical_eval_and_current_source_13_of_459:true,
  headline_caution:'Historical internal version2 Valid metrics only, not newly validated current-label performance or SEER policy improvement.',
  source_independence_verified:false,
  source_group_screening_only:true,
  no_new_original_model_inference:true,
  no_original_data_label_or_model_change:true,
  no_second_human_reviewer_required:true,
  test_not_read:true,
  explanation_energy_and_worker_safety_metrics_unavailable:true,
  strict_worker_safety_scoring_ready:false,
  totals:counts,
  descriptive_cohorts:results,
  delta_f1_percentage_points_relative_M0:{
   M1: six(100*(results[k1].f1_micro_historical_valid-results[k0].f1_micro_historical_valid)),
   M2: six(100*(results[k2].f1_micro_historical_valid-results[k0].f1_micro_historical_valid))
  },
  identity_resolved_individual_source_discrepancies:seenEntries.filter(x=>!x.source_label_count_matches_historical_eval).map(x=>({
   source_id:x.source_id,risk_bucket:x.risk_bucket,
   historical_eval_reference_objects:x.historical_eval_reference_object_count,
   current_source_saved_labels:x.current_saved_original_source_label_count,
   difference:x.historical_reference_count_minus_current_label_count
  })),
  per_image_numeric_audit:seenEntries
 };
}
function test(){
 const data=read(paths.historic),p1=read(paths.part1),p2=read(paths.part2),risk=read(paths.risk);
 const z=compile(data,p1,p2,risk);
 assert.equal(z.totals.historical_current_reference_mismatch_459,13);
 assert.equal(z.descriptive_cohorts[k0].images,459);
 assert.equal(z.descriptive_cohorts[k1].images,448);
 assert.equal(z.descriptive_cohorts[k2].images,367);
 const bad=structuredClone(data);bad.rows[0].source_split='test';
 assert.throws(()=>compile(bad,p1,p2,risk));
 const forged=structuredClone(data);forged.this_is_independent_SEER_validation=true;
 assert.throws(()=>compile(forged,p1,p2,risk));
 const drift=structuredClone(p1);drift.rows[0].saved_object_count+=1;
 assert.throws(()=>compile(data,drift,p2,risk));
 const duplicated=structuredClone(p2);duplicated.rows[0].source_id=p1.rows[0].source_id;
 assert.throws(()=>compile(data,p1,duplicated,risk));
 const independent=structuredClone(risk);independent.independent_valid_scientific_cohort_size=459;
 assert.throws(()=>compile(data,p1,p2,independent));
 console.log('SEER_V20_HISTORICAL_VALID_459_448_367_EXACT_ID_AND_13_REFERENCE_DRIFT_FAIL_CLOSED_TESTS_PASS');
}
try{
 const mode=process.argv[2]??'--audit';
 if(mode==='--self-test')test();
 else if(mode==='--audit'){
  const out=compile(read(paths.historic),read(paths.part1),read(paths.part2),read(paths.risk));
  if(process.argv[3])writeFileSync(process.argv[3],JSON.stringify(out,null,2)+'\n');
  console.log(JSON.stringify({totals:out.totals,
   cohorts:Object.fromEntries(Object.entries(out.descriptive_cohorts).map(([k,v])=>[k,{
    images:v.images,tp:v.historical_tp,fp:v.historical_fp,fn:v.historical_fn,
    precision:v.precision_micro_historical_valid,recall:v.recall_micro_historical_valid,
    f1:v.f1_micro_historical_valid,source_count_disagreements:v.label_count_mismatch_images
   }])),strict_worker_safety_scoring_ready:out.strict_worker_safety_scoring_ready},null,2));
  console.log('SEER_V20_READ_ONLY_HISTORICAL_VALID_INTERNAL_STATS_NOT_INDEPENDENT_PASS');
 } else throw Error('Usage --self-test | --audit [file]');
}catch(e){console.error(String(e));process.exitCode=2;}
