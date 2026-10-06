# EcoSafe-RFDETR

This branch is the version-control home for the EcoSafe-RFDETR paper and experiments.

## Objective
EcoSafe-RFDETR investigates whether a lightweight detector can process routine PPE frames while uncertain, shifted, or safety-relevant inputs are selectively escalated to a higher-capacity RF-DETR model, reducing measured inference energy without materially degrading PPE-violation recall.

## Workflow
1. Dataset audit and data lock.
2. RF-DETR Nano baseline.
3. RF-DETR Medium baseline.
4. RF-DETR Large only if justified by the pilot.
5. Per-frame comparison and real GPU energy measurement.
6. Oracle escalation and GO / MODIFY / NO-GO decision.
7. Calibration, uncertainty, OOD and safety-aware routing.
8. External/domain-shift evaluation.
9. Statistical and Pareto analysis.

## Data policy
Raw datasets are not stored in GitHub. Public datasets are downloaded from their official archival sources into the independent GPU environment. GitHub stores code, configuration, manifests/hashes, protocols and lightweight result summaries.

## Current status
The research problem, gap, contribution, architecture, experimental protocol and execution pack are prepared. GPU-based empirical runs are pending.

Execution pack: `EcoSafe-RFDETR/EcoSafe_RFDETR_Execution_Pack_v1.zip`.
