# EcoSafe Selective Experts

This directory contains the new extension study built on the already completed Stage 5/6 PPE experiments.

## Core idea

Reuse the six completed YOLO11m domain-specific models instead of retraining object detectors. For each seed (17, 42, 2026), pair:

- Y-PPE expert: `Y_YOLO_s<seed>`
- Construction-PPE expert: `C_YOLO_s<seed>`

The selective controller observes only lightweight signals available from the primary expert (confidence-derived uncertainty, safety-risk evidence, and optional domain-shift features) and decides whether to accept the primary prediction or invoke the second expert.

## Scientific objective

Test whether selective multi-expert inference can reduce the fraction of second-expert executions while preserving safety-critical violation recall relative to an always-run-both reference.

Primary safety classes are frozen from the prior study:

`no_helmet, no_gloves, no_boots`

## Non-negotiable evaluation rules

1. No detector retraining for the primary EcoSafe study.
2. Existing Stage 5 checkpoints are immutable evidence assets.
3. Router/calibration thresholds are selected on development/calibration data only.
4. Held-out test data are not used for router training or threshold selection.
5. Report measured energy only when obtained on one fixed GPU/software stack.
6. Until energy is measured, compute savings are reported only as execution-rate/proxy cost, never as Joules.
7. Results from the prior cross-domain paper remain baseline evidence; the new contribution must come from selective routing.

## Current asset status

The six completed `last.pt` checkpoints and six `best.pt` checkpoints have been verified to exist in the connected Stage5_Baselines storage. Stage 6 held-out evaluation is also complete for 12 train/test cells. Per-image prediction exports were not preserved, so they must be regenerated from the existing checkpoints before router training.

## Minimal new execution

1. Export per-image predictions from each immutable checkpoint.
2. Build development-only router labels from safety false-negative recovery.
3. Train/interrogate simple routing baselines.
4. Evaluate held-out selective inference across all three seeds.
5. Measure latency and energy in one short confirmatory GPU run.
