# SEER-PPE V28 — frozen target-box deletion and target-only insertion probes

**Frozen: 22 November 2026, before V28 perturbation inference.** V28 reuses the exact nine development-exposed images and ten unique target boxes frozen before V27. No target, image, arm assignment, model, confidence threshold, NMS setting or original data is changed after V27 outcomes. V28 is an engineering follow-up to V27, not an independent validation.

## Fixed sample and model
- Exact same ten unique target detections and A5/A6 arm memberships from `V27_FROZEN_TARGETS_2026-11-21.json`.
- Same original frozen model `altayyar-0oflt-lafos-qqauz/2`, confidence 0.20, NMS 0.50, Active Learning disabled.
- Each target Workflow makes one baseline, one deletion-perturbed, and one insertion-perturbed model pass: 10 × 3 = **30 planned model passes**.
- Exact target filter is copied unchanged from the validated V27 Workflow spec. If it does not return exactly one target, mark target isolation failure; do not widen thresholds or substitute a detection.

## Perturbations
1. **Deletion-style test:** use `ColorVisualization@v1` with a fully opaque black fill (`#000000`, opacity 1.0) over the frozen target bounding box, then re-run the same model.
2. **Single-step target-only insertion/sufficiency test:** use `BackgroundColorVisualization@v1` with black, opacity 1.0, to mask every pixel outside the frozen target bounding box while preserving the original target-box pixels, then re-run the same model.

Both perturbations use the original model coordinate frame. The output is matched to the unperturbed target using the exact same class and original-box IoU ≥0.50. Record the maximum matched same-class confidence; use zero only if no same-class IoU≥0.50 match remains. Preserve target-filter counts and all failures.

## Outcomes and limits
- Report baseline, deletion, and target-only insertion confidence, confidence drops, detection-retention flags, and target box area fraction.
- Compare V28 black-fill deletion with V27 Gaussian box-blur occlusion as a robustness check, not as interchangeable masks.
- Report A5/A6 per-arm summaries with the same eight target slots per arm; shared target outcomes are reused in both arms, not treated as independent observations.
- **Insertion is a single-step target-only sufficiency probe, not a progressive insertion curve or insertion-AUC. Deletion is a single-step box fill, not a ranked pixel-deletion curve.** No pixel saliency ordering is available from the hosted black-box endpoint.
- This does not produce Grad-CAM, SHAP, a human explanation ground truth, worker-level PPE compliance, employer task mandates, or a causal safety outcome. It is a local box-guided perturbation sensitivity pilot.
- All nine images are development-exposed. The five Valid images were used in V23. Source independence is not certified. Do not access Test.
- Record workflow wall-clock only; it includes network/provider overhead and is not isolated model latency. Hosted Workflow exposes no process memory or physical energy in Joules; do not invent those measures.
- No human review is dispatched. Strict worker-safety `NOT_FROZEN/scoring_ready=false` remains unchanged.
