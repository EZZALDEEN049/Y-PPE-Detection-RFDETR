#!/usr/bin/env node
/**
 * SEER-PPE V16.1 — existing human Train reference vs raw model cue directions.
 * Geometrical correspondence only: train pilot QA, NOT a scientific model metric.
 * In particular: "No <PPE>" detector class cannot override human PRESENT.
 */
import assert from 'node:assert/strict';
import {readFileSync,writeFileSync} from 'node:fs';
import {fileURLToPath} from 'node:url';
import {resolve} from 'node:path';
const ROOT=resolve(fileURLToPath(new URL('..',import.meta.url)));
const read=x=>JSON.parse(readFileSync(resolve(ROOT,x),'utf8'));
const QC={A:['8f7cce94-d46e-4fac-9a0a-641bcd1f12c8',2],
 B:['87b6cc58-43bd-4583-8b13-bd9b7413c03d',2],
 C:['c032f81d-64c5-44be-96f3-7e6fe9dad799',4],
 D:['c197d82e-7870-42a3-bf94-462420d3f6a2',1]};
function ck(b,m){if(!b)throw Error('SEER_V16_REFERENCE_DIAGNOSTIC_BLOCKED:'+m);}
function r(x){return Number(x.toFixed(5));}
function validBox(b){return Array.isArray(b)&&b.length===4&&b.every(z=>Number.isFinite(z)&&z>=0&&z<=1)
  &&b[0]<b[2]&&b[1]<b[3];}
function predictedNorm(d,w,h){
 const b=[(d.x-d.width/2)/w,(d.y-d.height/2)/h,(d.x+d.width/2)/w,(d.y+d.height/2)/h];
 ck(validBox(b),'model bbox invalid within source image');
 return b;
}
function iou(a,b){
 const dx=Math.max(0,Math.min(a[2],b[2])-Math.max(a[0],b[0]));
 const dy=Math.max(0,Math.min(a[3],b[3])-Math.max(a[1],b[1]));
 const ar=q=>(q[2]-q[0])*(q[3]-q[1]);
 const int=dx*dy;
 return int/(ar(a)+ar(b)-int);
}
function matchPeople(det,ref,cutoff){
 // Globally optimal max-count then max-IoU one-to-one matching, reproducible ties.
 // This matching is *candidate correspondence*, never person detection mAP or gold.
 const rows=det.map(d=>ref.map(g=>iou(d.box,g.bbox_xyxy_norm)));
 let best={n:-1,sum:-1,key:null,indices:[]};
 function dfs(i,used,chosen,n,sum){
  if(i===det.length){
   const key=chosen.map(x=>x===null?'z':String(x).padStart(2,'0')).join(',');
   if(n>best.n || (n===best.n&&(sum>best.sum+1e-10||
       (Math.abs(sum-best.sum)<1e-10&&(best.key===null||key<best.key)))))
     best={n,sum,key,indices:chosen.slice()};
   return;
  }
  chosen.push(null);dfs(i+1,used,chosen,n,sum);chosen.pop();
  for(let j=0;j<ref.length;j++){
   if(!used.has(j)&&rows[i][j]>=cutoff){
    used.add(j);chosen.push(j);dfs(i+1,used,chosen,n+1,sum+rows[i][j]);
    chosen.pop();used.delete(j);
   }
  }
 }
 dfs(0,new Set(),[],0,0);
 return {pairs:best.indices.flatMap((j,i)=>j===null?[]:[{
  model_person_detection_id:det[i].id,reference_person_id:ref[j].id,
  geometry_iou:r(rows[i][j]),
  human_identity_verified:false,
  matched_for_exploratory_diagnostic_only:true
 }]),unmatched_model:det.length-best.n,unmatched_reference:ref.length-best.n};
}
function run(input,gt,review){
 ck(input.schema_version==='seer-ppe/train-only-real-roboflow-preflight/v0.16','invalid model metadata');
 ck(gt.schema_version==='seer-ppe/live-train-human-gt-read-only-geometry-snapshot/v0.16','reference snapshot changed');
 ck(review.schema_version==='seer-ppe/conservative-geometric-person-ppe-review-proposals/v0.16','review cue schema changed');
 ck(input.cases.length===gt.cases.length&&gt.cases.length===review.cases.length&&review.cases.length===4,'A-D controls missing');
 ck(input.source_eval_dataset_id===gt.eval_dataset_id,'different evaluation datasets');
 ck(gt.existing_researcher_approved_item_owner_links===19&&gt.recorded_visual_states===38&&
 gt.total_visual_states_expected_for_A_B_C===42&&gt.missing_case_B_visual_states===4&&
 gt.case_D_zero_person_human_signed===false&&
 gt.model_prediction_promoted_to_reference===false&&gt.reference_modified===false,
 'current existing researcher reference state changed');
 ck(input.test_inputs_used===0&&input.validation_inputs_used===0&&
 review.developer_test_images===0,'non-Train model inference scope breach');
 const rows=[];
 for(const model of input.cases){
  const q=QC[model.case],human=gt.cases.find(x=>x.case===model.case);
  const cues=review.cases.find(x=>x.case===model.case);
  ck(q&&human&&cues,'case missing in live original-train reference');
  ck(model.source_split==='train'&&human.original_train_source_id?.length>10 &&
     human.case_id===q[0] &&human.case_revision===q[1] &&
     human.ground_truth_state==='incomplete' &&
     model.case_id===q[0]&&cues.case_id===q[0],
     'case identity/revision changed or Validation/Test inserted');
  const priorLinks=human.human_approved_associations.length;
  ck(human.task_mandates.every(p=>p.mandate_status==='POLICY_UNKNOWN'),
     'human policy approval unexpectedly changed');
  for(const person of human.persons)ck(validBox(person.bbox_xyxy_norm),'invalid frozen human bbox');
  const {width:w,height:h}=model.image_dimensions;
  const modelPersons=model.detections.filter(d=>d.cls==='Persons').map(d=>({id:d.id,box:predictedNorm(d,w,h)}));
  const match=matchPeople(modelPersons,human.persons,0.5);
  const modelToRef=new Map(match.pairs.map(x=>[x.model_person_detection_id,x.reference_person_id]));
  const savedVisual=new Map(human.recorded_visual_states.map(x=>[x.person_id+'|'+x.ppe_type,x.visual_state]));
  ck(savedVisual.size===human.recorded_visual_states.length,'duplicate person/PPE reference states');
  const cuelist=cues.per_item_candidate_review.map(x=>{
   const personId=x.single_strong_candidate_person_detection_id ?
       modelToRef.get(x.single_strong_candidate_person_detection_id)??null:null;
   const state=personId?savedVisual.get(personId+'|'+x.ppe_type)??null:null;
   let classification='NO_UNAMBIGUOUS_HUMAN_PERSON_BOX_CORRESPONDENCE';
   if(personId&&!state)classification='HUMAN_VISUAL_STATE_NOT_RECORDED_DO_NOT_INFER';
   else if(personId&&state==='UNKNOWN')classification='HUMAN_VISUAL_STATE_UNKNOWN_NOT_COMPARABLE';
   else if(personId&&state){
    if((x.cue_sense==='NEGATIVE_MARKER'&&state==='PRESENT')||
       (x.cue_sense==='POSITIVE'&&state==='ABSENT'))
      classification='DETECTOR_CUE_OPPOSES_RECORDED_HUMAN_VISUAL_STATE_REVIEW_ONLY';
    else classification='DETECTOR_CUE_DIRECTION_COMPATIBLE_WITH_RECORDED_HUMAN_STATE_NOT_SCORED';
   }
   return {detector_item_id:x.item_detection_id,detector_item_class:x.detector_class,
     detector_confidence:x.confidence,confidence_band:x.confidence_band,
     cue_sense:x.cue_sense,ppe_type:x.ppe_type,
     person_geometry_candidate_id:x.single_strong_candidate_person_detection_id,
     tentative_reference_person_id:personId,
     preexisting_human_visual_state:state,
     non_scoring_diagnostic:classification,
     evidence_quality:'EXPLORATORY_GEOMETRY_AND_EXISTING_HUMAN_REFERENCE',
     ground_truth_overridden:false,model_error_adjudicated_by_human:false,
     compliance_verdict:null};
  });
  const by=(tag)=>cuelist.filter(y=>y.non_scoring_diagnostic===tag).length;
  const opposing=by('DETECTOR_CUE_OPPOSES_RECORDED_HUMAN_VISUAL_STATE_REVIEW_ONLY');
  const missing=by('HUMAN_VISUAL_STATE_NOT_RECORDED_DO_NOT_INFER');
  const uncertain=by('HUMAN_VISUAL_STATE_UNKNOWN_NOT_COMPARABLE');
  const compatible=by('DETECTOR_CUE_DIRECTION_COMPATIBLE_WITH_RECORDED_HUMAN_STATE_NOT_SCORED');
  const unassigned=by('NO_UNAMBIGUOUS_HUMAN_PERSON_BOX_CORRESPONDENCE');
  rows.push({case:model.case,case_id:model.case_id,original_train_source_id:human.original_train_source_id,
   original_train_filename:human.filename,live_reference_revision:human.case_revision,
   existing_approved_human_item_owner_links:priorLinks,
   human_reference_scene_persons:human.persons.length,
   detector_person_candidates:modelPersons.length,
   exploratory_box_alignment:match,
   human_person_identity_correspondence_verified:false,
   model_per_person_cues_human_annotated:false,
   cue_review_counts:{total:cuelist.length,opposing,missing_human_visual:missing,
    human_unknown:uncertain,direction_compatible:compatible,
    no_unambiguous_reference_person_geometry:unassigned},
   case_D_zero_person_researcher_signed:false,
   cue_review_queue:cuelist,model_prediction_promoted_to_ground_truth:false,
   valid_or_test_image_scored:false});
 }
 rows.sort((a,b)=>a.case.localeCompare(b.case));
 ck(rows.reduce((a,c)=>a+c.existing_approved_human_item_owner_links,0)===19,'approved item links drift');
 ck(rows.reduce((a,c)=>a+c.exploratory_box_alignment.pairs.length,0)===7,'model GT person geometry unexpectedly shifted');
 ck(rows.find(x=>x.case==='D').cue_review_counts.no_unambiguous_reference_person_geometry===1,
   'zero detected D case spuriously assigned worker');
 const sums={};
 for(const k of Object.keys(rows[0].cue_review_counts))sums[k]=rows.reduce((a,x)=>a+x.cue_review_counts[k],0);
 ck(sums.total===38,'specific PPE review cue count should be 38');
 ck(sums.opposing+sums.missing_human_visual+sums.human_unknown+
 sums.direction_compatible+sums.no_unambiguous_reference_person_geometry===38,
 'one or more candidate classifications missing');
 return {schema_version:'seer-ppe/exploratory-train-detector-vs-recorded-human-cue-audit/v0.16.1',
  date:'2026-11-21',sample_scope:'EXACTLY_FOUR_EXISTING_TRAIN_CONTROLS_NO_VALID_OR_TEST',
  input_real_roboflow_inferences:4,actual_model_id:'altayyar-0oflt-lafos-qqauz/2',
  original_reference_cases_changed:false,
  historical_human_approved_item_owner_links:19,
  existing_human_visual_states_recorded:38,expected_visual_states:42,
  B_missing_human_states_preserved:4,D_zero_person_human_signed:false,
  exploratory_person_box_alignment_candidates:7,
  human_verified_model_to_reference_person_identity_pairs:0,
  per_item_cue_totals:sums,
  contradiction_counts_are_qualitative_review_queue_not_FPs_or_FNs:true,
  generic_No_Safety_Attire_used_as_specific_absence_label:false,
  policy_applicability_human_certified:false,worker_compliance_scored:false,
  detector_precision_recall_F1_mAP_scored:false,person_item_link_F1_scored:false,
  energy_measured_joules:null,explanation_fidelity_measured:false,
  test_accessed:false,validation_inference_run:false,
  original_model_retrained:false,source_annotations_or_splits_changed:false,
  scientific_scoring_ready:false,cases:rows};
}
function tests(){
 const m=read('ROBOFLOW_TRAIN_ONLY_REAL_MODEL_PREFLIGHT_2026-11-21_V16.json'),
 h=read('TRAIN_ONLY_LIVE_HUMAN_REFERENCE_GEOMETRY_V16.json'),
 p=read('TRAIN_ONLY_PERSON_PPE_GEOMETRIC_REVIEW_V16.json');
 const out=run(m,h,p);
 assert.equal(out.exploratory_person_box_alignment_candidates,7);
 assert.equal(out.historical_human_approved_item_owner_links,19);
 assert.equal(out.per_item_cue_totals.total,38);
 assert.equal(out.scientific_scoring_ready,false);
 const edited=structuredClone(h);edited.cases[2].task_mandates[0].mandate_status='REQUIRED';
 assert.throws(()=>run(m,edited,p),'fabricated PPE site policy should be rejected');
 const wrongRev=structuredClone(h);wrongRev.cases[1].case_revision=8;
 assert.throws(()=>run(m,wrongRev,p));
 const guessed=structuredClone(p);guessed.cases[3].per_item_candidate_review[0].single_strong_candidate_person_detection_id=m.cases[0].detections.find(d=>d.cls==='Persons').id;
 const out2=run(m,h,guessed);
 assert.equal(out2.cases.find(x=>x.case==='D').cue_review_counts.no_unambiguous_reference_person_geometry,1);
 const badTest=structuredClone(m);badTest.cases[0].source_split='test';
 assert.throws(()=>run(badTest,h,p));
 const modifiedGT=structuredClone(h);modifiedGT.reference_modified=true;
 assert.throws(()=>run(m,modifiedGT,p));
 const contradiction=structuredClone(h);contradiction.cases[0].recorded_visual_states.find(z=>z.ppe_type==='face_mask').visual_state='PRESENT';
 const withFlip=run(m,contradiction,p);
 assert.ok(withFlip.per_item_cue_totals.opposing>=out.per_item_cue_totals.opposing);
 assert.equal(withFlip.detector_precision_recall_F1_mAP_scored,false);
 console.log('SEER_V16_SYNTHETIC_REFERENCE_CONFLICT_TRIAGE_NEVER_COMPUTE_MODEL_METRICS_PASS');
 console.log('SEER_V16_SYNTHETIC_TRAIN_REVISION_POLICY_TEST_AND_HUMAN_SIGNOFF_GUARDS_PASS');
}
try{
 const arg=process.argv[2]??'--audit';
 if(arg==='--self-test')tests();
 else if(arg==='--audit'){
  const out=run(
   read('ROBOFLOW_TRAIN_ONLY_REAL_MODEL_PREFLIGHT_2026-11-21_V16.json'),
   read('TRAIN_ONLY_LIVE_HUMAN_REFERENCE_GEOMETRY_V16.json'),
   read('TRAIN_ONLY_PERSON_PPE_GEOMETRIC_REVIEW_V16.json'));
  if(process.argv[3])writeFileSync(process.argv[3],JSON.stringify(out,null,2)+'\n');
  console.log(JSON.stringify({cases:out.cases.map(x=>({case:x.case,reference_persons:x.human_reference_scene_persons,
   model_persons:x.detector_person_candidates,box_alignments:x.exploratory_box_alignment.pairs.length,
   review:x.cue_review_counts})),summary:out.per_item_cue_totals,
   scientific_scoring_ready:out.scientific_scoring_ready},null,2));
  console.log('SEER_V16_ACTUAL_TRAIN_CUE_VS_HUMAN_REFERENCE_REVIEW_ONLY_PASS');
 }else throw Error('Usage --self-test | --audit [file]');
}catch(e){console.error(String(e));process.exitCode=2;}
