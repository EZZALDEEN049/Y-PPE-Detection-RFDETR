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
