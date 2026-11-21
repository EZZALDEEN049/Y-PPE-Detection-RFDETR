#!/usr/bin/env node
/**
 * SEER-PPE V27 deterministic scorer.
 * Reads frozen target manifest, actual Roboflow target-occlusion outputs,
 * and the already-existing V23 current-label bbox match ledger.
 * V23 outcomes are joined only after selection and never enter A5/A6 ranking.
 */
import assert from 'node:assert/strict';
import {readFileSync,writeFileSync} from 'node:fs';
import {resolve} from 'node:path';
const ROOT=resolve(new URL('..',import.meta.url).pathname);
const read=n=>JSON.parse(readFileSync(resolve(ROOT,n),'utf8'));
const targets=read('V27_FROZEN_TARGETS_2026-11-21.json');
const runs=read('V27_ACTUAL_TARGETED_OCCLUSION_RESULTS_2026-11-22.json');
const v23=read('VALID_CURRENT_SOURCE_REAL_MODEL_BOX_MATCH_V23.json');
const need=(x,m)=>assert.ok(x,'SEER_V27_SCORE_BLOCKED:'+m);
const round=x=>Number(x.toFixed(6));
const mean=a=>a.length?round(a.reduce((s,x)=>s+x,0)/a.length):null;
need(targets.schema_version==='seer-ppe/v27-frozen-targeted-occlusion-sample-and-A6-class-error-calibrated-comparator/v0.27','frozen target schema');
need(runs.schema_version==='seer-ppe/v27-actual-original-model-target-box-occlusion-results/v0.27','actual run schema');
need(v23.schema_version==='seer-ppe/v23-actual-current-label-five-valid-descriptive-box-match/v0.23','V23 ledger schema');
need(runs.summary.target_workflows_completed===10&&runs.summary.actual_model_inference_passes_confirmed===27,'10 targets / 27 passes');
need(runs.results.length===10&&runs.results.every(x=>x.workflow_status==='completed'&&x.target_filter_count===1),'all target filters exact one');
need(runs.results.filter(x=>x.control_id).every(x=>x.control_filter_count===1),'all seven controls exact one');
const byTarget=new Map(runs.results.map(x=>[x.target_id,x]));
const bySource=new Map(v23.per_source.map(x=>[x.source_id,x]));
const shared=targets.unique_A5_A6_target_tests.filter(x=>x.arms.includes('A5')&&x.arms.includes('A6'));
const uniqueA5=targets.unique_A5_A6_target_tests.filter(x=>x.arms.length===1&&x.arms[0]==='A5');
const uniqueA6=targets.unique_A5_A6_target_tests.filter(x=>x.arms.length===1&&x.arms[0]==='A6');
need(shared.length===6&&uniqueA5.length===2&&uniqueA6.length===2,'matched target counts');
const arms={};
for(const arm of ['A5','A6']){
 const selected=targets.per_image_selections.filter(x=>x.selected?.[arm]).map(x=>{
  const id=x.selected[arm],r=byTarget.get(id);
  need(r,'missing actual target result '+id);
  let v23Status=null,v23Iou=null;
  if(x.split==='valid'){
   const s=bySource.get(x.asset_id);
   const event=s?.matched_pred_events?.find(e=>e.pred_id===id);
   need(event,'missing post-selection V23 match '+id);
   v23Status=event.status;v23Iou=event.matched_bbox_iou??event.best_unmatched_bbox_iou??null;
  }
  return {image_key:x.image_key,filename:x.filename,split:x.split,target_id:id,
   target_class:x.selected[arm+'_class'],baseline_confidence:r.baseline_target?.confidence??null,
   target_confidence_drop:r.target_confidence_drop,target_detection_retained:r.target_detection_retained,
   control_confidence_drop:r.control_confidence_drop,specificity_margin:r.specificity_margin,
   v23_postselection_status:v23Status,v23_bbox_iou:v23Iou};
 });
 const controlled=selected.filter(x=>x.specificity_margin!==null);
 const valid=selected.filter(x=>x.split==='valid');
 arms[arm]={selected_slots:selected.length,
  target_detection_lost:selected.filter(x=>x.target_detection_retained===false).length,
  target_detection_retained:selected.filter(x=>x.target_detection_retained===true).length,
  mean_baseline_confidence:mean(selected.map(x=>x.baseline_confidence).filter(Number.isFinite)),
  mean_target_confidence_drop:mean(selected.map(x=>x.target_confidence_drop).filter(Number.isFinite)),
  controlled_targets:controlled.length,
  mean_control_confidence_drop:mean(controlled.map(x=>x.control_confidence_drop).filter(Number.isFinite)),
  mean_specificity_margin:mean(controlled.map(x=>x.specificity_margin)),
  valid_selected_targets:valid.length,
  valid_selected_TP:valid.filter(x=>x.v23_postselection_status==='TP').length,
  valid_selected_FP:valid.filter(x=>x.v23_postselection_status==='FP').length,
  selected_targets:selected};
}
need(arms.A5.selected_slots===8&&arms.A6.selected_slots===8,'equal arm slots');
need(arms.A5.valid_selected_targets===4&&arms.A6.valid_selected_targets===4,'four valid targets per arm');
need(arms.A5.valid_selected_TP===4&&arms.A5.valid_selected_FP===0,'A5 V23 postselection alignment');
need(arms.A6.valid_selected_TP===3&&arms.A6.valid_selected_FP===1,'A6 V23 postselection alignment');
const out={
 schema_version:'seer-ppe/v27-a5-a6-matched-budget-occlusion-and-postselection-detection-alignment/v0.27',
 date:'2026-11-22',equal_budget:{A5:arms.A5.selected_slots,A6:arms.A6.selected_slots,shared:shared.length,unique_A5:uniqueA5.length,unique_A6:uniqueA6.length},
 xai_arm_comparison:arms,
 postselection_valid_detection_error_alignment:{A5:{TP:arms.A5.valid_selected_TP,FP:arms.A5.valid_selected_FP},
  A6:{TP:arms.A6.valid_selected_TP,FP:arms.A6.valid_selected_FP}},
 constraints:{no_test_accessed:true,V23_outcomes_used_for_selection:false,
  source_independence_verified:false,worker_compliance_measured:false,strict_worker_safety_scoring_ready:false}
};
const outPath=process.argv[2]??resolve(ROOT,'V27_A5_A6_COMPARISON_2026-11-22.json');
writeFileSync(outPath,JSON.stringify(out,null,2));
console.log(JSON.stringify({A5:arms.A5,A6:arms.A6,shared:shared.length,uniqueA5:uniqueA5.length,uniqueA6:uniqueA6.length},null,2));
