# V40 — Colleague reviewer 1 response and implementation record (AI-01–AI-10)
Date: 2026-11-24. Scope: pre-submission scientific review, not official journal peer review. No new inference, model training, data modifications or package export.

| ID | Decision | Action implemented and residual scientific limitation |
|:--|:--|:--|
| AI-01 | Accept limitation; defer new experiment | Abstract, discussion, conclusion and cover letter explicitly restrict claims to one fixed RF-DETR Small checkpoint. A second detector would test external architecture validity, but is not required to answer the narrow within-detector question. Architecture generalization remains untested. |
| AI-02 | Accept in part | Added primary D-RISE (Petsiuk et al., 2021, DOI 10.1109/CVPR46437.2021.01128) alongside D-MFPP (Andrés et al., 2024, DOI 10.1016/j.rineng.2024.103498). Clarify random evaluation order is not D-RISE/D-MFPP and neither was executed. Direct benchmark remains absent; a fair comparison needs predeclared matched targets, comparable scoring, mask budget and evaluation perturbations, not rebranding existing controls. |
| AI-03 | Accept | Retain original development-exposed cohorts and protected Test boundary. Explicitly conditional internal diagnostic, no independent-site claims. No independent sample added. |
| AI-04 | Accept and strengthen with archived evidence | Methods 2.8, abstract, Highlights, conclusion, S2 and cover letter clarify eligibility/selection bias. Frozen manifest confirms 225 eligible source images of 459 after screening/exclusions, 24 chosen, 48 targets, 11 categories. Archived baseline confidence min/median/max 0.5958752036094666 / 0.8463311791419983 / 0.9324679970741272; reference IoU 0.5267235188998202 / 0.7889154806374162 / 0.9464412864211136. All 48 manifest target IDs match audited result rows in order. These are reference-matched detections, not independently validated ground truth. No claims about missed objects or all detection outcomes. |
| AI-05 | Accept | Abstract, Highlights, cover letter and discussion identify sensitivity-vs-random comparison as internal non-independent response diagnostic; no independent attribution fidelity claim. Preserve all 264 AUCs and original evaluation design. |
| AI-06 | Accept and strengthen with archived evidence | Exact reviewer-proposed zero-score definition inserted in methods and limitations. Original gray maps have 45 LOST and 7 AMBIGUOUS out of 3072 fine target-cell records; 52 LOST and 6 AMBIGUOUS out of 768 coarse records. Descriptive LOST proportions 1.46% and 6.77%. Counts do not identify reason for non-match, distinguish internal scores from thresholded detections, or establish threshold effect. Lower-threshold replay not performed; no imputation or rethresholding. |
| AI-07 | Accept limitation | Discussion distinguishes offline numerical reproduction from future hosted inference reproduction; no weight availability or immutable provider environment promised. End-to-end reproducibility remains conditional. |
| AI-08 | Accept | Retain separation of historical PNG and extension JPEG 95/4:4:4 cohorts; explicit inability to isolate encoding effect from sample selection. Controlled encoding comparison not performed. |
| AI-09 | Accept limitation | Explicitly no independent human explanation/localization reference, no semantic correctness claim. No new human review of explanations. |
| AI-10 | Accept limitation; defer expanded grid experiment | Two evaluated resolutions only; no monotonicity or optimality conclusion. Additional resolutions would require new controlled experiment. |

## Technical evidence
Frozen manifest: research/seer-ppe/V38_B_FROZEN_CANDIDATE_SAMPLE_2026-11-23.json.
Audited per-target rows: research/seer-ppe/outputs/v38b_authorized_2026-11-23/V38_B_FINAL_NUMERICAL_RESULTS_SUMMARY_2026-11-23.json (blob f65cd9c0d91159fb47c1e73701ab7c97e8ecf006).
Score function: research/seer-ppe/seer_ppe/progressive_xai.py, target_score: MATCHED confidence; LOST 0; ambiguous None. Archived outputs cannot recover censored scores.
Primary D-RISE reference: https://openaccess.thecvf.com/content/CVPR2021/html/Petsiuk_Black-Box_Explanation_of_Object_Detectors_via_Saliency_Maps_CVPR_2021_paper.html
D-MFPP: https://doi.org/10.1016/j.rineng.2024.103498.

## Actual changes and checks
- Main manuscript commit 717bc8faa38e032c072365c3abe35a25558112f9.
- Highlights dfef26de499e3a2683bbaa0813a33a32ddbef2eb.
- Cover letter cbd44651d827a0f467f02c537a365f4e7577d57d.
- Supplement S2 a0395cf50224d6c32b376c04318be12dd493253d.
- Abstract 233 whitespace-separated words incl. labels, excluding keywords. Five Highlights lengths 77/78/72/76/76. Original manuscript and S2 table rows byte-equivalent. No new model calls; baseline numerical endpoints unchanged.
- At final packaging, regenerate Word/PDF and update Zenodo draft documentation (operational LOST definition, selection descriptors and archived counts), bibliography count and all verification manifests. Prior candidate ZIP is superseded for scientific content but retained as historical draft. Do not publish data or submit yet.

All ten comments addressed in writing or evidence; underlying limitations are not claimed resolved by editing. New experiments would require separate prospective design and explicit authorization. Maintain existing ethics, rights, archive and author approval holds.
