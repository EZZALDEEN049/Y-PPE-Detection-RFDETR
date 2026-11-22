# V33-B (prospective only) — frozen plan for actual 4×4 grid robustness

**Design drafted:** 22 November 2026. **Execution status:** NOT STARTED. No V33-B model calls authorized by this document.

## Rationale
V30 measured 8×8 single-cell gray-occlusion sensitivity and progressive blur-baseline deletion/insertion curves. V33-A demonstrated algebraic dependence of inverse controls, one-random-seed instability, strong baseline-blur heterogeneity and insufficient A5/A6 policy-comparison power. A real grid-resolution robustness test requires **new inference on 4×4 masks**, not arithmetic aggregation of 8×8 attributions.

## Frozen comparison
- Source assets: the exact eight original Train/Valid files and SHA-256s listed in `V30_ACTUAL_PROGRESSIVE_XAI_RESULTS_2026-11-22.json`, downloaded to ephemeral cloud storage only.
- Targets: the exact ten IDs and original boxes in `V30_FROZEN_TARGETS_2026-11-22.json`; A5/A6 arms unchanged (six common, two unique per arm).
- Model: the existing `altayyar-0oflt-lafos-qqauz/2` RF-DETR Small; confidence 0.20, overlap 0.50; same original pixel decoding.
- New map: 4×4 grid, 16 cells/image, replace each cell with constant RGB 127 in separate inferences.
- Saliency: current frozen baseline target confidence minus unique matched same-class target confidence after one-cell mask; LOST=0, AMBIGUOUS=missing (not imputed), IoU≥0.50 and 0.03 ambiguity margin.
- Baseline: Gaussian blur of the original, sigma=max(3, round(0.01×shorter image edge, 3)).
- Orders: saliency descending positive score drop with row-major ties; one SHA-256 seeded random ordering with 4×4 cells. Inverse is omitted as a separate 'independent' control because it is mathematically complementary under this implementation.
- Curves: deletion and insertion at x=0,.1,.2,…,1 with actual pixel-area fraction, normalized score clipped to [0,1], trapezoidal AUC. Original endpoints reused from archived, exactly reproduced V30 connector preflight; Gaussian endpoint run once per image. Any ambiguous map endpoint blocks that target and reduces the actual call count.
- Primary robustness: within the **same ten target IDs**, compare 4×4 and frozen 8×8 saliency deletion/insertion AUCs, target eligibility, and saliency-vs-random advantage; report target class and image as units, not cell/point pseudo-replicates.
- Secondary: compare A5/A6 **selection compositions** under equal target counts, not different explanations for shared targets; no safety- or causality-based outcome.

## Maximum hosted-call budget (must be explicitly authorized)
| Component | Count |
|---|---:|
| New Gaussian-blurred endpoints (8 original images) | 8 |
| New 4×4 single-cell occlusions (8 × 16) | 128 |
| Ten targets × 2 orderings × 2 directions × 9 intermediate steps | 360 |
| **Upper bound** | **496** |

Original-image baseline calls are already archived and are not repeated. Blocked targets reduce curve calls; there is no automatic retry, no budget overrun, and no fallback to Test. Source hashes must be compared against frozen V30 hashes *before* any inference; no credentials, original images or identifying source URLs may be published in result artifacts.

## Execution gates
1. Exact eight original file hashes match V30's cloud-archived hashes.
2. Ten target IDs/geometry and baseline scores exactly match the V30 connector preflight.
3. The repository's cloud credential is available only inside an ephemeral runner.
4. A new one-time explicit authorization fixes the **496 maximum additional calls**; edits to protocol or source after authorization require a new authorization.
5. The runner records all model calls, including failed attempts, without resubmission, and archives only pseudonymous/numeric JSON.
6. Review scientific limitations before adding V33-B values to the manuscript.

Until these gates pass, **V33-B remains an unexecuted prospective protocol**. V33-A is the completed read-only numeric study.
