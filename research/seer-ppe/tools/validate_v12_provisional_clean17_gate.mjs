#!/usr/bin/env node
/** V12 metadata-only original Valid→Clean17 candidate conservation gate.
 * Candidate similarity is not photo identity, nor certified scoring eligibility. */
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
const read=x=>JSON.parse(readFileSync(new URL('../'+x,import.meta.url),'utf8'));
const p=read('SEER_PPE_VALID_TO_CLEAN17_PROVISIONAL_V12.json');
const ledger=read('SOURCE_ELIGIBILITY_DECISION_LEDGER_2026-11-21_V11.json');
const freeze=read('VALIDATION_PERSON_PPE_SCORING_FREEZE_2026-11-21_V11.json');
function verify(x){
 assert.equal(x.schema_version,'seer-ppe/provisional-valid-to-clean17-candidate-join/v0.12.1');
 assert.equal(x.original_valid_sources,468);
 assert.equal(x.clean17_valid_export_files,459);
 assert.equal(x.unique_name_candidates,426);
 assert.equal(x.ranked_dhash_candidates,33);
 assert.equal(x.prior_historical_exclusions_without_clean_match,9);
 assert.equal(x.clean_valid_export_files_covered_by_distinct_candidates,459);
 assert.equal(x.duplicate_clean_export_assignments,0);
 assert.equal(x.existing_source_holds_preserved,5);
 assert.equal(x.source_to_clean17_pixel_identity_verified_count,0);
 assert.equal(x.independent_source_human_signoffs,0);
 assert.equal(x.scientifically_eligible_images_created,0);
 assert.equal(x.protected_test_images_read,0);
 assert.equal(x.scientific_scoring_ready,false);
 assert.equal(x.valid_rows.length,468);
 const old=new Map(ledger.rows.map(r=>[r.source_id,r]));
 const source=new Set(),clean=new Set();
 const count={};
 let held=0,ranked=0,unmatched=0;
 for(const r of x.valid_rows){
  assert.equal(r.split,'valid');
  assert.ok(!source.has(r.original_source_id),'Repeated original Source ID');
  source.add(r.original_source_id);
  const oldrow=old.get(r.original_source_id);
  assert.ok(oldrow,'V12 Source not in frozen original-valid ledger');
  assert.equal(r.original_filename,oldrow.filename,'Original Source filename changed');
  assert.equal(r.preexisting_research_hold,oldrow.preexisting_research_hold,'Existing hold changed');
  assert.equal(r.confirmed_clean17_membership,false,'Metadata may not certify image identity');
  assert.equal(r.source_to_clean17_pixel_identity_verified,false);
  assert.equal(r.source_family_independence_signed,false);
  assert.equal(r.eligible_for_scientific_scoring,false);
  if(r.preexisting_research_hold)held++;
  count[r.classification]=(count[r.classification]||0)+1;
  if(r.classification==='HISTORICAL_EXCLUSION_NO_CLEAN_NAME_MATCH'){
    unmatched++;
    assert.equal(r.clean17_export_candidate,null);
    assert.equal(r.candidate_count,0);
  }else{
    assert.ok(typeof r.clean17_export_candidate==='string'&&r.clean17_export_candidate.length>0);
    assert.ok(!clean.has(r.clean17_export_candidate),'Two Source IDs pointed at one Clean export');
    clean.add(r.clean17_export_candidate);
    assert.ok(r.candidate_count>=1);
    if(r.classification==='RANKED_DHASH_CANDIDATE'){
      ranked++;
      assert.ok(r.candidate_count>=2);
      assert.ok(r.dhash_rank_margin>=15);
      assert.ok(r.dhash_best<=6);
    }else{
      assert.equal(r.classification,'UNIQUE_NORMALIZED_NAME_CANDIDATE');
      assert.equal(r.candidate_count,1);
    }
  }
 }
 assert.equal(source.size,468);
 assert.equal(clean.size,459);
 assert.equal(held,5);
 assert.equal(ranked,33);
 assert.equal(unmatched,9);
 assert.deepEqual(count,{
  HISTORICAL_EXCLUSION_NO_CLEAN_NAME_MATCH:9,
  UNIQUE_NORMALIZED_NAME_CANDIDATE:426,
  RANKED_DHASH_CANDIDATE:33
 });
 assert.equal(freeze.authorized,false);
 assert.equal(freeze.state,'NOT_FROZEN');
 assert.equal(freeze.test_authorized,false);
 return true;
}
verify(p);
if(process.argv[2]==='--self-test'){
 const x=structuredClone(p);
 x.valid_rows[0].eligible_for_scientific_scoring=true;
 assert.throws(()=>verify(x),'Falsely score-authorized V12 candidate passed');
 const y=structuredClone(p);
 const valid=y.valid_rows.filter(a=>a.clean17_export_candidate);
 valid[1].clean17_export_candidate=valid[0].clean17_export_candidate;
 assert.throws(()=>verify(y),'Duplicate Clean candidate passed');
 console.log('SEER_V12_SYNTHETIC_CANDIDATE_MUTATION_GATES_PASS');
}else if(!process.argv[2]||process.argv[2]==='--verify'){
 console.log('SEER_V12_468_SOURCE_459_UNIQUE_CANDIDATE_NO_SCORING_PASS');
}else{throw Error('Usage: --self-test | --verify');}
