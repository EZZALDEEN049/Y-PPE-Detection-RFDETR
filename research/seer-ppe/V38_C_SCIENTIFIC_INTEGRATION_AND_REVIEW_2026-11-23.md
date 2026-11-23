# V38-C — Scientific integration, ambiguity audit and RINENG editorial decision

**Date:** 23 November 2026  
**Approved manuscript title:** Cross-Resolution Consistency of Target-Matched Perturbation Sensitivity Maps for Personal Protective Equipment Detection  
**Target journal:** Results in Engineering (Elsevier)  
**Research branch:** research/v30-progressive-xai-2026-11-22

## 1. Scientific evidence that was actually generated

The one-time Roboflow-hosted RF-DETR Small extension finished with 24/24 frozen Valid source images, 48/48 frozen detections across eleven PPE class names, and **4,984 model requests attempted and succeeded**, preserving a **6,000 total attempted-call ceiling**. Independent GitHub Actions numeric audit verified all 4,984 write-ahead attempted calls and all success records as contiguous, with no failed requests. No retraining, class/annotation modification or protected Test access took place.

**Rankable cross-grid (8×8 vs 4×4) signed-density maps:** 45/48 exact target IDs, with 3 non-estimable due to ambiguous same-class match after single-cell perturbation. The conditional 45-target mean Spearman rho was **0.648979**, Kendall tau-b **0.519741**, and top-four overlap **66.6667%**. The 24-image-balanced rho mean was **0.650758**; a deterministic 5,000-resample image-level bootstrap yielded descriptive percentiles **0.594957–0.704350**. These do not provide external acquisition-family population confidence coverage.

**Operator control:** Of 16 preselected targets in eight images, 15 were blur-fill rankable and 14 were paired rankable under gray and blur. The mean Spearman rho in the **same fourteen targets** was **0.694259 gray**, **0.481092 blur**, paired delta **−0.213166** blur-minus-gray; 10 cases fell and four rose. This supports sensitivity to the image occlusion replacement operator. It does not prove that neutral gray is a more truthful explanation.

**Random-order control:** Twelve preselected targets, eleven with valid 8×8 ranking and blurred endpoints; **264/264 planned run curves** yielded valid deletion/insertion AUCs. Saliency order beat the **mean of ten seeded random rankings per target** in the favorable AUC direction for 11/11 deletion and 11/11 insertion. Mean difference was **−0.408378 deletion** (lower favorable) and **+0.371961 insertion** (higher favorable). The same detector's perturbation scores construct and evaluate saliency; this is not independent causal XAI ground truth, nor a direct D-RISE/D-MFPP performance comparison.

**Historical data preserved:** The earlier V34A ten-target/eight-image development-exposed study yielded mean rho 0.5416, Kendall 0.4239 and 65% top-four overlap, including one zero-overlap target. It remains separately reported. The larger V38-B sample and the earlier cohort were not treated as a paired or externally independent replication; image selection and JPEG transmission settings differ.

## 2. Exactly three ambiguous target maps

See the separate target-by-target scientific note `V38_C_THREE_AMBIGUOUS_TARGETS_SCIENTIFIC_REVIEW_2026-11-23.md`. It records 13 ambiguous target-cell responses involving one No Safety Vest, one Safety Vests and one Hard Hat target. Map correlations for these three targets remain null (not zero). The No Safety Vest target was also blocked from curve testing and was not replaced. All 48 frozen target IDs remain in the scientific sample denominator.

## 3. Results in Engineering manuscript integration

A new **V38-C v0.3 scientific manuscript** is saved under `submissions/results-in-engineering/RINENG_MANUSCRIPT_V38C_v0.3_2026-11-23.md`, leaving V36 and V37 archival files intact. Additions include:
- Rewritten **219-word abstract**, retaining the accepted title and six original journal keywords.
- Explicit prospective V38-B sample, EXIF-canonical source selection, fixed JPEG 95 4:4:4 transport, signed area-normalized 8×8↔4×4 endpoint and image-level descriptive uncertainty.
- Tables **4 and 5** and two new standalone numbered artwork images **Figure 2** and **Figure 3**, while retaining historical Tables 1–3 and Figure 1.
- Separate **Supplementary File S2** with all 48 target-level rows, 11 category rows, exactly three ambiguity cases and all eleven target-wise random AUC comparisons. Original Supplementary S1 is not edited.
- New cover-letter draft and **five editable Highlights** of at most 85 characters each.
- A verified primary comparison to **Andrés, Martínez-Seras, Laña and Del Ser (2024)**, *Results in Engineering*, 24, Article 103498, https://doi.org/10.1016/j.rineng.2024.103498. This paper introduces D-MFPP, while ours evaluates specific matched-grid spatial rank consistency; no invented head-to-head comparison.

## 4. Reliability and publication limits

**Numeric/structural QA:** V38-B independent full JSON / JSONL QA passed. The V38-C scientific figures were generated directly from the audited JSON, at **300 dpi** with filenames `artwork/Figure_2.png` and `artwork/Figure_3.png`. Word versions of the manuscript, S2, Highlights and cover letter are programmatically generated; the manuscript and S2 are rendered to PDF and checked for core numeric anchors. A human final submission-layout scan and the author's substantive review remain requirements.

**Outstanding author/editorial sign-off:** correct names/order and full postal address, corresponding author, CRediT/funding/competing interests/originality/AI-assisted writing disclosures, journal rights and lawful privacy basis for identifiable workers, exactly which images may be shown or redistributed, journal latest formatting and figures' final physical sizes, DOI/reference checks, final Word visual QA and portal metadata. No author-signed declaration or journal submission is claimed.

**Judgment:** The enriched experiment materially strengthens the manuscript's diagnostic evidence, especially its independent random-order and occlusion-fill *controls* and its transparent ambiguity accounting. The study is still a development-exposed **internal engineering XAI diagnostic**, not a validated safety-compliance system or an independently site-generalizable causal attribution method. Scientific evidence strengthening V38-C is **complete as a draft-stage integration**, subject to editorial and author release gates.

**Original result evidence:** https://github.com/EZZALDEEN049/Y-PPE-Detection-RFDETR/actions/runs/45085935253  
**Independent numerical audit:** https://github.com/EZZALDEEN049/Y-PPE-Detection-RFDETR/actions/runs/45088345895

## 5. V38-C final derived-artifact QA outcome

The completed [V38-C GitHub Actions Word/artwork pipeline](https://github.com/EZZALDEEN049/Y-PPE-Detection-RFDETR/actions/runs/45089949225) returned success and committed the **exact-data 300-dpi Figure 2 and Figure 3**, the updated editable 13-page manuscript Word file, the 5-page landscape-A4 Supplement S2 Word file, the separate editable cover-letter draft, and the **five separate editable Highlights bullets** (all under 85 characters including spaces).

The source DOCX files were rendered to PDF and visually reviewed using whole-document page contact sheets. Independent PDF block-boundary checks found **zero text boxes outside either document's page boundaries** (13 A4 portrait manuscript pages and 5 A4 landscape supplement pages). Manuscript contains **five editable tables and three figures** in the verified conversion. The landscape supplement retains table editability and repeating first-row headers. This is a technical/editorial layout review and does **not** replace the author's final review of all proof pages and institutional/permission declarations.

The reference and manuscript version cited in Section 3 include the independently verified 2024 Andrés et al. target-journal paper. Source V26–V37 data and the full V38-B JSON/JSONL evidence were not modified during these build steps.

**Stage V38-C:** Scientific numbers/graphics/editorial drafts prepared and technically reviewed. **Journal submission is still NOT performed**, and the author-approval/privacy/originality gates remain open.

