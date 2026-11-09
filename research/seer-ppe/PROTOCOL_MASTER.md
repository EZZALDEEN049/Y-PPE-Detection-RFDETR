# SEER-PPE — experimental master protocol v0.3

**Status:** Draft/pilot engineering. **Not preregistered; no final-test data used for selection; no evidence of energy savings or safety improvement yet.**

## Scientific question
Can an adaptive post-detection policy minimize **measured incremental evidence-computation energy**, at acceptable worker-level risk and explanation fidelity, over Y-PPE-only images, against strong matched-review and matched-compute baselines?

## 1. Core design
- Source: Y-PPE only. Historical frozen 17-class `altayyar-0oflt-lafos-qqauz/2`; historical train-augmented version (5,577). Distinguish from 17-class 2,288-image candidate cleaned derivative and nine-class h9-v2 archive.
- State/actions: `BASIC` detector-only evidence, `EXPLAIN` targeted XAI followed by a specified decision gate, `REVIEW` human review request. Any missing worker and unknown policy must be audited, not silently treated as no violation.
- Inputs to runtime routing: detected boxes, scores, visibility/association confidence, **runtime-known** site/task PPE requirement; never adjudicated label/test truth.
- Outputs: route, abstention/review reason, detection identifier, explanation evidence summary, optional potential safety alert; explanation does **not** repair a missed worker.

## 2. Evaluation population and ground truth
- Sample independent acquisition families; purge/review visual and sequence leakage before splitting; SHA/group audit utility alone is insufficient.
- Record every visual worker independently (see `ANNOTATION_CODEBOOK.md`); use task rule to determine confirmed violation and treat unknowns explicitly.
- Fixed final test kept unviewed and unmodified until all thresholds/methods and analysis scripts are locked. Three historical engineering-smoke IDs cannot be counted as untouched test cases.

## 3. Experimental arms (same detector/data/hardware)
A0. Detector-only and fixed confidence threshold, no explanation.
A1. Explain-all-eligible detections, followed by same decision criteria.
A2. Confidence-only selective explanation.
A3. Matched-review/budget explanation routing (review capacity and explanation-call counts matched).
A4. Energy-only routing, without safety guard (diagnostic comparator, not recommended deployment).
A5. **SEER-PPE** joint safety–fidelity–energy routing; select on calibration, then lock.

## 4. Objective and outcomes
For policy `pi`, conceptual optimization is:

`min_pi mean(E_detector + E_additional_XAI(pi))`

subject to prespecified eligible-worker-level false-clearance rate `FC`, uncontained violations `UC` (including missed workers), minimum validated explanation fidelity `F`, and bounded human-review load `H`. Human review time/cost is reported **separately** from electrical device energy, never assigned zero. `REVIEW` is not a verified successful intervention. Report failure to meet constraints honestly.

Primary study endpoints (not yet measured): joules/image, joules/eligible worker, false-CLEAR per adjudicated true violation, missed/uncontained risk, explanation fidelity/target-match loss, review fraction, and accuracy by class/scenario. Secondary: latency, P95 latency, mean and maximum memory, precision/recall/mAP by class.

## 5. Explanations
- Distinguish attribution localization in equipment/worker ROIs from *behavioral faithfulness* under deletion/insertion perturbations.
- On a perturbed image, match same-class target box by IoU before computing confidence drop. Report `LOST` and `AMBIGUOUS` as separate outcomes; never set their score to 0 or reassign to a different item.
- Use permitted unexposed development images for implementation checks. Gradient access to exact checkpoint not yet established; hosted prediction JSON is insufficient for Grad-CAM.

## 6. Measurement and statistics
- Hardware: model/type, CPU/GPU, power sensor and metering scope, library versions, warm-up, batch size, run order and repeated seeds. GPU-only watts must not be described as system-level electrical consumption.
- Compute energy via measured watt trace integration, not FLOPs or simulated test vectors. Measure base detector and *incremental* XAI separately; report cold/warm conditions explicitly.
- Calibrate decision thresholds and risk bounds on calibration split using preregistered test families; final-test analysis with uncertainty at source-group level, not naive iid boxes.
- Rare-class support determines what can be claimed. Original historical test has 22 `No Hard Hat` object labels in 16 images, **not** 22 confirmed independent worker violations.
- Use no empirical plots until real runs have traceable config/manifest/outputs.

## 7. Gates
G1 clean-17 physical archive + group audit OPEN; G2 human-adjudicated GT OPEN; G3 exact checkpoint local load + gradient XAI OPEN; G4 measured energy OPEN; G5 calibration/test LOCK OPEN. Model endpoint smoke was completed in Phase2, but not any gate above.

## 8. External and original references
- Author's master's thesis (chapter 3) and four related IEEE papers; cite and differentiate results.
- RF-DETR loader: https://rfdetr.roboflow.com/latest/learn/train/ (check checkpoint schema/version compatibility).
- Original cleaned derivative audit: https://github.com/EZZALDEEN049/Y-PPE-Detection-RFDETR/blob/main/cross_domain_reliability/stage2_data_audit/results/Y-PPE_v2_clean_stage2_closure_2026-09-20.md
- Related literature on conformal risks, calibrated detection and PPE context should be checked before novelty claims; a complete systematic review is not claimed.


## Phase 6 protocol amendment (2026-11-10)
- Freeze backup stored in restricted Drive, SHA256 `d47d9676b785a847ef1bcb8a871574815b0b67b967f9107680fb0b85b1a52d61`. This verifies binary replay, not source-family independence.
- Seven low-distance visual similarity pairs are analyst-triaged as visually distinct; independent human/source review still required. Retain images pending source-level adjudication; do not mechanically remove merely due to dHash proximity.
- Pilot analysis includes product/non-work negative controls as separate **task-ineligible or uncertain** categories; only expert task-policy validation can create true/false occupational violations.
- `occlusion_explain` (model-agnostic) requires a real trained checkpoint and same-instance matching; no fabricated zero score for LOST/AMBIGUOUS. Grad-CAM is optional and not claimed.
- Actual power measurement is physically blocked in current CPU-only container. Synthetic watts, FLOPs and wall-clock time are prohibited as proxies for scientific joules.
- Stage6 preflight and unit tests are executed; A/B reviewer ground truth and experimental efficacy remain unperformed.
