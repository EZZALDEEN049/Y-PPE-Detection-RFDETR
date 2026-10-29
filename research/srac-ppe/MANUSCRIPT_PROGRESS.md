# Manuscript development and evidence checklist

**As-of:** 2026-10-29. This document is a public **outline/status**, not the full unpublished manuscript.

## Proposed title
*Trustworthy and Risk-Aware Vision Transformers for PPE Compliance Monitoring Under Domain Shift and Limited Data*

## Structured manuscript progress

| Manuscript element | Current status | Acceptance condition before submission |
|---|---|---|
| Title, motivation, abstract | Proposed / draft | Rewrite abstract once actual empirical estimates exist |
| Introduction and contribution hypotheses | Drafted | Verify narrow novelty claims against closest papers |
| Critical related work | Preliminary | Complete citation/source/DOI checks and journal quartile evidence by year/category |
| Formal problem: CLEAR/ALERT/REVIEW, FC/UC | Drafted | Validate label ontology, risk definitions, and independence assumptions |
| Frozen RF-DETR pipeline and score mapping | Prototype/draft | Verified 17-class inference and worker association on real images |
| Visibility/shift-aware evidence gate | Proposed | Independent gate validation and ablations |
| Scarce-target-label calibration | Prototype, unit-tested | Real calibration, fixed thresholds, proper confidence correction |
| Data provenance and split design | Partial audit | Independent site/acquisition grouping, leakage and permission review |
| Baseline comparisons | Planned | Fair matched-review and matched-site experiments |
| Results | **EMPTY / pending** | Verified experiment outputs with uncertainty estimates |
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
- The **existing unpublished v3 DOCX has not been edited**. When editing it next, synchronize all equations, diagrams, evaluation counts, policy-unknown handling and software schema before journal submission.

## Dataset scene overlap and protocol status update
- Follow-up pHash+manual review confirmed related train/test and train/validation images in the separately packaged nine-class ZIP, so the independence gate is **OPEN**. Quarantine is documented; full source-family re-freezing is still pending.
- [Split integrity gate](tools/group_independence_gate.py) and eight local synthetic tests have been added; no final field-site empirical tests have been completed.
- Local corrected risk integration package passes 19/19 tests; the [public patch](software/patches/0001-fix-coverage-denominator.patch) is documented but not merged into the archived original ZIP.

## 2026-10-29 methodological audit
- Strong 2026 overlaps established in [novelty audit](NOVELTY_AUDIT.md). Revise related-work comparison before empirical claims.
- Exact sample feasibility and a strict matched-review baseline protocol drafted in [experiment protocol](EXPERIMENT_PROTOCOL.md); neither constitutes an empirical result.
- [Data archive audit](DATA_AUDIT_2026-10-29.md) and [coverage metric bug reproduction](CODE_AUDIT_2026-10-29.md) added; the **v3 manuscript DOCX itself has not been revised by this GitHub-only update**.
- Before results are entered, patch the canonical risk evaluation code and freeze a context-adjudicated independent worker-level dataset.

The public manuscript state is: **methods-ready, empirical evidence pending**. Full draft, confidential materials and unpublished detailed wording are intentionally omitted from this public repository.
