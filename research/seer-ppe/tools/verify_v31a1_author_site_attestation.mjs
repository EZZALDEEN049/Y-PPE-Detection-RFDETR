#!/usr/bin/env node
/* V31-A1 verifies one specific author chat attestation and proves it cannot clear a site-overlap hold. */
import fs from 'node:fs';
import assert from 'node:assert/strict';
import path from 'node:path';
import {createHash} from 'node:crypto';
import {fileURLToPath} from 'node:url';

const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const read=n=>JSON.parse(fs.readFileSync(path.join(root,n),'utf8'));
const sha=s=>createHash('sha256').update(s,'utf8').digest('hex');
const evidencePath='evidence/AUTHOR_CHAT_ATTESTATION_SCHOOL_22_MAY_ASEEFRAH_2026-11-22.md';
const expectedSha='326c7ad0347a86822768e4f1703045248247bc3014cd5ccb139148332cc07605';
const validIds=['0De0PEUDyeg9v1J3T6zr','NZu6Faj6evgINF1qFE0V'];
const trainIds=['KrfW3xD7Vvxy6r6wISkv','H1KOFc0NQZnWRHJNcHPc'];

function audit(evidence,overlay,priority,ready,record){
  assert.equal(sha(evidence),expectedSha);
  assert.ok(evidence.includes('## Author\'s response\n\n"نعم"'));
  assert.ok(evidence.includes('IMG-20250416-WA0063.jpg'));
  assert.ok(evidence.includes('IMG-20250416-WA0051.jpg'));
  assert.ok(evidence.includes('IMG-20250416-WA0067.jpg'));
  assert.ok(evidence.includes('IMG-20250416-WA0066(1).jpg'));
  assert.equal(overlay.schema_version,'seer-ppe/source-family-human-attestation-overlay/v0.15');
  assert.equal(overlay.decisions.length,2);
  assert.deepEqual(overlay.decisions.map(x=>x.source_id).sort(),validIds.slice().sort());
  assert.equal(overlay.scoring_authorized,false);
  assert.equal(overlay.test_source_ids_used,false);
  for(const d of overlay.decisions){
    const p=priority.review_packets.find(x=>x.source_id===d.source_id);
    assert.ok(p);
    assert.equal(d.source_original_filename,p.original_valid_filename);
    assert.equal(d.clean17_export_filename,p.verified_clean17_valid_filename);
    assert.equal(d.verdict,'SHARED_CAPTURE_SESSION_OR_SITE');
    assert.equal(d.reviewer_id,'dataset_author_chat_attestation');
    assert.equal(d.signed_date,'2026-11-22');
    assert.equal(d.per_source_reviewer_inspected_evidence,true);
    assert.ok(d.evidence_basis.length>=3);
    assert.equal(d.evidence_ref,evidencePath);
    assert.equal(d.evidence_sha256,expectedSha);
    assert.equal(d.acquisition_site_id,'site_school_22may_aseefrah');
    assert.equal(d.acquisition_family_id,'site_school_22may_aseefrah');
    assert.equal(d.capture_session_id,null);
    assert.equal(d.train_family_overlap_verdict,'SHARED_SITE_FAMILY_WITH_TRAIN');
    assert.equal(d.train_family_crosscheck_completed,true);
    assert.equal(d.no_train_capture_or_site_family_overlap_supported,false);
    assert.equal(d.personally_attested_independence,false);
    assert.equal(p.research_hard_hold_preexisting,true);
    assert.equal(p.eligible_for_source_independent_scoring,false);
  }
  assert.deepEqual(trainIds.slice().sort(),record.train_members.map(x=>x.source_id).sort());
  assert.deepEqual(validIds.slice().sort(),record.valid_members.map(x=>x.source_id).sort());
  assert.equal(record.verdict,'SHARED_CAPTURE_SESSION_OR_SITE');
  assert.equal(record.site_family_id,'site_school_22may_aseefrah');
  assert.equal(record.author_scope.confirms_same_project_site,true);
  assert.equal(record.author_scope.permits_different_angles_or_times,true);
  assert.equal(record.author_scope.same_original_frame_asserted,false);
  assert.equal(record.author_scope.same_capture_session_asserted,false);
  assert.equal(record.author_scope.capture_session_id,null);
  assert.equal(record.evidence_sha256,expectedSha);
  assert.equal(record.consequences.prior_holds_released,0);
  assert.equal(record.consequences.independent_source_attestations,0);
  assert.equal(record.consequences.independent_source_eligible_valid_images,0);
  assert.equal(record.consequences.test_accessed,false);
  assert.equal(record.consequences.model_inference_calls,0);
  assert.equal(ready.human_source_family_attestations,2);
  assert.equal(ready.shared_site_attested_valid_sources,2);
  assert.equal(ready.independently_signed_source_family_verdicts,0);
  assert.equal(ready.independent_source_eligible_valid_images,0);
  assert.equal(ready.true_worker_safety_scoring_ready,false);
  assert.equal(ready.source_priority_review_packets.source_ids.filter(x=>x.human_source_family_relationship_verdict==='SHARED_CAPTURE_SESSION_OR_SITE').length,2);
  for(const id of validIds){
    const x=ready.source_priority_review_packets.source_ids.find(x=>x.valid_source_id===id);
    assert.equal(x.human_acquisition_site_id,'site_school_22may_aseefrah');
    assert.equal(x.human_capture_session_id,null);
    assert.equal(x.human_source_family_attestation,'AUTHOR_ATTESTED_SHARED_SITE_WITH_TRAIN');
    assert.equal(x.currently_eligible_for_independent_scoring,false);
  }
  return {status:'PASS_V31_A1_AUTHOR_SITE_ATTESTATION_AND_HARD_HOLD_PRESERVATION',
    valid_author_attestations:2,train_site_family_members:2,
    verdict:'SHARED_CAPTURE_SESSION_OR_SITE',site_family_id:'site_school_22may_aseefrah',
    independent_source_attestations:0,hold_releases:0,scoring_eligible:0,
    model_calls:0,test_access:false};
}
const evidence=fs.readFileSync(path.join(root,evidencePath),'utf8');
const overlay=read('SOURCE_FAMILY_SIGNED_ATTESTATIONS_V15.json');
const priority=read('SOURCE_FAMILY_EVIDENCE_PRIORITY_11_2026-11-21_V15.json');
const ready=read('V31_SOURCE_PERSON_SAFETY_READINESS_2026-11-22.json');
const record=read('V31_A1_AUTHOR_SITE_ATTESTATION_2026-11-22.json');
try{
  const result=audit(evidence,overlay,priority,ready,record);
  if(process.argv.includes('--self-test')){
    const mutations=[
      x=>{x.decisions.pop();},
      x=>{x.decisions[0].verdict='INDEPENDENT_SOURCE_SUPPORTED';},
      x=>{x.decisions[0].acquisition_site_id='different_site';},
      x=>{x.decisions[0].capture_session_id='invented_session';},
      x=>{x.decisions[0].no_train_capture_or_site_family_overlap_supported=true;},
      x=>{x.decisions[0].evidence_sha256='0'.repeat(64);},
      x=>{x.scoring_authorized=true;},
    ];
    for(const mutate of mutations){const bad=structuredClone(overlay);mutate(bad);assert.throws(()=>audit(evidence,bad,priority,ready,record));}
    const badRecord=structuredClone(record);badRecord.consequences.prior_holds_released=1;
    assert.throws(()=>audit(evidence,overlay,priority,ready,badRecord));
    console.log('V31_A1_MUTATION_SELF_TEST_FAIL_CLOSED_PASS');
  }else if(process.argv.includes('--verify'))console.log(JSON.stringify(result,null,2));
  else {console.error('Use --self-test or --verify');process.exitCode=2;}
}catch(e){console.error('V31_A1_AUTHOR_ATTESTATION_FAILED_CLOSED',e.message);process.exitCode=1;}
