#!/usr/bin/env node
/**
 * SEER-PPE V22: post-V20, read-only descriptive 17-class annotation support
 * across pre-existing M0/M1/M2 original-Source Valid membership.
 * Does NOT run inference, derive PPE compliance, identify workers, access Test,
 * modify original data, or claim independent acquisition groups.
 */
import assert from 'node:assert/strict';
import {readFileSync,writeFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import {resolve} from 'node:path';
import {fileURLToPath} from 'node:url';
const DIR=resolve(fileURLToPath(new URL('..',import.meta.url)));
const files={
part1:'V20_VALID_SOURCE_ANNOTATION_COUNTS_PART1_PRIVATE_WORKING.json',
part2:'V20_VALID_SOURCE_ANNOTATION_COUNTS_PART2_PRIVATE_WORKING.json',
risk:'VALIDATION_SOURCE_OVERLAP_NUMERIC_SENSITIVITY_V19.json',
historical:'HISTORICAL_VALID_INTERNAL_METRICS_V20.json',
author:'AUTHOR_CURATOR_REFERENCE_POLICY_2026-11-21_V18.json'
};
const read=n=>JSON.parse(readFileSync(resolve(DIR,n),'utf8'));
const hash=n=>createHash('sha256').update(readFileSync(resolve(DIR,n))).digest('hex');
const fail=(x,message)=>{if(!x)throw Error('SEER_V22_VALID_CLASS_AUDIT_BLOCKED:'+message);};
const f6=v=>Number(v.toFixed(6));
const K=[
'ALL_MATCHED_VALID_459',
'EXCLUDE_HISTORICAL_HOLDS_AND_TECHNICAL_QUARANTINES_448',
'UNFLAGGED_ONLY_BUT_UNCERTIFIED_367'
];
const classes=['Animal','Child','Face Masks','No Hard Hat','No Safety Boots',
'Soft Hat','Hard Hat','No Safety Vest','Pants','No Face Mask',
'No Safety Attire','No Gloves','Gloves','Safety Boots','Safety Vests','Goggles','Persons'];
function compile(a,b,risk,hist,author){
 fail(a.schema_version==='seer-ppe/read-only-valid-source-annotation-counts-part/v0.20'&&
   b.schema_version===a.schema_version&&a.part===1&&b.part===2&&a.total_parts===2&&b.total_parts===2&&
   a.project_id==='softyyemen/altayyar-0oflt-lafos-qqauz'&&a.project_id===b.project_id&&
   a.split==='valid'&&b.split==='valid'&&a.read_only&&b.read_only&&
   !a.source_annotations_modified&&!b.source_annotations_modified&&
   a.rows.length===250&&b.rows.length===209,
   'source annotation snapshots must be original read-only Valid 250 + 209');
 fail(risk.schema_version==='seer-ppe/validation-source-computational-sensitivity-screen/v0.19'&&
   risk.input_original_valid_count===468&&risk.input_clean17_valid_count===459&&
   risk.test_sources_or_images_accessed===false&&risk.scoring_ready===false&&
   risk.source_family_groups_are_hypotheses_not_confirmed_acquisition_ids===true&&
   risk.independent_valid_scientific_cohort_size===0,
   'source-risk cohort was changed or falsely marked independent');
 fail(hist.schema_version==='seer-ppe/historical-internal-valid-model-eval-three-risk-cohorts/v0.20'&&
   hist.model==='altayyar-0oflt-lafos-qqauz/2'&&hist.split==='valid'&&
   hist.existing_evaluation_id==='KyzP9neuyNTN5eQpGCAY'&&
   hist.no_new_original_model_inference===true&&
   hist.strict_worker_safety_scoring_ready===false&&
   hist.test_not_read===true&&
   hist.historical_counters_not_recomputed_against_current_source_box_geometry===true,
   'historical Valid model Eval provenance mismatched');
 fail(author.schema_version==='seer-ppe/author-single-curator-primary-reference-policy/v0.18'&&
   author.original_annotations_accepted_as_single_curator_object_detection_reference===true&&
   author.second_human_reviewer_required===false,'author approval status drift');
 const rows=[...a.rows,...b.rows],byid=new Map();
 const allowed=new Set(classes);
 for(const x of rows){
   fail(typeof x.source_id==='string'&&x.source_id.length>10&&!byid.has(x.source_id)&&
     typeof x.source_original_filename==='string'&&x.source_original_filename.length>0&&
     Number.isInteger(x.saved_object_count)&&x.saved_object_count>=0&&
     Number.isInteger(x.model_assisted_marker_count)&&x.model_assisted_marker_count>=0&&
     x.model_assisted_marker_count<=x.saved_object_count&&
     typeof x.class_counts==='object'&&x.class_counts!==null&&
     Object.entries(x.class_counts).every(([cls,v])=>allowed.has(cls)&&Number.isInteger(v)&&v>0)&&
     Object.values(x.class_counts).reduce((s,v)=>s+v,0)===x.saved_object_count,
     'invalid source box count, duplicate ID, label or assistance count');
   byid.set(x.source_id,x);
 }
 fail(byid.size===459,'missing annotated source images');
 const sets=K.map(k=>new Set(risk.descriptive_sensitivity_scenarios[k]?.source_ids));
 fail(sets[0].size===459&&sets[1].size===448&&sets[2].size===367&&
   [...sets[0]].every(id=>byid.has(id))&&
   [...sets[2]].every(id=>sets[1].has(id))&&
   [...sets[1]].every(id=>sets[0].has(id)),
   'source-risk cohorts are not exact nested M0/M1/M2');
 const riskMap=new Map(risk.per_image_technical_flags.map(x=>[x.original_valid_source_id,x]));
 fail(riskMap.size===459&&[...sets[0]].every(id=>riskMap.has(id)),
   'missing source-risk entries');
 function summary(ids){
   const chosen=[...ids].map(id=>byid.get(id));
   const n=chosen.length,objects=chosen.reduce((s,r)=>s+r.saved_object_count,0),
     assisted=chosen.reduce((s,r)=>s+r.model_assisted_marker_count,0);
   const counts=Object.fromEntries(classes.map(c=>[c,0]));
   const imageCounts=Object.fromEntries(classes.map(c=>[c,0]));
   for(const x of chosen){
     for(const [c,val] of Object.entries(x.class_counts)){
       counts[c]+=val;imageCounts[c]+=1;
     }
   }
   const numericalObjects=Object.values(counts).reduce((s,v)=>s+v,0);
   fail(numericalObjects===objects,'per-class box conservation violated');
   const perClass=classes.map(c=>({
     class_name:c,saved_current_reference_boxes:counts[c],
     images_containing_class:imageCounts[c],
     fraction_of_images_with_class:f6(imageCounts[c]/n),
     fraction_of_boxes_from_class:f6(counts[c]/objects)
   })).sort((a,b)=>b.saved_current_reference_boxes-a.saved_current_reference_boxes||
     a.class_name.localeCompare(b.class_name));
   const boxCounts=chosen.map(x=>x.saved_object_count).sort((x,y)=>x-y);
   const percentile=(fraction)=>boxCounts[Math.ceil(fraction*(boxCounts.length-1))];
   return {
     valid_original_source_images:n,
     stored_current_source_annotation_boxes:objects,
     mean_boxes_per_image:f6(objects/n),
     median_boxes_per_image:percentile(.5),
     p90_boxes_per_image:percentile(.90),
     max_boxes_in_one_image:boxCounts.at(-1),
     images_with_no_stored_annotation_boxes:chosen.filter(x=>x.saved_object_count===0).length,
     model_assisted_annotation_provenance_markers:assisted,
     fraction_annotation_boxes_with_model_assisted_marker:f6(assisted/objects),
     images_containing_any_model_assisted_marker:chosen.filter(x=>x.model_assisted_marker_count>0).length,
     fraction_images_containing_assisted_marker:f6(chosen.filter(x=>x.model_assisted_marker_count>0).length/n),
     observed_object_classes:perClass.filter(x=>x.saved_current_reference_boxes>0).length,
     class_support:perClass
   };
 }
 const cohorts=Object.fromEntries(K.map((key,i)=>[key,summary(sets[i])]));
 fail(cohorts[K[0]].stored_current_source_annotation_boxes===3471&&
  cohorts[K[1]].stored_current_source_annotation_boxes===3433&&
  cohorts[K[2]].stored_current_source_annotation_boxes===3049&&
  cohorts[K[0]].model_assisted_annotation_provenance_markers===729&&
  cohorts[K[1]].model_assisted_annotation_provenance_markers===725&&
  cohorts[K[2]].model_assisted_annotation_provenance_markers===655&&
  cohorts[K[0]].observed_object_classes===17,
  'known current author source reference counts disagree');
 // Existing historic V20 result provenance check; do not re-label its metrics.
 for(const key of K){
   const m=hist.descriptive_cohorts[key];
   fail(m.images===cohorts[key].valid_original_source_images&&
     m.current_source_saved_annotation_boxes===cohorts[key].stored_current_source_annotation_boxes&&
     m.current_source_model_assisted_annotation_markers===cohorts[key].model_assisted_annotation_provenance_markers,
     'historic V20 must count the same current labels per cohort');
 }
 const full=cohorts[K[0]],reduced=cohorts[K[2]];
 const excluded=[...sets[0]].filter(id=>!sets[2].has(id));
 const excludedObjects=excluded.reduce((s,id)=>s+byid.get(id).saved_object_count,0);
 const perClassFull=new Map(full.class_support.map(x=>[x.class_name,x]));
 const perClassReduced=new Map(reduced.class_support.map(x=>[x.class_name,x]));
 const retention=classes.map(c=>{
   const a=perClassFull.get(c),b=perClassReduced.get(c);
   return {class_name:c,
     m0_current_boxes:a.saved_current_reference_boxes,
     m2_current_boxes:b.saved_current_reference_boxes,
     boxes_removed:a.saved_current_reference_boxes-b.saved_current_reference_boxes,
     boxes_retained_fraction:f6(b.saved_current_reference_boxes/a.saved_current_reference_boxes),
     m0_images_containing_class:a.images_containing_class,
     m2_images_containing_class:b.images_containing_class};
 }).sort((a,b)=>a.boxes_retained_fraction-b.boxes_retained_fraction||
   a.class_name.localeCompare(b.class_name));
 const historicDiff=new Set(hist.identity_resolved_individual_source_discrepancies.map(x=>x.source_id));
 fail(historicDiff.size===13&&[...historicDiff].every(id=>byid.has(id))&&
   hist.totals.current_source_original_source_annotations===undefined,
   'legacy/current mismatch trace invalid or unexpected summary contract');
 const riskCounts={};
 for(const row of riskMap.values())riskCounts[row.risk_bucket]=(riskCounts[row.risk_bucket]??0)+1;
 fail(riskCounts.HISTORICAL_HOLD===5&&riskCounts.HIGH_OVERLAP_TECHNICAL_QUARANTINE===6&&
  riskCounts.POTENTIAL_SOURCE_FAMILY_LINK_PENDING===81&&
  riskCounts.UNFLAGGED_NOT_PROVEN_INDEPENDENT===367,'risk bucket counts changed');
 return {
   schema_version:'seer-ppe/author-valid-class-support-and-composition-risk-v0.22',
   date:'2026-11-21',scope:'CURRENT_AUTHOR_SOURCE_VALID_LABELS_ONLY_NOT_NEW_MODEL_SCORE',
   original_model_id_unchanged:'altayyar-0oflt-lafos-qqauz/2',
   original_images_modified:false,original_annotations_modified:false,
   new_model_inference:false,test_images_or_outcomes_accessed:false,
   second_human_image_reviewer_needed:false,
   primary_reference:'AUTHOR_CURATED_SINGLE_RESEARCHER_ORIGINAL_SOURCE_BOXES',
   source_independence_verified:false,
   scientific_SEER_worker_safety_scoring_ready:false,
   current_box_support_not_historical_eval_groundtruth_geometry:true,
   model_assisted_marker_is_provenance_not_automatic_error:true,
   source_sha256:Object.fromEntries(Object.entries(files).map(([k,n])=>[k,hash(n)])),
   cohorts,source_risk_bucket_counts:riskCounts,
   m0_to_m2_composition_sensitivity:{
     images_excluded:excluded.length,
     fraction_images_retained:f6(sets[2].size/sets[0].size),
     current_box_annotations_excluded:excludedObjects,
     fraction_boxes_retained:f6(reduced.stored_current_source_annotation_boxes/full.stored_current_source_annotation_boxes),
     mean_boxes_per_excluded_image:f6(excludedObjects/excluded.length),
     classes_retention:retention
   },
   historic_2025_legacy_eval_vs_current_source_count_disagreements_13_source_ids:[...historicDiff].sort(),
   analysis_limits:[
     'This audit counts CURRENT author-curated Source boxes, not 2025 versioned Eval GT',
     'Model-assistance marker counts are per-image aggregates, not per-class provenance',
     'Class names beginning No do not prove true task-specific occupational violations',
     'Box counts in M0/M1/M2 are descriptive compositions not new prediction accuracy',
     'All M2 sources are technically unflagged but not independently verified'
   ]
 };
}
function test(){
 const inputs=Object.values(files).map(read);
 const z=compile(...inputs);
 assert.equal(z.cohorts[K[0]].observed_object_classes,17);
 assert.equal(z.cohorts[K[0]].stored_current_source_annotation_boxes,3471);
 assert.equal(z.cohorts[K[2]].valid_original_source_images,367);
 const bad=structuredClone(inputs[0]);bad.rows[0].class_counts={Persons:1};
 assert.throws(()=>compile(bad,...inputs.slice(1)));
 const bad2=structuredClone(inputs[1]);bad2.split='test';
 assert.throws(()=>compile(inputs[0],bad2,...inputs.slice(2)));
 const bad3=structuredClone(inputs[2]);bad3.independent_valid_scientific_cohort_size=367;
 assert.throws(()=>compile(inputs[0],inputs[1],bad3,...inputs.slice(3)));
 const bad4=structuredClone(inputs[3]);bad4.existing_evaluation_id='unverified-new-eval';
 assert.throws(()=>compile(inputs[0],inputs[1],inputs[2],bad4,inputs[4]));
 const bad5=structuredClone(inputs[4]);bad5.second_human_reviewer_required=true;
 assert.throws(()=>compile(inputs[0],inputs[1],inputs[2],inputs[3],bad5));
 console.log('V22_SOURCE_CLASS_17_LABEL_COUNT_RETENTION_MODEL_ASSISTANCE_AND_TEST_GATE_SELFTESTS_PASS');
}
try{
 const mode=process.argv[2]||'--audit';
 if(mode==='--self-test')test();
 else if(mode==='--audit'){
  const z=compile(...Object.values(files).map(read));
  if(process.argv[3])writeFileSync(process.argv[3],JSON.stringify(z,null,2)+'\n');
  console.log(JSON.stringify({
   cohorts:Object.fromEntries(K.map(k=>[k,{
    images:z.cohorts[k].valid_original_source_images,
    boxes:z.cohorts[k].stored_current_source_annotation_boxes,
    assisted:z.cohorts[k].model_assisted_annotation_provenance_markers,
    classes:z.cohorts[k].observed_object_classes
   }])),
   m0_to_m2:z.m0_to_m2_composition_sensitivity,
   model_modified:false,Test_used:false,worker_safety_metric_measured:false
  },null,2));
  console.log('SEER_V22_AUTHOR_VALID_CLASS_SOURCE_DISTRIBUTION_AUDIT_PASS');
 }else throw Error('Usage: --self-test | --audit [output.json]');
}catch(e){console.error(String(e));process.exitCode=2;}
