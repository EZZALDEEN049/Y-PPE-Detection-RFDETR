#!/usr/bin/env node
/**
 * SEER-PPE V11: research source-eligibility and Person–PPE evaluation contract.
 * Offline only. No model execution, Test access or Roboflow mutations.
 *
 * --self-test: synthetic records only
 * --audit: current authentic read-only administrative/reference readiness
 * --score <bundle.json>: conditional VALIDATION-ONLY descriptive scoring after
 *                      signed lineage, human GT and frozen protocol gates.
 *
 * Passing any software test DOES NOT prove actual source independence or
 * convert synthetic examples into research model performance evidence.
 */
import {readFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import assert from 'node:assert/strict';

const R=new URL('../',import.meta.url);
const read=name=>JSON.parse(readFileSync(new URL(name,R),'utf8'));
const PPE=['hard_hat','safety_vest','goggles','face_mask','glove','safety_boot'];
const VALID_STATES=['PRESENT','ABSENT','UNKNOWN'];
const VERDICTS=['INDEPENDENT_SOURCE_SUPPORTED','SHARED_CAPTURE_SESSION_OR_SITE','SAME_IMAGE_OR_DERIVATIVE','SAME_ITEM_DISTINCT_PHOTO','UNRESOLVED'];
const model='altayyar-0oflt-lafos-qqauz/2';
function check(c,why){if(!c)throw Error('V11_GATE_BLOCKED: '+why);}
function nonempty(v){return typeof v==='string'&&v.trim().length>=3;}
const ratio=(a,b)=>b===0?null:a/b;
function exactKeys(actual,expected){return actual.length===expected.length&&actual.every(x=>expected.includes(x));}
function distinct(values,label){check(values.length===new Set(values).size,'duplicate '+label);}
const nameFor=x=>String(x??'');

export function signedEligibility(row,entry){
  check(row?.split==='valid','source must be original Valid');
  if(row.preexisting_research_hold)return {eligible:false,reason:'PREEXISTING_RESEARCH_HOLD_NOT_AUTOMATICALLY_LIFTED'};
  if(entry==null)return {eligible:false,reason:'NO_INDIVIDUAL_SIGNED_SOURCE_VERDICT'};
  check(entry.source_id===row.source_id,'source decision ID mismatch');
  check(VERDICTS.includes(entry.verdict),'invalid lineage verdict');
  check(nonempty(entry.reviewer_id)&&/^\d{4}-\d\d-\d\d$/.test(entry.signed_date??''),'invalid dated reviewer signoff');
  check(nonempty(entry.evidence_ref)&&nonempty(entry.evidence_basis),'case-specific evidence reference and basis required');
  check(entry.per_source_review_confirmed===true,'general visual acceptance is not source-specific signoff');
  if(entry.verdict!=='INDEPENDENT_SOURCE_SUPPORTED')
    return {eligible:false,reason:'NON_INDEPENDENT_OR_NOT_FULLY_ESTABLISHED'};
  check(nonempty(entry.acquisition_group_id),'independent acquisition grouping missing');
  check(entry.train_family_crosscheck_completed===true,'Train-family comparison must be signed');
  check(nonempty(entry.train_family_comparison_evidence_ref),'Train-family comparison evidence missing');
  check(entry.no_train_family_overlap_supported===true,'cannot certify independence while overlap unresolved');
  return {eligible:true,reason:'CASE_SPECIFIC_SIGNED_SOURCE_INDEPENDENCE_SUPPORTED'};
}

export function verifyLineage(ledger,overlay,planning,queue,manifest){
  check(ledger.schema_version==='seer-ppe/source-lineage-eligibility-ledger/v0.11','wrong ledger version');
  check(overlay.schema_version==='seer-ppe/signed-source-lineage-decision-overlay/v0.11','wrong overlay version');
  check(overlay.base_ledger==='SOURCE_ELIGIBILITY_DECISION_LEDGER_2026-11-21_V11.json','incorrect overlay base');
  check(ledger.rows.length===468&&planning.valid_rows.length===468,'468 Valid records required');
  check(manifest.images.length===2093&&!manifest.images.some(x=>x.split==='test'),'original Train/Valid manifest only');
  check(queue.review_queue.length===99,'99-source review queue required');
  check(queue.original_near_hash_pairs.length===46,'original near-edge evidence changed');
  const sourceIds=new Map(manifest.images.map(x=>[x.image_id,x]));
  distinct([...sourceIds.keys()],'source ID');
  const oldById=new Map(planning.valid_rows.map(x=>[x.source_id,x]));
  const flagById=new Map(queue.review_queue.map(x=>[x.valid_source_id,x]));
  distinct([...oldById.keys()],'V08 Valid ID');
  distinct([...flagById.keys()],'V06 review ID');
  distinct(ledger.rows.map(x=>x.source_id),'ledger Valid ID');
  const assigned=new Map();
  check(Array.isArray(overlay.decisions),'overlay decisions must be array');
  for(const d of overlay.decisions){
    check(oldById.has(d.source_id),'unknown Valid Source ID in overlay');
    check(!assigned.has(d.source_id),'two curator decisions on one source; preserve history by versioning');
    assigned.set(d.source_id,d);
  }
  const count={RETAIN_PREEXISTING_RESEARCH_HOLD:0,PENDING_INDIVIDUAL_SOURCE_LINEAGE_DECISION:0,NO_SCREEN_FLAG_INDEPENDENCE_UNCERTIFIED:0};
  let signed=0,eligible=0,flagged=0;
  const eligibility=new Map();
  for(const row of ledger.rows){
    const v=oldById.get(row.source_id),src=sourceIds.get(row.source_id),q=flagById.get(row.source_id);
    check(!!v&&src?.split==='valid','ledger source is not frozen original Valid');
    check(row.filename===src.filename&&row.filename===v.filename,'filename mismatch');
    check(row.width===v.width&&row.height===v.height,'dimension mismatch');
    check(row.split==='valid','Test/Train source smuggled into Valid ledger');
    check(row.individual_source_family_signoff===null&&row.site_independent_scoring_eligible===false,
      'immutable baseline ledger must remain unsigned');
    check(row.no_roboflow_mutation===true,'baseline indicates source write');
    const expected=v.prior_hold?'RETAIN_PREEXISTING_RESEARCH_HOLD':q?
      'PENDING_INDIVIDUAL_SOURCE_LINEAGE_DECISION':'NO_SCREEN_FLAG_INDEPENDENCE_UNCERTIFIED';
    check(row.provisional_research_disposition===expected,'administrative bucket mismatch');
    check(row.preexisting_research_hold===v.prior_hold,'hold changed');
    check(JSON.stringify(row.review_queue_reasons)===JSON.stringify(q?.reasons??[]),'screen evidence changed');
    check(row.nearest_train_id===(q?.nearest_train_id??null),'nearest Train evidence changed');
    check(row.near_hash_train_pairs.length===(q?.original_dhash_candidate_pairs??[]).length,'dHash edge evidence changed');
    count[expected]++;
    if(q)flagged++;
    const verdict=signedEligibility(row,assigned.get(row.source_id));
    if(assigned.has(row.source_id))signed++;
    if(verdict.eligible)eligible++;
    eligibility.set(row.source_id,verdict);
  }
  check(flagged===99,'99 original queue cases not reproduced');
  check(count.RETAIN_PREEXISTING_RESEARCH_HOLD===5,'five prior holds changed');
  check(count.PENDING_INDIVIDUAL_SOURCE_LINEAGE_DECISION===94,'94 candidate count changed');
  check(count.NO_SCREEN_FLAG_INDEPENDENCE_UNCERTIFIED===369,'369 unflagged-uncertified count changed');
  check(ledger.near_pairs===46&&ledger.connected_similarity_components===27,'graph counts changed');
  check(ledger.individual_human_lineage_signoffs===0,'baseline signed state falsely changed');
  check(ledger.independently_scoring_eligible_rows===0,'baseline scoring state falsely changed');
  check(ledger.scientific_scoring_ready===false,'baseline scoring state must remain false');
  check(overlay.test_images_accessed===false&&overlay.score_eligibility_override===false,'unsafe overlay');
  return {total:468,dispositions:count,flagged:99,signed_source_decisions:signed,
    source_independence_supported_valid_images:eligible,eligibility};
}

export function scoreValidationBundle(bundle,freeze,eligibility,options={}){
  check(bundle?.schema_version==='seer-ppe/worker-visual-validation-bundle/v0.11','wrong bundle schema');
  check(bundle.split==='valid'&&bundle.model_id===model,'only fixed-model Valid scoring; Test disabled');
  check(freeze?.schema_version==='seer-ppe/validation-scoring-freeze/v0.11','wrong freeze version');
  check(freeze.state==='SIGNED_VALIDATION_ONLY'&&freeze.authorized===true,
    'author-approved Validation freeze not active');
  check(freeze.test_authorized===false,'protected Test not allowed by this evaluator');
  check(freeze.model_id===model,'model ID changed');
  for(const key of ['source_lineage_signed','clean17_membership_reconciled',
    'person_reference_signed','person_coverage_audited','matching_policy_frozen',
    'metrics_plan_frozen','thresholds_frozen']){
    check(freeze.gates?.[key]===true,'freeze prerequisite absent: '+key);
  }
  check(nonempty(freeze.freeze_reviewer_id)&&/^\d{4}-\d\d-\d\d$/.test(freeze.freeze_date??''),
    'freeze signature absent');
  check(nonempty(freeze.protocol_commit_sha)&&freeze.protocol_commit_sha.length>=12,'protocol commit not pinned');
  check(Array.isArray(freeze.approved_valid_source_ids)&&freeze.approved_valid_source_ids.length>0,'no frozen approved samples');
  distinct(freeze.approved_valid_source_ids,'approved valid images');
  check(Array.isArray(bundle.cases)&&bundle.cases.length>0,'empty validation scoring bundle');
  const ids=bundle.cases.map(c=>c.source_id);distinct(ids,'validation scoring source');
  check(ids.length===freeze.approved_valid_source_ids.length&&
    ids.every(id=>freeze.approved_valid_source_ids.includes(id)),'case sources differ from frozen scope');
  check(typeof bundle.run_id==='string'&&bundle.run_id.trim().length>=3,'run ID missing');
  const byType=Object.fromEntries(PPE.map(p=>[p,{
    known_gt:0,human_unknown:0,prediction_abstentions:0,retained:0,correct:0,wrong:0,
    gt_present:0,tp_present:0,fp_present:0,fn_present_decided:0,
    gt_present_abstained:0,unscored_human_unknown_predictions:0
  }]));
  const pair={known_owner_items:0,unknown_owner_items:0,correct:0,
    wrong_owner:0,abstain_known:0,guesses_on_human_unknown:0,tp:0,fp:0,fn:0};
  let signedZeroPersonControls=0, workers=0, humanPolicyUnknown=0;
  for(const ca of bundle.cases){
    check(ca.split==='valid','Test/Train case blocked');
    check(eligibility.get(ca.source_id)?.eligible===true,'individual source independence not signed');
    check(ca.clean17_member_verified===true,'Clean17 scope not reconciled for case');
    check(ca.human_reference_complete===true&&ca.person_coverage_human_signed===true,
      'human gold, including missed persons/no-person controls, required');
    check(ca.person_correspondence_verified===true&&ca.item_correspondence_verified===true,
      'person/item GT correspondence not independently checked');
    check(nonempty(ca.reference_evidence_ref)&&nonempty(ca.reference_reviewer_id),'per-case human evidence missing');
    check(Array.isArray(ca.reference?.people)&&Array.isArray(ca.predictions?.people),
      'people arrays missing');
    check(Array.isArray(ca.reference?.items)&&Array.isArray(ca.predictions?.items),'item arrays missing');
    const pp=ca.reference.people,pr=ca.predictions.people;
    const people=pp.map(x=>x.person_id),predPersons=pr.map(x=>x.person_id);
    distinct(people,'reference person IDs');distinct(predPersons,'predicted person IDs');
    check(people.length===predPersons.length&&people.every(x=>predPersons.includes(x)),
      'predicted person coverage must contain every referenced person, including explicit abstentions');
    if(!people.length)signedZeroPersonControls++;
    workers+=people.length;
    const predPeople=new Map(pr.map(x=>[x.person_id,x]));
    for(const h of pp){
      check(nonempty(h.person_id)&&h.visual_states&&h.task_mandates,'human PPE states or mandates missing');
      const d=predPeople.get(h.person_id);
      check(exactKeys(Object.keys(h.visual_states),PPE),'human six-state PPE reference incomplete');
      check(exactKeys(Object.keys(h.task_mandates),PPE),'six PPE task-mandate fields required');
      check(d?.visual_states&&exactKeys(Object.keys(d.visual_states),PPE),'missing model PPE predictions for some person');
      for(const typ of PPE){
        const gt=h.visual_states[typ],pd=d.visual_states[typ],pol=h.task_mandates[typ];
        check(VALID_STATES.includes(gt)&&VALID_STATES.includes(pd),'no MISSING/NOT_RECORDED or invalid state');
        check(['REQUIRED','NOT_REQUIRED','POLICY_UNKNOWN'].includes(pol),'invalid separately-sourced PPE mandate');
        if(pol==='POLICY_UNKNOWN')humanPolicyUnknown++;
        const a=byType[typ];
        if(gt==='UNKNOWN'){a.human_unknown++;if(pd!=='UNKNOWN')a.unscored_human_unknown_predictions++;continue;}
        a.known_gt++;
        if(gt==='PRESENT')a.gt_present++;
        if(pd==='UNKNOWN'){a.prediction_abstentions++;if(gt==='PRESENT')a.gt_present_abstained++;continue;}
        a.retained++;
        if(pd===gt)a.correct++;else a.wrong++;
        if(pd==='PRESENT'&&gt==='PRESENT')a.tp_present++;
        if(pd==='PRESENT'&&gt==='ABSENT')a.fp_present++;
        if(pd==='ABSENT'&&gt==='PRESENT')a.fn_present_decided++;
      }
    }
    const items=ca.reference.items,ipred=ca.predictions.items;
    distinct(items.map(x=>x.item_id),'reference item IDs');
    distinct(ipred.map(x=>x.item_id),'predicted item IDs');
    const predMap=new Map(ipred.map(x=>[x.item_id,x]));
    check(items.length===ipred.length&&items.every(x=>predMap.has(x.item_id)),
      'explicit prediction/abstention required for every matched item; extras handled by separate detector audit');
    for(const item of items){
      const p=predMap.get(item.item_id);
      check(nonempty(item.item_id)&&['MATCHED','UNKNOWN'].includes(item.owner_state),
        'invalid human owner reference');
      check(p&&['MATCHED','ABSTAIN'].includes(p.decision),'invalid predicted item disposition');
      if(p.decision==='MATCHED')check(people.includes(p.person_id),'predicted owner not aligned to known person');
      if(p.decision==='ABSTAIN')check(p.person_id===null,'abstain may not assign a worker');
      if(item.owner_state==='UNKNOWN'){
        pair.unknown_owner_items++;
        check(item.person_id===null,'unknown human owner cannot carry a person ID');
        if(p.decision==='MATCHED')pair.guesses_on_human_unknown++;
        continue;
      }
      check(people.includes(item.person_id),'human MATCHED owner not in person reference');
      pair.known_owner_items++;
      if(p.decision==='ABSTAIN'){pair.abstain_known++;pair.fn++;continue;}
      if(p.person_id===item.person_id){pair.correct++;pair.tp++;}
      else{pair.wrong_owner++;pair.fp++;pair.fn++;}
    }
  }
  const visual=Object.fromEntries(PPE.map(typ=>{
    const a=byType[typ];
    return [typ,{...a,
      retained_cell_coverage:ratio(a.retained,a.known_gt),
      accuracy_among_retained:ratio(a.correct,a.retained),
      present_precision_among_decided:ratio(a.tp_present,a.tp_present+a.fp_present),
      present_recall_over_all_known_gt:ratio(a.tp_present,a.gt_present),
      present_recall_among_retained_gt_present:
        ratio(a.tp_present,a.tp_present+a.fn_present_decided)}];
  }));
  return {
    schema_version:'seer-ppe/descriptive-valid-only-person-ppe-summary/v0.11',
    evaluation_scope:'FROZEN_VALIDATION_DESCRIPTIVE_ONLY_NOT_HOLDOUT_TEST',
    model_id:model,run_id:bundle.run_id,valid_images:bundle.cases.length,
    human_reviewed_workers:workers,signed_zero_person_controls:signedZeroPersonControls,
    visual,association:{
      ...pair,pair_precision:ratio(pair.tp,pair.tp+pair.fp),
      pair_recall_including_abstentions:ratio(pair.tp,pair.tp+pair.fn),
      pair_f1:(pair.tp+pair.fp>0&&pair.tp+pair.fn>0)?
        2*pair.tp/(2*pair.tp+pair.fp+pair.fn):null,
      evaluation_universe:'ONLY_EXPLICITLY_BOX_CORRESPONDENCE_VERIFIED_ITEMS'
    },
    task_policy_unknown_cells:humanPolicyUnknown,
    workplace_compliance_metrics:null,
    detector_mAP:null,energy_joules:null,
    person_or_item_detection_metrics:null,
    statistical_confidence_intervals:null,
    may_be_reported_as_independent_test:false,
    measurement_limits:'Visual state and post-alignment item ownership only; no site-policy compliance, detector mAP, true electrical energy or independent Test generalization.'
  };
}

export function audit(){
  const ledger=read('SOURCE_ELIGIBILITY_DECISION_LEDGER_2026-11-21_V11.json');
  const overlay=read('SOURCE_LINEAGE_SIGNED_DECISIONS_2026-11-21_V11.json');
  const plan=read('VALIDATION_ELIGIBILITY_PLANNING_MANIFEST_2026-11-21_V08.json');
  const q=read('SOURCE_FAMILY_REVIEW_QUEUE_2026-11-21_V06.json');
  const manifest=read('SOURCE_ID_MANIFEST_TRAIN_VALID_2026-11-19_V01.json');
  const human=read('PERSON_PPE_REFERENCE_LIVE_SNAPSHOT_2026-11-21_V09.json');
  const freeze=read('VALIDATION_PERSON_PPE_SCORING_FREEZE_2026-11-21_V11.json');
  const result=verifyLineage(ledger,overlay,plan,q,manifest);
  check(human.case_count===4&&human.case_complete_count===0,'Train reference status unexpectedly changed');
  check(human.human_approved_links_preserved===19,'19 approved human associations changed');
  check(human.saved_worker_ppe_states===38&&human.expected_worker_ppe_states===42,'38/42 original states changed');
  check(human.missing_state_cells.length===4,'B missing cells count changed');
  check(human.case_D_human_signed_zero_person_decision===false,'D human-signoff mismatch');
  check(human.scoring_ready===false,'human Train gold must remain incomplete');
  check(freeze.authorized===false&&freeze.state==='NOT_FROZEN','current freeze cannot silently authorize scoring');
  check(freeze.test_authorized===false,'Test access is not authorized');
  return {
    stage:'V11_EXECUTABLE_READ_ONLY_ELIGIBILITY_AND_REFERENCE_GATE',
    original_valid_records:result.total,
    source_review_counts:result.dispositions,
    signed_individual_source_verdicts:result.signed_source_decisions,
    signed_source_independent_valid:result.source_independence_supported_valid_images,
    valid_reference_person_ppe_cases_scored:0,
    saved_train_human_links:19,
    saved_train_visual_states:38,
    expected_train_visual_states:42,
    missing_B_visual_states:4,
    D_human_signed_zero_person:false,
    validated_scoring_freeze_active:false,
    original_model_retrained:false,
    roboflow_cases_modified:false,
    test_accessed:false,
    all_scientific_accuracy_metrics:null,
    scoring_ready:false,
    explicit_blockers:[
      'No image-specific signed source-independence decisions for Valid',
      'Clean17 original-source membership needs image-ID reconciliation before any scoring',
      'Missing Valid worker-level gold, verified person/item correspondences, and evaluation policy freeze',
      'Original Train B four cells and D zero-person human decision remain unrecorded; not usable as test gold',
      'Protected Test evaluation deliberately blocked'
    ]
  };
}

function selfTest(){
  const src={source_id:'v-synthetic',split:'valid',preexisting_research_hold:false};
  const good={source_id:'v-synthetic',verdict:'INDEPENDENT_SOURCE_SUPPORTED',
    reviewer_id:'author-researcher',signed_date:'2026-11-21',evidence_ref:'evidence/ref',
    evidence_basis:'signed image-specific acquisition provenance',per_source_review_confirmed:true,
    acquisition_group_id:'independent-session',train_family_crosscheck_completed:true,
    train_family_comparison_evidence_ref:'evidence/comparison',no_train_family_overlap_supported:true};
  check(signedEligibility(src,null).eligible===false,'unsigned fake source passed');
  check(signedEligibility(src,good).eligible===true,'signed synthetic independence failed');
  check(signedEligibility({...src,preexisting_research_hold:true},good).eligible===false,
    'prior held synthetic source auto-cleared');
  check(signedEligibility(src,{...good,verdict:'SAME_ITEM_DISTINCT_PHOTO'}).eligible===false,
    'same item photo was wrongly treated as proven independent source');
  assert.throws(()=>signedEligibility(src,{...good,train_family_crosscheck_completed:false}));
  const freeze={schema_version:'seer-ppe/validation-scoring-freeze/v0.11',
    state:'SIGNED_VALIDATION_ONLY',authorized:true,test_authorized:false,model_id:model,
    gates:{source_lineage_signed:true,clean17_membership_reconciled:true,
      person_reference_signed:true,person_coverage_audited:true,matching_policy_frozen:true,
      metrics_plan_frozen:true,thresholds_frozen:true},freeze_reviewer_id:'researcher',
    freeze_date:'2026-11-21',protocol_commit_sha:'synthetic-contract-sha-123',
    approved_valid_source_ids:['v-synthetic']};
  const human={visual_states:{
    hard_hat:'PRESENT',safety_vest:'ABSENT',goggles:'UNKNOWN',face_mask:'UNKNOWN',
    glove:'PRESENT',safety_boot:'UNKNOWN'},
    task_mandates:Object.fromEntries(PPE.map(p=>[p,'POLICY_UNKNOWN']))};
  const pred={visual_states:{
    hard_hat:'PRESENT',safety_vest:'PRESENT',goggles:'UNKNOWN',
    face_mask:'UNKNOWN',glove:'UNKNOWN',safety_boot:'UNKNOWN'}};
  const ca={source_id:'v-synthetic',split:'valid',clean17_member_verified:true,
    human_reference_complete:true,person_coverage_human_signed:true,
    person_correspondence_verified:true,item_correspondence_verified:true,
    reference_evidence_ref:'synthetic/review-evidence',reference_reviewer_id:'researcher',
    reference:{people:[{person_id:'P001',...human}],
      items:[{item_id:'E001',owner_state:'MATCHED',person_id:'P001'},
             {item_id:'E002',owner_state:'UNKNOWN',person_id:null}]},
    predictions:{people:[{person_id:'P001',...pred}],
      items:[{item_id:'E001',decision:'MATCHED',person_id:'P001'},
             {item_id:'E002',decision:'MATCHED',person_id:'P001'}]}};
  const bundle={schema_version:'seer-ppe/worker-visual-validation-bundle/v0.11',
    split:'valid',model_id:model,run_id:'synthetic-only',cases:[ca]};
  const map=new Map([['v-synthetic',{eligible:true}]]);
  const r=scoreValidationBundle(bundle,freeze,map);
  assert.equal(r.visual.hard_hat.retained_cell_coverage,1);
  assert.equal(r.visual.safety_vest.fp_present,1);
  assert.equal(r.visual.glove.prediction_abstentions,1);
  assert.equal(r.visual.goggles.human_unknown,1);
  assert.equal(r.association.tp,1);
  assert.equal(r.association.guesses_on_human_unknown,1);
  assert.equal(r.workplace_compliance_metrics,null);
  assert.equal(r.detector_mAP,null);
  assert.throws(()=>scoreValidationBundle(bundle,{...freeze,authorized:false},map));
  assert.throws(()=>scoreValidationBundle({...bundle,split:'test'},freeze,map));
  assert.throws(()=>scoreValidationBundle(bundle,freeze,new Map()));
  assert.throws(()=>scoreValidationBundle(
    {...bundle,cases:[{...ca,reference:{...ca.reference,people:[{
      ...ca.reference.people[0],
      visual_states:{...human.visual_states,safety_boot:'NOT_RECORDED'}}]}}]},
    freeze,map));
  assert.throws(()=>scoreValidationBundle(
    {...bundle,cases:[{...ca,person_coverage_human_signed:false}]},freeze,map));
  assert.throws(()=>scoreValidationBundle(
    {...bundle,cases:[{...ca,predictions:{...ca.predictions,people:[]}}]},freeze,map));
  console.log('SEER_V11_SYNTHETIC_ELIGIBILITY_PPE_AND_ABSTENTION_CONTRACT_PASS');
}

const mode=process.argv[2]??'--audit';
try{
  if(mode==='--self-test')selfTest();
  else if(mode==='--audit'){
    const x=audit();
    console.log(JSON.stringify(x,null,2));
    console.log('SEER_V11_REAL_RECORD_GATE_FAIL_CLOSED_PASS');
  }else if(mode==='--score'){
    check(process.argv.length===4,'usage: --score <valid-bundle.json>');
    const ledger=read('SOURCE_ELIGIBILITY_DECISION_LEDGER_2026-11-21_V11.json');
    const overlay=read('SOURCE_LINEAGE_SIGNED_DECISIONS_2026-11-21_V11.json');
    const v=verifyLineage(ledger,overlay,
      read('VALIDATION_ELIGIBILITY_PLANNING_MANIFEST_2026-11-21_V08.json'),
      read('SOURCE_FAMILY_REVIEW_QUEUE_2026-11-21_V06.json'),
      read('SOURCE_ID_MANIFEST_TRAIN_VALID_2026-11-19_V01.json'));
    const freeze=read('VALIDATION_PERSON_PPE_SCORING_FREEZE_2026-11-21_V11.json');
    const bundle=JSON.parse(readFileSync(process.argv[3],'utf8'));
    // V12 metadata candidates are not confirmed Clean17 image identities.
    // A supplied boolean in an input bundle cannot override the independent crosswalk.
    const crosswalk=read('SEER_PPE_VALID_TO_CLEAN17_PROVISIONAL_V12.json');
    const cleanBySource=new Map(crosswalk.valid_rows.map(x=>[x.original_source_id,x]));
    for (const c of bundle.cases ?? []) {
      const row=cleanBySource.get(c.source_id);
      check(row && row.confirmed_clean17_membership === true &&
        row.source_to_clean17_pixel_identity_verified === true,
        'V12_SOURCE_TO_CLEAN17_IDENTITY_UNVERIFIED_NO_SCIENTIFIC_SCORE');
    }
    console.log(JSON.stringify(scoreValidationBundle(bundle,freeze,v.eligibility),null,2));
  }else{throw Error('usage: --self-test | --audit | --score <bundle.json>');}
}catch(e){console.error(String(e));process.exitCode=2;}
