# Stage 11 — Consolidated Response to Q1-Style Major Revision

This document maps the major reviewer concerns to the concrete revision action and current status.

| Reviewer concern | Revision action | Evidence / file | Status |
|---|---|---|---|
| Possible duplicate / near-duplicate train-test leakage | Performed exact SHA-256, perceptual/geometric, manual scene-dependence audit; froze strict and conservative test-only sensitivity subsets; reran evaluation without training | `STAGE11A_FULL_AUDIT_REPORT.md`, `stage11a_full_audit_summary.json`, sensitivity outputs | **Closed** |
| Safety-class cross-domain claim confounded by near-floor Construction-PPE in-domain recall | Rewrote Abstract, Results, Discussion, and Conclusion to separate in-domain class learnability from additional transfer degradation | `MANUSCRIPT_STAGE11G.md`, `STAGE11B_INTERPRETATION_REVISION.md` | **Closed** |
| Training recipe may be responsible for apparent domain shift | Froze a validation-selected `best.pt` sensitivity protocol using the existing six completed runs; no retraining or threshold tuning | `STAGE11D_BEST_CHECKPOINT_SENSITIVITY_PROTOCOL.md`, notebook + evaluator | **Pending GPU execution** |
| Harmonization/filtering rule not reproducible | Added exact 9-class map, IoU >= 0.50 OR excluded-box containment >= 0.80 rule, critical class relationships, mixed-label handling, pseudocode, split exclusions, reason counts, class support before/after, selection-bias statement | `STAGE11C_HARMONIZATION_FILTERING_REPRODUCIBILITY.md`, expanded Supplementary Methods | **Closed** |
| Ground-truth-based test membership can create selection bias | Explicitly define the final benchmark as the predeclared structurally harmonizable subset; disclose original→filtered counts and limitation | Methods, Supplementary S2.8, Limitations | **Closed** |
| Only mean ± seed SD; insufficient uncertainty analysis | Added image-cluster bootstrap for safety recall and consensus FN; froze separate inference-only mAP bootstrap because exact AP cannot be reconstructed from object counts | Stage 11E / 11E2 files | **Safety outcomes closed; mAP CI pending GPU execution** |
| Consensus across seeds could be misread as independent confirmation | Reworded throughout as persistence under training stochasticity, not independent replication | Results 3.4, Supplementary S5 | **Closed** |
| Supplementary Methods too weak | Expanded with full harmonization/filtering pseudocode, exact Ultralytics config, seed handling, fixed-point TP/FP/FN matching, consensus algorithm, per-seed 12-cell results, dependence audit, bootstrap, fingerprints | `SUPPLEMENTARY_METHODS.md` | **Closed** |
| Data/code availability contains internal placeholder language | Replaced with public repository URL, Stage 11 branch, fingerprints, and plan to pin final immutable commit/tag only after pending inference checks | `MANUSCRIPT_STAGE11G.md` | **Closed pending final tag** |
| Figure numbering mismatch | Frozen final Figure 1–6 manifest and corrected generation/naming plan | `FIGURE_MANIFEST.md` | **Closed** |
| Literature review too sparse and novelty framed as combination novelty | Added highly relevant 2024 Automation in Construction domain-adaptation study, 2026 Cross-HNM, PPE adaptation, DG/distribution-shift literature; reframed gap as reliability evaluation rather than first/novel combination | `STAGE11F_LITERATURE_NOVELTY_MATRIX.md`, Related Work | **Closed** |
| Cover letter/highlights overstate reverse-direction safety failure as domain shift | Rewritten to reflect asymmetric evidence and Stage 11A sensitivity result | `COVER_LETTER_DRAFT.md`, `HIGHLIGHTS.txt` | **Closed** |
| Ethics/image-use placeholder not suitable for final submission | Removed unsupported approval placeholder; retained only source-supported governance wording and clearly separated public platform license metadata from undocumented institutional redistribution authorization | `MANUSCRIPT_STAGE11G.md`, `DECLARATIONS_TO_CONFIRM.md` | **Closed as wording; documentary confirmation remains author-controlled** |

## Current scientific submission gate

Two analyses remain before the final immutable submission freeze:

1. **Stage 11D — best.pt checkpoint sensitivity**
2. **Stage 11E2 — image-level mAP50:95/domain-gap bootstrap**

Both are inference-only. No new model training is required.

Until both are complete, the manuscript status remains **SUBMISSION HOLD** rather than submission-ready.
