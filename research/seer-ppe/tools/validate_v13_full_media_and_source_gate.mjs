#!/usr/bin/env node
/** SEER-PPE V13 gate: direct technical image correspondence is not source-family independence. */
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
const read=n=>JSON.parse(readFileSync(new URL('../'+n,import.meta.url),'utf8'));
const valid=read('SEER_PPE_VALID_TO_CLEAN17_PROVISIONAL_V12.json');
const technical=read('ORIGINAL_CLEAN17_VALID_IMAGE_CONTENT_V13.json');
const cross=read('DIRECT_ORIGINAL_TRAIN_VALID_SOURCE_EVIDENCE_V13.json');
const priority=read('DIRECT_SOURCE_OVERLAP_PRIORITY_2026-11-21_V13.json');
const pending=read('PERSON_PPE_PENDING_HUMAN_SIGNOFF_2026-11-21_V13.json');
const freeze=read('VALIDATION_PERSON_PPE_SCORING_FREEZE_2026-11-21_V11.json');
function verify(t,x,p){
 assert.equal(t.mode,'full');
 assert.equal(t.requested,459);
 assert.equal(t.source_and_export_sha_verified,459);
 assert.equal(t.high_content_consistency,459);
 assert.equal(t.needs_further_review,0);
 assert.equal(t.errors,0);
 assert.equal(t.previous_held_valid_sample_count,5);
 assert.equal(t.test_images_decoded,0);
 assert.equal(t.test_image_inference,0);
 assert.equal(t.images_uploaded,false);
 assert.equal(t.scientific_scoring_ready,false);
 assert.equal(t.results.length,459);
 const all=new Map(valid.valid_rows.filter(y=>y.clean17_export_candidate).map(y=>[y.original_source_id,y]));
 assert.equal(all.size,459);
 const seen=new Set(),filenames=new Set();
 for(const row of t.results){
   assert.ok(!seen.has(row.source_id));
   seen.add(row.source_id);
   const v=all.get(row.source_id);
   assert.ok(v,'Unexpected Source ID in direct correspondence');
   assert.equal(row.export_filename,v.clean17_export_candidate);
   assert.ok(!filenames.has(row.export_filename));
   filenames.add(row.export_filename);
   assert.equal(row.original_sha_verified,true);
   assert.equal(row.export_sha_verified,true);
   assert.equal(row.technical_content_consistency,'HIGH_AUTOMATED_EVIDENCE_NOT_FINAL_PHOTO_IDENTITY');
   assert.equal(row.source_family_independence_human_signed,false);
   assert.equal(row.scoring_eligible,false);
   assert.ok(row.gray_ssim>=0.88);
   assert.ok(row.rgb_mean_absolute_error<=0.11);
 }
 assert.equal(filenames.size,459);
 assert.equal(x.cross_split_pairs_compared,50);
 assert.equal(x.originals_sha_verified,76);
 assert.equal(x.original_fetch_or_hash_errors,0);
 assert.equal(x.previous_dhash_close_edges,46);
 assert.equal(x.additional_previously_named_site_edges,4);
 assert.equal(x.automated_same_frame_candidates,7);
 assert.equal(x.nonhigh_pixel_pairs_remain_independence_unresolved,43);
 assert.equal(x.raw_byte_identical_cross_split_pairs,0);
 assert.equal(x.human_source_family_verdicts_added,0);
 assert.equal(x.test_image_bytes_opened,0);
 assert.equal(x.scoring_ready,false);
 assert.equal(x.pairs.length,50);
 assert.equal(p.highest_priority.length,7);
 assert.equal(p.new_technical_p0_candidates_retained_in_clean17_not_previously_held,4);
 assert.equal(p.already_held_high_candidates,2);
 assert.equal(p.previously_clean17_excluded_high_candidate,1);
 assert.equal(p.new_formal_source_holds_added,0);
 assert.equal(p.scoring_ready,false);
 const sourcePair=new Map(x.pairs.map(y=>[y.valid_id+'|'+y.train_id,y]));
 for(const q of p.highest_priority){
   const z=sourcePair.get(q.original_valid_source_id+'|'+q.original_train_source_id);
   assert.ok(z?.automated_same_frame_candidate);
   assert.equal(z.gray_ssim,q.gray_ssim);
   assert.equal(q.human_signoff,null);
   assert.equal(q.scientific_scoring_allowed,false);
 }
 assert.equal(pending.case_B_visual_state_pending.length,4);
 assert.ok(pending.case_B_visual_state_pending.every(y=>y.human_final_visual_state===null));
 assert.equal(pending.case_D.zero_person_scene_human_signed,null);
 assert.equal(freeze.authorized,false);
 assert.equal(freeze.test_authorized,false);
 return true;
}
verify(technical,cross,priority);
if(process.argv[2]==='--self-test'){
 const bad=structuredClone(technical);
 bad.results[0].scoring_eligible=true;
 assert.throws(()=>verify(bad,cross,priority),'False eligibility passed');
 const unsafe=structuredClone(priority);unsafe.new_formal_source_holds_added=5;
 assert.throws(()=>verify(technical,cross,unsafe),'Implicit new source holds passed');
 console.log('SEER_V13_SYNTHETIC_PHOTO_EVIDENCE_AND_SOURCE_HOLD_FAIL_CLOSED_PASS');
}else if(!process.argv[2]||process.argv[2]==='--verify'){
 console.log('SEER_V13_459_DIRECT_CLEAN17_AND_50_CROSS_SPLIT_NO_SCORE_PASS');
}else throw Error('Usage: --verify | --self-test');
