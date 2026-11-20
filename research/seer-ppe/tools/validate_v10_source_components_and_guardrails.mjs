#!/usr/bin/env node
/**
 * V10 offline research-record consistency and similarity-graph audit.
 * Read-only: no Roboflow access, image bytes, model inference, or Test labels.
 * Connected components denote dHash-candidate connectivity, NOT proven source families.
 */
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';

const read = name => JSON.parse(readFileSync(new URL('../' + name, import.meta.url), 'utf8'));
const node = (kind, id) => kind + ':' + id;

export function candidateComponents(pairs) {
  assert.ok(Array.isArray(pairs));
  const parent = new Map();
  const find = id => {
    if (!parent.has(id)) parent.set(id, id);
    if (parent.get(id) !== id) parent.set(id, find(parent.get(id)));
    return parent.get(id);
  };
  const seen = new Set();
  for (const e of pairs) {
    assert.ok(typeof e.valid_id === 'string' && e.valid_id.length > 0);
    assert.ok(typeof e.train_id === 'string' && e.train_id.length > 0);
    assert.ok(Number.isInteger(e.dhash_hamming) && e.dhash_hamming >= 0 && e.dhash_hamming <= 8);
    assert.equal(e.raw_sha256_equal, false, 'Do not silently discard exact-match evidence');
    assert.equal(e.rgb_sha256_equal, false, 'Do not silently discard exact-pixel evidence');
    const a = node('v', e.valid_id), b = node('t', e.train_id);
    const edge = a + '|' + b;
    assert.ok(!seen.has(edge), 'Repeated exact candidate edge: ' + edge);
    seen.add(edge);
    const ar = find(a), br = find(b);
    if (ar !== br) parent.set(br, ar);
  }
  const groups = new Map();
  for (const e of pairs) {
    const k = find(node('v', e.valid_id));
    const g = groups.get(k) || {valid: new Set(), train: new Set(), pair_count: 0, min_dhash: 9};
    g.valid.add(e.valid_id);
    g.train.add(e.train_id);
    g.pair_count += 1;
    g.min_dhash = Math.min(g.min_dhash, e.dhash_hamming);
    groups.set(k, g);
  }
  const components = [...groups.values()].map(g => ({
    valid_source_ids: [...g.valid].sort(),
    train_source_ids: [...g.train].sort(),
    candidate_pair_count: g.pair_count,
    minimum_dhash_distance: g.min_dhash
  })).sort((a,b) => a.minimum_dhash_distance - b.minimum_dhash_distance ||
      b.candidate_pair_count - a.candidate_pair_count ||
      a.valid_source_ids[0].localeCompare(b.valid_source_ids[0]));
  return components.map((x,i) => ({candidate_component_id:'SIM' + String(i+1).padStart(3,'0'), ...x}));
}

export function conservativeRecordDisposition(pilot) {
  assert.ok(pilot && pilot.output && pilot.review_codes, 'Missing preflight record');
  const {output, review_codes:codes} = pilot;
  for (const key of ['raw','high','lower','persons']) {
    assert.ok(Number.isInteger(output[key]) && output[key] >= 0);
  }
  assert.equal(output.raw, output.high + output.lower);
  assert.equal(codes.association, 'ASSOCIATION_UNKNOWN');
  assert.equal(codes.policy, 'POLICY_UNKNOWN');
  assert.ok(['PERSON_COVERAGE_UNKNOWN','PERSON_CANDIDATES_DETECTED_COVERAGE_UNVERIFIED'].includes(codes.person_coverage));
  assert.equal(codes.person_coverage, output.persons === 0
    ? 'PERSON_COVERAGE_UNKNOWN' : 'PERSON_CANDIDATES_DETECTED_COVERAGE_UNVERIFIED');
  const reasons = ['POLICY_UNKNOWN','ASSOCIATION_UNKNOWN','PERSON_COVERAGE_NOT_HUMAN_VERIFIED'];
  if (output.lower > 0) reasons.push('LOW_SCORE_DETECTION_CANDIDATES');
  if (output.persons === 0) reasons.push('ZERO_PERSON_CANDIDATES_DOES_NOT_PROVE_NO_PERSON');
  return {
    case:pilot.case,
    suggested_disposition:'ABSTAIN_AND_REQUEST_REVIEW',
    reasons,
    automatic_compliant_clearance:false,
    proved_workplace_violation:false,
    review_request_executed:false,
    review_completed:false,
    scientific_performance_observation:false
  };
}

export function audit() {
  const frozen=read('SOURCE_ID_MANIFEST_TRAIN_VALID_2026-11-19_V01.json');
  const queue=read('SOURCE_FAMILY_REVIEW_QUEUE_2026-11-21_V06.json');
  const validPlan=read('VALIDATION_ELIGIBILITY_PLANNING_MANIFEST_2026-11-21_V08.json');
  const workflow=read('TRAIN_ONLY_UNSCORED_PREFLIGHT_2026-11-21_V09.json');
  const human=read('PERSON_PPE_REFERENCE_LIVE_SNAPSHOT_2026-11-21_V09.json');
  const byId=new Map(frozen.images.map(x=>[x.image_id,x]));
  assert.equal(frozen.images.length,2093);
  assert.equal(byId.size,2093);
  assert.equal(frozen.images.filter(x=>x.split==='train').length,1625);
  assert.equal(frozen.images.filter(x=>x.split==='valid').length,468);
  assert.equal(frozen.images.filter(x=>x.split==='test').length,0);
  assert.equal(queue.original_near_hash_pairs.length,46);
  assert.equal(queue.raw_or_rgb_matches,0);
  assert.equal(queue.human_source_family_signoffs_added,0);
  for(const e of queue.original_near_hash_pairs){
    assert.equal(byId.get(e.valid_id)?.split,'valid','Invalid/future Test candidate in Valid source graph');
    assert.equal(byId.get(e.train_id)?.split,'train','Invalid/future Test candidate in Train source graph');
    assert.equal(byId.get(e.valid_id)?.filename,e.valid_filename);
    assert.equal(byId.get(e.train_id)?.filename,e.train_filename);
  }
  const components=candidateComponents(queue.original_near_hash_pairs);
  const allValid=new Set(components.flatMap(x=>x.valid_source_ids));
  const allTrain=new Set(components.flatMap(x=>x.train_source_ids));
  assert.equal(components.length,27);
  assert.equal(allValid.size,31);
  assert.equal(allTrain.size,41);
  assert.equal(components.filter(x=>x.candidate_pair_count>1).length,8);
  assert.equal(components.reduce((sum,x)=>sum+x.candidate_pair_count,0),46);
  assert.equal(validPlan.valid_rows.length,468);
  const bucket={};
  const validPlanIds=new Set();
  for(const row of validPlan.valid_rows){
    assert.equal(row.split,'valid');
    assert.equal(byId.get(row.source_id)?.split,'valid');
    assert.ok(!validPlanIds.has(row.source_id));
    validPlanIds.add(row.source_id);
    assert.equal(row.explicit_independent_source_signoff,false);
    assert.equal(row.may_use_for_independent_scientific_scoring,false);
    bucket[row.eligibility_bucket]=(bucket[row.eligibility_bucket]||0)+1;
  }
  assert.equal(bucket.PREEXISTING_RESEARCH_HOLD,5);
  assert.equal(bucket.SOURCE_FAMILY_REVIEW_CANDIDATE_NOT_SIGNED,94);
  assert.equal(bucket.NO_SCREEN_FLAG_SOURCE_INDEPENDENCE_UNCERTIFIED,369);
  assert.equal(queue.review_queue.length,99);
  assert.ok([...allValid].every(x=>queue.review_queue.some(y=>y.valid_source_id===x)));
  assert.equal(validPlan.test_sources_accessed,0);
  assert.equal(validPlan.scoring_ready,false);
  assert.equal(workflow.image_split,'train');
  assert.equal(workflow.evaluated_test_or_valid_images,0);
  assert.equal(workflow.model,'altayyar-0oflt-lafos-qqauz/2');
  assert.equal(workflow.workflow.disable_active_learning,true);
  assert.deepEqual(workflow.cases.map(x=>x.case),['A','B','C','D']);
  const suggestions=workflow.cases.map(conservativeRecordDisposition);
  assert.ok(suggestions.every(x=>x.automatic_compliant_clearance===false&&x.review_completed===false));
  assert.ok(suggestions[3].reasons.includes('ZERO_PERSON_CANDIDATES_DOES_NOT_PROVE_NO_PERSON'));
  assert.equal(human.human_approved_links_preserved,19);
  assert.equal(human.saved_worker_ppe_states,38);
  assert.equal(human.expected_worker_ppe_states,42);
  assert.equal(human.case_complete_count,0);
  assert.equal(human.case_D_human_signed_zero_person_decision,false);
  assert.equal(human.missing_state_cells.length,4);
  assert.deepEqual(human.missing_state_cells.map(x=>x.case+':'+x.person_id+':'+x.ppe_type).sort(),
    ['B:P001:face_mask','B:P001:safety_boot','B:P002:face_mask','B:P002:safety_boot'].sort());
  assert.equal(human.model_inference_promoted_to_reference,false);
  assert.equal(human.scoring_ready,false);
  assert.equal(workflow.scientific_readiness.mAP,null);
  assert.equal(workflow.scientific_readiness.F1,null);
  assert.equal(workflow.scientific_readiness.energy_joules,null);
  assert.equal(workflow.scientific_readiness.scoring_ready,false);
  return {
    schema_version:'seer-ppe/graph-and-fail-closed-record-derivation/v0.10',
    date:'2026-11-21',
    evidence_scope:'EXISTING_GITHUB_RECORDS_ONLY',
    read_only:true,
    graph_is_proven_source_family_adjudication:false,
    train_valid_originals_checked:2093,
    near_pair_edges:46,
    unique_valid_in_near_graph:allValid.size,
    unique_train_in_near_graph:allTrain.size,
    graph_candidate_components:components.length,
    multi_pair_candidate_components:components.filter(x=>x.candidate_pair_count>1).length,
    valid_eligibility_buckets:bucket,
    source_family_independence_confirmed:false,
    human_links_preserved:19,
    human_states_saved:38,
    human_states_expected:42,
    missing_B_cells:human.missing_state_cells,
    D_signed_zero_person:false,
    train_case_review_suggestions:suggestions,
    any_research_review_performed_by_this_script:false,
    original_dataset_or_model_changed:false,
    test_accessed:false,
    mAP:null,
    F1:null,
    compliance_accuracy:null,
    joules:null,
    scoring_ready:false,
    components
  };
}

function selfTest() {
  const e=(v,t,d)=>({valid_id:v,train_id:t,dhash_hamming:d,raw_sha256_equal:false,rgb_sha256_equal:false});
  const c=candidateComponents([e('v1','t1',0),e('v1','t2',2),e('v2','t2',4),e('v3','t3',1)]);
  assert.equal(c.length,2);
  assert.deepEqual(c.map(x=>x.candidate_pair_count).sort(),[1,3]);
  assert.throws(()=>candidateComponents([e('v1','t1',0),e('v1','t1',0)]));
  assert.throws(()=>candidateComponents([{...e('v1','t1',0),raw_sha256_equal:true}]));
  const d=conservativeRecordDisposition({case:'D',output:{raw:1,high:1,lower:0,persons:0},
    review_codes:{association:'ASSOCIATION_UNKNOWN',policy:'POLICY_UNKNOWN',person_coverage:'PERSON_COVERAGE_UNKNOWN'}});
  assert.equal(d.automatic_compliant_clearance,false);
  assert.equal(d.review_request_executed,false);
  assert.throws(()=>conservativeRecordDisposition({case:'D',output:{raw:1,high:0,lower:0,persons:0},
    review_codes:{association:'ASSOCIATION_UNKNOWN',policy:'POLICY_UNKNOWN',person_coverage:'PERSON_COVERAGE_UNKNOWN'}}));
  console.log('SEER_V10_SYNTHETIC_GRAPH_AND_GUARDRAIL_CONTRACT_PASS');
}

const arg=process.argv[2];
if(arg==='--self-test') selfTest();
else if(arg==='--report') process.stdout.write(JSON.stringify(audit(),null,2)+'\n');
else if(arg==='--verify'||arg===undefined) {
 const r=audit();
 assert.equal(r.scoring_ready,false);
 console.log('SEER_V10_27_CANDIDATE_COMPONENTS_4_SAFE_ABSTENTIONS_FAIL_CLOSED_PASS');
} else {console.error('Usage: --self-test | --verify | --report');process.exitCode=2;}
