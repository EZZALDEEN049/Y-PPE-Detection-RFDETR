#!/usr/bin/env node
/** SEER-PPE V13 must preserve missing decisions, not fabricate positive or negative labels. */
import assert from "node:assert/strict";
import {readFileSync} from "node:fs";
const read=x=>JSON.parse(readFileSync(new URL('../'+x,import.meta.url),'utf8'));
const packet=read('PERSON_PPE_PENDING_HUMAN_SIGNOFF_2026-11-21_V13.json');
const source=read('SOURCE_LINEAGE_EVIDENCE_HANDOFF_2026-11-21_V13.json');
const old=read('PERSON_PPE_REFERENCE_LIVE_SNAPSHOT_2026-11-21_V09.json');
function verify(p,s){
 assert.equal(old.human_approved_links_preserved,19);
 assert.equal(old.saved_worker_ppe_states,38);
 assert.equal(old.expected_worker_ppe_states,42);
 assert.equal(p.prior_reference_human_links_preserved,19);
 assert.equal(p.prior_recorded_visual_states,38);
 assert.equal(p.prior_expected_visual_states,42);
 assert.equal(p.case_B_visual_state_pending.length,4);
 assert.deepEqual(p.case_B_visual_state_pending.map(x=>x.case+':'+x.person_id+':'+x.ppe_type).sort(),
 old.missing_state_cells.map(x=>x.case+':'+x.person_id+':'+x.ppe_type).sort());
 assert.ok(p.case_B_visual_state_pending.every(x=>x.current_live_reference==='NOT_RECORDED'&&
 x.human_final_visual_state===null&&x.human_reviewer_signoff===null&&x.not_inferred_from_AI===true));
 assert.equal(p.case_D.zero_person_scene_human_signed,null);
 assert.equal(p.case_D.human_reviewer_signoff,null);
 assert.equal(p.case_D.unseen_person_coverage_may_not_be_concluded_from_zero_detections,true);
 assert.equal(p.original_gt_case_writes,0);
 assert.equal(p.scoring_ready,false);
 assert.equal(s.preexisting_valid_holds,5);
 assert.equal(s.flagged_unsigned_candidates_in_provisional_valid,87);
 assert.equal(s.unflagged_but_independence_uncertified_in_provisional_valid,367);
 assert.equal(s.human_source_family_new_signoffs,0);
 assert.equal(s.known_cross_split_named_site.valid_source_ids.length,2);
 assert.equal(s.known_cross_split_named_site.train_source_ids.length,2);
 assert.equal(s.known_cross_split_named_site.human_source_family_signed,false);
 assert.equal(s.scientific_scoring_ready,false);
}
verify(packet,source);
if(process.argv[2]==='--self-test'){
 const p=structuredClone(packet);p.case_B_visual_state_pending[0].human_final_visual_state='ABSENT';
 assert.throws(()=>verify(p,source));
 const s=structuredClone(source);s.human_source_family_new_signoffs=1;
 assert.throws(()=>verify(packet,s));
 console.log('SEER_V13_SYNTHETIC_NO_FABRICATED_GOLD_OR_SOURCE_SIGNOFF_PASS');
}else{
 console.log('SEER_V13_LIVE_REFERENCE_4_PENDING_B_D_UNSIGNED_5_HOLDS_PASS');
}
