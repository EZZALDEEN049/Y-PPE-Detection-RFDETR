# Stage 11 — Response to External Reviewer Critique

## Decision

The reviewer’s criticism is accepted in substantial part. Submission has been placed on **HOLD** until the leakage-safe / best-vs-last sensitivity run is completed.

## Comment 1 — Construction-PPE safety classes are already near floor in-domain

**Accepted.**

The manuscript will no longer interpret reverse-direction safety-class failure as primarily caused by domain shift.

The evidence is separated into:

- **Y-PPE → Construction-PPE:** clear additional cross-domain degradation because violation recall falls from non-trivial in-domain values.
- **Construction-PPE → Y-PPE:** violation classes are already near floor in-domain; these results primarily demonstrate poor class learnability under the completed Construction-PPE training protocol, with little room for additional measurable degradation.

The consensus false-negative analysis is retained as evidence of **failure persistence under training stochasticity**, not independent replication.

## Comment 2 — Training-protocol sensitivity

**Accepted.**

Saved validation trajectories confirm that the final epoch is not the best validation epoch:

| Run | Best validation mAP50:95 epoch | Best validation mAP50:95 | Epoch-100 validation mAP50:95 | Difference |
|---|---:|---:|---:|---:|
| Y_s17 | 54 | 0.27881 | 0.25961 | 0.01920 |
| Y_s42 | 38 | 0.27847 | 0.24846 | 0.03001 |
| Y_s2026 | 35 | 0.27379 | 0.25060 | 0.02319 |
| C_s17 | 9 | 0.26288 | 0.23670 | 0.02618 |
| C_s42 | 12 | 0.26626 | 0.23474 | 0.03152 |
| C_s2026 | 15 | 0.25313 | 0.22959 | 0.02354 |

Therefore the Stage 11 sensitivity run evaluates both `last.pt` and `best.pt` on the same leakage-safe held-out population.

No standard-augmentation retraining is added at this stage because the reviewer explicitly requested best.pt **and/or** standard augmentation; the best-vs-last check directly tests checkpoint-policy sensitivity without creating a new training family.

## Comment 3 — Novelty / research gap

**Accepted.**

Novelty is no longer stated as “domain shift has not been studied.”

The revised gap is:

> Existing construction-domain adaptation/generalization studies establish that visual-domain shift matters, but deployment-oriented PPE evaluation still does not adequately distinguish aggregate detector degradation from persistent failure of explicit safety-violation classes under frozen zero-shot transfer.

The manuscript will explicitly discuss the 2023/2024 Automation in Construction domain-adaptation studies and the 2026 Cross-HNM study.

## Comment 4 — Harmonization/filtering reproducibility

**Accepted and expanded.**

The exact structural match rule is:

- IoU >= 0.50 **OR**
- excluded-box containment >= 0.80.

Critical relationships:

- Y-PPE: Child vs Persons; No Safety Attire vs Persons; Soft Hat vs Hard Hat/No Hard Hat.
- Construction-PPE: none vs Person.

Final conservative image-membership rule:

> Exclude an entire image if it becomes empty after nine-class harmonization or contains at least one critical unmatched source annotation under the structural rule.

Final exclusions:

| Dataset | Train removed | Validation removed | Test removed | Total removed |
|---|---:|---:|---:|---:|
| Y-PPE | 359 | 103 | 48 | 510 |
| Construction-PPE | 31 | 2 | 3 | 36 |

For Y-PPE, the pre-correction audit contained 341 critical-unmatched images and 282 harmonized-empty images; because the categories overlap, their union is 510 images. The mutually exclusive totals are 228 critical-only, 169 empty-only, and 113 satisfying both conditions.

No model prediction was used for membership decisions, and held-out test pixels were not visually opened during the original Stage 4.5 membership adjudication.

## Comment 5 — Duplicate / near-duplicate leakage audit

**Accepted; audit completed.**

No exact SHA-256 duplicate pairs were detected, but a stricter perceptual/geometric audit detected high-confidence same-scene pairs across splits. The result is documented in `STAGE11_LEAKAGE_AUDIT_RESULTS.md`.

Because this can inflate in-domain performance, submission remains on hold until leakage-safe re-evaluation is complete.

## Comment 6 — Statistics

**Partially accepted.**

Seed-level SD will remain explicitly descriptive of training stochasticity only. The final manuscript will add binomial/proportion uncertainty for consensus-FN rates where appropriate and will avoid treating object instances as fully independent observations.

A full image-clustered bootstrap of AP is desirable but is secondary to correcting the more important leakage/checkpoint-sensitivity issues.

## Comment 7 — Supplementary Methods

**Accepted.**

The supplement is expanded with:

- exact harmonization mapping;
- structural exclusion rule and thresholds;
- exclusion flow/counts;
- full training configuration;
- evaluator thresholds;
- TP/FP/FN matching logic;
- consensus-FN definition;
- leakage audit method;
- full per-seed results location.

## Comment 8 — Data/code availability

**Accepted.**

The final manuscript will report a direct repository URL, frozen branch/commit, dataset fingerprints, and a release identifier. The previous internal wording about creating a release “if available” is removed.

## Comment 9 — Figure numbering

**Accepted.**

The final package will use manuscript-order filenames:

1. Figure_1_Experimental_Workflow
2. Figure_2_Semantic_Harmonization
3. Figure_3_Cross_Domain_mAP5095
4. Figure_4_Seed_Level_Domain_Gaps
5. Figure_5_Safety_Violation_Recall
6. Figure_6_Consensus_False_Negative_Rate

Result figures 3–6 will be regenerated after Stage 11 leakage-safe metrics are finalized.

## Comment 10 — Literature breadth

**Accepted.**

The related-work section is expanded to include construction-specific domain adaptation, domain generalization, few-shot/imbalanced detection, dynamic construction-site object detection reviews, and recent safety-monitoring studies.
