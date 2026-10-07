# Stage 7 — Scientific Results Analysis

**Status:** PRIMARY DESCRIPTIVE ANALYSIS COMPLETE

This stage uses only the frozen Stage 6 outputs: 12 held-out evaluation cells from six completed YOLO11m final-epoch checkpoints. No retraining, adaptation, checkpoint reselection, or post-test threshold tuning is introduced.

## 1. Primary cross-domain results

| Training domain | In-domain mAP50:95 | Cross-domain mAP50:95 | Absolute gap | Relative drop | In-domain F1 | Cross-domain F1 |
|---|---:|---:|---:|---:|---:|---:|
| Y-PPE | 0.291 ± 0.007 | 0.121 ± 0.003 | 0.170 | 58.4% | 0.651 ± 0.010 | 0.497 ± 0.015 |
| Construction-PPE | 0.252 ± 0.004 | 0.082 ± 0.005 | 0.170 | 67.4% | 0.712 ± 0.006 | 0.328 ± 0.022 |

Across all three seeds, the mAP50:95 generalization gap remained positive in both transfer directions. Y-trained models lost 0.170 ± 0.009 mAP50:95 when transferred to Construction-PPE, whereas Construction-trained models lost 0.170 ± 0.003 when transferred to Y-PPE. The near-identical absolute gaps conceal asymmetric relative degradation: 58.4% for Y→Construction and 67.4% for Construction→Y.

## 2. Fixed operating-point reliability

| Training direction | Precision in→cross | Recall in→cross | F1 in→cross |
|---|---:|---:|---:|
| Y-PPE → Construction-PPE | 0.881 → 0.711 | 0.516 → 0.382 | 0.651 → 0.497 |
| Construction-PPE → Y-PPE | 0.921 → 0.766 | 0.580 → 0.209 | 0.712 → 0.328 |

For Y→Construction, recall falls by 0.134 (25.9% relative) and precision by 0.170 (19.3% relative). For Construction→Y, recall falls by 0.371 (64.0% relative), producing an F1 reduction of 0.384 (53.9% relative). Cross-domain failure therefore cannot be described adequately by AP alone.

## 3. Safety-critical violation recall

| Condition | no_helmet recall | no_gloves recall | no_boots recall |
|---|---:|---:|---:|
| Y-PPE in-domain | 0.310 ± 0.109 | 0.303 ± 0.029 | 0.367 ± 0.033 |
| Y-PPE → Construction-PPE | 0.117 ± 0.031 | 0.039 ± 0.034 | 0.000 ± 0.000 |
| Construction-PPE in-domain | 0.027 ± 0.000 | 0.020 ± 0.000 | 0.000 ± 0.000 |
| Construction-PPE → Y-PPE | 0.024 ± 0.041 | 0.015 ± 0.007 | 0.000 ± 0.000 |

The most safety-relevant result is the collapse of violation-class recall. Y-trained models detect no_boots with mean recall 0.367 in-domain but 0.000 on Construction-PPE. no_gloves falls from 0.303 to 0.039 and no_helmet from 0.310 to 0.117.

Construction-trained models already show near-floor violation recall in-domain (0.027 no_helmet, 0.020 no_gloves, 0.000 no_boots). Therefore, their violation-class cross-domain behavior must be interpreted as a floor effect as well as a transfer problem, not as a pure domain-shift penalty.

## 4. Seed stability

The sign of the mAP50:95 domain gap is identical for every seed in both directions.

- Y-trained gaps: 0.173, 0.178, 0.159 for seeds 17, 42, 2026.
- Construction-trained gaps: 0.172, 0.166, 0.171 for seeds 17, 42, 2026.

This indicates that the observed cross-domain degradation is not driven by one anomalous seed.

## 5. Interpretation boundary

The evidence demonstrates cross-domain degradation and safety-class failure, but it does **not** yet identify the mechanism. The current results do not establish whether the cause is class imbalance, image-domain shift, annotation-policy differences, object scale, occlusion, or other dataset characteristics.

Those explanations must be tested in a separate diagnostic audit before being stated causally in the Discussion.

## 6. Immediate next task

Run a dataset-level diagnostic audit of:

1. class-frequency distributions by split and domain;
2. object-size distributions;
3. image resolution/aspect-ratio distributions;
4. safety-violation support and imbalance;
5. representative false-negative review for no_helmet, no_gloves, and no_boots.

This Stage 7 diagnostic work does not change any frozen Stage 6 model or evaluation setting.
