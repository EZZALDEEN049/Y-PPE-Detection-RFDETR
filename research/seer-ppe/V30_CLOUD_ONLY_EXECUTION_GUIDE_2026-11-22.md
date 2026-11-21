# SEER-PPE V30 — cloud-only execution (no local workstation)

**Date:** 22 November 2026. **Status:** cloud runner and read-only image-downloader prepared. This file is a runbook, not a claim that the progressive XAI experiment has completed.

## Goal

Execute the frozen V30 progressive black-box XAI protocol using **GitHub-hosted Linux compute** and the existing **Roboflow hosted RF-DETR Small model**, without running Python or storing the eight original image files on the researcher's computer.

## Frozen baseline already executed

- Baseline original-image inference: **8/8 images** and **10/10 frozen target detections** passed, via connected Roboflow inference.
- Evidence: `V30_BASELINE_PREFLIGHT_ACTUAL_2026-11-22.json`.
- Total experiment cap: **1,068 original-model calls**, including the completed eight baseline calls.
- Further calls: maximum **1,060**, comprising 8 fully blurred endpoints, 512 single-cell 8×8 occlusions, and up to 540 intermediate deletion/insertion requests.
- No Test, retraining, original-image edits, or new data uploads.

## Where the actual work runs

- GitHub Actions workflow: `.github/workflows/seer-ppe-v30-cloud.yml`.
- The workflow checks out the current repo version to an **ephemeral GitHub Actions runner**, installs Python dependencies, reads the eight frozen original URLs from the archived baseline JSON, and downloads **only the eight Train/Valid originals** into temporary runner storage.
- Every filename, split, Roboflow Asset Library ID and image dimension is checked against both the frozen target manifest and actual baseline record.
- Image SHA-256 hashes, numeric dry-run and image-bundle preflight JSONs are uploaded as workflow artifacts. Raw images are **never** uploaded as artifacts or committed to GitHub.
- The optional inference step calls hosted model `altayyar-0oflt-lafos-qqauz/2` and uploads numeric XAI results as a workflow artifact. It does not send source-image bytes to any new model/provider beyond the existing Roboflow inference pipeline.

## Safety and costs

The workflow is *non-spending* on branch-push checks: a push only tests downloading the eight sources and dry-run/preflight validation, and does not run model inference.

For the **full run**:
1. Merge the reviewed V30 Pull Request #19 into the repository default branch `main` so that the manual workflow becomes available in GitHub Actions.
2. In GitHub repository **Settings > Secrets and variables > Actions**, create repository secret **`ROBOFLOW_API_KEY`** containing a suitable Roboflow API key. Do not put the key in chat, source files, workflow inputs, comments, or logs.
3. Open **Actions > SEER-PPE V30 cloud-only XAI (manual full run) > Run workflow**.
4. Enable `run_progressive` and type `1068` as `confirm_budget`.
5. Review potential Roboflow/API usage charges or quotas before launching; this explicitly authorizes **up to 1,060 additional calls**. This execution requires a human click and is not initiated by the push checker.
6. On completion, download the **v30-cloud-numeric-evidence** artifact directly from GitHub Actions. Inspect `v30_numeric_results.json`, `v30_image_sha256.json`, `v30_local_preflight.json`.
7. Check numeric completeness, outcome statuses, inference-call counts, all ten target IDs, and A5/A6 descriptive summaries before archiving results or updating the manuscript.

The `confirm_budget` input is a **call cap confirmation, not a price quote**. The experiment may incur Roboflow usage charges and GitHub Actions minutes; the researcher should verify the account's remaining quota and limits in the respective platforms.

## If the cloud image download fails

The public Roboflow source URL may stop serving the original bytes or impose access restrictions. If the source URLs fail, do not silently substitute resized/versioned dataset images or Test images. Read the error logs and obtain fresh **original** Asset Library URLs for the **same eight frozen asset IDs**. Record the URL refresh and verify image dimensions and source IDs before executing V30. Do not override a failed gate or change target selection.

## How to interpret this status

Passing the cloud download and dry-run checks is **infrastructure readiness**. It does not supply saliency maps, deletion/insertion AUC, A5/A6 superiority, person-level compliance or safety impact. The manuscript stays v0.27 until actual model perturbations are run and audited.

**No local computer setup is needed for this GitHub Actions path.**
