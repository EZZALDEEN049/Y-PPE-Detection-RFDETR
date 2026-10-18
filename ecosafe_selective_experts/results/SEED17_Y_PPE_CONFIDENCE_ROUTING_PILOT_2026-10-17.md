# EcoSafe: confidence-only routing on Y-PPE development validation (seed 17)

**Pre-test exploratory result, 2026-10-17.** Same 356 frozen Y-PPE-h9-v2 validation images, 345 critical-class ground-truth boxes, two exact seed17 pretrained last.pt weights, image-complete private prediction exports. No test image examined, no new detector/router training, no energy measurement.

**Decision score:** `1 - max(primary safety-class detection confidence)`, with 1.0 if no safety-class detections. Prediction export at conf 0.001; evaluation safety conf >=0.25, GT match IoU >=0.50. If escalated, class-aware joint NMS of **both** experts at IoU 0.70; otherwise primary alone. This study only *screens* candidate thresholds and does not freeze one.

| Policy (fixed t=0.50 unless noted) | Secondary invocation rate | Expert executions/image (proxy) | Safety matched TP/345 | Recall |
|---|---:|---:|---:|---:|
| Y expert alone | 0% | 1.000 | 106 | 30.72% |
| Both / always joint NMS | 100% | 2.000 | 106 | 30.72% |
| Y primary + confidence rule | 79.49% | 1.795 | 106 | 30.72% |
| C expert alone | 0% | 1.000 | 1 | 0.29% |
| C primary + confidence rule | 99.72% | 1.997 | 106 | 30.72% |

Important: **the single Y expert alone already matches every safety GT box that the concatenation oracle and the joint NMS can match on this development split**. Every escalation of C as a second expert therefore adds computation but zero matched safety TP here; at threshold 0.50, Y-primary escalation yields 37 FP vs 35 FP with Y alone. Its confidence-only selective escalation is dominated on this validation split.

Reversing direction makes Construction expert extremely weak (1/345). Escalating to Y almost every frame restores the Y recall, but is not a meaningful reduction from always-both. This is a *development-only negative finding about a simple heuristic*, not a universal impossibility result, statistically demonstrated carbon savings, or a frozen test policy.

Combining this result with Construction validation (seed17, 98 critical objects) supports **direction- and domain-dependent expert complementarity**, not guaranteed gains from ensembling. Complete paired outputs for seeds 42 and 2026, all validation domains, safe fusion implementation, independent final heldout evaluation, site-aware intervals and measured power remain mandatory before publication-level deployment or sustainable-compute claims.
