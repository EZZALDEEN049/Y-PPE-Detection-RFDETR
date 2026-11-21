# SEER-PPE V30 — frozen progressive XAI and deletion/insertion AUC protocol

**Frozen: 22 November 2026, before V30 model inference.** V30 converts the existing single-step V27/V28 perturbation probes into target-specific grid attribution maps and progressive deletion/insertion curves. This is a development-exposed engineering pilot, not an independent validation or worker-safety efficacy study.

## 1. Frozen sample and model

- Reuse the exact ten unique A5/A6 target detections in `V27_FROZEN_TARGETS_2026-11-21.json`, with the archived V28 baseline geometry/confidence joined by target ID.
- Ten target detections occur in **eight target-bearing original images** (four Train and four Valid). The ninth V27 image had no A5/A6 PPE target and is not given an invented target or curve.
- A5 and A6 retain eight selected slots each: six shared targets, two A5-only targets, and two A6-only targets. Shared target outputs are computed once and reused across both arms.
- Model: original hosted RF-DETR Small `altayyar-0oflt-lafos-qqauz/2`; confidence 0.20; overlap/NMS 0.50. No retraining, fine-tuning, endpoint replacement, Dataset upload, or Workflow sink is part of this protocol.
- All eight images were already development-exposed. The four Valid images are not a source-independent or untouched validation cohort. No Test image is included.

## 2. Baseline reproduction gate

Before perturbation, run one original-image inference for each of the eight images. This baseline gate was executed through the connected Roboflow inference integration on 22 November 2026 and is archived in `V30_BASELINE_PREFLIGHT_ACTUAL_2026-11-22.json` (8/8 images and 10/10 targets reproduced exactly). The local runner reuses this recorded baseline rather than spending eight duplicate calls. For every frozen target:

1. Match the same exact class to the frozen original box at IoU >= 0.50.
2. Require one unique match; if the match is missing or ambiguous, stop before the perturbation stage.
3. Require current confidence to be within 0.08 of the archived V28 baseline confidence.
4. Use the current verified confidence with the frozen V27 target geometry as the V30 reference score.

No thresholds may be widened after observing an outcome.

## 3. Target-specific attribution map

For each of the eight images, generate a fixed **8 × 8 grid** (64 cells). Each cell is replaced individually with RGB gray (127,127,127), and the unchanged detector is run once. The resulting prediction list is reused to score every frozen target in that image, avoiding duplicate inference for targets sharing an image.

For each target and cell:

- Score = confidence of the unique same-class detection whose box has IoU >= 0.50 with the frozen target box.
- If no same-class target match remains, the target score is **0 by the pre-defined detection-score convention**; record status `LOST`.
- If multiple matches are ambiguous within an IoU margin of 0.03, the score is missing; record `AMBIGUOUS` and do not impute it.
- Cell importance = verified baseline target confidence minus the perturbed target score. Preserve negative values in the map.
- Rank cells by descending positive score drop; resolve ties row-major. If any cell is ambiguous, or no positive drop exists, the target map is not rankable; record explicit null curves for that target and continue with other targets. If the fully blurred endpoint is ambiguous, also skip that target's curves and record the reason.

This is a black-box grid occlusion-sensitivity map, not Grad-CAM, SHAP, D-RISE, a human explanation ground truth, or an internal-feature attribution. The single-cell gray perturbation used to form the map is intentionally different from the blurred baseline used for progressive curves.

## 4. Progressive deletion and insertion

Construct one blurred baseline per image using Gaussian blur with radius `max(3 px, round(1% of the shorter image edge))`.

For each of the ten target IDs, evaluate three deterministic region orders:

1. `saliency`: descending positive occlusion score drop.
2. `random`: one reproducible random permutation seeded from SHA-256 of the frozen target ID.
3. `inverse_saliency`: reverse of the saliency order.

For each order, run both directions at 0%, 10%, ..., 100% of grid-cell area:

- **Deletion:** begin with the original image and replace the highest-ranked cells progressively with the corresponding blurred-baseline pixels.
- **Insertion:** begin with the blurred baseline and progressively restore the highest-ranked cells from the original image.

The x-axis is the **actual modified pixel-area fraction**, not the nominal step percentage. At the original-image endpoint use the verified baseline confidence; at the fully blurred endpoint use one shared blurred-image inference per image. Intermediate points use real original-model inference.

Normalize each target confidence as `clip(confidence / verified_baseline_confidence, 0, 1)` for AUC, while retaining the unnormalized confidence in the output. A lost target contributes zero. An ambiguous match makes that curve's AUC unavailable; do not replace it with zero or drop the point.

Compute trapezoidal AUC over actual pixel-area fractions:
- Lower deletion AUC indicates faster loss of the target score as highly ranked evidence is removed.
- Higher insertion AUC indicates faster recovery as highly ranked evidence is restored.
- Compare saliency against the fixed random and inverse-saliency controls.

## 5. Frozen inference budget

| Component | Calls |
|---|---:|
| Original-image baselines: 8 images | 8 |
| Fully blurred endpoints: 8 images | 8 |
| Single-cell grid occlusion: 8 images × 64 cells | 512 |
| Intermediate curve points: up to 10 targets × 3 orders × 2 directions × 9 interior steps | up to 540 |
| **Maximum original-model calls** | **1,068** |

The 0% and 100% endpoints are shared and are not re-inferred per ordering. The maximum is 1,068 calls **including the eight baseline calls already completed**. The remaining execution maximum is 1,060 calls: eight blurred endpoints, 512 grid-map calls, and up to 540 curve-intermediate calls. Each curve-eligible target adds 54 intermediate calls. If a target map or blurred endpoint is unrankable, its curves are skipped and the actual call count is lower. The runner reuses the archived baseline preflight, checks the exact remaining-call formula, and never exceeds the total maximum. An explicit command-line confirmation of the total 1,068-call budget is required before the full run. No additional inference is authorized by this frozen protocol.

## 6. Scoring and reporting

- Report all ten target maps, all 64 cell outcomes per target, all curve points, match statuses, and AUC values or explicit nulls.
- Report A5 and A6 with eight selected slots each. Because six target outcomes are shared, they are not independent observations. Report shared-target paired differences separately from arm-unique targets.
- Report per-target values and descriptive arm means. With ten unique targets and development exposure, do not claim statistical superiority, independent generalization, or safety benefit.
- A5/A6 comparison is on explanation sensitivity and curve behavior only; it is not a comparison of worker compliance or PPE mandate decisions.

## 7. Reproducibility, privacy, and hard limits

- The runner reads local copies of the eight original images and writes only numeric outputs plus SHA-256 image hashes. It does not save image bytes or time-limited image URLs.
- Original image files, annotations, dataset splits, and model weights remain read-only.
- No Test access, worker/task mandate adjudication, human review, person-level compliance outcome, physical Joules, or process-memory measurement.
- Source-family independence remains unverified; strict worker-safety `scoring_ready=false` remains unchanged.

## 8. Execution

From the repository root, place the eight exact original images in a local folder (do not commit them), install the repository requirements, and set `ROBOFLOW_API_KEY` in the local environment.

First validate local inputs without inference:

```bash
python research/seer-ppe/tools/run_v30_progressive_xai.py --images-dir /path/to/original_images --dry-run
```

Then run the eight-image baseline reproduction gate (eight model calls only):

```bash
python research/seer-ppe/tools/run_v30_progressive_xai.py --images-dir /path/to/original_images --preflight-only --output /tmp/v30_baseline_preflight.json
```

Only after reviewing that baseline output, execute the frozen full budget:

```bash
python research/seer-ppe/tools/run_v30_progressive_xai.py --images-dir /path/to/original_images --confirm-model-call-budget 1068
```

The full run writes `research/seer-ppe/V30_ACTUAL_PROGRESSIVE_XAI_RESULTS_2026-11-22.json`. Commit that result only after checking its call count, all target IDs, curve completeness, and ambiguity records. Do not edit the frozen protocol or target manifest to accommodate an inconvenient result.


## 8. Execution status addendum — 22 November 2026

- The connected Roboflow integration executed the eight original-image baseline inferences using model `altayyar-0oflt-lafos-qqauz/2`, confidence 0.20 and overlap 0.50.
- All eight source images resolved to their frozen Asset Library IDs, splits, filenames and dimensions.
- All ten frozen target detections reproduced with exact class, bounding-box geometry and confidence. No baseline mismatch was observed.
- Inference IDs, per-image prediction counts, timings and target detection IDs are archived in `V30_BASELINE_PREFLIGHT_ACTUAL_2026-11-22.json`.
- These eight calls count toward the 1,068-call V30 total. The local runner reuses this record, leaving a maximum of 1,060 additional calls.
- Progressive occlusion maps, deletion/insertion curves and AUCs have **not** yet been executed. Local source-image byte hashes remain to be computed after the user downloads the exact eight Asset Library sources; they are not compared to a source hash in the connector record.
