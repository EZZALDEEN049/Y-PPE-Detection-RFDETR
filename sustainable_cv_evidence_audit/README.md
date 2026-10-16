# Sustainable Computer Vision: Existing-Model Evidence Audit (v0.1)

**Status:** Preliminary, auditable research scaffold; **not** a completed empirical study, validated sustainability benchmark, or submission-ready Q1 manuscript.

## Why this separate workstream?

The repository's existing RF-DETR and YOLO11m model projects provide separately published, already-trained PPE detector results. A sustainable-computer-vision study cannot infer power, carbon, latency, or affordability from mAP. This workstream transparently audits what is reported and what is missing before a defensible no-retraining experiment is planned.

Working title: **From Detection Accuracy to Deployability: An Evidence Audit of Pretrained PPE Computer Vision Models in Resource-Constrained Contexts**.

Working question: **What does existing public evidence actually establish about the accuracy comparability and resource-constrained deployability of two already-trained PPE detector tracks?**

This is a focused *case-study methodological audit*. Two models alone are inadequate to establish general claims about detector families or to validate a broad sustainability theory. Extending to multiple independent model families, domains, hardware platforms, and independent sites is a later requirement for stronger journal claims.

## Existing published-on-platform figures — descriptive only

| Trained model project | mAP@50 | Precision | Recall | Source |
|---|---:|---:|---:|---|
| YOLO11m | 92.2% | 95.3% | 87.2% | https://universe.roboflow.com/master-fylfq/altayyar-0oflt-lafos-qqauz-ty5nh |
| RF-DETR Small | 94.0% | 94.4% | 88.0% | https://universe.roboflow.com/softyyemen/altayyar-0oflt-lafos-qqauz |

These are **not independently recomputed**, and neither the identical test-image membership nor a single common evaluator has been established. **Do not publish the difference as an architecture win or a paired statistical comparison.**

The project overview mentions 2,327 original images; the linked augmented dataset versions are documented as 5,577 images each (see repository root README). These must not be conflated. RF-DETR's separate project-description statement of 96.2% mAP@50 lacks a linked common evaluation artifact in this audit and is recorded as a discordant claim, not as an alternative main metric.

## CPU-only reproducible audit

From this directory:

    python -m unittest -v test_audit.py
    python audit.py --out-dir outputs

Both commands use the Python standard library only. The outputs are a machine-readable status and a Markdown audit report. They do **not** run inference, retrain weights, or produce new statistical comparisons. The GitHub Actions workflow separately verifies these steps on a CPU runner.

## Evidence before claims

- Common accuracy superiority: requires verified held-out image membership and common metric definitions/evaluation.
- Efficiency: requires reproducible batch-size-controlled, hardware-specific inference latency and memory measurements.
- Energy and carbon: requires documented measured power/energy, system boundaries, workload, repetitions, power calibration, electricity emission factor/time/location and uncertainty. Do not extrapolate generic architecture benchmarks into Y-PPE carbon claims.
- Deployability and safety: requires offline operation verification, per-violation false-negative analysis and external-site testing.
- Privacy: source dataset and workers' image rights/governance must be cleared before public inference on identifiable persons.

Missing evidence is **not proof** of poor efficiency or inadequate performance.

Read PROTOCOL.md and MANUSCRIPT_SKELETON.md. Existing cross-domain work in cross_domain_reliability/ remains a separate experimental track: do not mix its split variants, manuscript conclusions, or baseline definitions into this audit.

## Reproducibility and security

No private dataset images, inference API keys, model checkpoints, or credentials are required or committed. Raw Roboflow model overview results and current GitHub README are the provenance sources. Captured snapshot: 2026-10-16. Future data updates must preserve previous snapshots or specify their revision.
