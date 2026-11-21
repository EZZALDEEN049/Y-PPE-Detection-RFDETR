# V19 — verified successful original-annotation box matching and computational source sensitivity

Date: 21 November 2026. GitHub Actions run [44853282012](https://github.com/EZZALDEEN049/Y-PPE-Detection-RFDETR/actions/runs/44853282012) **completed/success**; its fail-closed synthetic checks, actual read-only original Train object-box matching, direct technical Valid risk stratification, and numeric archives passed.

## Original single-curator labels versus original detector boxes

Four source Train original images: 48 saved object labels, 51 existing RF-DETR original detections, IoU=0.50, hosted confidence floor 0.20. **TP=47, FP=4, FN=1**. Precision **0.921569**; recall **0.979167**; F1 **0.949495**. Seven source boxes carry old model-assistance provenance markers in B; dropping the *entire* B sample yields 33 originals, 35 detections, TP 32, FP 3, FN 1. No source boxes or person-level decisions were changed.

The AP50 and AP50–95 metadata saved in the archive are **above-0.20 truncated AP proxies** on four reused Train images, not full COCO mAP and not generalization estimates. A negative PPE class means a bounding-box category, never an independently verified occupational violation.

## Source-overlap stratification

Existing 459 original Valid→Clean17 photo mappings; 280 direct Train–Valid candidate comparisons; 12 flagged high-similarity pairs; eight technical graph components. Computational descriptive scenarios M0 459, M1 448 excluding 5+6, M2 367 excluding additional 81. Zero source independence certifications are fabricated; no third-party or fresh human review requested.

## Strict nonclaims

No new hosted RF-DETR inference, no Validation performance, no Test inspection, no changes to original model or dataset, no independent safety/energy/XAI measurement, no compliance or false-clearance outcomes. Historical same-dataset Train reference and seven source `labeledByModel` flags are documented. Strict safety/source-independent evaluation remains `scoring_ready=false`.

Artifacts: [Train source annotations](TRAIN_ORIGINAL_SOURCE_ANNOTATIONS_READONLY_V19.json), [Train numeric result](TRAIN_SOURCE_LABEL_DETECTION_NUMERIC_PREFLIGHT_V19.json), [Valid overlap report](VALIDATION_SOURCE_OVERLAP_NUMERIC_SENSITIVITY_V19.json), [protocol](V19_AUTHOR_ANNOTATION_NUMERIC_EVAL_PROTOCOL.md).
