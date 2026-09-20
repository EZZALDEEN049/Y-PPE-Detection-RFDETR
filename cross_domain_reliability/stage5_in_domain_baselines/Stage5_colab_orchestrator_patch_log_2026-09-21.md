# Stage 5 Colab Orchestrator Patch Log — 2026-09-21

## Scope
This note documents two pre-training Colab-orchestrator defects found before any Stage 5 baseline completed. No held-out test evaluation was performed.

## Defect 1 — resource-freeze provenance key mismatch
Cell 7 wrote the checked-out Git commit under `git_sha`, while Cell 8 initially checked only `repo_git_sha`. This produced an immediate stale-freeze error even when the frozen commit and current repository HEAD were actually identical.

### Correction
Cell 8 now resolves the frozen repository identity as `repo_git_sha` if present, otherwise `git_sha`, and still requires exact equality to the current repository HEAD before training can proceed.

## Defect 2 — launcher console-log path ownership
The orchestrator initially attempted to open `run_dir/console.log` before the controlled trainer created `run_dir`. The trainer itself intentionally refuses to overwrite a pre-existing run directory, so the launcher must not create that directory first.

### Correction
Launcher logs are now written under `Stage5_Baselines/_orchestrator_logs/<run_id>.console.log`. After a successful run, the log is copied into the completed run directory for provenance. On failure, the external launcher log remains available for diagnosis.

## Scientific status
- Completed Stage 5 training runs at time of these fixes: 0.
- Held-out test evaluation performed: false.
- Frozen datasets, splits, class mapping, seeds, epochs, resolution, architecture-specific batch/accumulation policy, and test gate are unchanged.
- These patches change orchestration/provenance handling only; they do not modify model hyperparameters, datasets, annotations, or evaluation policy.
