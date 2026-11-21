# SEER-PPE V19 — original-author annotation numerical evaluation and no-reinspection source-sensitivity protocol

**Date:** 21 November 2026. **Scope:** reproducible, read-only, Train-only numerical preflight and computational Validation eligibility/sensitivity planning. **No additional human annotator or repeat image inspections** are required. Author's existing reviewed original class/box labels are accepted as the primary **single-curator object-level reference**; this is a limited detection reference and not a verified worker PPE safety-violation reference.

## Actual original reference available

Four existing original Train Source IDs were queried with Roboflow's **read-only saved annotations API**, not with inference or an image review tool. Each has a valid, non-null original annotation envelope. The [V19 read-only Source snapshot](TRAIN_ORIGINAL_SOURCE_ANNOTATIONS_READONLY_V19.json) preserves Source ID, filename, native annotation group/version, image dimensions, class, original box center/width/height, polygon-versus-box flag and model-assisted provenance marker. A/C contain historical polygon annotations; these are evaluated by their saved **bounding rectangles** only, not segmentation. The snapshot includes **48 original annotated objects**: A 5, B 15, C 27, D 1. **Seven** of B's annotations carry `labeledByModel=RFBoxPrompt/v1`. This provenance does not erase the author's review but rules out claims that all original labels were created from scratch by a blind independent rater. Retain them and report a full-image exclusion sensitivity, rather than silently changing ground truth.

The fixed original RF-DETR Small model `altayyar-0oflt-lafos-qqauz/2` already supplied **51 predicted boxes** (A 5, B 16, C 29, D 1), stored as a previous actual Train-only hosted inference. V19 never runs the model again. The V19 numerical evaluator checks Source IDs against existing Train Eval cases, checks original filenames and pixel dimensions, and matches original class-specific predicted boxes using deterministic score-ordered greedy IoU matching at **IoU 0.50**. One GT can match at most one detector prediction; unmatched extra predictions count FP, unmatched GT boxes count FN. `No Face Mask` and `No Safety Boots` are detection **class names**, not verified policy violations.

The evaluator calculates TP, FP, FN, precision/recall/F1 and 101-recall-point class AP at IoU=0.50, plus ten thresholds IoU 0.50–0.95, for object **bbox** comparison. **Important:** hosted predictions were returned with confidence floor 0.20, so AP is explicitly an **above-0.20 truncated AP proxy, NOT an official full-score-list COCO mAP**. The macro average includes only classes with original GT in this four-Train-image sample. Scores are saved strictly as *Train development checks*, not study efficacy, generalization, a validated model score or a scientific comparison between RF-DETR and SEER-PPE.

Two parallel Train source-label sensitivity profiles are written: all four original labeled Train examples and **the three complete images excluding the single image B that contains model-assisted label markers**. Dropping the whole image, rather than dropping individual labels and counting associated detections as false positives, avoids inducing fake errors by creating artificial unlabeled positives. No manual reannotation or reference change is made.

## Computational source-overlap treatment

Recompute without opening images using existing immutable forensic outputs: the full original→Clean17 459-photo technical mapping, V14 **280 original Train–Valid candidate-pair measurements**, and current V15 cohort readiness. No independent-site assertion is inferred from similarity or lack thereof. The V19 source tool computes three *descriptive-only* Valid source cohorts:

| Scenario | Size | Definition |
|---|---:|---|
| M0 — all technically matched corrected Valid | 459 | Includes all retained original Valid→Clean17 image IDs; does not imply independent acquisition |
| M1 — conservative risk exclusion | 448 | Excludes five prior research holds and six technical high-overlap quarantines |
| M2 — unflagged-only sensitivity | 367 | Additionally excludes 81 other possible cross-split source-family cases; these 367 remain **not proven independent** |

The program also derives **12 high-similarity original Train–Valid pair edges**, **9 distinct Valid IDs** (8 retained in corrected Clean17), and connected **technical hypothesis components**. Components are *possible* repeated image/scene groups, not verified individual site/session families or final exclusion rules. Sample-size changes and any later per-class metric changes on M0/M1/M2 must be reported, and independence uncertainty must be disclosed. No Test sources, protected Test images, original data or source splits are read or modified.

## Scientific endpoint separation and future scorer contract

**Endpoint A (possible):** historical internal object detection against the owner's original object labels, at a frozen metric policy and explicitly documented prior model-development exposure. A second reviewer is not a prerequisite. Source family risk is quantified via exclusions/sensitivity, and independence is not claimed without evidence.

**Endpoint B (not yet evidenced):** verified worker–PPE ownership, occupational false-clearance or a fully independent external safety comparison. Original object boxes do not automatically supply each worker's PPE status or applicable site/task mandate. Existing V16 Person–PPE observations remain preserved; unrecorded person-specific states cannot be fabricated. The V15 strict scoring gate remains closed for worker safety / independently verified source claims; `scoring_ready=false` is not a ban on calculating *Train diagnostic box alignment*.

**Next required for historical descriptive Valid numerical analysis:** obtain fixed-model original Valid predictions by original Source ID with identical inference and preprocess/confidence settings; obtain corresponding saved original annotation geometry from the already curated dataset; freeze matching code/threshold/denominators and list the three M0/M1/M2 cohort IDs. Report run provenance, class/box only, and never claim Test independence. The four A-D Train results cannot be used as the Validation result.

All algorithms fail closed on synthetic Train→Test injections, modified source-label IDs or provenance, fabricated independent source signoffs and mismatched dimensions. CI evidence is an engineering/software verification, not a safety result.
