#!/usr/bin/env node
/**
 * V33: read-only post-hoc analysis of the real V30 frozen target/curve ledger.
 * No model calls, no image loading, no worker-level compliance inference.
 *
 * Usage:
 *   node tools/verify_v33_existing_xai.mjs --verify
 *   node tools/verify_v33_existing_xai.mjs --self-test
 */
import fs from 'node:fs';
import assert from 'node:assert/strict';
import path from 'node:path';
import {createHash} from 'node:crypto';
import {fileURLToPath} from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const sourceName = 'V30_ACTUAL_PROGRESSIVE_XAI_RESULTS_2026-11-22.json';
const auditName = 'V30_INDEPENDENT_NUMERIC_AUDIT_2026-11-22.json';
const archivedName = 'V33_A5_A6_NUMERIC_ROBUSTNESS_2026-11-22.json';
const read = name => JSON.parse(fs.readFileSync(path.join(root, name), 'utf8'));
const tol = 1e-9;
const numeric = (a, b, label, eps = tol) => {
  assert.ok(typeof a === 'number' && typeof b === 'number' &&
            Number.isFinite(a) && Number.isFinite(b) && Math.abs(a-b) <= eps,
            label + ': numeric mismatch (' + a + ' versus ' + b + ')');
};
const mean = (rows, key) => {
  assert.ok(rows.length > 0, 'empty mean');
  return rows.reduce((s, r) => s + r[key], 0) / rows.length;
};
const trapezoid = pts => pts.slice(1).reduce((sum, p, i) =>
  sum + (p.normalized_score + pts[i].normalized_score) *
  (p.modified_fraction - pts[i].modified_fraction) * 0.5, 0);
const nominalArea = pts => pts.slice(1).reduce((sum, p, i) =>
  sum + (p.normalized_score + pts[i].normalized_score) *
  (p.requested_fraction - pts[i].requested_fraction) * 0.5, 0);
function earlyArea(pts, stop = 0.3) {
  const truncated = [pts[0]];
  for (let i=1; i<pts.length; i++) {
    if (pts[i].modified_fraction <= stop + 1e-12) truncated.push(pts[i]);
    else {
      const a = pts[i-1], b = pts[i];
      const w = (stop - a.modified_fraction) / (b.modified_fraction - a.modified_fraction);
      assert.ok(w >= 0 && w <= 1, 'early-area interpolation outside valid range');
      truncated.push({modified_fraction:stop,
        normalized_score:a.normalized_score + w*(b.normalized_score-a.normalized_score)});
      break;
    }
  }
  numeric(truncated.at(-1).modified_fraction, stop, 'early-area endpoint');
  return trapezoid(truncated)/stop;
}
function gitBlobSha256AndGitSha() {
  const raw=fs.readFileSync(path.join(root,sourceName));
  return {
    gitsha:createHash('sha1').update(Buffer.from('blob ' + raw.byteLength + '\0')).update(raw).digest('hex'),
    sha256:createHash('sha256').update(raw).digest('hex'),
  };
}
function compute(v30, audit) {
  assert.equal(v30.status,'COMPLETED');
  assert.equal(v30.model_id,'altayyar-0oflt-lafos-qqauz/2');
  assert.equal(v30.total_v30_model_inference_calls,1068);
  assert.equal(v30.baseline_preflight_model_calls_already_executed,8);
  assert.equal(v30.model_inference_calls_this_run,1060);
  assert.equal(v30.inference_settings.confidence,0.20);
  assert.equal(v30.inference_settings.overlap,0.50);
  assert.equal(v30.explainer.grid_rows,8);
  assert.equal(v30.explainer.grid_cols,8);
  assert.equal(v30.curve_settings.step_percent,10);
  assert.equal(v30.constraints.no_test_accessed,true);
  assert.equal(audit.audit_status,'PASS_NUMERIC_INTEGRITY_ONLY');
  assert.equal(audit.v30_total_model_calls,1068);
  assert.equal(audit.unique_targets,10);
  assert.equal(v30.target_results.length,10);
  const names=['saliency','random','inverse_saliency'];
  const directions=['deletion','insertion'];
  const keys=['saliency_deletion_auc','saliency_insertion_auc','random_deletion_auc','random_insertion_auc',
    'deletion_advantage','insertion_advantage','early30_deletion_advantage',
    'early30_insertion_advantage','blurred_to_baseline_ratio'];
  const rows=v30.target_results.map(t => {
    assert.equal(t.map_status,'RANKABLE');
    assert.equal(t.curve_status,'EXECUTED');
    assert.ok(t.baseline_confidence>0 && t.baseline_confidence<=1);
    assert.ok(['train','valid'].includes(t.split),'unexpected split');
    assert.ok(Array.isArray(t.arms) && t.arms.length>=1 && t.arms.length<=2);
    const get=(o,d)=>t.curves[o][d];
    for (const o of names) for (const d of directions) {
      const item=get(o,d), p=item.points;
      assert.equal(item.status,'EXECUTED');
      assert.equal(p.length,11);
      assert.equal(p[0].requested_fraction,0);
      assert.equal(p[10].requested_fraction,1);
      numeric(p[0].modified_fraction,0,'first x');
      numeric(p[10].modified_fraction,1,'last x');
      for(let j=0;j<11;j++) {
        assert.ok(Number.isFinite(p[j].normalized_score) &&
          p[j].normalized_score>=0 && p[j].normalized_score<=1);
        if(j) {
          assert.ok(p[j].modified_fraction>p[j-1].modified_fraction, 'non-monotone modified fractions');
          assert.ok(p[j].requested_fraction>p[j-1].requested_fraction, 'non-monotone requested fractions');
        }
      }
      numeric(trapezoid(p),item.auc,'recomputed AUC');
    }
    const auc=(o,d)=>get(o,d).auc;
    const salD=auc('saliency','deletion'), salI=auc('saliency','insertion'),
      rndD=auc('random','deletion'), rndI=auc('random','insertion');
    const row={
      target_id:t.target_id, image_key:t.image_key, source_asset_id:t.asset_id,
      split:t.split, target_class:t.target_class, arms:t.arms,
      baseline_confidence:t.baseline_confidence,
      blurred_endpoint_confidence:t.blurred_endpoint.score,
      blurred_to_baseline_ratio:t.blurred_endpoint.score/t.baseline_confidence,
      saliency_deletion_auc:salD, saliency_insertion_auc:salI,
      random_deletion_auc:rndD, random_insertion_auc:rndI,
      inverse_deletion_auc:auc('inverse_saliency','deletion'),
      inverse_insertion_auc:auc('inverse_saliency','insertion'),
      deletion_advantage:rndD-salD,
      insertion_advantage:salI-rndI,
      early30_deletion_advantage:earlyArea(get('random','deletion').points) -
        earlyArea(get('saliency','deletion').points),
      early30_insertion_advantage:earlyArea(get('saliency','insertion').points) -
        earlyArea(get('random','insertion').points),
      max_auc_recalc_abs_error:Math.max(...names.flatMap(o=>directions.map(d=>
        Math.abs(trapezoid(get(o,d).points)-auc(o,d))))),
      max_nominal_vs_actual_auc_abs_difference:Math.max(...names.flatMap(o=>directions.map(d=>
        Math.abs(nominalArea(get(o,d).points)-auc(o,d))))),
    };
    return row;
  });
  assert.equal(new Set(rows.map(r=>r.target_id)).size,10,'duplicate target IDs');
  assert.equal(new Set(rows.map(r=>r.image_key)).size,8,'incorrect source image count');
  const shared=rows.filter(r=>r.arms.length===2);
  const a5=rows.filter(r=>r.arms.includes('A5'));
  const a6=rows.filter(r=>r.arms.includes('A6'));
  const ua=rows.filter(r=>r.arms.length===1 && r.arms[0]==='A5');
  const ub=rows.filter(r=>r.arms.length===1 && r.arms[0]==='A6');
  assert.equal(shared.length,6);
  assert.equal(a5.length,8);assert.equal(a6.length,8);
  assert.equal(ua.length,2);assert.equal(ub.length,2);
  assert.deepEqual(shared.map(r=>r.target_id).sort(),audit.shared_target_ids.slice().sort());
  const avg=x=>Object.fromEntries(keys.map(k=>[k,mean(x,k)]));
  const exact={};
  for(const k of ['saliency_deletion_auc','saliency_insertion_auc','deletion_advantage','insertion_advantage']){
    const four=[...ua,...ub], observed=(ua.reduce((s,r)=>s+r[k],0)-ub.reduce((s,r)=>s+r[k],0))/8;
    const permutations=[];
    for(let i=0;i<4;i++)for(let j=i+1;j<4;j++){
      const other=four.filter((_,z)=>z!==i&&z!==j);
      permutations.push((four[i][k]+four[j][k]-other.reduce((s,r)=>s+r[k],0))/8);
    }
    exact[k]={
      observed_A5_minus_A6:observed,
      conditional_assignments:6,
      conditional_two_sided_tail_fraction:permutations.filter(v=>Math.abs(v)>=Math.abs(observed)-1e-12).length/6,
      min:Math.min(...permutations),max:Math.max(...permutations),
    };
  }
  const images=[...new Set(rows.map(r=>r.image_key))],loo={};
  for(const k of ['saliency_deletion_auc','saliency_insertion_auc','deletion_advantage','insertion_advantage']) {
    const vals=images.map(image=>{
      const av=a5.filter(r=>r.image_key!==image),bv=a6.filter(r=>r.image_key!==image);
      return {image_key:image,A5_minus_A6:mean(av,k)-mean(bv,k)};
    });
    loo[k]={minimum:Math.min(...vals.map(x=>x.A5_minus_A6)),
      maximum:Math.max(...vals.map(x=>x.A5_minus_A6)),
      sign_reversals_from_full_sample:vals.filter(x=>
        Math.sign(x.A5_minus_A6)!==Math.sign(mean(a5,k)-mean(a6,k))).length,
      by_image:vals};
  }
  return {rows,means:{all_targets:avg(rows),shared_targets:avg(shared),
      A5_selected:avg(a5),A6_selected:avg(a6),A5_only:avg(ua),A6_only:avg(ub)},
    exact,loo,
    diagnostics:{
      full_deletion_advantage_positive:rows.filter(x=>x.deletion_advantage>0).length,
      full_deletion_advantage_zero:rows.filter(x=>x.deletion_advantage===0).length,
      full_insertion_advantage_positive:rows.filter(x=>x.insertion_advantage>0).length,
      early30_deletion_advantage_positive:rows.filter(x=>x.early30_deletion_advantage>0).length,
      early30_insertion_advantage_positive:rows.filter(x=>x.early30_insertion_advantage>0).length,
      blurred_baseline_ratio_ge_0_8:rows.filter(x=>x.blurred_to_baseline_ratio>=.8).length,
      blurred_baseline_ratio_ge_0_9:rows.filter(x=>x.blurred_to_baseline_ratio>=.9).length,
      blurred_baseline_ratio_zero:rows.filter(x=>x.blurred_to_baseline_ratio===0).length,
      max_auc_recalc_abs_error:Math.max(...rows.map(x=>x.max_auc_recalc_abs_error)),
      max_nominal_vs_actual_auc_abs_difference:Math.max(...rows.map(x=>x.max_nominal_vs_actual_auc_abs_difference)),
      max_inverse_AUC_algebraic_identity_abs_error:Math.max(...rows.flatMap(x=>[
        Math.abs(x.inverse_deletion_auc-x.saliency_insertion_auc),
        Math.abs(x.inverse_insertion_auc-x.saliency_deletion_auc)])),
      inverse_is_independent_random_control:false,
    }};
}
function verify(v30,audit,archived,sha) {
  assert.equal(archived.status,'ACTUAL_V30_NUMERIC_POSTHOC_ANALYSIS_COMPLETED_NO_NEW_INFERENCE');
  assert.equal(archived.source_v30_git_blob_sha,sha);
  assert.equal(archived.design.additional_v33_model_calls,0);
  assert.equal(archived.design.actual_v30_model_calls,1068);
  assert.equal(archived.design.development_exposed,true);
  assert.equal(archived.design.unique_targets,10);
  assert.equal(archived.design.shared_targets,6);
  assert.equal(archived.design.fixed_random_control_per_target,1);
  assert.equal(archived.constraints.retraining,false);
  assert.equal(archived.constraints.no_test_accessed,true);
  assert.equal(archived.constraints.images_annotations_splits_unchanged,true);
  const calc=compute(v30,audit);
  for(const [i,row] of calc.rows.entries()){
    const saved=archived.per_target[i];
    for(const key of ['target_id','image_key','source_asset_id','split','target_class']){
      assert.equal(row[key],saved[key], 'target identity '+key);
    }
    assert.deepEqual(row.arms,saved.arms);
    for(const key of Object.keys(row)){
      if(typeof row[key]==='number')numeric(row[key],saved[key],'target '+i+' '+key);
    }
  }
  assert.equal(archived.per_target.length,10);
  for(const group of Object.keys(calc.means)) for(const [key,value] of Object.entries(calc.means[group])){
    numeric(value,archived.means[group][key],'group mean '+group+' '+key);
  }
  for(const [key,item] of Object.entries(calc.exact)){
    const saved=archived.conditional_balanced_reassignment[key];
    for(const prop of ['observed_A5_minus_A6','conditional_two_sided_tail_fraction','min','max'])
      numeric(item[prop],saved[prop],'exact reassignment '+key+' '+prop);
    assert.equal(saved.conditional_assignments,6);
  }
  for(const [key,item] of Object.entries(calc.loo)){
    const saved=archived.leave_one_source_image_out[key];
    for(const prop of ['minimum','maximum'])numeric(item[prop],saved[prop],'LOO '+key+' '+prop);
    assert.equal(item.sign_reversals_from_full_sample,saved.sign_reversals_from_full_sample);
    assert.equal(item.by_image.length,8);
    for(let i=0;i<8;i++){
      assert.equal(item.by_image[i].image_key,saved.by_image[i].image_key);
      numeric(item.by_image[i].A5_minus_A6,saved.by_image[i].A5_minus_A6,'LOO image '+key);
    }
  }
  for(const [key,value] of Object.entries(calc.diagnostics)){
    if(typeof value==='number')numeric(value,archived.control_diagnostics[key],'control '+key);
    else assert.equal(value,archived.control_diagnostics[key]);
  }
  assert.ok(calc.diagnostics.max_auc_recalc_abs_error<=1e-10);
  assert.ok(calc.diagnostics.max_inverse_AUC_algebraic_identity_abs_error<=1e-10);
  assert.equal(calc.diagnostics.full_deletion_advantage_positive,8);
  assert.equal(calc.diagnostics.full_insertion_advantage_positive,9);
  assert.equal(calc.diagnostics.blurred_baseline_ratio_ge_0_8,3);
  return {status:'PASS_V33_MATCHED_TARGET_REANALYSIS_FAIL_CLOSED',
    images:8,targets:10,shared_targets:6,
    additional_model_calls:0, A5_deletion_auc:calc.means.A5_selected.saliency_deletion_auc,
    A6_deletion_auc:calc.means.A6_selected.saliency_deletion_auc,
    A5_insertion_auc:calc.means.A5_selected.saliency_insertion_auc,
    A6_insertion_auc:calc.means.A6_selected.saliency_insertion_auc,
    conditional_deletion_reassignment_tail_fraction:calc.exact.saliency_deletion_auc.conditional_two_sided_tail_fraction,
    conditional_insertion_reassignment_tail_fraction:calc.exact.saliency_insertion_auc.conditional_two_sided_tail_fraction,
    source_hash_verified:true, inverse_complement_not_independent:true};
}
const v30=read(sourceName), audit=read(auditName), archived=read(archivedName);
const hashes=gitBlobSha256AndGitSha();
try{
  const outcome=verify(v30,audit,archived,hashes.gitsha);
  if(process.argv.includes('--self-test')) {
    const tamper=(which,mutate)=>{
      const v=structuredClone(v30),a=structuredClone(audit),r=structuredClone(archived);
      mutate(which==='source'?v:which==='audit'?a:r);
      assert.throws(()=>verify(v,a,r,hashes.gitsha));
    };
    tamper('source',v=>{v.target_results[0].curves.saliency.deletion.auc+=0.05;});
    tamper('source',v=>{v.target_results[0].curves.random.insertion.points[3].normalized_score=5;});
    tamper('source',v=>{v.target_results[0].arms=['A5'];});
    tamper('source',v=>{v.total_v30_model_inference_calls=1069;});
    tamper('audit',v=>{v.shared_target_ids=[];});
    tamper('archive',v=>{v.design.additional_v33_model_calls=1;});
    tamper('archive',v=>{v.means.A6_selected.saliency_deletion_auc+=0.01;});
    tamper('archive',v=>{v.control_diagnostics.inverse_is_independent_random_control=true;});
    tamper('archive',v=>{v.per_target[2].target_id='unmatched';});
    console.log('V33_NUMERIC_MUTATION_SELF_TEST_FAIL_CLOSED_PASS');
  } else if(process.argv.includes('--verify')) {
    console.log(JSON.stringify({...outcome,source_sha256:hashes.sha256},null,2));
  } else {
    console.error('Usage: --self-test or --verify');process.exitCode=2;
  }
}catch(error){
  console.error('V33_FAIL_CLOSED',error.stack||error.message);
  process.exitCode=1;
}
