# V39-R3 — Publication-integrity release audit and Submission Clean Final gate

**Date:** 24 November 2026 (Asia/Aden)  
**Target journal:** *Results in Engineering* (Elsevier)  
**Current editorial baseline:** `RINENG_MANUSCRIPT_V39_R1_REVIEWED_DRAFT_2026-11-23.md` and companion revised S2; historical S1 is retained.  
**Status:** **SCIENCE LOCKED / TECHNICAL REVIEW PASS / SUBMISSION HOLD (UNSIGNED)**. This is not a publisher acceptance or an actual submission.

## 1. Completed in this R3 pass (no RF-DETR inference)

1. Read source-controlled V39-R1 manuscript and supplement plus the V39-R2 simulated referee decision.
2. Cross-checked main manuscript abstract: **233 whitespace-separated tokens** after Markdown emphasis removal, including its inline headings, excluding keywords; this is below the **250-word maximum** recorded from the *author-supplied* RINENG guide excerpt (V37-B). A distinct Word-export upload should be counted again after final author revision.
3. Checked the **five** V38-C highlights: lengths **69, 76, 70, 71, 73 characters** excluding Markdown list marks, all below the guide-excerpt limit of **85 characters**. The final Word-export Highlights file must be separately verified, since the currently archived DOCX is earlier V38-C.
4. Confirmed in the *repository listing* exactly **three main** figure PNG files (`Figure_1.png` to `Figure_3.png`) and **ten supplementary** figure PNG files (`Figure_S1.png` to `Figure_S10.png`). Presence does **not** verify pixels, identifiable faces, effective DPI, color profile, rights or the journal's artwork preflight.
5. Checked that the R1 manuscript explicitly separates the old ten-target experimental set from the 48-target/24-image V38-B extension, preserving 45/48 estimable rank comparisons, 14 paired gray–blur comparisons and all 17 historical class metrics in S2.
6. Retained the already simulated V39-R2 scientific editorial caveats rather than inventing approval: internal cohort, three undefined targets, method-dependent perturbations, no independent-source field validation and no person-specific safety-compliance ground truth.
7. Checked Elsevier's **June 2026** generative-AI policy and current research ethics/publishing ethics pages. **The full current RINENG-specific ScienceDirect Guide was not accessible in this pass (HTTP 403)**; the V37-B report records only the subset of guide requirements previously supplied by the researcher.
8. Produced a separate **unsigned author decision sheet** rather than altering or silently filling the R1 author's declaration placeholders.

## 2. Final factual authorization gates

| ID | Gate | R3 state | Only acceptable closure evidence |
|:--|:--|:--|:--|
| A1 | Full final author roster, order, corresponding author, correct institutional English name and postal address | **OPEN — AUTHOR** | Verified metadata and all eligible coauthor approvals |
| A2 | Ethics/human-image determination | **OPEN — AUTHOR / INSTITUTION** | Actual committee approval or documented institutional determination/exemption as applicable; do not infer IRB status |
| A3 | Workers' privacy, identifiable-image publication consent and relevant NGO/project rights | **OPEN — AUTHOR / RIGHTS HOLDER** | Fig-by-fig disclosure assessment and lawful documentation; original photography ownership alone does not establish public image release permission |
| A4 | Funding, grants and in-kind support including any relevant model-host credit | **OPEN — AUTHOR** | True funder/role statement or documented confirmation of no specific grant |
| A5 | Competing interests | **OPEN — ALL AUTHORS** | Accurate declared interests or truthful no-conflicts statement, with publisher form if required |
| A6 | CRediT authorship allocation | **OPEN — ALL AUTHORS** | Approved roles mapped to final author roster |
| A7 | Originality, all related publications and exclusive submission | **OPEN — ALL AUTHORS** | Explicit nonduplication, reused data/figures permissions, not under review elsewhere |
| A8 | Full AI assistance declaration and human responsibility | **OPEN — AUTHOR** | Author review/edit/confirmation of ChatGPT assistance; method-side code/plot use accurately disclosed |
| A9 | Public repository image/metadata rights, code license, release/permalink | **OPEN — AUTHOR / TECHNICAL** | Legal/privacy audit of exposed image IDs/links; immutable approved release/commit; avoid claiming weight redistribution |
| A10 | Final current guide, upload slots and art resolution/size | **OPEN — PORTAL** | Verify direct target-journal guide and actual system fields before upload |
| A11 | Final author proofing and submission authorization | **OPEN — ALL AUTHORS** | Read entire article/S1/S2/cover/figures and explicit instruction to submit |

**Integrity rule:** a draft clause may not be treated as a signed certification. If the site-rights or ethics determination cannot be established, restrict or revise proposed public images/links and obtain appropriate institutional/journal guidance; never invent consent or exemption. Do not automatically assume generic facial blurring is sufficient anonymization.

## 3. Science and version lock

- Detector unchanged: RF-DETR Small, 17 annotated categories.
- Internal source Validation: 459 images; 3,297 TP, 806 FP, 174 FN, micro-F1 0.870610 against current single-curator ground truth.
- V38-B experiment: 48 fixed target detections, 24 development-exposed images, 4,984 successful logged image-model requests; 45 estimable rho values, Spearman mean 0.6490, median 0.687270, Q1–Q3 0.514706–0.811765, 11/45 below 0.50.
- Matched gray versus blur: 14 valid targets from 8 images, paired blur-minus-gray median −0.176471; 264 valid AUC curves from 11 scorable targets. The randomized-order comparison is *within the same perturbation protocol*.
- Those results do not measure causal explanation validity, worker-specific compliance, independent field generalization or relative performance against D-MFPP. No new inference, retraining, data selection or result manipulation in R3.
- Source evidence: `V39_R1_SECONDARY_STATS_AND_V26_PER_CLASS_VALIDATED_2026-11-23.md`; R2 simulated review; R1 source manuscript and S2.

## 4. Exact versioned inputs and proposed release files

**Keep unchanged for all future operations until sign-off:**
- `RINENG_MANUSCRIPT_V39_R1_REVIEWED_DRAFT_2026-11-23.md`
- `RINENG_SUPPLEMENT_V39_R1_S2_REVISED_2026-11-23.md`
- `../../exports/RINENG_V39_R1_Manuscript_Review_Only_UNSIGNED.docx`
- `../../exports/RINENG_V39_R1_Supplement_S1_Review_Only.docx`
- `../../exports/RINENG_V39_R1_Supplement_S2_Review_Only.docx`
- `../../exports/RINENG_V39_R1_REVIEW_ONLY_NOT_SUBMITTED_PACKAGE_2026-11-23.zip`

**R3 additions:** this audit and `RINENG_V39_R3_AUTHOR_APPROVAL_DECISIONS_UNSIGNED_2026-11-24.md`; local editable author decision/proofing worksheet available independently.

**There is no file labelled `Submission Clean Final` as a valid submit-ready manuscript yet.** Create one only after gates A1–A11 are actually closed, clean internal instructions from publisher uploads, re-render/proof final Word and PDF, and assemble a fresh upload manifest by actual portal slots. The current ZIP is explicitly `REVIEW_ONLY_NOT_SUBMITTED`.

## 5. Policy provenance and bounded guide match

- User-supplied RINENG guide subset recorded in `V37_B_USER_PROVIDED_JOURNAL_GUIDE_CROSSWALK_2026-11-23.md`: title, ≤250-word abstract, 1–7 keywords, 3–5 highlights ≤85 characters, editable tables, separately provided figure artwork and complete title-page details. This is *not* a verified capture of the full current live author guide.
- Elsevier generative-AI journals policy (June 2026): https://www.elsevier.com/about/policies-and-standards/generative-ai-policies-for-journals
- Elsevier human research/identifiable images policy: https://www.elsevier.com/about/policies-and-standards/research-ethics
- Elsevier publishing ethics including support and competing interests: https://www.elsevier.com/about/policies-and-standards/publishing-ethics
- Journal-specific guide URL (presently access restricted to automated inspection): https://www.sciencedirect.com/journal/results-in-engineering/publish/guide-for-authors

**Release verdict 2026-11-24:** **HOLD FOR AUTHOR/INSTITUTION/PORTAL DECISIONS**. Does not negate successful V39-R1 technical QA; is not an editor's decision.
