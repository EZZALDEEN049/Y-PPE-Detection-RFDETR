#!/usr/bin/env node
/* V31-A3 verifies aggregate dataset provenance and accepted prior author curation.
   It must not clear cross-split holds or claim independent site generalization. */
import fs from 'node:fs';
import assert from 'node:assert/strict';
import path from 'node:path';
import {createHash} from 'node:crypto';
import {fileURLToPath} from 'node:url';

const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const read=n=>JSON.parse(fs.readFileSync(path.join(root,n),'utf8'));
const sha=s=>createHash('sha256').update(s,'utf8').digest('hex');
const evidencePath='evidence/AUTHOR_DATASET_LEVEL_ACQUISITION_AND_PRIOR_CURATION_2026-11-22.md';
const expectedSha='201e16d8c24a0704fedab42ecccdc0fe5caf8a0abef205951bcf73f1ebdb901c';

function audit(evidence,record,ready,manuscript,protocol,curator){
  assert.equal(sha(evidence),expectedSha);
  assert.ok(evidence.includes('مشاريع كثيرة ومواقع كثيرة'));
  assert.ok(evidence.includes('منظمات المجتمع المدني في اليمن'));
  assert.ok(evidence.includes('مراجعة جميع الصور') || evidence.includes('review/selection'));
  assert.ok(evidence.includes('No repeat full-corpus review'));
  assert.equal(record.schema_version,'seer-ppe/v31-a3-dataset-level-acquisition-curation-attestation/v0.31a3');
  assert.equal(record.evidence_ref,evidencePath);
  assert.equal(record.evidence_sha256,expectedSha);
  assert.equal(record.author_attestation.multi_project_collection,true);
  assert.equal(record.author_attestation.multi_work_location_collection,true);
  assert.equal(record.author_attestation.country,'Yemen');
  assert.equal(record.author_attestation.project_context,'civil-society organization projects');
  assert.equal(record.author_attestation.prior_image_review_completed_during_dataset_preparation,true);
  assert.equal(record.author_attestation.repeat_full_corpus_visual_review_required,false);
  assert.equal(record.author_attestation.per_image_project_or_worksite_identity_required,false);
  assert.equal(record.methodological_decision.internal_image_level_detection_evaluation_requires_per_image_site_id,false);
  assert.equal(record.methodological_decision.source_independent_multi_site_generalization_claim_supported,false);
  assert.equal(record.methodological_decision.source_unknown_must_not_be_relabelled_independent,true);
  assert.equal(record.methodological_decision.known_cross_split_overlap_controls_preserved,true);
  assert.equal(record.methodological_decision.worker_level_person_ppe_gold_created_by_this_record,false);
  assert.equal(record.known_overlap_state.school_22may_valid_sources,2);
  assert.equal(record.known_overlap_state.wa0026_train_shared_scene_with_modifications_or_processing,true);
  assert.equal(record.known_overlap_state.other_unresolved_p0_cases,8);
  assert.equal(record.known_overlap_state.existing_holds_released,0);
  assert.equal(record.known_overlap_state.independent_source_eligible_valid_images_added,0);
  assert.equal(ready.dataset_level_acquisition_curation_attestation.evidence_sha256,expectedSha);
  assert.equal(ready.dataset_level_acquisition_curation_attestation.repeat_full_corpus_review_required,false);
  assert.equal(ready.dataset_level_acquisition_curation_attestation.per_image_worksite_or_project_id_required_for_internal_image_level_detection,false);
  assert.equal(ready.dataset_level_acquisition_curation_attestation.source_independent_multi_site_generalization_supported,false);
  assert.equal(ready.v31a3_methodology_decision.internal_image_level_detection_allowed,true);
  assert.equal(ready.v31a3_methodology_decision.site_independent_generalization_supported,false);
  assert.equal(ready.v31a3_methodology_decision.full_corpus_reinspection_requested,false);
  assert.equal(ready.v31a3_methodology_decision.known_overlap_holds_released,0);
  assert.equal(ready.human_source_family_attestations,3);
  assert.equal(ready.shared_site_attested_valid_sources,2);
  assert.equal(ready.shared_scene_processed_valid_sources,1);
  assert.equal(ready.independently_signed_source_family_verdicts,0);
  assert.equal(ready.independent_source_eligible_valid_images,0);
  assert.equal(ready.true_worker_safety_scoring_ready,false);
  assert.equal(ready.source_priority_review_packets.case_count,11);
  assert.equal(ready.source_priority_review_packets.source_ids.filter(x=>x.currently_eligible_for_independent_scoring).length,0);
  assert.ok(manuscript.includes('aggregate multi-project/multi-location level'));
  assert.ok(manuscript.includes('Per-image site identification is not required'));
  assert.ok(manuscript.includes('M0=459'));
  assert.ok(manuscript.includes('M1=448'));
  assert.ok(manuscript.includes('M2=367'));
  assert.ok(protocol.includes('a named worksite/project ID for every image is **not required**'));
  assert.ok(protocol.includes('do not repeat full-corpus review'));
  assert.ok(curator.includes('Do not ask the owner to repeat image review'));
  assert.ok(curator.includes('multi-project, multi-location collection in Yemen'));
  return {status:'PASS_V31_A3_AGGREGATE_PROVENANCE_AND_PRIOR_CURATION',
    per_image_site_ids_required:false,repeat_full_corpus_review:false,
    confirmed_nonindependent_valid_relationships:3,unresolved_p0:8,
    independent_source_clearances:0,holds_released:0,
    internal_image_level_detection_allowed:true,
    independent_multi_site_generalization:false,worker_safety_scoring_ready:false};
}
const evidence=fs.readFileSync(path.join(root,evidencePath),'utf8');
const record=read('V31_A3_DATASET_LEVEL_ACQUISITION_CURATION_2026-11-22.json');
const ready=read('V31_SOURCE_PERSON_SAFETY_READINESS_2026-11-22.json');
const manuscript=fs.readFileSync(path.join(root,'MANUSCRIPT_MASTER.md'),'utf8');
const protocol=fs.readFileSync(path.join(root,'PROTOCOL_MASTER.md'),'utf8');
const curator=fs.readFileSync(path.join(root,'AUTHOR_CURATOR_REFERENCE_POLICY_2026-11-21_V18.md'),'utf8');
try{
  const result=audit(evidence,record,ready,manuscript,protocol,curator);
  if(process.argv.includes('--self-test')){
    const badRecord=mutate=>{
      const x=structuredClone(record);mutate(x);
      assert.throws(()=>audit(evidence,x,ready,manuscript,protocol,curator));
    };
    badRecord(x=>{x.author_attestation.per_image_project_or_worksite_identity_required=true;});
    badRecord(x=>{x.author_attestation.repeat_full_corpus_visual_review_required=true;});
    badRecord(x=>{x.methodological_decision.source_independent_multi_site_generalization_claim_supported=true;});
    badRecord(x=>{x.methodological_decision.source_unknown_must_not_be_relabelled_independent=false;});
    badRecord(x=>{x.known_overlap_state.existing_holds_released=1;});
    const badReady=structuredClone(ready);badReady.independent_source_eligible_valid_images=1;
    assert.throws(()=>audit(evidence,record,badReady,manuscript,protocol,curator));
    console.log('V31_A3_MUTATION_SELF_TEST_FAIL_CLOSED_PASS');
  }else if(process.argv.includes('--verify'))console.log(JSON.stringify(result,null,2));
  else {console.error('Use --self-test or --verify');process.exitCode=2;}
}catch(e){console.error('V31_A3_DATASET_LEVEL_CURATION_FAILED_CLOSED',e.message);process.exitCode=1;}
