#!/usr/bin/env node
/** V12.2 full ID-level cross-tab: candidate Clean17 mapping != source-lineage eligibility. */
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
const read=n=>JSON.parse(readFileSync(new URL('../'+n,import.meta.url),'utf8'));
const V=read('SEER_PPE_VALID_TO_CLEAN17_PROVISIONAL_V12.json');
const E=read('SOURCE_ELIGIBILITY_DECISION_LEDGER_2026-11-21_V11.json');
const H=read('PERSON_PPE_REFERENCE_LIVE_SNAPSHOT_2026-11-21_V09.json');
const valid=new Map(E.rows.map(x=>[x.source_id,x]));
assert.equal(valid.size,468);
function cross(tab){
 const result={provisional:{held:0,source_flagged_unsigned:0,unflagged_uncertified:0},
  historically_excluded:{held:0,source_flagged_unsigned:0,unflagged_uncertified:0}};
 for(const r of tab){
  const e=valid.get(r.original_source_id);
  assert.ok(e,'Original Valid Source absent from previously frozen V11 ledger');
  assert.equal(e.filename,r.original_filename);
  assert.equal(e.preexisting_research_hold,r.preexisting_research_hold);
  assert.equal(r.source_to_clean17_pixel_identity_verified,false);
  assert.equal(r.confirmed_clean17_membership,false);
  assert.equal(r.eligible_for_scientific_scoring,false);
  const k=r.clean17_export_candidate?'provisional':'historically_excluded';
  const type=e.provisional_research_disposition==='RETAIN_PREEXISTING_RESEARCH_HOLD'?'held':
    e.provisional_research_disposition==='PENDING_INDIVIDUAL_SOURCE_LINEAGE_DECISION'?'source_flagged_unsigned':
    e.provisional_research_disposition==='NO_SCREEN_FLAG_INDEPENDENCE_UNCERTIFIED'?'unflagged_uncertified':null;
  assert.ok(type,'Unexpected source-family status');
  result[k][type]++;
 }
 return result;
}
const t=cross(V.valid_rows);
assert.deepEqual(t,{
 provisional:{held:5,source_flagged_unsigned:87,unflagged_uncertified:367},
 historically_excluded:{held:0,source_flagged_unsigned:7,unflagged_uncertified:2}
});
assert.equal(V.valid_rows.length,468);
assert.equal(H.human_approved_links_preserved,19);
assert.equal(H.saved_worker_ppe_states,38);
assert.equal(H.scoring_ready,false);
if(process.argv[2]==='--self-test'){
 const tampered=structuredClone(V.valid_rows);
 tampered[0].confirmed_clean17_membership=true;
 assert.throws(()=>cross(tampered),'False verified Clean17 membership passed');
 console.log('SEER_V12_CROSSWALK_SYNTHETIC_FALSE_CLEARANCE_FAIL_CLOSED_PASS');
}else if(!process.argv[2]||process.argv[2]==='--verify'){
 console.log('SEER_V12_CLEAN17_5_HELD_87_FLAGGED_367_UNCERTIFIED_NOT_SCORED_PASS');
}else{throw Error('Usage: --verify | --self-test');}
