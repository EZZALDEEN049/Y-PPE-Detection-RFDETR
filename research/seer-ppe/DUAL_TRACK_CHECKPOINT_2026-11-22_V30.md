# SEER-PPE — V30 continuation checkpoint (22 November 2026)

## Status

**V30 protocol and target manifest frozen; executable implementation added; synthetic tests passed. Actual V30 RF-DETR inference has not yet been run.**

The manuscript remains v0.27. No progressive XAI result, AUC, or new model-performance number is claimed in this checkpoint.

## Confirmed V30 scope

- Ten unique frozen A5/A6 target detections from V27/V28.
- Eight target-bearing original images: four Train and four Valid. The ninth V27 sample image had no selected PPE target and is excluded from target-specific curves.
- A5/A6: eight selected slots per arm, six shared, two A5-only and two A6-only.
- Original hosted model remains `altayyar-0oflt-lafos-qqauz/2`, confidence 0.20, overlap 0.50.
- 8×8 single-cell occlusion map, Gaussian-blur progressive deletion/insertion, random and inverse-saliency controls.
- Frozen maximum budget: **1,068 original-model calls** (528 fixed baseline/blur/map calls plus 54 intermediate calls per curve-eligible target; fewer if a target map or blurred endpoint is unrankable).

## Implemented artifacts

- `V30_FROZEN_PROGRESSIVE_XAI_PROTOCOL_2026-11-22.md`
- `V30_FROZEN_TARGETS_2026-11-22.json`
- `seer_ppe/progressive_xai.py`
- `tools/run_v30_progressive_xai.py`
- `tests/test_v30_progressive_xai.py`

The scorer defines a lost target's fixed-target score as zero, while ambiguous matches remain missing and block AUC. It records actual modified pixel area, preserves raw confidence, and clips only the normalized AUC score to [0,1]. Unrankable maps and ambiguous blurred endpoints receive explicit null curves; other targets continue.

## Verification performed in this continuation

- Nine synthetic unit tests passed locally and in GitHub Actions for target matching, lost/ambiguous handling, grid-map drops, deterministic random controls, blurred baseline, progressive endpoints, and AUC. [Unit-test run 44958488385](https://github.com/EZZALDEEN049/Y-PPE-Detection-RFDETR/actions/runs/44958488385).
- Python syntax compilation passed for the V30 module and runner.
- Source/reference readiness workflow passed after aligning stale V22–V26 manuscript assertions to the existing v0.27 master. [Readiness run 44958488365](https://github.com/EZZALDEEN049/Y-PPE-Detection-RFDETR/actions/runs/44958488365).
- No RF-DETR model calls were made in this continuation.
- No image bytes, original annotations, model weights, or Test assets were changed or committed.
- No human review or worker-safety scoring was performed.

## Remaining execution gates

1. Export or locally download the eight exact original images listed in the frozen manifest; keep them outside GitHub.
2. Set `ROBOFLOW_API_KEY` in the local execution environment.
3. Run `--dry-run` to verify all image filenames and dimensions.
4. Run `--preflight-only` to verify all ten target reproductions before spending the full budget.
5. After reviewing preflight, run the V30 job with the explicit maximum-budget confirmation; actual calls are checked against the number of curve-eligible targets.
6. Validate all maps, curve points, AUCs, target IDs, and actual call count; archive the numeric result JSON.
7. Only after actual results are verified, update the manuscript beyond v0.27 and decide whether any V30 claims are supportable.

## Scientific limits retained

All V30 images are development-exposed. Source-family independence is not established. Results can characterize target-specific model sensitivity and explanation-curve behavior only; they cannot establish worker-level PPE compliance, employer task-mandate correctness, safety efficacy, or statistical superiority of A5/A6. Protected Test remains unopened. Strict worker-safety `scoring_ready=false`.
