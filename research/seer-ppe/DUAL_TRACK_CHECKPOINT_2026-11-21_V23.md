# SEER-PPE V23 — actual new fixed-model original Valid current-box pilot and integrated manuscript v0.23

**21 November 2026.** Last *actually executed experiment*: 5 first-lexicographic original Valid Source IDs in predeclared unflagged but non-independently certified M2 cohort; read-only hosted RF-DETR Small model-infer against current already author-reviewed original saved bbox references, scored by a new reproducible pre-frozen evaluator.

## Before outcomes: locked controls

The [V23 pilot protocol](V23_VALID_CURRENT_BOX_GEOMETRY_FROZEN_PILOT_PROTOCOL.md) was committed at `56155f071d51cae7734210266861b02af24ba7bc` **before new predictor outcomes** and specified:
- Fixed original 17-class `altayyar-0oflt-lafos-qqauz/2` at confidence `0.20`, overlap `0.50` on **original, non-generated Source images** only;
- Five precisely named Source IDs in stable sorted M2 membership, all previously development-exposed `Valid` and not independent families;
- Current stored author annotations and dimensions from read-only native Roboflow, no user image reinspection or second reviewer;
- Same-class confidence-sorted, one-to-one greedy native-rectangle bounding-box IoU **≥0.50**;
- All outputs **development-only**, no Test, source mutation, retraining, safety violation, XAI or energy claim.

## New actual hosted model results (not historical V20 counters)

| Source original filename | Current GT boxes | New original RF-DETR boxes | TP | FP | FN |
|---|---:|---:|---:|---:|---:|
| `image_1282.jpg` | 13 | 13 | 13 | 0 | 0 |
| `5731201_4.jpg` | 1 | 1 | 1 | 0 | 0 |
| `c1e5a26df8225afb5be5beceae128ad5.jpg` | 3 | 3 | 3 | 0 | 0 |
| `imagem40.jpg` | 5 | 5 | 4 | 1 | 1 |
| `a16ea468abd845e68ea9ccbbe4f9762e.jpg` | 1 | 1 | 1 | 0 | 0 |
| **Total** | **23** | **23** | **22** | **1** | **1** |

**Micro precision 0.956522; micro recall 0.956522; micro F1 0.956522 (95.65%)**, at bbox IoU 0.5, hosted confidence 0.2, **only five nonrandom, previously exposed Valid images**. The single model-vs-current-label false positive and false negative are in the `Safety Vests` **detection class**; neither is an independently evidenced worker-level safety failure or compliance verdict. All current annotations in these particular five Source images had **zero model-assisted annotation markers**, whereas the overall 459-image current Valid reference contains **729 markers**.

A pre-committed protocol and verified native Source IDs do not make the five images statistically representative. **No new 459-image Valid current-GT score, population metric, accuracy improvement, energy saving, A5-vs-A2 SEER effect or independently unseen test was measured.** The previous V20 historical provider Eval (459/448/367) remains separately archived; its 13 image current-vs-legacy reference-count differences are not replaced by these five.

## Actual saved evidence and CI

- [V23 frozen five-source method](V23_VALID_CURRENT_BOX_GEOMETRY_FROZEN_PILOT_PROTOCOL.md)
- [Five real hosted original-model prediction geometries paired with current author Source annotations](VALID_ORIGINAL_SOURCE_CURRENT_BBOX_MODEL_PILOT_V23.json)
- [V23 deterministic bbox-matching scorer + synthetic fail-closed tests](tools/score_current_valid_source_boxes_v23.mjs)
- [V23 actual per-image and class-wise TP/FP/FN](VALID_CURRENT_SOURCE_REAL_MODEL_BOX_MATCH_V23.json)
- [GitHub Actions successful actual V23 recalculation (run 44860810115)](https://github.com/EZZALDEEN049/Y-PPE-Detection-RFDETR/actions/runs/44860810115)
- [Master paper now v0.23](MANUSCRIPT_MASTER.md), incorporating executed Methods §3.18, Results §4.18, Discussion and Appendix O. Prior V22 class-support results and V20 historical Eval are preserved.

## Current scientific gate and next work

The original author completed full image selection/annotation/checking, and no second reviewer is required for the narrow original-label detection benchmark. However, the independent-source occupational-safety worker-level experiment is **`NOT_FROZEN`/`scoring_ready=false`**. Unknown task mandates and missing worker-specific references are never invented. Historical Test was development-exposed and was not accessed in this continuation. The original model and all original data/labels/splits remain unchanged.

**Next experimental advancement:** implement a scalable **current-label full original Valid source-ID bbox scorer** with the same settings, immutable per-image GT and prediction geometry and the frozen M0/M1/M2 composition checks. The present five pilot Valid IDs must remain marked as already development-exposed, and all full-cohort results labeled historic/internal/possibly source-related. For the SEER scientific claim, execute the actual safety-constrained A5 vs a preselected strong selective comparator with measured explanations/cost only if per-worker mandate evidence genuinely supports such outcomes; otherwise narrow the claims rather than manufacturing compliance.
