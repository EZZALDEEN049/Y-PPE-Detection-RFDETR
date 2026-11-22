# SEER-PPE research changelog

## V33-B — 4x4 runner and pre-inference safeguards — 2026-11-22

- Added \`tools/run_v33b_grid4_xai.py\`, a separate execution runner for the frozen ten V30 targets and eight original Train/Valid images. It uses a 4x4 grid, exact modified-pixel fractions, saliency and one deterministic random ordering, and the original RF-DETR Small endpoint/settings.
- Added strict SHA-256 matching against the eight-image V30 cloud-runner bundle, exact target/geometry/confidence/arm checks, and fail-closed checks for the protected Test boundary.
- Added a hard ceiling of **496 additional hosted calls** (8 blurred endpoints + 128 shared grid-cell occlusions + up to 360 curve-intermediate calls). The runner refuses inference unless the exact explicit budget flag is supplied.
- Added write-ahead per-call logging to a partial JSON ledger, including failed attempts, and disabled automatic retries. No source images, API credentials, annotations, model weights or Test data are written to the repository.
- Added synthetic regression tests in \`tests/test_v33b_grid4_xai.py\` for the 4x4 partition, ambiguous-cell handling, curve point/call counts, deterministic random ordering and budget arithmetic; included them in the public engineering CI workflow.
- **Execution remains NOT STARTED.** No V33-B hosted inference calls, Roboflow mutations, retraining, Test access or manuscript performance claims were made by this implementation-only step. The 496-call cap still requires separate author authorization.
