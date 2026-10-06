# EcoSafe-RFDETR Experimental Protocol v1.0

## Primary question
Can per-input computational escalation reduce directly measured inference energy while preserving PPE-violation recall?

## Primary endpoints
- Safety: macro recall over explicit violation classes.
- Sustainability: joules per frame.
- System: escalation rate.

## Pilot model set
- RF-DETR Nano
- RF-DETR Medium
- RF-DETR Large only if justified by Pilot.

## Success logic
A configuration supports the main EcoSafe claim only if:
1. mean inference energy is lower than the fixed high-capacity reference; and
2. violation recall remains within a pre-specified acceptable margin.

## Data leakage safeguards
- Final test data cannot be used for model/threshold/router selection.
- Cross-dataset exact and near-duplicate checks are mandatory.
- Dataset manifests must be frozen with SHA-256 hashes.
- Calibration and router selection occur only in development data.

## Primary public data
- Mendeley PPE v6: training/development, 4 classes.
- PPED: controlled shift analysis using feature.csv.
- CHVG: external construction-domain evaluation after ontology mapping.

## Required reporting
Hardware, GPU power mode, driver, CUDA, PyTorch, RF-DETR package version, model precision, resolution, batch size, warm-up, repetitions, sampling interval, measurement boundary, mean/CI.

## Statistical plan
- Paired comparisons on common images.
- Bootstrap 95% CIs; cluster bootstrap where sequence/site identifiers exist.
- Pareto analysis: (J/frame, violation recall), (latency, violation recall).
- Formal non-inferiority only if delta is justified and frozen before final test.
