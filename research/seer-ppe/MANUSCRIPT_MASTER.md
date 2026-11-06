# SEER-PPE: Safety-Constrained, Energy-Aware, and Evidence-Grounded Explainable Vision for Occupational Safety Monitoring

**Working manuscript v0.4 — 6 November 2026**  
**Article class:** original empirical research candidate | **Status:** Methods draft; **NOT a validated empirical article or Q1-ready**  
**Data constraint:** original Y-PPE only; author-managed dataset and legacy ALTAYYAR 17-class RF-DETR Small checkpoint.  
**Draft integrity statement:** all planned findings remain unmeasured; do not cite the old model's 96.22% historical mAP@50 as a new SEER-PPE achievement.

## Abstract — structured proposal, NOT journal-ready results abstract

**Background:** PPE object detectors have demonstrated high localization accuracy in construction imagery, but detection accuracy alone does not address the computational expense or faithfulness of explanations, the uncertainty surrounding worker-level PPE decisions, or the workload imposed by requests for human review. **Objective:** This work proposes SEER-PPE, a post-detection evidence-routing framework designed to evaluate whether additional explanation computation can be allocated selectively while preserving prespecified worker-level safety requirements and evidence fidelity. **Methods (planned):** The study uses the author-developed 17-class Y-PPE image collection, a previously trained RF-DETR Small baseline, independent worker-level annotations on Y-PPE images, matched-object perturbation tests for explanations, measured power traces on declared hardware, and source-group-independent split controls. Candidate policies include detector-only, explain-all, confidence-based explanation, matched-review routing, energy-only routing and a jointly constrained policy. **Results:** PENDING — NO SEER-PPE quantitative experimental results. Historical model metrics are described exclusively as prior evidence. **Conclusion:** The empirical contribution and any efficiency benefit will be determined after image-independence, human-annotation, local-XAI and energy-metering gates pass.

**Keywords:** occupational safety; personal protective equipment; explainable AI; RF-DETR; energy-aware inference; computer vision; worker-level risk; Y-PPE.

## 1. Introduction — working draft

Construction-safety inspection increasingly benefits from computer vision models that can locate safety helmets, protective vests, gloves, and other equipment. Such detection systems are useful for screening complex sites, but a detector output alone does not verify a worker's compliance with the specific protective-equipment requirements of the assigned task. Moreover, a model can produce highly confident detections without identifying the visual evidence that made those detections reliable, while computing an elaborate explanation for every detection may impose costs that are material in resource-constrained deployment.

The researcher's earlier Y-PPE programme established a 17-class image corpus and evaluated RF-DETR Small for PPE and scene-related object detection. The original corpus comprises 2,327 images and 16,520 object annotations; a Roboflow training version generated 5,577 images after train-only augmentation. A historical RF-DETR evaluation reported mAP@50 of 96.22%. Those results demonstrate a foundation for this work and have already been disseminated in prior research; they are not proposed as new findings here.

SEER-PPE examines a distinct question: whether a deployed PPE detector can select the appropriate level of additional visual explanation or human review by balancing the energy expenditure of additional computation, the actual behavioral fidelity of the explanation, and the risk of incorrectly dismissing an eligible worker's PPE violation. Crucially, this question requires not only machine-generated boxes but also explicit, independently adjudicated worker identities, PPE-wearing status, image visibility, and the requirement of PPE for the particular task or site. Without this context, a `No Hard Hat` box is not sufficient proof of an occupational safety violation.

The proposed framework does not treat post-hoc saliency heatmaps as verified explanations. Attribution quality must be tested for the relevant detected instance using target-matched perturbation and stability analyses. Likewise, energy awareness requires actual electric power measurements on named hardware, not proxy estimates based on FLOPs. Human review remains an abstention/request and cannot be counted as a successful safety intervention unless a subsequent independent outcome is measured.

This study tests, rather than presumes, three possible contributions: (i) a safety-aware adaptive routing policy for additional evidence computation, (ii) a matched-instance explanation fidelity gate integrated with PPE-specific worker evidence, and (iii) a reproducible joint analysis of measured energy, verified worker-level decision errors, and review demand. Each claim is subject to a baseline comparison and a defined experimental gate.

## 2. Relation to previous work and literature — partial, verification pending

### 2.1 Author's prior publications

- Al-Tayar et al., *AI-Driven RF-DETR Decision System for Real-Time PPE Monitoring in Yemen's Development Projects* (IEEE, 2025), DOI: https://doi.org/10.1109/DASA68193.2025.11499131 — original detector and performance; **not new SEER experiments**.
- Al-Tayar et al., *X-RF-DETR: A Framework for Explainable and Trustworthy PPE Decision Support* (IEEE, 2025), DOI: https://doi.org/10.1109/DASA68193.2025.11498849 — prior XAI framework with preliminary 300-image evidence; the new study must add measured energy, independent worker truth and executed routing comparison.
- Al-Tayar et al., *PPE Detection in Yemeni Construction Sites: YOLOv11m vs. RF-DETRs* (IEEE, 2026), DOI: https://doi.org/10.1109/ESMARTA70636.2026.11652190 — prior architectural comparison; not to be replicated as novelty.
- Al-Tayar et al., *BIM-Integrated Explainable Vision for Real-Time PPE Safety in Yemen's Construction Sector* (IEEE, 2026), DOI: https://doi.org/10.1109/ESMARTA70636.2026.11652079 — prior selective explanation and integration concept; does not by itself establish SEER's energy–safety constrained policy empirically.

### 2.2 External methods and novelty boundary

General explainable AI, post-hoc attribution, selective routing, and risk calibration have existing literatures; none alone will be labeled a new algorithm. Relevant anchors include Wu et al. (CVPR 2024) on faithfulness of ViT explanations; prior energy measurement and PPE association approaches. A complete 2024–2026 bibliographic collision matrix remains **PENDING**; no claim of global priority is made. Official RF-DETR checkpoint documentation: https://rfdetr.roboflow.com/latest/learn/train/ .

## 3. Materials and Methods — preregistration candidate, NOT executed validation

### 3.1 Image corpus and dataset integrity

The input is Y-PPE only. The raw 17-class Roboflow corpus contains 2,327 images (1,625 training, 468 validation, 234 original test) and 16,520 labels. Roboflow Version 2 applied auto-orientation, stretch resizing to 640×640 and train-only mosaic expansion to 5,577 processed images (4,875/468/234). The historical fixed detector is the platform's 17-class `altayyar-0oflt-lafos-qqauz/2` RF-DETR Small model.

For new experiments, the candidate 17-class cleaned source is documented as 2,288 images and 16,300 labels (1,595/459/234). The existence of a successful September 2026 stage-2 audit does not substitute for verifying the actual archive, image hashes, source/camera/video acquisition groups and visually adjudicated scene-level overlaps. A later 1,778-image **nine-class** derivative underwent a different October audit that reopened an independence gate; its status must not be silently attributed to the 17-class candidate. A clean, unexposed SEER final-test partition will be defined before parameter selection, which may require reorganizing original Y-PPE images by acquisition family.

### 3.2 Worker-level safety reference

Independent safety reviewers will annotate every relevant person present in audited frames, including persons the detector fails to locate. Worker-versus-bystander role, specific PPE requirement and documented task-policy provenance, equipment worn status, occlusion, person–equipment association and ambiguity will be separately recorded. A violation is defined only when the role, PPE mandate and non-wearing condition are independently verified. Ambiguous/unknown cases are reported separately; neither the class name `No Hard Hat` nor culturally specific dress automatically establishes a violation. See `ANNOTATION_CODEBOOK.md`.

### 3.3 Target-specific explanation validation

The chosen detector output is associated with a target class and bounding box. A real explanation experiment will perturb pixels or regions and run the detector again. Targets will be matched to the same class and bounding-box region using original-image-coordinate IoU. If no matching detection persists, record `LOST` rather than treating the detection as score zero; if two detections match equally, record `AMBIGUOUS`. The new implementation includes this identity safeguard, but no real explanation was yet produced. Localization in a reference ROI, deletion-induced score variation, insertion effects, stability and failure rates will be reported once actual attribution is available.

### 3.4 Routing and decision states

Routing actions are `BASIC`, `EXPLAIN` and `REVIEW`. The runtime policy uses only input-visible evidence and separately verified runtime PPE rules, never post hoc adjudicated labels. `REVIEW` is a request, not evidence that a hazard was fixed. Base detector energy is incurred on all routes; any possible savings arise from skipping *additional* XAI computations. All routes must account for completely missed workers in offline scoring.

### 3.5 Multiobjective optimization

Let `pi` select additional evidence computation conditional on runtime-visible features. The planned objective is to minimize mean measured `E_detector + E_XAI(pi)`, subject to **preselected** bounds on false-clearance `R_FC`, uncontained violations `R_UC`, explanation evidence fidelity `F`, and reported human-review workload `H`. These constraints require independent ground truth and may be impossible to certify on a rare class; infeasibility or uncertainty will be published transparently. Neither synthetic energy traces nor mathematical example bounds are actual outcomes.

### 3.6 Matched baselines and evaluation

Compare against detector-only, explain-all, confidence-only explanation, matched-review budget, energy-only routing, and the full SEER policy. Keep detector weights, input population, hardware, and label policy consistent. Select method and thresholds on development/calibration splits only; perform locked final-test evaluation once. Report joules/image, joules/eligible worker, confidence intervals for worker risk with source-family dependence acknowledged, localization and target-matched behavioral faithfulness, review fraction and latency distributions.

### 3.7 Engineering validation status as of v0.3

Roboflow hosted inference succeeded on three existing Y-PPE images, solely as connectivity/output-shape proof. The historical test sample used in that pilot is now development-exposed and cannot constitute untouched final-test evidence. An authorized checkpoint URL was issued but the checkpoint has **not** been locally loaded and verified for gradients; the present container has CPU-only PyTorch. No energy sensor readings or independently adjudicated worker-level labels were generated. The Python research utilities have **40 passing synthetic unit tests**, including 17 newly added checks for split independence and target identity; such tests cannot establish research efficacy.

## 4. Results — intentionally empty pending real evidence

**PENDING — NO NEW SEER-PPE EMPIRICAL RESULTS.** Table R1: cleaned dataset and group-independence audit. R2: worker GT coverage/agreement. R3: explanation identity/fidelity vs baselines. R4: measured energy and latency with hardware scope. R5: final-test risk and selective coverage with uncertainty. Figure R1: experiment workflow. Figure R2: risk-energy frontier. Figure R3: target-matched explanation perturbation curves. All figures/results to be created only after corresponding experiments.

## 5. Discussion — questions, not claimed findings

The eventual discussion will address whether routing demonstrably reduces additional compute energy without intolerable safety errors, whether explanations are faithful rather than merely plausible, and which constraints cannot be supported by the available Y-PPE evaluation population. Claims of real-world incident reduction, deployability on arbitrary hardware, universal safety guarantees, and global generalization are outside present evidence.

## 6. Limitations, provenance, ethics and data availability

Y-PPE uses field images and supplementary third-party repository content. The author owns their original compilation, annotations and original contributions subject to other parties' image rights; public image redistribution rights must be audited separately. Historic source attribution and permissions are not presently resolved at per-image level. An identifiable site/worker image is not published in this project package. No outside image corpus is added. Model and data licenses, dataset lineage, source-related leakage and protected evaluation data will be reported in any submission.

## 7. Next canonical update target — v0.4

Update **this same file** after actual 17-class cleaned archive/manifest verification and human annotation pilot. Populate Methods 3.1–3.2 with verified counts, report reviewer agreement and source-family sampling. Results remains explicitly empty until legitimate experiments. Amend `PROTOCOL_MASTER.md`, append `CHANGELOG.md`, and record evidence paths in `PROGRESS.md`.


## Appendix A. Phase 4 Data Readiness and Adjudication Pilot — engineering evidence (6 November 2026)

The full current Roboflow **original** Y-PPE metadata index was read: 2,327 unique image IDs across 1,625 train, 468 validation, and 234 original test. The original test contains 104 images with a `Persons` object label and only 16 images with a `No Hard Hat` object label; these are **not worker-level confirmed violations**. Thirty deterministically sampled development images (16 train, 14 validation) from five deliberately enriched strata were read at saved-annotation level. The 30 records contained 396 object boxes; all passed basic geometric bounds checks. Eighty-nine boxes included `RFBoxPrompt/v1` model-assistance metadata; the extent of any later human verification is unknown. No human adjudication has been conducted for SEER-PPE.

The historical 2,288-image, 16,300-box 17-class corrected Y-PPE derivative remains the **candidate experimental archive** and is **not newly file-hash verified** in this phase; local binary access was unavailable. Thirty-one exact filename-string groups spanned raw dataset splits, including ten involving the original test split. Filename collisions are flags for inspection, not proof of scene leakage. Per-image source-family identifiers and source rights were absent from Roboflow's original image metadata, so true source-group independence cannot yet be certified. The 30-image stratified development review queue is provisional pending membership, rights, and source-family checks.

No SEER-PPE empirical performance, worker-level risk, explanation-fidelity, or energy metric has been measured. The journal Results section remains reserved for correctly preregistered and actually completed experiments. See the versioned companion `PHASE4_REPORT.md`, `ANNOTATION_REVIEW_PROTOCOL.md`, and `evidence/PHASE4_INDEX_AUDIT_2026-11-06.json`.
