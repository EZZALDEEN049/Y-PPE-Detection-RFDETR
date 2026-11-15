# Manuscript development and evidence checklist

**As-of:** 2026-11-15. This document is a public **outline/status**, not the full unpublished manuscript.

## Proposed title
*Trustworthy and Risk-Aware Vision Transformers for PPE Compliance Monitoring Under Domain Shift and Limited Data*

## Structured manuscript progress

| Manuscript element | Current status | Acceptance condition before submission |
|---|---|---|
| Title, motivation, abstract | Proposed / draft | Rewrite abstract once actual empirical estimates exist |
| Introduction and contribution hypotheses | Drafted | Verify narrow novelty claims against closest papers |
| Critical related work | Preliminary | Complete citation/source/DOI checks and journal quartile evidence by year/category |
| Formal problem: CLEAR/ALERT/REVIEW, FC/UC | Drafted | Validate label ontology, risk definitions, and independence assumptions |
| Frozen RF-DETR pipeline and score mapping | Hosted 17-class inference exercised on 48 public cross-dataset images; worker association remains a geometry-only diagnostic | Independent worker-level matching, duplicate handling, training-source overlap audit, and calibrated worker score |
| Visibility/shift-aware evidence gate | Proposed | Independent gate validation and ablations |
| Scarce-target-label calibration | Prototype, unit-tested | Real calibration, fixed thresholds, proper confidence correction |
| Data provenance and split design | Partial audit | Independent site/acquisition grouping, leakage and permission review |
| Baseline comparisons | Planned | Fair matched-review and matched-site experiments |
| Results | Exploratory image-level probe only (22/24 positive-stratum hits; 1/24 comparison-stratum label discordance at base cutoff) | Independent worker-level FC/UC risk, representative accepted-CLEAR risk, target-site calibration/test, and matched baselines |
| Discussion and limitations | Interpretive draft | Rewrite from actual results and failure cases |
| Conclusion | Prospective draft | No empirical superiority claims before results |
| Reproducibility / declarations | Partial | Code, exact model/dataset versions, checkpoints, ethics and permissions |

## Research questions
- RQ1: What happens to detection, decision calibration, and false-clearance risk under cross-dataset and independently verified cross-site shift?
- RQ2: At matched human-review budgets, does the proposed selective policy reduce false clearance compared with strong baselines?
- RQ3: What target-site violation-label budget supports prespecified risk thresholds, and when is the statistically justified action to abstain?
- RQ4: Which components contribute under occlusion, low image quality, and rare violation classes?

## Important scope distinction
The existing Roboflow RF-DETR Small model has **17 original categories**. The checked Y-PPE-h9 archive has **nine harmonized categories** from a separate previous experimental track. The two are not equivalent to one newly trained nine-class RF-DETR system.

## Subsequent methods change to incorporate into the manuscript
- The formal **UC risk** definition is expanded to include an erroneous **NOT_REQUIRED** routing of a true required-helmet violation, alongside CLEAR and UNDETECTED. This prevents false comfort from wrong site-policy assumptions.
- A versioned [research patch](software/patches/0002-separate-runtime-policy-and-ground-truth.patch) separates runtime site/task policy from independent GT labels and achieved **24/24 local tests** after patch 0001.
- A local working DOCX named `SRAC_PPE_Research_Manuscript_Working_v5_2026-11-10.docx` has been inspected. Its document metadata says v5, but its visible title page says Manuscript v4.0; its title-page status still mentions six smoke tests while Section 6.1 documents a 48-image probe. Reconcile these labels before freezing a revision. The full unpublished DOCX remains outside the public repository.

## Dataset scene overlap and protocol status update
- Follow-up pHash+manual review confirmed related train/test and train/validation images in the separately packaged nine-class ZIP, so the independence gate is **OPEN**. Quarantine is documented; full source-family re-freezing is still pending.
- [Split integrity gate](tools/group_independence_gate.py) and eight local synthetic tests have been added; no final field-site empirical tests have been completed.
- Local corrected risk integration package passes 19/19 tests; the [public patch](software/patches/0001-fix-coverage-denominator.patch) is documented but not merged into the archived original ZIP.

## 2026-10-29 methodological audit
- Strong 2026 overlaps established in [novelty audit](NOVELTY_AUDIT.md). Revise related-work comparison before empirical claims.
- Exact sample feasibility and a strict matched-review baseline protocol drafted in [experiment protocol](EXPERIMENT_PROTOCOL.md); neither constitutes an empirical result.
- [Data archive audit](DATA_AUDIT_2026-10-29.md) and [coverage metric bug reproduction](CODE_AUDIT_2026-10-29.md) added; the **v3 manuscript DOCX itself has not been revised by this GitHub-only update**.
- Before results are entered, patch the canonical risk evaluation code and freeze a context-adjudicated independent worker-level dataset.

## 2026-11-15 exploratory evidence and manuscript status

- Completed 48 hosted RF-DETR inferences on the public Construction-PPE test partition using the frozen 17-class model at confidence 0.25 / overlap 0.50. The sample was stratified by image-level labels (24 `Person + no_helmet`; 24 deterministic controls sampled from 103 `Person + helmet` images without `no_helmet`).
- Image-level `No Hard Hat` presence: 22/24 positive-stratum images at 0.25 (91.7%; nominal exact 95% CI 73.0–99.0%); 1/24 comparison images (4.2%; nominal exact CI 0.1–21.1%). The latter is label discordance, not a validated false-positive rate.
- Post-hoc filtering of the original 0.25 boxes: 20/24 positive images at 0.50 and 15/24 at 0.75; comparison stratum 1/24 at both. These values are descriptive only.
- Machine-assisted review suggested two positive examples were non-construction scenes and the discordant control may omit a bareheaded second person. No expert human adjudication was performed.
- Three crowded images: 10 predicted head-equipment boxes; 9 uniquely contained by one predicted-person box, 1 ambiguous, 0 unmatched under a top-40% geometry heuristic. Not a validated worker-association score.
- Cross-dataset only; no proof of independent construction sites or no training-source overlap. No worker-level PPE-required ground truth, calibration, FC/UC risk result, representative R_AC estimate, or matched baseline comparison exists.
- Public-safe detail: [15 November progress report](PROGRESS_UPDATE_2026-11-15.md) and [aggregate summary CSV](EXTERNAL_IMAGE_LEVEL_PROBE_SUMMARY_2026-11-15.csv).
- The local working manuscript is not uploaded to the public repository. Its filename/metadata/title-page version mismatch must be reconciled before freezing.

The public manuscript state is: **methods substantially drafted; exploratory image-level feasibility evidence recorded; worker-level risk-control evidence pending**. Full draft, confidential materials and unpublished detailed wording are intentionally omitted from this public repository.
