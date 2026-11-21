# SEER-PPE cumulative CHANGELOG

## v0.4 — 2026-11-06
- Full **live original** Roboflow index read: 2,327 image IDs, source/size/split label statistics and 31 filename-collision groups reported, carefully NOT classified as proven image leaks.
- 30 deterministic candidate *development* images (16 train / 14 valid), 0 original test; 396 saved boxes geometry reviewed and 89 model-assistance-provenance markers observed.
- Private blinded reviewer A/B and provenance/clean-archive membership queues written, initially unadjudicated/unverified.
- `PHASE4_REPORT.md`, source-scope evidence JSON, `ANNOTATION_REVIEW_PROTOCOL.md`; cumulative manuscript methods appendix updated.
- Physical 17-class clean derivative verification remains OPEN; original raw v2 Roboflow export accessible remotely but not downloadable in local runtime. No claim of a newly frozen SHA-hashed archive.
- No model weights, images, proprietary raw photo contents, training, or energy metrics published; no SEER results claimed.

## v0.3 — 2026-11-04
- Created evolving manuscript, split/target safety-gate utilities and 40 synthetic unit-test baseline.

## v0.2 / v0.1 — 2026-11-04
- Hosted model engineering smoke and initial paper protocol.

## v0.5 — 2026-11-06
- Reconstructed and audited clean 17-class Y-PPE images in GitHub Actions; run #42153641457 passed file integrity, retained only checksum/evidence artifacts, not raw image archive.
- Fixed an audit-script error that initially rejected 436 valid polygon annotation rows; final result: 15,864 box + 436 polygon rows, zero invalid rows.
- Prepared metadata-only 30-image clean-derivative candidate alignment (29 name+count unique, one one-row dedupe-consistent).
- Started human-review **administrative handoff**: generated anonymized and separately shuffled A/B case queues and blank third-expert log; no human judgments yet.
- Updated working manuscript with Phase5 Appendix B; no fabricated accuracy/XAI/energy results.


## v0.6 — 2026-11-10
- Archived the real 2,288-image cleaned 17-class Y-PPE derivative in three private Drive segments and verified complete round-trip integrity against SHA256; GitHub raw image files remain uncommitted.
- Added per-class support analysis for actual cleaned label files; 7 dHash candidate visual analyst decisions with expert confirmation pending; classified 30 development examples into work-plausible, product/non-work control and uncertain context.
- Added target-preserving black-box occlusion XAI skeleton and instrumented hardware capability probe; increased synthetic unit test pass count to 56.
- Updated master manuscript Methods/Results to include only verified descriptive data results, with risk, XAI and energy outcomes explicitly unmeasured.
- Did not solicit human reviews, modify any source labels or datasets, start training, or assert regulatory compliance or energy savings.


## v0.7 — 2026-11-22
- Froze V30 target-specific progressive XAI protocol and ten-target manifest, reusing V27/V28 target IDs and archived baseline geometry without target reselection.
- Added 8×8 single-cell occlusion maps, progressive deletion/insertion curves, random and inverse-saliency controls, and trapezoidal AUC implementation.
- Added a guarded local RF-DETR hosted-inference runner with an explicit 1,068-call confirmation requirement; local source images are not committed.
- Added nine synthetic V30 tests and CI coverage. All nine passed locally; Python syntax compilation passed. Unrankable target maps and ambiguous blurred endpoints fail closed with explicit null curves.
- Actual V30 model calls remain zero pending the local image bundle and Roboflow API key. Manuscript remains v0.27; no progressive XAI or worker-safety efficacy result is claimed.


## v0.8 — 2026-11-22
- Retrieved and verified the eight exact V30 source assets in the connected Roboflow workspace: four Train and four Valid, with frozen filenames, asset IDs and dimensions.
- Executed eight real hosted RF-DETR baseline calls at confidence 0.20 / overlap 0.50; all ten frozen target boxes and confidence values reproduced exactly.
- Archived inference IDs, target detection IDs, prediction counts and timings in `V30_BASELINE_PREFLIGHT_ACTUAL_2026-11-22.json`; no raw image bytes or credentials committed.
- Updated the V30 runner to reuse the completed baseline record and avoid eight duplicate calls. Total budget remains 1,068, with at most 1,060 additional calls.
- Progressive occlusion, deletion/insertion curves and AUC remain unexecuted; local image SHA-256 verification and full-run execution are still pending. Manuscript remains v0.27.

## v0.9 — 2026-11-22
- Created cloud-only V30 GitHub Actions workflow and read-only frozen-image downloader; raw images stay on an ephemeral hosted runner, never in GitHub commits or artifacts.
- [Cloud run 44962342687](https://github.com/EZZALDEEN049/Y-PPE-Detection-RFDETR/actions/runs/44962342687) succeeded: fetched all 8 original Roboflow sources, checked filenames/splits/asset IDs/dimensions, computed SHA-256 hashes, and passed dry-run and local-bundle preflight.
- Archived a numeric-only cloud preflight ledger: `V30_CLOUD_PREFLIGHT_ACTUAL_2026-11-22.json`. No cloud perturbation inference was triggered; V30 remains 8/1,068 model calls.
- Actual progressive XAI remains an explicit user-authorized manual Actions run, requiring `ROBOFLOW_API_KEY` as a repository secret and approval of the remaining 1,060-call maximum. No local workstation setup needed.
