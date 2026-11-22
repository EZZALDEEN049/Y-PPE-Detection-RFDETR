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

## V30 actual complete and V31 evidence readiness — 2026-11-22 (manuscript v0.30)

- Researchers explicitly authorized a one-time hosted V30 XAI run. [Run 44964287536](https://github.com/EZZALDEEN049/Y-PPE-Detection-RFDETR/actions/runs/44964287536) succeeded with 1,060 new model calls; together with eight baseline calls the frozen total is **1,068**. Earlier infrastructure/runner failures did not perform additional V30 inference.
- Original images 8/8; frozen targets 10/10; 8×8 single-cell occlusion outcomes 640 (from 512 shared image-cell calls); 60 progressive deletion/insertion curves with eleven points and independently validated trapezoidal AUC. All ten maps rankable, zero AUC blocked. Six fully blurred targets LOST, four MATCHED.
- The [complete actual V30 numeric file](V30_ACTUAL_PROGRESSIVE_XAI_RESULTS_2026-11-22.json) and [independent numeric audit](V30_INDEPENDENT_NUMERIC_AUDIT_2026-11-22.json) are permanently archived. [Audit run 44965260120](https://github.com/EZZALDEEN049/Y-PPE-Detection-RFDETR/actions/runs/44965260120) PASS with zero new model calls and matched eight-image SHA-256 preflight.
- Actual descriptive mean A5 saliency deletion/insertion AUC **0.496288/0.944195**; mean A6 **0.397182/0.871354**. Six of eight target slots are shared, so no independent-arm or worker-safety superiority is claimed.
- Updated canonical manuscript to **v0.30** (Methods 3.24, Results 4.24, Discussion 5.10, Appendix U), retaining strict no-source-independence, no-person-gold, no-energy and no-Test claim boundaries. Aligned manuscript-version CI guards with current manuscript.
- Compiled [V31 source/person readiness ledger](V31_SOURCE_PERSON_SAFETY_READINESS_2026-11-22.json) and [evidence handoff guide](V31_POST_XAI_SOURCE_PERSON_READINESS_GUIDE_2026-11-22.md) from current read-only source/valid human signing overlays: 5 historical holds + 6 technical quarantines + 81 other flagged unsigned + 367 unflagged but unsigned; **0/459 independently signed valid-source families**, **0 signed Valid worker references**. Existing 19 Train person-equipment links and 38/42 saved visual states preserved.
- Added [V31 fail-closed validator](tools/verify_v31_post_xai_readiness.mjs) and mutation self-tests to source-reference readiness CI; [verified pass](https://github.com/EZZALDEEN049/Y-PPE-Detection-RFDETR/actions/runs/44965651906). No new human decisions, full image rereview, workflow Eval writes, original-image bytes or source-split edits.
- Disabled optional additional V30 model inference in the general cloud workflow and added explicit completed-evidence refusal in the historic one-time workflow. New future paid experiments require a *new* frozen protocol and distinct authorization.

## V31-A — 11 P0 source-family packets reconciled from saved evidence — 2026-11-22

- Reconciled all 11 frozen original Valid P0 source IDs against **33** existing V14 Train-candidate pair records and the prior V18 visual-site evidence. No original photos were re-opened or re-reviewed.
- Archived [machine-readable reconciliation](V31_A_SOURCE_LINEAGE_RECONCILIATION_2026-11-22.json) and [human-readable evidence table](V31_A_SOURCE_LINEAGE_RECONCILIATION_2026-11-22.md); each retains source IDs, Train candidate IDs, SSIM, MAE, embedding, ORB inliers/matches, dimensions and raw-byte comparison.
- Confirmed the existing named-site record: Valid WA0063 and WA0051 plus Train WA0067 and WA0066(1) show School 22 May–Aseefrah. Their two Valid source-family holds remain.
- Corrected interpretation of Valid WA0026: prior visual record names School Shahid Al-Alafi, a distinct named site, so it must not be grouped with School 22 May from the WA filename stem. Its strong pixel/feature match to Train WA0079 remains unresolved; historical hold preserved.
- Stratified the six technical quarantines by corroborating image evidence: very-high alignment for Safety-Glasses-Toolbox-Talk/image_719 and image_153-1-/image_153; high alignment for h20/h2; weaker feature corroboration for v141, v150 and v9. These remain quarantined; similarity scores do not certify source lineage.
- Added [fail-closed V31-A validator](tools/verify_v31a_source_reconciliation.mjs), with mutation self-tests. [Source/reference CI run 44967406330](https://github.com/EZZALDEEN049/Y-PPE-Detection-RFDETR/actions/runs/44967406330) and [public engineering CI run 44967406346](https://github.com/EZZALDEEN049/Y-PPE-Detection-RFDETR/actions/runs/44967406346) both passed.
- **No human source-family signoff was fabricated; 0 holds released; 0 new scoring-eligible images; 0 model inference calls; Test remains unopened; no dataset/model/source-split changes.** The next step is targeted author acquisition/site/session clarification, not another image-quality review.

## V31-A1 — author-attested School 22 May shared-site overlap — 2026-11-22

- The dataset author directly confirmed that Valid WA0063 and WA0051 and Train WA0067 and WA0066(1) belong to the same School 22 May–Aseefrah construction project/site, despite potentially different times/angles.
- Recorded two source-specific `SHARED_CAPTURE_SESSION_OR_SITE` decisions in [the V15 overlay](SOURCE_FAMILY_SIGNED_ATTESTATIONS_V15.json), pinned to [the verbatim chat-evidence transcription](evidence/AUTHOR_CHAT_ATTESTATION_SCHOOL_22_MAY_ASEEFRAH_2026-11-22.md), SHA-256 `326c7ad0347a86822768e4f1703045248247bc3014cd5ccb139148332cc07605`. No capture-session ID or exact-frame identity is asserted.
- Both Valid cases remain **HARD_HOLD_STILL_BLOCKED** because the site family is present in Train. Independent-source attestations remain **0**, independent-scoring eligibility remains **0**, and Valid Person–PPE gold remains **0**.
- Updated the live V31 ledger, added [V31-A1 report](V31_A1_AUTHOR_SITE_ATTESTATION_2026-11-22.md) and [machine record](V31_A1_AUTHOR_SITE_ATTESTATION_2026-11-22.json), and added a SHA-pinned fail-closed validator with mutation tests. The source/reference CI dynamically recompiles the current 459-row audit rather than relying on the earlier pre-attestation snapshot.
- [V31-A1 source/reference CI #44968818900](https://github.com/EZZALDEEN049/Y-PPE-Detection-RFDETR/actions/runs/44968818900) passed the dynamic source audit and SHA/mutation checks; [public engineering CI #44968818901](https://github.com/EZZALDEEN049/Y-PPE-Detection-RFDETR/actions/runs/44968818901) passed.
- No photo reopened, model inference, retraining, Test access, split/annotation edits, or Roboflow mutation.
