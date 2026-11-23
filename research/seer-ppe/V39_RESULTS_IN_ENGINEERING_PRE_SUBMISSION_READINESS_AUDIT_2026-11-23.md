# V39 — Results in Engineering pre-submission technical, bibliography and author-signoff audit

**Audit date:** 23 November 2026 (Asia/Aden).  
**Article:** *Cross-Resolution Consistency of Target-Matched Perturbation Sensitivity Maps for Personal Protective Equipment Detection*.  
**Editorial status:** **HOLD — not authorized for journal submission**. Research and derived manuscript files are ready for author review, but personal/institutional declarations are neither signed nor independently verifiable from research records.

## Executive decision

**V39 technical checks passed** for existing results, Figures 1–3, five editable manuscript tables, supplementary 48-target data and figure export. An improved V39 author-signoff manuscript draft has been prepared from V38-C while preserving V36, V37, V38-C and all original experiment files. The remaining **author-only gates** are real; they must not be bypassed with guessed declarations.

## 1. Exact sources examined and journal-guide limitation

- V38-C original editable manuscript: 13-page A4 Word/PDF, 5 tables, 3 embedded figures, six keywords and a 219-word abstract.
- S2 numerical supplement: 5-page A4 landscape Word/PDF with all 48 targets, 11 categories, the three missing-map cases and 22 randomized direction comparisons; 5 tables.
- V38-C 2026-11-23 separated figure files: Figure 2 (3784×1564 pixels; nominal 300 dpi) and Figure 3 (3784×1474; nominal 300 dpi); historical Figure 1 and S1–S10 unchanged.
- PDF geometric audit on all 13+5 pages found **zero text blocks extending beyond page bounds** and no blank text pages. This is not a universal guarantee against all typographic defects.
- Current Research Plan/Roboflow QA, immutable V38-B numerical and call ledgers: 24/24 original Valid images, 48/48 targets, 4,984 attempted/succeeded requests, 45 estimable maps, 3 non-estimable maps, 264 valid curves, no Test usage or training.
- `مطابقة دليل المجلة.txt` supplied in the project was inspected; **it is a copy of an earlier assistant status response, NOT the journal's official author guide**. We therefore did NOT certify journal-specific compliance from this file.
- Attempted direct retrieval of the specific Results in Engineering Guide for Authors on ScienceDirect/Elsevier was rejected with **HTTP 403**, so exact journal-only mandatory items remain **VERIFY IN EDITORIAL MANAGER / OFFICIAL SITE** (article type, anonymization, Highlights status, abstract cap, optional graphical abstract, separate title page, mandatory forms, artwork upload types, reference style and any limits). Elsevier general preparation support is accessible: https://www.elsevier.support/publishing/answer/how-do-i-prepare-my-files-for-submission-in-editorial-manager and https://www.elsevier.com/subject/next/guide-for-authors. **Do not mistake general Elsevier guidelines or third-party journal summaries for a verified journal-specific guide.**

## 2. Scientific and numerical consistency — PASS

| Criterion | Verified value |
|:--|:--|
| Original-source validation set | 459 images, 3,471 current boxes |
| Detector raw class-exact TP / FP / FN | 3,297 / 806 / 174 |
| Internal micro-F1 | 0.8706 |
| Historical V34A map cohort | 10 targets / 8 images, 8×8 and 4×4; mean rho 0.5416, top-four overlap 65% |
| Frozen V38-B extension | 24 images / 48 exact targets / 11 PPE categories |
| 8×8↔4×4 estimable results | 45 / 48; 3 ambiguous cases kept null |
| V38-B mean Spearman rho | 0.6490 target-weighted; 0.6508 image-balanced |
| V38-B mean Kendall tau-b | 0.5197 |
| V38-B top-four overlap | 66.67% |
| Blur vs gray paired operator rho | 0.4811 vs 0.6943, n=14, mean paired delta −0.2132 |
| Repeated-random AUC | 264 available curves for 11 targets; 1 of original 12 blocked, no substitutions |
| Original hosted calls | 4,984/4,984, under hard cap 6,000 |
| External site-independence/worker compliance | **NOT demonstrated** |

The 10-target and 48-target cohorts differ in target selection and wire encoding and must not be statistically pooled as if a paired replication. No new numerical model experiment was initiated for V39.

## 3. Reference review — 18 entries, 14 DOI links + 4 other scholarly URLs

- The V38-C reference list has **18 distinct entries**, **14 DOI hyperlinks and 4 scholarly/arXiv/proceedings URLs**. Every reference's lead author name was matched to a text citation in the manuscript by a static check; this **does not** itself prove bibliographic accuracy.
- Independently verified primary/strong sources include the 2024 *Results in Engineering* paper by Alain Andrés, Aitor Martínez-Seras, Ibai Laña and Javier Del Ser, *vol. 24*, article **103498** (https://doi.org/10.1016/j.rineng.2024.103498). This comparator discusses D-MFPP; the manuscript correctly discloses **no direct D-MFPP hosted experiment**.
- Other DOI/title matches checked against publisher/proceedings sources: Fong & Vedaldi (https://doi.org/10.1109/ICCV.2017.371); Kendall (https://doi.org/10.1093/biomet/30.1-2.81); Spearman (https://doi.org/10.2307/1412159); Bouguessa et al. (https://doi.org/10.1016/j.engappai.2026.115725); Yi et al. (https://doi.org/10.1016/j.aei.2026.104612); Di Renzo et al. (https://doi.org/10.3390/jimaging12050195); Barlybayev et al. (https://doi.org/10.3390/computers15060388); Vaghani (https://doi.org/10.3389/fbuil.2026.1976288); Paes et al. (https://doi.org/10.52202/079017-1765). The RF-DETR architecture reference is available at ICLR 2026: https://proceedings.iclr.cc/paper_files/paper/2026/hash/5bed8703db85ab27dc32f6a42f8fbdb6-Abstract-Conference.html .
- Group-related IEEE 2025/2026 paper DOIs had supporting records, including DASA 2025 article 11499131 and eSmarTA 2026 articles 11652079 and 11652190. **Before submission**, compare each conference paper's exact author order, proceedings title and page metadata with the publisher's authoritative bibliographic record. Likewise verify the four non-DOI proceedings URLs and the exact Hooker NeurIPS pagination (bibliographic sources differ by version).
- New V39 text describes AI-assisted reference checking and program-code preparation in Methods and contains one detailed pre-References AI declaration. **Human verification of the final bibliography and each citation is still required.**

## 4. File compliance — what is actually verified

| Submission artifact | Verified stage | Further requirement |
|:--|:--|:--|
| V39 manuscript editable DOCX/PDF proof | Draft author-signoff regeneration underway; original V38-C export passed PDF render and content checks | Must verify final V39 page layout and author details |
| Figure 1 and Figure 2/3 | Standalone artwork and embedded figures present | Final figure physical-size/readability and journal formats via specific guide |
| Supplement S1 and S2 | Historical S1 archival; new S2 audited including 48 target rows | Ensure both are the actually intended uploads; supplementary disclosure check |
| Five Highlights bullets | Word document, all **<=85 characters including spaces**, syntactically appropriate | Journal-specific optional/mandatory status not independently verified |
| Cover letter | Editable draft, scientific summary updated | Do not send without author approvals and originality/ethics confirmation |
| Title page | Previously drafted with one author | **Final roster/affiliation/address/order must be confirmed** |
| Declarations | V39 unsigned worksheet provides truthful alternative language | **Not established / not signed** |

## 5. Author-only BLOCKERS (stop submission until resolved)

1. **Full author roster and author order:** The manuscript currently prints *Ezzaldeen Al-Tayar* as a single author and a Taiz University affiliation. These are prior-draft text, not proof of the final agreed roster or full postal address. Confirm exact names, ORCID if used, institutional full spelling, all co-author approvals and corresponding email.
2. **Funding and in-kind resources:** No trustworthy statement of grant/no grant exists. Confirm whether to use the accurate no-specific-grant sentence or list actual grants and sponsor role. Research Plan compute credits do not prove a grant, but any material support/affiliation should be acknowledged appropriately.
3. **Competing interests:** All authors must truthfully choose no-interest vs specific disclosures; no prefilled denial can be issued by the assistant. Confirm whether an official declaration form is needed.
4. **Ethics and person-image publication rights:** The researcher has already stated they captured the field photographs personally during engineering work; **we do not reopen image photographer-provenance tasks**. Separately, whether some figures/photos or reconstructible links reveal recognizable workers and whether institutional approval or a documented exemption and written publication permissions apply **must be resolved**. Elsevier's policy requires an appropriate ethics statement and written informed permission for identifiable persons where applicable: https://www.elsevier.com/en-gb/about/policies-and-standards/research-ethics . **Do not fabricate IRB clearance, a blanket exemption or worker consent.**
5. **Public research repository exposure:** https://github.com/EZZALDEEN049/Y-PPE-Detection-RFDETR is confirmed **public**, and its V38-B code/records contain source IDs and source-media URL construction. The author must check whether this renders original worker photographs publicly retrievable and whether that is lawfully permitted. Public access to derived numerical artifacts is not equivalent to permission to publish workers' likenesses or distribute raw photos. Never claim all original photos are private without a separate access audit.
6. **Originality and prior outputs:** The author must assess overlap/rights with the four cited related IEEE 2025/2026 research contributions, relevant abstracts and preprints, and confirm exclusive submission and all author approvals. A similarity tool score cannot substitute for this judgment.
7. **AI-use declaration:** Elsevier June 2026 policy requires a precise statement of material ChatGPT use for text, coding/visualization and literature support; authors must read, edit and approve the entire final manuscript. Source: https://www.elsevier.com/about/policies-and-standards/generative-ai-policies-for-journals . V39 corrects duplicate AI placeholder and adds methodology information but remains an author-signoff draft.
8. **Specific author guide and submission portal:** The exact Results in Engineering guide was not accessible programmatically; check within official portal, including required file designations, article type, data statement/declaration forms and any journal-specific artwork requirements. Submission was **not** performed.

## 6. Safe next step

Give the corresponding author the **unsigned V39 author certification worksheet** at `submissions/results-in-engineering/V39_AUTHOR_CERTIFICATION_AND_ETHICS_WORKSHEET_UNSIGNED_2026-11-23.md`. Do not request identity/photo provenance re-review, only final rights to publish identifiable people and privacy/ethics determination. Once certified, replace all pending placeholders, regenerate V39 manuscript/cover letter/Highlights/Title Page, and perform final full-page checks. Only then may the author separately authorize actual submission via the publisher portal.

**Internal audit verdict:** Scientific manuscript technically **READY FOR AUTHOR SIGNOFF**, not **READY FOR ACTUAL SUBMISSION**. No new model inference, no prior scientific result edits, and no journal submission.
