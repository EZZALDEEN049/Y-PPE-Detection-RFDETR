#!/usr/bin/env node
/* V26: compact deterministic source/reference-only results from verified full JSON. */
import {readFileSync,writeFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import assert from 'node:assert/strict';
const [input,summaryPath,reportPath]=process.argv.slice(2);
if(!input||!summaryPath||!reportPath)throw Error('Usage: node render_v26_current_valid_report.mjs <full> <summary> <report>');
const raw=readFileSync(input,'utf8'),v=JSON.parse(raw);
assert.equal(v.schema_version,'seer-ppe/v26-actual-original-valid-current-author-GT-detection-IoU50/v0.26');
assert.equal(v.full_459_complete,true);assert.equal(v.per_source.length,459);
assert.deepEqual(['M0','M1','M2'].map(k=>v.cohorts[k].images_scored),[459,448,367]);
assert.deepEqual(['M0','M1','M2'].map(k=>v.cohorts[k].current_original_author_GT_boxes),[3471,3433,3049]);
assert.equal(v.cohorts.M0.per_class.length,17);
assert.equal(v.SEER_policy_effectiveness_measured,false);
assert.equal(v.protected_Test_accessed,false);
const compact=x=>({
 images:x.images_scored,GT:x.current_original_author_GT_boxes,
 predictions:x.new_original_RFDETR_model_boxes,assisted_GT:x.current_author_model_assisted_annotation_markers,
 TP:x.tp,FP:x.fp,FN:x.fn,P:x.precision,R:x.recall,F1:x.f1,complete:x.complete,
 per_class:x.per_class.map(y=>({
  class_name:y.class_name,GT:y.current_author_GT_boxes,pred:y.new_original_model_boxes,
  images_with_GT:y.images_with_current_GT,assisted_GT:y.model_assisted_GT_markers,
  TP:y.tp,FP:y.fp,FN:y.fn,P:y.precision,R:y.recall,F1:y.f1,mean_matched_IoU:y.mean_matched_IoU
 }))
});
const summary={
 schema_version:'seer-ppe/v26-current-author-reference-full-459-compact/v0.26',
 date:v.date,original_model_id:v.original_model_id,
 actual_current_reference_459_complete:v.full_459_complete,
 input_full_detail_filename:'ACTUAL_CURRENT_SOURCE_ORIGINAL_VALID_459_CLASS_BBOX_METRICS_V26.json',
 input_full_detail_SHA256:createHash('sha256').update(raw).digest('hex'),
 confidence_floor:.2,hosted_overlap:.5,class_exact_IoU_threshold:.5,
 all_459_uniform_vectorized_model_inference:true,previously_V23_exposed_five_freshly_inferred:true,
 original_model_or_source_modified:false,original_source_independence_verified:false,
 SEER_safety_XAI_energy_superiority_evaluated:false,protected_test_used:false,
 historical_2025_provider_eval_not_current_GT_reference:true,
 current_reference_one_author_curation_no_second_reviewer_required:true,
 cohorts:Object.fromEntries(['M0','M1','M2'].map(k=>[k,compact(v.cohorts[k])])),
 sensitivities:Object.fromEntries(Object.entries(v.prespecified_descriptive_sensitivities).map(([k,x])=>[k,compact(x)])),
 historical_context_not_comparable:v.prior_2025_provider_eval_separate_context_only,
 exact_source_input_hashes:v.file_input_sha256
};
const pct=n=>n==null?'—':(n*100).toFixed(2)+'%';
const cohortLine=k=>{
 const x=summary.cohorts[k];
 return '| '+k+' | '+x.images+' | '+x.GT+' | '+x.predictions+' | '+x.TP+' | '+x.FP+' | '+x.FN+' | '+pct(x.P)+' | '+pct(x.R)+' | '+pct(x.F1)+' |';
};
const classRows=summary.cohorts.M0.per_class.map((x,i)=>{
 const y=summary.cohorts.M2.per_class[i];
 assert.equal(x.class_name,y.class_name);
 return '| '+x.class_name+' | '+x.GT+' | '+x.TP+' | '+x.FP+' | '+x.FN+' | '+pct(x.P)+' | '+pct(x.R)+' | '+pct(x.F1)+' | '+y.GT+' | '+pct(y.F1)+' |';
}).join('\n');
const sensitivity=Object.entries(summary.sensitivities).map(([k,x])=>
 '| '+k.replaceAll('_',' ')+' | '+x.images+' | '+x.GT+' | '+x.TP+' | '+x.FP+' | '+x.FN+' | '+pct(x.F1)+' |').join('\n');
const md=[
 '# SEER-PPE V26 — new current original Source Valid object-detection results',
 '',
 '**21 November 2026.** Actual fresh unmodified RF-DETR Small (17 classes) uniform vectorized hosted inference over ALL 459 already author-curated original Valid Source images, at confidence floor 0.20 and hosted overlap 0.50. Object-level class-exact greedy one-to-one original-coordinate bounding-box IoU >= 0.50. All 12 Source geometry shards and exact metadata/GT class counts passed tests. No original images/annotations/model weights modified, no Test used.',
 '',
 '## Current author Source Valid reference — actual V26 metrics',
 '',
 '| Cohort | Original images | Current GT boxes | New predicted boxes | TP | FP | FN | Precision | Recall | F1 |',
 '|:--|--:|--:|--:|--:|--:|--:|--:|--:|--:|',
 cohortLine('M0'),cohortLine('M1'),cohortLine('M2'),
 '',
 'M0=459 Clean17-matched original Valid images; M1=448 after historic holds/technical high-overlap exclusions; M2=367 technically unflagged but NOT independently acquired/certified. These class-exact IoU=0.50 object scores are NOT COCO mAP, PPE worker compliance or a SEER-PPE policy effect.',
 '',
 '## The original 17 detector classes — complete M0 and technical-risk M2 sensitivity',
 '',
 '| Original class | M0 GT | M0 TP | M0 FP | M0 FN | M0 P | M0 R | M0 F1 | M2 GT | M2 F1 |',
 '|:--|--:|--:|--:|--:|--:|--:|--:|--:|--:|',
 classRows,
 '',
 'The model class names beginning No (No Gloves, No Hard Hat, No Face Mask and similar) are annotated object categories, NOT proven worker-specific task-policy violations. No worker clearances, review outcomes, safety decisions, XAI explanation fidelity or physically metered Joules were evaluated.',
 '',
 '## Precommitted descriptive robustness checks',
 '',
 '| Filter (Source IDs fixed before V26 outcomes) | Images | Current GT | TP | FP | FN | F1 |',
 '|:--|--:|--:|--:|--:|--:|--:|',
 sensitivity,
 '',
 'The 13 original Source IDs excluded in one test are the pre-existing V20 current GT versus historical provider-GT count mismatches (16 additional current saved author boxes). The five V23 previously used original Valid pilot Source IDs were FRESHLY inferred in this uniform V26 workflow and remain development-exposed. Neither exclusion creates acquisition-independent validation.',
 '',
 '## Historical V20 versus newly computed V26 — keep results separated',
 '',
 'The 2025 model-v2 provider Eval had historical M0/M1/M2 micro-F1 0.885018 / 0.884642 / 0.880754. Its 2025 annotation geometry was not retrievable and current author boxes differ in 13 Source images; new V26 inference uses a different uniform vectorized execution. There is no scientifically controlled causal performance gain or loss to infer from the two sets of descriptive scores.',
 '',
 '## Reference provenance and research claim limits',
 '',
 'The author already curated and checked the original image labels, and they remain the accepted single-researcher current Source detection reference, without repeated manual inspection or a required second rater. Of M0 current boxes, 729/3471 carry existing model-assisted labeling provenance markers. The 459 original Valid images have historic model-development exposure and possibly shared source families; M2 excludes flags but does not establish independence.',
 '',
 'The V25 A2/A5 policy execution was proposal-only on 74 stored model boxes. The V26 object detector assessment does NOT test SEER A5 versus a strong selective reviewer, individual task mandates and false safe clearances, target-matched XAI faithfulness, actual human review, electrical Joules, or an independent external model generalization claim. The strict worker-safety gate is still NOT_FROZEN / scoring_ready=false.',
 '',
 '## Reproducible evidence',
 '',
 '- Full original current GT geometry and newly inferred prediction geometry: 12 numbered V26_ORIGINAL_VALID_GEOMETRY_SHARD files',
 '- Executable numeric IoU=0.5 scorer: tools/score_original_valid_current_boxes_v26.mjs',
 '- Full matching results by image, cue and class: ACTUAL_CURRENT_SOURCE_ORIGINAL_VALID_459_CLASS_BBOX_METRICS_V26.json',
 '- Compact current Source class metrics: V26_VALID_CURRENT_SOURCE_459_NUMERIC_SUMMARY.json',
 '- Exact 459 scope frozen before outcome: V26_FROZEN_FULL_CURRENT_SOURCE_VALID_BBOX_PROTOCOL_2026-11-21.md',
 '- Uniform vector batch inference: V26_FROZEN_VECTOR_BATCH_INFERENCE_ADDENDUM_2026-11-21.md',
 '- Distinct historic provider scores: HISTORICAL_VALID_INTERNAL_METRICS_V20.json',
 '',
 'The large full-result JSON is indexed by this compact summary and its SHA256 hash. No source-image bytes, HTTPS signed URLs, credentials or original Test data were published as part of V26.',
 ''
].join('\n');
writeFileSync(summaryPath,JSON.stringify(summary,null,2)+'\n');
writeFileSync(reportPath,md);
console.log('SEER_V26_COMPACT_17_CLASS_AND_M0_M1_M2_REPORT_FROM_REAL_FULL_RESULTS_PASS');
console.log(JSON.stringify({images:summary.cohorts.M0.images,P:summary.cohorts.M0.P,R:summary.cohorts.M0.R,F1:summary.cohorts.M0.F1,perClass:summary.cohorts.M0.per_class.length,sha:summary.input_full_detail_SHA256}));
