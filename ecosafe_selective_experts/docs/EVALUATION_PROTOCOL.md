# EcoSafe Selective Experts — Evaluation Protocol v1

## Study status

This extension reuses six completed YOLO11m detectors and does not retrain the detectors. The previous Stage 6 held-out evaluation remains baseline evidence. New scientific claims require per-image selective-inference evidence generated from the immutable checkpoints.

## Unit of analysis

The default unit is an image. If source metadata reveal video/session/site clustering, all confidence intervals must be recomputed with a cluster bootstrap and the image-level bootstrap becomes secondary.

## Development/calibration data

Router fitting, calibration, feature selection, and threshold selection must use only non-test development/calibration data. Existing held-out test labels must remain untouched until:
1. router features are frozen;
2. router fitting method is frozen;
3. safety margin delta is pre-specified;
4. threshold is frozen.

If the original validation split cannot be reconstructed byte-for-byte from the frozen dataset source, no held-out routing result should be reported until a defensible development split is recovered.

## Expert pairing

Pair experts by seed:
- Y seed 17 with Construction seed 17;
- Y seed 42 with Construction seed 42;
- Y seed 2026 with Construction seed 2026.

Run both directions:
- Y expert primary, Construction expert secondary;
- Construction expert primary, Y expert secondary.

This prevents cherry-picking one favorable seed or direction.

## Primary routing target

A frame is recovery-positive when the secondary expert reduces the primary expert's false negatives for the frozen safety classes:
- no_helmet;
- no_gloves;
- no_boots.

Matching is class-aware at IoU >= 0.50.

## Baselines

Required:
- primary expert only;
- secondary expert only;
- always run secondary after primary;
- random routing at matched escalation rate;
- raw-confidence threshold;
- logistic router using frozen lightweight features;
- oracle per-image expert selection as an upper bound.

Optional only after primary analysis:
- calibrated-confidence router;
- additional OOD/domain-shift features.

## Safety constraint

Threshold selection minimizes escalation rate subject to a pre-specified absolute violation-recall loss `delta` against the reference policy. No numeric delta is embedded in code or selected after test inspection.

## Sustainability claims

Before direct energy measurement:
- report escalation rate;
- report expected expert executions per image;
- call these compute proxies, not energy savings.

After a fixed-GPU confirmation:
- report latency and J/image for each expert and the selective pipeline;
- include router overhead;
- use the same GPU, software stack, image resolution, warm-up policy, and measurement window across policies.

## GO / MODIFY / NO-GO

- GO: per-image oracle demonstrates meaningful safety complementarity and a simple development-only router captures part of it at materially lower escalation than always-both.
- MODIFY: complementarity exists but a primary-first cascade is asymmetric; consider direction-specific routing or a domain classifier.
- NO-GO: oracle gain over the best single expert is negligible. Do not force a router contribution.
