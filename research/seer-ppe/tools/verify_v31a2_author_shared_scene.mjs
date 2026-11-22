#!/usr/bin/env node
/* V31-A2 verifies the author's WA0026/WA0079 shared-scene statement and retained Valid hold. */
import fs from 'node:fs';
import assert from 'node:assert/strict';
import path from 'node:path';
import {createHash} from 'node:crypto';
import {fileURLToPath} from 'node:url';

const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const read=n=>JSON.parse(fs.readFileSync(path.join(root,n),'utf8'));
const sha=s=>createHash('sha256').update(s,'utf8').digest('hex');
const evidencePath='evidence/AUTHOR_CHAT_ATTESTATION_WA0026_WA0079_SHARED_SCENE_2026-11-22.md';
const expectedSha='d75d626a38c65c3b81c74b7619e5ceae38fb38d30de2d910dea76129d9c706d7';
const validId='yeEvdkqXtNgsj7PZFDvI';
const trainId='xyKCHH49Xr7oCONLC9nN';

function audit(evidence,overlay,priority,ready,record){
  assert.equal(sha(evidence),expectedSha);
  assert.ok(evidence.includes('## Author\'s response (verbatim as typed)\n\n"ليس نفي الصورة وانما نفس المشهد مهع تغيرات عليه ومعالجات"'));
  assert.ok(evidence.includes('IMG-20250416-WA0026.jpg'));
  assert.ok(evidence.includes('IMG-20250416-WA0079.jpg'));
  assert.ok(evidence.includes('SHARED_SCENE_WITH_MODIFICATIONS_OR_PROCESSING'));
  assert.equal(overlay.schema_version,'seer-ppe/source-family-human-attestation-overlay/v0.15');
  assert.equal(overlay.decisions.length,3);
  assert.equal(overlay.scoring_authorized,false);
  assert.equal(overlay.test_source_ids_used,false);
  const d=overlay.decisions.find(x=>x.source_id===validId);
  assert.ok(d);
  assert.equal(d.source_original_filename,'IMG-20250416-WA0026.jpg');
  assert.equal(d.clean17_export_filename,'IMG-20250416-WA0026_jpg.rf.a3294f67d828b9a7fd892bc2820063c9.jpg');
  assert.equal(d.verdict,'SHARED_SCENE_WITH_MODIFICATIONS_OR_PROCESSING');
  assert.equal(d.reviewer_id,'dataset_author_chat_attestation');
  assert.equal(d.signed_date,'2026-11-22');
  assert.equal(d.per_source_reviewer_inspected_evidence,true);
  assert.ok(d.evidence_basis.includes('same scene content with changes and processing'));
  assert.equal(d.evidence_ref,evidencePath);
  assert.equal(d.evidence_sha256,expectedSha);
  assert.equal(d.acquisition_site_id,null);
  assert.equal(d.capture_session_id,null);
  assert.equal(d.acquisition_family_id,'scene_wa0026_wa0079_modified_processed');
  assert.equal(d.train_family_overlap_verdict,'SHARED_SCENE_WITH_TRAIN_MODIFIED_OR_PROCESSED');
  assert.equal(d.train_family_crosscheck_completed,true);
  assert.equal(d.no_train_capture_or_site_family_overlap_supported,false);
  assert.equal(d.personally_attested_independence,false);
  const p=priority.review_packets.find(x=>x.source_id===validId);
  assert.ok(p);
  assert.equal(p.original_valid_filename,'IMG-20250416-WA0026.jpg');
  assert.equal(p.nearest_direct_train_id,trainId);
  assert.equal(p.nearest_direct_train_filename,'IMG-20250416-WA0079.jpg');
  assert.equal(p.research_hard_hold_preexisting,true);
  assert.equal(p.human_source_family_relationship_verdict,'SHARED_SCENE_WITH_MODIFICATIONS_OR_PROCESSING');
  assert.equal(p.human_source_family_id,'scene_wa0026_wa0079_modified_processed');
  assert.equal(p.human_capture_session_id,null);
  assert.equal(p.human_evidence_sha256,expectedSha);
  assert.equal(p.eligible_for_source_independent_scoring,false);
  assert.equal(ready.human_source_family_attestations,3);
  assert.equal(ready.shared_site_attested_valid_sources,2);
  assert.equal(ready.shared_scene_processed_valid_sources,1);
  assert.equal(ready.independently_signed_source_family_verdicts,0);
  assert.equal(ready.independent_source_eligible_valid_images,0);
  assert.equal(ready.true_worker_safety_scoring_ready,false);
  const rp=ready.source_priority_review_packets.source_ids.find(x=>x.valid_source_id===validId);
  assert.ok(rp);
  assert.equal(rp.human_source_family_relationship_verdict,'SHARED_SCENE_WITH_MODIFICATIONS_OR_PROCESSING');
  assert.equal(rp.human_source_family_id,'scene_wa0026_wa0079_modified_processed');
  assert.equal(rp.human_capture_session_id,null);
  assert.equal(rp.currently_eligible_for_independent_scoring,false);
  assert.equal(record.verdict,'SHARED_SCENE_WITH_MODIFICATIONS_OR_PROCESSING');
  assert.equal(record.scene_family_id,'scene_wa0026_wa0079_modified_processed');
  assert.equal(record.valid_member.source_id,validId);
  assert.equal(record.train_member.source_id,trainId);
  assert.equal(record.author_scope.confirms_same_scene_content,true);
  assert.equal(record.author_scope.confirms_changes_or_processing,true);
  assert.equal(record.author_scope.byte_identical_asserted,false);
  assert.equal(record.author_scope.exact_original_frame_identity_asserted,false);
  assert.equal(record.author_scope.capture_session_id,null);
  assert.equal(record.evidence_sha256,expectedSha);
  assert.equal(record.consequences.prior_holds_released,0);
  assert.equal(record.consequences.independent_source_attestations,0);
  assert.equal(record.consequences.independent_source_eligible_valid_images,0);
  assert.equal(record.consequences.test_accessed,false);
  assert.equal(record.consequences.model_inference_calls,0);
  return {status:'PASS_V31_A2_AUTHOR_SHARED_SCENE_AND_HARD_HOLD_PRESERVATION',
    valid_source_id:validId,train_source_id:trainId,
    verdict:'SHARED_SCENE_WITH_MODIFICATIONS_OR_PROCESSING',
    independent_source_attestations:0,hold_releases:0,scoring_eligible:0,
    model_calls:0,test_access:false};
}
const evidence=fs.readFileSync(path.join(root,evidencePath),'utf8');
const overlay=read('SOURCE_FAMILY_SIGNED_ATTESTATIONS_V15.json');
const priority=read('SOURCE_FAMILY_EVIDENCE_PRIORITY_11_2026-11-21_V15.json');
const ready=read('V31_SOURCE_PERSON_SAFETY_READINESS_2026-11-22.json');
const record=read('V31_A2_AUTHOR_SHARED_SCENE_WA0026_WA0079_2026-11-22.json');
try{
  const result=audit(evidence,overlay,priority,ready,record);
  if(process.argv.includes('--self-test')){
    const badOverlay=mutate=>{
      const x=structuredClone(overlay);
      mutate(x.decisions.find(d=>d.source_id===validId));
      assert.throws(()=>audit(evidence,x,priority,ready,record));
    };
    badOverlay(x=>{x.verdict='INDEPENDENT_SOURCE_SUPPORTED';});
    badOverlay(x=>{x.acquisition_family_id='independent_family';});
    badOverlay(x=>{x.capture_session_id='invented_session';});
    badOverlay(x=>{x.no_train_capture_or_site_family_overlap_supported=true;});
    badOverlay(x=>{x.personally_attested_independence=true;});
    badOverlay(x=>{x.evidence_sha256='0'.repeat(64);});
    const badPriority=structuredClone(priority);
    badPriority.review_packets.find(x=>x.source_id===validId).eligible_for_source_independent_scoring=true;
    assert.throws(()=>audit(evidence,overlay,badPriority,ready,record));
    const badReady=structuredClone(ready);badReady.independent_source_eligible_valid_images=1;
    assert.throws(()=>audit(evidence,overlay,priority,badReady,record));
    const badRecord=structuredClone(record);badRecord.consequences.prior_holds_released=1;
    assert.throws(()=>audit(evidence,overlay,priority,ready,badRecord));
    console.log('V31_A2_MUTATION_SELF_TEST_FAIL_CLOSED_PASS');
  }else if(process.argv.includes('--verify'))console.log(JSON.stringify(result,null,2));
  else {console.error('Use --self-test or --verify');process.exitCode=2;}
}catch(e){console.error('V31_A2_AUTHOR_SHARED_SCENE_FAILED_CLOSED',e.message);process.exitCode=1;}
