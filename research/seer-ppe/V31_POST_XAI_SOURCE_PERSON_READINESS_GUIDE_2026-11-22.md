# SEER-PPE V31 — post-V30 source-family and Person–PPE scientific-scoring readiness

**Date:** 22 November 2026. **Evidence state:** read-only audit of saved historical source, signed-reference and Train pilot records, plus independently verified actual V30 XAI. **Not an expert signoff, new source classification or worker-compliance evaluation.**

## Completed foundation

V30 is now a **completed real-model development-exposed experiment**: eight original Train/Valid images, ten frozen target detections, 1,068 total real hosted calls, 640 8×8 target-cell outcomes, and 60 eleven-point progressive deletion/insertion curves. Its full numeric data are permanently stored in [V30 actual evidence](V30_ACTUAL_PROGRESSIVE_XAI_RESULTS_2026-11-22.json), with an independent [PASS_NUMERIC_INTEGRITY_ONLY audit](V30_INDEPENDENT_NUMERIC_AUDIT_2026-11-22.json). Independent arithmetic integrity is **not** independent visual-explanation or occupational-safety reference ground truth. No further V30 inference is needed.

## Current valid-source readiness: 0 of 459 signed

[Machine-readable source/person readiness ledger](V31_SOURCE_PERSON_SAFETY_READINESS_2026-11-22.json) uses the unchanged [V15 signed-source matrix](VALIDATION_459_SIGNED_SOURCE_COHORT_READINESS_V15.json), existing researcher-signature overlays and source-risk evidence.

| Current author-corrected Clean17 Validation group | Images | Scientific source independence signed? |
|:--|--:|:--|
| Historical research holds | **5** | No; remain held |
| Additional V14 direct-overlap technical quarantine | **6** | No; remain quarantined |
| Other source-family risk candidates | **81** | No; require evidence-based family decision |
| Unflagged by current technical screens | **367** | No; absence of a screen flag is not independence proof |
| **Total** | **459** | **0 independently signed source-family assessments** |

The original Valid Source split had **468** items; the Clean17 corrected Valid derivative has **459** matched items, with nine earlier exclusions. All 459 have technical image-content correspondence recorded, but none has acquired a **signed individual source-family independence verdict**. Historical holds are not lifted by a broad quality-review acceptance or by a pixel hash inequality.

**P0 administrative queue:** the ledger contains the exact 11 original Valid source IDs and filenames corresponding to **five historical holds plus six technical quarantine cases**. Existing comparison evidence remains attached to earlier versioned files. Prioritize reconciling provenance/family records for those 11, but do not automatically certify or release any. The 81 other flagged cases and 367 unflagged cases remain non-scoring until acquisition grouping and eligibility are truly documented.

## Current Person–PPE human reference: no signed Valid worker gold

The preserved Train-only Eval A/B/C/D record contains **19** author-approved person–equipment item-owner links and **38 of 42** recorded person×PPE visual states. Four visual fields are not entered in Train B: `P001:face_mask`, `P001:safety_boot`, `P002:face_mask`, and `P002:safety_boot`. Case D has no *signed* human zero-person statement. Those are **existing record-completeness gaps**, not a request to undo the author's accepted broad image review, and not validation reference coverage.

The [original Valid human-gold overlay](VALIDATION_PERSON_PPE_SIGNED_REFERENCE_V15.json) has **zero independently signed Valid worker cases**. Original 17-class detection boxes (including V26 and V30), previous author general visual-review acceptance, Train pilot wearer-item link statements and the original RF-DETR class labels cannot be converted into new per-worker signed Valid gold automatically.

For any future eligible Valid reference record, distinguish:
- *worker visible/coverage* and identity within the particular image, including missed-person and cropped-person cases;
- *item ownership* of detected PPE or negative-cue box;
- *visual PPE state* `PRESENT`, `ABSENT` or `UNKNOWN` for six categories, including face mask, safety boots, hard hat, vest, gloves and goggles;
- *occupational task/site mandate* `REQUIRED`, `NOT_REQUIRED` or `POLICY_UNKNOWN`, based on real applicable evidence rather than image appearance;
- *reviewer, date, evidence reference and SHA-256*, with unknown or unsigned decisions never imputed as negative/compliant.

These are prospective signatures, **not declarations that the researcher must redo all photographs**. Image review already accepted by the researcher remains recorded; the pending requirement is separately auditable *individual source lineage, per-person coverage and task-rule evidence* needed for a scientific outcome.

## Next bounded work packages

1. **V31-A — source P0 decision preparation:** reconcile existing Train–Valid comparison/evidence pointers and acquisition-family IDs for the 11 frozen high-overlap source IDs. Maintain current holds/quarantines until a human evidence-based family verdict exists.
2. **V31-B — full-scoring-cohort eligibility:** populate the existing separate signed source-family overlay, *only from authentic source records*. Avoid assuming all 367 unflagged images are independent. Re-run the unchanged V15 gate after truly signed records exist.
3. **V31-C — human reference:** on a legitimately selected and eligible Valid subset, obtain the existing protocol's signed person coverage, wearer-item associations, per-PPE visibility and applicable task-policy records. Keep `POLICY_UNKNOWN` or `UNKNOWN` where justified.
4. **V31-D — Train pilot administrative gaps:** retain the four unentered B fields and unsigned D zero-person coverage as missing until individually signed by the researcher; they are **not** a substitute for Valid scoring gold.
5. **V31-E — future comparison after gates:** freeze a separate source-eligible worker-outcome cohort and compare a strong selective A2/A6-style policy against A5 under matched review demand, actual detector/XAI calls and verified safety constraints. Physical Joules only if instrumented. **Do not reuse protected Test for threshold development.**

## Hard scientific gate

`scoring_ready=false` and `NOT_FROZEN` remain the only supported statuses for source-independent worker-level SEER-PPE effectiveness. This V31 work creates no new Roboflow inferences, source-image mutations, model retraining, Test viewing, signed reviewer decisions or compliance scores. V30 progressive AUC is **completed** but does not supersede the human/source gates.

Read-only executable verification: [`tools/verify_v31_post_xai_readiness.mjs`](tools/verify_v31_post_xai_readiness.mjs) with `--verify` and mutation-sensitive `--self-test`. Any later legitimate human/source registry update must regenerate the administrative ledger; the validator intentionally fails closed against stale claim counts.
