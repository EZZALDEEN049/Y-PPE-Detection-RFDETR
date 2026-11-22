# V35-E — Main manuscript/supplement packaging and visual layout QA

**Date:** 22 November 2026  
**Status:** PASS for editable package generation, automated validation and representative visual QA; submission gates remain open.  
**Branch:** `research/v30-progressive-xai-2026-11-22`  
**Archive commit:** [1ca9aed51b554677702d3b4c5a903ddc3ca76e7d](https://github.com/EZZALDEEN049/Y-PPE-Detection-RFDETR/commit/1ca9aed51b554677702d3b4c5a903ddc3ca76e7d)

## Deliverables

| Deliverable | Pages | Tables | Figures | File |
|---|---:|---:|---:|---|
| Main research manuscript v0.43 | 62 | 16 | 1 summary figure | [Editable Word file](https://github.com/EZZALDEEN049/Y-PPE-Detection-RFDETR/blob/research/v30-progressive-xai-2026-11-22/research/seer-ppe/exports/SEER_PPE_Research_Manuscript_v0.43_2026-11-22.docx) |
| Supplementary material v0.43 | 34 | 2 | 10 paired maps | [Editable Word file](https://github.com/EZZALDEEN049/Y-PPE-Detection-RFDETR/blob/research/v30-progressive-xai-2026-11-22/research/seer-ppe/exports/SEER_PPE_Supplementary_Material_v0.43_2026-11-22.docx) |
| Combined package | 96 | 18 | 11 | Main + supplement |

The complete v0.42 research dossier was preserved separately as `MANUSCRIPT_FULL_RESEARCH_DOSSIER_v0.42_2026-11-22.md`. The v0.43 main article retains the title/author block, a concise stage-neutral abstract, the scored image-level and perturbation results, the spatial-agreement summary figure and references. Historical non-scoring source-lineage/Person–PPE contracts and detailed audit appendices A–X were moved—not deleted—to the supplementary file. The ten target-specific paired heatmaps are Supplementary Figures S1–S10.

## QA performed

- Main and supplementary DOCX ZIP integrity checks passed.
- Main DOCX: 16 nonempty tables and one embedded image.
- Supplementary DOCX: two tables and ten embedded images.
- Rendered both DOCX files through LibreOffice to PDF: 62-page main and 34-page supplement.
- No page with fewer than 40 extracted text characters was detected in either PDF.
- Inspected main first, middle and last page previews; supplementary first and last previews; and the key V26 cohort/class-result pages.
- First page begins with the paper title and author block; no empty Table of Contents heading remains.
- Main summary figure and all ten supplementary paired maps render.
- No model inference, retraining, Test access, image/annotation/split mutation or original-model modification occurred.

## CI verification

- [Word export and main/supplement PDF QA — run 45038161463](https://github.com/EZZALDEEN049/Y-PPE-Detection-RFDETR/actions/runs/45038161463): **success**.
- [Source/reference readiness gates — run 45038166451](https://github.com/EZZALDEEN049/Y-PPE-Detection-RFDETR/actions/runs/45038166451): **success**.
- [Public engineering tests — run 45037976977](https://github.com/EZZALDEEN049/Y-PPE-Detection-RFDETR/actions/runs/45037976977): **success**.
- [Rendered QA artifact 14760248670](https://github.com/EZZALDEEN049/Y-PPE-Detection-RFDETR/actions/runs/45038161463/artifacts/14760248670) contains both PDFs, both DOCX files and representative page previews.

## Remaining before submission

1. Confirm the ethics approval/exemption and the consent/privacy basis for worker imagery.
2. Add the funding, competing-interest and author-contribution declarations.
3. Confirm the two eSmarTA 2026 author lists/order against the author PDFs or official IEEE metadata. Secondary records currently list:
   - *BIM-Integrated Explainable Vision for Real-Time PPE Safety in Yemen's Construction Sector*: Al-Tayar; Al-Azazi; Ali; Alawag.
   - *PPE Detection in Yemeni Construction Sites: YOLOv11m vs. RF-DETRs*: Al-Tayar; Al-Azazi; Saeed; Ali; Hassan.
   The conference proceedings DOI is listed by the publisher gateway, but individual IEEE Xplore pages were blocked by JavaScript verification in this pass. See [secondary record 1](https://eurekamag.com/research/110/329/110329262.php), [secondary record 2](https://eurekamag.com/research/110/329/110329220.php), and [official proceedings gateway](https://yostr.org/en/publications).
4. Select the target journal. The 62-page main article is a complete working research manuscript, not yet a journal-length submission; compress and reformat it against the selected journal's rules.
5. Move the internal reference-audit note out of the reference list and neutralize remaining internal V-stage labels in Results/Discussion headings.
6. Resolve or explicitly retain the two technical audit warnings: V27 timestamp chronology and the V34-B nested duplicate PDF hash.

## Scientific integrity boundary

The package reports image-level detection and perturbation-response evidence only. It does not claim worker-level compliance, Person–PPE association accuracy, reviewer efficacy, independent-site generalization, causal explanation faithfulness, physical energy savings or regulatory certification. No Test split was accessed and no model retraining was performed.
