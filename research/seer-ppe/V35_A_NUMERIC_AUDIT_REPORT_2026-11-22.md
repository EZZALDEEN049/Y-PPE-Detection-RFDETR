# SEER-PPE V35-A — Final numeric reconciliation audit

**Date:** 22 November 2026  
**Scope:** V26 through V34-B, including the current canonical `MANUSCRIPT_MASTER.md` v0.36  
**Execution:** read-only inspection and independent arithmetic recomputation; **zero new RF-DETR calls**

## 1. Audit decision

**Numeric checks: PASS**

The numerical evidence reviewed in V26–V34-B reconciles with the committed primary ledgers and the corresponding manuscript tables/claims checked in this pass. No numeric correction to the manuscript is required from the V35-A checks.

The overall audit is recorded as **PASS WITH TWO NON-NUMERIC WARNINGS**:

1. V27 contains a start timestamp that is later than its finish timestamp.
2. The V34-B figure outputs exist in a duplicated nested directory; the two archived PDF copies have different Git blob IDs.

Neither warning changes the recomputed scientific metrics. Both should be resolved or explicitly documented before final document assembly.

The machine-readable record is [V35-A numeric audit JSON](V35_A_NUMERIC_AUDIT_2026-11-22.json).

## 2. V26 — all 459 current Source Valid images

The SHA-256 of the full 2.4 MB per-source result ledger was independently recomputed and **matches** the SHA-256 recorded in the compact summary:

`4f350874a049019fc26c9970576f33208f10805868ae2d616daac676b60bb76d`

The detailed ledger contains **459 unique Source IDs**, all in Valid, with no missing records. Their per-source aggregates reconcile exactly to M0: 3,471 current author boxes, 4,103 model boxes, 729 existing model-assisted annotation markers, TP=3,297, FP=806 and FN=174. All 17 per-class rows also reconcile to the compact summary.

| Cohort | Images | GT | Predictions | TP | FP | FN | Precision | Recall | F1 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| M0 | 459 | 3,471 | 4,103 | 3,297 | 806 | 174 | 0.803558 | 0.949870 | 0.870610 |
| M1 | 448 | 3,433 | 4,063 | 3,261 | 802 | 172 | 0.802609 | 0.949898 | 0.870064 |
| M2 | 367 | 3,049 | 3,618 | 2,894 | 724 | 155 | 0.799889 | 0.949164 | 0.868157 |

All three cohorts contain 17 unique class rows, with zero missing source IDs. Precision, recall and F1 recomputed from TP/FP/FN agree within the source's six-decimal rounding. The manuscript's three-cohort table and 17-class table match the compact summary.

The three prespecified sensitivity profiles also reconcile:

- Excluding the 13 current-vs-historical GT-count mismatch images: 446 images, 3,152 GT, TP=3,022, FP=658, FN=130, F1=0.884660.
- Excluding the five V23 pilot images from M0: 454 images, 3,448 GT, TP=3,275, FP=805, FN=173, F1=0.870085.
- Excluding those five images from M2: 362 images, 3,026 GT, TP=2,872, FP=723, FN=154, F1=0.867543.

**Interpretation limit:** all 459 sources were historically development-exposed; zero rows are certified as source-independent. M2 is unflagged under the recorded risk screen, not an independent external cohort.

## 3. V27–V29 — perturbation and timing

| Stage | Reconciled result |
|---|---|
| V27 | 10/10 target workflows completed; 27 model passes; 9/10 target detections lost after target-box Gaussian blur; mean target confidence drop 0.622325 |
| V28 | 60 actual passes: 30 archived repeat outputs plus 30 first-attempt calls with no persisted outputs; 10/10 detections lost after black-fill deletion; 7/10 retained after target-only insertion |
| V29 | 10/10 direct hosted requests; recomputed mean round-trip 1,520.6 ms, median 1,469 ms, range 1,383–1,835 ms |

The V27–V29 call count reconciles to **97 actual model calls**. The 30 unarchived V28 first-attempt calls remain in call accounting but are not treated as numeric observations. V29 does not expose provider-side inference duration, so its timing remains request round-trip rather than pure model latency.

### V27 timestamp warning

The V27 record states:

- Start: `2026-11-22T00:29:00Z`
- Finish: `2026-11-21T21:35:46.679Z`

This is chronologically impossible as labelled. Git history places the frozen V27 workflow specifications at **21:25:03Z on 21 November** and the actual result-file commit at **21:35:48Z**. The start value may be a UTC+03 local clock time incorrectly labelled UTC; if so, its likely UTC conversion would be **21:29:00Z on 21 November**. That conversion is an inference, not a verified execution timestamp. The raw evidence file has deliberately **not** been edited. Verify against the original execution log before making a correction.

## 4. V30 — 8×8 progressive perturbation

The V30 accounting reconciles as **8 archived baseline calls + 1,060 additional calls = 1,068 total calls**. All ten frozen targets were rankable, with 640 target-cell outcomes, 26 LOST cell outcomes, 60 eleven-point curves and 60 valid AUCs.

I independently recalculated all 60 trapezoidal AUCs from their recorded actual modified-area fractions. The maximum absolute difference from the archived values was **2.22×10⁻¹⁶**. The 8×8 importance maps also matched their cell-trial score drops exactly.

A5 and A6 each selected eight target slots, sharing six targets and having two unique targets each. Their archived mean saliency AUCs match:

- A5: deletion 0.496288; insertion 0.944195.
- A6: deletion 0.397182; insertion 0.871354.

These are overlapping, development-exposed target slots, not independent arms or a policy-superiority test.

## 5. V33-A and V33-B

**V33-A** is a post-hoc, zero-new-inference reanalysis of V30. The source V30 blob identity matches. Its 60 AUCs reproduce within 2.22×10⁻¹⁶. The six shared A5/A6 targets, conditional six-way reassignment diagnostics and leave-one-image-out summaries reconcile with the report. The single seeded random ordering and algebraically related inverse ordering remain correctly described as limited controls.

**V33-B** is the separate 4×4 experiment:

- 496/496 successful calls, zero failures or automatic retries.
- Ten targets, 160 cell trials, 17 LOST cell outcomes.
- Forty eleven-point curves; 39 valid AUCs and one null AUC for a documented ambiguous target match.
- Independent AUC recomputation maximum absolute error: 2.22×10⁻¹⁶.
- All map/trial score differences: zero.

The ambiguous deletion point was not imputed. Recomputed A5/A6 means match the saved summary when the null deletion AUC is excluded: deletion means 0.487529 (A5) and 0.415104 (A6), each over seven valid targets; insertion means 0.922048 and 0.848435, each over eight. The six shared-target means also match the manuscript: deletion 0.493773 over five valid curves and insertion 0.912089 over six.

The direction of saliency's advantage over one fixed random order agreed across resolutions in 6/9 comparable deletion targets and 9/10 insertion targets. This is partial, direction-dependent robustness, not resolution invariance.

## 6. V34-A and V34-B — spatial agreement and figures

V34-A's ten-target spatial statistics reconcile to:

- Mean Spearman `rho = 0.5415659` (median 0.5656452).
- Mean Kendall `tau-b = 0.4238765` (median 0.4383910).
- Mean top-four region overlap: **65%**.
- All ten target Spearman coefficients are positive; one target has zero top-four overlap.
- Exact map/trial difference is zero; maximum coarse/fine area-partition error is 6.94×10⁻¹⁸; zero new inference calls.

The V34-B manifest's ten target-level Spearman values, Kendall values and top-four overlap counts match V34-A **exactly**. The repository contains ten target PNGs, one summary PNG, an 11-page PDF, a metrics CSV, a JSON manifest and a figure-generation report. This is a rendering/reproduction result, not another inference experiment.

### V34-B duplicate-output warning

The expected output folder `figures/V34B_2026-11-22/` contains a second same-named nested folder `figures/V34B_2026-11-22/V34B_2026-11-22/`. Each location contains 15 files. Fourteen matching files have identical Git blob IDs, but the two PDF copies do not:

- Expected folder PDF blob: `90c9385329b840c96239f5a8a7b93d91c53a1470`
- Nested folder PDF blob: `e89154a6f5f16a0df3dd8d0fe664d43c02245b67`

The numerical manifest checks pass, but the canonical PDF should be selected before insertion into Word. Do not silently treat the two PDFs as byte-identical.

## 7. Final V35-A disposition

**Numeric reconciliation: PASS.** The checked V26–V34-B numeric values in the manuscript agree with their committed source ledgers. No detector rerun, Test access, retraining, image review or annotation change was needed.

**Open non-numeric items:** verify the V27 timestamp from primary execution evidence and select/canonicalize the V34-B figure directory/PDF. The complete bibliography and DOI audit remains V35-C; figure placement/captions remains V35-B; editable Word generation and layout QA remains V35-D.

**Next phase:** V35-B — select the canonical V34-B output set, integrate the ten target figures and summary figure into the manuscript, and add numbered captions plus in-text figure references.

---
*All conclusions are limited to image-level detector outputs and perturbation-response sensitivity. They do not establish worker-level compliance, causal explanation faithfulness, human-review efficacy, independent-site generalization or electrical-energy savings.*
