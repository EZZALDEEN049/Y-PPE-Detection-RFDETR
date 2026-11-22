# V37 — Results in Engineering: academic sign-off and journal-guide compliance

**Audit date:** 23 November 2026  
**Journal decision:** Results in Engineering (Elsevier) — approved target, **not yet submitted**.  
**Source branch:** `research/v30-progressive-xai-2026-11-22`; baseline V36 head `09b120071e758f3cf862702c326e97cab9995aea`.  
**Research integrity:** Original RF-DETR checkpoint, dataset, annotations, splits, all V26–V35 numerical ledgers and protected Test unchanged. **No new inference** in V37.  
**V37 outcome:** **DOCUMENT PACKAGE TECHNICALLY PREPARED; FORMAL AUTHOR/JOURNAL RELEASE GATE = HOLD / NOT APPROVED TO SUBMIT.**

## 1. Evidence hierarchy and limitations

1. **Journal-specific current instructions:** https://www.sciencedirect.com/journal/results-in-engineering/publish/guide-for-authors — automated fetch returned 403. Exact RINENG article-type, word/abstract, anonymization, separate-figure and citation requirements **cannot be certified from this page**. Corresponding author must confirm the live page and currently displayed Editorial Manager attachment types.
2. **Publisher-wide verified guidance:** https://www.elsevier.support/publishing/answer/how-do-i-prepare-my-files-for-submission-in-editorial-manager (journal rules override generic); https://www.elsevier.support/publishing/answer/how-do-i-include-highlights-with-my-manuscript (3–5 highlights, ≤85 characters each, separate editable file); https://www.elsevier.com/about/policies-and-standards/generative-ai-policies-for-journals (June 2026 disclosure/author accountability); https://www.elsevier.com/subject/next/guide-for-authors (generic layout, abstract, keywords and figures).
3. **RINENG-specific historical author-supplied evidence:** October 2026 screenshot archived outside this branch of the *Results in Engineering* Editorial Manager Attach Files screen lists **Declaration of Interests Statement, Highlights, Manuscript, and Title Page (Editable version)**, with a visible CRediT roles-file instruction. This is relevant evidence of **that portal configuration on that date**, *not* proof that the live 23-Nov configuration remains unchanged or that the present SEER-PPE paper was previously submitted.
4. **Current project version/evidence:** `V36_RESULTS_IN_ENGINEERING_SUBMISSION_PREPARATION_REPORT_2026-11-23.md`; `RINENG_MANUSCRIPT_V36_v0.2_2026-11-23.md`; `RINENG_SUPPLEMENT_V36_S1_v0.1_2026-11-23.md`; `RINENG_HIGHLIGHTS_V36_v0.1_2026-11-23.md`. Verified V36 CI: https://github.com/EZZALDEEN049/Y-PPE-Detection-RFDETR/actions/runs/45074736436 (completed / success, as checked in V37). Automated rendering and PDF text checks **do not equal author page-by-page visual approval**.

## 2. Item-by-item compliance matrix

| Requirement | V37 audit result | Status / action |
|---|---|---|
| Correct journal and non-overstated article scope | Results in Engineering selected; original engineering evaluation of perturbation sensitivity, not a new detector or validated occupational compliance intervention | **PASS scope positioning, subject to editorial decision** |
| Manuscript file | V36 v0.2 DOCX: 8 rendered pages; 3 native tables; 1 embedded data-derived figure; editorial draft approx. 3.9k words including refs/declarations | **TECHNICAL PASS; journal-specific format unverified** |
| Abstract | 237 words; states actual methods/results and limitations | **PASS generic concision; live journal limit unverified** |
| Keywords | Six keywords (generic Elsevier guideline recommends at most six) | **PASS generic; live journal-specific rule unverified** |
| Highlights | Five bullets, each <85 characters; editable separate DOCX archived | **PASS publisher generic; live journal attachment check pending** |
| Title page | Candidate author/title metadata exists as Markdown but no **signed/verified editable separate Title Page DOCX** | **OPEN — author roster, ORCIDs, institutions; produce edited title page** |
| Separate declaration of interests | Placeholder in manuscript, no truthful signed statement or journal-generated declaration file | **BLOCKER — author must disclose** |
| CRediT contribution file | Roles are explicitly unconfirmed, no verified role-by-author file | **BLOCKER — all authors approve** |
| Funding / sponsor role | Placeholder, no funding/no-funding confirmation | **BLOCKER — author** |
| Worker imagery ethics/privacy/permission | No verified documented committee determination where required or identifiable-worker image-sharing basis | **BLOCKER — author/institution** |
| Data and code statements | Public numeric/code repo exists; immutable release, raw-image rights and exact allowed access not finalized | **BLOCKER — author data-rights decision; stable revision link** |
| AI-use disclosure | Appropriate section before References, but contains author-confirmation placeholder; Elsevier demands real reviewed statement | **BLOCKER — author validates disclosure and manuscript** |
| References / originality | 17 cited sources; four prior author-programme publications distinguished; V36 citation mention audit passed; final 2026 IEEE contributor metadata and close self-overlap still require human source verification | **EDITORIAL HOLD** |
| Figure and supplement | One main summary figure and ten paired maps in V36 eight-page supplement; native editable files and automated QA pass | **TECHNICAL PASS; human full visual + permissions + journal separate-artwork specifications open** |
| Peer-review anonymity and title-page separation | Journal-specific guide unavailable; the **main manuscript contains author name/affiliation/email**; separate title-page metadata also exists | **CONDITIONAL BLOCKER if double-anonymized review; do not silently choose model** |
| Line numbering, page layout, artwork dpi/file types | DOCX/PDF rendered; official RINENG-specific setting unknown | **OPEN** |
| Cover letter | V36 draft accurately notes limited scope and related publications, but contains unsent author affirmation prompt | **DRAFT ONLY — author release** |
| Submission-exclusive status | No confirmed no-simultaneous-submission signoff for this exact SEER-PPE manuscript | **BLOCKER — author** |
| RINENG Editorial Manager upload | No manuscript uploaded in V36/V37; paper remains unsent | **NOT STARTED** |

**QA reconciliation note:** The V36 report states approx. 3,937 whitespace-delimited total words; the readiness tracker cites approx. 3,867. This minor internal discrepancy requires **one defined word-count script/source and exact reporting**; neither count should be promoted as an authoritative live-portal requirement. The journal draft's method/claims are more important than choosing an unsupported count.

## 3. Scientific integrity retained and verified against V36

- M0: 459 original-source Valid images, 3,471 current author GT objects, TP 3,297 / FP 806 / FN 174; precision 0.8036, recall 0.9499, micro-F1 0.8706, exact-class IoU ≥0.50.
- M1/M2: 448 / 367 metadata-risk filtered source sets; F1 0.8701 / 0.8682; **not independent site cohorts**.
- Ten selected target detections from eight development-exposed images, not ten independent sites; 1,068 recorded 8×8 calls and 496 4×4 calls, with 39/40 valid 4×4 AUCs and one correctly null ambiguous deletion.
- Mean aligned spatial rank correlations ρ=0.5416 and τ-b=0.4239; top-four overlap 65%; one zero-overlap target. These are **spatial response-pattern agreement**, not verified explanation truth.
- One seeded random order only; A5/A6 share six targets; **no causal attribution, policy winner, verified compliance, human intervention impact, independent generalization, measured model latency or energy saving** is asserted.
- V37 **does not revise the experimental numbers, targets, images or model**. This audit checks manuscript/ledger consistency reported by V36, not independent replay of all source inferences.

## 4. Reviewer-risk assessment and disposition

**High priority — block submission:** (i) authentic ethics/privacy/rights decision for human imagery and planned public figures; (ii) correct final authorship/CRediT/funding/COI/AI declarations; (iii) explicit final human approval of manuscript/figures and disclosure of prior work; (iv) journal-specific current guide and actual attachment types.

**Medium priority — solve before release:** identify peer-review model and prepare anonymized main file only if required; confirm artwork export settings and editable separate title page; verify author-programme 2026 IEEE metadata and avoid repetitive publication; pin public code/numeric evidence to immutable commit or deposit if licenses permit; visually review all 16 rendered pages.

**Do not present as a problem solved by formatting:** observed dataset exposure/source-family overlap and the tiny selected target cohort restrict scientific generalization. Neither author metadata nor manuscript styling can make the evidence stronger than it is.

## 5. Decision — V37 sign-off gate

- **Editorial structure/automated QA:** PASS *at the verified V36 artifact and workflow version*.
- **Academic claims bounded to observed evidence:** PASS *for scope/wording review only*, subject to final author accountability.
- **Publisher-current-guide full compliance:** NOT VERIFIED (403).
- **Ethics, publication permission and author declarations:** NOT APPROVED / NEED HUMAN DOCUMENTATION.
- **Final visual page-by-page signoff:** NOT DOCUMENTED.
- **Authorization to press Submit:** **NO-GO** until every above critical gate is evidenced and the author explicitly approves the same frozen files.

**No journal submission, ethical approval, consent, authorship signoff, funding declaration or fee-waiver grant is represented as completed by V37.**

## 6. Linked working records

- [V37 upload manifest](V37_RINENG_UPLOAD_MANIFEST_2026-11-23.md).
- [V37 truthful declaration worksheet](V37_RINENG_AUTHOR_DECLARATION_WORKSHEET_2026-11-23.md).
- [V36 article source](RINENG_MANUSCRIPT_V36_v0.2_2026-11-23.md); [V36 supplementary](RINENG_SUPPLEMENT_V36_S1_v0.1_2026-11-23.md); [V36 highlights](RINENG_HIGHLIGHTS_V36_v0.1_2026-11-23.md).
- [V36 complete QA report](../../V36_RESULTS_IN_ENGINEERING_SUBMISSION_PREPARATION_REPORT_2026-11-23.md).

**V37 is an editorial, compliance and release-control audit. It neither starts a new empirical evaluation nor supersedes experimental provenance.**
