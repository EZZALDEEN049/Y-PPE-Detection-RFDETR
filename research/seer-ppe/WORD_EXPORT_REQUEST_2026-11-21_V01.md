# SEER-PPE — Editable Word export request (21 November 2026)

Create from the fully retained, unabridged GitHub sources:
- `research/seer-ppe/MANUSCRIPT_MASTER.md` → `research/seer-ppe/exports/SEER_PPE_Research_Manuscript_v0.20_2026-11-21.docx`
- `research/seer-ppe/SEER_PPE_COMPLETE_HANDOFF_2026-11-21_V21.md` → `research/seer-ppe/exports/SEER_PPE_Complete_Research_Handoff_V21_2026-11-21.docx`

Output DOCX is editable, preserving original Markdown paragraphs, headings, all substantive contents, text tables, academic author/affiliation/correspondence details, calculations, caveats and GitHub references. This is **not a claim of a final publishable paper**, and no new scientific evaluation or Test data access occurs. Word export must not alter the original paper, source datasets, detector or original annotations. PDF rendering in CI is a QA check, not a requested user deliverable.

This request triggers GitHub Actions **SEER-PPE manuscript and full handoff export to editable Word** and saves both DOCX files directly in the repository for cross-account download.
## Refresh requested after V22 verified manuscript integration

The previous V0.20 Word files remain archived and unchanged. The manuscript now advances to **v0.22** with executed V22 annotation class-support results, full Results §4.17, Discussion §5.1–5.6 and Appendix N. Re-run the same vetted converter and checks to save **`SEER_PPE_Research_Manuscript_v0.22_2026-11-21.docx`**, while preserving the V21 handoff DOCX. Validate new manuscript values and Appendix N text, and do not claim newly executed RF-DETR or SEER-PPE safety efficacy.

## Refresh after actually executed V23 original Valid current-source bbox pilot

The working manuscript is now **v0.23**, not v0.22, and includes V23's previously frozen five-original-Valid-image real fixed-model bbox comparison against current author-curated ground truth (23 original boxes, 23 hosted predictions, TP22/FP1/FN1; micro F1 0.956522). The five images are nonrandom and historically development-exposed; this is neither full 459-image independent Valid nor a verified safety-policy improvement. Archive an additional full editable **`SEER_PPE_Research_Manuscript_v0.23_2026-11-21.docx`** with Methods §3.18, Results §4.18, Discussion and Appendix O; preserve V0.20/V0.22 archived Word files and V21 handoff. Run DOCX and render QA and commit the new Word file. No fresh inference is performed by exporting Word.

## Refresh for targeted prior-art and bibliography V24 — latest full manuscript Word

The main canonical working paper has advanced to **v0.24** on 21 November 2026. In addition to the already measured V22/V23 data reference and five original Valid bbox pilot, it now includes a verified, clearly limited **2024–2026 literature overlap matrix**, expanded related work §§2.2/2.3, a selected bibliography with primary DOI links, revised novelty discussion, and Appendix P. Export the **entire** current `MANUSCRIPT_MASTER.md` to a new, genuinely editable `research/seer-ppe/exports/SEER_PPE_Research_Manuscript_v0.24_2026-11-21.docx`. Preserve previous v0.20/v0.22/v0.23 DOCX files and V21 handoff DOCX. Verify author/affiliation, historical and new numeric tables, Appendix O/P, DOI references and the explicit unmeasured SEER comparison. Rendering to PDF is only a layout QA process; no new images/model inference/labels/Test is involved.

## Refresh for real executed V25 A2 versus A5 routing manuscript

The latest master scientific paper is now **working manuscript v0.25**, with new **Methods §3.19**, **Results §4.19**, **Discussion §5.7**, updated limitations, and **Appendix Q**. Those sections describe the genuinely executed deterministic safety-invariant A2 vs A5 selection on **74 already saved real original-model detections** from four Train and five historically exposed original Valid photos. Each proposes eight explanation/review targets, differs on three images, but actually runs **zero XAI, zero real reviews and zero additional RF-DETR inference**. The experiment cannot establish worker safety or energy advantage; no Test accessed. Generate and archive a new fully editable **`research/seer-ppe/exports/SEER_PPE_Research_Manuscript_v0.25_2026-11-21.docx`** via the already configured GitHub workflow, while retaining all previous DOCX versions and the V21 handoff. Validate the entire source manuscript, author details, methods, bibliography and Appendices A–Q, and render via Word/PDF QA. Do not modify original Roboflow model/images/labels or expose private media/URLs.

## Refresh to v0.26 full original Source Valid results — after verified V26 inference and class scoring

The latest canonical research paper is **v0.26**, incorporating **459/459 real newly inferred original Source Valid images**, the original fixed 17-class RF-DETR Small model, same-class IoU≥0.50, M0 **GT3471 / predicted4103 / TP3297 FP806 FN174 / P0.803558 R0.949870 F1 0.870610**, M1=448 F1 0.870064 and M2=367 F1 0.868157, all 17 per-class outcome rows, 13 previous provider reference count mismatch sensitivity and five V23 prior development-exposure sensitivity. These are NEW current-author-reference object detection results, **not** the 2025 provider Eval scores, independent external accuracy, worker PPE compliance, A5 versus A2 or energy/XAI superiority.

Create an editable complete **research/seer-ppe/exports/SEER_PPE_Research_Manuscript_v0.26_2026-11-21.docx**, preserving original author affiliation, research methods **§3.20**, results **§4.20**, discussion **§5.8**, bibliography, appendices **A–R**, and original cumulative manuscript. Preserve all older Word versions and V21 handoff. Run DOCX structure and PDF-render QA then commit the real DOCX on GitHub. No further RF-DETR inference, Test access, human reinspection or source annotation edits during export.


## Refresh for executed V27–V29 target perturbation and hosted timing results — 22 November 2026

The canonical working manuscript is now v0.27 and includes Methods §§3.21–3.23, Results §§4.21–4.23, Discussion §5.9 and Appendices S/T. It reports actual V27 Gaussian target-box occlusion (27 original-model passes), V28 one-step black-fill deletion and target-only insertion (30 archived repeat passes plus 30 unarchived first-attempt passes; total 60 actual V28 calls), and V29 ten direct hosted request-timing calls. It explicitly distinguishes target-box sensitivity from full explanation Faithfulness, one-step deletion/insertion from progressive curves/AUC, request round-trip from model latency, and unavailable memory/Joules/financial cost from measured resources.

Generate the full editable manuscript Word file research/seer-ppe/exports/SEER_PPE_Research_Manuscript_v0.27_2026-11-22.docx from the entire current MANUSCRIPT_MASTER.md. Preserve the existing v0.20/v0.22/v0.23/v0.24/v0.25/v0.26 Word files and the frozen V21 handoff. Verify author/affiliation, all prior V26 tables and Appendices A–R, plus Appendix S, Appendix T, V27/V28/V29 and the numeric values 0.622325, 0.716721, 0.704532, 1.5206, 97 actual model calls. Run DOCX structure and PDF-render QA, then commit the new Word file. Do not overwrite older DOCX versions. Exporting Word performs no new RF-DETR inference, no Test access and no source/model changes.


## V35-D — export the complete v0.38 manuscript to editable Word — 22 November 2026

The canonical manuscript is now **v0.38**. Export the complete `research/seer-ppe/MANUSCRIPT_MASTER.md` to:

`research/seer-ppe/exports/SEER_PPE_Research_Manuscript_v0.38_2026-11-22.docx`

Requirements:
- Preserve the author, affiliation, correspondence, abstract, all tables, Sections 1–7, the 17-reference working bibliography and Appendices A–X.
- Resolve all eleven V34-B figures using Pandoc resource path `research/seer-ppe`; verify exactly eleven embedded media files in the DOCX package.
- Verify that the Word document is structurally valid, editable, and contains the key V26/V34 results, conclusion, references and Appendix X captions.
- Render the v0.38 DOCX to PDF for automated text and page-preview QA. The PDF is a QA artifact; the requested archival deliverable is the editable DOCX.
- Preserve all prior Word versions and the V21 handoff. Do not regenerate or overwrite the old handoff file.
- Commit the new DOCX to the current research branch `research/v30-progressive-xai-2026-11-22`, not to `main`.
- This is a document-export task only: zero new RF-DETR calls, no retraining, no Test access, and no image, annotation, split or model changes.

The workflow must not push generated artifacts to `main`; it must archive the DOCX on the branch that triggered the export.


### V35-D QA correction — 22 November 2026

The first v0.38 export successfully generated a 2.8 MB editable DOCX and verified that all **11 figures are embedded**. The content gate failed only because it incorrectly expected the internal workflow label `V35-C` to appear inside the scientific article; that internal stage label was correctly removed from the manuscript body. The QA assertion has been corrected to check the actual scientific content and the newly added methodological references instead. Re-run the same export and archive only after all content, media, PDF-render and branch-preservation checks pass.


### V35-D render-command correction — 22 November 2026

The v0.38 DOCX generation and content checks now pass, including a valid editable DOCX with 16 tables and exactly 11 embedded figures. The PDF-render step exposed a shell line-continuation error in the workflow (the generated command contained a doubled trailing backslash). The render invocation has been changed to one command line; no manuscript content or research data are affected. Re-run the export and commit only after the PDF text/layout smoke checks pass.


## V35-E — temporary rendered PDF and representative page previews — 22 November 2026

For final visual QA, the v0.38 export workflow should retain a short-lived GitHub Actions artifact containing the 96-page PDF render plus first, middle and final page previews. Use the artifact only for inspection; do not publish it as a final journal PDF before the target journal is selected. Retention is seven days. The editable DOCX remains the canonical manuscript deliverable.


### V35-E DOCX package inspection — 22 November 2026

Include the generated editable DOCX itself in the temporary render-QA artifact alongside the PDF and first/middle/last page previews. This permits inspection of the underlying Word table and section XML where the rendered preview shows narrow/stacked content. The artifact is temporary; the canonical archived manuscript remains the DOCX in the research branch.


## V35-E — correct Word layout and export v0.39 — 22 November 2026

Visual inspection of the v0.38 PDF found two issues that automated text checks had not detected:
- Pandoc wrote all 16 tables at 50% of the printable page width, causing 7–10-column tables to wrap vertically and become unreadable.
- The generated Table of Contents heading appeared without entries on the first page.

The v0.39 workflow must remove the empty TOC generation, set every Word table to 100% of the printable width with explicit column widths, repeat table header rows, prevent row splitting, and use compact readable table fonts. It must assert every table width is 100%, embed all eleven figures, render the PDF, and verify that the first page begins with the article title rather than an empty TOC. Preserve v0.38 as an earlier export; archive v0.39 as a new file. Do not alter any scientific values, images, annotations, model or splits.


### V35-E OOXML width-unit correction — 22 November 2026

The first visual correction revealed that WordprocessingML percentage table widths are stored in fiftieths of a percent: `w:tblW=5000` represents 100%, not 50%. The v0.39 attempt used `10000` (200%), which caused table-cell content to flow incorrectly even though the DOCX structure check passed. The original v0.38 grid columns summed to 7,920 twips and were too narrow for the long 7–10-column tables. The v0.40 export must therefore set `tblW=5000` (100%) while explicitly sizing the `tblGrid` and cell widths to 9,520 twips, preserving all cell text and all 11 images. Recheck actual rendered pages containing the 4.17 cohort table and the V26 class metrics table before acceptance.


### V35-E native Word table export trial — 22 November 2026

The v0.40 PDF still shows narrow headings and table content flowing outside the visible grid despite a valid DOCX structure. The issue appears tied to the custom reference DOCX/table rewriting rather than the scientific source. The v0.41 trial therefore removes the custom reference DOCX and all manual table-grid/cell-width rewriting, allowing Pandoc's native Word template and table layout to remain intact. The DOCX checks must verify all 16 native tables and their nonempty cell text, 11 embedded figures, and the PDF preview. Preserve v0.38–v0.40 as intermediate exports until the rendered v0.41 is visually checked.


## V35-E — split the two wide V26 result tables for publication readability — 22 November 2026

The v0.41 native Pandoc template fixed the narrow heading/paragraph flow and produced actual visible tables. Visual inspection identified two remaining 10-column V26 tables that are technically visible but cramped. In v0.42, split the overall cohort table into counts and metrics, and split the 17-class table into counts and metrics. Shorten only the descriptive labels in the earlier 7-column source-cohort table. Preserve every numeric value exactly. The expected Word table count increases from 16 to 18. Re-export and inspect the V26 pages plus first/middle/last previews.


## V35-E — journal-neutral main article and supplementary package v0.43 — 22 November 2026

The full v0.42 research dossier has been preserved unchanged as `MANUSCRIPT_FULL_RESEARCH_DOSSIER_v0.42_2026-11-22.md`. The clean v0.43 main article now contains the title/author block, a concise stage-neutral abstract, the scored image-level and perturbation methods, the V26/V34 results, the main summary figure and references. Historical non-scoring source-lineage/Person–PPE engineering contracts and appendices A–X have been moved—not deleted—to `SUPPLEMENTARY_MATERIALS_MASTER.md`. The main article retains Figure 1; the ten target-specific paired heatmaps are Supplementary Figures S1–S10.

Export two editable Word deliverables:
- `exports/SEER_PPE_Research_Manuscript_v0.43_2026-11-22.docx` — 18 tables and one main summary figure.
- `exports/SEER_PPE_Supplementary_Material_v0.43_2026-11-22.docx` — historical methods, appendices A–X and ten paired maps.

Verify one embedded figure in the main DOCX and ten in the supplement, all table text, references, title/abstract, conclusion, PDF text and representative page previews. Do not alter any scientific values or run new model inference.
