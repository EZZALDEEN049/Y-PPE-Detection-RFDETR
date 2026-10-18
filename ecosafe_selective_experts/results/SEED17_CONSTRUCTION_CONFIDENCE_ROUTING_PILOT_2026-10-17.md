# EcoSafe: fixed-threshold confidence routing — Construction development pilot

**Date:** 2026-10-17. **Scope:** 132 Construction-PPE-h9-v2 *validation* images, 98 safety GT objects, seed 17. No held-out evaluation, router training, checkpoint modification, power or CO2 measurement.

Two exact frozen last.pt checkpoints were used to export per-image predictions. A *descriptive, unselected* confidence-only routing rule was simulated:
- first run primary YOLO11m;
- compute `risk=1-max(primary safety-class predicted confidence)` from low-threshold exported predictions; if no safety detection, risk=1;
- escalate to secondary expert when `risk >= t`;
- after escalation, merge **both** experts by class-aware NMS (IoU 0.70). Without escalation, keep primary only;
- evaluate safety objects at operating confidence 0.25, class-aware matching IoU>=0.50.

This uses only primary predictions for the routing *decision*. Ground truth is used strictly to **evaluate** simulated policies and was not used to choose a routing threshold.

| Primary expert / threshold | Secondary use | Expert invocations per frame (proxy) | Safety TP/98 | Recall |
|---|---:|---:|---:|---:|
| Always both (joint NMS) | 100.0% | 2.000 | 13 | 13.27% |
| Y expert only | 0% | 1.000 | 7 | 7.14% |
| Y primary, t=0.50 | 75.0% | 1.750 | 9 | 9.18% |
| C expert only | 0% | 1.000 | 8 | 8.16% |
| C primary, t=0.50 | 94.7% | 1.947 | 13 | 13.27% |

At t=0.5 the Y-primary heuristic fails to retain the always-both safety recall (9 vs 13 objects). The C-primary version happens to retain all 13 but still invokes its secondary in ~95% of frames, limiting **expert-call proxy reduction**. The primary/secondary direction and number of FPs matter. This development-set result is not a prespecified non-inferiority finding, and the baseline recall is itself inadequate for a field-safety claim.

A matched-rate random-routing baseline is defined as an expectation, not simulated random outcomes. No threshold from this exploratory sweep has been frozen; development-only cross-fitting, stronger primary features, all three seeds/both domains and an external held-out test are required. The code for reproducible full-coverage private-chunk routing frontiers is `scripts/10_validation_routing_frontier.py`; current exploratory local CSVs remain private.

This is a **NO-GO for claiming confidence-only routing success on these pilot observations**. Not a NO-GO on all selective experts: more complete domain/seed evidence and a prespecified safety operating criterion are needed before that conclusion.

Measurements called "expert invocations per frame" are compute proxies, **not Joules or actual runtime measurements**.
