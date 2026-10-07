# Stage 9 — Q1 Readiness Audit

**Current decision:** MAJOR REVISION RESOLVED SCIENTIFICALLY; ADMINISTRATIVE/REPORTING BLOCKERS REMAIN.

## Scientific strengths now established

### 1. Clear research question
The manuscript now addresses a deployment-reliability question rather than an architecture-comparison question:

- how much does performance degrade under bidirectional domain transfer?
- is the degradation stable across independent seeds?
- do safety-critical negative-state classes fail more severely than aggregate metrics imply?

### 2. Strong protocol integrity
- two frozen harmonized domains;
- three independent seeds per source domain;
- final-epoch checkpoints only;
- held-out evaluator frozen before test exposure;
- no test-informed checkpoint or threshold selection;
- 12 completed held-out evaluation cells.

### 3. Reproducibility
The current paper now records:
- dataset fingerprints;
- exact class order;
- exact final split sizes;
- pretrained checkpoint;
- 100 epochs;
- 640 resolution;
- batch size 8;
- workers 2;
- AMP;
- Tesla T4;
- Python/PyTorch/CUDA/Ultralytics versions;
- optimizer policy and resolved AdamW log evidence.

### 4. Safety-oriented outcome analysis
The manuscript reports:
- aggregate mAP50:95, mAP50, mAP75;
- fixed-threshold precision/recall/F1;
- class-level safety recall/FNR;
- cross-domain generalization gaps;
- three-seed consensus false negatives.

### 5. Evidence-backed interpretation
The dataset diagnostic audit rules out stored image geometry as an explanation and identifies material differences in class support and object-scale distributions without overstating causality.

### 6. Novelty is now defensible
The novelty claim is framed as a combination of:
- bidirectional zero-shot PPE transfer;
- harmonized ontology;
- three seeds per source domain;
- pre-frozen held-out protocol;
- safety-negative-state analysis;
- consensus false-negative audit.

The paper no longer claims novelty merely from using YOLO11m or from studying domain shift.

## Remaining CRITICAL blockers before submission

### A. Ethics and image-use governance — BLOCKING
Available source material documents organizational coordination and a public CC BY 4.0 Roboflow declaration for Y-PPE, but it does not establish the exact wording needed for:
- institutional permission;
- worker-image consent/waiver;
- ethics/IRB approval or exemption;
- public redistribution authority for all primary field images.

The final paper must use the author's actual institutional record. Do not infer or invent this statement.

### B. Funding — BLOCKING
The exact funding statement for the new paper is not available in the current evidence.

### C. Competing interests — BLOCKING
The exact author declaration must be explicitly confirmed.

### D. Author contributions — BLOCKING
The final author list and CRediT roles must be confirmed.

### E. Archival reproducibility identifier — HIGH PRIORITY
The repository is active, but submission quality would improve by creating:
- a tagged immutable release;
- Zenodo/OSF DOI or equivalent archive;
- a frozen Stage 6/7 result bundle.

## Important non-blocking improvements

### 1. Add image-level uncertainty if feasible
The current three-seed mean ± SD analysis is scientifically valid as descriptive seed variability. A paired image-level bootstrap confidence interval for the domain gap would strengthen a Q1 submission if prediction-level evidence is preserved or can be regenerated under the already-frozen evaluator.

This is optional and must not involve model or threshold selection.

### 2. Add a compact ontology figure
A figure showing:
- 17-class Y-PPE source;
- 11-class Construction-PPE source;
- exclusions;
- final shared 9-class ontology
would make the methodology easier to audit.

### 3. Add a protocol-flow figure
Recommended flow:
Source datasets → Stage 2 integrity audit → Stage 3 semantic harmonization → Stage 4.5 conservative filtering → Stage 5 six completed YOLO runs → Stage 6 12 held-out cells → Stage 7 safety/diagnostic analysis.

### 4. Target-journal formatting
Formatting should be applied only after the target journal is selected.

## Q1 reviewer risk map

| Issue | Current risk |
|---|---|
| Research question | Low |
| Novelty | Low–moderate |
| Experimental leakage | Low |
| Reproducibility | Low |
| Statistical overclaiming | Low if descriptive wording is retained |
| Architecture breadth | Moderate, transparently acknowledged |
| External validity | Moderate, two-domain limitation |
| Ethics/data governance | High until confirmed |
| Data/code availability | Moderate until immutable archive exists |
| Literature positioning | Low after Stage 9 integration |

## Submission gate

Do not submit until the four author-controlled declarations are closed:
1. ethics/image permission;
2. funding;
3. competing interests;
4. author contributions.

Once those are supplied, the scientific manuscript can move to final language polishing, target-journal formatting, and a simulated Q1 peer review.
