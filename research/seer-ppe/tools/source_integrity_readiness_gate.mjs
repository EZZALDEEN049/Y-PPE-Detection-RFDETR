#!/usr/bin/env node
/** SEER-PPE source-integrity readiness gate; read-only, no detector inference.
 * Combines visually named-site overlap and highly suspicious same-source scene
 * pairs with filename-collision *review queues*. It never declares full readiness.
 * Usage:
 *   node research/seer-ppe/tools/source_integrity_readiness_gate.mjs --self-test
 *   node research/seer-ppe/tools/source_integrity_readiness_gate.mjs
 */
import {readFileSync} from "node:fs";
import assert from "node:assert/strict";
export function summarize(site,project){
 if(!Array.isArray(site?.images)||!Array.isArray(project?.groups))throw Error("Invalid source manifests");
 const byId=new Map(site.images.map(x=>[x.image_id,x]));
 if(byId.size!==site.images.length)throw Error("Duplicate candidate-family image ID");
 const siteIds=new Set();
 for(const fn of site.confirmed_cross_split_valid_hold_files||[]){
  const rec=site.images.find(x=>x.filename===fn&&x.split==="valid");
  if(!rec||!rec.site_id)throw Error("Site hold lacks confirmed Valid row: "+fn);
  siteIds.add(rec.image_id);
 }
 const visuallyShared=new Set(project.recommended_hold_valid_image_ids||[]);
 for(const id of visuallyShared){
  const verified=project.groups.some(g=>g.triage?.status==="HIGH_VISUAL_SHARED_SCENE_OR_DERIVATIVE_CANDIDATE"&&g.image_ids_by_split?.valid?.includes(id));
  if(!verified)throw Error("Visual hold unsupported by project collision register: "+id);
 }
 const candidateFlagIds=new Set();
 for(const g of project.groups)for(const id of g.image_ids_by_split?.valid||[])candidateFlagIds.add(id);
 const blocked=new Set([...siteIds,...visuallyShared]);
 const pendingNameOnly=[...candidateFlagIds].filter(id=>!blocked.has(id)).sort();
 const priorFamilyHold=site.images.filter(x=>x.split==="valid"&&x.eligibility_status==="HOLD_PREVIOUS_SOURCE_FAMILY_REVIEW").map(x=>x.image_id);
 const otherFamilyReview=site.images.filter(x=>x.split==="valid"&&x.eligibility_status.startsWith("REVIEW_")).map(x=>x.image_id);
 return {
  policy:"DENY_UNVERIFIED_SOURCE_INDEPENDENT_SCORING",
  verified_named_site_overlap_hold_valid_image_ids:[...siteIds].sort(),
  highly_suspicious_same_source_scene_hold_valid_image_ids:[...visuallyShared].sort(),
  combined_specific_source_hold_valid_image_ids:[...blocked].sort(),
  specific_source_hold_count:blocked.size,
  prior_source_family_hold_valid_image_ids:priorFamilyHold.sort(),
  unresolved_family_valid_image_ids:otherFamilyReview.sort(),
  unadjudicated_exact_filename_collision_valid_image_ids:pendingNameOnly,
  unadjudicated_exact_filename_collision_valid_count:pendingNameOnly.length,
  model_metric_scoring_ready:false,
  reason:"No independent complete source-family mapping or adjudicated human gold/held-out test; filename candidate review remains incomplete",
  no_test_image_inspection_or_inference_by_this_gate:true
 };
}
function read(file){return JSON.parse(readFileSync(file,"utf8"))}
if(process.argv[2]==="--self-test"){
 const site={images:[{image_id:"S",filename:"s.jpg",split:"valid",site_id:"A",eligibility_status:"HOLD_CONFIRMED_SITE_OVERLAP"},{image_id:"U",filename:"u.jpg",split:"valid",site_id:null,eligibility_status:"REVIEW_SOURCE_INDEPENDENCE_UNVERIFIED"}],confirmed_cross_split_valid_hold_files:["s.jpg"]};
 const project={groups:[{image_ids_by_split:{valid:["V","W"]},triage:{status:"HIGH_VISUAL_SHARED_SCENE_OR_DERIVATIVE_CANDIDATE"}}],recommended_hold_valid_image_ids:["V"]};
 const o=summarize(site,project);assert.equal(o.specific_source_hold_count,2);assert.deepEqual(o.combined_specific_source_hold_valid_image_ids,["S","V"]);assert.deepEqual(o.unadjudicated_exact_filename_collision_valid_image_ids,["W"]);assert.equal(o.model_metric_scoring_ready,false);console.log("SOURCE_INTEGRITY_READINESS_GATE_SELF_TEST_PASS");
}else{
 const base=new URL("../",import.meta.url);
 const site=read(new URL("SOURCE_FAMILY_EXPANSION_2026-11-18_V03.json",base));
 const project=read(new URL("PROJECT_WIDE_FILENAME_COLLISION_TRIAGE_2026-11-18_V01.json",base));
 const out=summarize(site,project);
 console.log(JSON.stringify(out,null,2));
}
