# Cross-Domain PPE Reliability Study

This workspace supports the empirical study on whether strong in-domain PPE detection performance remains reliable under unseen construction/industrial distribution shift.

## Working research question

Does in-domain performance remain reliable under unseen domain shift, and how much target-domain information is needed to recover detection, calibration, and safety performance?

## Planned evaluation sequence

1. Protocol and ontology freeze.
2. Raw data and annotation audit.
3. Harmonized in-domain baselines.
4. Zero-shot cross-domain evaluation.
5. Calibration and safety-aware reliability analysis.
6. Progressive target-domain adaptation.
7. Statistical analysis and uncertainty reporting.
8. Results, discussion, and submission-ready manuscript.

## Primary datasets

- **Y-PPE** — Yemeni construction/development-project PPE dataset.
- **Construction-PPE** — public construction PPE dataset used as the main external domain.

## Secondary robustness dataset

- **SH17** — industrial/manufacturing PPE dataset. It is not treated as a construction dataset and is reserved for secondary robustness analysis.

## Repository policy

Large image datasets, Roboflow API keys, model weights, private credentials, and raw audit outputs should not be committed to GitHub. This repository stores code, configuration, protocol documentation, and reproducible analysis scripts. Dataset archives should remain in Roboflow, Google Drive, or another controlled storage location.

Current active work: [`stage2_data_audit/`](stage2_data_audit/).
