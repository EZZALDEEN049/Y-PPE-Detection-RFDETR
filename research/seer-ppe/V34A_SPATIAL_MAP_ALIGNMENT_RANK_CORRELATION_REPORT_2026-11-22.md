# SEER-PPE V34-A — Spatial Map Alignment & Rank Correlation

**Analysis date:** 22 November 2026  
**Status:** Completed; offline-only; zero new model inference  
**Canonical branch:** research/v30-progressive-xai-2026-11-22  
**Primary archive:** [V34-A aligned maps and correlations](V34A_SPATIAL_MAP_ALIGNMENT_RANK_CORRELATION_2026-11-22.json)  
**Analysis script:** [analyze_v34a_spatial_map_alignment.py](tools/analyze_v34a_spatial_map_alignment.py)  
**Synthetic tests:** [test_v34a_spatial_map_alignment.py](tests/test_v34a_spatial_map_alignment.py)  
**V30 source maps:** [8×8 actual results](V30_ACTUAL_PROGRESSIVE_XAI_RESULTS_2026-11-22.json)  
**V33-B source maps:** [4×4 actual results](V33_B_GRID4_ACTUAL_RESULTS_2026-11-22.json)

## 1. Objective

V34-A measures how closely the **spatial ranking** of the original V30 8×8 single-cell gray-occlusion sensitivity maps agrees with the independently executed V33-B 4×4 maps for the same ten frozen target detections. Unlike the earlier 10/10 categorical RANKABLE comparison, this analysis compares the signed spatial response values over corresponding image regions.

This is a retrospective numerical analysis of archived outputs. It does not call RF-DETR, access Test, retrain the detector, or modify images, annotations, splits or Roboflow data.

## 2. Exact coordinate and area alignment

All source maps were joined by the frozen target_id, image key, class and A5/A6 assignment. The original image dimensions came from the V30 frozen target manifest.

Both runners use the same floor-based pixel-boundary rule:

\[
x_0=\left\lfloor\frac{cW}{C}\right\rfloor,\quad
x_1=\left\lfloor\frac{(c+1)W}{C}\right\rfloor
\]

\[
y_0=\left\lfloor\frac{rH}{R}\right\rfloor,\quad
y_1=\left\lfloor\frac{(r+1)H}{R}\right\rfloor
\]

For each 4×4 cell (r,c), its spatial footprint is exactly the union of the four 8×8 children (2r,2c), (2r,2c+1), (2r+1,2c), and (2r+1,2c+1). The actual pixel bounds and normalized pixel bounds are stored for each coarse region and each fine child in the machine-readable archive.

### Primary area-normalized signed sensitivity

For any occluded cell j, the frozen sensitivity value is:

\[
d_j = s_{\mathrm{baseline}}-s_{\mathrm{occluded},j}
\]

The signed per-area value is \(q_j=d_j/a_j\), where \(a_j\) is the exact pixel-area fraction of that cell in the original image.

For each coarse 4×4 region, the direct value is \(d_4/a_4\). Its aligned 8×8 value is the area-weighted mean of the four child densities:

\[
q_{8\rightarrow4} =
\frac{\sum_{j=1}^{4} d_{8,j}}{\sum_{j=1}^{4} a_{8,j}}
\]

Because the four child areas exactly partition the coarse region, the denominator equals \(a_4\). Thus the comparison is between direct coarse-mask sensitivity density and area-pooled fine-mask sensitivity density over the same image footprint.

Negative score drops are retained as signed values; they are not clipped, removed or converted to absolute values. This differs intentionally from the V30/V33-B saliency-order construction, which clips negative values to zero for the deletion/insertion ordering. V34-A asks whether the **signed sensitivity maps** agree spatially, not whether the exact curve ordering was reproduced.

### Correlation and secondary diagnostics

- **Spearman ρ:** average ranks for tied values, computed across the 16 aligned regions per target.
- **Kendall τ-b:** pairwise rank concordance with tie correction.
- **Area-weighted Spearman:** sensitivity summary using each 4×4 region's exact area fraction as a rank-correlation weight.
- **Top-four overlap:** number of common regions among the four highest signed values in each aligned 4×4 map; ties are resolved row-major.
- **Secondary additive diagnostic:** compare direct 4×4 raw score drop with the sum of the four 8×8 child drops. This is descriptive only; perturbation responses need not be additive.

No cell-level p-values are reported. The 16 spatial regions within an image are dependent, and targets can share an image.

## 3. Integrity and geometry checks

| Check | Result |
|:--|--:|
| Frozen target IDs matched | 10/10 |
| Unique source images | 8 |
| V30 8×8 maps rankable | 10/10 |
| V33-B 4×4 maps rankable | 10/10 |
| 8×8 importance-map vs. trial maximum absolute difference | 0 |
| 4×4 importance-map vs. trial maximum absolute difference | 0 |
| Maximum 4×4 area vs. four-child 8×8 area discrepancy | \(6.94\times10^{-18}\) |
| Null cell scores | 0 |
| V30 8×8 LOST cell outcomes | 26 |
| V33-B 4×4 LOST cell outcomes | 17 |
| New detector inference calls | **0** |

The 43 LOST cell outcomes are not missing observations: the frozen protocol assigns a lost target score of zero, so the baseline-minus-zero score drop remains numeric. No ambiguous cell score was imputed.

## 4. Overall spatial rank agreement

| Metric | Mean across 10 targets | Median | Range |
|:--|--:|--:|--:|
| Spearman ρ, signed area-normalized maps | **0.5416** | 0.5656 | 0.2295 to 0.6794 |
| Kendall τ-b, signed area-normalized maps | **0.4239** | 0.4384 | 0.1514 to 0.5500 |
| Area-weighted Spearman ρ | **0.5413** | 0.5655 | 0.2296 to 0.6787 |
| Secondary raw additive-drop Spearman | 0.5353 | 0.5509 | 0.2295 to 0.6755 |
| Secondary raw additive-drop Kendall τ-b | 0.4203 | 0.4467 | 0.1514 to 0.5500 |

All **10/10** target-level Spearman coefficients and all **10/10** Kendall coefficients were positive. The area-weighted and unweighted Spearman summaries are nearly identical, consistent with the relatively small pixel-area differences among the 16 coarse regions.

The mean top-four overlap was **2.6 of 4 regions (65%)**:
- 8 targets shared 3 of their top 4 regions;
- 1 target shared 2 of 4;
- 1 target shared 0 of 4.

These values indicate **moderate positive spatial rank agreement**, not near-identical maps or full spatial stability.

## 5. Per-target results

| Split / image | Target class | Spearman ρ | Kendall τ-b | Top-four overlap |
|:--|:--|--:|--:|--:|
| Train A | No Face Mask | 0.547 | 0.417 | 3/4 |
| Train B | Gloves | 0.602 | 0.527 | 3/4 |
| Train C | No Safety Boots | 0.555 | 0.427 | 3/4 |
| Train C | Face Masks | **0.230** | **0.151** | **0/4** |
| Train D | Hard Hat | 0.576 | 0.467 | 2/4 |
| Valid 07BnOpgFJyNaOhuzvh5i | No Gloves | 0.538 | 0.400 | 3/4 |
| Valid 09WO3iVNf9jOt21QAxmb | Safety Boots | 0.626 | 0.550 | 3/4 |
| Valid 0ABzMrjnd6I0Ws6FH7qo | No Face Mask | 0.632 | 0.450 | 3/4 |
| Valid 0ABzMrjnd6I0Ws6FH7qo | Safety Vests | **0.679** | 0.533 | 3/4 |
| Valid 0aGYjxE5LmocXyvuLHs8 | No Safety Boots | 0.429 | 0.317 | 3/4 |

### Main target-level discrepancy

The Train C **Face Masks** target is the clear low-agreement case: Spearman 0.230, Kendall 0.151 and zero shared top-four regions. This is a measured disagreement between perturbation maps at two mask scales. It does not, by itself, identify whether the cause is target size, confidence, local interactions, masking artifacts or detector nonlinearity; those explanations would require separate evidence.

## 6. Train and Validation descriptive summaries

| Split | Targets | Unique images | Mean Spearman | Mean Kendall τ-b | Mean top-four overlap |
|:--|--:|--:|--:|--:|--:|
| Train | 5 | 4 | 0.5020 | 0.3978 | 55% |
| Validation | 5 | 4 | 0.5812 | 0.4500 | 75% |

These are descriptive summaries only. The eight images were development-exposed, each split contains only four unique images, and Train C and Valid 0AB each contribute two target detections from one image. The Validation subset is not independent-site or external validation and the apparent split difference is not tested for significance.

## 7. Interpretation

V34-A adds the missing **spatial** comparison to V33-B's earlier categorical map-rankability check. It shows that the 4×4 and 8×8 maps generally preserve a positive ordering relationship, but only moderately. The top-four overlap is 65% on average, and one target has no top-four overlap at all. Consequently, the appropriate conclusion is:

> The signed perturbation-sensitivity maps show moderate, target-dependent spatial rank agreement between 4×4 and 8×8 resolutions on the frozen development-exposed sample. The agreement is not sufficiently uniform to claim that the maps are spatially interchangeable or resolution-invariant.

The secondary raw-drop aggregation produces similar mean rank correlations, which suggests that the overall conclusion is not an artifact of the per-area normalization choice. It does not validate an additive perturbation model: occluding a 4×4 region in one inference is not mathematically equivalent to summing four separate 8×8 occlusions, because the detector's response can be nonlinear and the interventions differ in mask size.

V34-A does **not** establish external explanation truth, causal faithfulness, worker-level PPE compliance, human-review efficacy, A5/A6 policy superiority, safety improvement or generalization to independent worksites. It remains an image/object-level model-response analysis.

## 8. Reproducibility and next work

The independent offline analyzer reads only the archived V30, V33-B and frozen-manifest JSON files. It validates target identity, map/trial arithmetic, pixel geometry, area partitioning and signed rank statistics. Synthetic tests cover tied ranks, Spearman direction, Kendall τ-b, row-major top-k ties and exact 4×4/8×8 pixel-boundary alignment. Engineering CI passed.

The next useful step is **figure generation from the archived aligned maps**: paired 4×4 heatmaps for all ten targets, using a common signed scale and showing the top-four region overlap. Any future random-seed or alternative-fill/blur experiment must have a separate prospective protocol and budget.

**Boundary:** zero new model calls; no Test access; no retraining; no changes to source images, annotations or splits; no causal, worker-safety, energy or A5/A6 superiority claim.
