# V40 — Section 14: Zenodo reproducibility archive specification
Date: 2026-11-24. Decision: adopt the colleague's proposed layout with extensions for reproducible curve and historical calculations. This is a preparatory specification, not a public release or deposit.

## Proposed archive title
PPE Cross-Resolution Reproducibility Archive

## Explicit file allowlist and expected content
| File | Purpose and expected records | Source / status |
|:--|:--|:--|
| README.md | Citation, run instructions, study scope, data dictionary, eligibility, missing-data conventions, workflow and reproducibility limits | Draft at R7 after preview test; no DOI invented |
| LICENSE.md | Scope of MIT for eligible owned code and CC BY 4.0 for rights-cleared derived data; third-party exclusions | Author approved scope in R4; separate license texts and provenance review pending |
| requirements.txt | Verified pinned direct and transitive dependencies used for the offline analysis and figure scripts | R7; historical inference environment not fully established |
| validation_metrics.csv | 459 pseudonymous V001–V459 rows with box counts, TP, FP, FN | V26 full-detail per_source; no original identifiers or boxes; preflight |
| validation_class_metrics.csv | Per-cohort/per-class counts for M0/M1/M2 (51 rows) | V26 numerical summary; preflight |
| target_manifest.csv | 48 T01–T48 rows and 24 I01–I24 image groups; category, archived and actual baseline score, IoU, endpoint and matching status | Frozen manifest and V38-B raw results; preflight |
| perturbation_scores.csv | 5,120 target-cell records: 3,840 gray + 1,280 blur; signed drops, scores, exact area fraction and match status | V38-B raw results; preflight |
| spatial_agreement.csv | All 48 targets including three missing coefficients | V38-B audited summary; preflight |
| aligned_density.csv | Matched coarse-region signed-density pairs where estimable | Recomputed from raw cell records; preflight |
| auc_results.csv | 264 executed curve AUCs including each of ten random rankings | V38-B actual curve output; preflight |
| curve_points.csv | 2,904 actual modified-area and normalized-score records (264 × 11), including shared endpoints | Necessary to reproduce trapezoidal AUC; preflight |
| operator_comparison.csv | All 16 selected operator-control targets, including 14 estimable pairs | V38-B raw and audited results; preflight |
| historical_spatial_agreement.csv | 10 historical targets across eight images, retained separately from extension | V34-A archive; preflight |
| historical_aligned_density.csv | 160 historical aligned coarse-region records | V34-A archived signed densities; preflight |
| inference_ledger.jsonl | 9,968 events for 4,984 successful requests; phase, call index, pseudonymous grouping and permitted numeric metadata | Explicit field allowlist; no raw payload or original IDs; preflight |
| analysis/ | Standalone analysis reading only the archive CSV/JSONL files; validation counts, rank correlations, overlap, AUC, bootstrap, sensitivity bounds | Existing cluster code plus independent CSV-only runner and tests to be completed at R7 |
| figures/ | 14 R5 vector PDFs and self-contained scripts reading sanitized numerical tables; include historical native cell values as needed for full figure reproduction | Existing R5 renderer depends on internal sources; adapt at R7, review provenance and final author approval |
| SHA256SUMS.txt | SHA-256 manifest of every released file except itself | Preview manifest limited to numerical outputs; final manifest generated only after approval |

## Release boundaries
- Existing public GitHub working repository retained at author's request; never archive the entire working tree. A Zenodo snapshot is a curated allowlisted subset.
- Do not publish original photographs, source IDs, filenames, target UUIDs, API credentials, request URLs, image hashes, raw boxes, consent documents or raw provider payloads. Do not add original model weights until exact checkpoint identity and redistribution rights are verified.
- Derived numerical content still needs disclosure-risk and rights assessment. Pseudonyms preserve study grouping, not a guarantee of anonymity; no blanket permission to redistribute the dataset is inferred. No linkage table is released between V26 V-series and V38 I-series IDs.
- Missing scores are empty CSV fields or JSON null, not zeros. LOST score is operational zero under fixed output/matching thresholds; ambiguous matches remain undefined. Gray/blur pairs and image-level bootstrap preserve clustering.
- Numerical reproduction from archived matched scores is distinct from rerunning inference, re-matching all predictions to reference boxes, reconstructing original images, or reproducing the hosted provider environment. V26 box-count CSV can reproduce aggregate metrics but not independently re-run box matching. Historical PNG and V38 JPEG cohorts remain separate. Full historical perturbation and curve data still require additional allowlisted export if claiming reproduction of those secondary endpoints.
- Research-specific consent, institutional ethics determination and other rights/author approval gates remain open. No deposit or DOI currently exists. No final ZIP or Zenodo upload before author's explicit request and applicable clearance.

## Internal preflight
Script: research/seer-ppe/tools/preflight_v40_zenodo_numeric_archive.py. Workflow: .github/workflows/seer-ppe-v40-zenodo-numeric-preflight.yml, run 45324237587. It creates a fresh temporary numerical preview, independently checks totals, map rankings, AUCs, clustered resampling and request accounting against saved results, checks identifier patterns and SHA-256, then deletes the preview. The script is not itself the final standalone archive analysis. No outputs are uploaded or committed by this workflow; no model requests.
 
## After an authorized deposit
1. Verify the actual version-specific DOI, archive content, license metadata and access conditions.
2. Update manuscript data/code availability and supplement links with the actual DOI.
3. Update cover letter and Editorial Manager data-availability fields where applicable.
4. Record final checksums, version and release evidence. Do not enter placeholder DOI or claim future hosted replay is proven.

## Verified preflight outcome
Run 45324237587 completed successfully (job 138209846471; CPython 3.11.18). Twelve temporary numerical files plus SHA256SUMS.txt were generated, checked and deleted. All 459 validation counts, 48 manifest targets and 24 image clusters, 5,120 map-cell records, 960 estimable aligned-region records, 264 AUCs, 2,904 curve-point rows, 16 operator targets (14 paired), 10 historical targets and 9,968 ledger events reproduced the stated checks. There were 4,984 reservations and 4,984 successes. The explicit field-allowlist and source/target-ID/UUID text checks passed. Actual file hashes and row counts: V40_SECTION14_ZENODO_NUMERIC_PREFLIGHT_EVIDENCE_2026-11-24.json. The test uses the internal source tree, not a self-contained released archive. It does not prove full rights/privacy clearance, original-image matching reproducibility or future hosted inference replay. The files were not deposited, committed as data, or bundled. R7 must complete standalone reanalysis and figure generation from sanitized files, historical secondary endpoint coverage, dependency pinning, licenses and data dictionary.
