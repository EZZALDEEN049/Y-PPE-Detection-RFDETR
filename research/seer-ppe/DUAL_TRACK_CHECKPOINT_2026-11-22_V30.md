# SEER-PPE — V30 continuation checkpoint (22 November 2026)

## Status

**V30 protocol, baseline reproduction and GitHub cloud-image preflight are complete. Progressive XAI model perturbations and AUC remain pending an explicitly authorized cloud Actions run. No researcher's local computer is required.**

The manuscript remains v0.27. No progressive XAI result or AUC is claimed in this checkpoint. The eight baseline inferences are setup/reproduction checks, not a new performance benchmark.

## Confirmed V30 scope

- Ten unique frozen A5/A6 target detections from V27/V28.
- Eight target-bearing original images: four Train and four Valid. The ninth V27 sample image had no selected PPE target and is excluded from target-specific curves.
- A5/A6: eight selected slots per arm, six shared, two A5-only and two A6-only.
- Original hosted model remains `altayyar-0oflt-lafos-qqauz/2`, confidence 0.20, overlap 0.50.
- 8×8 single-cell occlusion map, Gaussian-blur progressive deletion/insertion, random and inverse-saliency controls.
- Frozen total maximum: **1,068 original-model calls**. The eight original-image baseline calls are complete; the local runner has a remaining maximum of **1,060 calls** (8 blurred endpoints + 512 map calls + up to 540 curve-intermediate calls).

## Implemented artifacts

- `V30_FROZEN_PROGRESSIVE_XAI_PROTOCOL_2026-11-22.md`
- `V30_FROZEN_TARGETS_2026-11-22.json`
- `V30_BASELINE_PREFLIGHT_ACTUAL_2026-11-22.json`
- `V30_CLOUD_PREFLIGHT_ACTUAL_2026-11-22.json`
- `V30_CLOUD_ONLY_EXECUTION_GUIDE_2026-11-22.md`
- `.github/workflows/seer-ppe-v30-cloud.yml`
- `tools/fetch_v30_originals_cloud.py`
- `seer_ppe/progressive_xai.py`
- `tools/run_v30_progressive_xai.py`
- `tests/test_v30_progressive_xai.py`

The scorer defines a lost target's fixed-target score as zero, while ambiguous matches remain missing and block AUC. It records actual modified pixel area, preserves raw confidence, and clips only the normalized AUC score to [0,1]. Unrankable maps and ambiguous blurred endpoints receive explicit null curves; other targets continue.

## Verification performed in this continuation

- Nine synthetic unit tests and Python syntax compilation passed in GitHub Actions on the current branch head. [Current unit-test run 44960453523](https://github.com/EZZALDEEN049/Y-PPE-Detection-RFDETR/actions/runs/44960453523).
- Python syntax compilation passed for the V30 module and runner.
- Source/reference readiness workflow passed on the current branch head. [Current readiness run 44960453517](https://github.com/EZZALDEEN049/Y-PPE-Detection-RFDETR/actions/runs/44960453517).
- Eight real original-image RF-DETR calls were executed through connected Roboflow. All 8/8 source images resolved and all 10/10 frozen target boxes and confidence values reproduced exactly. [Detailed baseline record](V30_BASELINE_PREFLIGHT_ACTUAL_2026-11-22.json).
- **Actual cloud readiness run 44962342687 succeeded:** all 8 original Train/Valid images fetched automatically on GitHub Actions, filenames/IDs/dimensions validated, SHA-256 hashes recorded, archived numeric evidence artifact; zero new inference calls. [Run](https://github.com/EZZALDEEN049/Y-PPE-Detection-RFDETR/actions/runs/44962342687) · [ledger](V30_CLOUD_PREFLIGHT_ACTUAL_2026-11-22.json).
- No progressive XAI perturbation calls, maps, curves or AUCs have been executed yet.
- No image bytes, original annotations, model weights, or Test assets were changed or committed.
- No human review or worker-safety scoring was performed.

## Remaining execution gates — cloud only

1. Review and merge [draft PR #19](https://github.com/EZZALDEEN049/Y-PPE-Detection-RFDETR/pull/19) to `main` so the new manual GitHub Actions workflow is available on the default branch.
2. Add a Roboflow API key as the **GitHub Actions repository secret** `ROBOFLOW_API_KEY`, without placing its value in chat, source code, or workflow inputs.
3. Review Roboflow/GitHub Actions quota and usage costs; the authorization covers up to 1,060 **additional** model calls (1,068 total including 8 completed baseline calls).
4. Manually dispatch `SEER-PPE V30 cloud-only XAI (manual full run)` with `run_progressive=true` and `confirm_budget=1068`.
5. Review the numeric-only artifact. Audit original source SHA-256, all target statuses, maps, progressive curves, AUCs and actual model call count.
6. Only after V30 inference evidence is audited, update the manuscript beyond v0.27.

**No local image download or Python environment is required.** The validated cloud image-download preparation is recorded in `V30_CLOUD_PREFLIGHT_ACTUAL_2026-11-22.json`.

## Scientific limits retained

All V30 images are development-exposed. Source-family independence is not established. Results can characterize target-specific model sensitivity and explanation-curve behavior only; they cannot establish worker-level PPE compliance, employer task-mandate correctness, safety efficacy, or statistical superiority of A5/A6. Protected Test remains unopened. Strict worker-safety `scoring_ready=false`.


## Post-run factual closeout addendum — 22 November 2026 (supersedes the pre-run status above)

The earlier V30 checkpoint sections were written **before** the authorized XAI call and are intentionally preserved as an audit trail, not current execution guidance.

- **Actual V30 executed:** [run 44964287536](https://github.com/EZZALDEEN049/Y-PPE-Detection-RFDETR/actions/runs/44964287536) completed successfully, generating 1,060 *new* original model requests plus the 8 previously archived baseline calls = exactly **1,068**.
- Eight images, ten unique frozen target detections, all 64-cell target maps, all 60 11-point progressive curves, all 60 AUCs completed. Six blurred targets were LOST, four MATCHED, zero maps blocked.
- **Independent post-run audit passed:** [run 44965260120](https://github.com/EZZALDEEN049/Y-PPE-Detection-RFDETR/actions/runs/44965260120), [audited numeric file](V30_INDEPENDENT_NUMERIC_AUDIT_2026-11-22.json), [full actual numeric file](V30_ACTUAL_PROGRESSIVE_XAI_RESULTS_2026-11-22.json). It re-integrated AUC, checked ten targets, arm overlaps, 8 image hashes and call accounting; no additional inference.
- **Canonical manuscript is now v0.30**, with V30 Methods §3.24, Results §4.24, Discussion §5.10 and Appendix U.
- **V31 source/human readiness remains closed:** [V31 ledger](V31_SOURCE_PERSON_SAFETY_READINESS_2026-11-22.json) has 11 guarded source-overlap P0 cases, 0 independently signed Valid source-family verdicts and 0 signed Valid Person–PPE cases among the 459; [V31 read-only CI](https://github.com/EZZALDEEN049/Y-PPE-Detection-RFDETR/actions/runs/44965651906) passed.
- **Repeat-spending safeguard applied:** the former optional V30 cloud workflow is now source-preflight-only, and the historic single authorized-run workflow explicitly blocks execution whenever an archived V30 result exists. This does not retroactively change the executed run.
- Original Train/Valid/Test boundaries, RF-DETR Small, images, annotations, source holds, all previous human Train judgments and worker-safety `scoring_ready=false` are unchanged.
