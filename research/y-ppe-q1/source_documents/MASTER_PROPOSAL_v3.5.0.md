---
project: Y-PPE thesis-to-Q1 original article
canonical_document: true
version: 3.5.0
updated: 2026-11-22
status: Working research proposal; not a completed article
editorial_stage: Q14 conditional within-dataset subgroup protocol approved; real-data audit, trained models, subgroup analysis and results remain frozen
supersedes: Proposal Version 1.0; intermediate working ideas (Version 2.0)
---

# From Aggregate Accuracy to Safety-Relevant Reliability
## A Provenance-Audited and Uncertainty-Aware Evaluation of RF-DETR on the Y-PPE Dataset

**Master research proposal | Version 3.5.0 | 22 November 2026**

**Article type:** Original research, conditional upon genuinely new empirical work and a defensible literature gap.  
**Study status:** Protocol and contribution boundaries revised; no new model results are claimed.  
**Data policy:** Use the pre-existing Y-PPE images only, unless the research scope is formally revised and all restrictions are documented.  
**Editorial rule:** Previous thesis and conference results are historical evidence, not results of the proposed new experiments.

## 1. Executive abstract (prospective)

Computer-vision detectors for personal protective equipment (PPE) monitoring are commonly assessed using aggregate object-detection metrics. Previous work on the Y-PPE dataset established its 17-class annotation scheme, evaluated RF-DETR Small, and reported a comparison against YOLOv11m. Yet these studies do not, on the material presently available, establish a fully auditable image-acquisition provenance record, independently verified scene-level separation between evaluation partitions, or a joint analysis of uncertainty in safety-relevant class estimates. This study therefore proposes a provenance-aware, uncertainty-aware **reassessment**, not a new detection architecture. It will first reconstruct dataset lineage and investigate exact duplication, near duplication, and scene-level dependencies. If reliable group identifiers and an admissible protocol can be established, RF-DETR Small and YOLOv11m will be reevaluated on a prespecified partition with held-out group separation. Model-specific threshold selection will be restricted to validation data. The primary descriptive evidence will consist of class-specific missed annotated detections (FNR) **together with** spurious detections for missing-PPE classes per evaluated image (FPPI), with paired uncertainty intervals; conventional precision/recall and mAP remain supporting metrics. Conditional subgroup analysis will be limited to apparent object scale derived from existing boxes and other conditions already present in verified source metadata; no new visual labels are authorized under the current annotation policy. Computation and memory profiling on the same hardware will be conducted only if reliable measurement resources are available. The study will test whether prior interpretations remain stable under stronger evaluation controls, and will report null results and limits of inference explicitly. No model advantage, data-leakage event, operational harm reduction, or journal acceptance is presupposed.

**Keywords:** PPE detection; RF-DETR; Y-PPE; data provenance; partition independence; false-negative rate; statistical uncertainty; responsible evaluation.

## 2. Established results and explicit non-novel contributions

The thesis and previous author-provided papers established the Y-PPE dataset, the RF-DETR Small evaluation, the YOLOv11m comparison, interpretability/decision-support concepts, and a BIM-assisted governance framework. These outputs must be cited and acknowledged. Introducing RF-DETR, publishing Y-PPE, calculating mAP on the historical test split, visualizing attention/Grad-CAM, and combining BIM with AHP–TOPSIS cannot be claimed as new contributions in this manuscript.

**Prior published results as source-reported, not independently replicated:** Y-PPE raw corpus: 2,327 images, 16,520 annotations, 17 classes; raw splits: train 1,625, validation 468, test 234. A historical 2026 comparison reports RF-DETRs mAP@50 96.2%, mAP@50:95 64.3%, precision 95.2%, recall 93.4%; YOLOv11m mAP@50 92.9%, mAP@50:95 74.9%, precision 96.9%, recall 92.1% on the cited test split [S1, S4]. The numerical differences do not support declaring an absolute winner.

The supplied Version 1.0 proposal also *describes* a derivative set containing 2,288 images and 16,300 annotations (train 1,595, validation 459, test 234). This derivative has **not** been checked against source image/annotation files in the present review. Arithmetic is consistent: 2,327 − 2,288 = 39 images and 16,520 − 16,300 = 220 annotations, with 30 training and 9 validation images removed, and no change in test count. This is not proof of data independence.

### 2.1 Source reconciliation items requiring verification

- **Annotation taxonomy:** Thesis Table 3.1 lists 17 labels including `No Safety Attire`, but §3.2.5 discusses a purported `abaya` class. This must be reconciled against actual class-index files, label manifests, and image-level ground truth before any new claim about class semantics. The text alone cannot establish which description was used in training [S1].
- **Metric operating points:** Thesis Table 4.1 reports RF-DETR validation F1 = **91.1%**, whereas the validation threshold-optimized point in §4.3.1 reports **91.9%** at 0.48. These are explicitly different operating contexts, not demonstrably contradictory numbers. The 2026 paper reports validation F1 **91.9%**; its exact threshold/protocol must be aligned with the thesis logs before treating the figures as equivalent [S1, S4].
- **Compute and augmentation claims:** A 2025 paper describes an NVIDIA T4 and >100 FPS, while the 2026 comparison notes that no controlled same-hardware latency benchmark was exported. These can reflect different measurement settings; neither establishes a new reproducible latency result [S3, S4]. Report platform, software version, precision, batch size, preprocessing, synchronization, warm-up, and latency quantiles before making real-time or low-resource claims.
- **Data lineage:** Thesis §3.2.2 identifies field photos acquired with site partners and supplementary public repository images, which motivates provenance metadata and differentiation of local and external image origins [S1].

### 2.2 Platform metadata verification — new evidence (04 November 2026)

The public Roboflow project `softyyemen/altayyar-0oflt-lafos-qqauz` was inspected through read-only project, version, training and model-evaluation records [S8]. It currently reports 2,327 images, 17 classes (including `No Safety Attire` but no class named `abaya`), and 1,625/468/234 split counts. Platform versions **1** and **2** each list **5,577 exported images** (4,875 training, 468 validation, 234 test) with 640×640 stretch, auto-orientation and three image versions with Mosaic; version **3** lists **2,327 images** (1,625/468/234), 640×640 stretch and no linked training in the retrieved record. Matching split *counts* do not prove matching identities or source independence.

Training metadata records finished `rfdetr-small` runs for versions 1 and 2. The version-2 training summary reports map50 **93.97%**, precision **94.36%** and recall **88%**, aligning after rounding with the historical validation figures. More importantly, the version-2 evaluation record `KyzP9neuyNTN5eQpGCAY` reports platform `mAP` **0.9622053873**, precision **0.952**, recall **0.934**, F1 **0.942**. These figures align, after rounding, with the published **96.2%, 95.2%, 93.4%, 94.2%** headline test figures. This is now a **source-of-results audit**; it is not an independent recomputation of scores from predictions, and the platform API field `mAP` must not be silently assigned an exact IoU definition without the evaluation configuration.

A distinct 2,288-image / 16,300-label derivative was **not among the three returned public platform versions**. It may still exist separately; no conclusion on its availability or integrity is justified. A version-3 YOLOv8 export subsequently reached `ready=true` in Roboflow, but the working container could not fetch its archive because outbound DNS/network access failed. No image bytes were obtained, so no file- or scene-level audit has been performed. Consequently **raw file hashes, potential train/test scene duplication, label quality and model-checkpoint test exposure remain unverified**. The next stage is restricted to those tangible file-level questions.

## 3. Problem statement and scientific gap

High aggregate AP does not, by itself, identify uncertainty in class-specific missed detections or show whether benchmark images are statistically independent at the acquisition-scene level. The *within-project* gap is a missing documented link between provenance-verified sampling, explicit uncertainty in annotated violation classes, and interpretation of RF-DETR versus YOLOv11m rankings. This is a **provisional** scholarly gap: external novelty must still be assessed using a documented, updated literature search and a target-journal scope check. Audit techniques themselves are established; the potential contribution lies in new, traceable evidence on this dataset and a transparent evaluation protocol.

The study is not positioned as a proof of legal PPE compliance, reduction of accidents, fairness across demographic groups, or generalization to all Yemeni and international sites. Those would require additional ground truth, sampling, and study designs.

## 4. Research objective and questions

**Primary objective:** Determine whether the previously published interpretation of RF-DETR performance on Y-PPE remains warranted when image-source dependencies, both missed and spurious detections in annotated missing-PPE categories (FNR and FPPI), and statistical uncertainty are explicitly addressed.

- **RQ1 — Data provenance:** What exact, near-duplicate, and acquisition-scene dependencies can be established across Y-PPE training, validation, and test partitions; and, if a defensible group-separated partition is feasible, how does reevaluation under that partition affect performance estimates?
- **RQ2 — Reliability:** What paired missed-detection (class FNR) versus spurious-detection burden (violation FPPI) is observed at validation-derived operating points; how uncertain are these estimates; and, only where supported by existing verified fields or mechanically derived reference boxes, how do patterns vary across prespecified classes, apparent object scale and documented image/acquisition conditions?
- **RQ3 — Comparative inference:** Under common test images, explicit validation-derived operating points, and paired uncertainty analysis, do RF-DETR Small and YOLOv11m support the same deployment-oriented conclusions as their prior aggregate metric ranking?
- **Supporting question — Computational feasibility:** On a specified common inference system, what are the measured time, throughput, and memory requirements of the relevant models? This will not become a central claim unless an appropriate setup is available.

## 5. Testable propositions and null outcomes

**P1:** If the source audit identifies cross-partition dependency and a valid alternative group split is feasible, evaluation estimates under the revised split may differ from historically reported values. Null outcome: no documented dependency, or no substantive difference. If group identity cannot be reconstructed, report this limit without claiming split independence.

**P2:** Estimates for low-support annotated violation categories will be accompanied by uncertainty intervals that may preclude precise operational ranking. Report class support and interval width rather than forcing statistical significance.

**P3:** Paired comparison on identical images may reveal trade-offs among mAP, false-negative rates, and strict localization, rather than a universal model winner. The null outcome is a stable ordering under all prespecified criteria.

**P4 (conditional):** Standardized hardware profiling may reveal different quality–latency trade-offs. Do not claim a real-time property from historical or cross-platform FPS values.

No hypothesis assumes that data leakage exists or that RF-DETR is the superior model.

## 6. Primary experimental protocol

### Phase A — Source inventory, provenance and leakage audit

1. Freeze a copy of every *raw* image and annotation file (read-only) and record dataset-version information, file counts, file sizes, dimensions, label schema, label mapping, and hashes.
2. Assign durable `image_id`, `origin_type` (field / supplementary repository / unknown), `source_uri_or_code`, `site_id` when documented, `capture_session_id` or `sequence_id` when documented, original split, annotation version, and review status. Unknown is a legitimate value; do not infer acquisition origins from appearance.
3. Identify exact duplicate bytes with SHA-256, and identify near-duplicate candidates using perceptual hashes and/or image embeddings, followed by manual adjudication. Similarity score alone is not proof of duplicate provenance.
4. Inspect cross-split pairs and related frames. A pair shall be marked as `confirmed_same_scene`, `candidate_related`, `not_related`, or `unresolved`, with reviewer ID and documentary reason.
5. Distinguish **exact-image separation** from **scene/session/site-group separation**. Only claim the level of independence actually verified. Avoid labels such as “leakage-free” without a reproducible audit trail.
6. Compare historical and derivative dataset manifests. Audit all 39 alleged removals and the 220-annotation difference against actual versions rather than interpreting them from proposal counts alone.
7. Freeze a signed manifest and audit report before making new evaluation-based selection decisions.

**Decision gate A:** If reliable acquisition-group identifiers exist, construct or verify a group-disjoint partition; if they do not, retain current partition as historical evaluation and restrict generalization claims. Do not convert ambiguous image similarity into a claim that a particular site supplied the image.

### Phase B — Label and condition audit

- Verify whether taxonomy version includes `No Safety Attire`, `abaya`, or both as genuinely separate labels; reconcile names, indices, and semantic definitions against actual files.
- Document the existing inclusion rules for annotations and ignored regions without modifying the original reference. Under Q12 Option A, no new manual review or test-label changes are activated; any proposed amendment requires a separate researcher decision.
- Under the researcher-ratified Q12 Option A, do not create new human-coded visual-condition labels. Apparent object scale may be derived mechanically from existing ground-truth boxes and original image dimensions; other condition variables are eligible only when already present in authentic, documented source metadata. Missing fields are `NOT AVAILABLE / NOT ESTIMABLE`.
- The Q12 double-review contingency remains dormant and is not activated by Q14. Any future human review requires a separate explicit researcher decision; the original test reference remains immutable.

### Phase C — Matched model evaluation

- **Historical reference only:** Present previously published model metrics with their dataset/checkpoint provenance; do not depict them as new experiments.
- **New evaluation:** Use archived exact checkpoints only for partitions not included in their training, tuning, or model-selection exposure. If a new group split puts previously seen images in test, train fresh models on the new training split; do not reuse contaminated weights.
- Apply the same class map, image identities, evaluation IoU rules, and scoring code. Document architecture-specific preprocessing rather than asserting total training-stack equivalence.
- Determine operating thresholds using validation data only; precommit chosen rules and report test results once, without iterative retuning on the test partition.
- Record training seeds, checkpoint IDs, optimizer/scheduler metadata, augmentation settings, model library versions, image resolution, model input transforms, and hardware. Multi-seed evidence must be claimed only if independently repeated.

### Phase D — Error analysis and uncertainty

- Report conventional COCO-compatible mAP@50 and mAP@50:95, class-wise AP, and precision/recall at prespecified operating points.
- At the prespecified matched-count operating point, record **both** `FNR_c = FN_c / (TP_c + FN_c)` for annotated missing-PPE class `c` and `FPPI_V = sum(FP_c for c in V) / N_images` for the six-class missing-PPE set `V`. This is not worker-level compliance or incident risk. Define one-to-one class-aware matching, duplicate predictions, class substitutions and ignored labels.
- Preselect underrepresented-class analyses and condition strata; display denominators and **do not suppress uncertain estimates**. The historical test contains 22 `No Hard Hat` annotations, 15 `Face Masks`, and 19 `Child` annotations [S4]; verify any new test support independently.
- Use paired image-level uncertainty when images are independent; use clustered/bootstrap resampling by verified acquisition group when related frames occur. If the number of clusters is too small, flag interval instability and rely on descriptive estimates.
- If reporting many tests/strata, preselect primary contrasts and either control multiple comparisons or label other tests exploratory. Report point estimates, effect differences, intervals, and sampling limitations rather than relying on p-values alone.
- If safety cost weights are introduced, distinguish them from observed consequences; use externally justified weights or label them scenario assumptions, and run sensitivity analysis. Always include unweighted metrics.

### Phase E — Optional resource profiling

- Benchmark the same inference hardware, precision mode, workload, preprocessing, input resolution, batch size, runtime/compiler, synchronization policy and warm-up protocol.
- Report latency distribution (median and upper-tail), images/s, peak GPU memory, repeated-measure variability, and measurement limitations. Energy per image is excluded unless power instrumentation with documented sampling is available.
- Do not equate benchmark inference latency with end-to-end site deployment response time.

## 7. Data status and planned evidence outputs

| Item | Current evidence | Status |
|---|---|---|
| Raw corpus size | 2,327 images and 17 classes confirmed by public project metadata; 16,520 labels paper-reported | Platform verified; bytes uninspected |
| Historical split | 1,625 train / 468 validation / 234 test | Platform metadata verified; identities unverified |
| Derivative version | 2,288 images, 16,300 labels, 1,595/459/234 split | Proposal-reported only; unverified |
| Data hashes and acquisition groups | No verified image-level manifest in this review | Not available |
| RF-DETR and YOLO checkpoints | Roboflow platform lists RF-DETR Small runs on versions 1 and 2; YOLO not checked here | Model provenance partially verified; binaries uninspected |
| New group-disjoint split | Dependent on audit results | Not created |
| New model scores and confidence intervals | None | Not run |
| Same-hardware inference benchmark | None newly produced | Not run |

## 8. Acceptance and stop criteria

**Gate 1 — Source integrity:** Do the filenames, bytes, hashes, class mappings and historical split totals reconcile with a versioned manifest? If not, stop and repair lineage documentation.

**Gate 2 — Independence claim:** Are acquisition groups adequately documented to support the promised split-disjointness level? If not, narrow the claim rather than invent group metadata.

**Gate 3 — Novel contribution:** Does the empirical result add interpretable, nontrivial evidence beyond the four conference papers and current external literature? If not, redesign the manuscript scope before a Q1 submission.

**Gate 4 — Reproducibility:** Are test-set exposure, checkpoint history, metrics code, confidence selection and statistical assumptions recorded? If not, do not call the study fully reproducible.

**Gate 5 — Journal readiness:** After new experiments, assess scope, methodological rigor, ethics, overlap disclosures and contemporaneous journal ranking. Q1 status alone does not guarantee suitability or acceptance.

## 9. Planned output structure for the eventual article

1. Introduction and differentiated contribution statement.
2. Related research and exact overlap disclosure with prior papers.
3. Data lineage, acquisition-level grouping and label-quality audit.
4. Prespecified evaluation and statistical methods.
5. Source-audit findings and benchmark comparisons (results only when measured).
6. Safety-relevant error analysis, uncertainty and quantitative trade-offs.
7. Optional resource profile and deployment constraints.
8. Discussion, failure cases, study limitations and responsible use.
9. Reproducibility/data-availability statement, ethics, and conclusion.

## 10. Limitations and disclosure policy

The original Y-PPE dataset contains a mixture of locally acquired worksite imagery and supplementary public images, as described in the thesis; the geographic and acquisition proportions must be verified. No experiment on the same 234 repeatedly inspected images can be described as a prospectively untouched independent external test. Worker-level PPE compliance and injury-risk reduction require task-specific ground truth and cannot be inferred solely from object labels. A result that fails to change the previous model ranking is publishable only if the methodology and empirical insight still offer sufficient verified value. All thesis and previously published conference work will be cited; the final article must include a transparent account of reused data/results and genuinely new experiments.

## 11. Immediate next actions (ordered)

**Step 01 — Complete:** Build a source-aware novelty/overlap matrix for the thesis and four papers, differentiating prior findings from tentative additions.

**Step 02 — Protocol drafted, execution blocked by missing raw files:** Freeze the audit procedure and requested image/label/checkpoint manifest. Begin byte-level audit only when source materials are available in the working environment.

**Step 03 — Software prepared, dataset screening not yet run:** A local read-only YOLO annotation/image audit utility and manual-review templates were written and verified with five synthetic unit tests. Public Roboflow records remain reconciled, but actual dataset bytes, annotation taxonomy semantics, the 2,288-image derivative and split dependencies remain unaudited. The requested remote export failed at DNS resolution; the executable utility awaits a local dataset archive.

**Step 04 — Offline protocol drafted:** A conditional statistical analysis plan and paired-count software are available, with the final source groups, split, thresholds, model matching and primary test controls blocked until data audit.

**Step 05 — Pending:** Run original new experiments; store predictions, code commit, checkpoints, configuration and outputs.

**Step 06 — Pending:** Verify results, uncertainty estimates, disagreements and reviewer concerns; revise master proposal as necessary.

**Step 07 — Pending:** Transform the accepted empirical contribution into an article manuscript and verify Q1 journal fit.

## 12. Source register and provenance of statements

**[S1]** University of Taiz, 2026 master's thesis: *Enhancing Occupational Safety Monitoring and Risk Management through AI-Based Data and Image Analysis*. Specifically Ch. 3, §§3.2.2–3.2.6, Tables 3.1–3.2; Ch. 4, Table 4.1, §4.3.1. User-provided thesis PDF.

**[S2]** Al-Tayar et al. (2025), *X-RF-DETR: A Framework for Explainable and Trustworthy PPE Decision Support*. Conceptual framework and preliminary 300-image public-PPE subset; a different experiment from Y-PPE historical test, and not directly comparable. User-provided PDF.

**[S3]** Al-Tayar et al. (2025), *AI-Driven RF-DETR Decision System for Real-Time PPE Monitoring in Yemen’s Development Projects*. Dataset implementation and model results. User-provided PDF.

**[S4]** Al-Tayar et al. (2026), *PPE Detection in Yemeni Construction Sites: YOLOv11m vs. RF-DETRs*. Tables I–II and VI–VIII, class-level and threshold analyses; discusses missing fixed-hardware benchmark and lack of multi-seed evaluation. User-provided PDF.

**[S5]** Al-Tayar et al. (2026), *BIM-Integrated Explainable Vision for Real-Time PPE Safety in Yemen’s Construction Sector*. Analytical/conceptual framework incorporating BIM, XAI and AHP–TOPSIS; field validation deferred. User-provided PDF.

**[S6]** *Preliminary Research Proposal — Version 1.0* (2026). Proposed derivative 2,288-image inventory and planned E1–E8; unverified plan, not measured findings. User-provided text file.

**[S7]** Robinson et al. (2026), *RF-DETR: Neural Architecture Search for Real-Time Detection Transformers*, ICLR 2026; official conference record: https://proceedings.iclr.cc/paper_files/paper/2026/hash/5bed8703db85ab27dc32f6a42f8fbdb6-Abstract-Conference.html. This external source confirms RF-DETR model context and naming, not new results on Y-PPE.

**[S8]** Public Roboflow ALTAYYAR project, version, training and model-evaluation metadata (read through linked Roboflow tools on 04 November 2026); project identifier `softyyemen/altayyar-0oflt-lafos-qqauz`. This establishes a subset of platform metadata and historical score lineage but not image-level audit findings.

**Evidence boundaries:** S1–S6 are statements in the supplied works; S7 is an external ICLR record; S8 is a live project record. No image bytes, annotation archives or model binaries were examined in this version. External novelty remains an open research task.

## 13. Internal review decision

**Historical v2.3 reviewer decision: Methodological revision plus platform-record verification; original empirical evaluation is still pending.** This version corrects the central claim from “comprehensive benchmarking” to “testable, provenance-aware reassessment”, separates historical from new metrics, and introduces explicit stop criteria. The next acceptable update requires a genuine dataset-file audit or documented limitation, not further unsupported accuracy claims.


## 14. Protocol implementation amendment — Version 2.3.0 (04 November 2026)

### 14.1 Executable audit instrument and its limited evidence

A local, offline screening program (`tools/audit_y_ppe.py`, SHA-256 recorded in the tool validation register) has been authored to parse a Roboflow-style YOLO dataset. It checks image readability, per-split file counts, annotation-file pairing, class index validity, normalized bounding-box geometry, exact image-byte duplicates, decoded-pixel duplicates after EXIF orientation normalization, and candidate near duplicates using a 64-bit difference hash. If documented `confirmed_group_id` records are supplied, the program also flags groups spanning multiple partitions. The output includes a JSON summary, a confidential per-image inventory and confidential cross-partition review candidates. See `tools/AUDIT_RUNBOOK_v1.0.md`.

Five synthetic fixture-based unit tests passed on 04 November 2026 (`audit_results/SYNTHETIC_TOOL_TESTS_ONLY.log`). These test code behavior on constructed images and invalid labels, including cross-split duplicate detection, group conflict, wrong expected count, re-encoded pixel identity and ZIP path traversal. **They are not findings on Y-PPE and do not provide a model metric or data-independence result.** No actual Y-PPE image bytes were available locally, and the Roboflow v3 ZIP download retry failed due to DNS/network restrictions.

### 14.2 Scientific restrictions accepted after internal review

A near-duplicate dHash distance threshold of 4/64 is an initial candidate-screening setting, not a statistically calibrated decision boundary. Similarity flags require human adjudication; absence of flags does not exclude cross-frame or same-site dependence. `integrity_screen_pass` refers only to selected file-format checks, not source independence or annotation correctness. The program intentionally reports `independence_verified=false` regardless of screening outcome. The confirmed group record must be documentary, not inferred from filenames.

**Acceptance decision:** Instrument validation **passes for the five implemented synthetic tests**. Scientific Gate 1 (real Y-PPE file integrity) remains **blocked**; Gate 2 (scene/source independence) remains **blocked**. No new RF-DETR/YOLO training, prediction, confidence interval or latency result has been produced. The current article's novelty remains contingent on future real-data results and external comparison.

### 14.3 Required next-stage artifacts

1. Authorized local ZIP of Y-PPE v3 images and labels, or extracted train/valid/test folders plus `data.yaml`.
2. Optional but essential for scene-level claims: verified source/site/session manifest and manual image-pair adjudication form.
3. Execution of the code against the actual corpus, followed by independent review of anomalies, group boundaries and all class counts.
4. Only after Gates 1 and 2: frozen split manifests and a preregistered statistical model-comparison plan.

The next version may revise or abandon the group-disjoint hypothesis if the available provenance records cannot support it; a missing-data restriction is preferable to an unsupported result.


## 15. Offline planning amendment — Version 2.4.0 (06 November 2026)

### 15.1 Research advancement accomplished without external dependencies

The conditional Statistical Analysis Plan (SAP v1.0; `protocols/STATISTICAL_ANALYSIS_PLAN_v1.0.md`) now fixes primary estimands for **annotated absent-PPE classes**, the paired model difference sign, bootstrap resampling protocol, result non-estimability rules, transparent reporting requirements and explicit test-set exposure safeguards. A reporting and condition-annotation specification, manuscript scaffold, source-overlap crosswalk and frozen-dependency register have also been created. These are preparatory research artifacts, not novel empirical results.

The offline `analysis/paired_error_analysis.py` script consumes a complete, pre-matched CSV of `image_id × class_name × model` detection counts. It enforces identical ground-truth counts between models, `TP + FN = GT`, nonnegative integer counts, paired completeness, provenance-group consistency, and undefined-denominator handling. It calculates per-class FNR and paired FNR differences with shared-unit percentile bootstrap confidence intervals (default 2,000 draws; seed 20261106), and exposes the number of valid bootstrap replicates. It **does not** compute AP/mAP, validate detections-to-label matching, infer worker compliance, establish dataset independence or verify a checkpoint.

Fifteen tests across the legacy audit utility and new statistical utility passed on synthetic fixtures on 06 November 2026. The previous five synthetic audit tests remain valid, and the ten new paired-statistics unit tests check deterministic seeding, group resampling, sparse denominators, duplicated/missing cells and malformed records. These results verify selected software properties only. No real Y-PPE records were used.

### 15.2 Prespecified analysis rules and interpretation limits

- For each class `c`, `FNR_c = FN_c / (TP_c + FN_c)` at fixed IoU and validation-selected confidence rules; if the denominator is zero, report `not estimable`. The primary model contrast is `ΔFNR_c = FNR_c(RF-DETR Small) − FNR_c(YOLOv11m)` (negative values favor RF-DETR for that class/operating point).
- Resample **paired images** simultaneously for both models. Where documentary acquisition groups are available, resample complete groups; otherwise any image-level interval is merely conditional/descriptive and may understate uncertainty. A 95% percentile bootstrap interval is not an equivalence test or evidence of generalization.
- Across the prespecified missing-PPE labels, conclusions are primarily descriptive class-specific contrasts, with denominators and intervals. No unqualified multiple hypothesis testing, safety-risk costs, legal compliance or causal architecture superiority may be inferred.
- A dataset split with the historical 234-image test is not a newly untouched prospective external test; new split selection and checkpoint exposure records must precede any independent evaluation claim.
- Score-ranked AP/mAP computation, score calibration, local evaluation latency and training variability require additional distinct input datasets and protocols. The count-analysis script is not a substitute for any of them.

### 15.3 Frozen steps and resumption gates

`protocols/DEFERRED_EXECUTION_REGISTER.md` records eight distinct paused dependencies: D01 real image/label audit; D02 documentary scene/group verification; D03 2,288-image derivative reconciliation; D04 new model training/predictions; D05 expert cost weights and worker-level semantics; D06 fixed-hardware resource benchmarking; D07 updated external novelty and Q1 scope verification; D08 submission-grade article/ethics. These tasks remain **paused** until their specific evidence is provided. The user is not asked for further material during offline development.

### 15.4 Version 2.4.0 internal peer review

**Decision:** The offline conditional SAP and software test harness are accepted as reproducibility preparations. They do **not** satisfy scientific Gates 1–5, do not yield new Y-PPE findings, and do not demonstrate a Q1-level scientific contribution. The master proposal remains an unsubmitted working protocol. See `review/INTERNAL_PEER_REVIEW_v2.4.0.md`.

### 15.5 Source-document custody (offline verification)

The six uploaded reference documents (thesis, four prior conference papers and proposal v1.0) were copied into the local project package without altering their contents. A per-file SHA-256 manifest and byte sizes are recorded at `source_documents/SOURCE_DOCUMENTS_SHA256_v1.0.csv`. This establishes a fixed version of **documents consulted**, but does not establish source authenticity, new empirical measurements, dataset-file integrity or verification of citations against public indexing services.


## 16. Interactive research decision amendment — Version 2.5.0 (06 November 2026)

### 16.1 Decisions adopted with the researcher

- **Question 2:** use object-level PPE detection as the primary validated unit; worker-level assessments remain conditional on new person-to-PPE relationship ground truth.
- **Question 3 — selected Option C:** preserve historical published Y-PPE scores as previously reported evidence; if trustworthy acquisition groups and independent retraining are feasible, create a documented group-disjoint split and compare RF-DETR Small with YOLOv11m using the same test instances and scoring code. Do not infer the cause of across-split score differences from raw differences alone.
- **Question 4 — selected Option C:** assess both misses and spurious detections of annotated missing-PPE classes as **two primary descriptive outcome dimensions**; neither can be ignored when discussing model preference.

### 16.2 Authoritative definition of the two co-primary error dimensions

**P1 — Missed annotated absent-PPE instances:** For each class `c` in the prespecified set `V`, `FNR_c = FN_c/(TP_c+FN_c)`. The evaluation unit is a labelled object at fixed **IoU=0.50** and an externally specified one-to-one matching algorithm. The six candidate categories, subject to checking the `data.yaml` taxonomy, are `No Hard Hat`, `No Gloves`, `No Face Mask`, `No Safety Boots`, `No Safety Vest`, and `No Safety Attire`. If `TP_c+FN_c=0`, the result is **not estimable**. Report counts and source-group support.

**P2 — Spurious missing-PPE detections:** `FPPI_V = sum(FP_c, c in V) / N_evaluated_images`. The denominator includes all test images, with or without missing-PPE ground truth. Multiple unmatched detections on one image count separately. This is a count-based false-detection burden; it is **not** a conventional binary FPR because a meaningful object-detection TN denominator is unavailable. It is **not** a count of distinct safety officer alerts or worker violations.

Comparisons must present side-by-side classwise `FNR_c`, aggregate `FPPI_V`, and paired differences using `RF-DETR − YOLOv11m`, with lower values indicating fewer errors *on that specific axis*. Do **not** collapse into an arbitrary single safety score. As an optional summary, the equally weighted six-class macro FNR is defined only if every prespecified class has nonzero test GT support; always present the class table.

### 16.3 Secondary metrics, validation, and inference boundary

Secondary evidence: COCO-compatible `mAP@50`, `mAP@50:95`, AP by class, precision, recall, F1, and Q14 apparent-object-scale FNR strata derived from existing GT boxes; other condition strata only when an authentic, pre-existing metadata field supports them. No new visual-condition annotation is authorized under Q12 Option A. Q14 relative-area bands are not official COCO AP-size metrics. AP requires confidence-ranked detections and cannot be reconstructed from aggregate TP/FP/FN alone. The operating-point selection algorithm and any tolerable false-alert target must be locked using training/validation data before reading test predictions. No subgroup-specific test threshold is permitted.

Report 95% paired bootstrap intervals for `FNR_c`, `FPPI_V`, `ΔFNR_c`, and `ΔFPPI_V`, resampling documented source groups when available, with image-only caveats otherwise. Default is 2,000 draws at seed 20261106. These are **two descriptive co-primary dimensions**, not license to run two uncorrected significance tests or declare a globally safer detector. Formal superiority, noninferiority, and composite cost conclusions require separate prespecified margins, expert-justified weighting (when relevant), and multiple-testing controls. The historical 234-image test has already been reported and cannot be described as an untouched prospective sample.

### 16.4 Implementation and internal peer review

The paired count analysis tool was amended to compute missing-PPE `FPPI_V`, paired `ΔFPPI_V` with 95% bootstrap intervals, and an optional complete-support macro-FNR. The five audit-tool tests plus fourteen count-analysis tests pass on synthetic fixture data (**19/19 tests**). **These are software tests, not results on Y-PPE.** `STATISTICAL_ANALYSIS_PLAN_v1.1.md` and `DUAL_ENDPOINT_METRICS_DECISION_v1.0.md` contain the operational definitions and review notes.

**Internal review outcome:** CONDITIONAL METHODS APPROVAL. This amendment resolves the v2.4.0 asymmetry that classified FPPI as secondary despite the study's dual-error framing. Results, split independence, threshold values, model comparison and the Q1 novelty judgment remain unverified until real data and independent external evidence are available. All previously frozen execution tasks remain frozen.

## 17. Interactive research decision amendment — Version 2.6.0 (06 November 2026)

### 17.1 Researcher-ratified Q5 decision: fixed operating rule and sensitivity

The researcher approved Q5 option D: a **primary validation-only operating-point rule** accompanied by separate threshold-sensitivity analysis. This does **not** approve any numerical confidence threshold or imply that test data have been observed. A single global confidence threshold is selected separately for each model using the **same** procedure: on validation predictions, maximize pooled *micro-F1* across six prespecified absent-PPE annotation classes over the candidate grid `{0.05, 0.10, ..., 0.95}`. Exact ties are resolved by lower violation FPPI, then higher confidence threshold. This is a practical benchmark operating point, **not an empirically justified clinical or occupational-safety utility**.

### 17.2 Locking and evaluation rules

- Fix a one-to-one class-consistent IoU≥0.50 matching rule, ignore/crowd and postprocessing settings, validation images, taxonomy, model checkpoints, threshold grid, tie logic and all code identifiers **before** analyzing a putatively independent test split.
- Select threshold from *validation* only, then lock the RF-DETR and YOLOv11m thresholds as separate values and evaluate test FNR/FPPI at those points. FPPI refers to **unmatched annotated missing-PPE detections per all evaluated image**, not false-alert probability or number of workers non-compliant.
- Report exploratory FNR versus FPPI curves across the full predefined threshold grid, with a clear warning that **test-set curves must not be used to reselect the operating point** or to declare unadjusted multi-threshold superiority.
- Ranked-score mAP is evaluated separately via a COCO-compatible implementation. Threshold variation is **not** proof of probability calibration. Historical test exposure remains a major limitation; old published test figures cannot be recast as fresh blind validation.
- If no positive annotated absent-PPE instances exist in validation, stop and redesign from training/validation evidence only, without peeking at test. A lack of reliable source grouping or provenance is an independent stop condition for source-disjoint claims.

### 17.3 Executable check and peer-review boundary

`analysis/select_validation_threshold.py` uses complete **pre-matched validation counts**, explicitly refuses any input row marked `test` or `train`, validates the fixed 19-point grid, and returns the selected threshold and a validation curve for each model. Ten additional tests passed on synthetic fixtures; the project suite now contains **29 synthetic passing tests**. This does **not** constitute a real-data evaluation; the image matcher, Y-PPE archive, independence audit, model retraining and checkpoint availability are all still pending.

**Reviewer decision:** CONDITIONALLY ACCEPTED as a prespecified selection protocol; no confidence values, model advantage, safety improvement or Q1 novelty have been demonstrated. Next interactive question Q6 addresses the required level of acquisition/source independence when real metadata become available.


## 18. Researcher-ratified Q6 decision — strongest provable dataset independence (v2.7.0)

Q6 option **D** is approved prospectively: choose the strongest partition-independence level evidenced by **authentic image-acquisition provenance**; do not maximize the rhetorical strength of a split claim. The hierarchy is L1 file/image-level duplication control, L2 independently documented acquisition sessions or scenes, L3 independently documented construction sites, and L4 an actually new external acquisition/domain. For existing Y-PPE images, attempt L3 only if reliable site IDs and adequate group/class support are available; otherwise attempt L2, then restrict to L1 (or explicitly mark independence unverified). L4 is unavailable merely by repartitioning existing data. A group-separated internal test must not be labelled untouched external validation.

Build groups of original images from verified site/session/video/duplicate relations **before** generating augmented training samples. No confirmed group or augmentation descendants may span train/valid/test. Document missing source IDs and unresolved near-duplicate candidates; exclude, quarantine or adjudicate them rather than treating each as an independent source. No class-support threshold, split allocation or model checkpoint is to be chosen retrospectively using new test outcomes. If site-held-out separation removes rare classes from evaluation, report the limitations and consider a defensible lower-level estimand; never manufacture independence by fragmenting sites.

For a new controlled RF-DETR Small/YOLOv11m comparison, retrain on the revised training partition, select thresholds on the validation partition under Q5, then apply the locked models and rules to the same test groups. Model checkpoints previously trained on images moved into that holdout cannot be used to assert independence. Report exact/near-duplicate audit decisions, numbers of distinct sites/sessions per split, object-label support, model/test exposure and source limitations; compare models **within** the new split and treat shifts relative to published scores only descriptively.

A new offline metadata checker has been added to flag duplicate SHA-256 hashes, group/site/session crossing and unresolved metadata. Its synthetic test pass does **not** establish any independence level for Y-PPE. Complete evidence and scientific acceptance gates are specified in `protocols/Q6_PROVENANCE_DISJOINT_SPLIT_PROTOCOL_v1.0.md`. Real image auditing, human adjudication, split generation, retraining and empirical results remain frozen. The next interactive decision Q7 concerns uncertainty quantification for clustered and rare-class observations.


## 19. Researcher-ratified Q7 conditional statistical inference — Version 2.8.0 (06 November 2026)

**Researcher decision:** Q7 Option C was approved. The appropriate statistical unit is the most defensible independently documented acquisition group. Use site-level groups for site-level inference when site IDs are proven, otherwise verified session/scene groups and scope-restricted conclusions. When neither is verifiable, image resampling may only be a clearly conditional/descriptive sensitivity analysis and cannot establish site/scene independence.

**Estimands and algorithm:** Following approved Q4/Q5, calculate fixed-operating-point FNR for each of the six annotated absent-PPE categories and FPPI across those categories. Use shared-group paired percentile bootstrap, B=2,000, fixed seed 20261106, for pointwise 95% intervals for each model and differences (`RF-DETR Small − YOLOv11m`). Within each bootstrap draw, pool TP/FN across the selected acquisition groups; divide pooled false positives by the actual number of selected images to estimate FPPI. A negative difference indicates fewer errors on the named axis, not globally safer decisions.

**Rare classes and diagnostic obligations:** Publish GT/TP/FN/FP, total acquisition groups, **number of GT-positive acquisition groups for each class**, bootstrap valid-replicate counts and fractions, and undefined values (NA) when GT=0. Do not replace a missing denominator or infer precision from a rare class represented by many boxes in one group. Fewer than ten class-positive groups or less than 95% paired-valid replicates trigger diagnostic caution, not a claim that a higher count guarantees reliable inference. When grouping and sparse support undermine intervals, report observed counts and limitations rather than confirmatory superiority.

**Multiplicity and independent-test integrity:** The six classwise FNR contrasts and aggregate FPPI contrast are descriptive co-primary outcomes. A 95% pointwise CI is not familywise 95% simultaneous coverage. Any formal superiority or noninferiority test requires prospectively selecting the primary endpoint, multiplicity policy, meaningful effect margin, and power/precision justification. Do not tune the Q5 confidence threshold or Q6 partition on the future test outcomes. Historical exposed results are historical, not untouched new validations. All true-data and external dependencies remain frozen.

**Software and documentation:** `analysis/paired_error_analysis.py` now supplies per-class source-positive resampling-unit counts, valid paired bootstrap fractions and fragility flags; five additional synthetic unit tests pass (46 total project tests). These software tests provide no findings about the actual Y-PPE corpus. See `protocols/Q7_CONDITIONAL_INFERENCE_PROTOCOL_v1.0.md`, `protocols/STATISTICAL_ANALYSIS_PLAN_v1.4.md`, and `review/Q7_CONDITIONAL_STATISTICS_PEER_REVIEW_v1.0.md`.

**Review outcome:** CONDITIONAL APPROVAL of the methodological specification. Neither independent site-level generalization nor model superiority nor external originality is established.


## 20. Researcher-ratified Q8 staged experiments — Version 2.9.0 (12 November 2026)

The researcher approved Q8 Option D: a **staged, evidence-gated experimental design**. This plan does not produce new RF-DETR or YOLOv11m results and does not establish a Q1-worthy original contribution until real-data findings and external literature are assessed.

**Core route:** E0 trace historical scores to the original published thesis/papers and platform versions; E1 audit actual Y-PPE image origin, duplicate/scene/session/site dependencies and derive the strongest supportable partition level; E2 retrain RF-DETR Small and YOLOv11m, where independently justified, using the same frozen image roster/class map/ground truth/splits and validation-only model selection; E3 evaluate six missing-PPE class FNRs, pooled missing-PPE FPPI, group support, paired differences and conditional uncertainty under Q4–Q7.

**Optional or supporting route:** E4/Q14 stratifies class-specific FNR by apparent GT-box scale derived from existing annotations, and uses other conditions only when already present in verified metadata; no new human labels are created under Q12 A. E5 optionally benchmarks latency and memory on identical measured hardware (energy only if directly instrumented); E6 presents prespecified sensitivity to operating thresholds, independence assumptions and statistical fragility, with test-based curves explicitly exploratory.

**Experimental gates:** E1 must establish real data/provenance evidence before source-disjoint E2 claims. E2 requires comparable validation tuning, checkpoint/model-data independence and identical test evaluation—not merely identical epochs, which is generally not fair across architectures. E3 requires paired per-image prediction/GT counts and the fixed Q5 operating rule. Sparse class or cluster evidence leads to descriptive/NA reporting, not inferential escalation. Manuscript novelty and Q1 journal eligibility cannot be certified without substantive results and current external literature comparison.

**Reviewer decision:** CONDITIONAL DESIGN APPROVAL. Previous papers already reported baseline RF-DETR/YOLO comparisons and some per-class/threshold analysis; those are historical contributions. No new experiment has been run and the external-data/hardware/human tasks remain frozen. Detailed acceptance gates in `protocols/Q8_STAGED_EXPERIMENTAL_DESIGN_v1.0.md`; critical reviewer notes in `review/Q8_STAGED_DESIGN_PEER_REVIEW_v1.0.md`.


## 21. Q9 — Repeated training under a documented resource budget (Version 3.0.0; 12 November 2026)

**Researcher decision:** Q9 option C, a staged training protocol for RF-DETR Small and YOLOv11m, has been approved **prospectively**. This does not mean new Y-PPE training has occurred. T0 freezes audited data/splits, class taxonomy, initialization and software evidence (requires Q6 E1). T1 conducts one training/validation-only feasibility pilot per architecture. T2 prespecifies at most four validation-only HPO candidate evaluations per architecture as a **planning ceiling**, with actual equal-or-disclosed GPU-hour budgets determined after the pilot. T3 targets **three independent full fine-tuning runs per model**, with seed labels 11, 29 and 47 selected before new test exposure. Matching seed integers across implementations does not make random processes truly paired.

**Fairness:** Both models must use the same grouped image partitions, ground truth and evaluator, without any holdout data used for checkpoint/hyperparameter selection. Equal epoch counts are not required and alone are not fair. Model-specific learning schedules, effective batch sizes, architecture-native resizing and postprocessing are permitted only if logged transparently, with any resulting confounding reported. Planned primary comparison requires a documented equivalent opportunity and accelerator-hour budget; otherwise the analysis is explicitly labelled resource-asymmetric. Source checkpoint versions and possible prior exposure to new test images must be audited. Neither tuning budget nor GPU memory/time has been measured.

**Selection and outcomes:** One final configuration is locked per model based on a common validation checkpoint-selection criterion (proposed mAP@50:95 across all 17 classes). Each accepted seed produces one model checkpoint and one validation-selected global absent-PPE cutoff using Q5. At the locked cutoff, evaluate six-class FNR and pooled FPPI and run-level variation, and report per-run mAP as supportive. Distinguish seed-to-seed variation from the cluster-conditional uncertainty of the test groups (Q7). Three seeds are a minimum planned repeatability check, **not statistical proof of stability or independent sites**. Never discard a completed poor-performing seed, retrain after seeing test scores, or interpret seed SD as an external generalization CI.

**Resource tiers:** Tier A = pilot + bounded HPO + three completed final fits per architecture and conditional inference; Tier B = fewer than three final fits, with only descriptive comparisons and no repeated-training stability claim; Tier C = pilots/historical scores only, not an independent new benchmark. If a provenance-independent split fails E1, no tier can support an independently verified site-generalization claim. Freeze all empirical activities until real Y-PPE files and authorized resources become available.

**Review:** CONDITIONAL METHODS APPROVAL. No model has been retrained, no Y-PPE images have been audited in this version, and no new accuracy, energy, timing or Q1 originality claim is established. The binding detailed document is `protocols/Q9_TRAINING_REPRODUCIBILITY_AND_BUDGET_v1.0.md`; reviewer findings: `review/Q9_REPEATED_TRAINING_PEER_REVIEW_v1.0.md`. Q10 will determine evidence thresholds for treating results as a publishable new contribution rather than a repackaged comparison.


## 22. Q10 — Evidence-integrated originality and publication readiness (Version 3.1.0; 13 November 2026)

**Researcher-ratified decision:** Q10 Option C. The originality threshold is evidence-based, not an arbitrary gain in mAP, FNR or FPPI. Q1 is a target journal category, not a guaranteed publication result. A repeated RF-DETR/YOLO comparison or reuse of known audit/uncertainty tools is not novel merely by itself; the journal paper must establish a substantive new result or rigorously bounded inference distinguishable from the master's thesis, four related papers and recent 2026 PPE literature.

**Prospective evidence gates:** G1 original-image provenance and valid split level, with no unsupported site or external independence; G2 E0–E3 admissible evidence (source-traced historical numbers, actual dataset audit, a new honestly controlled benchmark where feasible, and FNR/FPPI plus paired, group-sensitive uncertainty); G3 a clearly articulated *new empirical inference* rather than an updated table; G4 documented nearest literature and transparent overlap, with no repeated XAI/BIM claims; G5 verified venue fit and manuscript integrity. Separate GO-DRAFT (writing after G1–G4) from GO-SUBMIT (ready after G5). A synthetically tested tool is not an empirical finding.

**Outcome-neutral criteria:** Improvements are not mandatory. A robustly bounded unchanged result could be informative if sufficiently precise and consequential; a null result with wide confidence limits does not prove equivalence. Lower scores on another split do not identify leakage as the cause absent controls. Ranking reversal and false-negative/false-positive tradeoffs need adequate paired evidence. Inadequate source IDs, irreparable test contamination, no new empirical data, or repetition of previously published conclusions implies NO-GO for the current original Q1 submission claim; resolvable shortcomings imply REVISE, not cherry-picking.

**New overlap warning:** A 2026 Buildings PPE study already uses video-level separation, repeated training and calibration; a 2026 Scientific Reports PPE study reports split/visual-condition sensitivity. Literature search here is targeted/exploratory, **not** a completed systematic review. References and constraints: `protocols/Q10_NOVELTY_PUBLICATION_GATES_v1.0.md`, `templates/Q10_NEAREST_WORK_NOVELTY_LEDGER.csv`, and `review/Q10_NOVELTY_PUBLICATION_PEER_REVIEW_v1.0.md`.

**Status:** The conditions are prospectively specified; none of E1–E3 have generated new Y-PPE evidence, no validated independent site split, no actual model comparison or publisher decision, and no verified target journal Q1 quartile. Previously frozen tasks remain frozen. Next decision Q11 addresses a structured, source-grounded literature gap and ethical overlap disclosure.


## 23. Q11 — Structured literature review, dual novelty matrices (Version 3.2.0; 13 November 2026)

**Researcher-ratified decision:** Option D. Two non-interchangeable novelty reviews are now required: (1) an author-publication overlap matrix against the 2026 Y-PPE master's thesis and four related IEEE conference papers; and (2) a contextual external matrix that tests originality against published PPE and adjacent computer-vision methods. The main journal deliverable remains a prospective original-research article, not a systematic review.

**Actual literature work completed:** A targeted publisher-verified external seed corpus of 13 studies has been classified by direct/adjacent relevance and evidence-access level (full text or abstract/metadata). It contains an especially close 2026 Buildings paper using recording-disjoint PPE splits, three independent training runs, validation thresholds and calibration; another 2026 Buildings study of adverse-weather robustness; 2025/2026 PPE non-compliance and worker-level decision research; a 2026 Automation in Construction cross-site generalization study, and a 2026 Technologies study of sequence-aware detection benchmark leakage in another domain. The five local publications and the thirteen external studies are inventoried in two CSV files with source URLs/DOIs and evidence constraints. This is an **organized exploratory evidence map**, not exhaustive database screening or a PRISMA systematic review.

**Novelty audit result:** Do not claim first RF-DETR PPE detector, first Yemeni Y-PPE dataset, novel YOLO/RF-DETR comparative benchmark, original XAI/BIM decision-support scheme, first multiseed PPE study, first source-aware splitting, first classwise safety-error analysis, or first leakage-audit methodology. A possible paper contribution remains strictly conditional on new E1–E3 results: provenance-audited reassessment of historically published RF-DETR/YOLOv11m outcomes on Y-PPE, validation-frozen missing-PPE FNR and FPPI, and group-aware paired uncertainty, showing what conclusions remain defensible and which do not. The value of such findings and distinction from global publications remain unverified.

**Procedural controls:** Source reviews distinguish 'confirmed in publisher full text' from 'abstract only'; silence in an abstract cannot establish absence. Do not pool AP/mAP across PPE classification and object-detection datasets or across different IoU/class definitions. A future reproducible Scopus/Web of Science/IEEE Xplore screening would need separate query counts, duplicate handling, and source-level decisions; none is claimed here. Q1 rank verification and journal choice remain pending. The original test images are not a fresh untouched holdout. Real Y-PPE dataset audit and all training activities remain frozen.

**Review outcome:** CONDITIONAL APPROVAL of the literature mapping protocol; MAJOR REVISION remains for any global originality claim. See `protocols/Q11_STRUCTURED_LITERATURE_REVIEW_PROTOCOL_v1.0.md`, `literature/OWN_PUBLICATION_OVERLAP_MATRIX_v1.0.csv`, `literature/EXTERNAL_EVIDENCE_AND_NOVELTY_MATRIX_v1.0.csv`, `review/Q11_LITERATURE_NOVELTY_PEER_REVIEW_v1.0.md` and `reports/RELATED_WORK_DRAFT_Q11_v0.1.md`. Next Q12 addresses annotation-label quality and safety-semantics before quantitative FNR/FPPI evaluation.


## 24. Q12 — Existing annotations as conditional reference; human review frozen (Version 3.3.0; 13 November 2026)

**Researcher-ratified choice: Q12 Option A.** Existing Y-PPE labels are retained without an additional manual annotation review in the extended study at this stage. No stratified image sample, independent dual annotation, reviewer agreement statistic, or revised test ground truth has been generated. The request to define sample strata and inter-rater agreement is fulfilled in a dormant, optional future protocol and **does not supersede Option A**.

**Interpretation:** The prespecified absent-PPE FNR and FPPI are measures relative to the available annotation reference, not independently validated real-world PPE compliance, accident risk, or label-error-free ground truth. Missing objects and semantic ambiguity may bias either endpoint. No independent annotation accuracy estimate is available. The `No Safety Attire` vs `Abaya` terminology question remains unresolved in source files.

**Anti-contamination:** Keep original test reference immutable for the primary results. Record suspected defects in a separate issue log without model-guided relabeling. If the researcher later authorizes blinded review, select a prospective image-level stratified sample across splits, absent-PPE classes and independently verified provenance groups; two independent annotators would code objects/classes/boxes and a third adjudicator would document conflicts. No sample-size or agreement values can be claimed now. Corrections motivated after observing test predictions may only appear as explicitly post-hoc sensitivity analyses; substantive test-label defects may require abandoning a confirmatory claim.

**Review decision:** CONDITIONAL ACCEPTANCE OF OPTION A AS A CONSTRAINT; annotation-label quality NOT VERIFIED. Real dataset QA, human review, model training and empirical metrics remain frozen. Details: `protocols/Q12_ANNOTATION_REFERENCE_POLICY_AND_CONTINGENCY_QA_v1.0.md`, `decisions/Q12_USE_EXISTING_LABELS_OPTION_A_v1.0.md`, `review/Q12_ANNOTATION_METHODS_PEER_REVIEW_v1.0.md`.


## 25. Q13 — Delegated safety-related error weighting (Version 3.4.0; 13 November 2026)

**Decision source:** Researcher selected **Option E (delegate)**. The assistant's scientifically chosen implementation is conservative **Option C**: retain **unweighted classwise FNR and pooled FPPI as two separate primary descriptive outcome domains**. Do not numerically privilege `No Hard Hat` or any other absent-PPE class based solely on its name. Existing annotations do not measure context-specific worker hazard severity, exposure, likely injury, alert cost or statutory noncompliance. The six names remain provisional until class-map verification; `No Safety Attire` semantic ambiguity remains unresolved.

**Weighting restriction:** No empirical risk weights are approved or available. A potential `W-FNR = Σ_c w_c FNR_c`, `w_c≥0`, `Σ_c w_c=1`, is an exploratory class-weighted macro sensitivity index ONLY after five evidence gates W1–W5: independently documented task/hazard/exposure and severity, qualified independent expert or injury-data provenance, transparent weight elicitation/disagreement, pretest lock of six complete weights, and adequate class support/verified mapping. If any class FNR is undefined, no full-six-class weighted macro is reported. A possible weighted FPPI uses a distinct false-alert utility vector `v`, not assumed to be the same as harm-severity weights. No blended risk score, worker-level compliance claim, injury probability or measured risk reduction is permitted.

**Review status:** Conditional methods acceptance only; safety-risk evidence is **NOT AVAILABLE**, weight elicitation and real model evaluation **NOT PERFORMED**. See `protocols/Q13_SAFETY_WEIGHTING_AND_BOUNDARIES_v1.0.md`, `decisions/Q13_DELEGATED_SAFETY_WEIGHTING_DECISION_v1.0.md`, and `review/Q13_SAFETY_WEIGHTING_PEER_REVIEW_v1.0.md`.


## 26. Q14 — Conditional within-dataset subgroup robustness (Version 3.5.0; 22 November 2026)

**Researcher-ratified decision:** The researcher approved Option D: analyze subgroup robustness only where existing source data or mechanically derivable fields support a valid, predeclared subgroup. This approves a conditional protocol, not an executed analysis.

**Scope correction:** Q14 evaluates within-Y-PPE heterogeneity. It does not establish cross-site or external-domain robustness; such claims require Q6-authenticated site/session groups or a genuinely independent L4 corpus. Apparent object scale is the primary candidate subgroup, derived from existing ground-truth boxes and original image dimensions. Occlusion, truncation, scene density, illumination, weather, viewpoint and other conditions are eligible only if already present as authentic, documented source fields. Under Q12 Option A, no new visual labels or additional manual review are authorized.

**Apparent-scale strata:** Use the fixed relative area ratio `r = GT box area / original image area`, with small `r < 0.0025`, medium `0.0025 ≤ r < 0.0225`, and large `r ≥ 0.0225`. These are COCO-inspired 640×640-equivalent relative-area bands, not official COCO AP-size metrics and not physical object-size measurements. Cutoffs are frozen before test prediction access.

**Estimand and controls:** For each of the six candidate absent-PPE classes and each eligible size stratum, report `FNR(c,s)=FN(c,s)/(TP(c,s)+FN(c,s))` and paired `ΔFNR=RF-DETR Small−YOLOv11m`. Use the same test images and original labels, Q5 validation-only global thresholds, and the frozen class-consistent one-to-one matcher at IoU ≥0.50. No subgroup-specific test threshold or post-hoc cutpoint is permitted. Zero GT support is `NA`, not zero.

**FPPI boundary:** Q4 pooled FPPI remains an image-level co-primary outcome and is not allocated to GT object-size strata. A subgroup FPPI may be reported only for a pre-existing, defined image-level condition, using the number of images in that condition as its denominator.

**Uncertainty and interpretation:** Inherit Q7 paired group bootstrap (2,000 draws; seed 20261106), with the strongest authenticated acquisition group available. Image-only resampling is conditional/descriptive and cannot establish site/scene independence. Report GT/TP/FN, image and group support, valid draws and valid fractions. Fewer than 10 GT-positive groups and paired-valid fraction below 95% are fragility warnings, not universal adequacy thresholds. The full subgroup table uses pointwise intervals and remains exploratory; no unadjusted subgroup superiority, interaction, worker-compliance, injury-reduction, or external-domain claim is authorized.

**Admission rules:** Admit a descriptive Q14 analysis only after authorized archive access, source integrity, verified class/box conventions, frozen subgroup register, paired model predictions, Q5 thresholds, fixed matching, and complete denominators are confirmed. Downgrade sparse or image-only results to descriptive/fragile reporting. Mark a cell `NOT ESTIMABLE` when the field is absent, the denominator is zero, or the class map/box convention/prediction pairing is unresolved. Reject new unapproved visual tags, test-driven cutoffs, subgroup-specific test tuning, or FPPI attributed to object-size bins.

**Review outcome:** CONDITIONAL DESIGN APPROVAL ONLY after correcting the previous proposal wording that implied new visual rubrics and double-review despite Q12 Option A. The current master metadata are normalized to Version 3.5.0 / 22 November 2026. No Q14 images have been audited, no subgroup labels created, no predictions or subgroup estimates produced, and no code tests run. E1–E3 remain frozen; the Q1 publication gate remains unmet. See `protocols/Q14_CONDITIONAL_SUBGROUP_ROBUSTNESS_PROTOCOL_v1.0.md`, `decisions/Q14_CONDITIONAL_SUBGROUP_ROBUSTNESS_DECISION_v1.0.md`, `review/Q14_CONDITIONAL_SUBGROUP_ROBUSTNESS_PEER_REVIEW_v1.0.md`, and `templates/Q14_SUBGROUP_EVIDENCE_REGISTER_TEMPLATE.csv`.