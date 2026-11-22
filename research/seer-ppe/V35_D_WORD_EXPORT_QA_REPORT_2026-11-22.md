# SEER-PPE V35-D — Editable Word export and automated QA

**Date:** 22 November 2026  
**Branch:** `research/v30-progressive-xai-2026-11-22`  
**Source manuscript:** `MANUSCRIPT_MASTER.md` v0.38  
**Status:** **PASS — editable DOCX archived; automated PDF-render smoke test passed**

## 1. Deliverable

- File: `research/seer-ppe/exports/SEER_PPE_Research_Manuscript_v0.38_2026-11-22.docx`
- GitHub file: https://github.com/EZZALDEEN049/Y-PPE-Detection-RFDETR/blob/research/v30-progressive-xai-2026-11-22/research/seer-ppe/exports/SEER_PPE_Research_Manuscript_v0.38_2026-11-22.docx
- Final archive commit after successful rerun: https://github.com/EZZALDEEN049/Y-PPE-Detection-RFDETR/commit/cbc65acf87f70d06ad6f1930516ce00d2e4f6dc0

## 2. Measured export checks

| Check | Result |
|---|---:|
| DOCX file size | 2,825,912 bytes |
| Word paragraphs | 455 |
| Word tables | 16 |
| Embedded figures | 11/11 |
| Extracted paragraph/table text | 218,183 characters |
| Rendered PDF pages | 96 |
| DOCX ZIP integrity | PASS |
| Key manuscript content checks | PASS |
| PDF text smoke checks | PASS |
| First-page preview generation | PASS |

The export used Pandoc with the explicit resource path `research/seer-ppe`, so all eleven V34-B PNGs were embedded in the Word document. The document remains editable rather than being a flat PDF image.

## 3. Successful CI evidence

- Final Word export, DOCX integrity, 11-image embedding, 96-page PDF render and preview QA: [run 45034033339](https://github.com/EZZALDEEN049/Y-PPE-Detection-RFDETR/actions/runs/45034033339)
- Final source/reference gates: [run 45034033034](https://github.com/EZZALDEEN049/Y-PPE-Detection-RFDETR/actions/runs/45034033034)
- Final public synthetic engineering tests and V34-B figure upload: [run 45034033098](https://github.com/EZZALDEEN049/Y-PPE-Detection-RFDETR/actions/runs/45034033098)
- QA artifact (rendered PDF + first, middle and last page previews): [seer-ppe-v038-render-qa — artifact 14759055979](https://github.com/EZZALDEEN049/Y-PPE-Detection-RFDETR/actions/runs/45034033339/artifacts/14759055979)

The earlier successful run 45033306609 is retained as historical evidence; run 45034033339 is the final verification tied to the archived v0.38 file.

The Word file was committed to the research branch, not `main`. Earlier DOCX versions and the V21 handoff were preserved. The PDF produced by LibreOffice was retained inside the GitHub Actions QA artifact together with first/middle/last page previews; it was not committed to the research branch as a publication-ready PDF.

## 4. Workflow corrections

The previous workflow was stale at v0.27, did not resolve the relative figure paths, validated obsolete manuscript phrases and pushed to `main`. V35-D updated it to:
- generate v0.38 from the complete current Markdown source;
- resolve and verify exactly eleven embedded images;
- validate current results, references, conclusion and Appendix X;
- render PDF text and a first-page preview;
- archive the DOCX on the branch that triggered the workflow.

Initial QA failures were corrected: an assertion that incorrectly expected an internal V35-C label in the article, and a doubled shell line-continuation character in the LibreOffice command. The final run 45034033339 passed all export, content, rendering, preview-upload and archive steps. The final source/reference gate run 45034033034 and public synthetic test run 45034033098 also passed.

## 5. Remaining V35-E work

1. **Visual inspection:** automated PDF text/render smoke tests passed, but a human page-by-page inspection of all 96 pages has not been completed.
2. **Journal length:** 96 pages includes Appendices A–X and the full research handoff history. After selecting a journal, determine which material belongs in the main article and which should become Supplementary Material.
3. **V34-B archive:** retain the manifest-selected canonical figure directory/PDF and explicitly reconcile the nested duplicate PDF during final archive QA.
4. **V27 metadata:** the start/end timestamp warning remains unresolved unless the original execution log is recovered; no inferred correction was made.
5. **Author and journal gates:** ethics/consent, funding, competing interests, author contributions, official IEEE author metadata for the two eSmarTA 2026 records and target-journal style still require confirmation.

## 6. Integrity constraints

- Zero new RF-DETR calls.
- No retraining, Test access, source-image mutation, annotation mutation, split change or original-model change.
- The Word export is a working manuscript artifact, not a guarantee of journal acceptance.
- No final PDF publication package is claimed.

**Decision:** V35-D is complete. V35-E remains the final editorial, visual and archive-quality stage.
