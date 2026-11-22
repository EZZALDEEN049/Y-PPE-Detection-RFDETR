# Internal peer review — Y-PPE Q1 manuscript v0.1

**Review date:** 22 November 2026  
**Basis:** uploaded `Y_PPE_Q1_First_Manuscript_Draft_v0.1.docx`, canonical master proposal v3.5.0, Q15 evidence checkpoint, researcher-supplied prior papers, and targeted publisher-level literature verification.

## Editorial decision

**MAJOR REVISION — NOT READY FOR SUBMISSION.** The manuscript is careful about separating historical, platform, and planned evidence. Its proposed error-focused evaluation may be useful. However, E1 has only partially advanced, E2 has not passed, and E3 has not started for an admissible common evaluation set. The Q1 publication gate remains **NO-GO**.

## Principal strengths

- Does not presume leakage or model superiority.
- Distinguishes object detections from worker-level compliance, legal conformity, and injury outcomes.
- Defines class-wise FNR and pooled FPPI as separate descriptive outcome domains.
- Prespecifies validation-only thresholds and paired/group-aware uncertainty.
- Acknowledges Q12 Option A and the unresolved No Safety Attire/Abaya semantics.
- Recognizes that a new comparison alone is insufficient to establish Q1 novelty.

## Major comments

1. **Update E1 status.** The v0.1 manuscript says no source-image audit has been completed. Q15 now records a technical audit over 2,093 Train/Validation images (1,625 Train; 468 Validation), with 760,500 cross-split comparisons, zero exact SHA-256 matches, zero decoded-RGB exact matches, no missing files or decode errors, and 46 dHash near-pair candidates involving 31 Validation IDs. The original Test bytes were not audited. Report this only as a partial technical screen, not a passed provenance gate.
2. **Do not transfer SEER-PPE V26 into Y-PPE results.** The 468-to-459 crosswalk remains provisional (`provisional_mapping_is_confirmed_image_identity=false`). The 459-row V26 output is RF-DETR-only, development-exposed Validation evidence; paired YOLOv11m geometry is unavailable, and stored predictions are truncated below confidence 0.20. Keep this evidence separate from Y-PPE Q1 claims.
3. **E2/E3 remain blocked.** Model IDs and platform records exist, but checkpoint binaries, full training histories, exact split identity, a common eligible roster, and paired predictions are unavailable. No Q5 threshold has been selected for both models from an admissible Validation set. Do not claim model superiority or independent-test performance.
4. **Clarify the historical operating point.** The prior comparison paper lists separate “optimal confidence” values for Validation and Test (YOLOv11m approximately 0.51/0.36; RF-DETRs approximately 0.48/0.46). The available text does not establish whether Test-specific values were selected using Test labels or shown descriptively. This is not proof of test leakage, but it must be disclosed as unresolved.
5. **Qualify historical training fairness.** The previous paper reports 300 epochs for YOLOv11m and 40 for RF-DETRs, managed optimizers/batches, dynamically allocated cloud GPU resources, and non-fixed random seeds. Do not describe it as a fixed-hardware or equal-compute training experiment. Q9's resource-budget disclosure is appropriate.
6. **Narrow the novelty claim.** Recent work already reports video-recording-disjoint PPE classification, repeated runs, validation thresholds and calibration (Buildings, 2026); multi-category PPE non-compliance detection and small-object sensitivity (Scientific Reports, 2026); and cross-site construction object detection (Automation in Construction, 2026). A 2026 PRISMA review also synthesizes PPE computer-vision evidence quality. Generic claims about leakage auditing, repeated training, thresholding, or class-wise errors are not novel by themselves.
7. **Keep metric sources separate.** Historical paper values differ from Roboflow overview/training/evaluation records. Do not average or merge them; preserve the exact source surface, metric label, split, and configuration.
8. **Resolve taxonomy before evaluation.** Verify the six candidate missing-PPE class indices and semantics against actual class files. No Safety Attire/Abaya remains unresolved.
9. **Respect the annotation constraint.** Under Q12 Option A, the existing annotations are not an independently validated gold standard. FNR/FPPI are errors relative to the available annotation reference, not real-world compliance error rates.
10. **Freeze the evaluator specification.** Before E3, document score filtering, prediction ordering, NMS/post-processing, class-exact one-to-one matching, box conventions, clipping, ignored regions, tie-breaking, and wrong-class overlaps.
11. **Correct the subtitle.** The v0.1 subtitle refers only to RF-DETR although the study compares RF-DETR Small and YOLOv11m. The revised subtitle should name both models. Keep “safety-relevant” bounded to annotated detection errors; no worker-level safety outcome is measured.

## Section-level actions

| Section | Required action |
|---|---|
| Cover/title | Name both models in subtitle; retain the approved project title with safety-outcome caveat. |
| Evidence note / Abstract | Add partial Train/Validation audit and state E1 partial, E2 not passed, E3 not started. |
| Introduction / Related Work | Add nearest 2026 studies; make author-publication overlap explicit. |
| Dataset/version | Separate raw 2,327-image/16,520-label inventory from the 2,288-image/16,300-label Clean17 derivative. |
| E1 | Report the 2,093-image audit, 760,500 comparisons, zero exact matches, 46 near-pair flags, and no Test audit. |
| E2 | Add Q9 three-run plan (seeds 11, 29, 47), bounded validation-only search, and compute-budget disclosure. |
| FNR/FPPI/Q5/Q7 | Retain separate endpoints and locked thresholds; fully specify deterministic evaluator; preserve pointwise-CI caveat. |
| Q14 | Keep apparent scale mechanically derived; FPPI remains image-level; exclude SEER RF-only table from Y-PPE results. |
| Results / Discussion | Separate historical paper metrics from platform records and the partial technical audit. |
| Limitations / Ethics | Add Test-audit, cross-track identity, checkpoint exposure, label validity, taxonomy, and rights limitations. |
| References | Complete authors/DOIs; add YOLO11 software citation and nearest 2026 literature; do not treat the preliminary proposal as a scholarly publication. |
| Appendices | Update gate table, renumber work plan, and explain why SEER-PPE V26 is excluded. |

## Bibliographic verification

- Thesis title page identifies Ezzaldeen Nabil Ghaleb Obadi Al-Tayyar, Taiz University, Faculty of Engineering and Information Technology, academic year 1447 AH / 2026 AD.
- DASA 2025 papers: DOI 10.1109/DASA68193.2025.11498849 and 10.1109/DASA68193.2025.11499131.
- eSmarTA 2026 comparison paper: DOI 10.1109/ESMARTA70636.2026.11652190.
- eSmarTA 2026 BIM paper: DOI 10.1109/ESMARTA70636.2026.11652079.
- RF-DETR reference should use the ICLR 2026 title and authors Isaac Robinson, Peter Robicheaux, Matvei Popov, Deva Ramanan, and Neehar Peri.
- Ultralytics states that YOLO11 has no formal research paper and provides a software citation for Glenn Jocher and Jing Qiu (2024).
- Add the 2026 Buildings, Scientific Reports, Automation in Construction, and Computers references.

## Required next steps

1. Complete E1: retrieve both exports into controlled storage, generate separate split manifests, compare exact image membership, adjudicate near-pairs, audit Test bytes, reconcile taxonomy/box conventions, and authenticate acquisition groups.
2. Verify or reject the provisional 468-to-459 crosswalk.
3. Complete E2: obtain authorized checkpoints and training provenance; audit holdout exposure; decide reuse versus retraining under Q9.
4. Freeze the evaluator.
5. Only after E1/E2 acceptance, generate paired full-confidence predictions, select thresholds on Validation only, and execute E3 with group-aware uncertainty.
6. Reassess novelty and journal readiness after the actual findings exist.

**Final recommendation:** accept v0.2 as an improved internal working draft only. Do not submit it. No training, inference, annotation, Test modification, or independent evaluation was performed during this manuscript review.
