#!/usr/bin/env node
/**
 * SEER-PPE V15 evidence-locked reviewer attestation and source-family readiness.
 * SCIENCE-SAFETY: no data/model/Test access, no auto-generated human signatures,
 * no promotion of author generic visual acceptance to source/site independence.
 * Live Roboflow Train-only reference decisions are a separate gold population.
 */
import assert from 'node:assert/strict';
import {readFileSync,writeFileSync,existsSync,realpathSync} from 'node:fs';
import {resolve,relative,sep} from 'node:path';
import {createHash} from 'node:crypto';
import {fileURLToPath} from 'node:url';

const ROOT=resolve(fileURLToPath(new URL('..',import.meta.url)));
const read=n=>JSON.parse(readFileSync(resolve(ROOT,n),'utf8'));
const SHA=s=>createHash('sha256').update(s).digest('hex');
const fail=s=>{throw Error('V15_EVIDENCE_GATE_BLOCKED:'+s);};
const check=(v,s)=>{if(!v)fail(s);};
const nonempty=s=>typeof s==='string'&&s.trim().length>=3;
const iso=s=>typeof s==='string'&&/^\d{4}-\d{2}-\d{2}$/.test(s)&&!Number.isNaN(Date.parse(s+'T00:00:00Z'))&&new Date(s+'T00:00:00Z').toISOString().slice(0,10)===s;
const ENUM=['INDEPENDENT_SOURCE_SUPPORTED','SHARED_CAPTURE_SESSION_OR_SITE','SAME_IMAGE_OR_DERIVATIVE','SAME_ITEM_DISTINCT_PHOTO','UNRESOLVED'];
function pinnedRef(path,hash){
 check(typeof path==='string'&&/^[A-Za-z0-9][A-Za-z0-9_./-]*\.(?:md|json|csv)$/.test(path),'malformed evidence path');
 check(!path.includes('..')&&!path.startsWith('/'),'evidence path traversal');
 const target=resolve(ROOT,path);
 const rel=relative(ROOT,target);
 check(rel&&!rel.startsWith('..'+sep)&&rel!=='..'&&existsSync(target),'evidence file absent');
 const real=realpathSync(target),sublocation=relative(ROOT,real);
 check(sublocation&&!sublocation.startsWith('..'+sep)&&sublocation!=='..',
  'evidence symlink escapes repository');
 check(typeof hash==='string'&&/^[a-f0-9]{64}$/.test(hash),'missing pinned evidence SHA');
 check(SHA(readFileSync(real))===hash,'evidence file SHA differs from reviewer attestation');
 return true;
}
function validateSourceDecision(d,source){
 check(d.source_id===source.original_valid_source_id,'Source ID mismatch');
 check(d.source_original_filename===source.original_valid_filename,'original filename does not match');
 check(d.clean17_export_filename===source.clean17_valid_filename,'clean export does not match');
 check(ENUM.includes(d.verdict),'invalid source-family verdict');
 check(nonempty(d.reviewer_id)&&iso(d.signed_date),'source reviewer and dated attestation missing');
 check(d.per_source_reviewer_inspected_evidence===true,'personal original Source inspection attestation missing');
 check(nonempty(d.evidence_basis),'source-specific evidence reasoning missing');
 pinnedRef(d.evidence_ref,d.evidence_sha256);
 // This evidence binding is *an integrity check*, not a proof that the reviewer spoke truth.
 if(d.verdict!=='INDEPENDENT_SOURCE_SUPPORTED')
  return {signed:true,independent:false,reason:'HUMAN_VERDICT_NOT_INDEPENDENT'};
 check(nonempty(d.acquisition_site_id)&&nonempty(d.capture_session_id)&&nonempty(d.acquisition_family_id),
  'independent acquisition/site/session family not documented');
 check(d.train_family_crosscheck_completed===true,'Train site/session family check not attested');
 check(d.no_train_capture_or_site_family_overlap_supported===true,'cannot support independence if site/session overlap');
 check(nonempty(d.train_family_comparison_basis),'Train-family comparison rationale absent');
 pinnedRef(d.train_family_evidence_ref,d.train_family_evidence_sha256);
 check(d.personally_attested_independence===true,'personal signed independence attestation absent');
 return {signed:true,independent:true,reason:'STRUCTURED_HUMAN_SOURCE_INDEPENDENCE_ATTESTATION'};
}
function validateBDecision(d,slot){
 check(d.slot_id===slot.slot_id,'B visual reference slot mismatch');
 check(['PRESENT','ABSENT','UNKNOWN'].includes(d.human_visual_state),'invalid visual state');
 check(d.case_id==='87b6cc58-43bd-4583-8b13-bd9b7413c03d'&&d.eval_case_revision===2,
   'case B ID/revision changed');
 check(nonempty(d.reviewer_id)&&iso(d.signed_date),'B visual reviewer signoff absent');
 check(d.personally_reviewed_original_visual_evidence===true,'B original image visual review not attested');
 pinnedRef(d.evidence_ref,d.evidence_sha256);
 return true;
}
function validateDDecision(d){
 if(d==null)return false;
 check(d.case_id==='c197d82e-7870-42a3-bf94-462420d3f6a2'&&d.eval_case_revision===1,
   'Case D ID/revision changed');
 check(['CONFIRM_ZERO_VISIBLE_PERSONS','NOT_CONFIRMED_OR_INSUFFICIENT_EVIDENCE'].includes(d.human_decision),
   'Case D human decision invalid');
 check(nonempty(d.reviewer_id)&&iso(d.signed_date),'Case D signer missing');
 check(d.personally_reviewed_original_scene===true,'Case D original image reviewer needed');
 pinnedRef(d.evidence_ref,d.evidence_sha256);
 return d.human_decision==='CONFIRM_ZERO_VISIBLE_PERSONS';
}
function evaluate(quarantine,sourceOverlay,personOverlay,basePacket,media,freeze){
 check(quarantine.schema_version==='seer-ppe/clean17-valid-research-quarantine/v0.14','V14 technical ledger changed');
 check(quarantine.rows.length===459,'459 corrected Valid source IDs required');
 check(media.mode==='full'&&media.source_and_export_sha_verified===459 &&
  media.high_content_consistency===459 && media.test_images_decoded===0,'V13 actual-image proof incomplete');
 check(sourceOverlay.schema_version==='seer-ppe/source-family-human-attestation-overlay/v0.15'&&
  Array.isArray(sourceOverlay.decisions),'source overlay schema changed');
 check(personOverlay.schema_version==='seer-ppe/train-only-person-ppe-human-attestation/v0.15'&&
  Array.isArray(personOverlay.case_B_visual_decisions),'person overlay schema changed');
 check(basePacket.case_B_visual_state_pending.length===4 &&
  basePacket.prior_reference_human_links_preserved===19 &&
  basePacket.prior_recorded_visual_states===38 &&
  basePacket.prior_expected_visual_states===42 &&
  basePacket.case_D.zero_person_scene_human_signed===null,'historical Train-only reference changed');
 check(freeze.model_id==='altayyar-0oflt-lafos-qqauz/2'&&freeze.test_authorized===false,
  'original model or Test freeze policy changed');
 const src=new Map(quarantine.rows.map(x=>[x.original_valid_source_id,x]));
 const direct=new Map(media.results.map(x=>[x.source_id,x]));
 check(src.size===459&&direct.size===459,'duplicate original or exported image identity in frozen metadata');
 const assigned=new Map();
 for(const d of sourceOverlay.decisions){
  check(src.has(d.source_id)&&!assigned.has(d.source_id),'unknown/duplicate signed Source ID');
  assigned.set(d.source_id,d);
 }
 let signed=0,independentAttestations=0,held=0,technical=0,review=0,unflagged=0;
 const eligibleCandidates=[],list=[];
 for(const [id,s] of [...src].sort(([a],[b])=>a.localeCompare(b))){
  const evidence=direct.get(id);
  check(evidence?.export_filename===s.clean17_valid_filename &&
    evidence.original_sha_verified===true && evidence.export_sha_verified===true &&
    evidence.technical_content_consistency==='HIGH_AUTOMATED_EVIDENCE_NOT_FINAL_PHOTO_IDENTITY',
    'original to clean export photo identity evidence mismatch');
  const d=assigned.get(id);
  let verdict=null,decisionStatus='UNSIGNED_SOURCE_FAMILY',signedEvidenceRef=null,groupId=null;
  if(s.eligibility_disposition==='RETAIN_PREEXISTING_RESEARCH_HOLD')held++;
  else if(s.eligibility_disposition==='TECHNICAL_OVERLAP_QUARANTINE_PENDING_REVIEW')technical++;
  else if(s.eligibility_disposition==='SOURCE_FAMILY_REVIEW_PENDING')review++;
  else if(s.eligibility_disposition==='NO_SCREEN_FLAG_INDEPENDENCE_UNCERTIFIED')unflagged++;
  else fail('unknown V14 research risk status');
  if(d){
   const r=validateSourceDecision(d,s);
   signed++;
   if(r.independent)independentAttestations++;
   verdict=d.verdict;signedEvidenceRef=d.evidence_ref;
   groupId=d.acquisition_family_id??null;
   decisionStatus=r.independent?'HUMAN_ATTESTED_INDEPENDENT_SOURCE_NOT_FROZEN':'SIGNED_NONINDEPENDENT_OR_UNRESOLVED';
  }
  const conflict=s.previous_research_hold ||
   s.eligibility_disposition==='TECHNICAL_OVERLAP_QUARANTINE_PENDING_REVIEW';
  if(conflict)decisionStatus=s.previous_research_hold?
   'HARD_HOLD_STILL_BLOCKED':'HIGH_OVERLAP_CONFLICT_STILL_BLOCKED';
  else if(verdict==='INDEPENDENT_SOURCE_SUPPORTED'){
   eligibleCandidates.push({source_id:id,acquisition_family_id:groupId,
      source_evidence_ref:signedEvidenceRef,clean17_export_filename:s.clean17_valid_filename});
  }
  list.push({source_id:id,source_filename:s.original_valid_filename,
    clean17_valid_export_filename:s.clean17_valid_filename,
    technical_correspondence_sha_verified:true,
    V14_risk_bucket:s.eligibility_disposition,
    reviewed_train_candidates:s.direct_source_train_candidate_pairs_examined,
    strong_train_same_frame_candidates:s.strong_source_train_candidate_pairs,
    signed_source_family_verdict:verdict,
    human_evidence_ref:signedEvidenceRef,
    source_family_id:groupId,
    decision_status:decisionStatus,
    eligible_for_scientific_scoring:false,
    source_reviewer_signoff_missing:d==null});
 }
 check(held===5&&technical===6&&review===81&&unflagged===367,'V14 category distribution changed');
 const pendingB=new Map(basePacket.case_B_visual_state_pending.map(x=>[x.slot_id,x]));
 const signedB=new Set();
 for(const d of personOverlay.case_B_visual_decisions){
  check(pendingB.has(d.slot_id)&&!signedB.has(d.slot_id),'B visual state unknown or repeated');
  validateBDecision(d,pendingB.get(d.slot_id));signedB.add(d.slot_id);
 }
 const dConfirmed=validateDDecision(personOverlay.case_D_zero_person_decision);
 const allTrainReferencesSigned=signedB.size===4&&dConfirmed;
 check(eligibleCandidates.every(x=>!list.find(r=>r.source_id===x.source_id)?.eligible_for_scientific_scoring),
  'source attestation alone must never authorize scoring');
 const freezeAuthorized=freeze.state==='FROZEN' && freeze.authorized===true;
 const freezeReady=freezeAuthorized && eligibleCandidates.length>0 &&
  Object.values(freeze.gates??{}).every(x=>x===true);
 // Even with Train-only A/B/C/D reference complete, a separately signed Valid-person
 // reference is indispensable; do not equate the two.
 const validationReferenceComplete=false;
 const scoringReady=freezeReady && validationReferenceComplete;
 return {schema_version:'seer-ppe/validation-evidence-qualification-audit/v0.15',
  date:'2026-11-21',original_valid_count:468,
  clean17_valid_count:459,previously_excluded_original_valid:9,
  direct_source_to_clean17_content_correspondence:459,
  source_eligibility_buckets:{historical_holds:held,technical_overlap_quarantine:technical,
    other_source_family_review:review,unflagged_but_unsigned:unflagged},
  per_image_source_family_human_decisions_signed:signed,
  human_independence_attestations:independentAttestations,
  individually_attested_nonconflicting_sources_pending_protocol:eligibleCandidates.length,
  candidate_ids_from_signed_independence:eligibleCandidates,
  train_reference:{previous_approved_person_item_links:19,previous_visual_states:38,
    previously_expected_visual_states:42,case_B_new_individually_signed:signedB.size,
    case_B_missing_visual_cells:4-signedB.size,
    case_D_human_confirmed_zero_person:dConfirmed,
    case_D_human_decision_signed:personOverlay.case_D_zero_person_decision!=null,
    train_only_all_requested_decisions_signed:allTrainReferencesSigned},
  current_validation_person_reference_signed:false,
  protocol_frozen:freezeAuthorized,
  source_family_independence_as_verified_scientific_cohort:false,
  scoring_ready:scoringReady,
  test_images_accessed:false,roboflow_data_or_model_modified:false,
  source_registry_file:'SOURCE_FAMILY_SIGNED_ATTESTATIONS_V15.json',
  human_registry_file:'TRAIN_REFERENCE_SIGNED_ATTESTATIONS_V15.json',
  image_rows:list};
}
function selfTest(){
 const q=read('VALIDATION_TECHNICAL_QUARANTINE_V14.json');
 const m=read('ORIGINAL_CLEAN17_VALID_IMAGE_CONTENT_V13.json');
 const f=read('VALIDATION_PERSON_PPE_SCORING_FREEZE_2026-11-21_V11.json');
 const packet=read('PERSON_PPE_PENDING_HUMAN_SIGNOFF_2026-11-21_V13.json');
 const currentSource=read('SOURCE_FAMILY_SIGNED_ATTESTATIONS_V15.json');
 const baselineSource=structuredClone(currentSource);baselineSource.decisions=[];
 const emptyHuman=read('TRAIN_REFERENCE_SIGNED_ATTESTATIONS_V15.json');
 const current=evaluate(q,baselineSource,emptyHuman,packet,m,f);
 assert.equal(current.scoring_ready,false);
 assert.equal(current.image_rows.length,459);
 assert.equal(current.per_image_source_family_human_decisions_signed,0);
 assert.equal(current.train_reference.case_B_missing_visual_cells,4);
 assert.equal(current.train_reference.case_D_human_confirmed_zero_person,false);
 const sample=q.rows.find(x=>x.eligibility_disposition==='NO_SCREEN_FLAG_INDEPENDENCE_UNCERTIFIED');
 const evidence='SOURCE_FAMILY_AND_VALIDATION_QUARANTINE_PROTOCOL_2026-11-21_V14.md';
 const hash=SHA(readFileSync(resolve(ROOT,evidence)));
 const good={source_id:sample.original_valid_source_id,
    source_original_filename:sample.original_valid_filename,clean17_export_filename:sample.clean17_valid_filename,
    verdict:'INDEPENDENT_SOURCE_SUPPORTED',reviewer_id:'synthetic-reviewer-not-a-real-signoff',
    signed_date:'2026-11-21',per_source_reviewer_inspected_evidence:true,
    evidence_basis:'SYNTHETIC ONLY: independent field log supports source selection',
    evidence_ref:evidence,evidence_sha256:hash,
    acquisition_site_id:'synthetic_site_A',capture_session_id:'synthetic_session_A',
    acquisition_family_id:'synthetic_family_A',
    train_family_crosscheck_completed:true,no_train_capture_or_site_family_overlap_supported:true,
    train_family_comparison_basis:'SYNTHETIC ONLY: matched site list checked',
    train_family_evidence_ref:evidence,train_family_evidence_sha256:hash,
    personally_attested_independence:true};
 const variant=structuredClone(baselineSource);variant.decisions=[good];
 const future=evaluate(q,variant,emptyHuman,packet,m,f);
 assert.equal(future.individually_attested_nonconflicting_sources_pending_protocol,1);
 assert.equal(future.scoring_ready,false);
 const bad={...good,source_id:q.rows.find(x=>x.previous_research_hold).original_valid_source_id};
 const reject=structuredClone(baselineSource);reject.decisions=[bad];
 assert.throws(()=>evaluate(q,reject,emptyHuman,packet,m,f));
 const conflict=q.rows.find(x=>x.eligibility_disposition==='TECHNICAL_OVERLAP_QUARANTINE_PENDING_REVIEW');
 const quarantined=structuredClone(baselineSource);quarantined.decisions=[
   {...good,source_id:conflict.original_valid_source_id,source_original_filename:conflict.original_valid_filename,
    clean17_export_filename:conflict.clean17_valid_filename}];
 const stillBlocked=evaluate(q,quarantined,emptyHuman,packet,m,f);
 assert.equal(stillBlocked.individually_attested_nonconflicting_sources_pending_protocol,0);
 const mutated=structuredClone(variant);mutated.decisions[0].evidence_sha256='0'.repeat(64);
 assert.throws(()=>evaluate(q,mutated,emptyHuman,packet,m,f));
 const invalidCalendarDate=structuredClone(variant);
 invalidCalendarDate.decisions[0].signed_date='2026-02-30';
 assert.throws(()=>evaluate(q,invalidCalendarDate,emptyHuman,packet,m,f));
 const guessed=structuredClone(emptyHuman);guessed.case_B_visual_decisions=[
   {slot_id:'B_P001_face_mask',human_visual_state:'ABSENT',reviewer_id:'guess',signed_date:'2026-11-21'}];
 assert.throws(()=>evaluate(q,baselineSource,guessed,packet,m,f));
 const injected=structuredClone(baselineSource);injected.decisions=[{...good,source_id:'TEST_IMAGE_SOURCE_ID'}];
 assert.throws(()=>evaluate(q,injected,emptyHuman,packet,m,f));
 const broken=structuredClone(q);broken.rows[0].clean17_valid_filename='unexpected.jpg';
 assert.throws(()=>evaluate(broken,baselineSource,emptyHuman,packet,m,f));
 console.log('SEER_V15_SYNTHETIC_SIGNED_EVIDENCE_SHA_AND_HARD_HOLD_REJECTION_PASS');
 console.log('SEER_V15_SYNTHETIC_FALSE_PERSON_LABEL_AND_TEST_SOURCE_REJECTION_PASS');
}
try{
 const mode=process.argv[2]??'--audit';
 if(mode==='--self-test')selfTest();
 else if(mode==='--audit'||mode==='--gate'){
  const out=evaluate(
    read('VALIDATION_TECHNICAL_QUARANTINE_V14.json'),
    read('SOURCE_FAMILY_SIGNED_ATTESTATIONS_V15.json'),
    read('TRAIN_REFERENCE_SIGNED_ATTESTATIONS_V15.json'),
    read('PERSON_PPE_PENDING_HUMAN_SIGNOFF_2026-11-21_V13.json'),
    read('ORIGINAL_CLEAN17_VALID_IMAGE_CONTENT_V13.json'),
    read('VALIDATION_PERSON_PPE_SCORING_FREEZE_2026-11-21_V11.json'));
  const outputPath=process.argv[3];
  if(outputPath&&mode==='--audit')writeFileSync(outputPath,JSON.stringify(out,null,2)+'\n');
  console.log(JSON.stringify({...out,image_rows:undefined,candidate_ids_from_signed_independence:undefined},null,2));
  if(mode==='--gate')check(out.scoring_ready,'V15_FREEZE_GATED_NO_SCIENTIFIC_SCORE');
  console.log('SEER_V15_459_DIRECT_MEDIA_SOURCE_ATTESTATION_AND_PPE_READINESS_FAIL_CLOSED_PASS');
 }else fail('Usage: --self-test | --audit [output-path] | --gate');
}catch(e){console.error(String(e));process.exitCode=2;}
