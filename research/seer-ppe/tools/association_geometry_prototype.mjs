/* SEER-PPE geometry-only item/person review. Outputs candidates, NEVER wearer ground truth.
   Supports multiple gloves/items per person, but at most one candidate person per item.
   Uses original bbox only; no pixel semantics, safety certification or site policy.
   Usage: node association_geometry_prototype.mjs --self-test
          node association_geometry_prototype.mjs annotated_images.json
   Input: {images:[{image_id,filename,split,boxes:[{id,label,x,y,width,height,confidence?}]}]}
*/
const TYPES={"Hard Hat":"hard_hat","Safety Vests":"safety_vest","Gloves":"glove","Safety Boots":"safety_boot","Goggles":"goggles","Face Masks":"face_mask"};
const ZONES={"hard_hat":[0,0.36],"safety_vest":[0.15,0.84],"glove":[0.17,0.94],"safety_boot":[0.67,1.15],"goggles":[0.02,0.35],"face_mask":[0.06,0.46]};
const SETTINGS={"minScore":0.57,"minMargin":0.12,"minConfidence":0.3};
function geomBox(b){const x=Number(b.x),y=Number(b.y),w=Number(b.width),h=Number(b.height);if(![x,y,w,h].every(Number.isFinite)||w<=0||h<=0)throw Error("Bad native bbox "+b.id);return {id:b.id,label:b.label,x,y,w,h,x1:x-w/2,x2:x+w/2,y1:y-h/2,y2:y+h/2};}
function rankPair(e,p,type){
 const centerInside=e.x>=p.x1&&e.x<=p.x2&&e.y>=p.y1&&e.y<=p.y2;
 const dx=Math.abs(e.x-p.x)/(p.w/2);
 const ny=(e.y-p.y1)/p.h;
 const [lo,hi]=ZONES[type];const vdist=Math.max(lo-ny,ny-hi,0);
 const hscore=Math.max(0,1-dx/1.50);
 const vscore=Math.max(0,1-vdist*2.4);
 const overlap=Math.max(0,Math.min(e.x2,p.x2)-Math.max(e.x1,p.x1))*Math.max(0,Math.min(e.y2,p.y2)-Math.max(e.y1,p.y1))/(e.w*e.h);
 const raw=.36*hscore+.28*vscore+.22*overlap+.14*(centerInside?1:0);
 return {person_id:p.person_id,source_person_box_id:p.id,score:Math.round(raw*10000)/10000,person_center_distance_in_halfwidths:Math.round(dx*1000)/1000,vertical_relative:Math.round(ny*1000)/1000,centre_inside_old_person_box:centerInside,intersection_over_item:Math.round(overlap*1000)/1000};
}
function inspectImage(input,settings=SETTINGS){
 const persons=input.boxes.filter(b=>b.label==="Persons").map(geomBox).sort((a,b)=>a.x-b.x||String(a.id).localeCompare(String(b.id))).map((x,i)=>({...x,person_id:"P"+String(i+1).padStart(3,"0")}));
 const positives=[],excluded=[];
 for(const raw of input.boxes){
  if(raw.label==="Persons")continue;
  const ppe_type=TYPES[raw.label];
  if(!ppe_type){excluded.push({source_id:raw.id,source_class:raw.label,reason:raw.label?.startsWith("No ")?"LEGACY_NEGATIVE_MARKER_NOT_PHYSICAL_PPE":"OUT_OF_SCOPE_CLASS"});continue;}
  const e=geomBox(raw);
  const confidence=(raw.confidence==null?null:Number(raw.confidence));
  const ranking=persons.map(p=>rankPair(e,p,ppe_type)).sort((a,b)=>b.score-a.score||a.person_id.localeCompare(b.person_id));
  const best=ranking[0],second=ranking[1];const gap=best?(second?Math.round((best.score-second.score)*10000)/10000:1):0;
  let status="UNKNOWN",why="NO_PERSON_CANDIDATE",candidate=null;
  if(persons.length){
   if(confidence!=null&&confidence<settings.minConfidence)why="DETECTION_LOW_CONFIDENCE";
   else if(best.score<settings.minScore)why="WEAK_GEOMETRY";
   else if(second&&gap<settings.minMargin)why="OVERLAPPING_OR_COMPETING_PEOPLE";
   else {status="MATCHED_CANDIDATE";candidate=best.person_id;why="HEURISTIC_CANDIDATE_NOT_HUMAN_GROUND_TRUTH";}
  }
  positives.push({source_id:raw.id,source_class:raw.label,ppe_type,person_id:candidate,status,abstention_reason:status==="UNKNOWN"?why:null,geometry_score:best?.score??null,score_margin:best?gap:null,source_confidence:confidence,ranked_evidence:ranking.slice(0,3)});
 }
 return {image_id:input.image_id,filename:input.filename,split:input.split,stage:"GEOMETRIC_REVIEW_SUGGESTIONS_ONLY",source_person_count:persons.length,person_ids_are_left_to_right_native_box_order:true,positive_item_count:positives.length,candidates:positives,excluded_boxes:excluded,never_infers_ABSENT_or_POLICY_COMPLIANCE:true};
}
function requireTest(condition,message){if(!condition)throw Error("SELFTEST_FAILED:"+message);}
export {inspectImage,rankPair,geomBox};
import {readFileSync} from "node:fs";
import {pathToFileURL} from "node:url";
if (process.argv[1] && import.meta.url===pathToFileURL(process.argv[1]).href){
 const arg=process.argv[2];
 if(arg==="--self-test"){
  const hat={id:"h",label:"Hard Hat",x:50,y:15,width:18,height:12};
  const person={id:"p",label:"Persons",x:50,y:50,width:60,height:100};
  const one=inspectImage({image_id:"single",filename:"synthetic",split:"valid",boxes:[person,hat]});
  requireTest(one.candidates[0].person_id==="P001","single_hat");
  const gloves=inspectImage({image_id:"gloves",filename:"synthetic",split:"valid",boxes:[person,hat,{id:"g1",label:"Gloves",x:35,y:58,width:12,height:12},{id:"g2",label:"Gloves",x:65,y:59,width:12,height:12}]});
  requireTest(gloves.candidates.filter(x=>x.person_id==="P001").length===3,"multiple_items");
  const no=inspectImage({image_id:"no",filename:"synthetic",split:"valid",boxes:[hat,{id:"neg",label:"No Safety Boots",x:50,y:50,width:10,height:10}]});
  requireTest(no.candidates[0].status==="UNKNOWN"&&no.excluded_boxes.length===1,"zero_person_legacy_neg");
  const ambiguous=inspectImage({image_id:"ambig",filename:"synthetic",split:"valid",boxes:[{id:"p1",label:"Persons",x:40,y:50,width:70,height:100},{id:"p2",label:"Persons",x:60,y:50,width:70,height:100},hat]});
  requireTest(ambiguous.candidates[0].status==="UNKNOWN","ambiguous_people");
  const low=inspectImage({image_id:"low",filename:"synthetic",split:"valid",boxes:[person,{...hat,confidence:0.15}]});
  requireTest(low.candidates[0].abstention_reason==="DETECTION_LOW_CONFIDENCE","low_confidence");
  const far=inspectImage({image_id:"far",filename:"synthetic",split:"valid",boxes:[person,{id:"far",label:"Safety Boots",x:500,y:500,width:10,height:10}]});
  requireTest(far.candidates[0].status==="UNKNOWN","far_bbox");
  process.stdout.write("6 SELF_TESTS_PASSED\n");
 }else if(arg){
  const input=JSON.parse(readFileSync(arg,"utf8"));if(!Array.isArray(input.images))throw Error("Expected {images:[...]}");
  const proposals=input.images.map(im=>inspectImage(im));process.stdout.write(JSON.stringify({stage:"PROPOSALS_ONLY",results:proposals},null,2)+"\n");
 }else{process.stderr.write("Usage: node association_geometry_prototype.mjs --self-test | annotated_images.json\n");process.exitCode=2;}
}
