# V35-D — editable Word export request for manuscript v0.38

**Date:** 22 November 2026  
**Branch:** `research/v30-progressive-xai-2026-11-22`

Generate the complete current `research/seer-ppe/MANUSCRIPT_MASTER.md` as the editable file:

`research/seer-ppe/exports/SEER_PPE_Research_Manuscript_v0.38_2026-11-22.docx`

Required checks:
1. Preserve the author, affiliation, correspondence, abstract, all tables, Sections 1–7, 17 working references and Appendices A–X.
2. Resolve and embed all eleven V34-B figures using Pandoc resource path `research/seer-ppe`; assert exactly 11 embedded images in the DOCX package.
3. Verify DOCX integrity, editability, 16+ tables, conclusion, references, V26/V34 numeric results, and Appendix X figure captions.
4. Render the DOCX to PDF with LibreOffice, verify PDF text includes the manuscript title, conclusion, references and Figure 11, and render a first-page preview.
5. Archive only the new v0.38 DOCX on this research branch. Preserve earlier DOCX versions and the V21 handoff; do not push to `main`.

This is a document-only operation: no RF-DETR inference, no retraining, no Test access, and no modification of images, annotations, splits or model weights.

The workflow's first attempt generated a valid 2.8 MB DOCX with 16 tables and exactly 11 embedded figures. The content assertion was corrected to remove an internal stage label that is not part of the paper. The remaining PDF-render shell continuation was corrected to a single-line LibreOffice invocation. Re-run the export and archive only after all gates pass.
