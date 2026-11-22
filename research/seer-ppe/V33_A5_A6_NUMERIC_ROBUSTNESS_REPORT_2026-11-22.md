# SEER-PPE V33 — A5/A6 matched-target comparison and XAI numeric robustness

**Executed:** 22 November 2026  
**Design:** post-hoc reanalysis of completed real V30 evidence; **zero new model calls**  
**Evidence:** [machine-readable V33 numerical record](V33_A5_A6_NUMERIC_ROBUSTNESS_2026-11-22.json) · [source V30 curves](V30_ACTUAL_PROGRESSIVE_XAI_RESULTS_2026-11-22.json) · [V30 independent numeric audit](V30_INDEPENDENT_NUMERIC_AUDIT_2026-11-22.json) · [V33 reproducibility validator](tools/verify_v33_existing_xai.mjs)

## 1. Question and method

The V32 manuscript asks whether A5/A6 target-selection policies differ in *which image-level detections* they select for additional black-box explanation under matched budgets. It does not test safety compliance. V30 ran the **same target-specific 8×8 perturbation algorithm** on **ten unique detections across eight development-exposed original images**. A5 and A6 each selected eight targets, with **six shared target IDs and two nonshared target IDs per arm**.

V33-A recalculated every stored curve's trapezoidal AUC from the actual modified-pixel fractions; compared saliency against the single frozen random ordering; recomputed early 0–30% partial AUC (linearly interpolated at exactly 30% actual modified area); tested area-fraction discretization; checked inverse-order algebraic identities; and performed leave-one-source-image-out and **conditional balanced reassignment** diagnostics across the four nonshared targets. No additional image was downloaded or inferred, no Test data accessed, and no original data/model changed.

For the conditional diagnostic, keep the six shared targets fixed and assign two of the four nonshared targets to A5 (the remaining two to A6); there are **C(4,2)=6** balanced allocations. A two-sided tail fraction counts allocations with an absolute A5–A6 mean difference at least as large as observed. **This is a post-hoc combinatorial sensitivity check, not a valid randomized-trial p-value or confirmation of superiority.**

## 2. Actual results

| Indicator | A5 (8 slots) | A6 (8 slots) | Interpretation |
|---|---:|---:|---|
| Saliency deletion AUC, lower better | 0.496288 | 0.397182 | A6 lower |
| Saliency insertion AUC, higher better | 0.944195 | 0.871354 | A5 higher |
| Random deletion AUC | 0.635836 | 0.619275 | One fixed random order/target |
| Random insertion AUC | 0.800164 | 0.752773 | One fixed random order/target |
| Deletion advantage (random − saliency) | +0.139549 | +0.222093 | A6 larger |
| Insertion advantage (saliency − random) | +0.144031 | +0.118581 | A5 larger |
| First 30% deletion advantage | +0.300943 | +0.438694 | Early-area diagnostic |
| First 30% insertion advantage | +0.211354 | +0.257544 | Early-area diagnostic, A6 larger |

Across **all ten unique targets** (not 16 arm slots), saliency exceeded the fixed random control for deletion in **8/10** (one tie, one worse) and for insertion in **9/10**. The first-30%-area advantage occurred in **8/10** targets for each direction. These are descriptive counts, not claims of independent-target sampling.

## 3. Matched-target policy comparison

The **six shared A5/A6 targets have identical saliency maps and identical deletion/insertion AUCs**, because V30 inferred each shared target once and reused its result in both arms. Therefore, the apparent arm-mean differences are **selection-composition effects**, not differences in explanation quality for the same target.

| Conditional six-allocation diagnostic | Observed A5 − A6 | Two-sided conditional tail fraction |
|---|---:|---:|
| Saliency deletion AUC | +0.099106 | 4/6 = 0.667 |
| Saliency insertion AUC | +0.072841 | 2/6 = 0.333 |
| Deletion advantage over random | −0.082545 | 2/6 = 0.333 |
| Insertion advantage over random | +0.025450 | 4/6 = 0.667 |

These six allocations cannot support a confirmatory claim of either arm's statistical superiority. Because the selection policies are not randomized assignments, the tail fractions should **not** be presented as conventional inferential p-values or as evidence that the policies are equivalent.

**Leave-one-source-image-out diagnostic:** A5 − A6 deletion AUC ranged from **+0.000007 to +0.113264**; insertion AUC ranged from **+0.011976 to +0.083247**. The sign of the A5 − A6 **insertion advantage-over-random** reversed in **one of eight** image omissions (range **−0.036682 to +0.065767**). This indicates sensitivity of the preferred comparison metric to source-image composition.

## 4. Technical sensitivity and controls

- **Actual vs nominal modified area:** re-integrating the stored curves with nominal 0%, 10%, …, 100% x-values instead of actual pixel-area fractions changed per-target AUC by at most **0.004748**. The archived actual-area integration reproduced every AUC with maximum absolute error **2.22×10⁻¹⁶**.
- **Blurred baseline saturation:** six targets had zero matched confidence in the fully blurred endpoint; three of ten retained **at least 80%** of the original target confidence after full-image Gaussian blur, and one retained **at least 90%**. High insertion/deletion AUCs for a blur-resistant target may reflect this ceiling/floor constraint instead of high explanatory informativeness. Stratify future studies by baseline-to-blur response.
- **Inverse order is not an independent control:** for this complementary masking scheme, inverse-saliency deletion AUC numerically equals saliency insertion AUC, and inverse-saliency insertion AUC equals saliency deletion AUC, within **1.11×10⁻¹⁶**. Treat these as algebraically related views, not independent experimental replications.
- **Random control limitation:** only **one deterministic random order per target** was run in V30. Random-seed stability and actual 4×4-versus-8×8 inference robustness have **not yet been measured**; an aggregation of archived cells must not be presented as a new 4×4 inference result.

## 5. Scientific conclusion and limitations

**Supported:** the fixed detector's selected detections respond measurably to target-specific perturbations; saliency order often performs better than a single seeded random control; A5/A6 select meaningfully different target compositions under equal target budgets.

**Not supported:** A5 and A6 generate different explanations on an identical shared target; statistical policy superiority; causal/external explanation faithfulness; worker-level Person–PPE compliance or safety efficacy; electrical energy savings; independently sampled image/site generalization.

The development-exposed sample has only eight source images, ten unique targets, and one random order per target. Multiple targets can share an image, so grid cells, curves and arm slots are **not independent experimental units**.

## 6. Next prospective V33-B experiment (not executed here)

A genuinely new robustness experiment would freeze a **4×4 grid** on the same eight source images and ten target IDs, keep the same hosted 17-class RF-DETR Small checkpoint and matching/blur rule, and compare a newly inferred 4×4 saliency map against at least one random-order control. With two orderings and both curve directions, the upper inference budget is **496 additional hosted calls** (8 Gaussian endpoints + 128 single-cell occlusions + 360 intermediate curve calls). This experiment must receive a separate, explicit inference-budget authorization and archive source hashes before it can be counted as actual V33-B evidence. **No such V33-B inferences are claimed by this report.**

## 7. Reproducibility and frozen boundaries

Run:

```bash
node research/seer-ppe/tools/verify_v33_existing_xai.mjs --self-test
node research/seer-ppe/tools/verify_v33_existing_xai.mjs --verify
```

The fail-closed test checks the immutable V30 source Git-blob SHA, all 60 actual-area AUCs, all ten IDs, the six shared targets, six balanced assignment outcomes, image-omission results, baseline response, and no new model calls. It also rejects mutations to target identities, group membership, curve AUC, modified fractions, model-call budget and the independence/control flags.

**Boundary:** no retraining, no Test opening, no annotation/split changes, no repeated full-dataset review, no inferred worker-compliance labels, and no new energy/causal-faithfulness claims.
