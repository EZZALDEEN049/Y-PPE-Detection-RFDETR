# Stage 7B — Deterministic Qualitative Failure Findings

**Status:** COMPLETE

Stage 7B uses the same frozen operating point as Stage 6 (imgsz=640, confidence=0.25, NMS IoU=0.70, class-matched IoU=0.50). It does not train, fine-tune, adapt, select checkpoints, or tune thresholds.

A **consensus false negative (consensus FN)** is a ground-truth safety-violation object that is missed by all three source-domain seeds (17, 42, 2026) in the same cross-domain direction.

## Consensus false-negative rates

| Transfer direction | Class | Ground-truth objects | Missed by all 3 seeds | Consensus FN rate |
|---|---|---:|---:|---:|
| Y-PPE → Construction-PPE | no_helmet | 37 | 31 | 83.8% |
| Y-PPE → Construction-PPE | no_gloves | 51 | 47 | 92.2% |
| Y-PPE → Construction-PPE | no_boots | 15 | 15 | 100.0% |
| Construction-PPE → Y-PPE | no_helmet | 14 | 13 | 92.9% |
| Construction-PPE → Y-PPE | no_gloves | 88 | 85 | 96.6% |
| Construction-PPE → Y-PPE | no_boots | 30 | 30 | 100.0% |

## Size-stratified consensus failures

### Y-PPE → Construction-PPE
- no_helmet: 5 small, 26 medium, 0 large consensus FNs.
- no_gloves: 24 small, 23 medium, 0 large consensus FNs.
- no_boots: 11 small, 4 medium, 0 large consensus FNs.

### Construction-PPE → Y-PPE
- no_helmet: 6 small, 3 medium, 4 large consensus FNs.
- no_gloves: 24 small, 54 medium, 7 large consensus FNs.
- no_boots: 6 small, 10 medium, 14 large consensus FNs.

## Interpretation

The failure is highly reproducible across random seeds. In both transfer directions, the overwhelming majority of safety-violation objects are missed by all three independently trained source-domain models.

The most severe result is no_boots: every held-out cross-domain ground-truth no_boots object is a consensus false negative in both directions (15/15 for Y→Construction and 30/30 for Construction→Y).

Object scale contributes to domain mismatch but cannot alone explain the failure. In Construction→Y, all 30 no_boots objects are missed despite spanning small, medium, and large size bins, including 14 large objects. Similarly, no_gloves failures span all size bins. Therefore, the evidence points to a broader representation/semantic/domain-appearance problem rather than a small-object-only failure.

The deterministic overlays are intended as qualitative illustrations of the already-established quantitative failure and are not used for threshold selection, model selection, or quantitative re-estimation.

## Publication-safe claim

> Cross-domain safety-violation detection exhibited systematic, seed-consistent failure. Across both transfer directions, consensus false-negative rates exceeded 83% for no_helmet, 92% for no_gloves, and reached 100% for no_boots. Because these failures occurred across multiple object-size strata, particularly in the Construction→Y direction, object scale alone cannot account for the observed reliability collapse.

## Boundary

These results do not establish a single causal mechanism. Plausible contributors include domain-specific visual appearance, annotation semantics, contextual cues, class imbalance, and scale distribution. The paper should present these as evidence-supported hypotheses rather than confirmed causes.
