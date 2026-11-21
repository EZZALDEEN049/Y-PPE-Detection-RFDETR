# SEER-PPE V11 — executable Person–PPE evaluation protocol (Validation only)

**Status:** implemented, **gated / not scored** as of 21 November 2026. Detector and dataset remain unchanged. This is an offline research evaluator that consumes externally documented reference and prediction records; it does not run RF-DETR or touch Test.

## Reproducible commands

```bash
node research/seer-ppe/tools/validate_v11_source_and_person_ppe_gate.mjs --self-test
node research/seer-ppe/tools/validate_v11_source_and_person_ppe_gate.mjs --audit
# Scoring is deliberately blocked by the current unsigned freeze:
node research/seer-ppe/tools/validate_v11_source_and_person_ppe_gate.mjs --score /path/to/actual-signed-valid-bundle.json
```

The first command runs **synthetic unit tests only**; the second audits real saved GitHub metadata and must report `scoring_ready=false`. The third is designed for **future** authorized, frozen Validation data; at present it must refuse with a non-zero exit, **without generating metrics**. It **never** accepts Test input.

## Preconditions before any real scoring

1. Source eligibility: immutable [468-source decision ledger](SOURCE_ELIGIBILITY_DECISION_LEDGER_2026-11-21_V11.json) plus [individual signed decisions overlay](SOURCE_LINEAGE_SIGNED_DECISIONS_2026-11-21_V11.json); each scored Valid image must have a source-specific supported independence verdict with evidence, acquisition group, explicit Train-family crosscheck and dated curator signoff. All five previous research holds remain ineligible in V11 regardless of overlay.
2. Cohort scope: reconcile **original Source IDs to the actually selected Clean17 export** (or state a separately frozen original-Valid scope); the V11 freeze deliberately requires verified Clean17 membership per scored case. The old original 468-image Valid is **not** automatically the cleaned 459-image Valid, and this implementation does not pretend such a mapping is finished.
3. Human reference: each visible person must have image-local ID, **six** visual PPE statuses `PRESENT/ABSENT/UNKNOWN`, six separately sourced task mandates, and human-signed person coverage including zero-person scenes; incomplete B Train cells and D no-person signoff cannot be filled by model predictions.
4. Verifiable correspondence: explicit human-reviewed alignment for person IDs and item IDs. Predicted state **UNKNOWN** denotes abstention, not a negative. Every enumerated worker must be represented even when the detector missed them. For association analysis, all GT item IDs must be accounted for as a matched owner candidate or abstention, and extraneous unmatched detector boxes belong to a separate detection evaluation.
5. Freeze: set [freeze record](VALIDATION_PERSON_PPE_SCORING_FREEZE_2026-11-21_V11.json) to `SIGNED_VALIDATION_ONLY` only after locking model, thresholds, source scope, matching policy, metrics plan, reference and reviewer details in a versioned commit. This software checks the presence and consistency of signed evidence, not the truth of externally attested provenance.

## Metrics emitted only after all gates

- **Visual PPE assessment** per equipment type: eligible known human states; unknown human states excluded and reported; model abstentions; selective retained coverage and retained accuracy; PRESENT precision, overall-PRESENT recall including abstained positives, and retained-only sensitivity. Denominators and zero-denominator `null` behavior are explicit; human `UNKNOWN` is never coerced into `ABSENT`.
- **Verified post-correspondence association**: correct/wrong item owner; known-owner abstentions; unsigned guesses on human-unknown-owner items, pair precision, recall including abstentions and F1 **only for verified item correspondence**. Without a box-matching audit these must not be presented as whole-detector association performance.
- **Always null / unsupported here:** detector mAP, actual electrical energy, worker/site compliance, true hazard severity, statistical confidence intervals, and independent Test generalization. `POLICY_UNKNOWN` remains explicit; a missing PPE visual state cannot establish an occupational violation absent a documented task/site requirement.

## Current real-world evidence boundary

The existing Train A/B/C/D preflight remains **0/4 complete**, with **19** human-approved item-owner links, **38/42** saved visual cells, **4** B mask/boot cells not recorded and no D human-signed zero-person reference. There are **0** signed Valid source-family eligibility decisions and **no frozen Valid evaluation population**. Synthetic test successes and record-audit passes are **engineering evidence, not model performance**. Historical Test was development-exposed and will need its own later explicitly frozen evaluation protocol, never supplied to this Validation-only tool.

[Example input contract](PERSON_PPE_EVAL_INPUT_CONTRACT_2026-11-21_V11.json) · [Source-decision protocol](SOURCE_ELIGIBILITY_DECISION_PROTOCOL_2026-11-21_V11.md).
