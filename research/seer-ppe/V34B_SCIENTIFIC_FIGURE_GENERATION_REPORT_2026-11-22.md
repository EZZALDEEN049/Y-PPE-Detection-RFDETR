# SEER-PPE V34-B — Data-derived scientific figures

**Date:** 22 November 2026  
**Status:** PASSED — ten target figures and one summary figure generated and numerically validated  
**Execution:** offline-only; zero new detector/model inference calls  
**Source archive:** [V34-A aligned maps and rank correlations](V34A_SPATIAL_MAP_ALIGNMENT_RANK_CORRELATION_2026-11-22.json)  
**Renderer:** [render_v34b_scientific_figures.py](tools/render_v34b_scientific_figures.py)  
**Synthetic tests:** [test_v34b_scientific_figures.py](tests/test_v34b_scientific_figures.py)

## 1. Scope and source data

V34-B converts the ten archived V34-A spatial-sensitivity map pairs into reproducible, publication-style figures. It does not generate new explanation values. All displayed cell values come from the frozen V34-A JSON archive, which itself was derived from the actual V30 8×8 and V33-B 4×4 gray-occlusion trials.

For each target, the left panel reconstructs the native 8×8 map from the 64 fine-cell signed score drops divided by their exact original-pixel area fractions. The right panel shows the direct 4×4 signed score-drop density. For spatial ranking, the 8×8 map is pooled into the 16 aligned 4×4 footprints exactly as in V34-A; Spearman ρ and Kendall τ-b are computed across these 16 corresponding regions, **not** across 64 fine cells against 16 coarse cells.

The four gold outlines on the 8×8 panel show the 2×2 fine-cell footprints of the four highest-ranked pooled 4×4 regions. The four gold outlines on the direct 4×4 panel show that map's own four highest-ranked regions. The displayed overlap is the intersection of these two four-region sets.

## 2. Shared color scale and clipping policy

A single symmetric diverging scale centered at zero is shared across all ten target figures and both displayed resolutions. The absolute scale limit is the 97.5th percentile of the absolute values across the 800 displayed cells (10 targets × (64 fine cells + 16 direct coarse cells)):

- Colormap: RdBu_r (blue negative, white near zero, red positive)
- Center: 0
- Shared display limit: **±15.470900859749108**
- Saturated values: **17/800 (2.125%)**

The 17 values beyond the common limit are saturated only in the rendered colors. They are **not clipped in the source archive**, and all rankings, top-four selections, Spearman coefficients and Kendall coefficients are calculated from the original un-clipped values. This robust shared scale preserves cross-target color comparability while making the small number of extreme values explicit.

## 3. Reproducibility checks

The renderer independently:
1. Matched all ten target IDs between the V34-A target summaries and aligned-map records.
2. Reconstructed all 64 8×8 fine cells and both 4×4 maps for every target.
3. Recomputed direct and pooled top-four sets using the archived row-major tie rule.
4. Recomputed Spearman ρ and Kendall τ-b from the 16 aligned coarse regions and compared them with the V34-A values (absolute tolerance 1e-10).
5. Recomputed top-four overlap counts and matched the V34-A archive.
6. Confirmed all values were finite and all target figures were generated.

All checks passed for 10/10 targets. The two synthetic unit tests also passed. No new model calls, Test access, retraining, image/annotation changes or split changes occurred.

## 4. Per-target results

| Figure | Target | Spearman ρ | Kendall τ-b | Top-4 overlap |
|:--|:--|--:|--:|--:|
| F01 | Train A — No Face Mask | 0.5471 | 0.4167 | 3/4 (75%) |
| F02 | Train B — Gloves | 0.6019 | 0.5272 | 3/4 (75%) |
| F03 | Train C — No Safety Boots | 0.5548 | 0.4268 | 3/4 (75%) |
| F04 | Train C — Face Masks | **0.2295** | **0.1514** | **0/4 (0%)** |
| F05 | Train D — Hard Hat | 0.5765 | 0.4667 | 2/4 (50%) |
| F06 | Valid 07BnOpgFJyNaOhuzvh5i — No Gloves | 0.5382 | 0.4000 | 3/4 (75%) |
| F07 | Valid 09WO3iVNf9jOt21QAxmb — Safety Boots | 0.6265 | 0.5500 | 3/4 (75%) |
| F08 | Valid 0ABzMrjnd6I0Ws6FH7qo — No Face Mask | 0.6324 | 0.4500 | 3/4 (75%) |
| F09 | Valid 0ABzMrjnd6I0Ws6FH7qo — Safety Vests | 0.6794 | 0.5333 | 3/4 (75%) |
| F10 | Valid 0aGYjxE5LmocXyvuLHs8 — No Safety Boots | 0.4294 | 0.3167 | 3/4 (75%) |

The aggregate results remain those of V34-A: mean Spearman ρ=**0.5416**, mean Kendall τ-b=**0.4239**, and mean top-four overlap=**65%**. The figures visualize these already-measured values; they do not constitute additional statistical evidence.

## 5. Outputs

The generated outputs are stored under research/seer-ppe/figures/V34B_2026-11-22/:

- Ten individual 300-dpi PNG target figures, V34B_F01 through V34B_F10
- V34B_SPATIAL_AGREEMENT_SUMMARY_2026-11-22.png
- V34B_PAIRED_HEATMAPS_2026-11-22.pdf (one summary page plus ten target pages)
- V34B_FIGURE_METRICS_2026-11-22.csv
- V34B_FIGURES_MANIFEST_2026-11-22.json
- V34B_FIGURE_GENERATION_REPORT_2026-11-22.md

The manifest records the V34-A source Git blob SHA, source SHA-256, display scale, clipping count, target IDs, per-target metrics, top-four region indices and reproducibility checks.

## 6. Interpretation boundary

V34-B is a rendering and reproducibility stage, not a new inference or validation experiment. The heatmaps show signed detector-response sensitivity under the frozen gray-occlusion protocol. They are not source photographs, human-grounded explanations, causal proof, worker-compliance labels, independent-site validation, or evidence of A5/A6 superiority. The strongest disagreement remains Train C — Face Masks (ρ=0.2295; τ-b=0.1514; top-four overlap 0/4). The defensible interpretation remains **moderate, target-dependent spatial rank agreement**, not spatial interchangeability or resolution invariance.
