# Stage 7 — Dataset Diagnostic Findings

**Status:** DATASET DIAGNOSTIC AUDIT COMPLETE

This audit is descriptive and analysis-only. It does not retrain, adapt, or reevaluate any model and does not change the frozen Stage 6 settings.

## Main findings

Both frozen derivatives are stored as 640×640 square images across train/validation/test. Stored image resolution and aspect ratio therefore do not explain the observed cross-domain gap.

Training-set max-to-min nonzero class ratios are 11.49 for Y-PPE-h9-v2 and 21.76 for Construction-PPE-h9-v2, indicating stronger class imbalance in Construction-PPE. Its validation split is even more imbalanced (57.0).

Safety-class training support is heterogeneous:
- Y-PPE-h9-v2: no_helmet=113, no_gloves=677, no_boots=226.
- Construction-PPE-h9-v2: no_helmet=352, no_gloves=403, no_boots=74.

The clearest scale mismatch is no_boots. In Y-PPE training, approximately 30.5% of no_boots instances are small, 21.2% medium, and 48.2% large. In Construction-PPE training, about 77.0% are small, 23.0% medium, and none are large.

no_helmet also shifts substantially in size profile: Y-PPE training is about 57.5% small and 36.3% medium, whereas Construction-PPE is about 24.1% small and 71.9% medium.

These results support the bounded conclusion that class support, imbalance, and object-scale distributions differ materially across the two domains. They do not establish that these factors are the sole causal explanation for Stage 6 failures. In particular, Construction-PPE no_helmet has nontrivial training support but still exhibits near-floor in-domain violation performance, so frequency alone is insufficient.

## Next gate

Stage 7B performs a deterministic qualitative failure audit at the already-frozen Stage 6 operating point. It identifies safety-class objects missed by all three source-domain seeds in each cross-domain direction and selects examples deterministically rather than by visual preference.
