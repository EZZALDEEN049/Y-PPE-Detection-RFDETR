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


## V31-A2 — author confirms WA0026/WA0079 shared scene with modifications/processing — 2026-11-22

- The author clarified that Valid `IMG-20250416-WA0026.jpg` and Train `IMG-20250416-WA0079.jpg` are not the same presented image but depict the same scene with changes/processing.
- Recorded the distinct `SHARED_SCENE_WITH_MODIFICATIONS_OR_PROCESSING` verdict; no byte identity, exact original frame, crop chain, site ID or capture session is inferred.
- Preserved WA0026's pre-existing hard hold and zero independent-source eligibility. Updated the source-family overlay, P0 packet, readiness ledger and compiler enum; added a SHA-pinned evidence record and fail-closed mutation verifier in CI.
- No image reopened, model inference, retraining, Test access, source-split change, annotation edit or Roboflow mutation.

## V31-A3 — aggregate multi-project provenance and completed original curation accepted — 2026-11-22

- The author states that the corpus was assembled across multiple projects and work locations in Yemen associated with civil-society organization projects, for PPE/occupational-safety analysis and solution development.
- Accepted the original image selection/review and dataset curation as completed during preparation, consistent with the V18 author-curator policy. **Per-image worksite/project IDs are not required for the internal image-level detection endpoint; no repeat full-corpus visual review is required.**
- Updated the canonical manuscript, PROTOCOL_MASTER, V18 curation policy, V31 readiness guide, README/START HERE and readiness ledger. The corpus is described at aggregate provenance level; the absence of a complete per-image site/session register remains disclosed.
- Kept cross-split leakage controls separate: two Valid images remain held for shared School 22 May site family; WA0026 remains held for the author-confirmed shared scene with Train WA0079; eight other P0 cases remain unresolved. No hold is released and no independent multi-site generalization is claimed.
- Added [V31-A3 machine record](V31_A3_DATASET_LEVEL_ACQUISITION_CURATION_2026-11-22.json), [methodology decision](V31_A3_DATASET_LEVEL_ACQUISITION_CURATION_2026-11-22.md), [SHA-pinned author evidence](evidence/AUTHOR_DATASET_LEVEL_ACQUISITION_AND_PRIOR_CURATION_2026-11-22.md), and a fail-closed CI verifier with mutation tests.
- Internal image-level detection analysis continues with exact Source-ID/label/prediction joins and M0=459, M1=448, M2=367 overlap-risk sensitivity cohorts; these are not independent-site cohorts. Worker-level safety and signed Valid Person–PPE gold remain separately gated.

- Final V31 source/reference gate [CI run 44971815503](https://github.com/EZZALDEEN049/Y-PPE-Detection-RFDETR/actions/runs/44971815503) passed, including the synchronized three-attestation P0 validator, V31 readiness, V31-A1, V31-A2, V31-A3 and V22 manuscript/source-composition checks.


## V32 — author selects image-level detection and perturbation-XAI scope — 2026-11-22

- The author selected Path 1: limit the current thesis paper to image-level PPE object detection, target-specific black-box perturbation sensitivity and selective explanation/inspection prioritization.
- Explicitly removed complete worker-level Person–PPE gold, task/site mandates, worker compliance/violation, false-clearance, actual human-review efficacy, external/site-independent generalization and physical Joules from the current paper's required endpoints. These are out of scope, not unfinished blockers.
- Retained existing Person–PPE pilot records as exploratory engineering artifacts only; missing fields remain missing and are not imputed or scored. The historical worker-safety flag remains `scoring_ready=false`, but the V32 readiness ledger explicitly states this is not a blocker to the current manuscript.
- Updated canonical manuscript to v0.32 and protocol to v0.8; added [V32 scope decision](V32_IMAGE_LEVEL_DETECTION_XAI_SCOPE_DECISION_2026-11-22.md) and [machine-readable record](V32_IMAGE_LEVEL_DETECTION_XAI_SCOPE_DECISION_2026-11-22.json); synchronized the V31 readiness ledger, handoff guide and repository entry points.
- Primary remaining work: explanation perturbation robustness, a larger matched-budget A5/A6-style image-target comparison, results/figure reconciliation, reference verification and editable Word export.
- No model inference, retraining, Test access, image reopening, original data/annotation/split changes or Roboflow writes were performed for V32.


## V33-A — A5/A6 shared-target and perturbation robustness reanalysis — 2026-11-22

- Independently recomputed all 60 V30 AUCs and performed target-level full-area/first-30%-area saliency-vs-fixed-random comparisons; 8/10 deletion and 9/10 insertion cases favor saliency on full area (descriptive only).
- Explicitly decomposed A5/A6 as six shared exact explanation targets plus two unique selected targets per arm. The conditional six-way 2+2 reassignment does not establish a statistically superior policy; explanation outputs for shared targets are identical.
- Quantified blur baseline saturation (3/10 retain >=80% baseline confidence), inverse-order complementary AUC identities, image-omission sensitivity and 0.004748 maximum nominal-vs-actual area AUC discrepancy.
- [V33 numeric archive](V33_A5_A6_NUMERIC_ROBUSTNESS_2026-11-22.json), [V33 report](V33_A5_A6_NUMERIC_ROBUSTNESS_REPORT_2026-11-22.md) and [V33 fail-closed mutation verifier](tools/verify_v33_existing_xai.mjs) added to CI. Canonical manuscript updated to v0.33; worker-safety V32 scope remains unchanged.
- [V33-B prospective actual 4x4 protocol](V33_B_GRID4_PROSPECTIVE_PROTOCOL_2026-11-22.md) specifies up to 496 new hosted calls **only if separately authorized**; no V33 inference, Test access, model retraining, image re-review or Roboflow mutations occurred in V33-A.


## V33-B — 4x4 runner and pre-inference safeguards — 2026-11-22

- Added `tools/run_v33b_grid4_xai.py`, a separate execution runner for the frozen ten V30 targets and eight original Train/Valid images. It uses a 4x4 grid, exact modified-pixel fractions, saliency and one deterministic random ordering, and the original RF-DETR Small endpoint/settings.
- Added strict SHA-256 matching against the eight-image V30 cloud-runner bundle, exact target/geometry/confidence/arm checks, and fail-closed checks for the protected Test boundary.
- Added a hard ceiling of **496 additional hosted calls** (8 blurred endpoints + 128 shared grid-cell occlusions + up to 360 curve-intermediate calls). The runner refuses inference unless the exact explicit budget flag is supplied.
- Added write-ahead per-call logging to a partial JSON ledger, including failed attempts, and disabled automatic retries. No source images, API credentials, annotations, model weights or Test data are written to the repository.
- Added synthetic regression tests in `tests/test_v33b_grid4_xai.py` for the 4x4 partition, ambiguous-cell handling, curve point/call counts, deterministic random ordering and budget arithmetic; included them in the public engineering CI workflow.
- **Execution remains NOT STARTED.** No V33-B hosted inference calls, Roboflow mutations, retraining, Test access or manuscript performance claims were made by this implementation-only step. The 496-call cap still requires separate author authorization.


## V33-B cloud handoff — 2026-11-22

- Added `.github/workflows/seer-ppe-v33b-authorized-once.yml`, an ephemeral cloud workflow that can only run after a separate authorization JSON is committed with the exact one-time authorization commit message.
- The workflow downloads only the frozen eight Train/Valid originals, performs zero-call SHA/target preflight, checks `ROBOFLOW_API_KEY` without exposing it, and runs the separate 4x4 runner under the fixed 496-call cap.
- A successful numeric result or a failed partial call ledger is archived to the research branch and blocks duplicate paid execution. Raw images and credentials are not committed or uploaded.
- At this preauthorization handoff point, no authorization JSON had yet been created and V33-B had not yet executed; the later successful preflight, one-time authorization and completed run are recorded in the V33-B execution entry below.

- Added `.github/workflows/seer-ppe-v33b-preflight.yml`, a separate no-secret/no-inference cloud preflight that validates the exact eight-image V30 bundle, ten targets and 496-call plan before any budget authorization.


## V33-B — actual 4×4 grid-resolution experiment completed — 2026-11-22 (manuscript v0.34)

- The author explicitly authorized one execution with a hard maximum of 496 additional hosted inference calls. Read-only preflight [45019722753](https://github.com/EZZALDEEN049/Y-PPE-Detection-RFDETR/actions/runs/45019722753) passed first: eight Train/Valid originals downloaded, all eight SHA-256 values matched the V30 cloud-runner bundle, all ten frozen targets passed, zero model calls made.
- The one-time paid cloud run [45019831430](https://github.com/EZZALDEEN049/Y-PPE-Detection-RFDETR/actions/runs/45019831430) succeeded on attempt 1: **496/496 calls successful, zero failed, zero retries** (8 blur endpoints + 128 4×4 cell occlusions + 360 curve-intermediate calls).
- Ten 4×4 maps were rankable; 40 eleven-point curves were executed and 39 AUCs were valid. One saliency-deletion AUC was correctly left null due to an ambiguous target match; no imputation was made.
- Saliency favored one deterministic random ordering in 8/9 scorable deletion curves and 10/10 insertion curves. Saliency-advantage sign agreement between 4×4 and 8×8 was 6/9 comparable deletion targets and 9/10 insertion targets; 10/10 categorical map-rankability statuses matched, which is not spatial map-rank correlation.
- A5 and A6 each retain eight selected slots, six shared and two unique. Shared targets reuse identical target-level curves; all-slot means are composition-dependent and do not establish policy superiority.
- Added [actual results JSON](V33_B_GRID4_ACTUAL_RESULTS_2026-11-22.json), [interpretive report](V33_B_GRID4_ACTUAL_RESULTS_REPORT_2026-11-22.md), [independent numeric audit JSON](V33_B_GRID4_NUMERIC_AUDIT_2026-11-22.json), and [read-only audit script](tools/audit_v33b_grid4_xai.py). [Engineering CI 45020503717](https://github.com/EZZALDEEN049/Y-PPE-Detection-RFDETR/actions/runs/45020503717) passed; maximum AUC recomputation error was 2.22×10⁻¹⁶.
- Updated the canonical manuscript to **v0.34** with Methods 3.25, Results 4.26, Discussion 5.11 and Appendix V. The prospective protocol now records the completed execution and supersedes its earlier pre-run status statements.
- No Test access, retraining, image/annotation/split changes, worker-compliance scoring, causal-faithfulness claim, human-review efficacy, energy measurement or A5/A6 superiority claim.


## V34-A — offline spatial map alignment and rank correlation completed — 2026-11-22 (manuscript v0.35)

- Aligned the ten frozen V30 8×8 and V33-B 4×4 signed gray-occlusion sensitivity maps by exact original-pixel bounds. Each coarse 4×4 region was matched to its four 8×8 child cells using the same floor-based pixel partition.
- Primary comparison used signed score drop per exact cell-area fraction; the four fine-cell values were area-weighted into the coarse region. Negative values were retained. Spearman used average ranks for ties; Kendall tau-b used tie correction.
- Results across ten targets: mean Spearman **0.5416** (median 0.5656; range 0.2295–0.6794), mean Kendall tau-b **0.4239** (median 0.4384; range 0.1514–0.5500). All ten target coefficients were positive. Mean top-four region overlap was **65%**; one Train C Face Masks target had zero top-four overlap (rho 0.230, tau-b 0.151).
- Geometry/integrity: 10/10 target IDs matched; all 20 maps rankable; map/trial maximum difference zero; max 4×4/four-child area partition discrepancy 6.94e-18; no null cell scores. The 26 V30 and 17 V33-B LOST outcomes remained numeric under the frozen zero-score rule.
- **Zero new model inference calls**, no Test access, no retraining, and no changes to images, annotations or splits. Results are descriptive only and do not establish causal faithfulness, external explanation truth, worker compliance, A5/A6 superiority or independent-site generalization.
- Added [V34-A aligned-map JSON](V34A_SPATIAL_MAP_ALIGNMENT_RANK_CORRELATION_2026-11-22.json), [report](V34A_SPATIAL_MAP_ALIGNMENT_RANK_CORRELATION_REPORT_2026-11-22.md), [offline analyzer](tools/analyze_v34a_spatial_map_alignment.py) and [synthetic tests](tests/test_v34a_spatial_map_alignment.py). Engineering CI [45022533089](https://github.com/EZZALDEEN049/Y-PPE-Detection-RFDETR/actions/runs/45022533089) passed.
- Updated canonical manuscript to **v0.35** with Methods 3.26, Results 4.27, Discussion 5.12 and Appendix W. The remaining paper work is final numeric/reference reconciliation and editable Word export.


## V34-B — data-derived scientific figures completed — 22 November 2026 (manuscript v0.36)

- Generated ten paired 8×8/4×4 target heatmaps and one summary chart directly from the V34-A archived aligned maps; no synthetic/illustrative heatmap values were used.
- Left panels reconstruct all 64 native 8×8 fine-cell signed score-drop densities. Right panels show the direct 4×4 map. Gold outlines show the four highest-ranked pooled 4×4 footprints (as 2×2 blocks on the fine map) and the four direct 4×4 regions.
- One shared symmetric diverging scale centered at zero: **±15.470900859749108**, the 97.5th percentile of absolute values across 800 displayed cells. **17/800 (2.125%)** are saturated for display only; rank ordering and all metrics use un-clipped values.
- Independently recomputed Spearman rho, Kendall tau-b, both top-four sets and overlap for all ten targets; all matched the V34-A archive. Two synthetic tests passed.
- Aggregate values remain mean Spearman **0.5416**, mean Kendall tau-b **0.4239**, mean top-four overlap **65%**. Train C Face Masks remains lowest (rho 0.2295; tau-b 0.1514; overlap 0/4).
- Outputs committed under [figures/V34B_2026-11-22/](figures/V34B_2026-11-22/): ten PNGs, summary PNG, 11-page PDF, CSV, JSON manifest and generation report. Reproducible [renderer](tools/render_v34b_scientific_figures.py) and [synthetic tests](tests/test_v34b_scientific_figures.py) are committed.
- Engineering CI [45024788647](https://github.com/EZZALDEEN049/Y-PPE-Detection-RFDETR/actions/runs/45024788647) passed, including figure generation, artifact upload and commit of generated figure files to the research branch.
- Zero new detector calls; no Test access, retraining, or dataset/annotation/split mutation. Updated manuscript to **v0.36** (Methods 3.27, Results 4.28, Discussion 5.13, Appendix X). Remaining paper work is final numeric/reference reconciliation and editable Word export.


## V35-C — focused literature and editorial audit — 22 November 2026 (manuscript v0.38)

- Expanded the working reference list from 9 to **17 sources**, adding foundational perturbation, deletion/insertion, saliency-sanity, quantitative-baseline and rank-correlation sources.
- Checked the focused reference set against official proceedings, publisher and institutional records where accessible. The two eSmarTA 2026 author lists remain secondary-index-only pending final IEEE metadata or author-PDF confirmation.
- Reframed the related-work section as a focused, non-systematic review; no PRISMA/systematic-search claim is made.
- Added explicit method citations and clarified that parameter/label randomization sanity checks were not performed and one deterministic random ordering is only a limited control.
- Added a substantive Section 7 conclusion based on the audited image-level results and their limits. Removed the internal V35 workplan from the article body; editorial closure status is now recorded in the V35-C audit report.
- Added author-confirmation gates for ethics/consent, funding, competing interests and author contributions. The target journal is not yet selected, so final style/length requirements remain open.
- Zero new model calls; no Test access, retraining, image/annotation/split mutation or original-model changes.
- Added [V35-C report](V35_C_LITERATURE_AND_EDITORIAL_AUDIT_REPORT_2026-11-22.md) and [machine-readable audit](V35_C_LITERATURE_AND_EDITORIAL_AUDIT_2026-11-22.json).


## V35-D — editable Word manuscript export and automated QA — 22 November 2026

- Generated and archived the complete **v0.38 editable Word manuscript** at `exports/SEER_PPE_Research_Manuscript_v0.38_2026-11-22.docx` (2,825,912 bytes; 455 paragraphs; 16 tables; 218,183 extracted text characters).
- Verified **11/11 embedded figures**, DOCX ZIP integrity and key scientific content.
- LibreOffice rendered the DOCX to a 96-page PDF; PDF text smoke checks and first-page preview generation passed. The QA PDF was temporary and was not archived.
- Updated the Word workflow to use the current manuscript, resolve figure paths, validate current content and archive only on the triggering research branch.
- Successful CI: Word export [45033306609](https://github.com/EZZALDEEN049/Y-PPE-Detection-RFDETR/actions/runs/45033306609), source/reference gates [45033306627](https://github.com/EZZALDEEN049/Y-PPE-Detection-RFDETR/actions/runs/45033306627), unit tests [45033306726](https://github.com/EZZALDEEN049/Y-PPE-Detection-RFDETR/actions/runs/45033306726).
- Zero new model calls; no retraining, Test access, source-image/annotation/split mutation or model changes.
- V35-E remains for human visual inspection, main-paper/supplement split after journal selection, duplicate-PDF reconciliation, the unresolved V27 timestamp and author/journal declarations.
- Added [V35-D QA report](V35_D_WORD_EXPORT_QA_REPORT_2026-11-22.md) and [machine-readable export record](V35_D_WORD_EXPORT_QA_2026-11-22.json).
