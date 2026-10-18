# EcoSafe best.pt: empirical secondary-expert value-of-information gate

**Recorded 2026-10-18. STATUS: exploratory DEVELOPMENT ONLY.** The primary last.pt study is unaffected. No held-out test, detector/router training, checkpoint tuning, hardware power/latency benchmark or carbon measurement was performed.

## Input / verification / reproducibility

- Original six immutable best.pt checkpoints and original 488 image validation files (Y-PPE 356; Construction 132); exact model SHA-256 locks were previously independently verified. Frozen source manifests: Y-PPE \`82c08766d5c5e50e93d41d21c4751fd686a3932ea6a8cb24ffd2838d9e30fba8\`, Construction \`59469299ba67355dbcb0e725851f73d244a7ad6e93522d44601be3c8323d3c14\`.
- **No new detector inference.** Reused exact low-confidence private per-frame prediction CSVs already exported at conf 0.001 using PyTorch CPU/Ultralytics 8.4.156 at 640 resolution, per-model NMS 0.70. Each private chunk and frame count was re-validated against its own SHA-256-locked manifest; every aggregated primary/joint/union TP/FP count was compared with the previously published anonymized, per-seed empirical reports (fail closed on mismatch).
- Fixed safety operational threshold confidence **0.25**, GT matching class-aware **maximum-cardinality IoU 0.50**, combined class-aware operational joint NMS **IoU 0.70**. All six seed/domain pairs scored in **both expert directions**, total 12 development cells, on 488 unique validation frames per seed (not independent sites).
- Separate local aggregate JSON SHA-256 \`91c7646274e5b4eaac1f5ebe6f9128061466168858986ec7a5a20d22f0aa34c2\`. Contains **only count/aggregate metrics**, never raw worker images, frame names, GT labels, predictions, paths or identifiers.
- Independently validated the AUC rank/tie calculation against \`sklearn.metrics.roc_auc_score\` on 40 deterministic synthetic cases. Seven additional synthetic private-local tests passed; repository code \`13_best_validation_oracle_efficiency_gate.py\`, synthetic CI tests and the existing SHA-locked reader provide an executable source-independent reproduction path. GitHub synthetic CPU gate: **56 tests successful**.

## Definitions: privileged oracle is NOT a trained/deployable method

For each validation frame i compute \`delta_i=TP(class-aware NMS(primary_i + secondary_i))-TP(primary_i)\`, using GT **only after inference**. A frame is **positive-benefit** if \`delta_i > 0\`. A **negative-benefit** frame loses a GT match under the operational joint merger; ordinary zero-delta frames cannot recover more GT matches at this fixed policy.

A **GT-privileged oracle** invokes the second expert on exactly the positive-benefit frames. It gets the primary outputs everywhere else and the actual same joint NMS only when needed. This retrospectively upper-bounds achievable recall/call tradeoffs **for these frozen predictions and merger**; it is impossible as a real-time policy because it needs the hidden GT. Any count of saved *expert calls* is a **theoretical proxy**, not energy, time, money, carbon or field safety.

For a primary-only, nonprivileged ranking diagnostic, compare two independently computable feature scores from the primary export:
- \`U_safety = 1 - max(confidence of primary's safety-class detections)\`, default 1 when none;
- \`U_all = 1 - max(confidence of ALL primary detections)\`, default 1 when none.

Use only a tied-rank Mann–Whitney ROC AUC of the *retrospective* positive-benefit label, with no fitted/calibrated threshold. This measures rank quality **on the same development images** and should be treated as unstable when positives are rare.

## New result A: Construction-PPE validation, C expert as primary

**132 frames, only 27 with annotated critical objects, and 98 safety objects overall.** Every seed uses the same frames and objects.

| Seed | C-alone TP / 98 | Always-joint TP / 98 | Positive-benefit frames / 132 | GT-privileged oracle TP / FP | Always-joint FP | AUC U_safety | AUC U_all |
|---|---:|---:|---:|---|---:|---:|---:|
| 17 | 13 | 20 | 7 | 20 / 37 | 110 | 0.063 | 0.865 |
| 42 | 40 | 47 | 8 | 48 / 95 | 157 | 0.053 | 0.753 |
| 2026 | 21 | 27 | 6 | 27 / 45 | 148 | 0.085 | 0.858 |

The 8 positive-benefit frames in seed42 provide +8 retrospectively recoverable GT objects, but one OTHER frame loses a GT match when joint NMS is applied, leaving the operational always-joint net gain at +7. The privileged frame oracle avoids that harmful frame and reaches 48 rather than 47 GT matches. This is direct evidence that object complementarity and a policy-induced matching loss can coexist. It does **not** show that 48/98 recall is acceptable.

Without GT a router cannot know those 6–8 frames. For the same three seeds, U_safety ROC AUC is far BELOW 0.5, indicating strongly reversed ranking in this small development set. U_all instead yields 0.753–0.865, but this is **ranking only**, and no threshold has been prospectively calibrated or independently tested. Since best.pt checkpoints were previously selected using source-domain validation, the ranking estimates may be optimistic/unstable.

## New result B: Y-PPE validation, Y expert as primary

**356 frames, 126 with safety GT, 345 annotated safety violations.**

| Seed | Y-alone TP / 345 | Always-joint TP / 345 | Positive-benefit frames / 356 | GT-privileged oracle TP / FP | Always-joint FP | AUC U_safety | AUC U_all |
|---|---:|---:|---:|---|---:|---:|---:|
| 17 | 111 | 113 | 2 | 113 / 50 | 54 | 0.194 | 0.446 |
| 42 | 119 | 122 | 3 | 122 / 61 | 74 | 0.297 | 0.384 |
| 2026 | 133 | 134 | 1 | 134 / 95 | 108 | 0.042 | 0.042 |

Positive-benefit prevalence is only **0.28%–0.84%** of frames. AUC calculated on 1–3 positives can fluctuate severely, and is a *diagnostic*, not a hypothesis-test p-value or population-level inference. A privileged oracle needing only 1–3 additional invocations is a hypothetical upper bound, not a viable selective controller.

## Additional nonprivileged fixed-grid check: Construction C-primary

As a further **development diagnostic**, \`U_all >= 0.25\` selects the secondary on **46/132, 31/132, 16/132** frames and results in **19/98, 42/98, 23/98** matched violations across seeds 17/42/2026, versus full always-joint **20/98, 47/98, 27/98**. This signal cannot retain all fused recall. This cutoff was part of a previously implemented five-point development-only signal grid, but it is not frozen for a test or suitable for field safety.

The prior \`U_safety >=0.50\` heuristic had escalated **131/132, 116/132, 116/132** frames for Construction primary and achieved **19/98, 42/98, 24/98** matches. Cross-threshold comparisons here are *descriptive* and cannot be treated as a controlled equated-TP efficiency comparison.

## Scientific interpretation and remaining blockers

1. **Value is sparse at the frame level**: a theoretically perfect selector would need very few secondary calls for the observed additional true positives, but exact-benefit labels require unavailable real-time GT.
2. **Feature definition matters**: reversing the intuitive safety-only uncertainty signal and observing a more informative all-class confidence ranking makes a testable routing hypothesis, but **none is independently validated**, and optimizing it against this very small development sample risks overfitting.
3. **Absolute safety remains inadequate**: even favorable best.pt Construction joint TP is 47/98 (47.96%) with 157 false detections in seed42; more missed than detected critical objects. Relative equivalence to this reference is not operational safety evidence.
4. **Source independence unknown**: frozen manifests do not establish true independent worksite/camera/video group IDs; bootstrap by frame cannot be interpreted as site-generalization inference.
5. **NO-GO remains for positive energy/safety claims**: obtain independent absolute safety criteria and stronger experts or adjusted question, freeze a simple routing policy only on designated development portions, then evaluate on independent test **once** if justified. Energy requires properly instrumented hardware and controller overhead.

**Possible revised contribution (not asserted as novel):** *value-of-information and false-alarm audit of conditional multi-expert PPE safety inference under checkpoint-policy and domain shift*. Cascades, selective prediction and domain adaptation are already established; a genuine publication contribution would need rigorous ablations, external/grouped verification, reproducibility and adequately scoped novelty, not a blanket claim that selective expert inference was invented here.
