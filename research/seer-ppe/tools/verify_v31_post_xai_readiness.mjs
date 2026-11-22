#!/usr/bin/env node
/* Independent, read-only post-V30 source-lineage and human-reference readiness gate.
   It NEVER opens images, Test, model endpoints, Roboflow, or review UI. */
import fs from 'node:fs';
import assert from 'node:assert/strict';
import path from 'node:path';
import {fileURLToPath} from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const read = name => JSON.parse(fs.readFileSync(path.join(root, name), 'utf8'));
const expected = {
  RETAIN_PREEXISTING_RESEARCH_HOLD: 5,
  TECHNICAL_OVERLAP_QUARANTINE_PENDING_REVIEW: 6,
  SOURCE_FAMILY_REVIEW_PENDING: 81,
  NO_SCREEN_FLAG_INDEPENDENCE_UNCERTIFIED: 367,
};

function audit(source, sig, validHuman, trainHuman, trainLive, v30, ready) {
  assert.equal(v30.audit_status, 'PASS_NUMERIC_INTEGRITY_ONLY');
  assert.equal(v30.rankable_curve_targets, 10);
  assert.equal(v30.v30_total_model_calls, 1068);
  assert.equal(v30.original_eight_image_sha256_match_cloud_preflight, true);
  assert.equal(source.clean17_valid_count, 459);
  assert.equal(source.original_valid_count, 468);
  assert.equal(source.previously_excluded_original_valid, 9);
  assert.equal(source.image_rows.length, 459);
  assert.equal(new Set(source.image_rows.map(r=>r.source_id)).size, 459);
  assert.ok(source.image_rows.every(r=>
    r.split === undefined &&
    r.eligible_for_scientific_scoring === false &&
    r.signed_source_family_verdict === null &&
    r.technical_correspondence_sha_verified === true));
  const counts = Object.fromEntries(Object.keys(expected).map(k=>[k,0]));
  for (const row of source.image_rows) {
    assert.ok(Object.prototype.hasOwnProperty.call(counts, row.V14_risk_bucket));
    counts[row.V14_risk_bucket]++;
  }
  assert.deepEqual(counts, expected);
  assert.equal(source.per_image_source_family_human_decisions_signed, 0);
  assert.equal(source.human_independence_attestations, 0);
  assert.equal(source.scoring_ready, false);
  assert.equal(source.test_images_accessed, false);
  assert.deepEqual(sig.decisions, []);
  assert.equal(sig.scoring_authorized, false);
  assert.equal(sig.test_source_ids_used, false);
  assert.deepEqual(validHuman.cases, []);
  assert.equal(validHuman.scoring_ready, false);
  assert.equal(validHuman.test_authorized, false);
  assert.deepEqual(trainHuman.case_B_visual_decisions, []);
  assert.equal(trainHuman.case_D_zero_person_decision, null);
  assert.equal(trainHuman.completed_human_reference, false);
  assert.equal(trainLive.totals.associations, 19);
  assert.equal(trainLive.totals.visual_reviewed_cells, 38);
  assert.equal(trainLive.totals.visual_missing_cells, 4);
  assert.equal(trainLive.model_scoring_ready, false);
  const caseB = trainLive.cases.find(c=>c.case==='B');
  const caseD = trainLive.cases.find(c=>c.case==='D');
  assert.equal(caseB.missing_visual_cells.length, 4);
  assert.equal(caseD.ground_truth_state, 'incomplete');
  const priority = source.image_rows.filter(r=>
    ['RETAIN_PREEXISTING_RESEARCH_HOLD',
     'TECHNICAL_OVERLAP_QUARANTINE_PENDING_REVIEW'].includes(r.V14_risk_bucket)
  ).map(r=>({id:r.source_id,filename:r.source_filename,bucket:r.V14_risk_bucket}));
  assert.equal(priority.length, 11);
  assert.equal(ready.true_worker_safety_scoring_ready, false);
  assert.equal(ready.independent_source_eligible_valid_images, 0);
  assert.equal(ready.independently_signed_source_family_verdicts, 0);
  assert.equal(ready.signed_valid_human_worker_references, 0);
  assert.equal(ready.original_valid_source_images, 468);
  assert.equal(ready.clean17_valid_mapped_images, 459);
  assert.equal(ready.previously_excluded_valid_sources, 9);
  assert.equal(ready.source_priority_review_packets.case_count, 11);
  assert.deepEqual(ready.current_cohort_buckets, {
    preexisting_source_holds: 5,
    v14_technical_overlap_quarantine: 6,
    other_flagged_unsigned: 81,
    unflagged_but_independence_unsigned: 367,
  });
  const readyP = ready.source_priority_review_packets.source_ids;
  assert.deepEqual(readyP.map(x=>({id:x.valid_source_id, filename:x.original_filename,
    bucket:x.risk_bucket})), priority);
  assert.deepEqual(ready.human_train_pilot_history.unentered_cells,
    caseB.missing_visual_cells.map(x=>'B:'+x));
  assert.equal(ready.human_train_pilot_history.general_author_visual_image_review_accepted, true);
  assert.equal(ready.human_train_pilot_history.repeat_author_original_image_review_requested, false);
  assert.equal(ready.policy_decision_rules.original_test_must_remain_unopened, true);
  assert.equal(ready.policy_decision_rules.no_source_hold_is_lifted_by_this_record, true);
  assert.equal(ready.policy_decision_rules.no_training_or_model_inference_for_this_step, true);
  assert.ok(ready.next_work_packages.every(x=>x.cannot_auto_sign===true));
  return {status:'PASS_V31_READ_ONLY_GAP_LEDGER',
    v30_audit_passed:true, mapped_valid:459, source_bucket_counts:counts,
    priority_conflict_cases:11, source_signed:0, valid_human_signed:0,
    preserved_train_links:19, preserved_train_visual_states:38,
    train_B_unentered_visual_states:4, true_worker_safety_scoring_ready:false,
    no_test_or_model_calls:true};
}

const source=read('VALIDATION_459_SIGNED_SOURCE_COHORT_READINESS_V15.json');
const sig=read('SOURCE_FAMILY_SIGNED_ATTESTATIONS_V15.json');
const validHuman=read('VALIDATION_PERSON_PPE_SIGNED_REFERENCE_V15.json');
const trainHuman=read('TRAIN_REFERENCE_SIGNED_ATTESTATIONS_V15.json');
const trainLive=read('PERSON_PPE_LIVE_READINESS_2026-11-21_V01.json');
const v30=read('V30_INDEPENDENT_NUMERIC_AUDIT_2026-11-22.json');
const ready=read('V31_SOURCE_PERSON_SAFETY_READINESS_2026-11-22.json');
try {
  const result=audit(source,sig,validHuman,trainHuman,trainLive,v30,ready);
  if(process.argv.includes('--self-test')){
    for(const modify of [
      x=>{x.true_worker_safety_scoring_ready=true;},
      x=>{x.signed_valid_human_worker_references=1;},
      x=>{x.source_priority_review_packets.source_ids.pop();},
      x=>{x.policy_decision_rules.original_test_must_remain_unopened=false;},
    ]){
      const bad=structuredClone(ready);modify(bad);
      assert.throws(()=>audit(source,sig,validHuman,trainHuman,trainLive,v30,bad));
    }
    console.log('V31_MUTATION_SELF_TEST_FAIL_CLOSED_PASS');
  } else if(process.argv.includes('--verify')){
    console.log(JSON.stringify(result,null,2));
  } else {
    console.error('Use --self-test or --verify');
    process.exitCode=2;
  }
} catch(err) {
  console.error('V31_READINESS_LEDGER_FAILED_CLOSED',err.message);
  process.exitCode=1;
}
