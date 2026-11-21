#!/usr/bin/env node
/**
 * V23: five actually inferred ORIGINAL Source Valid photos scored against
 * CURRENT saved author-curated Source boxes, using a pre-committed protocol.
 * Fixed RF-DETR Small v2, confidence floor 0.20, overlap 0.50, IoU 0.50.
 * The five were deliberately fixed before infer; all are development-exposed.
 * Not random/independent/generalizable; no full 459-Valid benchmark, no XAI,
 * safety mandate, worker compliance, SEER comparator or Test metrics.
 */
import assert from 'node:assert/strict';
import {readFileSync,writeFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import {resolve} from 'node:path';
import {fileURLToPath} from 'node:url';
const ROOT=resolve(fileURLToPath(new URL('..',import.meta.url)));
const fs={
pilot:'VALID_ORIGINAL_SOURCE_CURRENT_BBOX_MODEL_PILOT_V23.json',
counts:'V20_VALID_SOURCE_ANNOTATION_COUNTS_PART1_PRIVATE_WORKING.json',
risk:'VALIDATION_SOURCE_OVERLAP_NUMERIC_SENSITIVITY_V19.json',
v20:'HISTORICAL_VALID_INTERNAL_METRICS_V20.json',
protocol:'V23_VALID_CURRENT_BOX_GEOMETRY_FROZEN_PILOT_PROTOCOL.md'
};
const read=n=>JSON.parse(readFileSync(resolve(ROOT,n),'utf8'));
const sha=n=>createHash('sha256').update(readFileSync(resolve(ROOT,n))).digest('hex');
const need=(x,msg)=>{if(!x)throw Error('SEER_V23_READ_ONLY_CURRENT_BOX_VALID_PILOT_BLOCKED:'+msg)};
const model='altayyar-0oflt-lafos-qqauz/2';
const chosen=[
['07BnOpgFJyNaOhuzvh5i','image_1282.jpg',13],
['084u5kuwQXhWa4EKdsQ5','5731201_4.jpg',1],
['09WO3iVNf9jOt21QAxmb','c1e5a26df8225afb5be5beceae128ad5.jpg',3],
['0ABzMrjnd6I0Ws6FH7qo','imagem40.jpg',5],
['0aGYjxE5LmocXyvuLHs8','a16ea468abd845e68ea9ccbbe4f9762e.jpg',1]
];
const CLASS=new Set(['Animal','Child','Face Masks','No Hard Hat','No Safety Boots','Soft Hat',
 'Hard Hat','No Safety Vest','Pants','No Face Mask','No Safety Attire','No Gloves',
 'Gloves','Safety Boots','Safety Vests','Goggles','Persons']);
const isBox=z=>[z.x,z.y,z.width,z.height].every(Number.isFinite)&&
z.width>0&&z.height>0;
const bound=(b,w,h)=>{
 need(isBox(b),'invalid source/native box coordinates');
 const x1=Math.max(0,b.x-b.width/2),y1=Math.max(0,b.y-b.height/2);
 const x2=Math.min(w,b.x+b.width/2),y2=Math.min(h,b.y+b.height/2);
 need(x2>x1&&y2>y1,'box collapsed after image bounding');
 return [x1,y1,x2,y2];
};
function overlap(a,b){
 const dx=Math.max(0,Math.min(a[2],b[2])-Math.max(a[0],b[0]));
 const dy=Math.max(0,Math.min(a[3],b[3])-Math.max(a[1],b[1]));
 const intersection=dx*dy;
 const area=x=>(x[2]-x[0])*(x[3]-x[1]);
 return intersection/(area(a)+area(b)-intersection);
}
function compile(pilot,counts,risk,v20){
 need(pilot.schema_version==='seer-ppe/actual-hosted-valid-pilot-current-original-gt-pred-bboxes/v0.23'&&
   pilot.model_id===model&&
   pilot.source_project==='softyyemen/altayyar-0oflt-lafos-qqauz'&&
   pilot.selected_image_count===5&&pilot.original_current_reference_count===23&&
   pilot.new_hosted_inference_count===5&&pilot.no_test_accessed===true&&
   pilot.original_images_annotations_and_splits_untouched===true&&
   pilot.original_model_unchanged===true&&
   pilot.no_source_image_bytes_or_urls_saved===true&&
   pilot.scientific_independent_validation===false&&
   pilot.person_level_PPE_compliance_measured===false&&
   pilot.SEER_policy_comparison_executed===false&&pilot.scoring_ready===false,
   'pilot provenance or protected scientific scope violation');
 need(counts.schema_version==='seer-ppe/read-only-valid-source-annotation-counts-part/v0.20'&&
   counts.split==='valid'&&counts.read_only===true&&counts.source_annotations_modified===false,
   'GT source current snapshot changed');
 need(risk.schema_version==='seer-ppe/validation-source-computational-sensitivity-screen/v0.19'&&
   risk.source_family_groups_are_hypotheses_not_confirmed_acquisition_ids===true&&
   risk.independent_valid_scientific_cohort_size===0&&risk.scoring_ready===false&&
   risk.test_sources_or_images_accessed===false,
   'source ID risk screen or independence status unexpected');
 need(v20.schema_version==='seer-ppe/historical-internal-valid-model-eval-three-risk-cohorts/v0.20'&&
   v20.model===model&&v20.existing_evaluation_id==='KyzP9neuyNTN5eQpGCAY'&&
   v20.test_not_read===true&&v20.source_independence_verified===false&&
   v20.historical_counters_not_recomputed_against_current_source_box_geometry===true,
   'historic V20 version2 baseline reference changed');
 const expected=chosen.map(x=>x[0]);
 const m2=risk.descriptive_sensitivity_scenarios.UNFLAGGED_ONLY_BUT_UNCERTIFIED_367.source_ids;
 need(JSON.stringify(m2.slice(0,5))===JSON.stringify(expected),
   'pilot IDs must be first five source IDs of preexisting M2, selected before outcomes');
 need(JSON.stringify(pilot.selection_predeclared_ids)===JSON.stringify(expected)&&
   Array.isArray(pilot.rows)&&pilot.rows.length===5,'pilot source membership not fixed');
 const sourceCounts=new Map(counts.rows.map(x=>[x.source_id,x]));
 const inputIDs=new Set(),inferIDs=new Set(),analyses=[],overallClass=new Map();
 let totalGt=0,totalPred=0,totalTp=0,totalFp=0,totalFn=0,assisted=0;
 const classes=[...CLASS].sort();
 const tally=Object.fromEntries(classes.map(c=>[c,{gt:0,pred:0,tp:0,fp:0,fn:0}]));
 for(let i=0;i<chosen.length;i++){
   const row=pilot.rows[i],ex=chosen[i];
   need(row.source_id===ex[0]&&row.original_filename===ex[1]&&
     row.split==='valid'&&row.selection==='LEXICOGRAPHIC_FIRST_5_FROM_M2_UNFLAGGED_NOT_CERTIFIED'&&
     !inputIDs.has(row.source_id)&&row.model_id===model&&
     row.confidence_floor===0.2&&row.overlap_parameter===0.5&&
     Number.isInteger(row.image_width)&&row.image_width>0&&
     Number.isInteger(row.image_height)&&row.image_height>0&&
     row.annotation_valid===true&&Array.isArray(row.current_author_labels)&&
     row.current_author_labels.length===ex[2]&&Array.isArray(row.predictions)&&
     typeof row.model_inference_id==='string'&&row.model_inference_id.length>0&&
     !inferIDs.has(row.model_inference_id),'image/source model alignment or annotation integrity failed');
   inputIDs.add(row.source_id);inferIDs.add(row.model_inference_id);
   const old=sourceCounts.get(row.source_id);
   need(old?.source_original_filename===row.original_filename&&
     old.width===row.image_width&&old.height===row.image_height&&
     old.saved_object_count===ex[2]&&
     old.annotation_group_version===row.original_source_annotation_group_version,
     'current Source annotation version/count/dimension changed');
   const curCounts={};
   const refIDs=new Set();
   const refs=row.current_author_labels.map(g=>{
     need(typeof g.annotation_id==='string'&&!refIDs.has(g.annotation_id)&&
       CLASS.has(g.class_name),'GT duplicated ID or invalid source class');
     refIDs.add(g.annotation_id);
     curCounts[g.class_name]=(curCounts[g.class_name]||0)+1;
     return {...g,box:bound(g,row.image_width,row.image_height)};
   });
   need(Object.keys(curCounts).every(k=>curCounts[k]===old.class_counts[k])&&
     Object.keys(old.class_counts).every(k=>old.class_counts[k]===curCounts[k]),
     'annotation class labels changed since current V20 Source read');
   const assistedN=refs.filter(g=>g.labeled_by_model!==null).length;
   need(assistedN===old.model_assisted_marker_count,'annotation assistance provenance changed');
   assisted+=assistedN;
   const predictionIDs=new Set();
   const preds=row.predictions.map(p=>{
     need(typeof p.id==='string'&&!predictionIDs.has(p.id)&&
       CLASS.has(p.class_name)&&Number.isFinite(p.confidence)&&p.confidence>=0.2&&p.confidence<=1,
       'invalid class, confidence, prediction ID or hosted 0.2 floor');
     predictionIDs.add(p.id);
     return {...p,box:bound(p,row.image_width,row.image_height)};
   }).sort((a,b)=>b.confidence-a.confidence||a.id.localeCompare(b.id));
   const used=new Set(),events=[];
   for(const p of preds){
     const classRow=tally[p.class_name];classRow.pred++;
     let best=null,bestIoU=-1;
     for(const g of refs){
       if(used.has(g.annotation_id)||g.class_name!==p.class_name)continue;
       const v=overlap(p.box,g.box);
       if(v>bestIoU+1e-12||
         (Math.abs(v-bestIoU)<1e-12&&best&&g.annotation_id<best.annotation_id)){
         best=g;bestIoU=v;
       }
     }
     if(best&&bestIoU+1e-10>=0.50){
       used.add(best.annotation_id);classRow.tp++;
       events.push({pred_id:p.id,class_name:p.class_name,status:'TP',
         original_annotation_id:best.annotation_id,matched_bbox_iou:Number(bestIoU.toFixed(6))});
     }else{
       classRow.fp++;
       events.push({pred_id:p.id,class_name:p.class_name,status:'FP',
         original_annotation_id:null,best_unmatched_bbox_iou:bestIoU<0?null:Number(bestIoU.toFixed(6))});
     }
   }
   const missed=refs.filter(g=>!used.has(g.annotation_id));
   for(const g of refs)tally[g.class_name].gt++;
   for(const g of missed)tally[g.class_name].fn++;
   const tp=used.size,fp=preds.length-tp,fn=missed.length;
   need(tp+fn===refs.length&&tp+fp===preds.length,'per-source conservation mismatch');
   totalGt+=refs.length;totalPred+=preds.length;totalTp+=tp;totalFp+=fp;totalFn+=fn;
   const fscore=(a,b,c)=>2*a+b+c?2*a/(2*a+b+c):null;
   analyses.push({
     source_id:row.source_id,original_filename:row.original_filename,
     historically_exposed_validation:true,
     source_independence_verified:false,
     boxes_current_author_reference:refs.length,model_prediction_boxes:preds.length,
     model_assisted_current_source_ref_boxes:assistedN,
     tp,fp,fn,precision:tp+fp?Number((tp/(tp+fp)).toFixed(6)):null,
     recall:tp+fn?Number((tp/(tp+fn)).toFixed(6)):null,
     f1:fscore(tp,fp,fn)===null?null:Number(fscore(tp,fp,fn).toFixed(6)),
     matched_pred_events:events,
     unmatched_original_annotation_ids:missed.map(g=>g.annotation_id)
   });
 }
 need(totalGt===23&&totalPred===pilot.rows.reduce((s,x)=>s+x.predictions.length,0)&&
   totalTp+totalFn===23&&totalTp+totalFp===totalPred&&inputIDs.size===5&&inferIDs.size===5,
   'global current-source and predictor conservation violated');
 const micro={
   images:5,current_author_reference_boxes:totalGt,new_original_model_prediction_boxes:totalPred,
   tp:totalTp,fp:totalFp,fn:totalFn,
   precision:totalTp+totalFp?Number((totalTp/(totalTp+totalFp)).toFixed(6)):null,
   recall:totalTp+totalFn?Number((totalTp/(totalTp+totalFn)).toFixed(6)):null,
   f1:2*totalTp+totalFp+totalFn?Number((2*totalTp/(2*totalTp+totalFp+totalFn)).toFixed(6)):null,
   source_label_assistance_markers:assisted
 };
 return {
   schema_version:'seer-ppe/v23-actual-current-label-five-valid-descriptive-box-match/v0.23',
   date:'2026-11-21',scope:'ACTUAL_FIXED_MODEL_5_VALID_SOURCE_IMAGES_CURRENT_AUTHOR_LABEL_BOX_IOU_ONLY',
   original_model_id:model,confidence_floor:0.2,overlap_parameter:0.5,box_iou_threshold:0.5,
   original_model_modified:false,original_dataset_or_annotations_modified:false,
   new_real_hosted_inference_calls:5,
   original_valid_source_selection:'BEFORE_PREDICTIONS_FIRST_5_LEXICOGRAPHIC_M2_UNFLAGGED_UNCERTIFIED',
   historical_development_exposure:true,
   has_independent_validation_or_test_claim:false,
   source_independence_verified:false,worker_safety_compliance_scored:false,
   new_SEER_comparator_or_XAI_routing_experiment:false,physically_metered_energy:false,
   strict_independent_worker_safety_scoring_ready:false,test_source_or_evaluation_accessed:false,
   prior_2025_legacy_eval_NOT_USED_as_current_label_prediction:true,
   input_sha256:Object.fromEntries(Object.entries(fs).map(([k,p])=>[k,sha(p)])),
   source_pilot_box_match:micro,
   per_source:analyses,
   per_original_class:classes.map(c=>({class_name:c,...tally[c]})).filter(x=>x.gt||x.pred),
   interpretation:'Five deliberately chosen original Valid images, already historically exposed to development; numeric box-alignment implementation preflight only, no current 459-image population claim and no occupational PPE clearance/SEER efficacy inference.'
 };
}
function test(){
 const data=[read(fs.pilot),read(fs.counts),read(fs.risk),read(fs.v20)];
 const z=compile(...data);
 assert.equal(z.source_pilot_box_match.images,5);
 assert.equal(z.source_pilot_box_match.current_author_reference_boxes,23);
 const bad=structuredClone(data[0]);bad.rows[0].split='test';
 assert.throws(()=>compile(bad,...data.slice(1)));
 const bad2=structuredClone(data[0]);bad2.rows[0].model_id='wrong';
 assert.throws(()=>compile(bad2,...data.slice(1)));
 const bad3=structuredClone(data[0]);bad3.rows[0].current_author_labels[0].class_name='Imaginary PPE';
 assert.throws(()=>compile(bad3,...data.slice(1)));
 const bad4=structuredClone(data[0]);bad4.scientific_independent_validation=true;
 assert.throws(()=>compile(bad4,...data.slice(1)));
 const bad5=structuredClone(data[1]);bad5.rows.find(x=>x.source_id===chosen[0][0]).saved_object_count+=1;
 assert.throws(()=>compile(data[0],bad5,data[2],data[3]));
 const bad6=structuredClone(data[2]);bad6.independent_valid_scientific_cohort_size=367;
 assert.throws(()=>compile(data[0],data[1],bad6,data[3]));
 console.log('SEER_V23_CURRENT_BBOX_REAL_VALID_PILOT_WRONG_SPLIT_MODEL_CLASS_GT_ID_INDEPENDENCE_SELFTESTS_PASS');
}
try{
 const arg=process.argv[2]||'--audit';
 if(arg==='--self-test')test();
 else if(arg==='--audit'){
  const z=compile(read(fs.pilot),read(fs.counts),read(fs.risk),read(fs.v20));
  if(process.argv[3])writeFileSync(process.argv[3],JSON.stringify(z,null,2)+'\n');
  console.log(JSON.stringify({n:z.source_pilot_box_match.images,metrics:z.source_pilot_box_match,
   sources:z.per_source.map(x=>({id:x.source_id,gt:x.boxes_current_author_reference,
    predicted:x.model_prediction_boxes,tp:x.tp,fp:x.fp,fn:x.fn})),
   valid_pilot_only:true,test_used:false,worker_compliance_scored:false},null,2));
  console.log('SEER_V23_FIXED_RFDETR_REAL_VALID_SOURCE_CURRENT_AUTHOR_BOX_MATCH_PASS');
 } else throw Error('Usage --self-test | --audit [file]');
}catch(e){console.error(String(e));process.exitCode=2;}
