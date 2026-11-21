#!/usr/bin/env node
/** V15 validation human reference: no model labels may impersonate researcher GT.
 * This is a read-only SCHEMA / completeness gate, NOT a claim of signed gold. */
import assert from 'node:assert/strict';
import {readFileSync,existsSync,realpathSync} from 'node:fs';
import {resolve,relative,sep} from 'node:path';
import {createHash} from 'node:crypto';
import {fileURLToPath} from 'node:url';
const ROOT=resolve(fileURLToPath(new URL('..',import.meta.url)));
const read=n=>JSON.parse(readFileSync(resolve(ROOT,n),'utf8'));
const TYPES=['hard_hat','safety_vest','goggles','face_mask','glove','safety_boot'];
const STATES=['PRESENT','ABSENT','UNKNOWN'];
const POLICY=['REQUIRED','NOT_REQUIRED','POLICY_UNKNOWN'];
const REASONS=['FULLY_VISIBLE','PARTIALLY_OCCLUDED','TRUNCATED','LOW_RESOLUTION','NOT_DETERMINABLE'];
const check=(b,msg)=>{if(!b)throw Error('V15_GOLD_BLOCKED:'+msg);};
const nonempty=x=>typeof x==='string'&&x.trim().length>=3;
const iso=s=>typeof s==='string'&&/^\d{4}-\d\d-\d\d$/.test(s)&&!Number.isNaN(Date.parse(s+'T00:00:00Z'))&&new Date(s+'T00:00:00Z').toISOString().slice(0,10)===s;
function evidence(path,sha){
 check(typeof path==='string'&&/^[a-zA-Z0-9][a-zA-Z0-9_./-]*\.(md|json|csv)$/.test(path) &&
 !path.includes('..')&&!path.startsWith('/'),'untrusted evidence filename');
 const f=resolve(ROOT,path),rel=relative(ROOT,f);
 check(rel&&!rel.startsWith('..'+sep)&&rel!=='..'&&existsSync(f),'evidence outside repository');
 const real=realpathSync(f),relreal=relative(ROOT,real);
 check(relreal&&!relreal.startsWith('..'+sep)&&relreal!=='..','symlink evidence path escaped repository');
 check(typeof sha==='string'&&/^[0-9a-f]{64}$/.test(sha) &&
 createHash('sha256').update(readFileSync(real)).digest('hex')===sha,'unpinned/replaced evidence');
}
function bbox(b){
 check(Array.isArray(b)&&b.length===4&&b.every(x=>Number.isFinite(x)&&x>=0&&x<=1)&&
  b[0]<b[2]&&b[1]<b[3],'invalid normalized bbox');
}
function coverage(obj,keys,allowed,kind){
 check(obj&&typeof obj==='object'&&!Array.isArray(obj),'missing '+kind);
 check(Object.keys(obj).length===keys.length,'missing/extra '+kind+' keys');
 for(const k of keys)check(allowed.includes(obj[k]),'invalid '+kind+' '+k);
}
function validateCase(c,q,direct){
 check(c&&c.original_split==='valid','Test/Train not allowed in Validation gold');
 const src=q.get(c.source_id),image=direct.get(c.source_id);
 check(src && image,'not one of frozen 459 original Valid Source IDs');
 check(c.clean17_filename===src.clean17_valid_filename &&
 c.clean17_filename===image.export_filename,'source-to-Clean17 image mapping mismatch');
 check(image.original_sha_verified===true&&image.export_sha_verified===true&&
 image.technical_content_consistency==='HIGH_AUTOMATED_EVIDENCE_NOT_FINAL_PHOTO_IDENTITY',
 'source Clean17 byte-hash/visual provenance missing');
 check(c.human_signed===true && nonempty(c.reviewer_id)&&iso(c.signed_date),
 'real person/reviewer dated reference signoff required');
 check(c.reviewed_original_validation_image===true,'reference must be human-reviewed on original Valid image');
 check(nonempty(c.image_observation_basis),'individual human observation absent');
 evidence(c.evidence_ref,c.evidence_sha256);
 check(Number.isInteger(c.person_count_human)&&c.person_count_human>=0&&c.person_count_human<=100,
 'signed person count missing');
 check(Array.isArray(c.people)&&c.people.length===c.person_count_human,'human person count inconsistent');
 check(Array.isArray(c.items)&&c.items.length<=500,'item audit missing or implausible');
 check(c.person_coverage_human_complete===true && c.item_coverage_human_complete===true,
 'unreviewed people/items may not be treated as zero');
 check(c.zero_person_scene_human_signed===(c.person_count_human===0),
 'zero-person scene must be explicitly signed, never inferred from detector misses');
 const persons=new Set();
 const ppe=new Map();
 for(const p of c.people){
  check(/^P\d{3}$/.test(p.person_id)&&!persons.has(p.person_id),'bad/duplicate human person ID');
  persons.add(p.person_id);bbox(p.bbox_xyxy_norm);
  check(REASONS.includes(p.visibility_evidence),'missing person visibility information');
  coverage(p.visual_states,TYPES,STATES,'human visual states');
  coverage(p.task_mandates,TYPES,POLICY,'human task mandates');
  // Every known task REQUIREMENT is supported by policy evidence, separate from visual fact.
  if(Object.values(p.task_mandates).some(x=>x!=='POLICY_UNKNOWN')){
   check(nonempty(p.policy_basis),'PPE policy applicability rationale missing');
   evidence(p.policy_evidence_ref,p.policy_evidence_sha256);
  }
  ppe.set(p.person_id,p.visual_states);
 }
 const itemIds=new Set();
 for(const it of c.items){
  check(/^E\d{3}$/.test(it.item_id)&&!itemIds.has(it.item_id),'bad/duplicate item ID');
  itemIds.add(it.item_id);bbox(it.bbox_xyxy_norm);
  check(TYPES.includes(it.ppe_type),'PPE item type not one of six registered tasks');
  check(it.human_item_reviewed===true,'item cannot be model-only guessed label');
  check(['MATCHED','UNKNOWN'].includes(it.owner_decision),'invalid owner decision');
  if(it.owner_decision==='MATCHED'){
   check(persons.has(it.person_id),'linked equipment belongs to unknown worker');
   check(ppe.get(it.person_id)[it.ppe_type]==='PRESENT',
     'positive person-linked PPE item contradicts reviewed visual ABSENT/UNKNOWN');
  }else check(it.person_id===null,'UNKNOWN owner must not have person_id');
 }
 if(c.person_count_human===0)check(c.items.length===0,
   'zero-person reference contains putative worn PPE associations');
 return {source_id:c.source_id,people:c.person_count_human,items:c.items.length,
  policy_known_people:c.people.filter(p=>Object.values(p.task_mandates).some(v=>v!=='POLICY_UNKNOWN')).length};
}
function validate(overlay,qua,proof){
 check(overlay.schema_version==='seer-ppe/validation-person-ppe-signed-human-reference/v0.15' &&
  overlay.test_authorized===false && Array.isArray(overlay.cases),'incorrect reference overlay');
 check(qua.rows.length===459 && proof.results.length===459,'source coverage changed');
 const src=new Map(qua.rows.map(r=>[r.original_valid_source_id,r]));
 const dir=new Map(proof.results.map(r=>[r.source_id,r]));
 check(src.size===dir.size&&src.size===459,'duplicate source identities in frozen proof');
 const seen=new Set(),rows=[];
 for(const c of overlay.cases){
  check(!seen.has(c.source_id),'two signed Validation human records on one Source ID');
  seen.add(c.source_id);
  rows.push(validateCase(c,src,dir));
 }
 return {schema_version:'seer-ppe/validation-person-gold-readiness/v0.15',date:'2026-11-21',
  available_clean17_valid_original_sources:459,actual_human_signed_original_valid_images:rows.length,
  valid_person_and_ppe_complete_human_records:rows.length,
  total_human_signed_people:rows.reduce((a,x)=>a+x.people,0),
  signed_original_valid_source_ids:rows.map(x=>x.source_id),
  researcher_source_family_signoff_independent_from_human_reference:true,
  all_459_validation_images_have_human_reference:rows.length===459,
  authorized_scientific_scoring:false,zero_test_images_read:true,model_inference_performed:false,
  actual_model_metric_computed:false,scoring_ready:false};
}
function test(){
 const empty=read('VALIDATION_PERSON_PPE_SIGNED_REFERENCE_V15.json');
 const qua=read('VALIDATION_TECHNICAL_QUARANTINE_V14.json');
 const proof=read('ORIGINAL_CLEAN17_VALID_IMAGE_CONTENT_V13.json');
 const now=validate(empty,qua,proof);
 assert.equal(now.actual_human_signed_original_valid_images,0);
 const r=qua.rows.find(x=>x.eligibility_disposition==='NO_SCREEN_FLAG_INDEPENDENCE_UNCERTIFIED');
 const path='SOURCE_AND_PERSON_SIGNOFF_PROCEDURE_2026-11-21_V15.md';
 const sha=createHash('sha256').update(readFileSync(resolve(ROOT,path))).digest('hex');
 const human={source_id:r.original_valid_source_id,clean17_filename:r.clean17_valid_filename,
  original_split:'valid',human_signed:true,reviewer_id:'synthetic-only',
  signed_date:'2026-11-21',reviewed_original_validation_image:true,
  image_observation_basis:'SYNTHETIC TEST CASE, never signed by the user',
  evidence_ref:path,evidence_sha256:sha,
  person_count_human:1,person_coverage_human_complete:true,item_coverage_human_complete:true,
  zero_person_scene_human_signed:false,
  people:[{person_id:'P001',bbox_xyxy_norm:[0.1,0.1,0.9,0.9],visibility_evidence:'FULLY_VISIBLE',
    visual_states:Object.fromEntries(TYPES.map(k=>[k,k==='hard_hat'?'PRESENT':'UNKNOWN'])),
    task_mandates:Object.fromEntries(TYPES.map(k=>[k,'POLICY_UNKNOWN']))}],
  items:[{item_id:'E001',ppe_type:'hard_hat',bbox_xyxy_norm:[0.15,0.12,0.4,0.3],
    human_item_reviewed:true,owner_decision:'MATCHED',person_id:'P001'}]};
 const signed=structuredClone(empty);signed.cases=[human];
 assert.equal(validate(signed,qua,proof).actual_human_signed_original_valid_images,1);
 assert.equal(validate(signed,qua,proof).scoring_ready,false);
 const invalid=structuredClone(signed);invalid.cases[0].people[0].visual_states.hard_hat='ABSENT';
 assert.throws(()=>validate(invalid,qua,proof),'false human PPE item-person association passed');
 const missing=structuredClone(signed);delete missing.cases[0].people[0].visual_states.goggles;
 assert.throws(()=>validate(missing,qua,proof),'missing visual state passed');
 const wrong=structuredClone(signed);wrong.cases[0].original_split='test';
 assert.throws(()=>validate(wrong,qua,proof),'protected Test human label passed as Valid');
 const unseen=structuredClone(signed);unseen.cases[0].person_count_human=0;
 assert.throws(()=>validate(unseen,qua,proof),'detector zero person treated as signed reference');
 const noPpe=structuredClone(signed);noPpe.cases[0].items[0].owner_decision='UNKNOWN';
 assert.throws(()=>validate(noPpe,qua,proof),'UNKNOWN item owner with inferred worker passed');
 console.log('SEER_V15_VALIDATION_GOLD_SYNTHETIC_HUMAN_REFERENCE_AND_ABSTENTION_PASS');
 console.log('SEER_V15_VALIDATION_GOLD_SYNTHETIC_TEST_INJECTION_MISSING_PERSON_AND_PPE_REJECTED_PASS');
}
try{
 const mode=process.argv[2]??'--audit';
 if(mode==='--self-test')test();
 else if(mode==='--audit'){
  const r=validate(read('VALIDATION_PERSON_PPE_SIGNED_REFERENCE_V15.json'),
    read('VALIDATION_TECHNICAL_QUARANTINE_V14.json'),read('ORIGINAL_CLEAN17_VALID_IMAGE_CONTENT_V13.json'));
  console.log(JSON.stringify(r,null,2));
  console.log('SEER_V15_NO_HUMAN_SIGNED_VALID_REFERENCE_YET_FAIL_CLOSED_PASS');
 }else throw Error('Usage: --self-test | --audit');
}catch(e){console.error(String(e));process.exitCode=2;}
