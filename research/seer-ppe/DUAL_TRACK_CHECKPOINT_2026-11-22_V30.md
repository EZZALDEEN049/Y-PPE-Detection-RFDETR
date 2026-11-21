# SEER-PPE — V30 continuation checkpoint (22 November 2026)

## Status

**V30 protocol and implementation are ready; the eight-image baseline preflight is now executed and passed. Progressive XAI remains pending local access to the eight exact source images.**

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
- `seer_ppe/progressive_xai.py`
- `tools/run_v30_progressive_xai.py`
- `tests/test_v30_progressive_xai.py`

The scorer defines a lost target's fixed-target score as zero, while ambiguous matches remain missing and block AUC. It records actual modified pixel area, preserves raw confidence, and clips only the normalized AUC score to [0,1]. Unrankable maps and ambiguous blurred endpoints receive explicit null curves; other targets continue.

## Verification performed in this continuation

- Nine synthetic unit tests passed locally and in GitHub Actions for target matching, lost/ambiguous handling, grid-map drops, deterministic random controls, blurred baseline, progressive endpoints, and AUC. [Unit-test run 44958488385](https://github.com/EZZALDEEN049/Y-PPE-Detection-RFDETR/actions/runs/44958488385).
- Python syntax compilation passed for the V30 module and runner.
- Source/reference readiness workflow passed after aligning stale V22–V26 manuscript assertions to the existing v0.27 master. [Readiness run 44958488365](https://github.com/EZZALDEEN049/Y-PPE-Detection-RFDETR/actions/runs/44958488365).
- Eight real original-image RF-DETR calls were executed through connected Roboflow. All 8/8 source images resolved and all 10/10 frozen target boxes and confidence values reproduced exactly. [Detailed baseline record](V30_BASELINE_PREFLIGHT_ACTUAL_2026-11-22.json).
- No progressive XAI perturbation calls, maps, curves or AUCs have been executed yet.
- No image bytes, original annotations, model weights, or Test assets were changed or committed.
- No human review or worker-safety scoring was performed.

## Remaining execution gates

1. Download the eight exact original images from the Asset Library IDs/URLs in the frozen baseline record; keep them outside GitHub.
2. Run `--dry-run` to verify local filenames and dimensions.
3. Run `--preflight-only` to compare the local image bundle and frozen connector baseline record; this step makes zero model calls.
4. Set `ROBOFLOW_API_KEY` in the local execution environment.
5. Run the full V30 job with `--confirm-model-call-budget 1068`; the runner reuses the eight completed baseline calls and makes at most 1,060 additional calls.
6. Validate all maps, curve points, AUCs, target IDs, local SHA-256 hashes and total call count (baseline plus new calls); archive the numeric result JSON.
7. Only after actual results are verified, update the manuscript beyond v0.27 and decide whether any V30 claims are supportable.

## Scientific limits retained

All V30 images are development-exposed. Source-family independence is not established. Results can characterize target-specific model sensitivity and explanation-curve behavior only; they cannot establish worker-level PPE compliance, employer task-mandate correctness, safety efficacy, or statistical superiority of A5/A6. Protected Test remains unopened. Strict worker-safety `scoring_ready=false`.
