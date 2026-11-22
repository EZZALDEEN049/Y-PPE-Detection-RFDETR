# Results in Engineering — SEER-PPE submission readiness tracker

**Date:** 23 November 2026  
**Journal selection:** **FINAL** — Results in Engineering, Elsevier  
**Submission action:** **NOT STARTED; NO FILES SENT TO PUBLISHER**  
**Current editorial artifact:** [V36 manuscript v0.2](RINENG_MANUSCRIPT_V36_v0.2_2026-11-23.md); original v0.1 retained as history  
**Source of truth for measurements:** [research master v0.43](../../MANUSCRIPT_MASTER.md), its V26–V35 frozen records and the separate v0.43 supplement  
**V36 editorial audit:** main v0.2 approximately 3,867 whitespace-delimited words including declarations/references; 3 compact tables; 1 main figure; 17 selected references; abstract 237 words. Ten-map [supplement S1](RINENG_SUPPLEMENT_V36_S1_v0.1_2026-11-23.md) and five [highlights](RINENG_HIGHLIGHTS_V36_v0.1_2026-11-23.md) are prepared. Official RINENG-specific length/figure requirements **not independently verified**.

## A. Progress by workstream

| Workstream | Status | Evidence / next gate |
|---|---|---|
| Final journal selection | **DONE** | [Locked target decision](../../JOURNAL_TARGET_FINAL_DECISION_2026-11-23.md) |
| Official publisher policy check | **DONE IN PART** | Elsevier general author/file guidelines and full-OA APC/waiver policy verified; RINENG-specific author guide direct access blocked |
| Main research article rewrite | **V36 v0.2 CREATED** | Main paper narrowed to object-level validation and perturbation/grid-resolution robustness; abstract 237 words; no internal production note |
| Numerical consistency of selected results | **TEXT CHECK COMPLETE; FULL INDEPENDENT EDITORIAL QA OPEN** | M0/M1/M2 counts and F1, selected-target AUCs, 4×4 null count and spatial rank numbers matched source transcription; audit scripts are separately archived |
| Main article figures | **SOURCE LINKED** | Canonical V34-B spatial agreement summary referenced from original research figure folder; final publishing-resolution and caption review pending |
| Supplementary | **V36 SHORT JOURNAL SUPPLEMENT CREATED** | New two-table supplement with ten paired-map figures and clear interpretation limits; preserved original v0.43 dossier remains in archive |
| Journal-specific instructions | **OPEN** | Check real RINENG Guide for Authors: abstract length, highlights, keywords, article class, lines, image requirements, title-page/peer review masking and data policy |
| Research image ethics and privacy | **AUTHOR BLOCKER** | No documented ethics approval/exemption, rights or consent/privacy authority has been validated; cannot fabricate |
| Funding | **AUTHOR BLOCKER** | Author to truthfully confirm source(s) and grant IDs, or none |
| Competing interests | **AUTHOR BLOCKER** | Author to declare and use publisher form as necessary |
| Author list/affiliations and CRediT roles | **AUTHOR BLOCKER** | Verify corresponding author, coauthor order, affiliations, contributions, ORCID and all-author sign-off |
| Data/software public availability and permissions | **AUTHOR BLOCKER** | Repo numeric evidence/derived plots are not equivalent to permission to publish worker photographs; verify archive accessibility, versions and allowed disclosures |
| Prior literature / self-overlap | **EDITORIAL QA OPEN** | Verify final IEEE metadata for two eSmarTA 2026 papers; clearly separate 2025–26 previous Y-PPE RF-DETR/X-RF-DETR findings |
| AI assistance disclosure | **V36 MANUSCRIPT SECTION INSERTED; AUTHOR CONFIRMATION OPEN** | Section immediately before References follows Elsevier June 2026 policy; author must inspect/edit/approve actual statement |
| APC exemption | **CONDITIONAL** | Elsevier Research4Life 100% waiver only if all final author institutions qualify Group A. Automated in post-acceptance publisher workflow. No invoice/acceptance exists |
| Cover letter | **DRAFT EXISTS** | [Draft RINENG cover letter](RINENG_COVER_LETTER_DRAFT_2026-11-23.md), requires author affirmation |
| Final Word/PDF QA | **V36 AUTOMATED QA PASS** | [Final successful V36 run 45074736436](https://github.com/EZZALDEEN049/Y-PPE-Detection-RFDETR/actions/runs/45074736436) archived three DOCX files; 8-page main PDF + 8-page supplement PDF; 1+10 embedded figures; [detailed QA](../../V36_RESULTS_IN_ENGINEERING_SUBMISSION_PREPARATION_REPORT_2026-11-23.md). Human page-by-page visual inspection still open |
| Actual Elsevier submission | **NOT STARTED** | Must not be done absent author-approved complete package |

## B. V36 audit additions

- General Elsevier journal policy was verified on 23 Nov 2026; its own Results in Engineering Guide for Authors returned HTTP 403, so exact journal abstract/keywords/highlights/format rules remain a check and cannot be inferred from other Elsevier titles.
- The v0.2 abstract counts 237 words and now includes explicit numerical study boundaries. Elsevier's AI policy revised June 2026 requires a declaration immediately before references when generative AI materially assisted manuscript drafting; that declaration is in v0.2 but lacks mandatory final human-author validation.
- Candidate highlights file contains five bullets of 65–71 characters each, matching broad Elsevier highlights conventions, not claimed to be compulsory in this specific journal.
- The dedicated V36 Word/PDF workflow is separate from the archived v0.43 research handoff export and makes **zero model-inference calls**.

## C. Critical editorial integrity note

The old v0.43 abstract characterized one deterministic random ordering as frequently matching/exceeding saliency, but the archived 8×8 target-level record reports **saliency favorable against that one random ordering** in **8/10 deletion unique targets** (one tie, one worse) and **9/10 insertion unique targets**. The draft corrects this *wording inconsistency*, while preserving the correct limitations: one random permutation is insufficient to prove comparative robustness; A5 and A6 have six shared target detections and cannot identify the winning selection policy; all selected XAI targets are development-exposed.

**Do not publish both contradictory assertions.** The original numeric records remain unchanged and must be the arbitration authority.

## D. Draft candidate Elsevier highlights (not asserted mandatory for RINENG until guide confirmation)

- Frozen RF-DETR PPE detections evaluated on 459 source-validation images.
- Target-matched occlusion responses compared at 8×8 and 4×4 grids.
- Spatial sensitivity rankings agree only moderately across resolutions.
- One of ten paired targets shares no top-four sensitivity regions.
- A5/A6 target overlap prevents a defensible selection-policy winner.

## E. Required author confirmations — remain unanswered

1. **People photographed:** confirm privacy/consent and ethical/organizational authorization as required, including whether any workers are identifiable and may appear in shared paper/supplements. No statements of committee approval or waiver should be inserted without an actual basis.
2. **Authorship:** finalize author/coauthor list, order, institutional locations, ORCID and specific CRediT roles. This also determines Elsevier waiver.
3. **Funding/competing interests:** actual answers, not defaults.
4. **Data access:** which image pixels, labels, code and numeric results may be publicly shared and which are restricted, and the access/repository terms.
5. **Previous publications:** final IEEE author lists/ordering and all related overlap disclosures; approve re-used datasets and explanation of distinct novelty.
6. **Publisher-facing statements:** human approve all content, English, image permissions, AI declaration, no concurrent submission, and cover letter.

## F. Verified authoritative submission-policy sources

- Elsevier prep checklist, journal-specific guide overrides generic rules: https://www.elsevier.support/publishing/answer/how-do-i-prepare-my-files-for-submission-in-editorial-manager
- Elsevier current submission and publication responsibilities: https://www.elsevier.com/en-gb/researcher/author/policies-and-guidelines
- Elsevier automated post-acceptance Research4Life all-Group-A full waiver: https://www.elsevier.com/en-gb/researcher/author/open-access/choice
- Official journal landing page (the journal-specific Guide for Authors should be opened by the submitting author at preparation): https://www.sciencedirect.com/journal/results-in-engineering

**Current decision:** journal selected and journal-focused editorial conversion begun. Submission blocked only by publication QA and factual author/journal requirements, not by a need to repeat already completed experiments.
