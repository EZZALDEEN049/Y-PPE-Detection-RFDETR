# Stage 11C — Reproducible Harmonization and Conservative Filtering

## Status
**COMPLETE.** This document closes the reviewer concern that the semantic harmonization and structural exclusion rule were insufficiently reproducible.

## 1. Source-to-canonical ontology

The benchmark uses the following exact shared class order:

| Canonical ID | Canonical class | Y-PPE source label | Construction-PPE source label |
|---:|---|---|---|
| 0 | person | Persons | Person |
| 1 | helmet | Hard Hat | helmet |
| 2 | gloves | Gloves | gloves |
| 3 | vest | Safety Vests | vest |
| 4 | boots | Safety Boots | boots |
| 5 | goggles | Goggles | goggles |
| 6 | no_helmet | No Hard Hat | no_helmet |
| 7 | no_gloves | No Gloves | no_gloves |
| 8 | no_boots | No Safety Boots | no_boots |

Nonshared classes were not relabeled into shared classes. Y-PPE `No Safety Vest` was excluded because Construction-PPE has no direct `no_vest` counterpart. Construction-PPE `no_goggle` and `none` were excluded because no strict Y-PPE semantic counterpart exists.

Y-PPE polygon annotations in retained classes were deterministically converted to their enclosing axis-aligned bounding boxes. Construction-PPE was already bbox-only.

## 2. Stage 4 keep-all transformation

Before the conservative Stage 4.5 filter, the harmonizer:
1. preserved all clean Stage-2 images in their original split;
2. dropped only annotation rows outside the nine-class shared ontology;
3. wrote empty label files for images with no retained shared annotation;
4. did not move images between train, validation, or test.

This produced:

| Dataset | Train | Validation | Test | Shared instances |
|---|---:|---:|---:|---:|
| Y-PPE-h9 | 1,595 | 459 | 234 | 11,618 |
| Construction-PPE-h9 | 1,077 | 134 | 141 | 9,904 |

## 3. Why Stage 4.5 was required

Dropping a nonshared annotation can create false background if the excluded source object is semantically close to a retained target. Stage 4.5 therefore audited excluded-source boxes against prespecified retained-source boxes.

### Critical source relationships

**Y-PPE**
- `Child` against retained `Persons`;
- `No Safety Attire` against retained `Persons`;
- `Soft Hat` against retained `Hard Hat` or `No Hard Hat`.

**Construction-PPE**
- `none` against retained `Person`.

The Y-PPE `No Safety Vest`→`Safety Vests` and Construction-PPE `no_goggle`→`goggles` relationships were informational only and did not independently trigger exclusion.

## 4. Exact structural match rule

For every excluded box (E) and every candidate retained box (R) from the corresponding critical relationship, the excluded object was considered structurally matched if **either** condition held:

`IoU(E,R) >= 0.50`

**OR**

`area(E ∩ R) / area(E) >= 0.80`

The second criterion is excluded-box containment: at least 80% of the excluded annotation must lie inside the candidate retained annotation.

A `critical_unmatched:<source class>` flag was assigned when a critical excluded object had no retained candidate satisfying either threshold.

This is a **box-to-box annotation-geometry test**. It is not an image-level visual similarity criterion and does not use model predictions.

## 5. Final deterministic image-membership rule

Before Stage 5 training, the final conservative rule was frozen:

> Exclude the entire image if (a) it would become empty after nine-class harmonization, or (b) it contains at least one `critical_unmatched:*` source annotation under the structural match rule above.

If an image contained both shared and nonshared annotations, it was retained **unless** it satisfied one of those two conditions. If a critical excluded annotation was structurally matched to an allowed retained counterpart, that critical annotation did not by itself cause image removal.

The same annotation-only rule was applied to train, validation, and test. Test-image pixels were not opened for membership adjudication, and no model prediction, loss, confidence, or test metric was used.

## 6. Executed exclusion flow

| Dataset | Split | Stage-4 images | Excluded | Final h9-v2 images | Exclusion rate |
|---|---|---:|---:|---:|---:|
| Y-PPE | train | 1,595 | 359 | 1,236 | 22.5% |
| Y-PPE | validation | 459 | 103 | 356 | 22.4% |
| Y-PPE | test | 234 | 48 | 186 | 20.5% |
| Construction-PPE | train | 1,077 | 31 | 1,046 | 2.9% |
| Construction-PPE | validation | 134 | 2 | 132 | 1.5% |
| Construction-PPE | test | 141 | 3 | 138 | 2.1% |

Total exclusions:
- Y-PPE: **510 images**.
- Construction-PPE: **36 images**.

Final frozen identities:
- Y-PPE-h9-v2 fingerprint: `82c08766d5c5e50e93d41d21c4751fd686a3932ea6a8cb24ffd2838d9e30fba8`
- Construction-PPE-h9-v2 fingerprint: `59469299ba67355dbcb0e725851f73d244a7ad6e93522d44601be3c8323d3c14`

## 7. Exclusion-reason accounting

### Y-PPE
Because one image can contain multiple risk reasons, reason-token counts overlap:
- `harmonized_empty`: 282 images;
- `critical_unmatched:Soft Hat`: 171;
- `critical_unmatched:Child`: 113;
- `critical_unmatched:No Safety Attire`: 73.

Non-overlapping reason combinations over the 510 excluded images:

| Risk-reason combination | Images |
|---|---:|
| harmonized_empty only | 169 |
| critical_unmatched:Soft Hat only | 152 |
| critical_unmatched:Child + harmonized_empty | 81 |
| critical_unmatched:No Safety Attire only | 44 |
| critical_unmatched:No Safety Attire + harmonized_empty | 23 |
| critical_unmatched:Child only | 19 |
| critical_unmatched:Child + critical_unmatched:Soft Hat | 9 |
| critical_unmatched:Soft Hat + harmonized_empty | 6 |
| critical_unmatched:No Safety Attire + critical_unmatched:Soft Hat | 3 |
| critical_unmatched:Child + critical_unmatched:No Safety Attire + harmonized_empty | 2 |
| critical_unmatched:Child + critical_unmatched:No Safety Attire | 1 |
| critical_unmatched:Child + critical_unmatched:Soft Hat + harmonized_empty | 1 |

### Construction-PPE
- 35 images: `critical_unmatched:none` only;
- 1 image: `critical_unmatched:none + harmonized_empty`.

## 8. Effect of filtering on retained class support

Whole-image filtering changed class support, particularly for Y-PPE safety-negative classes.

| Dataset | Class | Stage-4 count | Final v2 count | Relative change |
|---|---|---:|---:|---:|
| Y-PPE | person | 2,351 | 1,802 | -23.4% |
| Y-PPE | helmet | 1,959 | 1,698 | -13.3% |
| Y-PPE | gloves | 1,310 | 1,170 | -10.7% |
| Y-PPE | vest | 1,391 | 1,173 | -15.7% |
| Y-PPE | boots | 1,608 | 1,329 | -17.4% |
| Y-PPE | goggles | 826 | 806 | -2.4% |
| Y-PPE | no_helmet | 256 | 167 | -34.8% |
| Y-PPE | no_gloves | 1,373 | 1,016 | -26.0% |
| Y-PPE | no_boots | 544 | 310 | -43.0% |
| Construction-PPE | person | 2,180 | 2,062 | -5.4% |
| Construction-PPE | helmet | 1,671 | 1,613 | -3.5% |
| Construction-PPE | gloves | 1,339 | 1,331 | -0.6% |
| Construction-PPE | vest | 1,553 | 1,513 | -2.6% |
| Construction-PPE | boots | 1,518 | 1,480 | -2.5% |
| Construction-PPE | goggles | 487 | 485 | -0.4% |
| Construction-PPE | no_helmet | 485 | 432 | -10.9% |
| Construction-PPE | no_gloves | 556 | 505 | -9.2% |
| Construction-PPE | no_boots | 115 | 93 | -19.1% |

Therefore, the final benchmark is explicitly a **structurally harmonizable subset**, not a random sample of the full cleaned source datasets.

## 9. Test-set selection-bias interpretation

The Stage 4.5 rule does use source ground-truth annotation metadata to determine whether a test image belongs to the structurally harmonizable evaluation population. This is not model/test-performance leakage because:
- the rule was frozen before Stage 5 training and before test prediction;
- no test pixels were visually adjudicated for membership;
- no model output influenced removal;
- exactly the same rule was applied to all splits.

However, it can change the composition of the held-out population. The manuscript should therefore state explicitly that results estimate performance on the **predeclared structurally harmonizable subset**, not on every image in the original source datasets. The before/after counts above make this selection transparent.

## 10. Reproducibility assets

The exact exclusion lists are stored in:
- `Y-PPE_exclusion_manifest.csv`
- `Construction-PPE_exclusion_manifest.csv`

The implementation is:
- `apply_stage4_5_conservative_filter.py`

The final Stage 4.5 evidence artifact is:
- GitHub Actions run: `35536050231`
- Artifact ID: `10612876023`
- Artifact digest: `sha256:24b5851f8eef044e17d6804272db2965fed9737098718ed229d0e5a57028786f`
- Head SHA: `eb87aa14dab07d7546e713c2d5eb68ef583f2d5a`

This artifact contains the exclusion manifests, structural summaries, filter summaries, and final harmonized dataset summaries.
