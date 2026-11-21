#!/usr/bin/env node
/**
 * V19: read-only original annotated object boxes vs existing fixed RF-DETR
 * predictions. Train A/B/C/D ONLY. Numbers are exploratory source-label
 * reproducibility diagnostics, NOT independent Validation/Test scoring.
 * Source polygons are evaluated using saved enclosing bbox, NOT segmentation.
 *
 * Bounding-box average-precision proxy is truncated at the hosted output
 * floor score >= 0.20. Do not present it as full mAP, as an independent holdout,
 * or as a metric of PPE violation / occupational compliance.
 */
import assert from 'node:assert/strict';
import {readFileSync,writeFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import {resolve} from 'node:path';
import {fileURLToPath} from 'node:url';
const ROOT=resolve(fileURLToPath(new URL('..',import.meta.url)));
const names={
 gt:'TRAIN_ORIGINAL_SOURCE_ANNOTATIONS_READONLY_V19.json',
 pred:'ROBOFLOW_TRAIN_ONLY_REAL_MODEL_PREFLIGHT_2026-11-21_V16.json',
 author:'AUTHOR_CURATOR_REFERENCE_POLICY_2026-11-21_V18.json'
};
const read=n=>JSON.parse(readFileSync(resolve(ROOT,n),'utf8'));
const digest=n=>createHash('sha256').update(readFileSync(resolve(ROOT,n))).digest('hex');
const need=(b,msg)=>{if(!b)throw Error('SEER_V19_TRAIN_DETECTION_BLOCKED:'+msg)};
const expected={
 A:['0jRe8fpRDE5fLgAJrYvT','8f7cce94-d46e-4fac-9a0a-641bcd1f12c8','image_604.jpg'],
 B:['0xxsYWiz1FZBYERolu4z','87b6cc58-43bd-4583-8b13-bd9b7413c03d','000760.jpg'],
 C:['0jGu9euJp1MbvkLtfBcs','c032f81d-64c5-44be-96f3-7e6fe9dad799','Kathiah Gets a Chance03.jpg'],
 D:['0oVmRAxL0SM1PWqZCNyM','c197d82e-7870-42a3-bf94-462420d3f6a2','h1.jpg']
};
const nums=x=>Array.isArray(x)&&x.length===4&&x.every(v=>Number.isFinite(v));
const box=(b,w,h)=>{
 need(nums(b)&&b[2]>0&&b[3]>0,'malformed bounding box');
 const [x,y,bw,bh]=b;
 const x1=Math.max(0,x-bw/2),y1=Math.max(0,y-bh/2);
 const x2=Math.min(w,x+bw/2),y2=Math.min(h,y+bh/2);
 need(x2>x1&&y2>y1,'box empty/out of image bounds');
 return [x1,y1,x2,y2];
};
const iou=(a,b)=>{
 const dx=Math.max(0,Math.min(a[2],b[2])-Math.max(a[0],b[0]));
 const dy=Math.max(0,Math.min(a[3],b[3])-Math.max(a[1],b[1]));
 const ia=dx*dy,area=x=>(x[2]-x[0])*(x[3]-x[1]);
 return ia/(area(a)+area(b)-ia);
};
function prepare(gt,pred,author){
 need(gt.schema_version==='seer-ppe/live-original-source-annotation-bbox-snapshot/v0.19' &&
  pred.schema_version==='seer-ppe/train-only-real-roboflow-preflight/v0.16',
  'original labels / model schema changed');
 need(gt.train_cases_only===true&&gt.original_annotations_modified===false &&
  gt.validation_or_test_annotations_accessed===false&&gt.scoring_ready===false&&
  gt.snapshot_is_independent_gold===false,
  'source annotation gold independence or scope fabricated');
 need(author.schema_version==='seer-ppe/author-single-curator-primary-reference-policy/v0.18' &&
  author.original_annotations_accepted_as_single_curator_object_detection_reference===true &&
  author.second_human_reviewer_required===false &&
  author.scientific_scoring_ready===false,
  'author original curation changed or reference status invalid');
 need(pred.model_id==='altayyar-0oflt-lafos-qqauz/2' &&
  pred.workflow_id==='61llCTFuQ4Aq4goQ9HiP'&&
  pred.model_modified===false && pred.model_retrained===false &&
  pred.dataset_images_or_labels_modified===false &&
  pred.test_inputs_used===0&&pred.validation_inputs_used===0&&
  pred.scoring_ready===false && pred.scientific_performance_metric_computed===false,
  'original predictor or protected split changed');
 need(gt.cases.length===4&&pred.cases.length===4&&
  new Set(gt.cases.map(x=>x.case)).size===4&&
  new Set(pred.cases.map(x=>x.case)).size===4,'A-D identities inconsistent');
 const out=[];
 for(const a of gt.cases){
  const exp=expected[a.case],p=pred.cases.find(x=>x.case===a.case);
  need(exp&&p && a.source_image_id===exp[0] && p.case_id===exp[1] &&
   a.filename===exp[2]&&p.filename===exp[2]&&
   a.split==='train'&&p.source_split==='train'&&
   a.width===p.image_dimensions.width&&a.height===p.image_dimensions.height&&
   a.annotation_valid===true&&a.annotation_state==='ANNOTATED' &&
   p.human_reference_read_only===true&&p.used_as_scientific_score===false,
   'case ID, filename, dimensions, split, or annotation validity changed');
  const ids=new Set(),labs=a.original_source_boxes.map(g=>{
   need(!ids.has(g.annotation_id),'duplicate annotation ID');
   ids.add(g.annotation_id);
   need(typeof g.class_name==='string'&&g.class_name.length>0 &&
    ['BOX','POLYGON_BBOX'].includes(g.annotation_shape),
    'malformed annotation category/shape');
   return {case:a.case,source_id:a.source_image_id,id:g.annotation_id,cls:g.class_name,
     box:box(g.center_xywh,a.width,a.height),assisted:g.labeled_by_model!==null};
  });
  need(a.annotated_objects===labs.length &&
   a.model_assisted_label_count===labs.filter(x=>x.assisted).length,
   'annotation count or model-assisted provenance drift');
  const predIds=new Set();
  const preds=p.detections.map(d=>{
   need(!predIds.has(d.id),'duplicate detection ID');predIds.add(d.id);
   need(typeof d.cls==='string'&&d.cls.length>0 &&
    d.confidence>=0.20&&d.confidence<=1&&Number.isFinite(d.confidence),
    'prediction label or hosted score floor invalid');
   return {case:a.case,source_id:a.source_image_id,id:d.id,cls:d.cls,
    score:d.confidence,box:box([d.x,d.y,d.width,d.height],a.width,a.height)};
  });
  need(preds.length===p.counts.raw,'prediction total inconsistent');
  out.push({case:a.case,source_id:a.source_image_id,reference:labs,predictions:preds,
   source_annotation_group_version:a.annotation_group_version,
   contains_model_assisted_reference:labs.some(x=>x.assisted)});
 }
 out.sort((a,b)=>a.case.localeCompare(b.case));
 need(out.reduce((s,x)=>s+x.reference.length,0)===48 &&
  out.reduce((s,x)=>s+x.predictions.length,0)===51 &&
  out.reduce((s,x)=>s+x.reference.filter(b=>b.assisted).length,0)===7,
  'live Train label/prediction counts changed');
 return out;
}
const round=n=>Number(n.toFixed(6));
function classRank(gt,pred,cls,threshold){
 const refs=gt.filter(g=>g.cls===cls);
 const predicted=pred.filter(p=>p.cls===cls).sort((a,b)=>b.score-a.score||
  a.case.localeCompare(b.case)||a.id.localeCompare(b.id));
 const used=new Set();let tp=0,fp=0;
 const steps=[];
 for(const p of predicted){
  let best=null,bestIoU=-1;
  for(const g of refs) {
   const key=g.case+'|'+g.id;
   if(g.case!==p.case||used.has(key))continue;
   const v=iou(g.box,p.box);
   if(v>bestIoU+1e-10||(Math.abs(v-bestIoU)<1e-10&&best&&g.id<best.id)){best=g;bestIoU=v;}
  }
  const match=best&&bestIoU+1e-10>=threshold;
  if(match){tp++;used.add(best.case+'|'+best.id);}else fp++;
  steps.push({confidence:p.score,tp,fp,recall:refs.length?tp/refs.length:0,precision:tp/(tp+fp)});
 }
 const fn=refs.length-tp;
 const ap=()=>{
  if(!refs.length)return null;
  let sum=0;
  for(let r=0;r<=100;r++){
   const recall=r/100;
   sum+=Math.max(0,...steps.filter(x=>x.recall>=recall-1e-10).map(x=>x.precision));
  }
  return sum/101;
 };
 return {gt:refs.length,pred:predicted.length,tp,fp,fn,ap:ap()};
}
function calc(rows){
 const g=rows.flatMap(x=>x.reference),p=rows.flatMap(x=>x.predictions);
 const categories=[...new Set([...g.map(x=>x.cls),...p.map(x=>x.cls)])].sort();
 const thresholds=Array.from({length:10},(_,i)=>0.5+i*.05);
 const perClass=categories.map(cls=>{
  const m=classRank(g,p,cls,0.5);
  const aps=thresholds.map(t=>classRank(g,p,cls,t).ap);
  return {class_name:cls,original_reference_boxes:m.gt,fixed_model_predicted_boxes:m.pred,
    true_positive_bbox_iou_0p5:m.tp,false_positive_bbox_iou_0p5:m.fp,
    false_negative_bbox_iou_0p5:m.fn,ap50_proxy_above_conf_0p2:m.ap===null?null:round(m.ap),
    mean_ap50_to_95_proxy_above_conf_0p2:m.ap===null?null:round(aps.reduce((s,x)=>s+x,0)/10)};
 });
 const count=k=>perClass.reduce((s,x)=>s+x[k],0);
 const positives=perClass.filter(x=>x.original_reference_boxes>0);
 const macro=k=>positives.length?round(positives.reduce((s,x)=>s+x[k],0)/positives.length):null;
 const tp=count('true_positive_bbox_iou_0p5'),fp=count('false_positive_bbox_iou_0p5'),fn=count('false_negative_bbox_iou_0p5');
 return {images:rows.length,reference_boxes:g.length,prediction_boxes:p.length,
  source_boxes_marked_model_assisted:g.filter(x=>x.assisted).length,
  classes_with_gt:positives.length,predicted_classes:perClass.filter(x=>x.fixed_model_predicted_boxes>0).length,
  bbox_iou:0.5,prediction_floor_confidence:0.2,
  tp,fp,fn,precision:tp+fp?round(tp/(tp+fp)):null,
  recall:tp+fn?round(tp/(tp+fn)):null,
  f1:2*tp+fp+fn?round(2*tp/(2*tp+fp+fn)):null,
  proxy_macro_ap50_above_conf_0p2:macro('ap50_proxy_above_conf_0p2'),
  proxy_macro_ap50_95_above_conf_0p2:macro('mean_ap50_to_95_proxy_above_conf_0p2'),
  per_class:perClass};
}
function run(gt,pred,author){
 const rows=prepare(gt,pred,author);
 const full=calc(rows);
 const noAssistedImage=calc(rows.filter(x=>!x.contains_model_assisted_reference));
 need(full.images===4 && full.reference_boxes===48&&full.prediction_boxes===51&&
  full.source_boxes_marked_model_assisted===7&&
  noAssistedImage.images===3&&noAssistedImage.source_boxes_marked_model_assisted===0,
  'model-assisted annotation image sensitivity invalid');
 return {
  schema_version:'seer-ppe/train-original-annotation-bbox-qa/v0.19',
  date:'2026-11-21',purpose:'DEVELOPMENT_ONLY_TRAIN_NUMERIC_REFERENCE_ALIGNMENT_NOT_SCIENTIFIC_VALIDATION',
  source:"LIVE_ORIGINAL_SOURCE_ANNOTATION_BBOXES_READ_ONLY_V19_VS_REAL_SAVED_ORIGINAL_RFDETR_TRAIN_PREDICTIONS_V16",
  original_model_id:pred.model_id,
  evidence_sha256:Object.fromEntries(Object.entries(names).map(([k,f])=>[k,digest(f)])),
  metrics_are_scientific_valid_or_test_performance:false,
  source_reference_independent_from_training:false,
  historical_same_Train_images_used_in_model_development:true,
  source_reference_is_single_author_curated:true,
  model_assisted_reference_tags_preserved:true,
  classes_with_negative_prefix_are_box_labels_not_workplace_violations:true,
  polygon_segmentation_metric_computed:false,
  ap_metrics_are_truncated_above_hosted_prediction_floor:true,
  additional_inference_calls:0,valid_inference_calls:0,test_accessed:false,
  independent_valid_scoring_approved:false,worker_compliance_scored:false,
  original_images_or_labels_modified:false,
  scoring_ready:false,
  profiles:{
   ALL_FOUR_EXISTING_TRAIN_SOURCE_BOXES_NONSCORING:full,
   EXCLUDE_ENTIRE_IMAGES_WITH_MODEL_ASSISTED_SOURCE_LABELS_NONSCORING:noAssistedImage
  }
 };
}
function tests(){
 const g=read(names.gt),p=read(names.pred),a=read(names.author),r=run(g,p,a);
 assert.equal(r.profiles.ALL_FOUR_EXISTING_TRAIN_SOURCE_BOXES_NONSCORING.reference_boxes,48);
 assert.equal(r.profiles.ALL_FOUR_EXISTING_TRAIN_SOURCE_BOXES_NONSCORING.prediction_boxes,51);
 assert.equal(r.profiles.EXCLUDE_ENTIRE_IMAGES_WITH_MODEL_ASSISTED_SOURCE_LABELS_NONSCORING.images,3);
 assert.equal(r.scoring_ready,false);
 const g2=structuredClone(g);g2.cases[0].split='test';
 assert.throws(()=>run(g2,p,a));
 const p2=structuredClone(p);p2.cases[3].source_split='valid';
 assert.throws(()=>run(g,p2,a));
 const g3=structuredClone(g);g3.cases[1].original_source_boxes[0].labeled_by_model=null;
 assert.throws(()=>run(g3,p,a));
 const p3=structuredClone(p);p3.cases[0].detections[0].confidence=0.1;
 assert.throws(()=>run(g,p3,a));
 const toyGt=[{case:'X',id:'g1',cls:'Hard Hat',box:[0,0,10,10]}];
 const toyP=[{case:'X',id:'p1',cls:'Hard Hat',score:0.9,box:[0,0,10,10]},
 {case:'X',id:'p2',cls:'Hard Hat',score:0.8,box:[0,0,10,10]}];
 const t=classRank(toyGt,toyP,'Hard Hat',0.5);
 assert.deepEqual([t.gt,t.pred,t.tp,t.fp,t.fn],[1,2,1,1,0]);
 assert.ok(t.ap>=0&&t.ap<=1);
 const mismatched=classRank(toyGt,[{...toyP[0],cls:'No Hard Hat'}],'Hard Hat',0.5);
 assert.deepEqual([mismatched.tp,mismatched.fn],[0,1]);
 console.log('SEER_V19_TRAIN_REFERENCE_BOX_MATCHER_SYNTHETIC_TEST_AND_SPLIT_GUARDS_PASS');
}
try{
 const mode=process.argv[2]??'--audit';
 if(mode==='--self-test')tests();
 else if(mode==='--audit'){
  const out=run(read(names.gt),read(names.pred),read(names.author));
  if(process.argv[3])writeFileSync(process.argv[3],JSON.stringify(out,null,2)+'\n');
  console.log(JSON.stringify({profiles:Object.fromEntries(Object.entries(out.profiles).map(([k,v])=>[k,{
   images:v.images,gt:v.reference_boxes,pred:v.prediction_boxes,assisted:v.source_boxes_marked_model_assisted,
   tp:v.tp,fp:v.fp,fn:v.fn,precision:v.precision,recall:v.recall,f1:v.f1
  }])),scoring_ready:out.scoring_ready},null,2));
  console.log('SEER_V19_ACTUAL_ORIGINAL_TRAIN_ANNOTATION_MATCH_READ_ONLY_PASS');
 }else throw Error('Usage: --self-test | --audit [output.json]');
}catch(e){console.error(String(e));process.exitCode=2;}
