# V40 cumulative compliance register — batches 01–02 (items 01–56)

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
| 02 | Article type | PORTAL CHECK | Sole author delegated selection; recommend Original Research Paper. Verify exact selectable portal label. |
| 03 | Scientific title | SOURCE VERIFIED | Retained author-approved informative full title; no unclear abbreviation. |
| 04 | Final title page | SOURCE UPDATED / PROOF PENDING | Author confirmed sole roster, affiliation, correspondence and ORCID. P.O. Box 6803 corroborated by WHED and published correspondence; confirm mailing address and inspect final Word title page. |
| 05 | Author names/order | AUTHOR CONFIRMED | Ezzaldeen Al-Tayar, sole author as explicitly stated on 2026-11-24; final authorship eligibility and rights for reused collaborative materials still require check. |
| 06 | Affiliations | AUTHOR CONFIRMED / POSTAL CHECK | Faculty of Engineering and Information Technology, Taiz University, Taiz, Yemen confirmed. P.O. Box 6803 corroborated by IAU WHED and published correspondence, pending final author proof. |
| 07 | Correspondence | AUTHOR CONFIRMED | Sole author is corresponding author; existing email explicitly confirmed. |
| 08 | ORCID | AUTHOR CONFIRMED / PORTAL CHECK | Author supplied ORCID 0009-0003-9506-6669; ISO 7064 MOD 11-2 checksum valid. Account ownership/authentication and mandatory portal field not independently verified. |
| 09 | Abstract length | SOURCE VERIFIED | 225 whitespace-separated words including headings, excluding keywords; within archived author-provided ≤250 limit. Recount actual final DOCX. |
| 10 | Abstract content | SOURCE VERIFIED / CORRECTED | Defined AUC, clarified internal detection and initial study; objective/method/results/conclusion present, no bibliographic citations, unchanged numerical endpoints. |
| 11 | Keywords | SOURCE VERIFIED | Six terms: personal protective equipment; RF-DETR; explainable artificial intelligence; perturbation sensitivity; spatial robustness; object detection. |
| 12 | Highlights count | SOURCE VERIFIED / CORRECTED | Five revised standalone editable-source bullets. |
| 13 | Highlights length | SOURCE VERIFIED / CORRECTED | 77/69/72/76/77 characters excluding list marker; each ≤85 according to archived guide excerpt; confirm final exported text. |
| 14 | Graphical abstract | POLICY VERIFIED / ARTWORK PENDING | Author authorizes preparation in accordance with policy. Elsevier general requirements: 1328 × 531 px minimum, 300 dpi, separate file, dedicated professional/scientific illustration tool, no general-purpose generative image tool. Journal-specific requirement remains unknown; no graphic created. |
| 15 | Article structure | SOURCE VERIFIED | Abstract, keywords, Introduction, Materials and methods, Results, Discussion, Conclusion, declarations, supplement, AI statement, References; numbered sections 1–5. |
| 16 | Research gap | SOURCE VERIFIED | Bounded cross-grid matched-target rank agreement and fill-operator dependence, distinguished from published D-MFPP; no unsupported universal novelty assertion. |
| 17 | Scientific originality | AUTHOR CONFIRMED / PARTIAL OVERLAP AUDIT | Author confirms new cross-grid results and no concurrent submission. Three prior full texts inspected; Y-PPE 2,327 images/16,520 labels reuse explicitly disclosed. No same 8×8/4×4 endpoint found in these texts; 2025 decision-system full text and exact rights/text/figure overlap still pending. |
| 18 | Detailed methodology | SOURCE VERIFIED / CORRECTED | Added exact archived same-class IoU ≥0.50, ambiguity margin ≤0.03, baseline drift gate >0.08, Gaussian radius formula, prespecified equal-image primary endpoint. Verified against V38-B protocol and executable runner/gaussian_blur_baseline implementation. Public preregistration not asserted; use prospectively specified. |
| 19 | Original numerical results | PARTIAL | Recomputed from stored S2 rounded target rows: 48 total, 45 estimable, mean rho 0.648988889, mean tau 0.519737778, mean overlap 0.666666667, and micro-F1 0.870609982 from archived TP/FP/FN. No new full raw-ledger audit claimed. Prior immutable audits retained. |
| 20 | Statistical analysis | PARTIAL | S2 median 0.6873 and 11/45 <0.50 reproduced from displayed rows; image bootstrap/LOIO and paired operator reported against frozen secondary-statistics report. No fresh raw bootstrap computation. Explicit descriptive clustered inference and missingness. |
| 21 | Discussion/conclusions | SOURCE VERIFIED / CORRECTED | Clarified 65% overlap belongs to initial ten-target cohort; distinguish both cohorts, keep all measured conclusions. |
| 22 | Boundaries of claims | SOURCE VERIFIED | No causal explanation correctness, independent site validation, worker-level compliance, safety outcome or D-MFPP superiority. |
| 23 | Fonts/margins | EXPORT/GUIDE CHECK | Final Word style and journal-specific requirements not verified. Use conventional readable single-column layout pending confirmed rules; inspect rendered pages. |
| 24 | Page/line numbers | EXPORT/GUIDE CHECK | Final Word pagination and required line numbering pending; do not invent mandatory journal formatting. |
| 25 | Word/page count | PARTIAL | Working Markdown has 6,666 whitespace-separated tokens, including tables, Markdown, declarations and references; not a Word count. Final document page and actual word count pending. |
| 26 | Tables | PARTIAL / SOURCE CORRECTED | Six sequential captions and in-text citations, all Markdown data rows preserved; final native Word tables, border/shading, caption placement, non-splitting and page rendering still require new QA. Former results Tables 1–5 now Tables 2–6; prior Table 4 becomes Table 5, so update old QA rules for intact extension table. |

**Interpretation:** SOURCE VERIFIED means the source-level check is complete, not a certification that the final DOCX or current complete journal guide has passed. 12 previously source-verified/corrected (01,03,09–13,15,16,18,21,22); author confirmations now recorded for 05–08, with the postal/portal checks retained; 17 remains partial. No final document certification. No overall compliance percentage or acceptance probability is claimed.

## Actual changed source files

- `RINENG_MANUSCRIPT_V40_BATCH01_WORKING_UNSIGNED_2026-11-24.md` — abstract, table numbering/references, methodology specificity, study boundaries, no changed table rows.
- `RINENG_SUPPLEMENT_V40_S1_WORKING_UNSIGNED_2026-11-24.md` — corrected associated manuscript title; unchanged table rows.
- `RINENG_SUPPLEMENT_V40_S2_WORKING_UNSIGNED_2026-11-24.md` — prospective protocol terminology; unchanged table rows.
- `RINENG_Highlights_V40_WORKING_2026-11-24.md` — five clarified highlights, no new results.
- `RINENG_TITLE_PAGE_V40_WORKING_UNSIGNED_2026-11-24.md` — candidate only, explicit ORCID gate.

**Scientific lock:** RF-DETR Small checkpoint, 459 validation images, 24 extension images/48 targets/45 estimable, 4,984 successful calls, all numerical table rows and historical source archives unchanged. No actual journal submission or Zenodo deposit. Next batches extend this register, and clean final packages are issued only after the user requests them and required gates are resolved.

## Author update, 2026-11-24
Sole author confirms name, affiliation, corresponding author/email, ORCID, no previous publication of the present cross-grid XAI results and no prior journal submission of this manuscript. Delegates article type selection and authorizes policy-compliant graphical abstract preparation. No authorization to submit. Full rights, ethics, funding, conflicts, CRediT, AI signoff and final proof remain open. See V40_AUTHOR_METADATA_AND_PRIOR_WORK_AUDIT_2026-11-24.md.

## Batch 02 — items 27–56 (2026-11-24)

| ID | Requirement | Current status | Evidence/action and remaining condition |
|:--|:--|:--|:--|
| 27 | Figure numbering | SOURCE CORRECTED | Main Figures 1–3 now explicitly cited; S1 Figures S1–S10 cited. Final native rendering and artwork aliases must be verified. |
| 28 | Artwork resolution/dimensions | BINARY HEADER VERIFIED / RE-EXPORT PENDING | All 13 actual GitHub PNG headers inspected; nominal 300 dpi. Figure 1 3970×2174; Figure 2 3784×1564; Figure 3 3784×1474; S1–S10 each 3377×2255. Elsevier general guidance 300 halftone, 500 combination, 1000 bitmapped line art; prefer vector output for plots and check effective resolution at publication size. Do not assert all are compliant merely because 300 dpi. |
| 29 | Artwork publication rights | AUTHOR ATTESTED / TECHNICAL CHECK | Author reports image and depicted-person publication permissions; no written permissions inspected. Derived numerical artwork preferred; final privacy/rights and render QA remain. |
| 30 | Equations/symbols | SOURCE CORRECTED | Defined pooled P/R/F1 using TP/FP/FN; existing signed score/area-normalization equations retained. Native Word equation and visual QA pending. |
| 31 | Citations/references | PARTIAL | 19 bibliography entries (18 previous plus primary D-RISE reference); author–date form retained, 4 prior works transparently cited. Need complete citation-to-reference mapping, final publisher metadata and exact guide style. |
| 32 | DOI validity | TITLE/IDENTIFIER SCREEN PASS | 15 DOI identifiers (14 previous plus D-RISE DOI verified against indexed CVPR metadata) indexed records/titles in public search (publisher or bibliographic records); remaining four works have conference/archive URLs. Not a complete live resolver/metadata audit; check final authors, year, pages and links. |
| 33 | English language | PARTIAL / SOURCE CORRECTED | Adjusted sole-author declarations, consistency and cover letter; full final copyediting and author proof remain. |
| 34 | Supplement S1 | SOURCE CORRECTED / EXPORT PENDING | Unified section numbering, title, citations and replaced raw Validation image IDs with aliases in prose/table. Numerical columns preserved. Planned artwork-publication PDF links require renderer execution and inspection. |
| 35 | Supplement S2 | SOURCE VERIFIED / EXPORT PENDING | Updated terminology and removed internal status line; all numeric table rows identical. 48-target, 45 estimable and 17-class tables retained. |
| 36 | Data availability | AUTHOR POLICY APPROVED / DEPOSIT PENDING | Author approved Zenodo archive of results, code and permitted data only. No DOI created; verify rights, licenses, metadata and final data statement. |
| 37 | Code availability | PARTIAL | Existing analysis, renderer, runner and requirements files verified. Root listing showed no LICENSE filename. License, exact environment and sanitization must be resolved before public archival. |
| 38 | Reproducibility | PARTIAL | Stored V34-B audit and scripts and V38-B pipeline inspected. Earlier numeric cross-check retained. New candidate renderer not run; no independent full rerun or additional inference. |
| 39 | Fixed repository version | TECHNICAL PIN VERIFIED / RELEASE PENDING | Commit d76ebc595cff628f21231b45dab51170dc82b405 verified by reading V38-B runner at that commit. This is a stable technical source snapshot, not a rights-approved final release or Zenodo DOI. |
| 40 | Ethical approval/exemption | INSTITUTIONAL DETERMINATION PENDING | Prior field-engineer/source provenance testimony and new publication-permission attestation reviewed. Retrospective computational analysis described; no actual approval or exemption document located. Request competent institutional determination; do not equate image consent with ethics exemption. |
| 41 | Privacy of persons | AUTHOR ATTESTED / TECHNICAL CHECK | Author reports publication permissions for images and persons. Written scope not inspected; omit identifiable photos and raw identifiers from proposed public archive unless specifically cleared. Child annotations (31 boxes in 22 images) require explicit applicable safeguards and permission scope; no raw photos or personal records in intended public release. Final artwork/metadata audit remains. |
| 42 | Organization/project permissions | SCOPE NOT VERIFIED | Prior Case C rights records show publisher PWP and author photographer testimony, but no verified institutional release. New author response did not separately answer organization permissions. Verify applicable written rights and employer/project conditions. |
| 43 | Funding/in-kind support | AUTHOR CONFIRMED / SOURCE UPDATED | Self-funded, no research grant, free research plan or granted Roboflow credits; disclose both. Exact type of support and provider role to be confirmed at proof. |
| 44 | Competing interests | AUTHOR CONFIRMED / FORM PENDING | Author declares no known competing interests; text inserted, disclose computational support via publisher tool as applicable. |
| 45 | Acknowledgments | AUTHOR CONFIRMED / SOURCE CLOSED | Author reports no special acknowledgments; placeholder removed. Roboflow support disclosed in funding statement. |
| 46 | CRediT | AUTHOR CONFIRMED / SOURCE UPDATED | Exactly 11 selected roles entered. Data curation, Supervision and Funding acquisition not selected and not inferred. Prior collaborative authorship eligibility remains separate. |
| 47 | AI disclosure | AUTHOR DISCLOSURE APPROVED / PROOF PENDING | Author approves disclosure of all actual uses; declaration updated. Final human review/edit and responsibility statement pending. |
| 48 | AI in research | AUTHOR DISCLOSURE APPROVED / TECHNICAL CHECK | Methods and disclosure describe actual AI-assisted code, writing, analysis support and plotting; environment and final human verification remain. |
| 49 | Prior publication overlap | PARTIAL | Previous three full-text comparison and fourth abstract audit retained; no same cross-grid endpoint found in three texts; source corpus reused and explicitly cited. Remaining full text, thesis/reuse rights and exact similarity open. |
| 50 | Concurrent submission | AUTHOR CONFIRMED | Sole author explicitly confirmed no previous journal submission of this manuscript; recorded in manuscript/cover letter. Reconfirm at submission. |
| 51 | Cover letter | SOURCE CORRECTED / AUTHOR PENDING | New V40 letter aligned with sole author, study limits, distinct contribution and author-confirmed exclusivity. Final proof and outstanding declarations needed. |
| 52 | Submission file formats | GENERAL POLICY VERIFIED / PORTAL PENDING | Editable manuscript DOCX, editable highlights, separate suitable artwork and supplements proposed; full journal-specific guide/slots and exported files still unverified. |
| 53 | Anonymization policy | GUIDE CHECK | Third-party summary reports single-anonymized review; not treated as official confirmation. Verify live guide/portal; retain named title-page source pending instructions. |
| 54 | Editorial Manager requirements | PORTAL CHECK | Actual logged-in journal submission fields not accessed; verify selectable article type, author fields, declarations, file slots, data/AI statements and generated proof before submission. |
| 55 | Final author approval | PENDING | New declaration answers recorded, but ethics determination, organization rights, permitted archive, final human proof and explicit submission authorization remain. |
| 56 | Post-acceptance production | NOT APPLICABLE NOW | No acceptance or submission; proofing/license/production requirements apply later. |

**Batch 02 source modifications:** working main manuscript, S1, S2, and new V40 cover letter; candidate offline artwork renderer `research/seer-ppe/tools/render_v40_publication_artwork_candidate.py` saved but not executed. S1 figure links are planned outputs, not validated existing files. No final DOCX/PDF/package or DOI deposit. All numerical results preserved. Artwork evidence and references: see V40_BATCH02_TECHNICAL_EVIDENCE_2026-11-24.md. Existing source audits remain unchanged; final document formatting, full guide and logged-in portal checks remain outstanding.

## Batch 02 author response (2026-11-24)
Author confirms image/person publication permissions, self-funding without a grant, free research plan or granted Roboflow credits, no known competing interests, no acknowledgments, 11 selected CRediT roles, comprehensive AI disclosure and archive of authorized results/code/data. Organization/project permissions and institutional ethics determination are not independently established. No signature, approval number, provider-role claim or DOI invented. See V40_BATCH02_AUTHOR_DECLARATIONS_AND_ETHICS_ROUTE_2026-11-24.md.

## Colleague reviewer 1 — AI-01–AI-10, 2026-11-24
Source revisions implemented in manuscript, Highlights, cover letter and S2. Abstract 233 words; Highlights 77/78/72/76/76 characters; original numeric table rows unchanged. New descriptive verification from archived frozen manifest and audited records: eligible image pool 225, selected confidence and IoU ranges, LOST counts 45/3072 and 52/768. D-RISE primary citation added (19 references, 15 DOI identifiers; final full bibliography review remains). All ten comments addressed with bounded claims; no direct D-RISE/D-MFPP, second detector, independent site, lower threshold replay, human reference or additional grid experiments performed. See V40_REVIEWER01_AI_RESPONSE_AND_IMPLEMENTATION_2026-11-24.md. Final package and Zenodo draft must reflect this revision when requested; no new export or deposit now. Existing release gates remain.

## Colleague reviewer 2 — occupational safety and PPE, 2026-11-24
All 17 class totals rechecked against V26 M0: GT 3471, predictions 4103, TP 3297, FP 806, FN 174; macro-F1 0.8678108196461584. Goggles F1=0.9037037037037037 (90.37%, not 90.41% in reviewer report); manuscript S2 correct. New Figure 4 is a vector conceptual workflow candidate, not field validation, with explicit human assessment/no automatic clearance and AI-assistance disclosure. It is saved as SVG; author review, final visual/export QA and updated figure counts pending. Ethics request amended to address Child annotation category and applicable legal-representative safeguards; institutional determination and organization permission scope still open. No raw photos or personal records in proposed public archive. No new experiments or final packages. See V40_REVIEWER02_OHS_RESPONSE_AND_IMPLEMENTATION_2026-11-24.md.
