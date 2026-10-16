# Pre-execution Protocol v0.1 — Sustainable CV Evidence Audit

**Protocol date:** 2026-10-16. **Status:** frozen for this two-track *source audit only*, not preregistered. Revision required before any new inference experiment.

## Design and unit of analysis
Descriptive methodological audit of two *existing* Roboflow-hosted Y-PPE model tracks (YOLO11m and RF-DETR Small). The unit is a publicly reported model-evaluation/deployment-evidence record, not an independent image or training seed. No new GPU training is needed. Source dates and URLs must be retained.

## Evidence hierarchy
A. Independent common-test evaluation with identifiable test manifest, reproducible code and thresholds.
B. Verifiable model platform metrics with exact model/version identifiers.
C. Text claims lacking linked evaluation artifacts.
Only B currently supplies the main descriptively reported accuracy values. C is not promoted to B. Shared counts and preprocessing configuration never by themselves prove identical test membership.

## Extracted dimensions
1. Accuracy provenance: mAP@50, precision, recall, model ID, dataset version, reporting source.
2. Controlled comparison: same held-out test files, common ontology and metric definitions, threshold handling, no leakage.
3. Compute: local executable model artifact and licensing, processor, precision, RAM/VRAM, median/p95 latency, warmup, batch size, repetitions.
4. Environment: measured joules/image with measurement boundaries, idle baseline, power sampling, uncertainty; energy mix and time-bound carbon intensity.
5. Real-world safety: per-class false negatives, per-image errors, out-of-domain sites, confidence calibration, presence of vulnerable non-workers.
6. Deployment readiness: offline capability, hardware/maintenance costs, field use duration, network dependency, local governance and privacy.

Every metric is classified as directly supported, reported-with-limits, not documented in audited sources, or not applicable. Null means unknown/not documented, never measured zero.

## Decision gates
Accuracy comparison is NOT ESTABLISHED until source images in the held-out tests are demonstrably identical and a common evaluator is used.
Efficiency comparison is NOT ESTABLISHED until model inference is benchmarked with a frozen workload on controlled hardware.
Energy/carbon advantage is NOT ESTABLISHED until workload-level energy and corresponding contextual carbon measurements exist.
Deployment readiness is NOT ESTABLISHED until operational and safety-critical tests exist.

Do not compute a single overall sustainability score from incomplete heterogeneous evidence. Do not call one model greener based on parameter count or architecture alone.

## Exact work remaining for a stronger experimental study without model retraining
1. Verify rights and access to export trained model artifacts or a reproducible execution environment for both tracks. An online hosted API call by itself cannot measure local model compute energy.
2. Export or hash the two original split manifests, explicitly de-duplicate near-duplicates/source sequences and establish a common held-out test benchmark.
3. Freeze per-class label mapping and confidence/IoU rules; report mAP50:95, per-class recall, per-class false-negative rates, confidence calibration and paired uncertainty.
4. If runnable local artifacts exist, use the **same** CPU/edge machine for both models. Record OS, device model, memory, runtime, precision, input preprocessing, warmup, repeated timing, latency distribution, RAM and energy source (if instrumented).
5. Measure per-inference energy against a documented idle baseline; repeat runs and describe uncertainty. Use appropriate location/time emissions factors for any carbon estimate, and keep grid assumptions explicit.
6. Evaluate a distinct field/site distribution with governance safeguards, ideally across additional independent model/dataset pairs.
7. Separate prior Y-PPE/RF-DETR or cross-domain manuscripts: cite previous data/model publications and require a distinct new experiment and question to justify a new research contribution.

## Known research validity risks
- Comparing hosted model overview numbers from possibly different splits.
- Calling 5,577 augmented images independent 5,577 source worksite scenes.
- Architecture differences confounded by optimization/preprocessing/hosting.
- Reusing a prior manuscript's results as if newly generated.
- Treating energy estimates from TDP, parameters or published COCO benchmarks as measured energy on Y-PPE.
- Claiming broad Q1-worthy novelty on two public metrics without measured sustainability outcomes.

## Integrity statement
This protocol and software audit can be executed on GitHub-hosted CPU CI. It documents evidence boundaries. It does NOT constitute evidence of reduced electricity use, CO2e, or field deployment success.
