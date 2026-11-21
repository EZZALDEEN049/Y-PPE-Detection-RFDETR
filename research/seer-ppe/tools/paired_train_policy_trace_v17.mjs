#!/usr/bin/env node
/**
 * SEER-PPE V17: paired detector-input / conservative-policy OFFLINE trace.
 *
 * Reads only public, immutable Train-only V16 numeric model and geometry records.
 * DOES NOT read human PPE labels as online policy features, run inference, perform
 * XAI, send human-review requests, change Roboflow data, or compute scientific
 * performance. A0 and A5 below are two views of SAME saved model detections,
 * not measured comparative inference runs or validated safety outcomes.
 */
import assert from 'node:assert/strict';
import {readFileSync,writeFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import {fileURLToPath} from 'node:url';
import {resolve} from 'node:path';

const ROOT=resolve(fileURLToPath(new URL('..',import.meta.url)));
const files={
 raw:'ROBOFLOW_TRAIN_ONLY_REAL_MODEL_PREFLIGHT_2026-11-21_V16.json',
 geometry:'TRAIN_ONLY_PERSON_PPE_GEOMETRIC_REVIEW_V16.json',
 readiness:'VALIDATION_459_SIGNED_SOURCE_COHORT_READINESS_V15.json',
 freeze:'VALIDATION_PERSON_PPE_SCORING_FREEZE_2026-11-21_V11.json'
};
const read=name=>JSON.parse(readFileSync(resolve(ROOT,name),'utf8'));
const sha=name=>createHash('sha256').update(readFileSync(resolve(ROOT,name))).digest('hex');
const ck=(value,message)=>{if(!value)throw Error('SEER_V17_PAIRED_PRE_FREEZE_GATE_BLOCKED:'+message);};
const expected={
 A:'8f7cce94-d46e-4fac-9a0a-641bcd1f12c8',
 B:'87b6cc58-43bd-4583-8b13-bd9b7413c03d',
 C:'c032f81d-64c5-44be-96f3-7e6fe9dad799',
 D:'c197d82e-7870-42a3-bf94-462420d3f6a2'
};
const geometryStates=new Set([
 'SINGLE_STRONG_GEOMETRIC_CANDIDATE_REVIEW_ONLY',
 'MULTIPLE_OR_WEAK_GEOMETRIC_CANDIDATES_REVIEW_ONLY',
 'NO_GEOMETRIC_PERSON_CANDIDATE',
 'NO_PERSON_DETECTION_COVERAGE_UNKNOWN'
]);
function trace(raw,geom,valid,freeze){
 ck(raw.schema_version==='seer-ppe/train-only-real-roboflow-preflight/v0.16' &&
  geom.schema_version==='seer-ppe/conservative-geometric-person-ppe-review-proposals/v0.16',
  'original V16 evidence schema changed');
 ck(raw.model_id==='altayyar-0oflt-lafos-qqauz/2' &&
  raw.workflow_id==='61llCTFuQ4Aq4goQ9HiP' &&
  geom.original_model_id===raw.model_id &&
  geom.source_workflow_id===raw.workflow_id,
  'model or workflow identity mismatch');
 ck(raw.source==='ACTUAL_HOSTED_ROBOFLOW_WORKFLOW_RUN_ON_FOUR_EXISTING_TRAIN_CASE_READ_CAPABILITY_URLS' &&
  raw.test_inputs_used===0 && raw.validation_inputs_used===0 &&
  raw.model_retrained===false && raw.model_modified===false &&
  raw.reference_cases_modified===false && raw.scientific_performance_metric_computed===false &&
  raw.scoring_ready===false && raw.validation_freeze_authorized===false &&
  geom.scientific_scoring_ready===false && geom.original_model_retrained===false &&
  geom.source_images_or_annotations_modified===false &&
  geom.human_case_ground_truth_modified===false &&
  geom.automated_person_PPE_compliance_verdicts===0,
  'source model, read-only, train-only or scoring boundary altered');
 ck(raw.cases.length===4 && geom.cases.length===4 &&
  new Set(raw.cases.map(x=>x.case)).size===4 &&
  new Set(geom.cases.map(x=>x.case)).size===4,
  'A-D case identity/number drift');
 ck(valid.schema_version==='seer-ppe/validation-evidence-qualification-audit/v0.15' &&
  valid.original_valid_count===468 && valid.clean17_valid_count===459 &&
  valid.direct_source_to_clean17_content_correspondence===459 &&
  valid.per_image_source_family_human_decisions_signed===0 &&
  valid.human_independence_attestations===0 &&
  valid.current_validation_person_reference_signed===false &&
  valid.scoring_ready===false &&
  valid.image_rows.length===459 &&
  valid.image_rows.every(x=>x.eligible_for_scientific_scoring===false),
  'unsigned original Valid cohort unexpectedly represented as scoring-ready');
 ck(freeze.schema_version==='seer-ppe/validation-scoring-freeze/v0.11' &&
  freeze.state==='NOT_FROZEN' && freeze.authorized===false &&
  freeze.test_authorized===false && freeze.current_scoring_ready===false &&
  freeze.approved_valid_source_ids.length===0 &&
  Object.values(freeze.gates).every(x=>x===false),
  'Validation scoring freeze must remain closed');
 const cases=[];
 const allIDs=new Set();
 for(const m of raw.cases){
  const g=geom.cases.find(c=>c.case===m.case);
  ck(g && m.case_id===expected[m.case] && g.case_id===m.case_id &&
   m.source_split==='train' && g.original_split==='train' &&
   m.model_id===raw.model_id && m.workflow_id===raw.workflow_id &&
   m.no_test_media===true && m.used_as_scientific_score===false &&
   m.human_reference_read_only===true &&
   g.human_scene_person_coverage_signed===false &&
   g.scientific_performance_scored===false && g.source_ground_truth_modified===false,
   'case identity / split / coverage / ground truth mismatch');
  ck(m.counts.raw===m.detections.length &&
   m.counts.raw===g.counts.detection_candidates &&
   m.counts.persons===g.counts.person_candidates &&
   g.counts.specific_ppe_candidates===g.per_item_candidate_review.length &&
   g.counts.context_only_not_specific_ppe===g.context_only_candidate_classes.length,
   'case count drift');
  const detMap=new Map();
  for(const d of m.detections){
   ck(!detMap.has(d.id)&&!allIDs.has(d.id),'duplicate detection ID');
   ck(Number.isFinite(d.confidence)&&d.confidence>=0.2&&d.confidence<=1,
    'invalid score');
   detMap.set(d.id,d);allIDs.add(d.id);
  }
  const people=m.detections.filter(d=>d.cls==='Persons');
  ck(people.length===m.counts.persons, 'missing person detection');
  const personIDs=new Set(people.map(x=>x.id));
  ck(g.per_person_candidate_review.length===people.length &&
   g.per_person_candidate_review.every(x=>personIDs.has(x.person_detection_id) &&
    x.person_human_coverage_confirmed===false &&
    x.worker_compliance_status==='NOT_ESTIMABLE_POLICY_AND_HUMAN_EVIDENCE_MISSING'),
   'person candidate improperly verified');
  const seen=new Set();
  const policyItems=g.per_item_candidate_review.map(it=>{
   const d=detMap.get(it.item_detection_id);
   ck(d&&!seen.has(it.item_detection_id)&&d.cls===it.detector_class &&
    d.confidence===it.confidence && geometryStates.has(it.geometry_status) &&
    it.workplace_requirement==='POLICY_UNKNOWN' &&
    it.clearance_or_violation_decision===null &&
    it.human_confirmed_owner_id===null &&
    it.human_verified_visual_state===null &&
    ['POSITIVE','NEGATIVE_MARKER'].includes(it.cue_sense) &&
    ['HIGH','LOW_REVIEW'].includes(it.confidence_band) &&
    it.confidence_band===(d.confidence>=0.60?'HIGH':'LOW_REVIEW'),
    'specific cue changed, human verdict introduced, or confidence drift');
   seen.add(it.item_detection_id);
   const candidate=it.single_strong_candidate_person_detection_id;
   const single=it.geometry_status==='SINGLE_STRONG_GEOMETRIC_CANDIDATE_REVIEW_ONLY';
   ck((candidate===null&&!single) || (single&&personIDs.has(candidate)),
    'geometry candidate not within the same image');
   ck(it.candidate_people.every(x=>personIDs.has(x.person_detection_id)),
    'person cue crossing source images');
   const why=['TASK_POLICY_UNKNOWN','HUMAN_PERSON_COVERAGE_UNVERIFIED'];
   if(!single)why.push('PERSON_EQUIPMENT_ASSOCIATION_UNRESOLVED');
   if(it.confidence_band==='LOW_REVIEW')why.push('LOW_DETECTOR_CONFIDENCE');
   if(it.cue_sense==='NEGATIVE_MARKER')why.push('NEGATIVE_CLASS_IS_NOT_PROOF_OF_ABSENCE');
   return {
    item_detection_id:it.item_detection_id,
    original_detector_class:it.detector_class,
    confidence:it.confidence,
    ppe_type:it.ppe_type,
    detector_cue_sense:it.cue_sense,
    tentative_geometric_owner_detection_id:candidate,
    geometry_review_status:it.geometry_status,
    A0_original_detector_only:{
     cue_id:it.item_detection_id,output:'RAW_MODEL_CUE_NO_COMPLIANCE_DECISION',
     human_review_dispatched:false,xai_calls_executed:0,worker_clearance:null
    },
    A5_offline_SEER_policy_proposal:{
     input_cue_id:it.item_detection_id,
     proposed_route:'ABSTAIN_AND_SUGGEST_HUMAN_REVIEW_NOT_DISPATCHED',
     reasons:why,worker_clearance:null,violation_verdict:null,
     human_review_dispatched:false,explanation_produced:false,
     xai_calls_executed:0
    }
   };
  });
  ck(seen.size===g.counts.specific_ppe_candidates,'typed cue conservation failed');
  const context=m.detections.filter(d=>d.cls!=='Persons'&&!seen.has(d.id));
  ck(context.length===g.counts.context_only_not_specific_ppe,
   'context count drift');
  ck(context.every(x=>['No Safety Attire','Pants','Soft Hat','Animal','Child'].includes(x.cls)),
   'unregistered PPE class was silently discarded as context');
  ck(g.counts.single_geometric_owner_proposals===
   policyItems.filter(x=>x.geometry_review_status==='SINGLE_STRONG_GEOMETRIC_CANDIDATE_REVIEW_ONLY').length &&
   g.counts.ambiguous_or_unassigned_specific_ppe===
    policyItems.filter(x=>x.geometry_review_status!=='SINGLE_STRONG_GEOMETRIC_CANDIDATE_REVIEW_ONLY').length,
   'provisional owner counts disagree');
  if(m.case==='D')ck(people.length===0&&policyItems.length===1&&
    policyItems[0].tentative_geometric_owner_detection_id===null &&
    m.workflow_review_codes.person_coverage==='PERSON_COVERAGE_UNKNOWN',
    'D no-person must never be cleared or assigned');
  cases.push({
   case:m.case,case_id:m.case_id,source_split:'train',
   shared_real_V16_inference_id:m.inference_id,
   raw_detected_boxes:m.counts.raw,
   detector_person_candidates:people.length,
   typed_ppe_review_suggestions:policyItems.length,
   context_boxes_not_ppe:context.length,
   coverage_status:'PERSON_COVERAGE_UNVERIFIED',
   A0_baseline:{
    view:'ORIGINAL_FROZEN_DETECTOR_NUMERIC_OUTPUT_NO_POLICY',
    raw_detection_ids:m.detections.map(d=>d.id),
    worker_compliance_verdicts:0,
    scene_safe_clearances:0,xai_calls_executed_by_v17:0
   },
   A5_SEER_offline_proposal:{
    view:'POST_DETECTION_POLICY_SIMULATION_NO_NEW_INFERENCE',
    person_candidate_ids:people.map(x=>x.id),
    context_only_ids:context.map(x=>x.id),
    typed_cues:policyItems,
    human_review_suggestions_not_submitted:policyItems.length,
    scene_coverage_review_suggested_not_submitted:true,
    compliance_verdicts:0,scene_safe_clearances:0,
    review_requests_actually_dispatched:0,xai_calls_executed_by_v17:0
   }
  });
 }
 cases.sort((a,b)=>a.case.localeCompare(b.case));
 const total=(key)=>cases.reduce((sum,c)=>sum+c[key],0);
 ck(total('raw_detected_boxes')===51 && total('detector_person_candidates')===7 &&
   total('typed_ppe_review_suggestions')===38 && total('context_boxes_not_ppe')===6 &&
   geom.totals.detection_candidates===51 && geom.totals.person_candidates===7 &&
   geom.totals.specific_ppe_candidates===38 &&
   geom.totals.single_geometric_owner_proposals===34 &&
   geom.totals.ambiguous_or_unassigned_specific_ppe===4,
   'historical original model cue totals drift');
 return {
  schema_version:'seer-ppe/paired-train-detector-input-policy-offline-preflight/v0.17',
  date:'2026-11-21',
  execution_type:'DETERMINISTIC_OFFLINE_TRACE_FROM_EXISTING_REAL_V16_TRAIN_PREDICTIONS',
  input_file_sha256:Object.fromEntries(Object.entries(files).map(([k,v])=>[k,sha(v)])),
  original_model_id:raw.model_id,source_workflow_id:raw.workflow_id,
  comparators:{
   A0:'FIXED_RFDETR_RAW_OUTPUT_NO_SAFETY_POLICY',
   A5:'CONSERVATIVE_SEER_POST_DETECTION_POLICY_DRY_RUN_ONLY'
  },
  eligible_scientific_validation_source_images:0,
  technically_matched_original_to_clean17_valid_images:459,
  runtime_human_reference_loaded_as_routing_feature:false,
  signed_human_item_assignments_created:0,
  detector_inference_calls_new_in_v17:0,
  XAI_calls_new_in_v17:0,human_review_requests_dispatched:0,
  original_model_or_labels_modified:false,
  protected_test_read_or_used:false,validation_inference_performed:false,
  paired_benefit_or_safety_superiority_measured:false,
  accuracy_F1_mAP_computed:false,explanation_faithfulness_measured:false,
  electrical_energy_joules_measured:null,
  comparator_primary_not_yet_selected:true,
  validation_policy_frozen:false,scoring_ready:false,
  totals:{
   real_original_train_images_reused:4,
   raw_model_detections:51,
   person_box_candidates_not_verified_people:7,
   typed_ppe_cues_review_suggested_not_sent:38,
   geometry_single_owner_proposals_not_verified:34,
   ambiguous_or_unassigned_ppe:4,
   context_only_detections:6,
   scene_coverage_uncertain:4,
   worker_compliance_verdicts:0,
   unsafe_scene_clearances:0
  },
  cases
 };
}
function test(){
 const raw=read(files.raw),geom=read(files.geometry),
  valid=read(files.readiness),freeze=read(files.freeze);
 const o=trace(raw,geom,valid,freeze);
 assert.equal(o.totals.raw_model_detections,51);
 assert.equal(o.totals.typed_ppe_cues_review_suggested_not_sent,38);
 assert.equal(o.totals.person_box_candidates_not_verified_people,7);
 assert.equal(o.scoring_ready,false);
 assert.ok(o.cases.every(c=>c.A5_SEER_offline_proposal.compliance_verdicts===0));
 assert.ok(o.cases.every(c=>c.A5_SEER_offline_proposal.typed_cues.every(q=>
   q.A0_original_detector_only.cue_id===q.A5_offline_SEER_policy_proposal.input_cue_id)));
 const testInput=structuredClone(raw);testInput.cases[0].source_split='test';
 assert.throws(()=>trace(testInput,geom,valid,freeze));
 const forgedCoverage=structuredClone(geom);forgedCoverage.cases[3].human_scene_person_coverage_signed=true;
 assert.throws(()=>trace(raw,forgedCoverage,valid,freeze));
 const forgedClearance=structuredClone(geom);
 forgedClearance.cases[2].per_item_candidate_review[0].clearance_or_violation_decision='COMPLIANT';
 assert.throws(()=>trace(raw,forgedClearance,valid,freeze));
 const invalidSource=structuredClone(valid);invalidSource.per_image_source_family_human_decisions_signed=1;
 assert.throws(()=>trace(raw,geom,invalidSource,freeze));
 const invalidFreeze=structuredClone(freeze);invalidFreeze.authorized=true;
 assert.throws(()=>trace(raw,geom,valid,invalidFreeze));
 const low=structuredClone(geom);
 const item=low.cases[1].per_item_candidate_review.find(x=>x.confidence_band==='LOW_REVIEW');
 assert.ok(item);item.confidence_band='HIGH';
 assert.throws(()=>trace(raw,low,valid,freeze));
 const d=o.cases.find(x=>x.case==='D');
 assert.equal(d.detector_person_candidates,0);
 assert.equal(d.A5_SEER_offline_proposal.typed_cues[0].tentative_geometric_owner_detection_id,null);
 console.log('SEER_V17_SYNTHETIC_TEST_SPLIT_POLICY_SIGNOFF_AND_COVERAGE_FAIL_CLOSED_PASS');
}
try{
 const arg=process.argv[2]??'--audit';
 if(arg==='--self-test')test();
 else if(arg==='--audit'){
  const output=trace(read(files.raw),read(files.geometry),read(files.readiness),read(files.freeze));
  if(process.argv[3])writeFileSync(process.argv[3],JSON.stringify(output,null,2)+'\n');
  console.log(JSON.stringify({totals:output.totals,scoring_ready:output.scoring_ready,
   explanation_calls:output.XAI_calls_new_in_v17},null,2));
  console.log('SEER_V17_PAIRED_TRAIN_OFFLINE_NOT_SCIENTIFIC_SCORE_PASS');
 }else throw Error('Usage: --self-test | --audit [output_file]');
}catch(e){console.error(String(e));process.exitCode=2;}
