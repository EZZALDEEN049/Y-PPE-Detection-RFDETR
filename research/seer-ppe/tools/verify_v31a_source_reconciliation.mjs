#!/usr/bin/env node
/* V31-A read-only reconciler: source IDs and pair metrics must match archived V14/V15.
   It does not open images, infer, or sign/release any source family. */
import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';
import {fileURLToPath} from 'node:url';

const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const read=n=>JSON.parse(fs.readFileSync(path.join(root,n),'utf8'));
const same=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
function audit(dossier,priority,pairs,visual){
  const ids=priority.review_packets.map(x=>x.source_id);
  assert.equal(dossier.schema_version,'seer-ppe/v31-a-source-lineage-reconciliation/v0.31a');
  assert.equal(dossier.cases.length,11);
  assert.equal(new Set(dossier.cases.map(x=>x.valid_source_id)).size,11);
  assert.ok(same([...dossier.cases.map(x=>x.valid_source_id)].sort(),[...ids].sort()));
  assert.equal(dossier.totals.preexisting_holds,5);
  assert.equal(dossier.totals.technical_quarantines,6);
  assert.equal(dossier.totals.train_valid_pair_records,33);
  const reviewed=Object.fromEntries(visual.images_reviewed.map(x=>[x.image_id,x]));
  for(const c of dossier.cases){
    const p=priority.review_packets.find(x=>x.source_id===c.valid_source_id);
    assert.ok(p);
    assert.equal(c.original_valid_filename,p.original_valid_filename);
    assert.equal(c.clean17_valid_filename,p.verified_clean17_valid_filename);
    assert.equal(c.prior_status,p.research_status);
    assert.equal(c.prior_hard_hold,p.research_hard_hold_preexisting);
    assert.equal(c.nearest_train_source_id,p.nearest_direct_train_id);
    assert.equal(c.nearest_train_filename,p.nearest_direct_train_filename);
    assert.equal(c.prior_packet_strongest_ssim,p.strongest_direct_train_gray_ssim);
    const sourcePairs=pairs.pair_rows.filter(x=>x.valid_id===c.valid_source_id);
    assert.equal(c.all_direct_v14_train_candidate_pairs.length,sourcePairs.length);
    assert.equal(c.compared_train_candidate_count,sourcePairs.length);
    const mapped=c.all_direct_v14_train_candidate_pairs.map(x=>({
      train_source_id:x.train_source_id,train_filename:x.train_filename,
      gray_ssim:x.gray_ssim,rgb_mae:x.rgb_mae,
      embedding_cosine:x.embedding_cosine,
      orb_good_matches:x.orb_good_matches,orb_inliers:x.orb_inliers,
      raw_bytes_identical:x.raw_bytes_identical,
      technical_assessment:x.technical_assessment,
      original_dimensions:x.original_dimensions,train_export_dimensions:x.train_export_dimensions
    }));
    assert.ok(same(mapped,sourcePairs.map(x=>({
      train_source_id:x.train_id,train_filename:x.original_train_filename,
      gray_ssim:x.gray_ssim,rgb_mae:x.rgb_mean_absolute_error,
      embedding_cosine:x.original_embedding_cosine??null,
      orb_good_matches:x.orb_good_matches,orb_inliers:x.orb_inliers,
      raw_bytes_identical:x.raw_source_bytes_identical,
      technical_assessment:x.technical_content_consistency,
      original_dimensions:x.original_dimensions,train_export_dimensions:x.export_dimensions
    }))));
    assert.ok(c.all_direct_v14_train_candidate_pairs.every(x=>x.raw_bytes_identical===false));
    assert.equal(c.current_human_source_family_verdict,null);
    assert.equal(c.current_human_acquisition_site_id,null);
    assert.equal(c.current_human_capture_session_id,null);
    assert.equal(c.current_human_source_family_id,null);
    assert.equal(c.current_human_evidence_sha256,null);
    assert.equal(c.scoring_eligibility,false);
    assert.equal(c.hold_or_quarantine_release_authorized,false);
    const vi=reviewed[c.valid_source_id];
    if(vi){
      assert.equal(c.prior_visual_site_record.site_id,vi.site_id);
      assert.equal(c.prior_visual_site_record.site_review,vi.site_review);
    }
  }
  const wa63=dossier.cases.find(x=>x.valid_source_id==='0De0PEUDyeg9v1J3T6zr');
  const wa51=dossier.cases.find(x=>x.valid_source_id==='NZu6Faj6evgINF1qFE0V');
  const wa26=dossier.cases.find(x=>x.valid_source_id==='yeEvdkqXtNgsj7PZFDvI');
  assert.equal(wa63.confirmed_site_family_evidence.site_id,'site_school_22may_aseefrah');
  assert.equal(wa51.confirmed_site_family_evidence.site_id,'site_school_22may_aseefrah');
  assert.equal(wa26.prior_visual_site_record.site_id,'site_school_shahid_alalafi');
  assert.notEqual(wa26.prior_visual_site_record.site_id,'site_school_22may_aseefrah');
  assert.equal(wa26.prior_status,'RETAIN_PREEXISTING_RESEARCH_HOLD');
  assert.equal(dossier.findings.raw_byte_identical_pairs_among_11,0);
  assert.equal(dossier.constraints.model_inference_calls,0);
  assert.equal(dossier.constraints.original_images_reopened,false);
  assert.equal(dossier.constraints.test_opened,false);
  assert.equal(dossier.constraints.human_verdicts_created,0);
  assert.equal(dossier.constraints.scoring_eligibility_changed,0);
  assert.equal(dossier.constraints.prior_holds_preserved,true);
  assert.equal(dossier.constraints.technical_quarantines_preserved,true);
  return {status:'PASS_V31A_EVIDENCE_RECONCILIATION_ONLY',
    valid_cases:11,preexisting_holds:5,technical_quarantines:6,
    direct_train_pair_records:33,school_22may_valid:2,
    distinct_school_alalafi_valid:1,source_verdicts_signed:0,
    hold_releases:0,scoring_eligible:0,model_calls:0,test_access:false};
}
const dossier=read('V31_A_SOURCE_LINEAGE_RECONCILIATION_2026-11-22.json');
const priority=read('SOURCE_FAMILY_EVIDENCE_PRIORITY_11_2026-11-21_V15.json');
const pairs=read('ORIGINAL_99_VALID_SOURCE_FAMILY_PAIRS_2026-11-21_V14.json');
const visual=read('VISUAL_SOURCE_FAMILY_ADJUDICATION_2026-11-18_V01.json');
try{
 const result=audit(dossier,priority,pairs,visual);
 if(process.argv.includes('--self-test')){
  const tests=[
   x=>{x.cases.pop();},
   x=>{x.cases.find(c=>c.valid_source_id==='yeEvdkqXtNgsj7PZFDvI').prior_visual_site_record.site_id='site_school_22may_aseefrah';},
   x=>{x.cases[0].scoring_eligibility=true;},
   x=>{x.cases[0].current_human_source_family_verdict='INDEPENDENT_SOURCE_SUPPORTED';},
   x=>{x.constraints.model_inference_calls=1;},
  ];
  for(const mutate of tests){const bad=structuredClone(dossier);mutate(bad);assert.throws(()=>audit(bad,priority,pairs,visual));}
  console.log('V31A_MUTATION_SELF_TEST_FAIL_CLOSED_PASS');
 }else if(process.argv.includes('--verify'))console.log(JSON.stringify(result,null,2));
 else {console.error('Use --verify or --self-test');process.exitCode=2;}
}catch(e){console.error('V31A_RECONCILIATION_FAILED_CLOSED',e.message);process.exitCode=1;}
