#!/usr/bin/env node
/**
 * SEER-PPE V26: 459 actual vector-inferred original Source Valid images.
 * Fixed, unchanged RF-DETR Small 17 classes, conf>=0.20, hosted overlap .50,
 * exact-class greedy native-pixel bounding-box IoU >= .50 against CURRENT
 * already author-curated original Source labels. NOT SEER policy efficacy.
 */
import {readFileSync,writeFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import {fileURLToPath} from 'node:url';
import {resolve} from 'node:path';
import assert from 'node:assert/strict';
const ROOT=resolve(fileURLToPath(new URL('..',import.meta.url)));
const baseNames=[
 'VALIDATION_SOURCE_OVERLAP_NUMERIC_SENSITIVITY_V19.json',
 'V20_VALID_SOURCE_ANNOTATION_COUNTS_PART1_PRIVATE_WORKING.json',
 'V20_VALID_SOURCE_ANNOTATION_COUNTS_PART2_PRIVATE_WORKING.json',
 'HISTORICAL_VALID_INTERNAL_METRICS_V20.json',
 'VALID_ORIGINAL_SOURCE_CURRENT_BBOX_MODEL_PILOT_V23.json'
];
const shardName=i=>'V26_ORIGINAL_VALID_GEOMETRY_SHARD_'+String(i).padStart(2,'0')+'_OF_12.json';
const read=n=>JSON.parse(readFileSync(resolve(ROOT,n),'utf8'));
const sha=n=>createHash('sha256').update(readFileSync(resolve(ROOT,n))).digest('hex');
const must=(x,m)=>{if(!x)throw Error('SEER_V26_FAIL_CLOSED_'+m)};
const classes=['Animal','Child','Face Masks','No Hard Hat','No Safety Boots','Soft Hat','Hard Hat','No Safety Vest','Pants','No Face Mask','No Safety Attire','No Gloves','Gloves','Safety Boots','Safety Vests','Goggles','Persons'];
const allowed=new Set(classes);
const model='altayyar-0oflt-lafos-qqauz/2';
const round=n=>Number(n.toFixed(6));
const divide=(a,b)=>b>0?round(a/b):null;
const clip=(b,w,h)=>{
 must(['x','y','width','height'].every(k=>typeof b[k]==='number'&&Number.isFinite(b[k]))&&b.width>0&&b.height>0,'BAD_RECTANGLE');
 const z=[Math.max(0,b.x-b.width/2),Math.max(0,b.y-b.height/2),Math.min(w,b.x+b.width/2),Math.min(h,b.y+b.height/2)];
 must(z[2]>z[0]&&z[3]>z[1],'ZERO_AREA_AFTER_CLIP');return z;
};
const iou=(a,b)=>{
 const w=Math.max(0,Math.min(a[2],b[2])-Math.max(a[0],b[0])),h=Math.max(0,Math.min(a[3],b[3])-Math.max(a[1],b[1]));
 const area=z=>(z[2]-z[0])*(z[3]-z[1]);
 return w*h/(area(a)+area(b)-w*h);
};
function score(row){
 const usedG=new Set(),usedP=new Set(),count={};
 for(const c of classes)count[c]={gt:0,pred:0,tp:0,fp:0,fn:0,assisted:0,iouSum:0};
 const gt=row.current_author_boxes.map(a=>{
  must(typeof a.id==='string'&&!usedG.has(a.id)&&allowed.has(a.cls)&&
   (a.labeledByModel===null||typeof a.labeledByModel==='string'),'BAD_GT_REFERENCE_ID_CLASS');
  usedG.add(a.id);count[a.cls].gt++;if(a.labeledByModel!==null)count[a.cls].assisted++;
  return {...a,rect:clip(a,row.image_width,row.image_height)};
 });
 const pred=row.model_predictions.map(p=>{
  must(typeof p.id==='string'&&!usedP.has(p.id)&&allowed.has(p.cls)&&
   Number.isFinite(p.confidence)&&p.confidence>=.2&&p.confidence<=1,'BAD_MODEL_PRED_ID_CONF_CLASS');
  usedP.add(p.id);count[p.cls].pred++;
  return {...p,rect:clip(p,row.image_width,row.image_height)};
 }).sort((a,b)=>b.confidence-a.confidence||a.id.localeCompare(b.id));
 const matched=new Set(),pairs=[],fpPred=[];
 for(const p of pred){
  let best=null,bestIoU=-1;
  for(const g of gt){
   if(g.cls!==p.cls||matched.has(g.id))continue;
   const n=iou(p.rect,g.rect);
   if(n>bestIoU+1e-12||(Math.abs(n-bestIoU)<=1e-12&&best&&g.id<best.id)){
    best=g;bestIoU=n;
   }
  }
  if(best&&bestIoU+1e-10>=.50){
   matched.add(best.id);count[p.cls].tp++;count[p.cls].iouSum+=bestIoU;
   pairs.push({pred_id:p.id,gt_id:best.id,cls:p.cls,iou:round(bestIoU)});
  }else{count[p.cls].fp++;fpPred.push({pred_id:p.id,cls:p.cls});}
 }
 const missing=[];
 for(const g of gt)if(!matched.has(g.id)){count[g.cls].fn++;missing.push({gt_id:g.id,cls:g.cls});}
 must(pairs.length+missing.length===gt.length&&pairs.length+fpPred.length===pred.length,'PER_IMAGE_BOX_CONSERVATION');
 return {counts:count,gt:gt.length,pred:pred.length,tp:pairs.length,fp:fpPred.length,fn:missing.length,
 assisted:gt.filter(g=>g.labeledByModel!==null).length,matches:pairs,unmatched_predictions:fpPred,unmatched_reference:missing};
}
function compile(shards,inputs){
 const [risk,a,b,hist,pilot]=inputs;
 must(risk.schema_version==='seer-ppe/validation-source-computational-sensitivity-screen/v0.19'&&
  risk.input_clean17_valid_count===459&&risk.test_sources_or_images_accessed===false&&risk.scoring_ready===false&&
  risk.independent_valid_scientific_cohort_size===0,'V19_RISK_SCOPE');
 must(a.schema_version==='seer-ppe/read-only-valid-source-annotation-counts-part/v0.20'&&a.part===1&&a.rows.length===250&&
  b.schema_version===a.schema_version&&b.part===2&&b.rows.length===209&&a.split==='valid'&&b.split==='valid'&&
  a.read_only&&b.read_only&&!a.source_annotations_modified&&!b.source_annotations_modified,'V20_AUTHOR_REFERENCE_SCOPE');
 must(hist.schema_version==='seer-ppe/historical-internal-valid-model-eval-three-risk-cohorts/v0.20'&&
  hist.model===model&&hist.existing_evaluation_id==='KyzP9neuyNTN5eQpGCAY'&&hist.test_not_read===true&&
  hist.historical_counters_not_recomputed_against_current_source_box_geometry===true,'HISTORIC_GT_NOT_CURRENT');
 must(pilot.schema_version==='seer-ppe/actual-hosted-valid-pilot-current-original-gt-pred-bboxes/v0.23'&&
  pilot.model_id===model&&pilot.selected_image_count===5&&pilot.no_test_accessed===true,'V23_PILOT');
 const IDs=risk.descriptive_sensitivity_scenarios.ALL_MATCHED_VALID_459.source_ids;
 const ref=new Map([...a.rows,...b.rows].map(z=>[z.source_id,z]));
 const pilotIds=new Set(pilot.selection_predeclared_ids);
 must(IDs.length===459&&new Set(IDs).size===459&&ref.size===459&&pilotIds.size===5&&
  [...pilotIds].every(id=>IDs.includes(id))&&shards.length===12,'459_SOURCE_COVERAGE');
 const rows=[];
 for(let k=0;k<12;k++){
  const sh=shards[k],expected=IDs.slice(k*40,(k+1)*40);
  must(sh.schema_version==='seer-ppe/v26-vector-original-valid-current-gt-real-pred-bbox-shard/v0.26'&&
   sh.shard_index===k&&sh.total_shards===12&&sh.source_start_index===k*40&&
   sh.original_model_id===model&&sh.original_source_split==='valid'&&
   sh.hosted_confidence_floor===.2&&sh.hosted_overlap_threshold===.5&&sh.bbox_match_IoU_threshold===.5&&
   sh.image_urls_saved===false&&sh.original_image_bytes_saved===false&&
   sh.test_unaccessed===true&&sh.original_model_weights_unchanged===true&&sh.author_annotations_unchanged===true&&
   sh.source_independence_verified===false&&sh.worker_compliance_not_scored===true&&
   sh.expected_original_images===expected.length&&sh.rows.length===expected.length&&
   JSON.stringify(sh.expected_source_ids)===JSON.stringify(expected),'SHARD_OR_FROZEN_INPUT_DRIFT_'+k);
  rows.push(...sh.rows);
 }
 must(rows.length===459&&rows.every((r,i)=>r.source_id===IDs[i])&&
  new Set(rows.map(r=>r.source_id)).size===459,'459_SOURCE_IDS_NOT_IDENTICAL');
 const errors=[],perImage=[],byId=new Map();
 for(const row of rows){
  if(row.status!=='SCORED_INPUT_ACQUIRED'){
   errors.push({source_id:row.source_id,status:row.status,error:row.error??null});continue;
  }
  const c=ref.get(row.source_id);
  must(c&&c.source_original_filename===row.original_filename&&
   row.image_width===c.width&&row.image_height===c.height&&
   row.source_annotation_group_version===c.annotation_group_version&&
   row.current_author_boxes?.length===c.saved_object_count&&
   row.model_id===model&&row.execution_method==='V26_VECTOR_WORKFLOW_0p2_CONF_0p5_IOU'&&
   typeof row.inference_id==='string'&&row.inference_id.length>10&&
   row.previously_reused_in_v23_pilot===pilotIds.has(row.source_id),'SOURCE_GT_OR_MODEL_PROVENANCE_'+row.source_id);
  const cls={},assisted=row.current_author_boxes.reduce((n,o)=>{
   cls[o.cls]=(cls[o.cls]??0)+1;return n+Number(o.labeledByModel!==null);
  },0);
  must(Object.entries(c.class_counts).every(([k,v])=>cls[k]===v)&&
   Object.entries(cls).every(([k,v])=>c.class_counts[k]===v)&&
   assisted===c.model_assisted_marker_count,'CURRENT_AUTHOR_GT_CLASSES_OR_ASSISTANCE_CHANGED_'+row.source_id);
  const sc=score(row);
  const z={source_id:row.source_id,original_filename:row.original_filename,split:'valid',
   model_inference_id:row.inference_id,
   originally_development_exposed:true,already_V23_pilot_exposed:row.previously_reused_in_v23_pilot,
   person_worker_safety_state_not_estimated:true,source_independence_verified:false,
   reference_boxes:sc.gt,model_boxes:sc.pred,assisted_reference_boxes:sc.assisted,
   tp:sc.tp,fp:sc.fp,fn:sc.fn,per_class:sc.counts,
   matched_boxes:sc.matches,unmatched_model_boxes:sc.unmatched_predictions,unmatched_GT_boxes:sc.unmatched_reference};
  perImage.push(z);byId.set(z.source_id,z);
 }
 const group=(ids,label)=>{
  const membership=new Set(ids),items=[...membership].map(id=>byId.get(id)).filter(Boolean);
  const sums={tp:0,fp:0,fn:0,reference:0,predictions:0,assisted:0};
  const cat=Object.fromEntries(classes.map(c=>[c,{gt:0,pred:0,tp:0,fp:0,fn:0,assisted:0,iouSum:0,images:0}]));
  for(const z of items){
   sums.tp+=z.tp;sums.fp+=z.fp;sums.fn+=z.fn;sums.reference+=z.reference_boxes;
   sums.predictions+=z.model_boxes;sums.assisted+=z.assisted_reference_boxes;
   for(const name of classes){
    const from=z.per_class[name],to=cat[name];
    for(const key of ['gt','pred','tp','fp','fn','assisted','iouSum'])to[key]+=from[key];
    if(from.gt>0)to.images++;
   }
  }
  must(sums.tp+sums.fn===sums.reference&&sums.tp+sums.fp===sums.predictions&&
   Object.values(cat).reduce((n,x)=>n+x.gt,0)===sums.reference,'COHORT_BOX_SUM_'+label);
  return {
   label,expected_source_images:membership.size,images_scored:items.length,
   complete:items.length===membership.size,
   missing_source_ids:[...membership].filter(id=>!byId.has(id)),
   current_original_author_GT_boxes:sums.reference,
   current_author_model_assisted_annotation_markers:sums.assisted,
   new_original_RFDETR_model_boxes:sums.predictions,
   tp:sums.tp,fp:sums.fp,fn:sums.fn,
   precision:divide(sums.tp,sums.tp+sums.fp),recall:divide(sums.tp,sums.tp+sums.fn),
   f1:divide(2*sums.tp,2*sums.tp+sums.fp+sums.fn),
   per_class:classes.map(c=>({
    class_name:c,images_with_current_GT:cat[c].images,
    current_author_GT_boxes:cat[c].gt,new_original_model_boxes:cat[c].pred,
    model_assisted_GT_markers:cat[c].assisted,
    tp:cat[c].tp,fp:cat[c].fp,fn:cat[c].fn,
    precision:divide(cat[c].tp,cat[c].tp+cat[c].fp),
    recall:divide(cat[c].tp,cat[c].tp+cat[c].fn),
    f1:divide(2*cat[c].tp,2*cat[c].tp+cat[c].fp+cat[c].fn),
    mean_matched_IoU:divide(cat[c].iouSum,cat[c].tp)
   }))
  };
 };
 const m0=IDs,m1=risk.descriptive_sensitivity_scenarios.EXCLUDE_HISTORICAL_HOLDS_AND_TECHNICAL_QUARANTINES_448.source_ids,
 m2=risk.descriptive_sensitivity_scenarios.UNFLAGGED_ONLY_BUT_UNCERTIFIED_367.source_ids;
 must(m1.length===448&&m2.length===367&&m1.every(id=>IDs.includes(id))&&m2.every(id=>m1.includes(id)),'RISK_GROUP_MEMBERSHIP');
 const mismatch=new Set(hist.identity_resolved_individual_source_discrepancies.map(x=>x.source_id));
 must(mismatch.size===13&&[...mismatch].every(id=>IDs.includes(id)),'HISTORICAL_REFERENCE_VERSION_DIFFERENCES');
 const cohorts={
  M0:group(m0,'M0_459_ALL_ORIGINAL_SOURCE_VALID_CURRENT_GT'),
  M1:group(m1,'M1_448_EXCLUDES_HOLDS_AND_HIGH_OVERLAP'),
  M2:group(m2,'M2_367_UNFLAGGED_BUT_NOT_INDEPENDENT')
 };
 if(errors.length===0){
  must(cohorts.M0.current_original_author_GT_boxes===3471&&cohorts.M0.current_author_model_assisted_annotation_markers===729&&
   cohorts.M1.current_original_author_GT_boxes===3433&&cohorts.M1.current_author_model_assisted_annotation_markers===725&&
   cohorts.M2.current_original_author_GT_boxes===3049&&cohorts.M2.current_author_model_assisted_annotation_markers===655,
   'FROZEN_AUTHOR_REFERENCE_TOTALS');
 }
 return {
  schema_version:'seer-ppe/v26-actual-original-valid-current-author-GT-detection-IoU50/v0.26',
  date:'2026-11-21',original_model_id:model,
  full_source_original_Valid_population_before_clean17:468,
  current_author_reference_original_Valid_source_count:459,
  V26_fresh_original_Valid_source_inferences:perImage.length,
  full_459_complete:perImage.length===459&&errors.length===0,
  inference_or_source_failures:errors,
  fixed_hosted_model_confidence_floor:.2,fixed_hosted_overlap:.5,
  fixed_original_source_class_exact_greedy_bbox_IoU:.5,
  method:'UNIFORM_VECTOR_WORKFLOW_FULL_ORIGINAL_VALID_CURRENT_AUTHOR_GT',
  five_prior_V23_images_freshly_reinferred_not_reused:true,
  historical_2025_provider_eval_reference_is_not_same_current_GT:true,
  historical_13_image_16_box_reference_count_version_difference:true,
  original_weights_images_splits_labels_unchanged:true,protected_Test_accessed:false,
  original_Valid_historically_development_exposed:true,source_independence_verified:false,
  individual_worker_safety_compliance_scored:false,SEER_policy_effectiveness_measured:false,
  XAI_faithfulness_and_energy_Joules_measured:false,
  strict_independent_worker_safety_scoring_ready:false,
  file_input_sha256:Object.fromEntries([...baseNames,...Array.from({length:12},(_,i)=>shardName(i))].map(n=>[n,sha(n)])),
  prior_2025_provider_eval_separate_context_only:{
   eval_id:'KyzP9neuyNTN5eQpGCAY',
   M0_historic_micro_f1:0.885018,M1_historic_micro_f1:0.884642,M2_historic_micro_f1:0.880754,
   not_directly_comparable_or_causal_improvement:true
  },
  cohorts,
  prespecified_descriptive_sensitivities:{
   M0_minus_13_current_vs_old_GT_count_differences:group(m0.filter(id=>!mismatch.has(id)),'M0_446_EXCLUDES_13_GT_COUNT_VERSION_DIFFERENCES'),
   M0_minus_5_V23_pilot_exposures:group(m0.filter(id=>!pilotIds.has(id)),'M0_454_EXCLUDES_5_PREVIOUS_V23_EXPOSED'),
   M2_minus_5_V23_pilot_exposures:group(m2.filter(id=>!pilotIds.has(id)),'M2_362_EXCLUDES_5_PREVIOUS_V23_EXPOSED')
  },
  per_source:perImage,
  disclaimer:'Executed unchanged original RF-DETR Small detection on 459 previously model-exposed original Source Valid IDs, scored with CURRENT author-curated boxes. This is internal object detection only, not independent-source generalization or an A5-vs-A2 worker PPE safety/energy effect. Do not pool with historical provider Eval GT.'
 };
}
function selfTest(){
 const inps=baseNames.map(read),raw=Array.from({length:12},(_,i)=>read(shardName(i)));
 const q=compile(raw,inps);
 assert.equal(q.full_459_complete,true);
 assert.equal(q.V26_fresh_original_Valid_source_inferences,459);
 assert.equal(q.cohorts.M0.current_original_author_GT_boxes,3471);
 assert.equal(q.cohorts.M1.current_original_author_GT_boxes,3433);
 assert.equal(q.cohorts.M2.current_original_author_GT_boxes,3049);
 assert.equal(q.cohorts.M0.tp+q.cohorts.M0.fn,3471);
 assert.equal(q.cohorts.M0.tp+q.cohorts.M0.fp,q.cohorts.M0.new_original_RFDETR_model_boxes);
 const bad=structuredClone(raw);bad[0].rows[0].source_id='WRONG_ID';
 assert.throws(()=>compile(bad,inps));
 const bad2=structuredClone(raw);bad2[0].rows[0].model_id='WRONG_MODEL';
 assert.throws(()=>compile(bad2,inps));
 const bad3=structuredClone(raw);bad3[0].original_source_split='test';
 assert.throws(()=>compile(bad3,inps));
 const bad4=structuredClone(raw);bad4[0].rows[0].current_author_boxes[0].cls='UNRECOGNIZED';
 assert.throws(()=>compile(bad4,inps));
 const bad5=structuredClone(raw);bad5[0].rows[0].model_predictions[0].confidence=.01;
 assert.throws(()=>compile(bad5,inps));
 const partial=structuredClone(raw);partial[0].rows[0].status='FAIL_CLOSED';
 const p=compile(partial,inps);
 assert.equal(p.full_459_complete,false);
 assert.equal(p.V26_fresh_original_Valid_source_inferences,458);
 assert.equal(p.cohorts.M0.complete,false);
 console.log('SEER_V26_ALL_459_CURRENT_AUTHOR_BOXES_17_CLASSES_3_RISK_GROUPS_AND_NEGATIVE_TESTS_PASS');
}
try{
 const opt=process.argv[2]??'--audit';
 if(opt==='--self-test')selfTest();
 else if(opt==='--audit'){
  const q=compile(Array.from({length:12},(_,i)=>read(shardName(i))),baseNames.map(read));
  if(process.argv[3])writeFileSync(process.argv[3],JSON.stringify(q,null,2)+'\n');
  console.log(JSON.stringify({full_459_complete:q.full_459_complete,images:q.V26_fresh_original_Valid_source_inferences,
   cohorts:Object.fromEntries(Object.entries(q.cohorts).map(([k,v])=>[k,{images:v.images_scored,gt:v.current_original_author_GT_boxes,preds:v.new_original_RFDETR_model_boxes,tp:v.tp,fp:v.fp,fn:v.fn,precision:v.precision,recall:v.recall,f1:v.f1}]))},null,2));
  console.log('SEER_V26_459_VALID_NEW_ORIGINAL_MODEL_CURRENT_AUTHOR_BOX_EVALUATION_PASS');
 }else throw Error('Usage: --self-test | --audit [output.json]');
}catch(e){console.error(String(e));process.exitCode=2;}
