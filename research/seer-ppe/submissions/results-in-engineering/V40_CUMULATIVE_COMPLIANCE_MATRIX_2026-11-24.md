# V40 cumulative compliance register — batch 01 (items 01–26)

**Date:** 2026-11-24. **Target:** Results in Engineering. **State:** working source revisions only; not approved for submission. No new inference, retraining, dataset changes or new experimental claims.

## Authority and coverage

- Target-journal landing page: https://www.sciencedirectelsevier.com/journal/Results-in-Engineering (broad engineering scope). Directly relevant research-paper precedent: https://doi.org/10.1016/j.rineng.2024.103498.
- Official current full guide https://www.sciencedirect.com/journal/results-in-engineering/publish/guide-for-authors returned HTTP 403 in this batch. The archive `V37_B_USER_PROVIDED_JOURNAL_GUIDE_CROSSWALK_2026-11-23.md` records the earlier author-provided partial guide (abstract ≤250 words; 1–7 keywords; 3–5 highlights ≤85 characters; editable tables; title metadata). Do not misrepresent it as live complete verification.
- Publisher general technical preparation: https://www.elsevier.support/publishing/answer/how-do-i-prepare-my-files-for-submission-in-editorial-manager. Journal submission login https://editorialmanager.sciencedirectelsevier.com/submit-paper/Results-in-Engineering supports ORCID login; that does not establish mandatory ORCID for each author.
- Actual V39-R1 manuscript and historical S1 and revised S2 sources inspected; final V40 Word/PDF not yet generated, old binary could not be downloaded into local environment in this batch. Font/line/page/table formatting remains an export-stage gate.

## Register (original item numbering preserved)

| ID | Requirement | Current status | Evidence/action and remaining condition |
|:--|:--|:--|:--|
| 01 | Journal scope | SOURCE VERIFIED | Engineering diagnostic use case; journal has directly related industrial object-detection XAI paper DOI 10.1016/j.rineng.2024.103498. Suitability does not imply acceptance. |
| 02 | Article type | PORTAL CHECK | Recommend full original research paper; published precedent uses Research paper label. Verify exact selectable type at submission. |
| 03 | Scientific title | SOURCE VERIFIED | Retained author-approved informative full title; no unclear abbreviation. |
| 04 | Final title page | AUTHOR PENDING | New V40 working title-page source prepared; no final author/affiliation certification. |
| 05 | Author names/order | AUTHOR PENDING | Existing provisional single-name block retained; confirm complete eligible roster/order and approvals. |
| 06 | Affiliations | AUTHOR PENDING | Existing faculty/university/city/country retained; verify institutional English spelling and full mailing address. |
| 07 | Correspondence | AUTHOR PENDING | Existing provisional author/email retained; confirm correspondence identity, email and address. |
| 08 | ORCID | PORTAL/AUTHOR CHECK | ORCID login supported by portal; author identifier and mandatory field status not verified. |
| 09 | Abstract length | SOURCE VERIFIED | 225 whitespace-separated words including headings, excluding keywords; within archived author-provided ≤250 limit. Recount actual final DOCX. |
| 10 | Abstract content | SOURCE VERIFIED / CORRECTED | Defined AUC, clarified internal detection and initial study; objective/method/results/conclusion present, no bibliographic citations, unchanged numerical endpoints. |
| 11 | Keywords | SOURCE VERIFIED | Six terms: personal protective equipment; RF-DETR; explainable artificial intelligence; perturbation sensitivity; spatial robustness; object detection. |
| 12 | Highlights count | SOURCE VERIFIED / CORRECTED | Five revised standalone editable-source bullets. |
| 13 | Highlights length | SOURCE VERIFIED / CORRECTED | 77/69/72/76/77 characters excluding list marker; each ≤85 according to archived guide excerpt; confirm final exported text. |
| 14 | Graphical abstract | GUIDE CHECK | No verified requirement from complete current guide. If needed, author-prepared compliant non-generative diagram based on actual data; do not invent requirement or produce unapproved art. |
| 15 | Article structure | SOURCE VERIFIED | Abstract, keywords, Introduction, Materials and methods, Results, Discussion, Conclusion, declarations, supplement, AI statement, References; numbered sections 1–5. |
| 16 | Research gap | SOURCE VERIFIED | Bounded cross-grid matched-target rank agreement and fill-operator dependence, distinguished from published D-MFPP; no unsupported universal novelty assertion. |
| 17 | Scientific originality | AUTHOR PENDING | Prior-work scope matrix explicitly captioned and cited. Author/rights overlap audit against full prior works remains necessary; no certification. |
| 18 | Detailed methodology | SOURCE VERIFIED / CORRECTED | Added exact archived same-class IoU ≥0.50, ambiguity margin ≤0.03, baseline drift gate >0.08, Gaussian radius formula, prespecified equal-image primary endpoint. Verified against V38-B protocol and executable runner/gaussian_blur_baseline implementation. Public preregistration not asserted; use prospectively specified. |
| 19 | Original numerical results | PARTIAL | Recomputed from stored S2 rounded target rows: 48 total, 45 estimable, mean rho 0.648988889, mean tau 0.519737778, mean overlap 0.666666667, and micro-F1 0.870609982 from archived TP/FP/FN. No new full raw-ledger audit claimed. Prior immutable audits retained. |
| 20 | Statistical analysis | PARTIAL | S2 median 0.6873 and 11/45 <0.50 reproduced from displayed rows; image bootstrap/LOIO and paired operator reported against frozen secondary-statistics report. No fresh raw bootstrap computation. Explicit descriptive clustered inference and missingness. |
| 21 | Discussion/conclusions | SOURCE VERIFIED / CORRECTED | Clarified 65% overlap belongs to initial ten-target cohort; distinguish both cohorts, keep all measured conclusions. |
| 22 | Boundaries of claims | SOURCE VERIFIED | No causal explanation correctness, independent site validation, worker-level compliance, safety outcome or D-MFPP superiority. |
| 23 | Fonts/margins | EXPORT/GUIDE CHECK | Final Word style and journal-specific requirements not verified. Use conventional readable single-column layout pending confirmed rules; inspect rendered pages. |
| 24 | Page/line numbers | EXPORT/GUIDE CHECK | Final Word pagination and required line numbering pending; do not invent mandatory journal formatting. |
| 25 | Word/page count | PARTIAL | Working Markdown has 6,666 whitespace-separated tokens, including tables, Markdown, declarations and references; not a Word count. Final document page and actual word count pending. |
| 26 | Tables | PARTIAL / SOURCE CORRECTED | Six sequential captions and in-text citations, all Markdown data rows preserved; final native Word tables, border/shading, caption placement, non-splitting and page rendering still require new QA. Former results Tables 1–5 now Tables 2–6; prior Table 4 becomes Table 5, so update old QA rules for intact extension table. |

**Interpretation:** SOURCE VERIFIED means the source-level check is complete, not a certification that the final DOCX or current complete journal guide has passed. 12 source-verified/corrected (01,03,09–13,15,16,18,21,22), 4 partial (19,20,25,26), 10 author/portal/guide/export gates pending. No overall compliance percentage or acceptance probability is claimed.

## Actual changed source files

- `RINENG_MANUSCRIPT_V40_BATCH01_WORKING_UNSIGNED_2026-11-24.md` — abstract, table numbering/references, methodology specificity, study boundaries, no changed table rows.
- `RINENG_SUPPLEMENT_V40_S1_WORKING_UNSIGNED_2026-11-24.md` — corrected associated manuscript title; unchanged table rows.
- `RINENG_SUPPLEMENT_V40_S2_WORKING_UNSIGNED_2026-11-24.md` — prospective protocol terminology; unchanged table rows.
- `RINENG_Highlights_V40_WORKING_2026-11-24.md` — five clarified highlights, no new results.
- `RINENG_TITLE_PAGE_V40_WORKING_UNSIGNED_2026-11-24.md` — candidate only, explicit ORCID gate.

**Scientific lock:** RF-DETR Small checkpoint, 459 validation images, 24 extension images/48 targets/45 estimable, 4,984 successful calls, all numerical table rows and historical source archives unchanged. No actual journal submission or Zenodo deposit. Next batches extend this register, and clean final packages are issued only after the user requests them and required gates are resolved.
