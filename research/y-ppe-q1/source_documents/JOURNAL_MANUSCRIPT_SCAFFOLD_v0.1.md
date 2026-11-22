# Journal manuscript working scaffold — v0.1 (methods-only drafting)

**Working title:** From Aggregate Accuracy to Safety-Relevant Reliability: A Provenance-Audited and Uncertainty-Aware Evaluation of RF-DETR on Y-PPE

**Status and safeguards:** Unsubmitted internal outline. Introduction and methods are provisional drafts grounded in the author's uploaded thesis and four conference papers. This file contains **no new empirical results**, does **not** assert a verified literature gap, and does **not** claim Q1 suitability. Citation tags [S1]–[S8] refer to the master proposal's *internal source register* and are NOT submission-ready bibliography numbering.

## 1. Introduction — provisional text

Reliable personal protective equipment (PPE) monitoring requires more than producing an accurate set of object detections on a curated benchmark. At a construction site, errors affecting missing-PPE categories may have different practical implications from errors involving contextual objects; nevertheless, object-detection performance is commonly summarized with aggregate precision, recall and average precision. These metrics are useful for comparing detection systems, but cannot alone establish how uncertain rare-class error estimates are or whether image samples originate from independent acquisition events.

The Y-PPE research program has contributed a 17-category image corpus from Yemeni construction and development contexts and demonstrated RF-DETR Small for detecting annotated PPE-related objects [S1, S3]. A prior controlled comparison with YOLOv11m on the historical split reported an RF-DETR advantage in mAP@50 and recall but a YOLOv11m advantage in stricter mAP@50:95 and precision [S4]. Related author work has also proposed interpretable PPE decision support [S2] and a conceptual BIM-integrated safety governance pipeline [S5]. These developments collectively motivate a narrower scientific question: how confidently can model-level conclusions be interpreted when acquisition provenance, class support and dependence between evaluated observations are made explicit?

The present **proposed** study will examine, rather than presume, potential dependencies among Y-PPE images and evaluate class-specific missing-detection uncertainty using an auditable protocol. It is not a new detector architecture and does not claim that the historical results are incorrect. Its intended new contribution, conditional upon access to the raw materials and execution of admissible experiments, is a provenance-informed interpretation of safety-relevant detection errors and of the previously reported cross-model tradeoff.

## 2. Prior studies and delimitation of novelty — internal outline

- **Detection and dataset:** Summarize S1/S3 with explicit reused acquisition/labels/model identity.
- **Benchmark tradeoffs:** Summarize S4, including full precision/recall and strict localization tradeoffs, with identical metric definitions and split caveats.
- **Explanation and governance:** S2/S5 remain related work, not newly implemented components.
- **External literature gap:** **FROZEN — requires an updated independently documented search**. Do not write “first to...” or “novel benchmark” before doing that work.

## 3. Methods — pre-results draft

### 3.1 Dataset lineage and identity controls

Before modeling, original and derived image/annotation versions will be mapped to persistent image identifiers. Recorded source type, site, capture session and image sequence will be treated as documentary variables: missing provenance will remain missing. Exact byte and pixel duplicates will be screened algorithmically, visually similar image pairs will be referred for documented manual adjudication, and source-group separation will only be claimed where the metadata and reviews substantiate it. An older historical 234-image test split cannot be represented as a previously untouched external benchmark [S1, S4].

### 3.2 Models and evaluation comparability

RF-DETR Small and YOLOv11m will be compared on identical verified test images with one class map and one scoring implementation, if a defensible new protocol can be constructed. Confidence-policy selection will be restricted to validation data. Prior trained weights will be reused only when their training/tuning exposure is compatible with the selected test set. Model-specific preprocessing and training settings will be disclosed, rather than asserting that identical images alone eliminate all architectural or training confounding.

### 3.3 Error estimands and statistical uncertainty

The primary error outcome is a missed *annotated object* in the predefined absent-PPE categories, not failure of occupational compliance or evidence of injury risk. For class c, `FNR_c = FN_c / (TP_c + FN_c)` at an explicitly fixed matching IoU and confidence policy. The paired contrast is `FNR_c(RF-DETR) − FNR_c(YOLOv11m)`. Where documentary acquisition groups are available, resampling will occur at the group level with the same sampled groups applied to both detectors. Otherwise image-level resampling will be described as conditional and potentially underestimating uncertainty from shared scenes. The primary output is a paired effect estimate with a 95% percentile interval, not a binary declaration of a superior architecture.

### 3.4 Condition metadata, annotations and optional resources

Prespecified object-size and visibility labels will be reviewed independently of model predictions where feasible. Missing or ambiguous labels will not be silently discarded. Optional common-hardware latency and memory evaluation will require real instrumented execution; such metrics will not be inferred from model size or historical heterogeneous sources.

## 4. Results — intentionally not written

**[BLOCKED — no new Y-PPE image audit, class-matched prediction export or experiment was conducted.]** Tables T1–T7 remain *empty templates*. Prior publications' numerical values may be included in a separately titled “Historical benchmark” table with source citations, never in a new-experiment results table.

## 5. Discussion — conditional logic only

The discussion must distinguish (a) source integrity from scene independence, (b) class-level missed-detection uncertainty from worker-level compliance, (c) paired model differences from domain transfer, and (d) evidence of variation from causal attribution. A model-rank change is not guaranteed. If no material new knowledge arises, return to the research design rather than submitting a redundant article.

## 6. Ethics, provenance and reproducibility — drafted disclosure prompts

Identify all reused source articles and thesis components; describe actual dataset permissions, privacy handling and staff/worker visibility; report any institutional review or waiver **only if documentary evidence exists**. Include dataset/checkpoint versions, code checksums, exclusion logs, software versions and confidence-selection policy. Declare image/annotation access limitations and prior test exposure. Never state that a participant review or field trial occurred unless performed and approved.

## 7. Submission gating

The following sections are frozen: current external literature, verified source-level split audit, actual experiments and model selection, effect estimates, external reviewers, target journal indexing, final ethics approvals and submission-ready references.