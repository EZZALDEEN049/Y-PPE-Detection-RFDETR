# Author declarations and data availability — fact-checked DRAFT

**This is an editorial template, not an author-attested submission statement. All assertions about grant support, approvals, conflicts, photographs and individual author contributions require confirmation from the actual authors.**

## Data availability (working safe wording)

The Y-PPE research source is the Roboflow **ALTAYYAR Version 2** object-detection dataset, and the Construction-PPE source is **Ultralytics Construction-PPE v1.0.0**, whose published dataset record describes AGPL-3.0 terms. The studied nine-class derivatives were reconstructed using documented source-data cleaning and conservative annotation-based exclusion procedures that reduce the original test populations before Stage 5 training; the training, validation and test frozen manifest SHA-256 and counts are specified in `docs/DATASET_SOURCE_LINEAGE_AND_TEST_SELECTION_2026-10-18.md`. The repository includes scripts and aggregate analysis/figure input data, while underlying source photographs, per-person identifiable image details, raw source model checkpoints and original per-image output files are not redistributed by this project. Access to the original dataset versions remains subject to their actual publisher/version rights and authentication policies. **The author must verify the exact Roboflow Version 2 license before submission**, since the earlier Version 1 license does not automatically establish Version 2 conditions. A source-download link is not a grant of unlimited republication rights.

Any newly acquired public external robustness cohort would be separately versioned and credited; **no new external test dataset has been downloaded or scored in this paper draft**.

## Code availability (working safe wording)

Public research code, frozen evaluation logic, synthetic unit tests, and aggregated Figure 1/2 data are available within the EcoSafe Selective Experts research branch of https://github.com/EZZALDEEN049/Y-PPE-Detection-RFDETR, currently under draft PR #16. The article must cite a **specific immutable commit or released archive at actual submission**, not a moving branch or draft PR. Some full experimental reproductions require downloading the original source datasets and preexisting weights under their access terms.

## Original data rights / research ethics (REQUIRES REVIEW)

The project researcher has confirmed that the images are normally used for academic research. A publicly shared original photograph, and especially identifiable worker imagery, may require additional source-specific publisher and human-subject privacy permission. No committee approval number, informed-consent register or waiver declaration was provided in this conversation; **do not invent** one. Publisher and institutional requirements for original image examples, source reuse and personnel consent must be resolved with the qualified data steward before any photos are reproduced in submitted figures. The current plotted figures use aggregate counts only.

## Funding (PLACEHOLDER)

**[All authors must confirm actual grant support, institutional support or the absence thereof, including sponsor name, award number and funder role. Never assert “no external funding” automatically.]**

## Conflicts of interest (PLACEHOLDER)

**[Each author must declare actual financial/nonfinancial relationships and any links with dataset providers, employers, equipment suppliers or funding bodies. Do not auto-assert “no conflicts.”]**

## CRediT authorship (PLACEHOLDER)

**[List only real authors and their verified roles in conceptualization, data curation, methodology, formal analysis, investigation, software, writing original draft, writing review/editing, visualization, supervision and funding acquisition. Do not invent names, affiliations, email addresses or contributions.]**

## AI-assisted writing disclosure (AUTHOR REVIEW)

AI tools may have assisted preparation of the working language and technical editing. The authors must verify the **actual use**, accept accountability for all text/citations/experiments, and disclose AI-assisted writing where required by the selected publisher's current policy. AI tools are not listed as authors. Do not assert an AI tool generated original empirical measurements; all figures/analysis must be traceable to original locked aggregate values.

## Prior overlapping manuscript disclosure (MANDATORY)

A separate **Cross-Domain Reliability of YOLO11m for Safety-Critical PPE Monitoring** manuscript previously evaluated the **same Stage 5 detector weights and test images** for model-only reliability, including final-epoch and separate best-epoch sensitivity. The proposed EcoSafe paper has a distinct question about conditional activation/fusion and class-aware marginal violation recovery, but shared methods, source data and previous known test outcomes MUST be disclosed to editors and overlap checked to avoid redundant/salami-sliced publication. Report the previous manuscript's actual submission/publication status accurately after author verification; do NOT claim publication or acceptance based only on a working committee draft.

## Statement of nonclaims

No newly independently confirmed field worksite evaluation, universally safe violation recall, validated per-class safety lower bound, measured joules per image, verified lower CO2e or Q1 journal decision exists for the present EcoSafe manuscript. Do not replace these missing scientific results with editorial declarations.

**Sign-off gate:** [corresponding author] [all co-authors] [source rights steward, if needed] [institutional ethics reviewer, if applicable]. All signatures/approvals PENDING.
