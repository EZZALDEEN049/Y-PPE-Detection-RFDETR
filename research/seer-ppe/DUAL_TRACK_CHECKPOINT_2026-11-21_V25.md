# SEER-PPE V25 — executed A2 / A5 offline selective routing on 74 real fixed RF-DETR boxes

**Dated 21 November 2026; working manuscript v0.25.** This is a reproducible **code-executed, post-detection A2-versus-A5 engineering comparison**, but it is **not** an actual explanation/human review, an independently sampled safety-policy evaluation, or a successful energy/worker-risk superiority study. The original `altayyar-0oflt-lafos-qqauz/2` model and all source data were untouched.

## 1. What was actually executed

- **Before executing the V25 code:** committed [V25 frozen protocol](V25_A2_A5_PAIRED_ROUTING_PROTOCOL_FROZEN_2026-11-21.md), git commit `4f42128cc2a39197a7ecf8ee78643b22337b7185`.
- **Frozen real detector sources:** [V16 original hosted Train model outputs](ROBOFLOW_TRAIN_ONLY_REAL_MODEL_PREFLIGHT_2026-11-21_V16.json) from 4 Train photos (51 boxes) and [V23 original hosted Valid model outputs](VALID_ORIGINAL_SOURCE_CURRENT_BBOX_MODEL_PILOT_V23.json) from 5 historically development-exposed original Valid photos (23 boxes). **Nine images, 74 real existing model boxes, zero new inference.** Test not accessed.
- **Implementation:** [actual deterministic A0/A2/A5 routing code](tools/run_v25_paired_selective_routing.mjs) executed in [successful GitHub Actions run 44944842661](https://github.com/EZZALDEEN049/Y-PPE-Detection-RFDETR/actions/runs/44944842661). All fail-closed tests and the source-ID/model/score/cue/geometry/safety budget checks passed.
- **A0** = unchanged detector output, no occupational safety policy. **A2** = lowest-confidence typed PPE cue priority, with the *same mandatory abstention* as A5. **A5** = pre-specified additive uncertainty, negative-named class, provisional association uncertainty and severity proxy. A5 proxy is **not independently calibrated hazard risk**.
- **Both policies:** exactly one **proposed** XAI target and one **proposed** human-review item maximum per image with any typed PPE cue. Zero actual XAI calls, zero actual reviews dispatched, zero model calls in V25, no measured runtime/energy efficiency. Task mandate is always `POLICY_UNKNOWN`, individual visual PPE state unadjudicated, person coverage unverified; both output no verified employee compliance/violation and no scene-safe clearance.

## 2. Actual results, restricted to software routing decisions

| Recorded property | A0 detector | A2 confidence-only guarded | A5 SEER guarded proxy |
|---|---:|---:|---:|
| Same real original model detection boxes | 74 | 74 | 74 |
| Person candidate boxes | 10 | 10 | 10 |
| Typed PPE cue boxes | 59 | 59 | 59 |
| Context category boxes | 5 | 5 | 5 |
| Proposed explanation targets | not applicable | **8** | **8** |
| Proposed review items | not applicable | **8** | **8** |
| **Actual additional XAI requests completed** | 0 | **0** | **0** |
| **Actual reviewer items dispatched** | 0 | **0** | **0** |
| Unselected cue boxes still pending (no auto-clearance) | n/a | **51** | **51** |
| Worker-level safe clearances or confirmed violations issued | 0 (no policy) | **0** | **0** |

Across **9 images**, exact target IDs agreed in **6** (including one image with no typed PPE cue) and differed in **3**. **Four images** had no Person detection; none was interpreted as human-free. A2/A5 proposed XAI and review caps were identical, but because the proposals were never executed this does not demonstrate less compute, shorter latency or safe review effectiveness.

**Exploratory post-routing object-level error probe:** In the separate, previously available V23 actual Valid 5-image object matching results, a single detected `Safety Vests` bbox was FP. A2 happened to nominate that one object-FP, while A5 nominated a `No Face Mask` bbox matched as TP instead, giving **1 vs 0 nominated known object FPs**. The V23 outcome *was not used in either routing priority*. One box-level FP, and no real PPE-mandate reference, provides **no basis to claim one method improves worker safety**. It is not fair to compare this small posthoc count as an efficacy advantage for either policy.

## 3. Scientific status and remaining work

The [canonical paper is now v0.25](MANUSCRIPT_MASTER.md) with updated Abstract, Methods §3.19, Results §4.19, Discussion §5.7, limitations/remaining work and Appendix Q. The original manuscript and V24 bibliography remain preserved. **This closes "first actual A2 and A5 policy-code execution on real detector outputs"**, not the primary empirical comparison. The next genuine experimental milestones are:
1. Execute a *strong* uncertainty-gated safety-matched selective competitor, target-matched perturbation XAI, and any review actions that can be meaningfully verified, with genuinely available reference and explicit budget/cost.
2. Extend current-author-GT per-class bbox matching to preselected original Valid Source IDs, separated from the historical 2025 provider counters and the tiny development-only V23 pilot; keep previously exposed examples flagged.
3. Report actual measured latency/memory/XAI calls and physical joules **only if instrumented**. When individual worker safety task mandates are absent, do not invent a false-clearance denominator or occupational-compliance result.
4. Prepare journal tables, diagrams, accurate literature review and final Word with transparently bounded outcomes.

**Author's images were already chosen/classified/reviewed by the author; no repeated comprehensive image review or second human rater is requested.** The strict acquisition-independent person–PPE worker-scoring gate is still **`NOT_FROZEN` / `scoring_ready=false`**. Historical Test was development-exposed and was not accessed in this continuation. Github repository visibility must be checked separately if author wants privacy; archival research code is public by default until changed.

## 4. Exact reproducible evidence

- [V25 frozen-before-execution protocol](V25_A2_A5_PAIRED_ROUTING_PROTOCOL_FROZEN_2026-11-21.md)
- [Executable policy code, deterministic negative-control unit tests](tools/run_v25_paired_selective_routing.mjs)
- [V25 full actual per-image class/association/priority/target trace](ACTUAL_A0_A2_A5_PAIRED_OFFLINE_ROUTING_V25.json)
- [Successful V25 original model input/abstention/budget checks](https://github.com/EZZALDEEN049/Y-PPE-Detection-RFDETR/actions/runs/44944842661)
- [Working paper v0.25 including main analysis and Appendix Q](MANUSCRIPT_MASTER.md)
