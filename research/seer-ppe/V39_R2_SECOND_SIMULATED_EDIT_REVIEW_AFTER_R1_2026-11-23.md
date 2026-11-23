# V39-R2 — Second simulated editorial and peer-review round after V39-R1 changes

**Date:** 23 November 2026, Asia/Aden.  
**Paper:** *Cross-Resolution Consistency of Target-Matched Perturbation Sensitivity Maps for Personal Protective Equipment Detection*  
**Target:** *Results in Engineering*, Elsevier  
**Nature:** **Internal simulated review only**. This is not a journal editor's decision, actual peer-review report or forecast of acceptance odds.

## Evidence available to the second-round board

1. V39-R1 **new Markdown manuscript** `submissions/results-in-engineering/RINENG_MANUSCRIPT_V39_R1_REVIEWED_DRAFT_2026-11-23.md` includes 6 editable tables (five original numbered results tables and one prior-work scope matrix), three figures with **non-duplicated** captions, mathematical response-density definitions, new rank-distribution and leave-one-image-out sensitivity discussion, field-use caveat, and still-unsigned author declaration placeholders.
2. The revised `RINENG_SUPPLEMENT_V39_R1_S2_REVISED_2026-11-23.md` includes all 48 target outcomes, 11 category groups, three undecidable targets, 264 valid AUCs, 45-target rho median/IQR/range, image-level influence checks, and **all 17 V26 class-exact precision/recall/F1 entries**.
3. `V39_R1_SECONDARY_STATS_AND_V26_PER_CLASS_VALIDATED_2026-11-23.md` derives the additional data from two immutable sources: the archived V38-B 48-target per-target summary, and the archived original 459-image V26 `M0.per_class` file. No new hosted model inference.
4. **Technical reproducibility:** [GitHub Actions V39-R1 QA run 45094516733](https://github.com/EZZALDEEN049/Y-PPE-Detection-RFDETR/actions/runs/45094516733) returned `completed/success`. It generated new Word documents for the revised manuscript, historical Supplement S1 and revised S2; verified three embedded manuscript figures, 10 S1 figures and per-class S2 content; rendered PDFs; **checked that the beginning and final row of Table 4 were on the same PDF page**; checked unique figure captions; included original standalone Figure 1, Figures 2/3, Supplementary Figures S1–S10, cover letter, Highlights and existing provisional title page in a ZIP labeled **REVIEW ONLY / NOT SUBMITTED**.
5. Independent local Word/PDF render-and-inspect QA of the same V39-R1 scientific fixes confirmed 13 portrait manuscript pages, six landscape S2 pages, three unique figure caption paragraphs, no geometric text overflows and intact Table 4 on page 8 of the local proof. These proofs establish typographic stability, not formal journal-specific formatting acceptance.
6. The general Elsevier guide and its artwork checklist are reference points; **the exact journal-specific official Results in Engineering current portal guide remains unverified** and is still an author/editorial gate.

## Second-round scores — subjective 0–10, not probabilities

| Simulated review role | Round 1 | Round 2 | Technical judgment |
|:--|--:|--:|:--|
| Technical editorial office | 6.0 | **8.0** | Layout, Figure captions, Table 4, and full review attachment manifest corrected; declarations and publisher-specific guide still block submission |
| Associate editor / engineering novelty | 6.2 | **7.0** | Clearer difference from four related earlier studies and D-MFPP; still a bounded diagnosis, not new method validation |
| Reviewer 1 — XAI / object detection | 6.4 | **7.2** | Explicit signed-density formulas, circular AUC caveat and no unjustified causal/general method claims; stronger published XAI comparator not run |
| Reviewer 2 — experimental statistics | 6.3 | **7.7** | Median/IQR, 11/45 below 0.5, LOIO image sensitivity, matched operator LOIO and nulls; independent-site testing still absent |
| Reviewer 3 — occupational engineering | 6.0 | **7.0** | All 17 internal PPE class F1 values and a conditional human-inspection use case added; no person–PPE/field safety outcomes established |
| Publication integrity / ethics | 4.0 | **4.0** | Still unsigned author/funder/competing interest/AI originality statements and unpublished worker image disclosure-rights determination |
| Language, references and production | 7.0 | **8.1** | Captions repaired and S1/S2 inclusion verified, but each reference and final portal metadata require last human checks |

**No numeric increase is evidence of a higher journal acceptance probability.** The scores express only the relative completeness of this updated simulation.

## Reviewer comment closure matrix

| Item | Resolution in R1 | Status |
|:--|:--|:--|
| T2 Table 4 split across pages 7–8 | Move V38-B heading/table together and enforce non-splitting table rows; GitHub PDF QA checks first and last table line on same page | **CLOSED — verified in PDF** |
| T3 duplicate captions for Figures 1–3 | Single complete descriptive caption per image; GitHub Word test asserts one per figure | **CLOSED — verified** |
| T4 missing original Figure 1, original Supplement S1 and Figures S1–S10 from prior review ZIP | Generate separate historical S1 Word with 10 embedded images; include original standalone Figure 1, all supplement artwork | **CLOSED for review package**; upload classification requires journal-guide check |
| Editor novelty unclear | Six-row prior-publication/D-MFPP scope matrix; title and exact claimed novelty retained | **ADDRESSSED WITH LIMITATION**; source/text overlaps still require author certification |
| R1.1 AUC ranking/evaluation circularity | Revised wording states within-detector perturbation diagnostic rather than independent explanation faithfulness | **CLOSED as disclosure**; no new independent comparator |
| R1.2 coarse–fine spatial area logic unclear | Equations for signed drop and 4×4 direct versus sum of four fine 8×8 drops divided by exact coarse area | **CLOSED**; nonlinear spatial effects remain |
| R1.3 JPEG vs PNG cohorts | Keep historical V34 and V38-B results separate | **CLOSED as limitation** |
| R1.4 ambiguity accounting | Three missing targets remain explicitly null with original denominators; no post hoc substitute | **CLOSED** |
| R2 rank distribution and cluster influence | rho median 0.687270, IQR 0.514706–0.811765, range −0.017647–0.926471, 11/45 <0.5, image LOIO 0.640997–0.664868 | **CLOSED as descriptive sensitivity** |
| R2 operator paired robust interval | 14 matched across eight images, paired median blur-minus-gray −0.176471, image-LOIO paired mean −0.248039 to −0.178659 | **CLOSED as descriptive sensitivity** |
| R3 17-class PPE detection metrics | Exact archived 17-class TP/FP/FN, precision/recall/F1 appended to S2 | **CLOSED**; limited single-curator GT |
| R3 engineering interpretation | Conditional human-review recommendation with no unmeasured outcomes | **CLOSED as measured-boundary clarification** |
| T1 author/ethics declaration placeholders | Unsigned worksheet retained; no false statements of approval, consent, funding or absence of conflict | **OPEN / AUTHOR-ONLY** |
| T5 public image identifiers, personal-image disclosure and contractual publication rights | Risks identified; immutable numeric evidence not altered, no rights or anonymity invented | **OPEN / AUTHOR+INSTITUTION** |
| T6 exact current journal author guide and submission metadata | General Elsevier guidance checked but journal-specific portal rules unverified | **OPEN / JOURNAL-PORTAL CHECK** |
| Originality overlap with own 2025/2026 papers | Prior-work matrix added, but no signed detailed originality certification or text/figure license verification | **OPEN / AUTHOR-ONLY** |

## Remaining *scientific* weaknesses (not software bugs)

- The images were **development-exposed**, source-project-family independence not certified. The 24 images are not independent site samples. An internal image-cluster bootstrap/LOIO is no substitute for independent-source field validation.
- Target score changes are *perturbation responses* and may differ with the replacement operator. The methodology does not demonstrate true causal explanations or worker PPE compliance.
- The favorable AUC margins against ten randomized rankings are **same-model, same-perturbation-type controls**; they are not a head-to-head experiment with D-RISE/D-MFPP.
- The set of 45 estimable targets may suffer selection bias when three same-class target matches become ambiguous. Results are conditional on estimability.
- Class F1 results are against the **single-curator** original-source validation reference at the frozen threshold, not a second blinded annotator.
- The author must still certify novelty and distinguish exact experiments/datasets/figures reused in related earlier work. A published title alone does not fully settle publication overlap.

## Editorial decision of this simulated second round

**TECHNICAL FILE QUALITY:** PASS for reviewed Word/PDF/layout and complete *review-only* ZIP; this is **not** a journal-specific technical submission clearance.

**SCIENTIFIC REVIEW READINESS:** Improved and **plausible to send to external reviewers after author-only P0 gates**, with **Major Revision** still a reasonable possible outside outcome. Additional model inference is not a prerequisite for a *bounded descriptive XAI study*. A broader causal/algorithm-superiority claim would need new comparisons and independently sourced data.

**PUBLICATION/ETHICS AND FINAL SUBMISSION:** **HOLD**. Do **not** strip placeholders automatically or certify unproven informed consent, IRB exemption, no conflicts, no grant funding, author list approval, originality or lawful public photo links. No journal submission has been made.

## Exact available review artifacts in GitHub

- R1 manuscript source: `research/seer-ppe/submissions/results-in-engineering/RINENG_MANUSCRIPT_V39_R1_REVIEWED_DRAFT_2026-11-23.md`
- R1 S2 source: `research/seer-ppe/submissions/results-in-engineering/RINENG_SUPPLEMENT_V39_R1_S2_REVISED_2026-11-23.md`
- R1 Word manuscript: `research/seer-ppe/exports/RINENG_V39_R1_Manuscript_Review_Only_UNSIGNED.docx`
- Original historical S1 editable Word: `research/seer-ppe/exports/RINENG_V39_R1_Supplement_S1_Review_Only.docx`
- Updated S2 editable Word: `research/seer-ppe/exports/RINENG_V39_R1_Supplement_S2_Review_Only.docx`
- **Complete review-only ZIP:** `research/seer-ppe/exports/RINENG_V39_R1_REVIEW_ONLY_NOT_SUBMITTED_PACKAGE_2026-11-23.zip`
- CI result: https://github.com/EZZALDEEN049/Y-PPE-Detection-RFDETR/actions/runs/45094516733

### External/public standards checked, not substituted for the journal's guide

- Elsevier generic author guide: https://www.elsevier.com/en-gb/subject/next/guide-for-authors
- Elsevier artwork checklist: https://www.elsevier.com/about/policies-and-standards/author/artwork-and-media-instructions/artwork-formats-checklist
- Industrial object-detector XAI comparator: https://doi.org/10.1016/j.rineng.2024.103498
- DASA 2025 conceptual X-RF-DETR: https://ieeexplore.ieee.org/abstract/document/11498849

## Post-review technical patch: native mathematical typesetting (verified)

Subsequent full-document visual proof found that an initial Pandoc conversion had rendered the new response-density equations as literal TeX. The source was corrected to Pandoc-supported `$...# V39-R2 — Second simulated editorial and peer-review round after V39-R1 changes

**Date:** 23 November 2026, Asia/Aden.  
**Paper:** *Cross-Resolution Consistency of Target-Matched Perturbation Sensitivity Maps for Personal Protective Equipment Detection*  
**Target:** *Results in Engineering*, Elsevier  
**Nature:** **Internal simulated review only**. This is not a journal editor's decision, actual peer-review report or forecast of acceptance odds.

## Evidence available to the second-round board

1. V39-R1 **new Markdown manuscript** `submissions/results-in-engineering/RINENG_MANUSCRIPT_V39_R1_REVIEWED_DRAFT_2026-11-23.md` includes 6 editable tables (five original numbered results tables and one prior-work scope matrix), three figures with **non-duplicated** captions, mathematical response-density definitions, new rank-distribution and leave-one-image-out sensitivity discussion, field-use caveat, and still-unsigned author declaration placeholders.
2. The revised `RINENG_SUPPLEMENT_V39_R1_S2_REVISED_2026-11-23.md` includes all 48 target outcomes, 11 category groups, three undecidable targets, 264 valid AUCs, 45-target rho median/IQR/range, image-level influence checks, and **all 17 V26 class-exact precision/recall/F1 entries**.
3. `V39_R1_SECONDARY_STATS_AND_V26_PER_CLASS_VALIDATED_2026-11-23.md` derives the additional data from two immutable sources: the archived V38-B 48-target per-target summary, and the archived original 459-image V26 `M0.per_class` file. No new hosted model inference.
4. **Technical reproducibility:** [GitHub Actions V39-R1 QA run 45094516733](https://github.com/EZZALDEEN049/Y-PPE-Detection-RFDETR/actions/runs/45094516733) returned `completed/success`. It generated new Word documents for the revised manuscript, historical Supplement S1 and revised S2; verified three embedded manuscript figures, 10 S1 figures and per-class S2 content; rendered PDFs; **checked that the beginning and final row of Table 4 were on the same PDF page**; checked unique figure captions; included original standalone Figure 1, Figures 2/3, Supplementary Figures S1–S10, cover letter, Highlights and existing provisional title page in a ZIP labeled **REVIEW ONLY / NOT SUBMITTED**.
5. Independent local Word/PDF render-and-inspect QA of the same V39-R1 scientific fixes confirmed 13 portrait manuscript pages, six landscape S2 pages, three unique figure caption paragraphs, no geometric text overflows and intact Table 4 on page 8 of the local proof. These proofs establish typographic stability, not formal journal-specific formatting acceptance.
6. The general Elsevier guide and its artwork checklist are reference points; **the exact journal-specific official Results in Engineering current portal guide remains unverified** and is still an author/editorial gate.

## Second-round scores — subjective 0–10, not probabilities

| Simulated review role | Round 1 | Round 2 | Technical judgment |
|:--|--:|--:|:--|
| Technical editorial office | 6.0 | **8.0** | Layout, Figure captions, Table 4, and full review attachment manifest corrected; declarations and publisher-specific guide still block submission |
| Associate editor / engineering novelty | 6.2 | **7.0** | Clearer difference from four related earlier studies and D-MFPP; still a bounded diagnosis, not new method validation |
| Reviewer 1 — XAI / object detection | 6.4 | **7.2** | Explicit signed-density formulas, circular AUC caveat and no unjustified causal/general method claims; stronger published XAI comparator not run |
| Reviewer 2 — experimental statistics | 6.3 | **7.7** | Median/IQR, 11/45 below 0.5, LOIO image sensitivity, matched operator LOIO and nulls; independent-site testing still absent |
| Reviewer 3 — occupational engineering | 6.0 | **7.0** | All 17 internal PPE class F1 values and a conditional human-inspection use case added; no person–PPE/field safety outcomes established |
| Publication integrity / ethics | 4.0 | **4.0** | Still unsigned author/funder/competing interest/AI originality statements and unpublished worker image disclosure-rights determination |
| Language, references and production | 7.0 | **8.1** | Captions repaired and S1/S2 inclusion verified, but each reference and final portal metadata require last human checks |

**No numeric increase is evidence of a higher journal acceptance probability.** The scores express only the relative completeness of this updated simulation.

## Reviewer comment closure matrix

| Item | Resolution in R1 | Status |
|:--|:--|:--|
| T2 Table 4 split across pages 7–8 | Move V38-B heading/table together and enforce non-splitting table rows; GitHub PDF QA checks first and last table line on same page | **CLOSED — verified in PDF** |
| T3 duplicate captions for Figures 1–3 | Single complete descriptive caption per image; GitHub Word test asserts one per figure | **CLOSED — verified** |
| T4 missing original Figure 1, original Supplement S1 and Figures S1–S10 from prior review ZIP | Generate separate historical S1 Word with 10 embedded images; include original standalone Figure 1, all supplement artwork | **CLOSED for review package**; upload classification requires journal-guide check |
| Editor novelty unclear | Six-row prior-publication/D-MFPP scope matrix; title and exact claimed novelty retained | **ADDRESSSED WITH LIMITATION**; source/text overlaps still require author certification |
| R1.1 AUC ranking/evaluation circularity | Revised wording states within-detector perturbation diagnostic rather than independent explanation faithfulness | **CLOSED as disclosure**; no new independent comparator |
| R1.2 coarse–fine spatial area logic unclear | Equations for signed drop and 4×4 direct versus sum of four fine 8×8 drops divided by exact coarse area | **CLOSED**; nonlinear spatial effects remain |
| R1.3 JPEG vs PNG cohorts | Keep historical V34 and V38-B results separate | **CLOSED as limitation** |
| R1.4 ambiguity accounting | Three missing targets remain explicitly null with original denominators; no post hoc substitute | **CLOSED** |
| R2 rank distribution and cluster influence | rho median 0.687270, IQR 0.514706–0.811765, range −0.017647–0.926471, 11/45 <0.5, image LOIO 0.640997–0.664868 | **CLOSED as descriptive sensitivity** |
| R2 operator paired robust interval | 14 matched across eight images, paired median blur-minus-gray −0.176471, image-LOIO paired mean −0.248039 to −0.178659 | **CLOSED as descriptive sensitivity** |
| R3 17-class PPE detection metrics | Exact archived 17-class TP/FP/FN, precision/recall/F1 appended to S2 | **CLOSED**; limited single-curator GT |
| R3 engineering interpretation | Conditional human-review recommendation with no unmeasured outcomes | **CLOSED as measured-boundary clarification** |
| T1 author/ethics declaration placeholders | Unsigned worksheet retained; no false statements of approval, consent, funding or absence of conflict | **OPEN / AUTHOR-ONLY** |
| T5 public image identifiers, personal-image disclosure and contractual publication rights | Risks identified; immutable numeric evidence not altered, no rights or anonymity invented | **OPEN / AUTHOR+INSTITUTION** |
| T6 exact current journal author guide and submission metadata | General Elsevier guidance checked but journal-specific portal rules unverified | **OPEN / JOURNAL-PORTAL CHECK** |
| Originality overlap with own 2025/2026 papers | Prior-work matrix added, but no signed detailed originality certification or text/figure license verification | **OPEN / AUTHOR-ONLY** |

## Remaining *scientific* weaknesses (not software bugs)

- The images were **development-exposed**, source-project-family independence not certified. The 24 images are not independent site samples. An internal image-cluster bootstrap/LOIO is no substitute for independent-source field validation.
- Target score changes are *perturbation responses* and may differ with the replacement operator. The methodology does not demonstrate true causal explanations or worker PPE compliance.
- The favorable AUC margins against ten randomized rankings are **same-model, same-perturbation-type controls**; they are not a head-to-head experiment with D-RISE/D-MFPP.
- The set of 45 estimable targets may suffer selection bias when three same-class target matches become ambiguous. Results are conditional on estimability.
- Class F1 results are against the **single-curator** original-source validation reference at the frozen threshold, not a second blinded annotator.
- The author must still certify novelty and distinguish exact experiments/datasets/figures reused in related earlier work. A published title alone does not fully settle publication overlap.

## Editorial decision of this simulated second round

**TECHNICAL FILE QUALITY:** PASS for reviewed Word/PDF/layout and complete *review-only* ZIP; this is **not** a journal-specific technical submission clearance.

**SCIENTIFIC REVIEW READINESS:** Improved and **plausible to send to external reviewers after author-only P0 gates**, with **Major Revision** still a reasonable possible outside outcome. Additional model inference is not a prerequisite for a *bounded descriptive XAI study*. A broader causal/algorithm-superiority claim would need new comparisons and independently sourced data.

**PUBLICATION/ETHICS AND FINAL SUBMISSION:** **HOLD**. Do **not** strip placeholders automatically or certify unproven informed consent, IRB exemption, no conflicts, no grant funding, author list approval, originality or lawful public photo links. No journal submission has been made.

## Exact available review artifacts in GitHub

- R1 manuscript source: `research/seer-ppe/submissions/results-in-engineering/RINENG_MANUSCRIPT_V39_R1_REVIEWED_DRAFT_2026-11-23.md`
- R1 S2 source: `research/seer-ppe/submissions/results-in-engineering/RINENG_SUPPLEMENT_V39_R1_S2_REVISED_2026-11-23.md`
- R1 Word manuscript: `research/seer-ppe/exports/RINENG_V39_R1_Manuscript_Review_Only_UNSIGNED.docx`
- Original historical S1 editable Word: `research/seer-ppe/exports/RINENG_V39_R1_Supplement_S1_Review_Only.docx`
- Updated S2 editable Word: `research/seer-ppe/exports/RINENG_V39_R1_Supplement_S2_Review_Only.docx`
- **Complete review-only ZIP:** `research/seer-ppe/exports/RINENG_V39_R1_REVIEW_ONLY_NOT_SUBMITTED_PACKAGE_2026-11-23.zip`
- CI result: https://github.com/EZZALDEEN049/Y-PPE-Detection-RFDETR/actions/runs/45094516733

### External/public standards checked, not substituted for the journal's guide

- Elsevier generic author guide: https://www.elsevier.com/en-gb/subject/next/guide-for-authors
- Elsevier artwork checklist: https://www.elsevier.com/about/policies-and-standards/author/artwork-and-media-instructions/artwork-formats-checklist
- Industrial object-detector XAI comparator: https://doi.org/10.1016/j.rineng.2024.103498
- DASA 2025 conceptual X-RF-DETR: https://ieeexplore.ieee.org/abstract/document/11498849

 and `$...$` math. The **final** [GitHub Actions full-package QA run 45095099443](https://github.com/EZZALDEEN049/Y-PPE-Detection-RFDETR/actions/runs/45095099443) returned success and explicitly inspected `word/document.xml` for editable native Office Math (`m:oMath`), while refusing literal `\\Delta` or `\\frac` leakage. Inspection of the archived final DOCX confirms **15 Office Math XML elements** with no raw LaTeX in the Word XML; PDF visual examination shows two correctly typeset equations on the Methods page. The previous review-only PDF was superseded by this corrected version.

Final Word: 15 manuscript pages, six editable tables (including novelty matrix) and three uniquely captioned figures. Table 4's first and last data rows appear together on PDF page 9. Historical Supplement S1 contains ten visualizations (13 landscape pages) and revised S2 includes the full 17-category detection metric table (six landscape pages). A complete review-only ZIP with original Figure 1, Figures 2–3 and the ten S1–S10 individual artwork files has been preserved in GitHub. Layout is technically checked; the journal's exact guide and author-only signoffs remain open.

**Second-round simulation authorship:** Generated as editorial-analysis assistance, not by named external professors and not representing a journal verdict. No scientific numerical files or model source images were modified.
