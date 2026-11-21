# SEER-PPE V27 — frozen targeted box-occlusion XAI and class-error-calibrated selective comparator

**Frozen before V27 perturbation inference, 21 November 2026.** This is an actual black-box, bbox-guided perturbation study on the exact nine development images and selected PPE detections already used in V25. It does not retrain, edit, or replace the original RF-DETR Small model, original labels, or dataset splits. It does not access Test.

## 1. Fixed sample and pre-existing targets

Reuse exactly the nine images already used in V25: four original Train images A/B/C/D and five original Source Valid images selected before V23 model prediction. The set contains 74 original fixed-model detections, including 59 typed PPE cues, 10 person candidates and five context detections. All nine images are development-exposed; the five Valid images have prior model development and V23 pilot exposure. No independent acquisition or generalization claim is permitted.

- Train: `image_604.jpg`, `000760.jpg`, `Kathiah Gets a Chance03.jpg`, `h1.jpg`.
- Valid: `image_1282.jpg`, `5731201_4.jpg`, `c1e5a26df8225afb5be5beceae128ad5.jpg`, `imagem40.jpg`, `a16ea468abd845e68ea9ccbbe4f9762e.jpg`.
- Source identity is fixed by the Roboflow Asset Library IDs in `V27_FROZEN_TARGETS_2026-11-21.json`. Image URLs are retrieved read-only at execution and are not saved to GitHub.

The V25 A5 policy and its A2 confidence-only reference targets are preserved. The V27 primary comparison is **A5 versus A6**, a stronger proposed error-calibrated selective baseline. A2 is retained only as a historical weak reference, not as the primary competitor.

## 2. A6 comparator frozen before perturbation outcomes

A6 is a class-error-calibrated selective review priority, using only V25 detector features and class-level current-reference calibration from V26. For every typed PPE detection:

`A6 = 0.50(1 - confidence) + 0.30 FDR(class) + 0.20 U_association`

- `FDR(class) = FP/(TP+FP)` from V26's current-author-reference **M0 minus the five V23 pilot images** (454 other original Source Valid images).
- `U_association=1` for `ASSOCIATION_AMBIGUOUS`, `ASSOCIATION_UNKNOWN`, or `PERSON_CANDIDATE_NOT_DETECTED`; otherwise 0.
- Highest A6 score per image is selected; ties are broken by detection ID.
- No per-image GT, per-detection FP/TP outcome, or V23 matching error is used to select a target. The five V23 Valid images are excluded from the class-FDR calibration set. Calibration remains historically development-exposed and not source-independent.

A5 remains exactly the frozen V25 score: uncertainty + 0.26 negative-named cue + 0.24 unresolved association + fixed unvalidated severity proxy. A6 is not assumed superior; superiority must be earned by the measured outcomes.

## 3. Matched selection and review budget

Both A5 and A6 have exactly one selected explanation target and one proposed human-review slot per image when PPE cues exist; no-cue images select none. The human-review item is **not dispatched**. Each arm has eight selected target slots across the nine images, six shared targets and two image-level disagreements. The union contains ten unique target tests. Shared targets are tested once and the result is shared by both arms; disagreements receive one target test each. Thus the arms have equal per-image target capacity and the same XAI procedure.

The exact A2/A5/A6 selected detection IDs, classes, confidences, original pixel-coordinate boxes, arm membership and non-target controls are computed by `tools/build_v27_frozen_targets.mjs` and archived in `V27_FROZEN_TARGETS_2026-11-21.json`. This target manifest is frozen before V27 inference.

## 4. Actual XAI perturbation: detection-box guided occlusion

For each of the ten unique targets, execute the unchanged original model in a Roboflow Workflow:

1. Run `altayyar-0oflt-lafos-qqauz/2` on the original image using `roboflow_object_detection_model@v3`, custom confidence **0.20**, NMS overlap **0.50**, and Active Learning disabled.
2. Isolate exactly one target using exact class plus frozen original box geometry. Use `x_min/x_max/y_min/y_max` tolerances of `max(6 px, 1% of the smaller image dimension)`, `width/height` tolerances of `max(4 px, 25% of target dimension)`, and confidence tolerance ±0.08. If the filter returns zero or more than one detection, record target reproduction failure and stop that target; **do not widen thresholds after observing results**.
3. Apply `BlurVisualization@v1` to the target box only, with kernel size **51** and padding **5 px**.
4. Re-run the same unchanged model on the target-occluded image with the same confidence and NMS thresholds.
5. Where a non-overlapping different-class detection exists, use the pre-frozen control box, blur it with the identical settings, and re-run the same model. The control is the closest-area available different-class detection with IoU <0.01 and target intersection fraction <0.05. Its area ratio is retained; it is not assumed to be perfectly area-matched. Images without an eligible control remain target-only and are not assigned an invented control.

This is a **black-box, detection-box-guided occlusion sensitivity explanation**, not Grad-CAM, SHAP, an internal-feature attribution map, or a claim that the selected region contains all causal evidence. It tests whether the model's target-class detection relies on the selected region and whether that effect is more target-specific than blurring a non-target object.

## 5. Fixed outcome definitions

Match each perturbed model output to the original baseline target by **same exact class and original-box IoU ≥0.50**. For each target:

- `baseline_confidence`: the original unblurred matched target confidence.
- `target_occluded_confidence`: maximum same-class confidence at IoU ≥0.50 after blurring the target box; zero if no match remains.
- `control_occluded_confidence`: the same matched confidence after blurring the control box; null when no control exists.
- `target_confidence_drop = baseline - target_occluded`.
- `control_confidence_drop = baseline - control_occluded`.
- `specificity_margin = target_confidence_drop - control_confidence_drop`, only where a control exists.
- `target_detection_retained`: whether the same-class IoU≥0.50 match remains after target occlusion.

A positive target drop and positive specificity margin support local model reliance on the selected region in that image. They do **not** establish PPE compliance, a worker-specific violation, an injury-risk reduction, or complete explanation faithfulness. Report every per-target result, including nulls and failures; do not drop inconvenient cases.

## 6. Post-selection detector-error diagnostic

After all A5/A6 target IDs are frozen and selected, the five Valid target IDs may be joined to the already-existing V23 original-current-box TP/FP match ledger. This is a separate object-detection error-alignment diagnostic only. It must never be fed back into A5/A6 selection or used as a worker-safety label. The four Train images have no comparable independent current-reference outcome in this protocol.

## 7. Execution budget and reproducibility

Ten target workflows are planned. Each uses two original-model passes (baseline and target occlusion); seven also use one matched control-occlusion pass. **Planned total: 27 original-model inference passes**. No extra retraining, Test, new human review, dataset edits, or original-label changes. All model inference runs use the same Workflow execution path, model ID and settings.

Archive the exact target manifest, workflow specification template, each execution's compact numeric outputs, target/control match status, and deterministic scorer in GitHub. Do not save original pixels or time-limited image URLs. If a Roboflow Workflow filter cannot isolate one target, fail closed rather than substituting a visually guessed box.

## 8. Scientific limits

All nine images are development-exposed; the four Train images are training examples and the five Valid images were used in V23. The 454-image class-FDR calibration set is also historically development-exposed, even though it excludes the five V23 pilot IDs. The V27 sample is an engineering/faithfulness pilot, not an independent validation cohort. No human review is dispatched, no task-specific PPE mandate is adjudicated, no person-to-PPE relation is human-verified, and no worker false-safe-clearance endpoint is estimated. No physical energy in Joules is measured. Strict worker-safety `NOT_FROZEN/scoring_ready=false` remains unchanged.
