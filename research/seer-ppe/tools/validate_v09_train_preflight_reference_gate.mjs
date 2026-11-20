#!/usr/bin/env node
/**
 * SEER-PPE research engineering-only check:
 * train-only Workflow diagnostic output and saved human reference stay distinct.
 * Do NOT compute true/false positive metrics or evaluate on Valid/Test.
 */
import { readFileSync } from 'node:fs';
import assert from 'node:assert/strict';

const base = new URL('../', import.meta.url);
const read = name => JSON.parse(readFileSync(new URL(name, base), 'utf8'));
const manifest = read('SOURCE_ID_MANIFEST_TRAIN_VALID_2026-11-19_V01.json');
const pilot = read('TRAIN_ONLY_UNSCORED_PREFLIGHT_2026-11-21_V09.json');
const reference = read('PERSON_PPE_REFERENCE_LIVE_SNAPSHOT_2026-11-21_V09.json');
const approvedVisualReview = read('AUTHOR_VISUAL_REVIEW_ACCEPTANCE_2026-11-21_V08.json');

const byId = new Map(manifest.images.map(x => [x.image_id, x]));
assert.equal(manifest.images.length, 2093);
assert.equal(byId.size, 2093);
assert.equal(manifest.images.filter(x => x.split === 'test').length, 0);
assert.equal(pilot.sample_count, 4);
assert.equal(pilot.image_split, 'train');
assert.equal(pilot.evaluated_test_or_valid_images, 0);
assert.equal(pilot.model, 'altayyar-0oflt-lafos-qqauz/2');
assert.equal(pilot.workflow.id, '61llCTFuQ4Aq4goQ9HiP');
assert.equal(pilot.workflow.disable_active_learning, true);
assert.equal(pilot.workflow.custom_candidate_confidence_threshold, 0.2);
assert.equal(pilot.workflow.high_confidence_cue_threshold, 0.6);
assert.deepEqual(pilot.cases.map(x => x.case), ['A','B','C','D']);

for (const row of pilot.cases) {
  const original = byId.get(row.source_id);
  assert.ok(original, 'Unrecognized Source ID');
  assert.equal(original.split, 'train', 'Never run Valid/Test preflight');
  assert.equal(original.filename, row.filename);
  assert.deepEqual([original.width,original.height], row.image_dimensions);
  assert.equal(row.output.raw, row.output.high + row.output.lower);
  assert.equal(row.review_codes.association, 'ASSOCIATION_UNKNOWN');
  assert.equal(row.review_codes.policy, 'POLICY_UNKNOWN');
  assert.ok(row.output.raw >= row.output.persons);
  assert.ok(row.output.raw >= row.output.ppe);
  assert.ok(row.output.raw >= 0 && row.output.geometric >= 0 && row.output.pairwise >= 0);
  assert.equal(row.review_codes.confidence,
      row.output.lower > 0 ? 'LOW_CONFIDENCE_NEEDS_REVIEW' : 'NO_LOW_SCORE_CANDIDATES_RETURNED');
  assert.equal(row.review_codes.person_coverage,
      row.output.persons > 0 ? 'PERSON_CANDIDATES_DETECTED_COVERAGE_UNVERIFIED' : 'PERSON_COVERAGE_UNKNOWN');
}
assert.equal(pilot.cases.find(x => x.case === 'D').output.persons, 0);
assert.equal(pilot.invariants.scores_computed, false);
assert.equal(pilot.invariants.model_retrained, false);
assert.equal(pilot.invariants.eval_case_mutated, false);
assert.equal(pilot.invariants.original_dataset_mutated, false);
assert.equal(pilot.invariants.energy_measured, false);
assert.equal(pilot.scientific_readiness.mAP, null);
assert.equal(pilot.scientific_readiness.F1, null);
assert.equal(pilot.scientific_readiness.scoring_ready, false);

assert.equal(reference.case_count, 4);
assert.equal(reference.case_complete_count, 0);
assert.equal(reference.human_approved_links_preserved, 19);
assert.equal(reference.saved_worker_ppe_states, 38);
assert.equal(reference.expected_worker_ppe_states, 42);
assert.equal(reference.missing_state_cells.length, 4);
assert.deepEqual(reference.missing_state_cells.map(x => x.case + ':' + x.person_id + ':' + x.ppe_type).sort(),
  ['B:P001:face_mask','B:P001:safety_boot','B:P002:face_mask','B:P002:safety_boot'].sort());
assert.deepEqual(reference.cases.map(x => x.revision), [2,2,4,1]);
assert.deepEqual(reference.cases.map(x => x.approved_links), [3,4,12,0]);
assert.deepEqual(reference.cases.map(x => x.saved_visual_rows), [6,8,24,0]);
assert.ok(reference.cases.every(x => x.ground_truth_state === 'incomplete' && x.all_saved_mandates_policy_unknown));
assert.equal(reference.case_D_human_signed_zero_person_decision, false);
assert.equal(reference.model_inference_promoted_to_reference, false);
assert.equal(reference.no_eval_case_writes, true);
assert.equal(reference.scoring_ready, false);
assert.equal(reference.saved_visual_state_distribution_not_a_model_metric.PRESENT,22);
assert.equal(reference.saved_visual_state_distribution_not_a_model_metric.ABSENT,3);
assert.equal(reference.saved_visual_state_distribution_not_a_model_metric.UNKNOWN,13);
assert.equal(reference.saved_visual_state_distribution_not_a_model_metric.NOT_RECORDED,4);

const ppes = ['hard_hat','safety_vest','goggles','face_mask','glove','safety_boot'];
let counted=0, missing=0;
for (const row of reference.cases) {
  const persons = row.people || [];
  assert.equal(persons.length, row.person_count);
  for(const person of persons) {
    assert.deepEqual(Object.keys(person.states).sort(), [...ppes].sort());
    for(const s of Object.values(person.states)) {
      if (s.state === 'NOT_RECORDED') missing++;
      else assert.ok(['PRESENT','ABSENT','UNKNOWN'].includes(s.state));
      counted++;
    }
  }
}
assert.equal(counted,42);
assert.equal(missing,4);
assert.equal(approvedVisualReview.author_visual_review_status,
  'COMPLETED_AND_AUTHOR_ACCEPTED_AS_CORRECT_AND_APPROPRIATE');
assert.equal(approvedVisualReview.scoring_ready,false);

console.log('SEER_V09_TRAIN_ONLY_PREFLIGHT_REFERENCE_FAIL_CLOSED_PASS');
