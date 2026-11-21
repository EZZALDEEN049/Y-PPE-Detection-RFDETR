# SEER-PPE V27–V29 — actual perturbation and timing results (22 November 2026)

## Scope
Original hosted RF-DETR Small model altayyar-0oflt-lafos-qqauz/2; unchanged weights, dataset, labels and splits. No Test access. Nine development-exposed images, ten unique target boxes, five Valid images previously used in V23. These are engineering pilots, not independent validation or worker-level safety efficacy.

## V27 — Gaussian target-box occlusion
- 10/10 target filters and 7/7 control filters returned exactly one detection.
- 27 original-model passes: 10 baseline + 10 target blur + 7 control blur.
- 9/10 target detections lost; mean target confidence drop 0.622325.
- Mean control-region confidence drop 0.008304; mean target-minus-control specificity margin 0.616005.
- Mean Workflow wall-clock 2.9122 s (includes platform/network overhead).
- A5/A6 each selected eight target slots, six shared and two unique. Target loss was 7/8 in each arm; mean target drop 0.641018 (A5) versus 0.621806 (A6); mean specificity margin 0.645060 versus 0.615807.
- Post-selection V23 Valid detection ledger join: A5 4 TP/0 FP, A6 3 TP/1 FP across four selected Valid targets each. This is object-detection alignment only.

## V28 — one-step deletion and target-only insertion
- 10/10 target filters passed.
- Archived repeat: 30 passes; first 30-pass attempt had no persisted outputs and is excluded. Total actual V28 calls = 60.
- Black-fill deletion lost all 10 target detections; mean confidence drop 0.716721.
- Target-only insertion retained 7/10 detections; mean confidence 0.630300; mean confidence delta −0.086421; mean sufficiency ratio 0.704532.
- Three insertion failures were the three smallest boxes (0.011%, 0.025%, 0.102% image area); all seven retained boxes were at least 0.732%.
- Train D Hard Hat box covered 63.75% of the image and is the only case where V27 blur and V28 black deletion differed in target retention.
- A5/A6 each lost 8/8 after deletion and retained 6/8 in insertion. Mean deletion drop 0.759013 versus 0.739801; mean insertion ratio 0.757727 versus 0.758744.

## V29 — hosted timing
Ten sequential direct hosted inference calls on five images × two repetitions; zero request failures. Mean request round-trip 1.5206 s, median 1.469 s, range 1.383–1.835 s. No provider-reported server inference time was returned. This is not pure model latency.

## Resource and compute accounting
- V27: 27 model passes.
- V28: 60 actual passes (30 unarchived first attempt + 30 archived repeat).
- V29: 10 direct timing calls.
- Total: **97 actual model calls**, of which 30 V28 first-attempt calls have no persisted numeric outputs; 67 have archived result/metadata records.
- Roboflow workspace devices: 0. Process memory and physical energy in Joules were not exposed; financial credits/USD usage was not available through the connected workspace. No values are estimated.

## Scientific interpretation
These are local target-box perturbation sensitivity probes. V28 deletion is a one-step black fill, and insertion is a one-step target-only sufficiency test. They are not progressive pixel-ranked deletion/insertion curves, AUC, SHAP/Grad-CAM or validated explanation Faithfulness. No human review was dispatched, no worker/task mandate or compliance outcome was scored, and source independence is not established. The strict worker-safety gate remains NOT_FROZEN/scoring_ready=false.

## Reproducibility files
- [V27 frozen protocol](V27_FROZEN_TARGETED_OCCLUSION_AND_A6_COMPARATOR_PROTOCOL_2026-11-21.md)
- [V27 actual results](V27_ACTUAL_TARGETED_OCCLUSION_RESULTS_2026-11-22.json)
- [V27 A5/A6 comparison](V27_A5_A6_COMPARISON_2026-11-22.json)
- [V28 frozen protocol](V28_FROZEN_TARGETED_DELETION_INSERTION_PROTOCOL_2026-11-22.md)
- [V28 actual results](V28_ACTUAL_TARGET_BOX_DELETION_INSERTION_RESULTS_2026-11-22.json)
- [V28 A5/A6 comparison](V28_A5_A6_DELETION_INSERTION_COMPARISON_2026-11-22.json)
- [V29 frozen timing protocol](V29_FROZEN_HOSTED_INFERENCE_TIMING_PROTOCOL_2026-11-22.md)
- [V29 timing results](V29_ACTUAL_HOSTED_INFERENCE_TIMING_RESULTS_2026-11-22.json)
- [V27 scorer](tools/score_v27_actual_occlusion.mjs) · [V28 scorer](tools/score_v28_deletion_insertion.mjs)

**Next required:** full pixel-ranked explanation fidelity with progressive deletion/insertion curves, worker/task-level reference, actual review efficacy, independent-source validation, and metered memory/Joules on instrumented hardware. No Test or original-data/model changes.
