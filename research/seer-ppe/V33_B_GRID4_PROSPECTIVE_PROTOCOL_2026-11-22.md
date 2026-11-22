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

These gates were frozen before execution. Their completion and the actual one-time run are recorded in the V33-B execution record appended below; V33-A remains the separate zero-new-inference reanalysis.


## Implementation handoff (runner and safeguards completed before execution)

- Dedicated runner: `tools/run_v33b_grid4_xai.py`. It reuses the exact frozen V30 manifest, connector baseline record, V30 result archive, and local original-image bundle; it does not change the model or dataset.
- Zero-call validation:
  - `python tools/run_v33b_grid4_xai.py --images-dir PATH_TO_FROZEN_V30_IMAGES --dry-run`
  - `python tools/run_v33b_grid4_xai.py --images-dir PATH_TO_FROZEN_V30_IMAGES --preflight-only --output PATH_TO_READINESS_JSON`
- The runner checks the eight local SHA-256 values against the values archived from the V30 cloud-runner image bundle, then checks the ten target IDs, original geometry, confidence, classes and A5/A6 assignments against the frozen V30 records. **These are repeatability hashes of the V30 downloaded bundle, not independent source-side checksums.**
- The actual inference command is deliberately gated and must not be used until the author separately authorizes the 496-call maximum:
  - `ROBOFLOW_API_KEY=... python tools/run_v33b_grid4_xai.py --images-dir PATH_TO_FROZEN_V30_IMAGES --confirm-additional-call-budget 496 --output PATH_TO_V33B_RESULTS_JSON`
- Every inference attempt is written to a partial call ledger before the request; failures are retained and not automatically retried. The public engineering workflow includes synthetic V33-B tests and does not run hosted inference.
- At the time of this implementation handoff, V33-B had not yet been executed. The subsequent author authorization, successful preflight and completed one-time run are recorded below.


## Ephemeral cloud execution workflow

- The dedicated one-time cloud workflow is `.github/workflows/seer-ppe-v33b-authorized-once.yml`. Ordinary pushes do not invoke it; it listens only for the dedicated authorization record path.
- After explicit author approval, the authorization record must be created at `V33_B_CLOUD_EXECUTION_AUTHORIZATION_2026-11-22.json` with the exact frozen scope, 4x4 grid, eight Train/Valid images, ten targets, zero Test images and `max_additional_calls: 496`. Its commit message must be exactly `V33B-AUTHORIZED-ONCE: execute frozen 4x4 XAI`.
- The workflow downloads only the eight frozen V30 originals to an ephemeral GitHub Actions runner, performs zero-call SHA/target preflight, checks the repository secret `ROBOFLOW_API_KEY` without printing it, and then runs the gated 496-call runner.
- A successful numeric result or a failed partial call ledger is committed back to the research branch; either artifact blocks duplicate execution. Raw images and credentials are never uploaded or committed.
- At the time of this cloud-workflow handoff, no authorization record existed. A separate authorization record was later created after the read-only preflight passed; the resulting one-time execution is recorded below.

- A separate zero-inference workflow, `.github/workflows/seer-ppe-v33b-preflight.yml`, downloads the same eight originals on an ephemeral runner and validates hashes/targets/budget without requiring `ROBOFLOW_API_KEY`. It uploads numeric readiness evidence only; this preflight is not a paid experiment.


## Author authorization and preflight request — 2026-11-22

The author explicitly approved a one-time V33-B execution with a hard maximum of 496 additional hosted inference calls. This commit requested the **read-only cloud preflight first**. The preflight passed successfully before the one-time authorization record was created and the paid workflow was triggered. The preflight itself made zero model calls.


## V33-B actual execution and numeric audit — completed 22 November 2026

The author explicitly authorized one execution with a hard maximum of 496 additional hosted calls. The read-only preflight [GitHub Actions 45019722753](https://github.com/EZZALDEEN049/Y-PPE-Detection-RFDETR/actions/runs/45019722753) completed successfully before the paid workflow was authorized. It downloaded only the eight frozen Train/Valid originals, matched all eight SHA-256 values to the archived V30 cloud-runner bundle, validated all ten frozen targets and recorded zero model calls. The hash comparison is a repeatability check against the V30 downloaded bundle, not an independent source-side checksum.

The dedicated authorization record was then committed with the exact one-time trigger message. The paid workflow [GitHub Actions 45019831430](https://github.com/EZZALDEEN049/Y-PPE-Detection-RFDETR/actions/runs/45019831430) completed successfully on run attempt 1. It passed the duplicate guard, exact authorization/budget checks, source download, zero-call preflight and hosted credential gate before executing the experiment.

**Actual additional calls: 496 attempted, 496 successful, zero failed, zero retries.** Phase counts were 8 Gaussian-blur endpoints, 128 4×4 single-cell occlusions and 360 intermediate curve calls. The experiment produced ten rankable maps, 40 eleven-point curves and 39 valid AUCs. One saliency-deletion AUC remained null due to an ambiguous target match and was not imputed. The paired 4×4/8×8 analysis found 10/10 categorical map-rankability matches, but only 6/9 comparable deletion and 9/10 insertion saliency-versus-random advantage signs were preserved across resolutions.

The independent read-only audit script tools/audit_v33b_grid4_xai.py passed in [engineering CI 45020503717](https://github.com/EZZALDEEN049/Y-PPE-Detection-RFDETR/actions/runs/45020503717). It recomputed the available AUCs from actual modified-area fractions with maximum absolute error 2.22×10⁻¹⁶, checked all 496 ledger entries, target IDs, map dimensions, curve contexts, paired V30 metrics and guardrails.

**Final scientific boundary:** V33-B is a descriptive within-target resolution-robustness experiment on eight development-exposed images and ten selected targets. It does not establish spatial map-rank correlation, causal/external explanation faithfulness, independent acquisition generalization, A5/A6 superiority, worker-level compliance, human-review efficacy, safety improvement or energy savings. Test was not accessed; no retraining or original dataset changes occurred.

Archived outputs:
- [V33-B actual results JSON](V33_B_GRID4_ACTUAL_RESULTS_2026-11-22.json)
- [V33-B actual results report](V33_B_GRID4_ACTUAL_RESULTS_REPORT_2026-11-22.md)
- [V33-B independent numeric audit JSON](V33_B_GRID4_NUMERIC_AUDIT_2026-11-22.json)
