#!/usr/bin/env node
/** V14 conservative source-family quarantine / freeze readiness, read-only. */
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
const read=n=>JSON.parse(readFileSync(new URL('../'+n,import.meta.url),'utf8'));
const quarantine=read('VALIDATION_TECHNICAL_QUARANTINE_V14.json');
const packet=read('VALIDATION_P0_HIGH_OVERLAP_HUMAN_REVIEW_V14.json');
const lineage=read('SOURCE_ELIGIBILITY_DECISION_LEDGER_2026-11-21_V11.json');
const source=read('ORIGINAL_99_VALID_SOURCE_FAMILY_PAIRS_2026-11-21_V14.json');
const exportMedia=read('ORIGINAL_CLEAN17_VALID_IMAGE_CONTENT_V13.json');
const cleanCrosswalk=read('SEER_PPE_VALID_TO_CLEAN17_PROVISIONAL_V12.json');
const person=read('PERSON_PPE_PENDING_HUMAN_SIGNOFF_2026-11-21_V13.json');
const freeze=read('VALIDATION_PERSON_PPE_SCORING_FREEZE_2026-11-21_V11.json');
const allowed=['RETAIN_PREEXISTING_RESEARCH_HOLD',
'TECHNICAL_OVERLAP_QUARANTINE_PENDING_REVIEW',
'SOURCE_FAMILY_REVIEW_PENDING',
'NO_SCREEN_FLAG_INDEPENDENCE_UNCERTIFIED'];
function verify(d,p){
 assert.equal(d.schema_version,'seer-ppe/clean17-valid-research-quarantine/v0.14');
 assert.equal(d.clean17_valid_files,459);
 assert.equal(d.technical_direct_clean17_matches,459);
 assert.equal(d.previous_signed_research_holds,5);
 assert.equal(d.additional_technical_quarantine_unsigned,6);
 assert.equal(d.other_flagged_source_family_unsigned,81);
 assert.equal(d.unflagged_independence_uncertified,367);
 assert.equal(d.signed_independent_source_family_decisions,0);
 assert.equal(d.scientific_scoring_eligible,0);
 assert.equal(d.no_new_formal_holds_created,true);
 assert.equal(d.scoring_ready,false);
 assert.equal(d.test_opened,false);
 assert.equal(d.rows.length,459);
 assert.equal(source.original_review_valid_sources,99);
 assert.equal(source.train_valid_direct_pairs_total,280);
 assert.equal(source.original_valid_retained_clean17_under_review,92);
 assert.equal(source.original_valid_historically_excluded_under_review,7);
 assert.equal(source.high_same_frame_candidate_pairs,12);
 assert.equal(source.distinct_valid_sources_with_high_same_frame_candidate,9);
 assert.equal(source.retained_clean17_valid_sources_with_high_same_frame_candidate,8);
 assert.equal(source.retained_clean17_high_overlap_not_previously_held,6);
 assert.equal(source.high_overlap_already_historically_excluded,1);
 assert.equal(source.original_source_hold_count_unchanged,5);
 assert.equal(source.signed_independence_decisions_added,0);
 assert.equal(source.test_images_decoded,0);
 assert.equal(source.scientific_scoring_ready,false);
 assert.equal(exportMedia.source_and_export_sha_verified,459);
 assert.equal(exportMedia.high_content_consistency,459);
 assert.equal(exportMedia.test_images_decoded,0);
 assert.equal(freeze.authorized,false);
 assert.equal(freeze.state,'NOT_FROZEN');
 assert.equal(freeze.test_authorized,false);
 assert.equal(person.prior_reference_human_links_preserved,19);
 assert.equal(person.prior_recorded_visual_states,38);
 assert.equal(person.case_B_visual_state_pending.length,4);
 assert.equal(person.case_D.zero_person_scene_human_signed,null);
 assert.equal(p.items.length,6);
 assert.equal(p.all_six_reviews_unsigned,true);
 assert.equal(p.additional_formal_holds_created,0);
 const prev=new Map(lineage.rows.map(x=>[x.source_id,x]));
 const review=new Map(source.source_rows.map(x=>[x.valid_id,x]));
 const clean=new Map(cleanCrosswalk.valid_rows.filter(x=>x.clean17_export_candidate).map(x=>[x.original_source_id,x]));
 const media=new Map(exportMedia.results.map(x=>[x.source_id,x]));
 const ids=new Set(),names=new Set(),summary=Object.fromEntries(allowed.map(s=>[s,0]));
 for(const row of d.rows){
  assert.ok(!ids.has(row.original_valid_source_id),'duplicate original Source ID');
  assert.ok(!names.has(row.clean17_valid_filename),'duplicate clean export filename');
  ids.add(row.original_valid_source_id);names.add(row.clean17_valid_filename);
  const b=prev.get(row.original_valid_source_id);
  const c=clean.get(row.original_valid_source_id);
  const v=review.get(row.original_valid_source_id);
  const m=media.get(row.original_valid_source_id);
  assert.ok(b && c && m,'unrecognized original Valid Source');
  assert.equal(row.original_valid_filename,b.filename);
  assert.equal(row.original_valid_filename,c.original_filename);
  assert.equal(row.clean17_valid_filename,c.clean17_export_candidate);
  assert.equal(m.export_filename,row.clean17_valid_filename);
  assert.equal(m.original_sha_verified,true);
  assert.equal(m.export_sha_verified,true);
  assert.equal(row.original_to_clean17_direct_media_sha_verified,true);
  assert.equal(row.high_source_export_content_consistency,true);
  assert.equal(row.previous_research_hold,b.preexisting_research_hold);
  assert.equal(row.previous_review_queue_flag,!!v);
  assert.equal(row.strong_source_train_candidate_pairs,v?.technical_high_same_frame_pairs??0);
  assert.equal(row.human_source_family_verdict_signed,false);
  assert.equal(row.source_group_independence_scoring_authorized,false);
  assert.equal(row.frozen_validation_scoring_eligible,false);
  assert.equal(row.human_source_signoff_required,true);
  assert.equal(row.no_original_data_mutation,true);
  const expected=b.preexisting_research_hold?'RETAIN_PREEXISTING_RESEARCH_HOLD':
    (v?.technical_high_same_frame_pairs??0)>0?'TECHNICAL_OVERLAP_QUARANTINE_PENDING_REVIEW':
    v?'SOURCE_FAMILY_REVIEW_PENDING':'NO_SCREEN_FLAG_INDEPENDENCE_UNCERTIFIED';
  assert.equal(row.eligibility_disposition,expected,'source/quarantine misclassified');
  summary[expected]++;
 }
 assert.equal(ids.size,459);
 assert.deepEqual(summary,{
 RETAIN_PREEXISTING_RESEARCH_HOLD:5,
 TECHNICAL_OVERLAP_QUARANTINE_PENDING_REVIEW:6,
 SOURCE_FAMILY_REVIEW_PENDING:81,
 NO_SCREEN_FLAG_INDEPENDENCE_UNCERTIFIED:367
 });
 const techIds=new Set(d.rows.filter(x=>x.eligibility_disposition==='TECHNICAL_OVERLAP_QUARANTINE_PENDING_REVIEW').map(x=>x.original_valid_source_id));
 assert.equal(techIds.size,6);
 for(const item of p.items){
  assert.ok(techIds.has(item.source_id),'priority case is outside quarantine');
  assert.equal(item.curator_signature,null);
  assert.equal(item.curator_source_family_verdict,null);
  assert.equal(item.research_scoring_allowed,false);
 }
 return summary;
}
const summary=verify(quarantine,packet);
if(process.argv[2]==='--self-test'){
 const t=structuredClone(quarantine);t.rows[0].frozen_validation_scoring_eligible=true;
 assert.throws(()=>verify(t,packet));
 const t2=structuredClone(quarantine);t2.rows.find(x=>x.eligibility_disposition==='TECHNICAL_OVERLAP_QUARANTINE_PENDING_REVIEW').eligibility_disposition='SOURCE_FAMILY_REVIEW_PENDING';
 assert.throws(()=>verify(t2,packet));
 const p2=structuredClone(packet);p2.items[0].curator_source_family_verdict='INDEPENDENT_SOURCE_SUPPORTED';
 assert.throws(()=>verify(quarantine,p2));
 console.log('SEER_V14_SYNTHETIC_SOURCE_QUARANTINE_FALSE_CLEARANCE_REJECTED_PASS');
}else if(!process.argv[2]||process.argv[2]==='--verify'){
 console.log(JSON.stringify({clean17_valid:459,status_counts:summary,source_family_independence_signed:0,person_B_unrecorded:4,D_zero_person_human_signed:false,validation_freeze_authorized:false,scoring_ready:false},null,2));
 console.log('SEER_V14_459_VALID_5_OLD_HOLDS_6_TECHNICAL_QUARANTINES_FAIL_CLOSED_PASS');
}else throw Error('Usage: --verify | --self-test');
