#!/usr/bin/env node
/** SEER-PPE read-only expanded source-family audit.
 * Usage: node research/seer-ppe/tools/expanded_source_family_gate.mjs --self-test
 *        node research/seer-ppe/tools/expanded_source_family_gate.mjs
 * Does NOT modify Roboflow or calculate model performance.
 */
import {readFileSync} from "node:fs";
import assert from "node:assert/strict";
export function audit(rows){
  if(!Array.isArray(rows))throw Error("Expected images array");
  const knownSplits=["train","valid","test"],ids=new Set(),duplicates=[],counts={train:0,valid:0,test:0},pending=[];
  const bySite=new Map();
  for(const r of rows){
    if(!r?.image_id||!r?.filename||!knownSplits.includes(r?.split))throw Error("Missing image id/filename or bad split");
    if(ids.has(r.image_id))duplicates.push(r.image_id);
    ids.add(r.image_id);counts[r.split]++;
    if(r.eligibility_status==="ELIGIBLE" && !r.site_id)throw Error("Unsafe eligibility with unknown site: "+r.filename);
    if(r.split==="valid" && r.eligible_for_site_independent_validation!==true)pending.push(r.filename);
    if(r.site_id && r.site_evidence==="PRIOR_VISIBLE_SITE_NAME"){
      if(!bySite.has(r.site_id))bySite.set(r.site_id,[]);
      bySite.get(r.site_id).push(r);
    }
  }
  const collisions=[...bySite.entries()].filter(([site,records])=>new Set(records.map(x=>x.split)).size>1)
      .map(([site_id,records])=>({site_id,split_counts:Object.fromEntries(knownSplits.map(s=>[s,records.filter(x=>x.split===s).length])),valid_ids:records.filter(x=>x.split==="valid").map(x=>x.image_id).sort()}));
  return {total:rows.length,counts,duplicate_image_ids:duplicates,cross_split_named_sites:collisions,valid_uncleared_count:pending.length,valid_uncleared_filenames:pending.sort(),all_valid_site_independence_verified:pending.length===0 && rows.some(x=>x.split==="valid"),absence_of_collision_proves_independence:false};
}
if(process.argv[2]==="--self-test"){
 const one=(image_id,split,site_id=null)=>({image_id,filename:image_id+".jpg",split,site_id,site_evidence:site_id?"PRIOR_VISIBLE_SITE_NAME":"NOT_ESTABLISHED",eligibility_status:"REVIEW",eligible_for_site_independent_validation:false});
 const x=audit([one("a","train","S"),one("b","valid","S"),one("c","valid"),one("d","test")]);
 assert.equal(x.total,4);assert.equal(x.valid_uncleared_count,2);assert.equal(x.cross_split_named_sites.length,1);assert.deepEqual(x.cross_split_named_sites[0].valid_ids,["b"]);assert.equal(x.absence_of_collision_proves_independence,false);console.log("EXPANDED_SOURCE_FAMILY_GATE_SELF_TEST_PASS");
}else{
 const f=process.argv[2] || new URL("../SOURCE_FAMILY_EXPANSION_2026-11-18_V02.json",import.meta.url);
 const v=JSON.parse(readFileSync(f,"utf8"));const summary=audit(v.images);
 if(summary.duplicate_image_ids.length)throw Error("Duplicate image IDs in register");
 console.log(JSON.stringify({scope:v.scope,family_split_counts:v.family_split_counts,...summary},null,2));
}
