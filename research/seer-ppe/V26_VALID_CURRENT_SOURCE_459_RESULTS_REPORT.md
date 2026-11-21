# SEER-PPE V26 — new current original Source Valid object-detection results

**21 November 2026.** Actual fresh unmodified RF-DETR Small (17 classes) uniform vectorized hosted inference over ALL 459 already author-curated original Valid Source images, at confidence floor 0.20 and hosted overlap 0.50. Object-level class-exact greedy one-to-one original-coordinate bounding-box IoU >= 0.50. All 12 Source geometry shards and exact metadata/GT class counts passed tests. No original images/annotations/model weights modified, no Test used.

## Current author Source Valid reference — actual V26 metrics

| Cohort | Original images | Current GT boxes | New predicted boxes | TP | FP | FN | Precision | Recall | F1 |
|:--|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| M0 | 459 | 3471 | 4103 | 3297 | 806 | 174 | 80.36% | 94.99% | 87.06% |
| M1 | 448 | 3433 | 4063 | 3261 | 802 | 172 | 80.26% | 94.99% | 87.01% |
| M2 | 367 | 3049 | 3618 | 2894 | 724 | 155 | 79.99% | 94.92% | 86.82% |

M0=459 Clean17-matched original Valid images; M1=448 after historic holds/technical high-overlap exclusions; M2=367 technically unflagged but NOT independently acquired/certified. These class-exact IoU=0.50 object scores are NOT COCO mAP, PPE worker compliance or a SEER-PPE policy effect.

## The original 17 detector classes — complete M0 and technical-risk M2 sensitivity

| Original class | M0 GT | M0 TP | M0 FP | M0 FN | M0 P | M0 R | M0 F1 | M2 GT | M2 F1 |
|:--|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| Animal | 66 | 66 | 9 | 0 | 88.00% | 100.00% | 93.62% | 60 | 93.02% |
| Child | 31 | 29 | 8 | 2 | 78.38% | 93.55% | 85.29% | 28 | 85.25% |
| Face Masks | 80 | 74 | 27 | 6 | 73.27% | 92.50% | 81.77% | 69 | 81.76% |
| No Hard Hat | 56 | 55 | 9 | 1 | 85.94% | 98.21% | 91.67% | 50 | 93.33% |
| No Safety Boots | 93 | 85 | 41 | 8 | 67.46% | 91.40% | 77.63% | 82 | 77.08% |
| Soft Hat | 60 | 57 | 12 | 3 | 82.61% | 95.00% | 88.37% | 54 | 87.93% |
| Hard Hat | 388 | 377 | 39 | 11 | 90.63% | 97.16% | 93.78% | 330 | 93.14% |
| No Safety Vest | 160 | 156 | 42 | 4 | 78.79% | 97.50% | 87.15% | 146 | 87.12% |
| Pants | 207 | 201 | 62 | 6 | 76.43% | 97.10% | 85.53% | 185 | 85.78% |
| No Face Mask | 280 | 269 | 51 | 11 | 84.06% | 96.07% | 89.67% | 253 | 89.67% |
| No Safety Attire | 87 | 80 | 25 | 7 | 76.19% | 91.95% | 83.33% | 75 | 81.93% |
| No Gloves | 328 | 308 | 115 | 20 | 72.81% | 93.90% | 82.02% | 298 | 83.28% |
| Gloves | 278 | 250 | 80 | 28 | 75.76% | 89.93% | 82.24% | 240 | 80.91% |
| Safety Boots | 365 | 337 | 105 | 28 | 76.24% | 92.33% | 83.52% | 315 | 82.69% |
| Safety Vests | 315 | 297 | 45 | 18 | 86.84% | 94.29% | 90.41% | 273 | 90.21% |
| Goggles | 189 | 183 | 33 | 6 | 84.72% | 96.83% | 90.37% | 154 | 89.16% |
| Persons | 488 | 473 | 103 | 15 | 82.12% | 96.93% | 88.91% | 437 | 89.05% |

The model class names beginning No (No Gloves, No Hard Hat, No Face Mask and similar) are annotated object categories, NOT proven worker-specific task-policy violations. No worker clearances, review outcomes, safety decisions, XAI explanation fidelity or physically metered Joules were evaluated.

## Precommitted descriptive robustness checks

| Filter (Source IDs fixed before V26 outcomes) | Images | Current GT | TP | FP | FN | F1 |
|:--|--:|--:|--:|--:|--:|--:|
| M0 minus 13 current vs old GT count differences | 446 | 3152 | 3022 | 658 | 130 | 88.47% |
| M0 minus 5 V23 pilot exposures | 454 | 3448 | 3275 | 805 | 173 | 87.01% |
| M2 minus 5 V23 pilot exposures | 362 | 3026 | 2872 | 723 | 154 | 86.75% |

The 13 original Source IDs excluded in one test are the pre-existing V20 current GT versus historical provider-GT count mismatches (16 additional current saved author boxes). The five V23 previously used original Valid pilot Source IDs were FRESHLY inferred in this uniform V26 workflow and remain development-exposed. Neither exclusion creates acquisition-independent validation.

## Historical V20 versus newly computed V26 — keep results separated

The 2025 model-v2 provider Eval had historical M0/M1/M2 micro-F1 0.885018 / 0.884642 / 0.880754. Its 2025 annotation geometry was not retrievable and current author boxes differ in 13 Source images; new V26 inference uses a different uniform vectorized execution. There is no scientifically controlled causal performance gain or loss to infer from the two sets of descriptive scores.

## Reference provenance and research claim limits

The author already curated and checked the original image labels, and they remain the accepted single-researcher current Source detection reference, without repeated manual inspection or a required second rater. Of M0 current boxes, 729/3471 carry existing model-assisted labeling provenance markers. The 459 original Valid images have historic model-development exposure and possibly shared source families; M2 excludes flags but does not establish independence.

The V25 A2/A5 policy execution was proposal-only on 74 stored model boxes. The V26 object detector assessment does NOT test SEER A5 versus a strong selective reviewer, individual task mandates and false safe clearances, target-matched XAI faithfulness, actual human review, electrical Joules, or an independent external model generalization claim. The strict worker-safety gate is still NOT_FROZEN / scoring_ready=false.

## Reproducible evidence

- Full original current GT geometry and newly inferred prediction geometry: 12 numbered V26_ORIGINAL_VALID_GEOMETRY_SHARD files
- Executable numeric IoU=0.5 scorer: tools/score_original_valid_current_boxes_v26.mjs
- Full matching results by image, cue and class: ACTUAL_CURRENT_SOURCE_ORIGINAL_VALID_459_CLASS_BBOX_METRICS_V26.json
- Compact current Source class metrics: V26_VALID_CURRENT_SOURCE_459_NUMERIC_SUMMARY.json
- Exact 459 scope frozen before outcome: V26_FROZEN_FULL_CURRENT_SOURCE_VALID_BBOX_PROTOCOL_2026-11-21.md
- Uniform vector batch inference: V26_FROZEN_VECTOR_BATCH_INFERENCE_ADDENDUM_2026-11-21.md
- Distinct historic provider scores: HISTORICAL_VALID_INTERNAL_METRICS_V20.json

The large full-result JSON is indexed by this compact summary and its SHA256 hash. No source-image bytes, HTTPS signed URLs, credentials or original Test data were published as part of V26.
