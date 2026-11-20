#!/usr/bin/env node
/** Engineering-only verifier: author approval must never be converted into scoring eligibility. */
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';

const base=new URL('../',import.meta.url);
const read=name=>JSON.parse(readFileSync(new URL(name,base),'utf8'));
const frozen=read('SOURCE_ID_MANIFEST_TRAIN_VALID_2026-11-19_V01.json');
const previous=read('SOURCE_FAMILY_REVIEW_QUEUE_2026-11-21_V06.json');
const approval=read('AUTHOR_VISUAL_REVIEW_ACCEPTANCE_2026-11-21_V08.json');
const manifest=read('VALIDATION_ELIGIBILITY_PLANNING_MANIFEST_2026-11-21_V08.json');

assert.equal(approval.author_visual_review_status,'COMPLETED_AND_AUTHOR_ACCEPTED_AS_CORRECT_AND_APPROPRIATE');
assert.equal(approval.need_to_reinspect_images_for_general_visual_review,false);
assert.equal(approval.individual_train_valid_source_family_verdicts_not_specified,true);
assert.equal(approval.no_test_image_access,true);
assert.equal(approval.scoring_ready,false);

assert.equal(frozen.images.length,2093);
assert.equal(frozen.images.filter(x=>x.split==='train').length,1625);
const valid=frozen.images.filter(x=>x.split==='valid');
assert.equal(valid.length,468);
const byId=new Map(valid.map(x=>[x.image_id,x]));
assert.equal(byId.size,468);
assert.equal(manifest.valid_rows.length,468);
assert.equal(new Set(manifest.valid_rows.map(x=>x.source_id)).size,468);

const reviewById=new Map(previous.review_queue.map(x=>[x.valid_source_id,x]));
assert.equal(reviewById.size,99);
let held=0, flagged=0, unflagged=0;
for(const row of manifest.valid_rows){
  const a=byId.get(row.source_id);
  assert.ok(a,'source not in frozen Valid');
  assert.equal(row.split,'valid');
  assert.equal(row.filename,a.filename);
  assert.equal(row.width,a.width);
  assert.equal(row.height,a.height);
  assert.equal(row.byte_pixel_integrity_checked,true);
  assert.equal(row.explicit_independent_source_signoff,false);
  assert.equal(row.source_family_scoring_eligible,false);
  assert.equal(row.may_use_for_independent_scientific_scoring,false);
  assert.equal(row.may_use_for_unscored_development_preflight,true);
  const q=reviewById.get(row.source_id);
  if(q?.prior_hold){
    held++;
    assert.equal(row.eligibility_bucket,'PREEXISTING_RESEARCH_HOLD');
    assert.equal(row.prior_hold,true);
  }else if(q){
    flagged++;
    assert.equal(row.eligibility_bucket,'SOURCE_FAMILY_REVIEW_CANDIDATE_NOT_SIGNED');
    assert.equal(row.prior_hold,false);
  }else{
    unflagged++;
    assert.equal(row.eligibility_bucket,'NO_SCREEN_FLAG_SOURCE_INDEPENDENCE_UNCERTIFIED');
    assert.equal(row.prior_hold,false);
  }
}
assert.deepEqual([held,flagged,unflagged],[5,94,369]);
assert.equal(manifest.unflagged_valid_are_independent,false);
assert.equal(manifest.new_automatic_holds,0);
assert.equal(manifest.test_sources_accessed,0);
assert.equal(manifest.original_data_split_changes,0);
assert.equal(manifest.valid_for_scientific_heldout_scoring,false);
assert.equal(manifest.scoring_ready,false);

console.log('SEER_V08_AUTHOR_ACCEPTED_REVIEW_WITHOUT_UNSUPPORTED_SCORING_PASS');
