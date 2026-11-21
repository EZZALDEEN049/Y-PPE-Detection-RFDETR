#!/usr/bin/env node
/**
 * SEER-PPE V27: freeze target IDs and non-target control boxes BEFORE any
 * new perturbation inference. A6 is a class-error-calibrated selective
 * comparator using V26 M0-minus-five-V23-pilot class FDR.
 *
 * This script only reads existing V16/V23/V25/V26 numeric files. It does
 * not read image pixels, annotations per target, Test, or run inference.
 */
import {readFileSync,writeFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import {resolve} from 'node:path';
import {fileURLToPath} from 'node:url';
import assert from 'node:assert/strict';
const ROOT=resolve(fileURLToPath(new URL('..',import.meta.url)));
const files={
 train:'ROBOFLOW_TRAIN_ONLY_REAL_MODEL_PREFLIGHT_2026-11-21_V16.json',
 valid:'VALID_ORIGINAL_SOURCE_CURRENT_BBOX_MODEL_PILOT_V23.json',
 route:'ACTUAL_A0_A2_A5_PAIRED_OFFLINE_ROUTING_V25.json',
 summary:'V26_VALID_CURRENT_SOURCE_459_NUMERIC_SUMMARY.json'
};
const read=n=>JSON.parse(readFileSync(resolve(ROOT,n),'utf8'));
const sha=n=>createHash('sha256').update(readFileSync(resolve(ROOT,n))).digest('hex');
const need=(v,m)=>{if(!v)throw Error('SEER_V27_TARGET_FREEZE_BLOCKED:'+m)};
const model='altayyar-0oflt-lafos-qqauz/2';
const sourceProject='softyyemen/altayyar-0oflt-lafos-qqauz';
const imageAssetIds={
 'train:A':'0jRe8fpRDE5fLgAJrYvT',
 'train:B':'0xxsYWiz1FZBYERolu4z',
 'train:C':'0jGu9euJp1MbvkLtfBcs',
 'train:D':'0oVmRAxL0SM1PWqZCNyM'
};
const round=n=>Number(n.toFixed(6));
const area=d=>d.width*d.height;
const corners=d=>[d.x-d.width/2,d.y-d.height/2,d.x+d.width/2,d.y+d.height/2];
function overlap(a,b){
 const A=corners(a),B=corners(b);
 const w=Math.max(0,Math.min(A[2],B[2])-Math.max(A[0],B[0]));
 const h=Math.max(0,Math.min(A[3],B[3])-Math.max(A[1],B[1]));
 const inter=w*h;
 return {iou:inter/(area(a)+area(b)-inter),target_intersection_fraction:inter/area(a)};
}
const train=read(files.train),valid=read(files.valid),route=read(files.route),v26=read(files.summary);
need(train.schema_version==='seer-ppe/train-only-real-roboflow-preflight/v0.16'&&
 train.model_id===model&&train.model_retrained===false&&train.model_modified===false&&
 train.dataset_images_or_labels_modified===false&&train.test_inputs_used===0&&
 train.validation_inputs_used===0&&train.cases.length===4,'V16_TRAIN_INPUT');
need(valid.schema_version==='seer-ppe/actual-hosted-valid-pilot-current-gt-pred-bboxes/v0.23'&&
 valid.model_id===model&&valid.source_project===sourceProject&&
 valid.selected_image_count===5&&valid.no_test_accessed===true&&
 valid.selection_predeclared_ids.length===5&&valid.rows.length===5,'V23_VALID_INPUT');
need(route.schema_version==='seer-ppe/v25-real-saved-prediction-A2-A5-safety-matched-offline-routing/v0.25'&&
 route.model_id===model&&route.aggregate.images===9&&route.aggregate.original_detector_boxes===74&&
 route.no_test_or_external_holdout_used===true&&route.no_real_XAI_or_human_review_executed===true,
 'V25_ROUTING_INPUT');
need(v26.schema_version==='seer-ppe/v26-current-author-reference-full-459-compact/v0.26'&&
 v26.cohorts.M0.images===459&&v26.sensitivities.M0_minus_5_V23_pilot_exposures.images===454,
 'V26_CLASS_CALIBRATION_INPUT');
const calibration=v26.sensitivities.M0_minus_5_V23_pilot_exposures;
const pilotIds=new Set(valid.selection_predeclared_ids);
need(pilotIds.size===5&&valid.rows.every(r=>pilotIds.has(r.source_id)),'V23_PILOT_IDS');
const fdr=Object.fromEntries(calibration.per_class.map(c=>{
 need(c.TP+c.FP>0,'ZERO_CLASS_CALIBRATION_DENOMINATOR_'+c.class_name);
 return [c.class_name,round(c.FP/(c.TP+c.FP))];
}));
const images=new Map();
for(let i=0;i<4;i++){
 const c=train.cases[i],letter=['A','B','C','D'][i],key='train:'+letter;
 need(c.case===letter&&c.source_split==='train'&&c.filename&&c.detections?.length===c.counts.raw,
  'TRAIN_CASE_'+letter);
 images.set(key,{
  image_key:key,asset_id:imageAssetIds[key],source_id:null,split:'train',
  filename:c.filename,width:c.image_dimensions.width,height:c.image_dimensions.height,
  historically_development_exposed:true,
  detections:c.detections.map(d=>({id:d.id,cls:d.cls,confidence:d.confidence,x:d.x,y:d.y,width:d.width,height:d.height}))
 });
}
for(const r of valid.rows){
 need(r.split==='valid'&&r.annotation_valid===true,'VALID_SOURCE_'+r.source_id);
 const key='valid:'+r.source_id;
 images.set(key,{
  image_key:key,asset_id:r.source_id,source_id:r.source_id,split:'valid',
  filename:r.original_filename,width:r.image_width,height:r.image_height,
  historically_development_exposed:true,
  detections:r.predictions.map(d=>({id:d.id,cls:d.class_name,confidence:d.confidence,x:d.x,y:d.y,width:d.width,height:d.height}))
 });
}
need(images.size===9,'NINE_FROZEN_IMAGES');
const imageResults=[],targets=[];
for(const im of route.paired_images){
 const src=images.get(im.image_key);
 need(src&&src.detections.length>0,'ROUTING_IMAGE_MISSING_'+im.image_key);
 const cues=im.A5.ranked_cues??[];
 const scored=cues.map(c=>{
  const association=c.association?.status??'ASSOCIATION_UNKNOWN';
  const unresolved=!['TENTATIVE_SINGLE','TENTATIVE_MARGIN'].includes(association);
  const classFdr=fdr[c.original_class];
  need(classFdr!==undefined,'MISSING_CLASS_FDR_'+c.original_class);
  const priority=.50*(1-c.confidence)+.30*classFdr+.20*Number(unresolved);
  return {...c,a6_priority:round(priority),a6_class_fdr:classFdr,a6_unresolved_association:unresolved};
 }).sort((a,b)=>b.a6_priority-a.a6_priority||a.detection_id.localeCompare(b.detection_id));
 const A2=im.A2.explanation_target_detection_id??null;
 const A5=im.A5.explanation_target_detection_id??null;
 const A6=scored[0]?.detection_id??null;
 const selected={A2,A5,A6,
  A2_class:im.A2.ranked_cues?.[0]?.original_class??null,
  A5_class:im.A5.ranked_cues?.[0]?.original_class??null,
  A6_class:scored[0]?.original_class??null,
  A6_priority:scored[0]?.a6_priority??null,
  A6_class_FDR:scored[0]?.a6_class_fdr??null,
  A6_association:scored[0]?.association?.status??null
 };
 imageResults.push({image_key:im.image_key,filename:src.filename,split:src.split,asset_id:src.asset_id,
  original_detection_count:src.detections.length,typed_PPE_cue_count:cues.length,selected});
 for(const [arm,id] of [['A5',A5],['A6',A6]]){
  if(!id)continue;
  let existing=targets.find(t=>t.image_key===im.image_key&&t.target_id===id);
  if(existing){existing.arms.push(arm);continue;}
  const d=src.detections.find(x=>x.id===id);
  need(d&&d.cls,'SELECTED_TARGET_GEOMETRY_MISSING_'+im.image_key+'_'+id);
  const cue=cues.find(x=>x.detection_id===id);
  const candidates=src.detections.filter(x=>x.id!==id&&x.cls!==d.cls)
   .map(x=>({...x,...overlap(d,x),area_ratio:round(area(x)/area(d))}))
   .filter(x=>x.iou<.01&&x.target_intersection_fraction<.05)
   .sort((a,b)=>Math.abs(Math.log(a.area_ratio))-Math.abs(Math.log(b.area_ratio))||a.id.localeCompare(b.id));
  const ctrl=candidates[0]??null;
  targets.push({
   image_key:im.image_key,asset_id:src.asset_id,source_id:src.source_id,
   split:src.split,filename:src.filename,image_width:src.width,image_height:src.height,
   target_id:d.id,target_class:d.cls,confidence:round(d.confidence),
   bbox_center_xywh:{x:round(d.x),y:round(d.y),width:round(d.width),height:round(d.height)},
   arms:[arm],
   A5_fixed_priority:cue?.fixed_priority_proxy??null,
   A6_class_FDR:fdr[d.cls],
   control:ctrl?{
    detection_id:ctrl.id,class_name:ctrl.cls,confidence:round(ctrl.confidence),
    bbox_center_xywh:{x:round(ctrl.x),y:round(ctrl.y),width:round(ctrl.width),height:round(ctrl.height)},
    area_ratio_relative_to_target:ctrl.area_ratio,
    target_intersection_fraction:round(ctrl.target_intersection_fraction)
   }:null
  });
 }
}
const A5count=imageResults.filter(x=>x.selected.A5).length;
const A6count=imageResults.filter(x=>x.selected.A6).length;
const shared=imageResults.filter(x=>x.selected.A5&&x.selected.A5===x.selected.A6).length;
const diff=imageResults.filter(x=>x.selected.A5&&x.selected.A6&&x.selected.A5!==x.selected.A6).length;
need(A5count===8&&A6count===8&&shared===6&&diff===2&&targets.length===10,'ARM_TARGET_BUDGET_OR_DEDUP');
need(targets.filter(x=>x.control).length===7,'CONTROL_REGION_COUNT');
const manifest={
 schema_version:'seer-ppe/v27-frozen-targeted-occlusion-sample-and-A6-class-error-calibrated-comparator/v0.27',
 frozen_date:'2026-11-21',model_id:model,source_project:sourceProject,
 source_images:9,original_detector_boxes:74,typed_PPE_cues:59,
 image_selection:'EXACT_REUSE_OF_ALL_NINE_PREVIOUS_V25_DEVELOPMENT_IMAGES_NO_NEW_IMAGE_SELECTION',
 train_source_asset_ids:imageAssetIds,
 valid_source_ids:valid.selection_predeclared_ids,
 no_image_bytes_or_urls_saved:true,no_test_accessed:true,
 original_model_or_data_changed:false,source_independence_verified:false,
 A2_included_as_historical_confidence_only_baseline:true,
 A5_policy:'V25_FROZEN_UNCHANGED_NEGATIVE_CUE_PLUS_UNRESOLVED_ASSOCIATION_PLUS_FIXED_SEVERITY',
 A6_policy:{
  name:'A6_CLASS_ERROR_CALIBRATED_SELECTIVE_REVIEW',
  formula:'0.50*(1-detection_confidence)+0.30*class_FDR_calibration+0.20*unresolved_person_association',
  unresolved_association_statuses:['ASSOCIATION_AMBIGUOUS','ASSOCIATION_UNKNOWN','PERSON_CANDIDATE_NOT_DETECTED'],
  calibrated_class_FDR_source:'V26 M0 minus five V23 prior-pilot source images; 454 other original Source Valid images',
  class_FDR:'FP/(TP+FP) from V26 current author-reference class-wise results',
  target_image_GT_used_as_a_feature:false,
  A6_is_proven_superior:false,
  source_calibration_independent_or_unexposed:false
 },
 calibration_class_FDR:fdr,
 per_image_selections:imageResults,
 unique_A5_A6_target_tests:targets,
 budget:{
  per_arm_max_target_XAI_requests_per_image:1,
  per_arm_max_proposed_human_reviews_per_image:1,
  A5_target_slots:A5count,A6_target_slots:A6count,
  shared_target_slots:shared,different_target_slots:diff,
  unique_target_occlusion_tests:targets.length,
  controls_available:targets.filter(x=>x.control).length,
  no_control:targets.filter(x=>!x.control).length,
  planned_original_model_inference_calls:targets.length*2+targets.filter(x=>x.control).length,
  actual_XAI_calls_before_execution:0,actual_human_reviews_dispatched:0
 },
 no_per_detection_GT_or_V23_match_error_used_in_selection:true,
 V23_match_join_only_after_execution_for_object_detection_diagnostic:true,
 no_worker_compliance_or_violation_inference:true,
 strict_worker_safety_scoring_ready:false
};
const out=process.argv[2]??resolve(ROOT,'V27_FROZEN_TARGETS_2026-11-21.json');
writeFileSync(out,JSON.stringify(manifest,null,2)+'\n');
console.log(JSON.stringify({
 schema:manifest.schema_version,images:manifest.source_images,boxes:manifest.original_detector_boxes,
 cues:manifest.typed_PPE_cues,A5:A5count,A6:A6count,shared,different:diff,
 uniqueTargets:targets.length,controls:manifest.budget.controls_available,
 modelCallsPlanned:manifest.budget.planned_original_model_inference_calls,
 inputHashes:Object.fromEntries(Object.values(files).map(n=>[n,sha(n)]))
},null,2));
