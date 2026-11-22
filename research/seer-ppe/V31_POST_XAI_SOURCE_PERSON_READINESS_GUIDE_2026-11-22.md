# SEER-PPE V31 — post-V30 source-family and Person–PPE scientific-scoring readiness

**Date:** 22 November 2026. **Evidence state:** read-only audit of saved historical source, signed-reference and Train pilot records, plus independently verified actual V30 XAI. **Not an expert signoff, new source classification or worker-compliance evaluation.**

## V32 author-selected scope amendment — 22 November 2026

The author selected **Path 1: limit the current manuscript to image-level PPE object detection and perturbation-based XAI**. The canonical manuscript is now v0.32 and the experimental protocol v0.8. Accordingly, the Person–PPE and worker/task-policy procedures below remain historical/future-research documentation only. Their incomplete status and `scoring_ready=false` are **not blockers** to the current manuscript. No worker-level compliance, false-clearance, actual review-efficacy, external explanation-faithfulness or energy claim is made. Current XAI evidence is described as perturbation sensitivity only. See [V32 scope decision](V32_IMAGE_LEVEL_DETECTION_XAI_SCOPE_DECISION_2026-11-22.md) and [machine record](V32_IMAGE_LEVEL_DETECTION_XAI_SCOPE_DECISION_2026-11-22.json).


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

## Current work packages after V32

1. **Detection/XAI scope:** continue from V26–V30 using the frozen original model and image-level references.
2. **Explanation robustness:** evaluate grid, mask/background, blur and target-selection sensitivity; do not call perturbation AUC externally validated faithfulness.
3. **Matched-budget routing comparison:** expand A5/A6-style image-target comparison and report overlap, correctness alignment and call counts without unsupported superiority claims.
4. **Editorial completion:** reconcile results tables/figures, verify references and export the manuscript.

The former V31-C/V31-D/V31-E worker-reference tasks are **superseded for the current manuscript**. Person–PPE pilot artifacts remain archived and may support a separately scoped future study, but no new worker-level annotations or task mandates are requested now.

## Current scope status

The strict worker-safety readiness flag remains `scoring_ready=false`, accurately reflecting that no signed Valid worker-level gold or independent worker-safety cohort exists. Under V32, this is **not a current manuscript gate**. Source-family overlap controls and M0/M1/M2 sensitivity remain relevant and must not be removed. The current manuscript is limited to image-level detection and perturbation-sensitivity XAI; it makes no worker-compliance, actual review-efficacy, acquisition-independent generalization, causal-faithfulness or Joule claim.

Read-only V31 validators remain historical checks of the archived readiness record; they do not define the V32 scientific scope.
## V31-A completed — read-only reconciliation of all 11 P0 source packets (22 November 2026)

The 11 frozen cases have now been reconciled against **33 saved original Train–Valid pair measurements** from V14 and the prior V18 visual-site record. No new photo review was requested or performed. [The detailed machine-readable dossier](V31_A_SOURCE_LINEAGE_RECONCILIATION_2026-11-22.json) and [human-readable case table](V31_A_SOURCE_LINEAGE_RECONCILIATION_2026-11-22.md) preserve every original Valid ID, strongest Train candidate, SSIM/MAE, ORB matches/inliers, embedding score where present, image dimensions, raw-byte inequality and current hold status. [The V31-A validator](tools/verify_v31a_source_reconciliation.mjs) passed its mutation tests and full read-only CI [run 44967406330](https://github.com/EZZALDEEN049/Y-PPE-Detection-RFDETR/actions/runs/44967406330); public engineering tests also passed [run 44967406346](https://github.com/EZZALDEEN049/Y-PPE-Detection-RFDETR/actions/runs/44967406346).

### Specific source correction

The prior visual record shows Valid `IMG-20250416-WA0063.jpg` and `IMG-20250416-WA0051.jpg`, together with Train `IMG-20250416-WA0067.jpg` and `IMG-20250416-WA0066(1).jpg`, all bearing the named **مدرسة 22 مايو – عصيفرة** site. Preserve the two Valid site-family holds. The earlier visual record identifies Valid `IMG-20250416-WA0026.jpg` as **مدرسة الشهيد العلفي**, distinct from the 22 May school; do not group WA0026 with the 22 May school based only on the WA filename prefix. The author subsequently clarified that Valid WA0026 and Train `IMG-20250416-WA0079.jpg` depict the **same scene with changes and processing**. This is recorded as a shared-scene relationship, not byte identity or an exact original-frame claim; WA0026's historical hold remains **not released**.

### V31-A status boundary

**11/11 technical packets reconciled; 5 historical holds and 6 technical quarantines preserved; 33 pair records checked; 0 new human attestations; 0 releases; 0 newly eligible scoring images.** This work does not certify source independence. Those eight unresolved cases remain held for any future acquisition-independent source-family claim. Under V31-A3, they are **not a blocker** to the narrower author-annotation-backed internal image-level detection analysis; no further site/project mapping or full-corpus reinspection is requested unless the research objective changes to independent site-level generalization. No model calls, Test access, original image reopening, dataset writes or repeated general image review occurred.


## V31-A1 — author confirms the shared School 22 May site (22 November 2026)

The dataset author answered **“نعم”** to the specific question whether Valid `IMG-20250416-WA0063.jpg` and `IMG-20250416-WA0051.jpg`, together with Train `IMG-20250416-WA0067.jpg` and `IMG-20250416-WA0066(1).jpg`, belong to the same **مدرسة 22 مايو – عصيفرة** construction project/site, even if photographed at different times or angles.

This is recorded as `SHARED_CAPTURE_SESSION_OR_SITE`, site-family ID `site_school_22may_aseefrah`, for the two Valid members. It is a site/project-family decision only: no same-frame or same-capture-session claim is made, and no session ID is invented. The exact chat response is preserved in [the author evidence record](evidence/AUTHOR_CHAT_ATTESTATION_SCHOOL_22_MAY_ASEEFRAH_2026-11-22.md), SHA-256 `326c7ad0347a86822768e4f1703045248247bc3014cd5ccb139148332cc07605`. The two per-image decisions are in [the V31-A1 machine record](V31_A1_AUTHOR_SITE_ATTESTATION_2026-11-22.json) and [human-readable report](V31_A1_AUTHOR_SITE_ATTESTATION_2026-11-22.md).

**Result:** 2 of the 11 P0 Valid cases now have author-attested shared-site verdicts; both remain hard-held because Train contains the same site. The other 3 historical holds and all 6 technical quarantines remain blocked. There are **0 independent-source attestations, 0 newly eligible Valid images, and 0 signed Valid Person–PPE gold cases**. The cohort remains `scoring_ready=false`. [V31-A1 validator](tools/verify_v31a1_author_site_attestation.mjs) checks the evidence SHA and rejects mutations that would invent a capture session, erase Train overlap, or release a hold. It passed [source/reference CI #44968818900](https://github.com/EZZALDEEN049/Y-PPE-Detection-RFDETR/actions/runs/44968818900) and [public engineering CI #44968818901](https://github.com/EZZALDEEN049/Y-PPE-Detection-RFDETR/actions/runs/44968818901).

## V31-A2 — author confirms WA0026/WA0079 shared scene with modifications/processing (22 November 2026)

The author clarified that Valid `IMG-20250416-WA0026.jpg` and Train `IMG-20250416-WA0079.jpg` are not the same presented image, but represent the same scene with changes and processing. The relationship is recorded as `SHARED_SCENE_WITH_MODIFICATIONS_OR_PROCESSING`, scene-family ID `scene_wa0026_wa0079_modified_processed`. The record does not assert byte identity, exact original-frame identity, crop lineage, a site ID for Train WA0079 or a common capture session.

See the [verbatim author evidence](evidence/AUTHOR_CHAT_ATTESTATION_WA0026_WA0079_SHARED_SCENE_2026-11-22.md), [machine record](V31_A2_AUTHOR_SHARED_SCENE_WA0026_WA0079_2026-11-22.json), and [human-readable report](V31_A2_AUTHOR_SHARED_SCENE_WA0026_WA0079_2026-11-22.md). WA0026 remains hard-held; no independent-source eligibility is created. The [V31-A2 validator](tools/verify_v31a2_author_shared_scene.mjs) and mutation tests are included in the source/reference workflow.

## V31-A3 — aggregate dataset provenance and completed original curation accepted (22 November 2026)

The author states that the corpus was assembled from multiple projects and work locations in Yemen associated with civil-society organization projects, for PPE/occupational-safety analysis and practical solution development. The author also confirms that image review and curation were completed during the original database-preparation phase, consistent with the existing V18 single-curator policy.

**Methodological decision:** a per-image project/worksite ID is not required for internal image-level detection analysis because site identity is not the study's outcome or sampling stratum. The corpus is described at aggregate multi-project/multi-location level. No repeat full-corpus review is requested. The absence of a complete per-image site/session register is disclosed; `SOURCE_UNKNOWN` is not relabelled independent.

This does **not** remove cross-split leakage controls. Three Valid relationships are now author-confirmed non-independent (two shared-site and one shared-scene-with-processing); eight P0 cases remain unresolved and held. Internal image-level detection analysis may use exact Source-ID/label/prediction joins and the frozen M0=459, M1=448 and M2=367 overlap-risk sensitivity cohorts. None is described as acquisition-independent or as proving site-independent generalization.

See the [V31-A3 decision](V31_A3_DATASET_LEVEL_ACQUISITION_CURATION_2026-11-22.md), [machine record](V31_A3_DATASET_LEVEL_ACQUISITION_CURATION_2026-11-22.json), and [SHA-pinned author evidence](evidence/AUTHOR_DATASET_LEVEL_ACQUISITION_AND_PRIOR_CURATION_2026-11-22.md). The [V31-A3 fail-closed verifier](tools/verify_v31a3_dataset_level_acquisition_curation.mjs) protects the aggregate-provenance decision and the no-hold-release boundary.