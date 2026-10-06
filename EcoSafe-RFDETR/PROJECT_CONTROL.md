# EcoSafe-RFDETR Project Control

## Authoritative branch
`ecosafe-rfdetr`

GitHub is the version-control authority for the EcoSafe-RFDETR study. Code, protocol revisions, experiment configurations, manifests, lightweight result summaries, analysis scripts and manuscript-support files should be committed here before being treated as part of the reproducible study.

## Data rule
GitHub controls the project but is not the raw-data store. Raw datasets remain on the independent GPU/storage environment. Dataset identity is frozen using source DOI/URL, ontology, split metadata, manifests and SHA-256 hashes.

## Test-set rule
The final test set must not be used to select the detector variant, calibration method, OOD method, router, thresholds or non-inferiority margin.

## First empirical gate
Pilot-0 compares RF-DETR Nano and Medium; Large is added only if justified. Adaptive EcoSafe development proceeds only if a useful safety-energy separation is demonstrated.

## Evidence to version in GitHub
- environment metadata
- dataset manifests and hashes
- frozen configs
- lightweight training logs
- summary metrics
- energy summary tables
- derived per-frame analysis tables when practical
- statistical outputs
- Pareto source data
- manuscript table/figure source data

## Do not commit
- raw datasets
- large checkpoints unless intentionally released
- credentials or API keys
- private personal data
