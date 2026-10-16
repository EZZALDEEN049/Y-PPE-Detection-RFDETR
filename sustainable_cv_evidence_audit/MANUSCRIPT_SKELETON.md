# Manuscript Skeleton v0.1 — NOT submission-ready

## Provisional title
**From Detection Accuracy to Deployability: Evidence Gaps in Existing PPE Detection Models for Resource-Constrained Environments**

## Design note
Focused transparency/provenance case-study. The argument is methodological: reported high detector accuracy is not proof of sustainable deployment. This is distinct from any study reporting new Y-PPE training, cross-domain YOLO11m degradation, or model superiority.

## Proposed abstract (draft)
Computer vision is increasingly proposed for occupational safety in resource-constrained environments, yet detection scores alone do not establish deployability, operational affordability or energy efficiency. We performed an evidence audit of two publicly available, previously trained PPE object detection tracks, YOLO11m and RF-DETR Small, linked to a localized worksite dataset. We extracted publicly reported accuracy values, model and dataset identifiers, available comparison controls, compute indicators, power measurements and field-readiness evidence, without new training. The model overview pages report mAP@50 values of 92.2% and 94.0%, respectively, but identical test-split membership and a common evaluator could not be established from the audited documentation. No controlled energy-per-image or matched-hardware inference measurements were established in this source audit. Accordingly, these results support descriptive reporting, not a controlled architectural ranking or a claim of greater environmental sustainability. We propose explicit evidence thresholds to guide a future no-retraining deployment benchmark.

**Status of this abstract:** Describes only documentary audit and evidence limits; not a novel generalizable empirical efficiency study. Re-evaluate novelty and journal fit after independent measurements.

## 1 Introduction
Occupational-safety vision systems and resource-constrained worksites. Distinguish detection accuracy from deployment and sustainability. Establish a verified literature gap after a structured related-work search, not an asserted first-in-literature claim.

## 2 Related Work
PPE detectors; transformer/CNN comparisons; energy-aware/edge AI benchmarking; transparent reporting; domain shift, false-negative risk. Cite the earlier Y-PPE and cross-domain work rather than republishing their results.

## 3 Methods
Case-study selection criteria and public artifact identity; extraction form; provenance hierarchy; comparison gates; missingness policy; no-accelerator reproducibility procedure.

## 4 Results — currently limited to documentary evidence
Table of platform-reported metrics with source links; audit of split identity and missing compute/energy evidence; no unsupported performance delta, confidence interval, energy saving or significance claims.

## 5 Discussion
What can be inferred, what cannot; conflicts between text claims and overview metrics; risks in low-connectivity deployment. Identify specific measurable extensions.

## 6 Limitations
N=2 model tracks, same source domain, data-family reuse, lack of independent inference, missing power data and external deployment evidence. A Q1 empirical submission is premature on the present evidence.

## 7 Future experiment
A matched hardware/common-held-out inference experiment on already trained downloadable model weights, if licensing and model access permit it. Document energy measurement instrumentation, images, repetitions and external-field safety errors before interpreting sustainability.

## Declarations
Ethics permissions/photograph rights and data governance: **to be verified**. Funding and conflict-of-interest statements: **not available in this audit**. Do not reuse prior declarations without checking applicability.
