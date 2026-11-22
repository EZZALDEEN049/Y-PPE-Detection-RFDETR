# SEER-PPE — Publication journal targeting and due-diligence memorandum

**Research date:** 22 November 2026  
**Project:** SEER-PPE, main manuscript v0.43 + v0.43 supplementary material  
**Purpose:** Evidence-based journal selection, not an acceptance prediction  
**Assessment type:** Editorial fit and publisher-policy due diligence; **not** a formal JCR institutional eligibility determination.

## Executive recommendation

**Tier 1, strategically recommended:** (1) **IEEE Access** if the final author affiliations satisfy IEEE's 2026 Group-A geographic waiver; (2) **Results in Engineering** if the final author group qualifies for Elsevier's fully-OA Research4Life/GPOA waiver and the journal's technical-soundness criterion; (3) **Journal of Imaging** for the strongest direct topic match, subject to an APC budget or written discount.

**Budget-conscious hybrid alternative:** **Machine Vision and Applications** (Springer Nature), under subscription publishing with no APC, but experimental-strength requirements are more demanding than the current ten-target XAI cohort.

**Stretch journals, not first submissions on present evidence:** **Engineering Applications of Artificial Intelligence**, **Automation in Construction**, **Safety Science**; each demands substantial additional novelty, generalization, or actual downstream worker-safety evaluation beyond the existing evidence.

**No journal is presently ready for submission** while worker-image ethics/consent/privacy and author declarations remain incomplete. A 62-page journal-neutral main manuscript needs article-focused trimming and removal of internal stage/audit labels.

## 1. Study actually performed — editorial scope boundary

Current facts in manuscript v0.43:
- 17-class frozen RF-DETR Small on the Y-PPE corpus, Clean17 2,288 images.
- Original-source Validation: 459 images, 3,471 annotated instances; 3,297 TP, 806 FP, 174 FN; micro precision 0.8036, recall 0.9499, F1 0.8706.
- Black-box target-matched occlusion/deletion/insertion, ten selected targets from eight development-exposed images; 8×8 versus 4×4 maps.
- Mean Spearman spatial rank agreement 0.5416; Kendall tau-b 0.4239; mean top-four region overlap 65%; one target zero overlap.
- A5/A6 arm populations are not identical; a deterministic random ordering frequently equaled/exceeded saliency. No statistical A5/A6 superiority.
- No verified worker–PPE compliance endpoint, independent site generalization, valid human efficacy, causal explanation faithfulness, physical energy savings, or untouched external Test endpoint.
- Earlier 2025–2026 Y-PPE model/AI papers have already disclosed the detector and conceptual PPE/XAI integrations. Novelty must be confined to the *newly measured target-specific perturbation and grid-stability evidence*, without redundant publication.

**Recommended main-paper title:** “Target-Matched Perturbation Responses and Grid-Resolution Stability in PPE Object Detection: A Frozen RF-DETR Case Study.”

**Preferred framing:** reproducible diagnostic/robustness evidence, including limitations/negative findings; not a worker-safety intervention validated in the field, not a new detector, not an established new saliency method.

## 2. Matrix — journals, scope, metrics, costs, editorial decisions

Rank is an **editorial priority judgment**, *not* an estimated chance of acceptance. Where multiple Q1/Q2 designations appear, the metric family matters. Reported 2025 journal indicators are those available in November 2026.

| Priority | Journal/publisher | Verified category or indicator | Current manuscript fit | APC/publication model and 2026 policy | Editorial call |
|---|---|---|---|---|---|
| **1** | **IEEE Access** / IEEE | SCIE and Scopus; **JCR JIF quartile Q2**, 2025 IF **4.2**; CiteScore **9.3**; SJR 0.884 | **High after refocusing**, including negative measurement results in explicit scope | Gold OA **USD 2,160** for 2026 submissions; **100% waiver conditional** on *all* authors' institutions being in IEEE's low-income Group A (2026 list expressly includes Yemen) | Best strategic balance for an eligible Yemeni-only author group; 20% journal-wide average acceptance rate reported, **not** a manuscript-specific probability |
| **2** | **Results in Engineering** / Elsevier | **SCImago SJR Q1 (Engineering miscellaneous, 2025)**; **do not equate this with verified JCR Q1** | **High–moderate**, broad scientifically sound engineering outcomes | Fully OA. Elsevier waiver policy: **100% for eligible Group A author groups** (Yemen is expressly listed); exact journal APC to reconfirm in submission. DOAJ currently says up to USD 2,160, not a price quotation | Very attractive if sound applied-engineering results + no-fee publication are priorities. Direct publisher journal-page retrieval was restricted, so journal-specific APC/JCR not claimed verified |
| **3** | **Journal of Imaging** / MDPI | Scopus, WoS **ESCI**, Ei Compendex; **JCR Q2** (Imaging Science and Photographic Technology), CiteScore Q1 in publisher's listed category; IF **3.8** | **Very high scientific subject fit** in image understanding and explainability | Fully OA, **CHF 1,800** for submissions in 2026; **CHF 2,000** for submissions from 1 Jan 2027; no confirmed Yemen automatic waiver | Top topic-match if fees can be covered/waived by written approval. Has published a close 2026 PPE-XAI stability study, so differential novelty must be explicit |
| **4** | **Machine Vision and Applications** / Springer Nature | Scopus and SCIE; Q status is category/year dependent; external sources indicate **JCR Q3** | High *field* fit but stricter substantial experimental validation demanded | **Hybrid**: subscription route **no APC**; optional OA GBP 2,590 / USD 3,590 / EUR 2,890 at time checked | Best zero-APC non-OA fallback if data and comparator analyses are strengthened |
| **5** | **Applied Sciences** / MDPI | Scopus, SCIE; **JCR Q2** (Engineering, Multidisciplinary) | Broad applied-engineering fit, moderate selectivity | Fully OA **CHF 2,400**; discounts dependent on publisher rules and written approval | Backup if broad applied framing and fee budget |
| **6** | **Sensors** / MDPI | Scopus, SCIE; **JCR Q2** (Instruments and Instrumentation) | Moderate: imaging is a sensing modality, but no sensor hardware/fusion contribution | Fully OA **CHF 2,600** | Do not create sensor-system novelty that does not exist |
| **7** | **Frontiers in Built Environment** / Frontiers | Scopus, WoS ESCI; **JCR Q2**, CiteScore Q1 (publisher's 2026 metrics) | Moderate–low under Construction Management scope: explicitly excludes generic safety without management perspective | Gold OA, Original Research **CHF 2,695** before discretionary fee support | Consider only with real construction-management workflow/outcome framing; otherwise scope rejection risk |
| **8 (stretch)** | **Engineering Applications of Artificial Intelligence** / Elsevier | Publisher lists **IF 9.0** | Low for present experimental strength; high engineering-AI novelty standards | Hybrid subscription or paid OA; specific APC not asserted | Journal explicitly requests novel AI application and validation with public datasets; current proprietary/controlled-image setting and small XAI sample are major barriers |
| **9 (stretch)** | **Automation in Construction** / Elsevier | 2025 **SCImago Q1** | Low *now*: no tested construction-management or worker-safety intervention | Hybrid subscription or paid OA | Better target for a future paper with independent site tests and worker/task-level safety outcomes |
| **Excluded for current study** | **Safety Science** / Elsevier | 2025 SCImago Q1 | **Low**: no hazard reduction, human workflow outcome, or risk-control effectiveness estimated | Hybrid subscription or paid OA | Do not submit an object-detection/perturbation study while advertising measured safety effectiveness |

### Why the rankings are deliberately conditional

- **Quartiles are not universal:** IEEE Access = **JCR Q2** (IEEE's September 2026 title list) even if SCImago lists a Q1 category. Journal of Imaging = **JCR Q2** despite CiteScore Q1 in some Scopus categories. Results in Engineering = **SCImago Q1** in the verified search metadata; **JCR quartile was not verified in an authoritative institution-accessible Clarivate record**.
- An author team with **one noneligible affiliate** may lose the IEEE waiver entirely. IEEE's Group A, B and C mix rules are explicit. Eligibility depends on **institutional location, not ethnicity/nationality or photo locations**. For Elsevier gold OA, all author groups must satisfy its country policy. **Do not claim guaranteed free publication before submission/billing confirmation.**
- MDPI did not publish an equivalent automatic Yemen waiver in the APC sources inspected. Publisher discretion/institutional discount should be asked about **before financial commitment**.
- Publisher's 'first decision' or 4–6 week publication statements are historical/advertised and **not promised timelines for this article**.
- Q1 in one ranking service is **not** a substitute for the university's required JCR category/edition: obtain the local master's/doctoral promotion regulation before using a journal as Q1-qualified.
- Selection does **not** establish that any journal is guaranteed to accept the paper.

## 3. Editorial SWOT for the research

**Strengths**
- Archived fixed-model object-level evaluation on a 459-image validation cohort, detailed numerical audit, full perturbation-call accounting and reproducible signed heatmaps.
- Scientifically useful *negative* result: black-box attribution changes with grid resolution and frequently does not outperform deterministic random deletion control.
- Conservative separation of detector object predictions from worker-level legal/occupational compliance, and no false energy-performance claims.
- A real Yemen field-photo corpus adds applied relevance, provided image rights/privacy are addressed.

**Risks requiring remediation before *any* submission**
1. **Ethics/privacy**: author must supply real committee approval, exemption determination or a journal-accepted documented rationale plus the rights/consent/privacy basis for people pictured; no fabricated approval.
2. **Image-source dependence**: source/media-family overlap across source Train/Validation weakens generalization; retain sensitivity analyses and explicit limits.
3. **XAI sample**: ten targets in eight development-exposed images do not support broad, independent-site or population inferential claims. No p-values/uncertainty estimates for performance across sites without legitimate denominators.
4. **Comparators**: one deterministic random ordering and non-identical A5/A6 target sets do not demonstrate selective-policy superiority. Explain failures in primary discussion.
5. **Prior-work overlap**: cite and differentiate the author's 2025 RF-DETR/X-RF-DETR and 2026 PPE comparison/BIM work; avoid novel-architecture or deployed-safety claims.
6. **Submission aesthetics**: 62-page v0.43 main plus 34-page supplement remain working research dossiers. Move audit registers, stage codes, row-level engineering logs and much of the 16 main tables out of main paper. Journal-specific page/word limits must be checked.
7. **Disclosures**: funding, competing interests, author contributions, permissions, data/software sharing terms. Verify IEEE author lists in two eSmarTA citations.
8. **Provenance warnings**: original V27 execution start/end chronology and nested V34-B PDF hash duplication stay in internal audit unless primary evidence resolves them.

## 4. Two realistic submission pathways

### Path A — strong journal, current completed evidence, minimal new inference
1. Reframe as *object detection and perturbation-response robustness*, NOT 'validated SEER-PPE safety routing'.
2. Lead abstract with testable question: Do 8×8 and 4×4 black-box occlusion rankings agree for the *same frozen target detections*? Report full ten-target sample and the zero-overlap case prominently.
3. Concentrate results: one detector metrics table, one AUC/baseline table, one alignment table, one composite figure; target maps in supplement.
4. Trim technical manuscript to an article-shaped narrative (suggested editorial **target** ~6,000–8,000 words, **not** a verified limit of any journal); follow journal-specific rules.
5. Complete ethics/rights and author financial disclosures.
6. Submission order **one journal at a time**: IEEE Access (if eligibility confirmed) → Results in Engineering (if university considers its index acceptable) → Journal of Imaging (if APC support obtained). If publisher preference/discipline is predominant, Journal of Imaging can go first.

### Path B — prioritize higher-selectivity Q1 specialist journal (new evidence required)
- Define independent site/source groups and an authorized **new** held-out evaluation; do not access currently protected Test opportunistically.
- Plan many more independently sampled targets, image/site-clustered confidence intervals and repeated-seed random and alternate baseline attribution controls.
- Prespecify strong *target-matched* comparator(s), explanation faithfulness tests, and prospective human review/worker–PPE association if the actual contribution claims occupational safety.
- Validate energy and latency only by direct physical measurements on named hardware, not cloud round-trip as device latency or estimated energy.
- Obtain actual incremental novelty over Di Renzo 2026, Paes et al. 2024 and previous SEER conceptual work.
- **No inference/retraining is authorized by this journal-ranking report**; these are proposed future-study requirements, not completed research.

## 5. Publisher and journal sources (verified 22 Nov 2026)

1. IEEE Access aims, negative-result scope, 20% overall acceptance, process: https://ieeeaccess.ieee.org/about/
2. IEEE September 2026 title list (**IEEE Access JCR Q2, IF 4.2**): https://open.ieee.org/wp-content/uploads/IEEE-Title-List-September-2026-CAPES.pdf
3. IEEE Access bibliometrics/SCIE/Scopus: https://ieeeaccess.ieee.org/about/bibliometrics/
4. IEEE 2026/2027 APC schedule: https://open.ieee.org/for-authors/article-processing-charges/
5. IEEE low-income waiver conditions (all-author location): https://open.ieee.org/for-authors/ieee-low-and-lower-middle-income-country-open-access-discount-program/
6. IEEE 2026 country list (**Yemen in Group A**): https://open.ieee.org/wp-content/uploads/2026-GEO-Countries-Updated.pdf
7. Elsevier full gold OA country waivers including **Yemen** and limitations: https://www.elsevier.com/about/policies-and-standards/pricing
8. Results in Engineering independent SCImago journal record (2025 SJR Q1): https://www.scimagojr.com/journalsearch.php?q=21100904991&tip=sid
9. Results in Engineering DOAJ record (fully OA, waiver policy, APC cap): https://doaj.org/toc/2590-1230
10. Journal of Imaging official scope and reproducibility provisions: https://www.mdpi.com/journal/jimaging/about
11. Journal of Imaging indexing, quartiles, IF: https://www.mdpi.com/journal/jimaging/
12. Journal of Imaging **CHF 1800 in 2026; CHF 2000 if submitted from 2027**: https://www.mdpi.com/journal/jimaging/apc
13. Closest 2026 PPE explainability prior publication: https://www.mdpi.com/2313-433X/12/5/195
14. Machine Vision and Applications scope, significant validation requirement: https://link.springer.com/journal/138/aims-and-scope
15. Springer journal-specific hybrid costs and no-APC subscription route: https://link.springer.com/journal/138/how-to-publish-with-us
16. Applied Sciences official scope/metrics and APC: https://www.mdpi.com/journal/applsci ; https://www.mdpi.com/journal/applsci/apc
17. Sensors official scope/metrics and APC: https://www.mdpi.com/journal/sensors ; https://www.mdpi.com/journal/sensors/apc
18. Frontiers in Built Environment 2026 JCR/CiteScore status: https://www.frontiersin.org/about/impact
19. Frontiers construction-management scope exclusion: https://www.frontiersin.org/journals/built-environment/sections/construction-management/about
20. Frontiers Original Research APC/fee-support route: https://www.frontiersin.org/journals/built-environment/sections/construction-management/for-authors/publishing-fees
21. Engineering Applications of Artificial Intelligence publisher scope and mandatory pre-review conditions: https://shop.elsevier.com/journals/engineering-applications-of-artificial-intelligence/0952-1976
22. Automation in Construction SCImago Q1 and journal scope: https://www.scimagojr.com/journalsearch.php?q=24931&tip=sid

## 6. Decision requiring author/institution facts — not yet answered

**A.** Does the university require JCR-Q1 specifically, JCR-Q2, Scopus/SCImago-Q1, or only indexed SCI/SCIE? **Do not equate metrics**.  
**B.** Are *all* named manuscript authors (including any future coauthor) affiliated with eligible Group A institutions in 2026 for IEEE/Elsevier waivers?  
**C.** Can the author document the legal/ethics/consent basis for recognizable worker images and describe permitted public sharing accurately?  
**D.** Can an MDPI fee of CHF 1800/2000 be funded or waived if Journal of Imaging is preferred?

**Decision of this report:** proceed to editorial reshaping and disclosure work under **Path A**; keep the higher-tier **Path B** as a separate prospective research design requiring explicit later approval. No manuscript submission has been initiated.
