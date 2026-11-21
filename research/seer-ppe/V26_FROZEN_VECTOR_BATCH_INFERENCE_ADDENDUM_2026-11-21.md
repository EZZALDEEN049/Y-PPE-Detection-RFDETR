# V26 prescore execution-mode addendum — vectorized fixed-model read-only hosted inference

**Dated 21 November 2026, committed before any V26 bulk per-image reference scoring or M0/M1/M2 outcomes.** The original [V26 frozen original-source Valid protocol](V26_FROZEN_FULL_CURRENT_SOURCE_VALID_BBOX_PROTOCOL_2026-11-21.md) still binds 459 original Source IDs, 17 labels, IoU=0.50, confidence=0.20, overlap=0.50, current author GT and no Test/training/source modification.

The Roboflow connector's `models_infer` accepts **one** image per request. Its `workflow_specs_run` endpoint supports arrays of original image URLs as one vectorized call with a valid inline, side-effect-free Workflow spec. The validated minimal spec (no visualization/storage/routing/active learning actions) is:
```json
{
  "version": "1.0",
  "inputs": [{"type": "WorkflowImage", "name": "image"}],
  "steps": [{
    "type": "roboflow_core/roboflow_object_detection_model@v3",
    "name": "detect_original",
    "images": "$inputs.image",
    "model_id": "altayyar-0oflt-lafos-qqauz/2",
    "confidence_mode": "custom",
    "custom_confidence": 0.2,
    "iou_threshold": 0.5,
    "disable_active_learning": true
  }],
  "outputs": [
    {"type": "JsonField", "name": "predictions", "selector": "$steps.detect_original.predictions"},
    {"type": "JsonField", "name": "resolved_model_id", "selector": "$steps.detect_original.model_id"},
    {"type": "JsonField", "name": "inference_id", "selector": "$steps.detect_original.inference_id"}
  ]
}
```

**Why this amendment is explicit:** A pre-score 2-original-image smoke call succeeded but produced slightly different pixel coordinates and confidence values from the earlier V23 per-image `models_infer` call while preserving the same resolved original model and detection classes/counts. These variants must NOT be silently combined or portrayed as identical bit-level inference. V26 therefore re-infers **all 459 eligible original valid images** using **the SAME vectorized inference spec**, including the five previously studied V23 Valid images, and records `V26_BATCH_WORKFLOW_EXECUTION`, per-image inference ID, model resolution, image shape, and `previously_development_exposed=true` for all. V23 five cases are marked `previously_reused_in_V23_pilot=true` but V23 prediction coordinates are **not** reused in V26 numerical scoring.

The image array order and returned output array order must be checked by the Workflow's returned `parent_id = image.[batch_index]` for each prediction; each output must have the original native Source dimensions, unchanged model ID, 0.2 confidence floor and valid 17-class names. A zero-prediction output may legitimately lack parent IDs, but output array length must equal input array length. Keep processing chunks in exact M0 Source-ID order and archive numeric original Source reference boxes / new prediction boxes with **no image pixel data, URLs, credentials, visualization files or Test material**.

The IoU 0.50 single-class confidence-ordered matching and M0/M1/M2 risk groups are **unchanged**. No XAI, worker-level evaluation, electricity measurement or A5 superiority claim occurs in V26. If service fails or an annotation does not match the frozen V20 Source record, mark that ID failed without silently changing denominators.
