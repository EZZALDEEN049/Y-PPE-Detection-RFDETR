# SEER-PPE V33-B — actual 4×4 grid-resolution robustness experiment

**Execution date:** 22 November 2026  
**Status:** COMPLETED; one authorized run; no retries  
**Experiment run:** [GitHub Actions 45019831430](https://github.com/EZZALDEEN049/Y-PPE-Detection-RFDETR/actions/runs/45019831430)  
**Read-only preflight:** [GitHub Actions 45019722753](https://github.com/EZZALDEEN049/Y-PPE-Detection-RFDETR/actions/runs/45019722753)  
**Independent numeric audit CI:** [GitHub Actions 45020503717](https://github.com/EZZALDEEN049/Y-PPE-Detection-RFDETR/actions/runs/45020503717)  
**Primary result:** [V33-B actual results JSON](V33_B_GRID4_ACTUAL_RESULTS_2026-11-22.json)  
**Independent audit:** [V33-B numeric audit JSON](V33_B_GRID4_NUMERIC_AUDIT_2026-11-22.json)  
**V30 comparator:** [V30 actual 8×8 results](V30_ACTUAL_PROGRESSIVE_XAI_RESULTS_2026-11-22.json)

## 1. Question and frozen design

V33-B tests whether the target-specific perturbation-sensitivity findings from the completed V30 8×8 grid are stable when the same detector, original images and ten frozen target detections are evaluated with a coarser **4×4 grid**. It is a within-target grid-resolution sensitivity experiment, not an independent validation cohort or randomized policy trial.

The experiment reused exactly eight development-exposed original images (four Train and four Valid), ten frozen target IDs, the original hosted RF-DETR Small model altayyar-0oflt-lafos-qqauz/2, confidence threshold 0.20 and overlap threshold 0.50. The original-image baseline calls were reused; no new baseline calls were made. The 4×4 map used 16 single-cell neutral-gray occlusions per image, with actual pixel-area fractions. Each target then received one deterministic SHA-256(target-ID)-seeded random order and a saliency order, each evaluated with deletion and insertion curves at 0%, 10%, …, 100%.

The read-only preflight downloaded only the eight frozen Train/Valid source images, verified dimensions and matched all eight SHA-256 values to the previously archived V30 cloud-runner image bundle. All ten frozen target identities, classes, coordinates, baseline confidences and A5/A6 assignments passed. These are **repeatability hashes of the V30 downloaded bundle**, not independent source-side checksums. Test was not accessed.

## 2. Execution and call accounting

The one-time authorized workflow completed successfully on its first attempt:

| Phase | Successful hosted calls |
|:--|--:|
| Gaussian-blur endpoints (one per image) | 8 |
| 4×4 single-cell occlusions (16 per image) | 128 |
| Curve-intermediate calls (40 curves × 9 points) | 360 |
| **Total additional calls** | **496/496** |

There were **496 attempted, 496 successful and zero failed calls**, no automatic retries, ten curve-eligible targets and 40 curve contexts. The write-ahead ledger has contiguous call indices 1–496 and all rows are SUCCEEDED. The hard 496-call ceiling was not exceeded.

The experiment made no changes to images, annotations, splits or model weights; no retraining or Test access occurred. The run and numeric-only backup completed successfully.

## 3. 4×4 curve and saliency-versus-random results

All ten 4×4 target maps were rankable. The ten targets generated 40 eleven-point curves. **Thirty-nine AUCs were valid**; one saliency-deletion AUC was correctly withheld because one intermediate target match was ambiguous. No missing AUC was imputed.

| Curve | Curves | Valid AUCs | Null AUCs |
|:--|--:|--:|--:|
| Saliency deletion | 10 | 9 | 1 |
| Saliency insertion | 10 | 10 | 0 |
| Random deletion | 10 | 10 | 0 |
| Random insertion | 10 | 10 | 0 |
| **Total** | **40** | **39** | **1** |

For deletion, saliency is favorable when its AUC is lower than random; for insertion, saliency is favorable when its AUC is higher than random.

| Diagnostic | Favorable targets | Unfavorable | Unscored |
|:--|--:|--:|--:|
| Saliency vs. random — deletion | **8/9** | 1/9 | 1/10 |
| Saliency vs. random — insertion | **10/10** | 0/10 | 0/10 |

The deletion advantage (random AUC − saliency AUC) had mean **+0.162915**, median **+0.018301**, range **−0.062500 to +0.711114**; three of nine absolute margins were below 0.01 and four exceeded 0.05. The insertion advantage (saliency AUC − random AUC) had mean **+0.229045**, median **+0.156418**, range **+0.001838 to +0.875092**; one of ten margins was below 0.01 and eight exceeded 0.05. These are descriptive target-level contrasts against **one** deterministic random ordering per target, not a random-seed distribution or inferential test.

### The single ambiguous curve point

The only null AUC is for the **Safety Boots** target in valid:09WO3iVNf9jOt21QAxmb, saliency deletion. At requested 20% deletion, the actual modified image area was **18.7431%**. Two same-class detections met the matching ambiguity rule; the best candidate IoU was **0.519474**, but the IoU margin was insufficient to choose a unique target match. The point remains AMBIGUOUS and the saliency-deletion AUC remains null. This is the intended fail-closed behavior, not a failed inference.

## 4. Paired 4×4 versus 8×8 resolution comparison

The comparison pairs the exact same ten target IDs and the stored V30 8×8 curves. AUC deltas below are **4×4 minus 8×8**; lower deletion AUC is favorable, whereas higher insertion AUC is favorable.

| Metric | Paired n | Mean delta | Median delta | Positive / negative deltas |
|:--|--:|--:|--:|:--:|
| Saliency deletion AUC | 9 | −0.021799 | +0.013040 | 5 / 4 |
| Saliency insertion AUC | 10 | −0.017560 | −0.001365 | 4 / 6 |
| Random deletion AUC | 10 | −0.013424 | +0.007614 | 5 / 5 |
| Random insertion AUC | 10 | −0.111982 | −0.080256 | 1 / 9 |

The deletion mean and median move in opposite directions, demonstrating target heterogeneity rather than a uniform resolution effect. The insertion mean delta is slightly negative and its median is close to zero; neither establishes universal equivalence or superiority of one grid.

The **sign of saliency's advantage over the single random control** was preserved across grid resolutions for:
- deletion: **6/9 comparable targets**, changed in 3/9, with one target not comparable because the 4×4 saliency-deletion AUC is null;
- insertion: **9/10 targets**, changed in 1/10.

All **10/10** targets retained the categorical RANKABLE map status at both resolutions. This is only agreement in map eligibility; it is **not** a spatial rank-correlation or cell-by-cell attribution-map stability measure.

The evidence therefore supports **partial, direction-dependent resolution robustness**: insertion-versus-random ordering was more consistent across 4×4 and 8×8 than deletion-versus-random ordering. It does not support a blanket claim that the spatial saliency ranking itself is stable across grid resolutions.

## 5. A5/A6 target-selection composition

A5 and A6 each selected eight target slots: **six shared target IDs and two unique target IDs per arm**. The shared targets reuse the same target-level 4×4 explanation outputs; there is no separate explanation result for the same target under each policy.

- A5-only: Train C — No Safety Boots; Valid 0ABzMrjnd6I0Ws6FH7qo — No Face Mask.
- A6-only: Train C — Face Masks; Valid 0ABzMrjnd6I0Ws6FH7qo — Safety Vests.

On the six shared targets, the saliency deletion AUC mean was **0.493773** across five valid curves, and the insertion AUC mean was **0.912089** across all six. These values are identical for the common A5 and A6 target subset.

The archived all-slot means (A5 deletion/insertion **0.487529/0.922048**; A6 **0.415104/0.848435**) differ because the two arms contain different unique detections and because one shared deletion AUC is missing. They are not a matched comparison of explanation algorithms and **do not establish A5 or A6 superiority**.

## 6. Independent numeric audit

The independent read-only audit in tools/audit_v33b_grid4_xai.py passed in engineering CI. It checked:
- ten exact target IDs against the V30 manifest and result archive;
- eight source-image hash matches to the archived V30 cloud-runner bundle;
- model ID, confidence/overlap settings, target geometry, classes and A5/A6 assignments;
- the 496-call ledger, contiguous indices, phase counts, 40 curve contexts and nine intermediate calls per curve;
- 4×4 map dimensions, finite importance values and 16-cell area partitioning;
- all 40 eleven-point curves and recomputation of every available AUC from actual modified pixel-area fractions;
- paired target-level 4×4/8×8 metrics and the A5/A6 shared/unique composition;
- no-Test, no-retraining and no-original-data-modification guardrails.

The maximum absolute difference between recomputed and archived valid AUCs was **2.22×10⁻¹⁶**. The audit passed without any additional model inference.

## 7. Scientific interpretation and limits

**Supported:** the frozen 4×4 experiment executed successfully; all ten maps were rankable; saliency was favorable against one fixed random order in 8/9 scorable deletion curves and 10/10 insertion curves; and insertion-direction advantage was more consistent than deletion-direction advantage when comparing 4×4 with 8×8.

**Not supported:** universal spatial-map stability, independent/external generalization, causal explanation faithfulness, A5/A6 policy superiority, worker-level PPE compliance, false-clearance reduction, actual human-review efficacy, safety improvement, electrical-energy savings or financial-cost conclusions.

The ten targets were selected from development-exposed V27/V28 work, and multiple targets share images. The eight images are not an independent site sample. One random permutation per target does not quantify random-seed variance. AUC describes this detector's response to this particular neutral-gray/blur perturbation protocol, not external explanation truth. The categorical 10/10 rankability match must not be described as a map-rank correlation.

## 8. Next analysis

The next low-cost analysis should align the archived 8×8 and 4×4 importance maps in common image coordinates and compute descriptive spatial-rank agreement (for example, area-weighted pooling of 8×8 cell responses onto the 4×4 partition, followed by per-target rank correlation). This can be performed from the archived maps without additional hosted calls. Repeated random seeds or alternative masking/blur baselines would require a separate prospective design and budget; they are not part of V33-B.

**Boundary:** no Test access, no retraining, no changes to original images/annotations/splits, no worker-level safety scoring, and no causal or energy claims.
