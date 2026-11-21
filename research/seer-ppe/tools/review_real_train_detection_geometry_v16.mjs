#!/usr/bin/env node
/**
 * SEER-PPE V16: exploratory Train-only detector-cue geometry and abstention.
 *
 * NO human reference scoring, compliance decisions, policy adjudication,
 * source-family release, Test data, model weights or scientific metrics.
 *
 * Inputs are actual Roboflow-hosted detections saved from an existing published
 * read-only workflow. Geometry proposes REVIEWS, not worker-item ground truth.
 */
import assert from 'node:assert/strict';
import {readFileSync,writeFileSync} from 'node:fs';
import {fileURLToPath} from 'node:url';
import {resolve} from 'node:path';

const ROOT=resolve(fileURLToPath(new URL('..',import.meta.url)));
const get=x=>JSON.parse(readFileSync(resolve(ROOT,x),'utf8'));
const CLASSES=Object.freeze({
 "Hard Hat":{ppe:"hard_hat",sense:"POSITIVE"},
 "No Hard Hat":{ppe:"hard_hat",sense:"NEGATIVE_MARKER"},
 "Safety Vests":{ppe:"safety_vest",sense:"POSITIVE"},
 "No Safety Vest":{ppe:"safety_vest",sense:"NEGATIVE_MARKER"},
 "Goggles":{ppe:"goggles",sense:"POSITIVE"},
 "Face Masks":{ppe:"face_mask",sense:"POSITIVE"},
 "No Face Mask":{ppe:"face_mask",sense:"NEGATIVE_MARKER"},
 "Gloves":{ppe:"glove",sense:"POSITIVE"},
 "No Gloves":{ppe:"glove",sense:"NEGATIVE_MARKER"},
 "Safety Boots":{ppe:"safety_boot",sense:"POSITIVE"},
 "No Safety Boots":{ppe:"safety_boot",sense:"NEGATIVE_MARKER"},
 "No Safety Attire":{ppe:null,sense:"GENERIC_NEGATIVE_CONTEXT"},
 "Pants":{ppe:null,sense:"CONTEXT_ONLY"},
 "Soft Hat":{ppe:null,sense:"CONTEXT_ONLY"},
 "Animal":{ppe:null,sense:"CONTEXT_ONLY"},
 "Child":{ppe:null,sense:"CONTEXT_ONLY"},
 "Persons":{ppe:null,sense:"PERSON"}
});
const TYPES=["hard_hat","safety_vest","goggles","face_mask","glove","safety_boot"];
const caseIds={A:"8f7cce94-d46e-4fac-9a0a-641bcd1f12c8",B:"87b6cc58-43bd-4583-8b13-bd9b7413c03d",C:"c032f81d-64c5-44be-96f3-7e6fe9dad799",D:"c197d82e-7870-42a3-bf94-462420d3f6a2"};
const thresholds={candidate_confidence:0.20,high_confidence:0.60,minimum_positive_overlap:0.25,unique_ppe_overlap:0.75,ambiguous_second_overlap:0.45,unambiguous_margin:0.30};
function ensure(cond,msg){if(!cond)throw Error("SEER_V16_REVIEW_CUE_GATE_BLOCKED:"+msg);}
function round(x){return Number(x.toFixed(5));}
function bbox(d,W,H){
 ensure(Number.isFinite(d.x)&&Number.isFinite(d.y)&&
  Number.isFinite(d.width)&&Number.isFinite(d.height)&&d.width>0&&d.height>0,
  'invalid detector xywh');
 const x1=Math.max(0,d.x-d.width/2),y1=Math.max(0,d.y-d.height/2),
       x2=Math.min(W,d.x+d.width/2),y2=Math.min(H,d.y+d.height/2);
 ensure(x2>x1&&y2>y1,'detection outside image');
 return {x1,y1,x2,y2,area:(x2-x1)*(y2-y1)};
}
function intersectionFrac(item,person){
 const x=Math.max(0,Math.min(item.x2,person.x2)-Math.max(item.x1,person.x1));
 const y=Math.max(0,Math.min(item.y2,person.y2)-Math.max(item.y1,person.y1));
 return x*y/item.area;
}
function inspectCase(c){
 ensure(c.source_split==='train'&&caseIds[c.case]===c.case_id,'only four verified Train controls allowed');
 ensure(c.model_id==='altayyar-0oflt-lafos-qqauz/2'&&
 c.workflow_id==='61llCTFuQ4Aq4goQ9HiP'&&
 c.ground_truth_state==='incomplete','model/workflow/GT changed');
 ensure(c.no_test_media===true&&c.used_as_scientific_score===false&&
 c.human_reference_read_only===true,'unsupported scientific/use scope');
 const {width:W,height:H}=c.image_dimensions??{};
 ensure(Number.isInteger(W)&&Number.isInteger(H)&&W>0&&H>0,'bad source image dims');
 ensure(Array.isArray(c.detections)&&c.counts.raw===c.detections.length,'raw detection count altered');
 ensure(c.counts.high_confidence+c.counts.lower_confidence===c.counts.raw,
 'confidence split mismatch');
 ensure(c.counts.raw>=0&&c.counts.raw<=5000,'anomalous number of detections');
 const ids=new Set();
 const detections=c.detections.map(d=>{
  ensure(typeof d.id==='string'&&d.id.length>=8&&!ids.has(d.id),'duplicate detector ID');
  ids.add(d.id);
  ensure(Object.hasOwn(CLASSES,d.cls),'unexpected model class');
  ensure(typeof d.class_id==='number'&&Number.isInteger(d.class_id),'invalid class index');
  ensure(Number.isFinite(d.confidence)&&d.confidence>=thresholds.candidate_confidence-0.00001
   &&d.confidence<=1,'unexpected low/high detector threshold');
  return {...d,rect:bbox(d,W,H),group:CLASSES[d.cls]};
 });
 const persons=detections.filter(d=>d.group.sense==='PERSON');
 const items=detections.filter(d=>d.group.ppe!==null);
 const contexts=detections.filter(d=>d.group.ppe===null&&d.group.sense!=='PERSON');
 ensure(persons.length===c.counts.persons,'original workflow person count changed');
 ensure(detections.filter(d=>d.confidence<0.6).length===c.counts.lower_confidence,
 'original lower-confidence detection count changed');
 const personById=new Map(persons.map(p=>[p.id,p]));
 const itemRows=items.map(it=>{
  const overlaps=persons.map(p=>({person_detection_id:p.id,overlap_fraction:round(intersectionFrac(it.rect,p.rect))}))
   .filter(x=>x.overlap_fraction>=thresholds.minimum_positive_overlap)
   .sort((a,b)=>b.overlap_fraction-a.overlap_fraction||
    a.person_detection_id.localeCompare(b.person_detection_id));
  const best=overlaps[0],second=overlaps[1];
  let status='NO_PERSON_DETECTION_COVERAGE_UNKNOWN',candidate=null;
  if(persons.length>0){
   if(!best)status='NO_GEOMETRIC_PERSON_CANDIDATE';
   else if(best.overlap_fraction>=thresholds.unique_ppe_overlap&&
    (!second||second.overlap_fraction<thresholds.ambiguous_second_overlap||
       best.overlap_fraction-second.overlap_fraction>=thresholds.unambiguous_margin)){
     status='SINGLE_STRONG_GEOMETRIC_CANDIDATE_REVIEW_ONLY';
     candidate=best.person_detection_id;
   }else status='MULTIPLE_OR_WEAK_GEOMETRIC_CANDIDATES_REVIEW_ONLY';
  }
  return {
   item_detection_id:it.id,detector_class:it.cls,
   ppe_type:it.group.ppe,cue_sense:it.group.sense,
   confidence:it.confidence,confidence_band:it.confidence>=thresholds.high_confidence?'HIGH':'LOW_REVIEW',
   candidate_people:overlaps,
   geometry_status:status,
   single_strong_candidate_person_detection_id:candidate,
   human_confirmed_owner_id:null,
   human_verified_visual_state:null,
   workplace_requirement:'POLICY_UNKNOWN',
   clearance_or_violation_decision:null
  };
 });
 const personRows=persons.map(p=>{
  const types={};
  for(const type of TYPES){
   const attached=itemRows.filter(i=>i.ppe_type===type&&
     i.single_strong_candidate_person_detection_id===p.id);
   const positives=attached.filter(i=>i.cue_sense==='POSITIVE').map(i=>i.item_detection_id);
   const markers=attached.filter(i=>i.cue_sense==='NEGATIVE_MARKER').map(i=>i.item_detection_id);
   let state='NO_STRONG_SINGLE_OWNER_CUE';
   if(positives.length&&markers.length)state='CONFLICTING_POSITIVE_AND_NEGATIVE_MARKER_CUES';
   else if(positives.length)state='POSITIVE_DETECTOR_CUE_UNVERIFIED';
   else if(markers.length)state='NEGATIVE_DETECTOR_MARKER_UNVERIFIED';
   types[type]={detector_cue_status:state,strong_positive_candidate_ids:positives,
    strong_negative_marker_candidate_ids:markers,
    human_visual_state:null,task_mandate:'POLICY_UNKNOWN',
    false_clearance_assessment:null};
  }
  return {person_detection_id:p.id,person_candidate_confidence:p.confidence,
   person_human_coverage_confirmed:false,person_identity_human_matched:null,
   visual_ppe_cues:types,worker_compliance_status:'NOT_ESTIMABLE_POLICY_AND_HUMAN_EVIDENCE_MISSING'};
 });
 const uncertain=itemRows.filter(x=>x.geometry_status!=='SINGLE_STRONG_GEOMETRIC_CANDIDATE_REVIEW_ONLY');
 const low=itemRows.filter(x=>x.confidence_band==='LOW_REVIEW');
 const count={detection_candidates:detections.length,person_candidates:persons.length,
  specific_ppe_candidates:itemRows.length,context_only_not_specific_ppe:contexts.length,
  single_geometric_owner_proposals:itemRows.length-uncertain.length,
  ambiguous_or_unassigned_specific_ppe:uncertain.length,
  low_confidence_specific_ppe_review_items:low.length,
  generic_negative_attire_context_only:contexts.filter(x=>x.cls==='No Safety Attire').length,
  human_matched_item_owners:0,person_PPE_visual_states_inferred_as_GT:0,
  compliance_verdicts:0};
 return {case:c.case,case_id:c.case_id,original_split:'train',
  model_id:c.model_id,workflow_id:c.workflow_id,
  input_image_dimensions:[W,H],
  workflow_person_coverage_code:c.workflow_review_codes.person_coverage,
  human_scene_person_coverage_signed:false,
  non_scoring_review_status:persons.length===0?'ZERO_DETECTED_PERSONS_HUMAN_SCENE_REVIEW_NEEDED':
    'DETECTED_PERSONS_BUT_FULL_COVERAGE_NOT_VERIFIED',
  confidence_review_status:c.workflow_review_codes.confidence,
  potential_review_suggestions_not_human_annotations:true,
  counts:count,per_person_candidate_review:personRows,per_item_candidate_review:itemRows,
  context_only_candidate_classes:contexts.map(x=>({detection_id:x.id,detector_class:x.cls,
   confidence:x.confidence,explicit_PPE_absence_inferred:false})),
  source_ground_truth_modified:false,scientific_performance_scored:false};
}
function compile(input){
 ensure(input.schema_version==='seer-ppe/train-only-real-roboflow-preflight/v0.16',
  'wrong preflight schema');
 ensure(input.model_id==='altayyar-0oflt-lafos-qqauz/2'&&
  input.workflow_id==='61llCTFuQ4Aq4goQ9HiP'&&input.active_learning_disabled===true,
  'training/active learning or model version prohibited');
 ensure(input.model_retrained===false&&input.reference_cases_modified===false&&
  input.dataset_images_or_labels_modified===false&&input.test_inputs_used===0&&
  input.validation_inputs_used===0&&input.scientific_performance_metric_computed===false&&
  input.workflow_outputs_image_bytes_retained===false&&
  input.workflow_outputs_signed_urls_retained===false,'training/split/media/score scope violation');
 ensure(input.cases.length===4&&new Set(input.cases.map(c=>c.case)).size===4,
   'four original Train cases A-D required');
 const rows=input.cases.map(inspectCase).sort((a,b)=>a.case.localeCompare(b.case));
 const totals={};
 for(const key of Object.keys(rows[0].counts))
  totals[key]=rows.reduce((a,x)=>a+x.counts[key],0);
 ensure(totals.detection_candidates===51&&totals.person_candidates===7,
  'live Train detector baseline count unexpectedly drifted');
 ensure(rows.find(x=>x.case==='D').counts.person_candidates===0,'zero person D regression');
 ensure(rows.find(x=>x.case==='D').non_scoring_review_status===
    'ZERO_DETECTED_PERSONS_HUMAN_SCENE_REVIEW_NEEDED','zero human coverage fallacy');
 for(const r of rows){
  ensure(r.counts.human_matched_item_owners===0&&r.counts.compliance_verdicts===0,
    'geometry must not promote human compliance');
 }
 return {schema_version:'seer-ppe/conservative-geometric-person-ppe-review-proposals/v0.16',
  date:'2026-11-21',execution_basis:'REAL_HOSTED_ROBOFLOW_TRAIN_ONLY_RFDETR_V2_PREDICTIONS',
  developer_test_images:0,test_or_valid_inference_performed_by_this_tool:false,
  original_model_id:input.model_id,source_workflow_id:input.workflow_id,
  source_ground_truth_inspected_for_scientific_metric:false,
  human_validated_PPE_or_person_coverage_count:0,
  automated_person_PPE_compliance_verdicts:0,policy_required_assumptions_made:0,
  model_accuracy_mAP_F1_measured:false,energy_joules_measured:null,
  original_model_retrained:false,source_images_or_annotations_modified:false,
  human_case_ground_truth_modified:false,source_independence_signed:false,
  validation_freeze_authorized:false,scientific_scoring_ready:false,
  thresholds,totals,cases:rows};
}
function selfTest(){
 const src=get('ROBOFLOW_TRAIN_ONLY_REAL_MODEL_PREFLIGHT_2026-11-21_V16.json');
 const out=compile(src);
 assert.equal(out.totals.detection_candidates,51);
 assert.equal(out.totals.person_candidates,7);
 assert.equal(out.automated_person_PPE_compliance_verdicts,0);
 const d=out.cases.find(x=>x.case==='D');
 assert.equal(d.non_scoring_review_status,'ZERO_DETECTED_PERSONS_HUMAN_SCENE_REVIEW_NEEDED');
 assert.ok(d.per_item_candidate_review.every(x=>x.human_confirmed_owner_id===null));
 assert.equal(d.counts.single_geometric_owner_proposals,0);
 const b=out.cases.find(x=>x.case==='B');
 assert.ok(b.per_person_candidate_review.every(p=>p.worker_compliance_status.startsWith('NOT_ESTIMABLE')));
 const c=out.cases.find(x=>x.case==='C');
 assert.ok(c.per_item_candidate_review.every(p=>p.human_verified_visual_state===null));
 const duplicate=structuredClone(src);
 duplicate.cases[0].detections[1].id=duplicate.cases[0].detections[0].id;
 assert.throws(()=>compile(duplicate));
 const test=structuredClone(src);test.cases[0].source_split='test';
 assert.throws(()=>compile(test));
 const changedModel=structuredClone(src);changedModel.model_id='changed-model/99';
 assert.throws(()=>compile(changedModel));
 const falseGT=structuredClone(src);falseGT.cases[0].ground_truth_state='complete';
 assert.throws(()=>compile(falseGT));
 const contradiction=structuredClone(src);
 contradiction.cases[3].counts.persons=1;
 assert.throws(()=>compile(contradiction));
 const absence=structuredClone(src);
 const noMask=absence.cases[0].detections.find(x=>x.cls==='No Face Mask');
 noMask.cls='No Safety Attire';
 const output=compile(absence);
 assert.ok(output.cases[0].per_person_candidate_review.every(p=>p.visual_ppe_cues.face_mask.human_visual_state===null));
 console.log('SEER_V16_SYNTHETIC_NEVER_INFER_HUMAN_PPE_ABSENCE_OR_COMPLIANCE_PASS');
 console.log('SEER_V16_SYNTHETIC_INVALID_TEST_GT_MODEL_AND_GEOMETRY_REJECTED_PASS');
}
try{
 const cmd=process.argv[2]??'--audit';
 if(cmd==='--self-test')selfTest();
 else if(cmd==='--audit'){
  const r=compile(get('ROBOFLOW_TRAIN_ONLY_REAL_MODEL_PREFLIGHT_2026-11-21_V16.json'));
  if(process.argv[3])writeFileSync(process.argv[3],JSON.stringify(r,null,2)+'\n');
  console.log(JSON.stringify({schema_version:r.schema_version,totals:r.totals,
   cases:r.cases.map(x=>({case:x.case,counts:x.counts,
     review_status:x.non_scoring_review_status})),
   scores_computed:false,energy_measured:false,scientific_scoring_ready:r.scientific_scoring_ready},null,2));
  console.log('SEER_V16_REAL_TRAIN_ONLY_DETECTION_METADATA_GEOMETRY_ABSTENTION_PASS');
 }else throw Error('Usage: --self-test | --audit [output-file]');
}catch(e){console.error(String(e));process.exitCode=2;}
