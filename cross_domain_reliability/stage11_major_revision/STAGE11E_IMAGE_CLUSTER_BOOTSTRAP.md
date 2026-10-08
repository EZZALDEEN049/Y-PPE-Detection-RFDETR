# Stage 11E — Image-cluster bootstrap for safety outcomes

**Status: COMPLETE for cross-domain safety recall and consensus false-negative rates.**

Bootstrap unit: image; 10,000 percentile replicates; deterministic seed 20261009. Intervals quantify test-image sampling uncertainty conditional on the six trained models. They are not site-level population confidence intervals.

| Direction | Class | Metric | Estimate | 95% CI | GT objects | Images |
|---|---|---|---:|---:|---:|---:|
| Y_to_C | no_helmet | consensus_fn_rate | 0.838 | 0.694–0.947 | 37 | 23 |
| Y_to_C | no_helmet | mean_recall_across_3_seeds | 0.117 | 0.036–0.225 | 37 | 23 |
| Y_to_C | no_gloves | consensus_fn_rate | 0.922 | 0.848–0.980 | 51 | 22 |
| Y_to_C | no_gloves | mean_recall_across_3_seeds | 0.039 | 0.007–0.085 | 51 | 22 |
| Y_to_C | no_boots | consensus_fn_rate | 1.000 | 1.000–1.000 | 15 | 5 |
| Y_to_C | no_boots | mean_recall_across_3_seeds | 0.000 | 0.000–0.000 | 15 | 5 |
| C_to_Y | no_helmet | consensus_fn_rate | 0.929 | 0.750–1.000 | 14 | 12 |
| C_to_Y | no_helmet | mean_recall_across_3_seeds | 0.024 | 0.000–0.083 | 14 | 12 |
| C_to_Y | no_gloves | consensus_fn_rate | 0.966 | 0.925–1.000 | 88 | 45 |
| C_to_Y | no_gloves | mean_recall_across_3_seeds | 0.015 | 0.000–0.034 | 88 | 45 |
| C_to_Y | no_boots | consensus_fn_rate | 1.000 | 1.000–1.000 | 30 | 15 |
| C_to_Y | no_boots | mean_recall_across_3_seeds | 0.000 | 0.000–0.000 | 30 | 15 |

## Interpretation boundary
- Object instances from the same image were not treated as independent bootstrap units.
- Three seeds share architecture/data/protocol; mean-recall intervals are conditional on these trained seed realizations and do not constitute independent-site replication.
- mAP/domain-gap bootstrap CIs are **not** included here because Stage 6 did not retain the per-image ranked prediction archive needed to recompute AP under image resampling. That requires an inference-only prediction archive step under the frozen evaluator.
