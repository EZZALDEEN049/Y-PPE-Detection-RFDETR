# V36 — Results in Engineering editorial submission package and automated QA

**Date:** 23 November 2026  
**Selected target:** *Results in Engineering* (Elsevier); **final journal choice approved by the author**  
**Editorial package status:** **PASS for document-generation and automated text/figure/PDF QA; AUTHOR/JOURNAL GATES STILL OPEN**  
**Actual publisher submission status:** **NOT SUBMITTED**  
**Research branch:** `research/v30-progressive-xai-2026-11-22`  
**Canonical full research manuscript v0.43 blob SHA:** `a5080d5a33df310e985f72f84a0f7f3fac07932f` (**unchanged after V36**)

## 1. V36 generated outputs

| Artifact | Source | Editable Word (committed) | Measured automated QA |
|---|---|---|---|
| Research article | [V36 v0.2 source](submissions/results-in-engineering/RINENG_MANUSCRIPT_V36_v0.2_2026-11-23.md) | [Manuscript DOCX](exports/RINENG_V36_Manuscript_v0.2_2026-11-23.docx) | 259,629 bytes; 8 PDF-rendered pages; 3 native tables; 1 embedded scientific figure; 98 paragraphs |
| Concise Supplementary File S1 | [V36 S1 source](submissions/results-in-engineering/RINENG_SUPPLEMENT_V36_S1_v0.1_2026-11-23.md) | [Supplement DOCX](exports/RINENG_V36_Supplement_v0.1_2026-11-23.docx) | 2,476,784 bytes; 8 PDF-rendered pages; 2 native tables; 10 embedded paired sensitivity maps; 50 paragraphs |
| Candidate journal highlights | [Five highlights](submissions/results-in-engineering/RINENG_HIGHLIGHTS_V36_v0.1_2026-11-23.md) | [Highlights DOCX](exports/RINENG_V36_Highlights_v0.1_2026-11-23.docx) | 10,764 bytes; 5 complete bullet points, 61–72 characters each; no internal commentary |
| Draft cover letter | [Draft letter](submissions/results-in-engineering/RINENG_COVER_LETTER_DRAFT_2026-11-23.md) | Not final or sent | Author signoff and specific journal requirements outstanding |
| Separate title-page metadata | [Candidate title page](submissions/results-in-engineering/RINENG_V36_TITLE_PAGE_AUTHOR_METADATA_2026-11-23.md) | Author input required | ORCID/CRediT/author roster/funding ethics and affiliation confirmation pending |
| Release criteria | [Author/ethics gates](submissions/results-in-engineering/V36_AUTHOR_APPROVAL_AND_ETHICS_GATES_2026-11-23.md) | — | Explicit unanswered questions maintained |

The article has approximately **3,937 whitespace-delimited words including bibliography and declaration text**, a **237-word abstract**, **six keywords**, **17 selected references**, three results tables and one V34-B data-derived spatial agreement figure. A read-only editorial citation pass confirmed all 17 selected sources have corresponding in-text mentions (counting 2025a/b and 2026a/b Al-Tayar works separately).

The supplement intentionally **does not reproduce the full 34-page historical research dossier**. It retains all ten frozen paired figures, per-target rho/tau/overlap rows, the 17-class source-validation count table, and concise methods/provenance/missing-data details. The complete older dossier is preserved at `MANUSCRIPT_FULL_RESEARCH_DOSSIER_v0.42_2026-11-22.md` and the research master v0.43.

## 2. Numerical/editorial integrity

- Study outcome remains **image/object-level** only: 459 original-source validation images; 3,471 GT objects; 3,297 TP, 806 FP and 174 FN; micro precision 0.8036, recall 0.9499, F1 0.8706. M1 and M2 results are presented as metadata-based sensitivity cohorts, **not acquisition-independent test sets**.
- Target-matched perturbation analysis uses **ten selected targets from eight development-exposed images**. 8×8 grid used 1,068 model-call ledger records; 4×4 follow-up used 496 calls; the latter has 39/40 valid AUCs (one null ambiguous deletion).
- One seeded-random order, not repeated random baselines: the archived 8×8 saliency ordering is favorable in **8/10 deletion** and **9/10 insertion** distinct targets. This corrects the old manuscript abstract's contradictory sentence; the original numeric data did **not** change.
- Six target IDs overlap A5 and A6; their differing arm means reflect selection composition and cannot establish policy superiority.
- The ten exact target maps have mean Spearman rho **0.5416**, Kendall tau-b **0.4239**, top-four overlap **65%**, including one zero-overlap target. None is external ground-truth saliency.
- No worker compliance endpoint, verified human review, independent field generalization, measured detector latency or energy saving is claimed.
- No new inference, model retraining, source image alteration, label/split mutation, Test access, original model change or numerical record alteration took place in V36.

## 3. Automated QA evidence

The final successful workflow was [GitHub Actions run **45074736436**](https://github.com/EZZALDEEN049/Y-PPE-Detection-RFDETR/actions/runs/45074736436) with [artifact **14774702903**](https://github.com/EZZALDEEN049/Y-PPE-Detection-RFDETR/actions/runs/45074736436/artifacts/14774702903) (DOCX copies, both PDF renders, first/middle/last previews). Final run checked:
- DOCX ZIP archive integrity, nontrivial file size, **3/2 native-table counts** and **1/10 embedded-image counts** for article and supplement;
- Article essential numeric markers, keyword/figure counts, declaration placement before References, ten matched supplementary map captions/figures, five highlights ≤85 characters;
- Successful LibreOffice conversion of both editable Word files into **8- and 8-page PDFs**, plus PDF text smoke checks and previews;
- Safe preservation of the generated DOCX files on the **research branch**, with a three-attempt fetch/reset/copy/commit method avoiding binary Git rebase conflicts.

**Engineering incident and resolution:** initial Word/PDF QA passed; an extra concurrent run failed *only* on binary `.docx` rebase/merge conflicts while archiving. The V36 GitHub Actions workflow was subsequently changed to serialize builds and reapply freshly generated binary outputs over the latest branch before commit; the final run **45074736436 passed every step**, including the archive, and supersedes the failed run. Previous failed/successful jobs remain in the GitHub Actions history for transparent audit.

**Visual QA limit:** full-page PDFs and preview PNGs were rendered automatically. Manual inspection of every individual journal-draft page, images, tables and line breaks is **not independently documented as completed**. Do not mark final human visual approval as done.

## 4. Publisher policy and remaining submission blockers

Official current Elsevier policies used:
1. [Elsevier Editorial Manager manuscript/file requirements](https://www.elsevier.support/publishing/answer/how-do-i-prepare-my-files-for-submission-in-editorial-manager): journal-specific Guide for Authors takes priority over generic guidance.
2. [Elsevier generative AI policies (June 2026)](https://www.elsevier.com/about/policies-and-standards/generative-ai-policies-for-journals): substantive AI-assisted restructuring/writing must be transparently disclosed immediately before references, and the human authors must review/edit and take full responsibility. V36 includes a proposed declaration and an **unresolved author-confirmation placeholder**, not a signed declaration.
3. [Elsevier highlights](https://www.elsevier.com/en-in/researcher/author/tools-and-resources/highlights): three to five highlights, maximum 85 characters, supplied as a Word file; v36 complies with the generic guidance.
4. [Actual journal Guide for Authors](https://www.sciencedirect.com/journal/results-in-engineering/publish/guide-for-authors): **HTTP 403 Forbidden** to automated lookup in this pass. Therefore article type, peer-review anonymity model, exact keyword/abstract limits, figure submission format, title page, article length and final references **remain unverified for this particular journal**.

Author/institution actions still required:
- Provide the **real** ethics approval/exemption determination (if needed) and photographic worker-image consent, privacy and image-sharing legal basis; ownership/field capture alone is not blanket publication consent.
- Confirm authorship/order/affiliations/ORCIDs, real CRediT contributions, funding, conflicts of interest and all-author approvals.
- Review/authorize precise data and code public-access/permissions, including any source identifiers and preprints; secure an immutable numeric/code release if permitted.
- Verify full IEEE author metadata for two 2026 eSmarTA references; resolve originality overlap against prior 2025–2026 PPE/RF-DETR/XAI work.
- Approve AI-assistance declaration, final English/article contents and 16 PDF-rendered pages after **complete human visual review**.
- Confirm the live journal Guide for Authors and conditional Yemen geographic APC-waiver eligibility after full institutional author roster is final.
- Explicitly confirm no concurrent submission. **No actual manuscript upload or publication payment has been made.**

**Conclusion:** V36 journal-targeted *editorial construction and automated document QA* are complete. Full publication release is blocked by factual author confirmations, journal-specific live-guide compliance, and final human review; it is not blocked by any need to rerun the frozen experiments.
