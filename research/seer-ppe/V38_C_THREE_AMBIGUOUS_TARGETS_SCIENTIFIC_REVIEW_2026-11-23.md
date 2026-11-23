# V38-C — Scientific review of three ambiguous target maps (no new inference)

**Date:** 23 November 2026. **Study:** 24 original Valid images; 48 frozen detection targets; same RF-DETR Small model; real one-time inference completed with 4,984 successful calls. The archive remains unchanged.

## Main conclusion

Exactly **3/48** prospectively selected targets had an ambiguity at one or more of their 8×8 or 4×4 single-cell perturbation outcomes, so their cross-resolution Spearman, Kendall tau-b and top-four overlap were recorded **null**, not zero. The remaining **45/48 (93.75%)** provide valid spatial summary coefficients.

## Affected exact frozen targets

| Case | PPE class | Immutable target ID | Ambiguous 8×8 cells | Ambiguous 4×4 cells | Progressive-curve status |
|:--|:--|:--|--:|--:|:--|
| 1 | No Safety Vest | f1a0f1b9-d7bd-4be1-8c42-18588349574a | 1 | 0 | NOT_RUN |
| 2 | Safety Vests | 02eeeb67-d8d1-4652-8b99-9df315d9a53e | 4 | 4 | NOT_SELECTED |
| 3 | Hard Hat | e8d236fd-7b12-454e-a12b-1d8791da238f | 2 | 2 | NOT_SELECTED |

These are **13** ambiguity-flagged target-region observations in the pair of direct gray maps across the selected target instances. They arose under the frozen same-class matched-detection rule and its tie margin. The original response ledger records their unusable scores explicitly as missing. The underlying outputs do **not establish which of several possible scenarios** occurred (e.g., a different same-class instance became competitive, temporary localization shift, or a true loss): explaining which requires additional annotated observation or carefully authorized qualitative review. It must **not** be inferred simply from a missing scalar.

## Why each case matters

- **No Safety Vest:** one undefined 8×8 region is sufficient to invalidate its 16-cell rank comparison; this same target was preselected for progressive curves, and those curves were not run. **No replacement target** was substituted. The protocol correctly retained the missing AUC.
- **Safety Vests:** four undefined fine and four undefined coarse responses mean rank comparison is not available; treating these as zero would distort both ranks and region overlap.
- **Hard Hat:** two ambiguous fine and two ambiguous coarse responses were flagged and retained. The target cannot be used to estimate the paired correlation.
- It would be invalid to report 48 estimated correlations or to claim 3/48 negative results. The missing results may not be missing at random, and the 45 available targets are a **conditional estimable subset**. The complete target selection denominator remains 48.

## Quantitative consequences and reporting

- Rankable target maps: **45 of 48**. Means: Spearman rho **0.648979**, Kendall tau-b **0.519741**, top-four overlap **66.6667%** among those 45.
- Descriptive 24-image balanced rho **0.650758**; image resampling 95% percentiles **0.594957–0.704350**; neither is an independent-site generalization interval.
- Progressive-curve subset: **12 selected**, **11 run**, **1 blocked** due to fine-grid ambiguity; **264 valid curves** belong to the 11 run targets and cannot justify counting the blocked target as success.
- Occlusion-fill controls also have varying missing denominators: **15** valid blur-filled rho, **14** paired valid gray/blur rho. The proper paired rho difference (blur minus gray) is **−0.213166** for n=14, not a difference of separate cohort means.

## Research verdict

This is appropriate conservative scientific handling of uncertain detection identity and should be **emphasized as a methodological integrity check**, not hidden as a technical error. A reviewer may still ask for an identity-aware tracking/same-class object matching benchmark, especially in cluttered scenes; those results have not been measured and must not be invented. The current observations do not establish worker-to-PPE association or independent deployment safety.

**Evidence:** archived complete V38-B result JSON and append-only write-ahead attempt ledger; independently audited 48-target summary; V38-C S2 includes all 48 rows and records the ambiguous cases. No model calls, retraining or Test image exposure were performed for this V38-C review.
