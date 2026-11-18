/* SEER-PPE read-only reference structural QA, NOT model performance scoring.
 * Input: {"cases":[{"case_id":"A","revision":2,"split":"train","ground_truth_state":"incomplete","ground_truth":{...}}]}
 * Usage: node research/seer-ppe/tools/validate_reference.mjs --self-test
 *        node research/seer-ppe/tools/validate_reference.mjs exported_cases.json
 */
const types=["hard_hat","safety_vest","goggles","face_mask","glove","safety_boot"];
function validateCase(x){
 const g=x.ground_truth||x.groundTruth||{},errors=[],warnings=[];
 const a=Array.isArray(g.persons)?g.persons:[],b=Array.isArray(g.ppe_items)?g.ppe_items:[],s=Array.isArray(g.worker_ppe_states)?g.worker_ppe_states:[],l=Array.isArray(g.associations)?g.associations:[],m=Array.isArray(g.task_mandates)?g.task_mandates:[];
 const personIDs=new Set(),ppeIDs=new Set(),stateKeys=new Set(),linkIDs=new Set(),policyKeys=new Set();
 const bboxOK=z=>Array.isArray(z)&&z.length===4&&z.every(v=>Number.isFinite(v)&&v>=0&&v<=1)&&z[0]<z[2]&&z[1]<z[3];
 for(const p of a){if(!p.id||personIDs.has(p.id))errors.push("DUPLICATE_OR_EMPTY_PERSON:"+p.id);personIDs.add(p.id);if(!bboxOK(p.bbox_xyxy_norm))errors.push("BAD_PERSON_BOX:"+p.id);}
 for(const p of b){if(!p.id||ppeIDs.has(p.id))errors.push("DUPLICATE_OR_EMPTY_PPE:"+p.id);ppeIDs.add(p.id);if(!types.includes(p.ppe_type))errors.push("BAD_PPE_TYPE:"+p.id);if(!bboxOK(p.bbox_xyxy_norm))errors.push("BAD_PPE_BOX:"+p.id);}
 const visual={PRESENT:0,ABSENT:0,UNKNOWN:0};
 for(const x of s){const k=x.person_id+":"+x.ppe_type;if(stateKeys.has(k))errors.push("DUPLICATE_STATE:"+k);stateKeys.add(k);if(!personIDs.has(x.person_id))errors.push("STATE_ORPHAN:"+k);if(!types.includes(x.ppe_type)||!Object.hasOwn(visual,x.visual_state))errors.push("BAD_STATE:"+k);else visual[x.visual_state]++;}
 for(const x of l){if(linkIDs.has(x.equipment_id))errors.push("DUPLICATE_PPE_LINK:"+x.equipment_id);linkIDs.add(x.equipment_id);if(!ppeIDs.has(x.equipment_id))errors.push("LINK_ORPHAN_EQUIPMENT:"+x.equipment_id);if(x.status==="MATCHED"&&!personIDs.has(x.person_id))errors.push("LINK_ORPHAN_PERSON:"+x.equipment_id);if(x.status==="MATCHED"&&Array.isArray(x.candidate_person_ids)&&!x.candidate_person_ids.includes(x.person_id))errors.push("LINK_PERSON_NOT_CANDIDATE:"+x.equipment_id);}
 for(const x of m){const k=x.person_id+":"+x.ppe_type;if(policyKeys.has(k))errors.push("DUPLICATE_POLICY:"+k);policyKeys.add(k);if(!personIDs.has(x.person_id))errors.push("POLICY_ORPHAN:"+k);if(!types.includes(x.ppe_type)||!["REQUIRED","NOT_REQUIRED","POLICY_UNKNOWN"].includes(x.mandate_status))errors.push("INVALID_POLICY:"+k);}
 const missingVisual=[],missingPolicy=[];
 for(const p of a)for(const t of types){if(!stateKeys.has(p.id+":"+t))missingVisual.push(p.id+":"+t);if(!policyKeys.has(p.id+":"+t))missingPolicy.push(p.id+":"+t);}
 const split=x.split||"UNKNOWN",status=x.ground_truth_state||x.groundTruthState||"missing",source=Object.hasOwn(g,"source_review");
 if(missingVisual.length)warnings.push("UNFILLED_VISUAL_CELLS:"+missingVisual.length);
 if(missingPolicy.length)warnings.push("UNFILLED_POLICY_CELLS:"+missingPolicy.length);
 if(!source)warnings.push("SOURCE_REVIEW_UNFILLED");
 if(status!=="complete")warnings.push("REFERENCE_INCOMPLETE");
 if(!["valid","test"].includes(split))warnings.push("NOT_HELD_OUT:"+split);
 if(!a.length)warnings.push("NO_PERSON_ROWS_VERIFY_CONTROL_EXTERNALLY");
 return {case_id:x.case_id,revision:x.revision,split,ground_truth_state:status,persons:a.length,positive_items:b.length,matched_links:l.filter(x=>x.status==="MATCHED").length,visual_cells:s.length,visual_counts:visual,policy_unknown:m.filter(x=>x.mandate_status==="POLICY_UNKNOWN").length,missing_visual:missingVisual,missing_policy:missingPolicy,source_review_present:source,errors,warnings,can_claim_test_accuracy:status==="complete"&&split==="test"&&source&&errors.length===0&&missingVisual.length===0,can_claim_PPE_compliance:false};
}
function summarize(list){
 const sum=k=>list.reduce((n,x)=>n+x[k],0);
 return {cases:list.length,persons:sum("persons"),positive_items:sum("positive_items"),matched_links:sum("matched_links"),visual_cells:sum("visual_cells"),unknown_cells:list.reduce((n,x)=>n+x.visual_counts.UNKNOWN,0),absent_cells:list.reduce((n,x)=>n+x.visual_counts.ABSENT,0),missing_visual_cells:list.reduce((n,x)=>n+x.missing_visual.length,0),policy_unknown_cells:sum("policy_unknown"),structurally_invalid_cases:list.filter(x=>x.errors.length).length,complete_cases:list.filter(x=>x.ground_truth_state==="complete").length,held_out_test_cases:list.filter(x=>x.split==="test").length,scorable_test_cases:list.filter(x=>x.can_claim_test_accuracy).length};
}
export {validateCase,summarize};

import {readFileSync} from "node:fs";
import {pathToFileURL} from "node:url";
if(process.argv[1] && import.meta.url===pathToFileURL(process.argv[1]).href){
 const arg=process.argv[2];
 if(arg==="--self-test"){
  const t={case_id:"T",revision:1,split:"test",ground_truth_state:"complete",ground_truth:{persons:[{id:"P1",bbox_xyxy_norm:[0.1,0.1,0.9,0.9]}],ppe_items:[{id:"E1",ppe_type:"hard_hat",bbox_xyxy_norm:[0.2,0.2,0.4,0.4]}],worker_ppe_states:types.map(k=>({person_id:"P1",ppe_type:k,visual_state:"UNKNOWN"})),task_mandates:types.map(k=>({person_id:"P1",ppe_type:k,mandate_status:"POLICY_UNKNOWN"})),associations:[{equipment_id:"E1",person_id:"P1",status:"MATCHED",candidate_person_ids:["P1"]}],source_review:{status:"REVIEWED",context_status:"POLICY_UNKNOWN"}}};
  if(validateCase(t).errors.length)throw Error("positive test failed");
  const broken=JSON.parse(JSON.stringify(t));broken.ground_truth.associations[0].person_id="MISSING";
  if(!validateCase(broken).errors.includes("LINK_ORPHAN_PERSON:E1"))throw Error("orphan link test failed");
  process.stdout.write("SELF_TESTS_PASSED\\n");
 }else if(arg){const obj=JSON.parse(readFileSync(arg,"utf8"));if(!Array.isArray(obj.cases))throw Error("Expected {cases: [...]}");const records=obj.cases.map(validateCase);process.stdout.write(JSON.stringify({summary:summarize(records),cases:records},null,2)+"\\n");}
 else{process.stderr.write("Usage: node validate_reference.mjs --self-test | cases.json\\n");process.exitCode=2;}
}
