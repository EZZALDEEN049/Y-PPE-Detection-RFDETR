# EcoSafe — evidence-grounded novelty and related-work screening (2026-10-18)

**Status: targeted, non-systematic literature screening, NOT a completed systematic review, novelty certificate, journal-Q1 determination, or evidence of independent held-out superiority.** Search date: 2026-10-18. Primary journal/publisher/conference, lab and official benchmarking pages were checked. Keep all results from separate tasks, datasets and metrics **non-comparable** with EcoSafe's frozen fixed-IoU safety-object counts.

## Candidate research question (framed to match actual evidence)

> When do frozen domain-specialized PPE detectors supply *additional matchable violation objects* beyond the stronger primary detector, and how do checkpoint selection, domain shift and false-positive burden alter the *conditional value of invoking a second expert*?

This differs substantively from demonstrating a new reliable or low-carbon operational cascade. Explicitly separate (i) GT-privileged retrospective oracle, (ii) prospective primary-only router, (iii) checkpoint policy chosen during original training, (iv) absolute safety performance, and (v) actual instrumented energy.

## Source-screening matrix

| Reference / stable original source | Relevant prior contribution | Consequence for EcoSafe's novelty claim | Still needed |
|---|---|---|---|
| Lebovitz, Cavigelli, Magno & Müller, *Efficient Inference with Model Cascades*, **TMLR 2023**. https://mlanthology.org/tmlr/2023/lebovitz2023tmlr-efficient/ | Conditional execution among pretrained models, confidence threshold versus compute/accuracy tradeoffs; reproducible baselines. | **Never claim invention of pretrained two-model conditional cascades or confidence deferral.** Our distinct empirical unit is class-aware safety-object recovery and FP burden under PPE domain shifts. | Compare actual two-expert fusion vs switching and costs under common execution semantics; our current confidence gate fails. |
| Rabanser, Rauschmayr, Kulshrestha et al., *I Know What I Don't Know: Improving Model Cascades Through Confidence Tuning*, **2025**. https://research.google/pubs/i-know-what-i-dont-know-improving-model-cascades-through-confidence-tuning/ ; arXiv:2502.19335 | Learns to improve deferral/calibration in model cascades across classification, text and vision-language settings. | **Never claim confidence-only/learned routing calibration novel in general.** Our retrospective AUC is not evidence of a deployable equivalent. | Verify final proceedings venue; any learned route must be evaluated independently with leakage-safe fitting. |
| Pathiraja, Gunawardhana & Khan, *Multiclass Confidence and Localization Calibration for Object Detection*, **CVPR 2023**, pp. 19734–19743. https://openaccess.thecvf.com/content/CVPR2023/html/Pathiraja_Multiclass_Confidence_and_Localization_Calibration_for_Object_Detection_CVPR_2023_paper.html | Object-detection confidence and localization can be miscalibrated in/out of domain. | A low \`1-max(safety_confidence)\` AUC is consistent with the *need to examine detection calibration*, but our diagnostic does **not establish** the mechanism of miscalibration. | Add calibration/reliability metrics only if defined as a distinct validation analysis; not infer causal mechanism from AUC alone. |
| Ahmad & Rahimi, *SH17: A dataset for human safety and personal protective equipment detection in manufacturing industry*, **Journal of Safety Science and Resilience**, 6(2), 175–185 (2025). DOI: https://doi.org/10.1016/j.jnlssr.2024.09.002 | 8,099 annotated images / 17 classes, PPE detection benchmarks and cross-domain validation. | **Do not claim PPE cross-domain benchmarking or a 17-class dataset is unprecedented.** Our study has two separately harmonized nine-class private frozen datasets with different support. | Clarify dataset licensing/rights, class ontology and scene/source independence; do not substitute SH17 metrics for EcoSafe's evaluation. |
| Seong, Kim & Jung, *Improving cross-site generalization in construction object detection via hard negative mining*, **Automation in Construction**, 182:106761 (Feb 2026). DOI: https://doi.org/10.1016/j.autcon.2026.106761 | Cross-HNM assessed across 11 construction sites and five unseen sites; single-model inference without ensemble-time overhead. | **Do not claim first construction cross-site object-detection method, or that adding experts is a preferred architectural remedy.** This is a strong methodological alternative with better site-group evidence. | Explain no verified site IDs in our frozen manifests; do not compare its mAP to our fixed-confidence TP recall. |
| Barz & Denzler, *Do We Train on Test Data? Purging CIFAR of Near-Duplicates*, **J. Imaging**, 6(6):41 (2020). DOI: https://doi.org/10.3390/jimaging6060041 | Near-duplicate images can invalidate apparent held-out performance; demonstrates the need for deduplication. | Exact hash and 64-bit dHash scans are only **preflight**, not proof of source independence or a valid held-out test. | Seek scene/site/video provenance and freeze grouping before touching a final test. |
| MLCommons, *MLPerf Inference Power Measurement Rules*, official project policy. https://github.com/mlcommons/inference_policies/blob/master/power_measurement.adoc | Full-system wall-power measurement and paired performance/power logging; replicable measurement principles. | **Fewer expert calls ≠ measured energy savings.** Do not use estimated accelerator TDP as measured energy. Do not call an informal experiment MLPerf-compliant. | Arrange an authorized system power meter/validated telemetry and matched repeat runs before reporting J/image or CO2e. |

All bibliographic metadata above should be checked again at final submission; journal ranking is not asserted. Earlier working manuscript cited the first four but lacked a systematic comparator map and incorrectly placed PPE/domain-shift novelty as potentially broad. This screening narrows the claim deliberately.

## Claim-to-evidence decision table

| Proposed statement | Current status |
|---|---|
| Six immutable YOLO11m last.pt experts evaluated on both original validation domains with three seeds; best.pt treated separately | **SUPPORTED on DEVELOPMENT** by existing hash-locked reports. |
| Safety-object complementarity depends on source domain and checkpoint policy at a fixed confidence threshold | **DESCRIPTIVELY SUPPORTED on DEVELOPMENT**, unconfirmed on independent sites. |
| Positive GT recovery from activating secondary is very sparse for best.pt, especially on Y-PPE | **DESCRIPTIVELY SUPPORTED**, GT-privileged retrospective labels, no deployable selector. |
| Safety-only maximum-confidence uncertainty weakly identifies these recoveries on Construction in the observed split | **DESCRIPTIVELY SUPPORTED**; rare positive counts, source-selection bias and no independent route validation. |
| Calibrated new router can find most beneficial frames without seeing GT | **UNPROVEN**: no learned calibrated prospective router and no held-out test. |
| EcoSafe is safe for site deployment, has sufficient critical-class recall or acceptable FP rate | **NOT SUPPORTED**: majority of violations missed even under best checkpoint and FP tradeoffs severe. |
| EcoSafe measurably reduces electricity, J/image, emissions, or is lower-carbon | **NOT MEASURED**: invocation proxy only. |
| EcoSafe is the first conditional multi-expert detector / Q1-ready contribution | **NOT SUPPORTED**: prior cascade and domain-generalization work exists; novelty and journal fit require independent scholarly assessment. |

## Defensible contribution wording for a limitations/audit manuscript

> "We present a reproducible, safety-object-level audit of the conditional value of a second frozen PPE detector under checkpoint selection and domain shift. By separating class-aware operational fusion from GT-privileged oracle recovery, we document when extra expert invocation yields additional violation matches, the accompanying false-positive costs, and the limitations of primary-only confidence ranking on two development domains. We report negative findings, source-dependence limitations and unmeasured energy explicitly."

This is a **candidate framing**, not a positive algorithm/energy claim or demonstrated Q1 novelty. It will become suitable for submission only with an ethically cleared, non-leaky independent evaluation and adequate contribution beyond this descriptive diagnostic.

## Reproducible screening notes

Original/publisher webpages accessed 2026-10-18. We did not run a bibliometric database search across Scopus/Web of Science/IEEE Xplore and did not establish exhaustive novelty. No test data, private images, original camera IDs, or sensitive checkpoint binaries were shared in this public research note.
