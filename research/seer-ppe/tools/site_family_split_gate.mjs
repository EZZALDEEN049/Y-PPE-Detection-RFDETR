#!/usr/bin/env node
/**
 * SEER-PPE: conservative site-family split gate (read-only, no inference).
 * Consumes manually inspected site-name evidence. Never groups by generic
 * filename stem or semantic image similarity alone. Rows with unknown site
 * remain unassessed; absence of a collision is NOT a readiness pass.
 *
 * Usage:
 *   node research/seer-ppe/tools/site_family_split_gate.mjs --self-test
 *   node research/seer-ppe/tools/site_family_split_gate.mjs
 *   node research/seer-ppe/tools/site_family_split_gate.mjs path/to/evidence.json
 */
import { readFileSync } from "node:fs";
import assert from "node:assert/strict";

export function analyze(rows){
  if(!Array.isArray(rows))throw new TypeError("Expected images_reviewed array.");
  const bySite=new Map();
  for(const row of rows){
    if(!row || typeof row.image_id!=="string" || typeof row.split!=="string")continue;
    if(typeof row.site_id!=="string" || row.site_evidence!=="VISIBLE_IMAGE_TEXT_SCHOOL_NAME" || !String(row.site_review).startsWith("CONFIRMED_"))continue;
    if(!bySite.has(row.site_id))bySite.set(row.site_id,[]);
    bySite.get(row.site_id).push(row);
  }
  const groups=[];
  for(const [site_id,records] of [...bySite.entries()].sort((a,b)=>a[0].localeCompare(b[0]))){
    const splits={train:0,valid:0,test:0};
    for(const row of records) splits[row.split]=(splits[row.split]||0)+1;
    const observed_splits=Object.keys(splits).filter(x=>splits[x]>0);
    groups.push({
      site_id,reviewed_images:records.length,split_counts:splits,
      cross_split:observed_splits.length>1,
      site_independent_valid_hold_image_ids:observed_splits.length>1?records.filter(r=>r.split==="valid").map(r=>r.image_id).sort():[],
      member_image_ids:records.map(r=>r.image_id).sort()
    });
  }
  return {
    scope:"ONLY_EXPLICIT_VISUALLY_NAMED_SITE_GROUPS_FROM_REVIEWED_SAMPLE",
    all_images_screened:rows.length,
    grouped_images:groups.reduce((s,g)=>s+g.reviewed_images,0),
    cross_split_site_group_count:groups.filter(g=>g.cross_split).length,
    site_independent_valid_hold_image_ids:groups.flatMap(g=>g.site_independent_valid_hold_image_ids).sort(),
    site_groups:groups,
    does_not_prove_eligibility_of_unflagged_images:true
  };
}

if(process.argv[2]==="--self-test"){
  const result=analyze([
    {image_id:"a",split:"train",site_id:"S",site_evidence:"VISIBLE_IMAGE_TEXT_SCHOOL_NAME",site_review:"CONFIRMED_NAME_MATCH"},
    {image_id:"b",split:"valid",site_id:"S",site_evidence:"VISIBLE_IMAGE_TEXT_SCHOOL_NAME",site_review:"CONFIRMED_NAME_MATCH"},
    {image_id:"c",split:"valid",site_id:"T",site_evidence:"VISIBLE_IMAGE_TEXT_SCHOOL_NAME",site_review:"CONFIRMED_DIFFERENT_NAMED_SITE"},
    {image_id:"d",split:"test",site_id:null,site_evidence:"NONE",site_review:"SITE_UNKNOWN"}
  ]);
  assert.equal(result.cross_split_site_group_count,1);
  assert.deepEqual(result.site_independent_valid_hold_image_ids,["b"]);
  assert.equal(result.grouped_images,3);
  process.stdout.write("SITE_FAMILY_GATE_SYNTHETIC_PASS\n");
} else {
  const path=process.argv[2] || new URL("../VISUAL_SOURCE_FAMILY_ADJUDICATION_2026-11-18_V01.json",import.meta.url);
  const evidence=JSON.parse(readFileSync(path,"utf8"));
  const summary=analyze(evidence.images_reviewed);
  process.stdout.write(JSON.stringify(summary,null,2)+"\n");
}
