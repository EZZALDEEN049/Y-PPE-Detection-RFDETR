# SEER-PPE V35-C — Literature and editorial audit

**Date:** 22 November 2026  
**Branch:** `research/v30-progressive-xai-2026-11-22`  
**Manuscript:** v0.38  
**Status:** **PARTIAL PASS — focused reference set expanded and checked; author/journal declarations remain open**

## 1. Scope

This pass reviewed the references actually used in Sections 1–3 and the V34-A statistical methods, checked bibliographic metadata against official proceedings, publisher or institutional records where accessible, expanded the reference list, and corrected the article structure. This is a focused literature and metadata audit, **not** a PRISMA systematic review and not proof of worldwide novelty.

## 2. Work completed

- Expanded the bibliography from 9 selected entries to **17 references**.
- Added foundational sources for meaningful perturbation, deletion/insertion evaluation, saliency sanity checks, random/quantitative baselines, and rank correlation:
  - Fong & Vedaldi (2017)
  - Petsiuk et al. (2018)
  - Adebayo et al. (2018)
  - Hooker et al. (2019)
  - Spearman (1904)
  - Kendall (1938)
- Completed the four author-prior-publication entries in the reference list and distinguished same-year records as 2025a/2025b and 2026a/2026b.
- Replaced the incomplete “systematic verification incomplete” heading with an explicit **focused, non-systematic related-work** description.
- Added method citations to Sections 2, 3.6 and 3.26. The text explicitly states that model-parameter/label-randomization sanity checks were **not** run and that one deterministic random ordering is only a limited control.
- Added a substantive **Section 7. Conclusion** based only on the audited image-level results and their limits.
- Removed the internal V35 workplan from the article body. The closure tasks are retained in this audit record instead.
- Updated Section 3.11 to reflect that V35-A and V35-B are complete.
- Added transparent statements that ethics/consent, funding, competing-interest and author-contribution declarations still require author confirmation.

## 3. Reference-source audit

| Reference group | Verification source | Outcome |
|---|---|---|
| Selective explanations — Paes et al. (2024) | Official NeurIPS proceedings: https://papers.nips.cc/paper_files/paper/2024/hash/647af5f6b2538524f6c047c1d9170fd9-Abstract-Conference.html | Title, authors, venue and DOI confirmed |
| Sentry–Judge PPE — Vaghani (2026) | Official Frontiers record: https://www.frontiersin.org/journals/built-environment/articles/10.3389/fbuil.2026.1976288/abstract | Title, author, journal, year and DOI confirmed |
| CA4PPE — Bouguessa et al. (2026) | ScienceDirect publisher record: https://www.sciencedirect.com/science/article/pii/S0952197626020099 | Title, authors, journal, volume/article number and DOI confirmed from publisher record/abstract |
| Work-at-height scene graph — Yi et al. (2026) | ScienceDirect and institutional record: https://www.sciencedirect.com/science/article/pii/S1474034626003046 ; https://research.polyu.edu.hk/en/publications/regulation-aligned-ppe-compliance-assessment-for-work-at-height-u/ | Title, authors, journal, volume/article number and DOI confirmed |
| PPE ViT explainability — Di Renzo et al. (2026) | Official MDPI record: https://www.mdpi.com/2313-433x/12/5/195 | Full author list, title, issue and DOI confirmed |
| RF-DETR — Robinson et al. (2026) | ICLR/OpenReview record: https://openreview.net/pdf?id=qHm5GePxTh ; official project citation: https://github.com/roboflow/rf-detr | Authors, ICLR 2026 venue and paper title confirmed |
| PPE systematic review — Barlybayev et al. (2026) | Official MDPI record: https://www.mdpi.com/2073-431x/15/6/388 | Full eight-author list, journal, issue/article number and DOI confirmed |
| Meaningful perturbation — Fong & Vedaldi (2017) | CVF proceedings: https://openaccess.thecvf.com/content_iccv_2017/html/Fong_Interpretable_Explanations_of_ICCV_2017_paper.html | Title, authors, venue and DOI confirmed; page range omitted because secondary records disagreed |
| Saliency sanity checks — Adebayo et al. (2018) | Official NeurIPS proceedings: https://proceedings.neurips.cc/paper/2018/hash/294a8ed24b1ad22ec2e7efea049b8737-Abstract.html | Title, authors and venue confirmed |
| Interpretability benchmark — Hooker et al. (2019) | Official NeurIPS proceedings: https://proceedings.neurips.cc/paper/2019/hash/fe4b8556000d0f0cae99daa5c5c5a410-Abstract.html | Title, authors, venue and pages confirmed |
| Spearman (1904) | JSTOR DOI record: https://doi.org/10.2307/1412159 | Title, journal, volume, issue, pages and DOI confirmed |
| Kendall (1938) | Oxford Academic: https://academic.oup.com/biomet/article-abstract/30/1-2/81/176907 | Title, journal, volume, issue, pages and DOI confirmed |
| Author's two DASA 2025 papers | IEEE Xplore: https://ieeexplore.ieee.org/abstract/document/11499131 ; https://ieeexplore.ieee.org/abstract/document/11498849 | Titles, venue, year and DOI confirmed; proceedings index also supplied page ranges and author order |
| Author's two eSmarTA 2026 papers | Secondary proceedings index: https://eurekamag.com/research/110/329/110329220.php ; https://eurekamag.com/research/110/329/110329262.php | Titles, DOI, venue/year and abbreviated author order recorded; **official IEEE author metadata was not retrievable and remains to be confirmed** |

## 4. Scientific-claim boundary

The updated text does not claim that selective explanation, uncertainty-gated PPE verification, scene-graph reasoning, PPE heatmaps or RF-DETR were invented by this study. The novelty boundary remains a measured, limited combination of fixed-detector image-level evaluation and target-specific perturbation-response analysis. The current experiments do not establish causal explanation faithfulness, worker compliance, human-review efficacy, independent-site generalization, policy superiority or physical-energy savings.

## 5. Remaining blockers to final submission readiness

1. **Ethics and consent:** the repository contains no ethics approval/exemption identifier or documented participant-consent statement for identifiable worker imagery. The author must provide the applicable institutional determination and confirm the consent/privacy basis; no approval or consent is assumed.
2. **Author declarations:** funding, competing interests and author contributions are not documented and require confirmation.
3. **Two eSmarTA references:** verify the complete author lists and final proceedings details against the official IEEE records or author PDFs.
4. **Target journal:** not yet selected. Abstract limits, reference style, word limits, figure specifications and supplementary-material rules therefore cannot be finalized.
5. **Supplementary material:** decide whether Appendices A–X remain in the full handoff or are separated into a journal-length main paper plus supplementary file.
6. **V27 timestamp:** the impossible start/finish chronology remains unresolved because the original execution log is not present in the audited evidence; no inferred UTC correction was applied.
7. **V35-D Word export:** the existing workflow is stale: it names v0.27, lacks the V34-B resource path needed to resolve relative images, validates old content only, and pushes generated files to `main`. It must be updated to generate v0.38 on the selected research branch before triggering.
8. **V35-E final QA:** inspect rendered pages, embedded images, tables, figure numbering/cross-references, links and metadata; retain the manifest-selected canonical V34-B PDF and resolve or clearly archive the nested duplicate PDF.

## 6. Integrity constraints

- Zero new RF-DETR calls.
- No retraining, Test access, image mutation, annotation mutation or split change.
- No change to the original model or original dataset.
- The V35-A numeric warning and V34-B duplicate-PDF warning remain visible; neither is silently corrected.
- The reference review is focused and non-systematic; it must not be described as a PRISMA review.

**Decision:** V35-C reference and structural edits are recorded in manuscript v0.38. The manuscript is more complete, but it is **not yet 100% submission-ready** until the author and journal-dependent blockers above are resolved.
