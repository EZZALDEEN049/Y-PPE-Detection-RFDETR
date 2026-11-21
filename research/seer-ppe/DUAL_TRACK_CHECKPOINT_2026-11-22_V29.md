# SEER-PPE — dual-track research checkpoint V29 (22 November 2026)

## Confirmed current baseline
- Canonical paper: MANUSCRIPT_MASTER.md, updated to v0.27.
- Original hosted model: altayyar-0oflt-lafos-qqauz/2, RF-DETR Small, unchanged.
- V26: all 459 original Source Valid images scored against current author boxes; M0 TP3297/FP806/FN174, micro-F1 0.870610; 17-class results and M1/M2 sensitivity preserved.
- Original source images, annotations, model weights and splits remain unchanged. Protected Test was not accessed.

## Newly executed V27–V29 work
1. **V27 Gaussian target-box occlusion:** 10 unique frozen targets on nine development-exposed images; 27 model passes; 9/10 target detections lost, mean target confidence drop 0.622325, mean control drop 0.008304, specificity margin 0.616005. All ten target filters and seven control filters exact-one.
2. **A5/A6 V27:** eight selected target slots per arm, six shared and two unique; 7/8 target losses each. Mean target drop A5 0.641018 versus A6 0.621806. Post-selection V23 detection ledger: A5 4 TP/0 FP, A6 3 TP/1 FP on four selected Valid targets each. Object-detection diagnostic only.
3. **V28 black-fill deletion / target-only insertion:** ten targets; 30 archived repeat passes plus 30 unarchived first-attempt passes, total 60 actual calls. Black deletion lost 10/10 targets; target-only insertion retained 7/10. Three failures were the three smallest boxes (<0.11% image area). The one-step probes are not progressive deletion/insertion curves or AUC.
4. **A5/A6 V28:** deletion lost 8/8 for both arms; insertion retained 6/8 for both. Mean deletion drop A5 0.759013 versus A6 0.739801; mean insertion ratio 0.757727 versus 0.758744.
5. **V29 hosted timing:** ten direct calls, five images × two repetitions; mean request round-trip 1.5206 s, median 1.469 s, range 1.383–1.835 s. No provider server time.
6. **Total compute accounting:** 97 original-model calls (V27 27 + V28 60 + V29 10); 30 V28 first-attempt calls have no persisted outputs; 67 calls have archived result/metadata. No billing credits/USD cost available.

## Resource observability
- Connected Roboflow workspace has zero registered devices.
- Hosted inference exposes no process memory or physical energy in Joules.
- Round-trip includes network/provider overhead; it is not pure model latency.
- No memory, energy or financial-cost estimates are reported.

## Research interpretation and hard limits
- V27/V28 measure local sensitivity of selected detector boxes to black-box perturbations, not complete attribution Faithfulness.
- V28 deletion is a single black-fill step; insertion is a single target-only sufficiency step. No progressive pixel-ranked curves/AUC, SHAP/Grad-CAM map or human explanation ground truth.
- Nine images are development-exposed; five Valid images were previously used in V23; acquisition-source independence is not established.
- A5/A6 differences are descriptive; no statistical superiority or worker-safety advantage.
- No human review, worker/task mandate scoring, PPE compliance, false-clearance analysis or independent external validation.
- Strict worker-safety gate remains NOT_FROZEN / scoring_ready=false.

## Authoritative new files
- [V27–V29 actual results report](V27_V29_ACTUAL_XAI_AND_PERFORMANCE_REPORT_2026-11-22.md)
- [V27 actual occlusion ledger](V27_ACTUAL_TARGETED_OCCLUSION_RESULTS_2026-11-22.json)
- [V27 A5/A6 comparison](V27_A5_A6_COMPARISON_2026-11-22.json)
- [V28 actual deletion/insertion ledger](V28_ACTUAL_TARGET_BOX_DELETION_INSERTION_RESULTS_2026-11-22.json)
- [V28 A5/A6 comparison](V28_A5_A6_DELETION_INSERTION_COMPARISON_2026-11-22.json)
- [V29 timing ledger](V29_ACTUAL_HOSTED_INFERENCE_TIMING_RESULTS_2026-11-22.json)
- [V27 scorer](tools/score_v27_actual_occlusion.mjs)
- [V28 scorer](tools/score_v28_deletion_insertion.mjs)

## Next execution order
1. Obtain pixel-ranked attribution or a defensible human explanation reference, then execute progressive deletion/insertion curves and AUC under a frozen baseline.
2. Freeze worker/task-level endpoints and false-clearance costs; keep unknowns explicit.
3. Evaluate actual review operations and a stronger selective comparator under matched safety, review and compute budgets.
4. For memory and Joules, use a named instrumented host/device with validated telemetry; do not infer them from hosted round-trip.
5. Finish journal editing and verified editable Word export after the evidence checks pass.
