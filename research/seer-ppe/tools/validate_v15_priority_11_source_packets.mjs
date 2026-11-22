#!/usr/bin/env node
/** SEER-PPE V15: high-priority 11 packet must exactly match immutable V14 risks. */
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
const read=x=>JSON.parse(readFileSync(new URL('../'+x,import.meta.url),'utf8'));
const data=read('SOURCE_FAMILY_EVIDENCE_PRIORITY_11_2026-11-21_V15.json');
const quarantine=read('VALIDATION_TECHNICAL_QUARANTINE_V14.json');
const evidence=read('ORIGINAL_99_VALID_SOURCE_FAMILY_PAIRS_2026-11-21_V14.json');
const school=new Set(['0De0PEUDyeg9v1J3T6zr','NZu6Faj6evgINF1qFE0V']);
const sharedScene='yeEvdkqXtNgsj7PZFDvI';
const schoolEvidenceSha='326c7ad0347a86822768e4f1703045248247bc3014cd5ccb139148332cc07605';
const sceneEvidenceSha='d75d626a38c65c3b81c74b7619e5ceae38fb38d30de2d910dea76129d9c706d7';
function check(x){
 assert.equal(x.schema_version,'seer-ppe/high-priority-11-original-valid-source-family-signoff-packet/v0.15');
 assert.equal(x.total_priority_valid_cases,11);
 assert.equal(x.retained_previous_historical_holds,5);
 assert.equal(x.new_unsigned_high_pixel_overlap_quarantines,6);
 assert.equal(x.old_named_school_site_valid_holds,2);
 assert.equal(x.human_source_family_independence_signoffs_added,0);
 assert.equal(x.research_quarantine_not_original_data_mutation,true);
 assert.equal(x.scoring_ready,false);
 assert.equal(x.test_images_accessed,false);
 assert.equal(x.review_packets.length,11);
 const states=new Set(['RETAIN_PREEXISTING_RESEARCH_HOLD','TECHNICAL_OVERLAP_QUARANTINE_PENDING_REVIEW']);
 const base=new Map(quarantine.rows.filter(y=>states.has(y.eligibility_disposition)).map(y=>[y.original_valid_source_id,y]));
 assert.equal(base.size,11);
 const seen=new Set(),counts={prior:0,technical:0};
 for(const row of x.review_packets){
  assert.ok(!seen.has(row.source_id),'duplicate review packet');
  seen.add(row.source_id);
  const actual=base.get(row.source_id);
  assert.ok(actual,'source priority packet not in V14 immutable study hold');
  assert.equal(row.original_valid_filename,actual.original_valid_filename);
  assert.equal(row.verified_clean17_valid_filename,actual.clean17_valid_filename);
  assert.equal(row.research_status,actual.eligibility_disposition);
  assert.equal(row.research_hard_hold_preexisting,actual.previous_research_hold);
  assert.equal(row.same_frame_technical_high_pair_count,actual.strong_source_train_candidate_pairs);
  assert.equal(row.nearest_direct_train_id,actual.strongest_train_source_id);
  assert.equal(row.nearest_direct_train_filename,actual.strongest_train_filename);
  assert.equal(row.strongest_direct_train_gray_ssim,actual.highest_train_ssim);
  assert.equal(row.original_train_candidates_compared,actual.direct_source_train_candidate_pairs_examined);
  assert.equal(row.eligible_for_source_independent_scoring,false);
  if(school.has(row.source_id)){
    assert.equal(row.human_source_family_relationship_verdict,'SHARED_CAPTURE_SESSION_OR_SITE');
    assert.equal(row.human_acquisition_site_id,'site_school_22may_aseefrah');
    assert.equal(row.human_capture_session_id,null);
    assert.equal(row.human_source_family_id,'site_school_22may_aseefrah');
    assert.equal(row.human_train_source_family_overlap_verdict,'SHARED_SITE_FAMILY_WITH_TRAIN');
    assert.equal(row.human_reviewer_id,'dataset_author_chat_attestation');
    assert.equal(row.human_signed_date,'2026-11-22');
    assert.equal(row.human_evidence_sha256,schoolEvidenceSha);
  }else if(row.source_id===sharedScene){
    assert.equal(row.human_source_family_relationship_verdict,'SHARED_SCENE_WITH_MODIFICATIONS_OR_PROCESSING');
    assert.equal(row.human_acquisition_site_id,null);
    assert.equal(row.human_capture_session_id,null);
    assert.equal(row.human_source_family_id,'scene_wa0026_wa0079_modified_processed');
    assert.equal(row.human_train_source_family_overlap_verdict,'SHARED_SCENE_WITH_TRAIN_MODIFIED_OR_PROCESSED');
    assert.equal(row.human_reviewer_id,'dataset_author_chat_attestation');
    assert.equal(row.human_signed_date,'2026-11-22');
    assert.equal(row.human_evidence_sha256,sceneEvidenceSha);
  }else{
    assert.equal(row.human_source_family_relationship_verdict,null);
    assert.equal(row.human_reviewer_id,null);
    assert.equal(row.human_signed_date,null);
    assert.equal(row.human_evidence_sha256,null);
  }
  if(actual.previous_research_hold)counts.prior++;
  else {counts.technical++;assert.ok(actual.strong_source_train_candidate_pairs>0);}
  assert.equal(row.named_site_evidence=== 'PREVIOUS_NAMED_SCHOOL_22_MAY_ASEEFRAH_SHARED_TRAIN_VALID',
    school.has(row.source_id));
 }
 assert.equal(counts.prior,5);assert.equal(counts.technical,6);
 assert.equal(seen.size,11);
 assert.equal(evidence.original_valid_retained_clean17_under_review,92);
 assert.equal(evidence.retained_clean17_high_overlap_not_previously_held,6);
}
check(data);
if(process.argv[2]==='--self-test'){
 const changed=structuredClone(data);changed.review_packets[0].human_reviewer_id='fake';
 assert.throws(()=>check(changed));
 const changed2=structuredClone(data);changed2.review_packets[0].eligible_for_source_independent_scoring=true;
 assert.throws(()=>check(changed2));
 const changed3=structuredClone(data);changed3.review_packets.pop();
 assert.throws(()=>check(changed3));
 console.log('SEER_V15_SYNTHETIC_PRIORITY_11_FALSE_SIGNOFF_AND_CLEARANCE_REJECTION_PASS');
}else if(!process.argv[2]||process.argv[2]==='--verify'){
 console.log('SEER_V15_11_PRIORITY_SOURCE_CASES_5_HARD_HOLDS_6_TECHNICAL_QUARANTINES_PASS');
}else throw Error('Usage: --verify | --self-test');
