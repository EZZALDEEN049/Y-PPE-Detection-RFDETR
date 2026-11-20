#!/usr/bin/env node
/**
 * Fail-closed structural gate for V06 original-source review records.
 * Confirms audits/queues were *documented*, not that human media families
 * or scientific model scoring eligibility were established.
 */
import fs from 'node:fs';
import assert from 'node:assert/strict';

const dir = new URL('../', import.meta.url);
const load = name => JSON.parse(fs.readFileSync(new URL(name, dir), 'utf8'));
const manifest = load('SOURCE_ID_MANIFEST_TRAIN_VALID_2026-11-19_V01.json');
const old = load('SOURCE_FAMILY_REVIEW_QUEUE_2026-11-21_V05.json');
const merged = load('SOURCE_FAMILY_REVIEW_QUEUE_2026-11-21_V06.json');
const checkpoint = load('DUAL_TRACK_CHECKPOINT_2026-11-21_V06.json');

assert.equal(manifest.images.length, 2093);
const byId = new Map(manifest.images.map(x => [x.image_id, x]));
assert.equal(byId.size, 2093);
assert.equal(manifest.images.filter(x => x.split === 'train').length, 1625);
assert.equal(manifest.images.filter(x => x.split === 'valid').length, 468);
assert.equal(manifest.images.filter(x => x.split === 'test').length, 0);

assert.equal(merged.originals_hashed, 2093);
assert.equal(merged.train, 1625);
assert.equal(merged.valid, 468);
assert.equal(merged.all_vs_all_cross_split_comparisons, 760500);
assert.equal(merged.raw_or_rgb_matches, 0);
assert.equal(merged.near_pairs_0_to_8, 46);
assert.equal(merged.near_unique_valid_ids, 31);
assert.equal(merged.previous_queue, 83);
assert.equal(merged.previous_queue_near_overlap, 15);
assert.equal(merged.new_queue_valid_ids, 16);
assert.equal(merged.queue_valid_total, 99);
assert.equal(merged.preexisting_specific_holds, 5);
assert.equal(merged.new_automatic_holds, 0);
assert.equal(merged.scientific_scoring_ready, false);
assert.equal(merged.test_accessed, false);

const pairs = merged.original_near_hash_pairs;
assert.equal(pairs.length, 46);
assert.equal(new Set(pairs.map(x => x.valid_id)).size, 31);
for (const p of pairs) {
  assert.equal(byId.get(p.valid_id)?.split, 'valid');
  assert.equal(byId.get(p.train_id)?.split, 'train');
  assert.ok(Number.isInteger(p.dhash_hamming) && p.dhash_hamming >= 0 && p.dhash_hamming <= 8);
  assert.equal(p.raw_sha256_equal, false);
  assert.equal(p.rgb_sha256_equal, false);
}

const v5 = old.review_queue;
const v6 = merged.review_queue;
assert.equal(v5.length, 83);
assert.equal(v6.length, 99);
assert.equal(new Set(v6.map(x => x.valid_source_id)).size, 99);
const oldIds = new Set(v5.map(x => x.valid_source_id));
assert.ok(v5.every(x => v6.some(y => y.valid_source_id === x.valid_source_id)));
assert.equal(v6.filter(x => !oldIds.has(x.valid_source_id)).length, 16);
assert.equal(v6.filter(x => x.prior_hold).length, 5);
assert.equal(v6.filter(x => x.original_dhash_candidate_pairs.length > 0).length, 31);
assert.ok(v6.every(x =>
  x.human_signoff === 'PENDING' &&
  x.source_family_eligible_for_scoring === false &&
  x.source_family_eligibility_finalized === false &&
  (x.valid_eligibility === (x.prior_hold ? 'PREEXISTING_RESEARCH_HOLD' : 'UNDETERMINED_REVIEW_REQUIRED'))
));

assert.equal(checkpoint.source_audit.manifest_originals_total, 2093);
assert.equal(checkpoint.source_audit.exact_byte_pairs, 0);
assert.equal(checkpoint.source_audit.exact_decoded_rgb_pairs, 0);
assert.equal(checkpoint.source_audit.dhash_le8_pairs, 46);
assert.equal(checkpoint.source_family.merged_valid_review_queue, 99);
assert.equal(checkpoint.source_family.new_human_signoffs, 0);
assert.equal(checkpoint.person_ppe.associations_researcher_approved, 19);
assert.equal(checkpoint.person_ppe.visual_review_cells_recorded, 38);
assert.equal(checkpoint.person_ppe.visual_review_cells_expected, 42);
assert.equal(checkpoint.person_ppe.cases_complete, 0);
assert.equal(checkpoint.invariants.test_image_accessed, false);
assert.equal(checkpoint.invariants.scoring_ready, false);

console.log('SEER_V06_ORIGINAL_SOURCE_REVIEW_FAIL_CLOSED_GATE_PASS');
