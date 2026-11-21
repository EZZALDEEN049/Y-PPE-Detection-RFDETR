#!/usr/bin/env node
/**
 * V28 deterministic scorer: one-step black-fill deletion and target-only
 * insertion/sufficiency probes, paired by frozen target ID to V27 blur.
 */
import assert from 'node:assert/strict';
import {readFileSync,writeFileSync} from 'node:fs';
import {resolve} from 'node:path';
const ROOT=resolve(new URL('..',import.meta.url).pathname);
const read=n=>JSON.parse(readFileSync(resolve(ROOT,n),'utf8'));
const targets=read('V27_FROZEN_TARGETS_2026-11-21.json');
const v27=read('V27_ACTUAL_TARGETED_OCCLUSION_RESULTS_2026-11-22.json');
const v28=read('V28_ACTUAL_TARGET_BOX_DELETION_INSERTION_RESULTS_2026-11-22.json');
const need=(x,m)=>assert.ok(x,'SEER_V28_SCORE_BLOCKED:'+m);
const round=x=>Number(x.toFixed(6)),mean=a=>a.length?round(a.reduce((s,x)=>s+x,0)/a.length):null;
need(targets.unique_A5_A6_target_tests.length===10,'10 frozen target IDs');
need(v27.summary.actual_model_inference_passes_confirmed===27,'V27 27 passes');
need(v28.summary.archived_repeat_model_inference_passes===30&&
 v28.summary.uncaptured_initial_attempt_model_inference_passes===30,'V28 60 pass accounting');
need(v28.results.length===10&&v28.results.every(x=>x.workflow_status==='completed'&&x.target_filter_count===1),'all V28 target filters exact one');
const a=new Map(v27.results.map(x=>[x.target_id,x])),b=new Map(v28.results.map(x=>[x.target_id,x]));
need(targets.unique_A5_A6_target_tests.every(x=>a.has(x.target_id)&&b.has(x.target_id)),'target ID pairing');
const arms={};
for(const arm of ['A5','A6']){
 const rows=targets.per_image_selections.filter(x=>x.selected?.[arm]).map(x=>{
  const id=x.selected[arm],p=a.get(id),q=b.get(id);need(p&&q,'missing target '+id);
  return {target_id:id,image_key:x.image_key,target_class:x.selected[arm+'_class'],
   area_fraction:q.target_area_fraction,V27_blur_drop:p.target_confidence_drop,
   V27_blur_retained:p.target_detection_retained,
   V28_deletion_drop:q.deletion_confidence_drop,V28_deletion_retained:q.deletion_detection_retained,
   V28_insertion_confidence:q.insertion_confidence,V28_insertion_delta:q.insertion_confidence_delta,
   V28_insertion_ratio:q.insertion_sufficiency_ratio,V28_insertion_retained:q.insertion_detection_retained};
 });
 need(rows.length===8,'equal eight target slots '+arm);
 arms[arm]={selected_slots:8,
  deletion_lost:rows.filter(x=>x.V28_deletion_retained===false).length,
  mean_deletion_drop:mean(rows.map(x=>x.V28_deletion_drop)),
  insertion_retained:rows.filter(x=>x.V28_insertion_retained===true).length,
  insertion_lost:rows.filter(x=>x.V28_insertion_retained===false).length,
  mean_insertion_confidence:mean(rows.map(x=>x.V28_insertion_confidence)),
  mean_insertion_ratio:mean(rows.map(x=>x.V28_insertion_ratio)),targets:rows};
}
need(arms.A5.deletion_lost===8&&arms.A6.deletion_lost===8,'black deletion target loss');
need(arms.A5.insertion_retained===6&&arms.A6.insertion_retained===6,'insertion retained slots');
const output={schema_version:'seer-ppe/v28-a5-a6-matched-budget-deletion-insertion-comparison/v0.28',
 date:'2026-11-22',A5:arms.A5,A6:arms.A6,
 constraints:{no_test_accessed:true,source_independence_verified:false,
  worker_compliance_measured:false,full_progressive_curves:false,strict_worker_safety_scoring_ready:false}};
const out=process.argv[2]??resolve(ROOT,'V28_A5_A6_DELETION_INSERTION_COMPARISON_2026-11-22.json');
writeFileSync(out,JSON.stringify(output,null,2)+'\n');
console.log(JSON.stringify({A5:arms.A5,A6:arms.A6},null,2));
