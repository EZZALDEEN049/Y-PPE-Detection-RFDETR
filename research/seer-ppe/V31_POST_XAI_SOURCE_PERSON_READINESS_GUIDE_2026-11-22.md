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
2. **V31-B — full-scoring-cohort eligibility:** continue the existing source-family overlay from authentic source records. Two Valid images now have a signed non-independent shared-site verdict; this does not qualify them for scoring. The remaining 457 Valid images still need an evidence-based source-family decision, and the 5+6 guarded cases remain blocked. Avoid assuming any unflagged images are independent.
3. **V31-C — human reference:** on a legitimately selected and eligible Valid subset, obtain the existing protocol's signed person coverage, wearer-item associations, per-PPE visibility and applicable task-policy records. Keep `POLICY_UNKNOWN` or `UNKNOWN` where justified.
4. **V31-D — Train pilot administrative gaps:** retain the four unentered B fields and unsigned D zero-person coverage as missing until individually signed by the researcher; they are **not** a substitute for Valid scoring gold.
5. **V31-E — future comparison after gates:** freeze a separate source-eligible worker-outcome cohort and compare a strong selective A2/A6-style policy against A5 under matched review demand, actual detector/XAI calls and verified safety constraints. Physical Joules only if instrumented. **Do not reuse protected Test for threshold development.**

## Hard scientific gate

`scoring_ready=false` and `NOT_FROZEN` remain the only supported statuses for source-independent worker-level SEER-PPE effectiveness. This V31 work creates no new Roboflow inferences, source-image mutations, model retraining, Test viewing, signed reviewer decisions or compliance scores. V30 progressive AUC is **completed** but does not supersede the human/source gates.

Read-only executable verification: [`tools/verify_v31_post_xai_readiness.mjs`](tools/verify_v31_post_xai_readiness.mjs) with `--verify` and mutation-sensitive `--self-test`. Any later legitimate human/source registry update must regenerate the administrative ledger; the validator intentionally fails closed against stale claim counts.


## V31-A completed — read-only reconciliation of all 11 P0 source packets (22 November 2026)

The 11 frozen cases have now been reconciled against **33 saved original Train–Valid pair measurements** from V14 and the prior V18 visual-site record. No new photo review was requested or performed. [The detailed machine-readable dossier](V31_A_SOURCE_LINEAGE_RECONCILIATION_2026-11-22.json) and [human-readable case table](V31_A_SOURCE_LINEAGE_RECONCILIATION_2026-11-22.md) preserve every original Valid ID, strongest Train candidate, SSIM/MAE, ORB matches/inliers, embedding score where present, image dimensions, raw-byte inequality and current hold status. [The V31-A validator](tools/verify_v31a_source_reconciliation.mjs) passed its mutation tests and full read-only CI [run 44967406330](https://github.com/EZZALDEEN049/Y-PPE-Detection-RFDETR/actions/runs/44967406330); public engineering tests also passed [run 44967406346](https://github.com/EZZALDEEN049/Y-PPE-Detection-RFDETR/actions/runs/44967406346).

### Specific source correction

The prior visual record shows Valid `IMG-20250416-WA0063.jpg` and `IMG-20250416-WA0051.jpg`, together with Train `IMG-20250416-WA0067.jpg` and `IMG-20250416-WA0066(1).jpg`, all bearing the named **مدرسة 22 مايو – عصيفرة** site. Preserve the two Valid site-family holds. In contrast, the earlier visual record identifies Valid `IMG-20250416-WA0026.jpg` as **مدرسة الشهيد العلفي**, a different named site; do not group WA0026 with the 22 May school based only on the WA filename prefix. However, its Train `IMG-20250416-WA0079.jpg` match remains a strong unresolved image-lineage issue (SSIM 0.93240; 756 ORB matches/751 inliers), so its historical hold is **not released**.

### V31-A status boundary

**11/11 technical packets reconciled; 5 historical holds and 6 technical quarantines preserved; 33 pair records checked; 0 new human attestations; 0 releases; 0 newly eligible scoring images.** This work does not certify source independence. The next necessary input is the author's specific acquisition/site/session knowledge for unresolved pairs, recorded transparently as an actual human attestation rather than inferred from image metrics. No model calls, Test access, original image reopening, dataset writes or repeated general image review occurred.


## V31-A1 — author confirms the shared School 22 May site (22 November 2026)

The dataset author answered **“نعم”** to the specific question whether Valid `IMG-20250416-WA0063.jpg` and `IMG-20250416-WA0051.jpg`, together with Train `IMG-20250416-WA0067.jpg` and `IMG-20250416-WA0066(1).jpg`, belong to the same **مدرسة 22 مايو – عصيفرة** construction project/site, even if photographed at different times or angles.

This is recorded as `SHARED_CAPTURE_SESSION_OR_SITE`, site-family ID `site_school_22may_aseefrah`, for the two Valid members. It is a site/project-family decision only: no same-frame or same-capture-session claim is made, and no session ID is invented. The exact chat response is preserved in [the author evidence record](evidence/AUTHOR_CHAT_ATTESTATION_SCHOOL_22_MAY_ASEEFRAH_2026-11-22.md), SHA-256 `326c7ad0347a86822768e4f1703045248247bc3014cd5ccb139148332cc07605`. The two per-image decisions are in [the V31-A1 machine record](V31_A1_AUTHOR_SITE_ATTESTATION_2026-11-22.json) and [human-readable report](V31_A1_AUTHOR_SITE_ATTESTATION_2026-11-22.md).

**Result:** 2 of the 11 P0 Valid cases now have author-attested shared-site verdicts; both remain hard-held because Train contains the same site. The other 3 historical holds and all 6 technical quarantines remain blocked. There are **0 independent-source attestations, 0 newly eligible Valid images, and 0 signed Valid Person–PPE gold cases**. The cohort remains `scoring_ready=false`. [V31-A1 validator](tools/verify_v31a1_author_site_attestation.mjs) checks the evidence SHA and rejects mutations that would invent a capture session, erase Train overlap, or release a hold.
