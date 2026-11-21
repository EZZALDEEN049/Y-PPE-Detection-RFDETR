#!/usr/bin/env node
/**
 * V25: ACTUALLY EXECUTE the frozen A0/A2/A5 post-detector decision
 * algorithm on saved, real original RF-DETR outputs: 4 Train + 5 historically
 * exposed original Valid Source images. No new model inference, no Test, no
 * XAI, no actual review dispatch or worker-level compliance adjudication.
 *
 * Mandatory safety invariants apply IDENTICALLY to A2 and A5. Differences
 * are priority/selection only; their matched proposal budgets are NOT
 * measured resource savings or proof of worker-safety benefit.
 */
import assert from 'node:assert/strict';
import {readFileSync,writeFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import {resolve} from 'node:path';
import {fileURLToPath} from 'node:url';

const ROOT=resolve(fileURLToPath(new URL('..',import.meta.url)));
const input={
 train:'ROBOFLOW_TRAIN_ONLY_REAL_MODEL_PREFLIGHT_2026-11-21_V16.json',
 valid:'VALID_ORIGINAL_SOURCE_CURRENT_BBOX_MODEL_PILOT_V23.json',
 validMatch:'VALID_CURRENT_SOURCE_REAL_MODEL_BOX_MATCH_V23.json',
 protocol:'V25_A2_A5_PAIRED_ROUTING_PROTOCOL_FROZEN_2026-11-21.md'
};
const read=name=>JSON.parse(readFileSync(resolve(ROOT,name),'utf8'));
const sha=name=>createHash('sha256').update(readFileSync(resolve(ROOT,name))).digest('hex');
const need=(ok,why)=>{if(!ok)throw Error('SEER_V25_PAIRED_ROUTING_BLOCKED:'+why)};
const model='altayyar-0oflt-lafos-qqauz/2';
const PERSON='Persons';
const POS=new Set(['Hard Hat','Safety Vests','Safety Boots','Gloves','Goggles','Face Masks']);
const NEG=new Set(['No Hard Hat','No Safety Vest','No Safety Boots','No Gloves',
  'No Face Mask','No Safety Attire']);
const CONTEXT=new Set(['Pants','Soft Hat','Animal','Child']);
const CUES=new Set([...POS,...NEG]);
const CLASSES=new Set([PERSON,...CUES,...CONTEXT]);
need(CLASSES.size===17 && POS.size===6 && NEG.size===6 && CONTEXT.size===4,
  'original RF-DETR 17-class mapping violated');
const SEVERITY={
 'Hard Hat':0.12,'No Hard Hat':0.12,
 'Safety Boots':0.10,'No Safety Boots':0.10,
 'Safety Vests':0.08,'No Safety Vest':0.08,'No Safety Attire':0.08,
 'Goggles':0.08,
 'Gloves':0.04,'No Gloves':0.04,
 'Face Masks':0.03,'No Face Mask':0.03
};
const FROZEN={
 confidence_floor:0.2,
 hosted_overlap:0.5,
 per_image_max_proposed_explanations:1,
 per_image_max_proposed_reviews:1,
 negative_cue_priority_bonus:0.26,
 unresolved_association_priority_bonus:0.24,
 ambiguous_if_containment_margin_below:0.15
};
const SOURCEIDS=[
 '07BnOpgFJyNaOhuzvh5i','084u5kuwQXhWa4EKdsQ5',
 '09WO3iVNf9jOt21QAxmb','0ABzMrjnd6I0Ws6FH7qo','0aGYjxE5LmocXyvuLHs8'
];
const round=n=>Number(n.toFixed(6));
const number=n=>typeof n==='number'&&Number.isFinite(n);
function corners(b){
 const x1=b.x-b.width/2,y1=b.y-b.height/2;
 return [x1,y1,b.x+b.width/2,b.y+b.height/2];
}
function region(cls){
 if(['Hard Hat','No Hard Hat','Goggles','Face Masks','No Face Mask'].includes(cls))return [0,0.48];
 if(['Safety Vests','No Safety Vest','No Safety Attire'].includes(cls))return [0.13,0.87];
 if(['Gloves','No Gloves'].includes(cls))return [0.25,0.92];
 if(['Safety Boots','No Safety Boots'].includes(cls))return [0.62,1];
 throw Error('Unhandled typed PPE class '+cls);
}
function intersectionFractionOfCue(cue,person){
 const a=corners(cue),b=corners(person);
 const width=Math.max(0,Math.min(a[2],b[2])-Math.max(a[0],b[0]));
 const height=Math.max(0,Math.min(a[3],b[3])-Math.max(a[1],b[1]));
 return width*height/(cue.width*cue.height);
}
function associate(cue,persons){
 if(persons.length===0)return {
  status:'PERSON_CANDIDATE_NOT_DETECTED',
  tentative_person_id:null,eligible_person_candidates:0,
  best_containment:null,top_two_containment_margin:null
 };
 const r=region(cue.cls);
 const eligible=persons.filter(p=>{
  const a=corners(p);
  const inBox=cue.x>=a[0]&&cue.x<=a[2]&&cue.y>=a[1]&&cue.y<=a[3];
  const vertical=(cue.y-a[1])/p.height;
  return inBox && vertical>=r[0]-1e-10 && vertical<=r[1]+1e-10;
 }).map(p=>({id:p.id,confidence:p.confidence,frac:intersectionFractionOfCue(cue,p)}))
 .sort((a,b)=>b.frac-a.frac||b.confidence-a.confidence||a.id.localeCompare(b.id));
 if(eligible.length===0)return {
  status:'ASSOCIATION_UNKNOWN',tentative_person_id:null,
  eligible_person_candidates:0,best_containment:null,top_two_containment_margin:null
 };
 if(eligible.length===1)return {
  status:'TENTATIVE_SINGLE',tentative_person_id:eligible[0].id,
  eligible_person_candidates:1,best_containment:round(eligible[0].frac),
  top_two_containment_margin:null
 };
 const margin=eligible[0].frac-eligible[1].frac;
 const distinct=margin+1e-10>=FROZEN.ambiguous_if_containment_margin_below;
 return {
  status:distinct?'TENTATIVE_MARGIN':'ASSOCIATION_AMBIGUOUS',
  tentative_person_id:distinct?eligible[0].id:null,
  eligible_person_candidates:eligible.length,
  best_containment:round(eligible[0].frac),
  top_two_containment_margin:round(margin)
 };
}
const unresolved=status=>!['TENTATIVE_SINGLE','TENTATIVE_MARGIN'].includes(status);

function normalize(train,valid){
 need(train.schema_version==='seer-ppe/train-only-real-roboflow-preflight/v0.16'&&
   train.model_id===model&&train.model_modified===false&&
   train.model_retrained===false&&train.dataset_images_or_labels_modified===false&&
   train.test_inputs_used===0&&train.validation_inputs_used===0&&
   train.scoring_ready===false&&Array.isArray(train.cases)&&train.cases.length===4,
   'V16 Train source/model/split/protection mismatch');
 need(valid.schema_version==='seer-ppe/actual-hosted-valid-pilot-current-original-gt-pred-bboxes/v0.23'&&
   valid.model_id===model&&valid.source_project==='softyyemen/altayyar-0oflt-lafos-qqauz'&&
   valid.selected_image_count===5&&valid.new_hosted_inference_count===5&&
   valid.no_test_accessed===true&&valid.original_images_annotations_and_splits_untouched===true&&
   valid.original_model_unchanged===true&&valid.scientific_independent_validation===false&&
   valid.person_level_PPE_compliance_measured===false&&valid.scoring_ready===false&&
   JSON.stringify(valid.selection_predeclared_ids)===JSON.stringify(SOURCEIDS)&&
   Array.isArray(valid.rows)&&valid.rows.length===5,
   'V23 original Valid source/model/split/actual output incorrect');
 const imgs=[];
 const trCounts={A:5,B:16,C:29,D:1};
 for(let i=0;i<4;i++){
  const c=train.cases[i],key=['A','B','C','D'][i];
  need(c.case===key&&c.source_split==='train'&&c.model_id===model&&
    c.counts?.raw===trCounts[key]&&c.detections?.length===trCounts[key]&&
    c.image_dimensions?.width>0&&c.image_dimensions?.height>0&&
    c.person_coverage_verified_by_human===false&&
    c.no_test_media===true&&
    c.used_as_scientific_score===false,
    'Train original image identity, safety state or detections changed');
  imgs.push({
   image_key:'train:'+c.case,case:c.case,split:'train',filename:c.filename,
   w:c.image_dimensions.width,h:c.image_dimensions.height,
   historical_development_exposure:true,
   detections:c.detections.map(d=>({
    id:d.id,cls:d.cls,confidence:d.confidence,x:d.x,y:d.y,
    width:d.width,height:d.height
   }))
  });
 }
 for(let i=0;i<5;i++){
  const c=valid.rows[i];
  need(c.source_id===SOURCEIDS[i]&&c.split==='valid'&&
    c.model_id===model&&c.confidence_floor===FROZEN.confidence_floor&&
    c.overlap_parameter===FROZEN.hosted_overlap&&
    c.annotation_valid===true&&c.image_width>0&&c.image_height>0&&
    c.selection==='LEXICOGRAPHIC_FIRST_5_FROM_M2_UNFLAGGED_NOT_CERTIFIED',
    'V23 Valid original Source ID/shape/settings changed');
  // Deliberately do not read current_author_labels here:
  // routing is independent of ALL ground-truth labels or outcomes.
  imgs.push({
   image_key:'valid:'+c.source_id,split:'valid',filename:c.original_filename,
   source_id:c.source_id,w:c.image_width,h:c.image_height,
   historical_development_exposure:true,
   detections:c.predictions.map(d=>({
    id:d.id,cls:d.class_name,confidence:d.confidence,x:d.x,y:d.y,
    width:d.width,height:d.height
   }))
  });
 }
 const keys=new Set();
 for(const im of imgs){
  need(!keys.has(im.image_key),'duplicate image ID');keys.add(im.image_key);
  need(im.split!=='test'&&im.historical_development_exposure===true&&
    typeof im.filename==='string'&&im.filename.length>0&&
    im.w>0&&im.h>0&&Array.isArray(im.detections)&&im.detections.length>0,
    'invalid image, Test access or false independence');
  const predIds=new Set();
  for(const d of im.detections){
   need(typeof d.id==='string'&&d.id.length>0&&!predIds.has(d.id)&&
    CLASSES.has(d.cls)&&number(d.confidence)&&d.confidence>=FROZEN.confidence_floor&&
    d.confidence<=1&&[d.x,d.y,d.width,d.height].every(number)&&
    d.width>0&&d.height>0&&
    d.x>=0&&d.y>=0&&d.x<=im.w&&d.y<=im.h,
    'prediction missing, duplicate, wrong class, invalid geometry or below floor');
   predIds.add(d.id);
  }
 }
 need(imgs.length===9&&imgs.filter(x=>x.split==='train').length===4&&
   imgs.filter(x=>x.split==='valid').length===5&&
   imgs.reduce((n,x)=>n+x.detections.length,0)===74,
   'must reuse exactly 51 Train and 23 Valid real detections');
 return imgs;
}
function rankedPolicy(im,arm){
 need(['A2','A5'].includes(arm),'comparison arm invalid');
 const person=im.detections.filter(x=>x.cls===PERSON);
 const cue=im.detections.filter(x=>CUES.has(x.cls)).map(d=>{
  const a=associate(d,person),uncertainty=1-d.confidence;
  const score=arm==='A2'?uncertainty:
    uncertainty+(NEG.has(d.cls)?FROZEN.negative_cue_priority_bonus:0)+
    (unresolved(a.status)?FROZEN.unresolved_association_priority_bonus:0)+
    SEVERITY[d.cls];
  need(number(score),'priority score invalid');
  return {
   detection_id:d.id,original_class:d.cls,confidence:round(d.confidence),
   model_uncertainty:round(uncertainty),
   negative_named_cue:NEG.has(d.cls),
   safety_severity_weight_unvalidated:SEVERITY[d.cls],
   association:a,
   fixed_priority_proxy:round(score),
   rank_sort_value:score,
   person_PPE_visual_state:'NOT_ADJUDICATED',
   site_task_requirement:'POLICY_UNKNOWN',
   worker_compliance_verdict:null,
   verified_violation_verdict:null,
   cue_resolution:'PENDING_EVIDENCE_NOT_CLEARED'
  };
 });
 const ranks=cue.sort((a,b)=>b.rank_sort_value-a.rank_sort_value||
   a.detection_id.localeCompare(b.detection_id));
 const chosen=ranks[0]??null;
 const select=chosen?.detection_id??null;
 const rows=ranks.map(({rank_sort_value,...d},i)=>({
  ...d,rank:i+1,
  proposed_explanation_not_executed:d.detection_id===select,
  proposed_review_not_dispatched:d.detection_id===select
 }));
 const n=Number(select!==null);
 need(n<=FROZEN.per_image_max_proposed_explanations&&
   n<=FROZEN.per_image_max_proposed_reviews,'budget overrun');
 const people=person.map(p=>({
  detection_id:p.id,
  visual_person_coverage:'PERSON_COVERAGE_UNVERIFIED',
  worker_compliance_verdict:null,
  verified_violation_verdict:null,
  human_reference_loaded_as_feature:false
 }));
 return {
  arm,route_algorithm_executed:true,source_image_key:im.image_key,
  detected_person_candidates:people,
  detected_person_candidate_count:person.length,
  person_coverage_status:'PERSON_COVERAGE_UNVERIFIED',
  task_policy_status:'POLICY_UNKNOWN',
  scene_safe_clearance:null,verified_scene_violation:null,
  action_confirmed:false,actual_review_dispatched:false,
  actual_xai_executed:false,additional_model_inferences_executed:0,
  proposed_explanation_requests:n,proposed_review_items:n,
  explanation_target_detection_id:select,review_target_detection_id:select,
  per_image_max_proposed_explanations:FROZEN.per_image_max_proposed_explanations,
  per_image_max_proposed_reviews:FROZEN.per_image_max_proposed_reviews,
  pending_unselected_cues:rows.length-n,
  ppe_cues_with_no_automatic_clearance:rows.length,
  ranked_cues:rows
 };
}
function verifyPolicy(r,im){
 const cues=im.detections.filter(x=>CUES.has(x.cls)).length;
 need(r.person_coverage_status==='PERSON_COVERAGE_UNVERIFIED'&&
   r.task_policy_status==='POLICY_UNKNOWN'&&
   r.scene_safe_clearance===null&&r.verified_scene_violation===null&&
   r.action_confirmed===false&&r.actual_review_dispatched===false&&
   r.actual_xai_executed===false&&r.additional_model_inferences_executed===0&&
   r.detected_person_candidates.every(p=>p.worker_compliance_verdict===null&&
     p.verified_violation_verdict===null&&p.human_reference_loaded_as_feature===false)&&
   r.ranked_cues.every(c=>c.worker_compliance_verdict===null&&
     c.verified_violation_verdict===null&&c.site_task_requirement==='POLICY_UNKNOWN'&&
     c.person_PPE_visual_state==='NOT_ADJUDICATED'&&
     c.cue_resolution==='PENDING_EVIDENCE_NOT_CLEARED')&&
   r.proposed_explanation_requests===r.proposed_review_items&&
   r.proposed_explanation_requests===Number(cues>0)&&
   r.pending_unselected_cues===cues-Number(cues>0),
   'unsafe auto-clearance, review dispatch, XAI execution, uncoded case or unequal budget');
}
function objectDiagnostic(paired,validMatch){
 // IMPORTANT: this result is joined AFTER policy routing; NEVER a ranking
 // feature. V23 detected FP is object-level, NOT confirmed human PPE hazard.
 need(validMatch.schema_version==='seer-ppe/v23-actual-current-label-five-valid-descriptive-box-match/v0.23'&&
   validMatch.original_model_id===model&&
   validMatch.new_real_hosted_inference_calls===5&&
   validMatch.worker_safety_compliance_scored===false&&
   validMatch.source_pilot_box_match.tp===22&&
   validMatch.source_pilot_box_match.fp===1&&
   validMatch.source_pilot_box_match.fn===1&&
   validMatch.test_source_or_evaluation_accessed===false,
   'separate V23 objective matching provenance mismatched');
 const outcomes=new Map();
 for(const image of validMatch.per_source){
  const rows=new Map(image.matched_pred_events.map(x=>[x.pred_id,x.status]));
  need(rows.size===image.model_prediction_boxes,'V23 detection outcome duplicate');
  outcomes.set('valid:'+image.source_id,rows);
 }
 const perImage=paired.filter(x=>x.split==='valid').map(x=>{
  const a2=x.A2.explanation_target_detection_id,a5=x.A5.explanation_target_detection_id;
  const r=outcomes.get(x.image_key);
  need(r && (!a2||r.has(a2)) && (!a5||r.has(a5)),
    'post-routing object matching join failed');
  return {
   original_valid_source_id:x.source_id,filename:x.filename,
   A2_chosen_pred_id:a2,A2_chosen_object_level_match_status:a2?r.get(a2):null,
   A5_chosen_pred_id:a5,A5_chosen_object_level_match_status:a5?r.get(a5):null
  };
 });
 return {
  method:'POST_ROUTING_GT_JOIN_AS_DESCRIPTIVE_OBJECT_FP_DIAGNOSTIC_ONLY',
  used_for_policy_priority_or_calibration:false,worker_level_false_clearance_evaluable:false,
  A2_selected_known_current_ref_FP_count:perImage.filter(x=>x.A2_chosen_object_level_match_status==='FP').length,
  A5_selected_known_current_ref_FP_count:perImage.filter(x=>x.A5_chosen_object_level_match_status==='FP').length,
  caveat:'Object FP selection does not measure worker violation, false-safe clearance, reviewer confirmation, explanation fidelity or representativeness; only ONE FP occurs in 5 V23 Valid photos.',
  per_original_valid_image:perImage
 };
}
function run(train,valid,validMatch){
 const imgs=normalize(train,valid);
 const out=imgs.map(im=>{
  const p=im.detections.filter(d=>d.cls===PERSON).length;
  const context=im.detections.filter(d=>CONTEXT.has(d.cls)).length;
  const cues=im.detections.filter(d=>CUES.has(d.cls)).length;
  need(p+cues+context===im.detections.length,'original classes lost');
  const A2=rankedPolicy(im,'A2'),A5=rankedPolicy(im,'A5');
  verifyPolicy(A2,im);verifyPolicy(A5,im);
  return {
   image_key:im.image_key,source_id:im.source_id??null,
   original_filename:im.filename,split:im.split,
   previously_development_exposed:true,
   source_independence_proven:false,
   original_detector_boxes:im.detections.length,
   detected_person_candidates:p,typed_PPE_cues:cues,context_boxes:context,
   A0_original_fixed_model:{
    raw_detector_boxes:im.detections.length,
    original_model_id:model,
    additional_explanations_or_reviews_executed:0,
    worker_safety_policy_applied:false,
    verified_worker_clearances:0
   },
   A2,A5,
   both_policies_chose_same_target:
     A2.explanation_target_detection_id===A5.explanation_target_detection_id,
   both_policies_selective_proposals_equal_budgets:
     A2.proposed_explanation_requests===A5.proposed_explanation_requests&&
     A2.proposed_review_items===A5.proposed_review_items
  };
 });
 const sum=name=>out.reduce((s,r)=>s+r[name],0);
 need(sum('original_detector_boxes')===74,'original boxes changed');
 const total=(arm,key)=>out.reduce((n,r)=>n+r[arm][key],0);
 const aggregate={
  images:9,Train_images:4,historically_exposed_original_Valid_images:5,
  original_detector_boxes:74,
  detected_person_box_candidates:sum('detected_person_candidates'),
  typed_PPE_detection_cues:sum('typed_PPE_cues'),
  non_PPE_context_boxes:sum('context_boxes'),
  images_with_no_person_detection:out.filter(x=>x.detected_person_candidates===0).length,
  images_with_no_typed_PPE_cue:out.filter(x=>x.typed_PPE_cues===0).length,
  A2_proposed_XAI_requests_NOT_executed:total('A2','proposed_explanation_requests'),
  A5_proposed_XAI_requests_NOT_executed:total('A5','proposed_explanation_requests'),
  A2_proposed_review_items_NOT_dispatched:total('A2','proposed_review_items'),
  A5_proposed_review_items_NOT_dispatched:total('A5','proposed_review_items'),
  A2_pending_unselected_cues:total('A2','pending_unselected_cues'),
  A5_pending_unselected_cues:total('A5','pending_unselected_cues'),
  image_target_agreements_including_no_cue:out.filter(x=>x.both_policies_chose_same_target).length,
  image_target_disagreements:out.filter(x=>!x.both_policies_chose_same_target).length,
  proposed_request_budget_matched_for_every_image:out.every(x=>x.both_policies_selective_proposals_equal_budgets),
  original_model_calls_additional_in_V25:0,
  actual_XAI_calls_in_V25:0,
  actual_human_review_dispatched_in_V25:0,
  actual_worker_safe_clearances_in_V25:0,
  verified_worker_violations_in_V25:0,
  confirmed_review_actions_in_V25:0,
  externally_independent_source_group_results:0
 };
 need(aggregate.detected_person_box_candidates+aggregate.typed_PPE_detection_cues+
  aggregate.non_PPE_context_boxes===74&&
  aggregate.A2_proposed_XAI_requests_NOT_executed===
   aggregate.A5_proposed_XAI_requests_NOT_executed&&
  aggregate.proposed_request_budget_matched_for_every_image&&
  aggregate.actual_worker_safe_clearances_in_V25===0,
  'A0 original conservation, matched selective budgets or safety breach');
 const result={
  schema_version:'seer-ppe/v25-real-saved-prediction-A2-A5-safety-matched-offline-routing/v0.25',
  date:'2026-11-21',
  executed_algorithm:'DETERMINISTIC_OFFLINE_POST_DETECTION_ROUTING_ON_REAL_SAVED_FIXED_RFDETR_OUTPUTS',
  model_id:model,
  inputs_sha256:Object.fromEntries(Object.entries(input).map(([k,v])=>[k,sha(v)])),
  fixed_engineering_parameters:FROZEN,
  routing_uses_current_author_annotations_as_features:false,
  routing_uses_groundtruth_detection_errors_as_features:false,
  safety_guards_identical_A2_A5:true,
  original_model_retrained_or_modified:false,
  source_images_annotations_splits_modified:false,
  no_test_or_external_holdout_used:true,
  no_new_hosted_inference_performed:true,
  no_real_XAI_or_human_review_executed:true,
  matched_budgets_for_proposals_not_actual_compute:true,
  source_independence_certified:false,
  actual_person_level_compliance_efficacy_measured:false,
  explanation_faithfulness_measured:false,
  actual_electric_joules_measured:false,
  SEER_safety_or_energy_superiority_supported:false,
  strong_real_world_uncertainty_gated_comparator_still_pending:true,
  strict_scientific_worker_safety_scoring_ready:false,
  aggregate,paired_images:out,
  post_route_object_FP_alignment_probe:objectDiagnostic(out,validMatch),
  scientific_interpretation:'A2 confidence-only and A5 risk-proxy algorithms were executed on 74 saved real original-model detections with equal proposed explanation/review slots and the same abstention; outcomes are routing IDs and queue PROPOSALS, not actually performed XAI/reviews, worker violation labels, latency, cost or safety improvement.'
 };
 return result;
}
function selfTest(){
 const data=[read(input.train),read(input.valid),read(input.validMatch)];
 const good=run(...data);
 assert.equal(good.aggregate.images,9);
 assert.equal(good.aggregate.original_detector_boxes,74);
 assert.equal(good.aggregate.actual_worker_safe_clearances_in_V25,0);
 assert.equal(good.aggregate.actual_XAI_calls_in_V25,0);
 assert(good.aggregate.proposed_request_budget_matched_for_every_image);
 assert.deepEqual(run(...data),good,'execution is deterministic');
 const mutated=structuredClone(data[1]);
 mutated.rows[0].current_author_labels=[{annotation_id:'FAKE_REFERENCE_IS_NOT_FEATURE'}];
 assert.deepEqual(run(data[0],mutated,data[2]).paired_images,good.paired_images,
   'author GT accidentally leaked into model policy inputs');
 const bad=structuredClone(data[0]);bad.model_id='changed-model';
 assert.throws(()=>run(bad,data[1],data[2]));
 const bad2=structuredClone(data[1]);bad2.rows[0].split='test';
 assert.throws(()=>run(data[0],bad2,data[2]));
 const bad3=structuredClone(data[0]);bad3.cases[0].detections[0].confidence=0.01;
 assert.throws(()=>run(bad3,data[1],data[2]));
 const s={image_key:'synthetic',detections:[
  {id:'p',cls:'Hard Hat',confidence:0.9,x:30,y:30,width:20,height:20}
 ]};
 const noPerson=rankedPolicy(s,'A5');
 assert.equal(noPerson.ranked_cues[0].association.status,'PERSON_CANDIDATE_NOT_DETECTED');
 assert.equal(noPerson.scene_safe_clearance,null);
 assert.equal(noPerson.actual_review_dispatched,false);
 const noCue=rankedPolicy({image_key:'s',detections:[{
  id:'none',cls:'Child',confidence:0.9,x:5,y:5,width:4,height:4}]},'A5');
 assert.equal(noCue.proposed_explanation_requests,0);
 assert.equal(noCue.scene_safe_clearance,null);
 const pp=[0,1].map(i=>({id:'person'+i,cls:'Persons',confidence:0.8,
   x:50,y:50,width:100,height:100}));
 const ppe={id:'hat',cls:'Hard Hat',confidence:0.8,x:50,y:20,width:20,height:20};
 const amb=associate(ppe,pp);
 assert.equal(amb.status,'ASSOCIATION_AMBIGUOUS');
 assert.equal(amb.tentative_person_id,null);
 const alt=rankedPolicy({image_key:'s2',detections:[...pp,ppe]},'A5');
 assert.equal(alt.ranked_cues[0].association.status,'ASSOCIATION_AMBIGUOUS');
 assert.equal(alt.ranked_cues[0].worker_compliance_verdict,null);
 assert.equal(alt.scene_safe_clearance,null);
 console.log('SEER_V25_REAL_DETECTIONS_74_SAFETY_BUDGET_PRIORITY_AND_NEGATIVE_CONTROLS_PASS');
}
try{
 const mode=process.argv[2]??'--audit';
 if(mode==='--self-test')selfTest();
 else if(mode==='--audit'){
  const result=run(read(input.train),read(input.valid),read(input.validMatch));
  if(process.argv[3])writeFileSync(process.argv[3],JSON.stringify(result,null,2)+'\n');
  const small={
   aggregate:result.aggregate,
   object_fp_probe:{
    A2:result.post_route_object_FP_alignment_probe.A2_selected_known_current_ref_FP_count,
    A5:result.post_route_object_FP_alignment_probe.A5_selected_known_current_ref_FP_count
   },
   choices:result.paired_images.map(x=>({image:x.image_key,persons:x.detected_person_candidates,
    cues:x.typed_PPE_cues,A2:x.A2.explanation_target_detection_id,
    A5:x.A5.explanation_target_detection_id,agreed:x.both_policies_chose_same_target})),
   original_model_retrained:false,test_used:false,actual_XAI_executed:false,
   worker_safety_compliance_scored:false
  };
  console.log(JSON.stringify(small,null,2));
  console.log('SEER_V25_REAL_FIXED_RFDETR_A0_A2_A5_ROUTING_MATCHED_BUDGETS_PASS');
 }else throw Error('Usage: --self-test | --audit [output.json]');
}catch(e){console.error(String(e));process.exitCode=2;}
