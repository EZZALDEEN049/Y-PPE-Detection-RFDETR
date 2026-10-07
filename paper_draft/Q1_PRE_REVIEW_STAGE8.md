# Stage 8 — Strict Q1 Pre-Review

## Editorial recommendation at current state
**Major Revision before journal submission.**

The experimental core is now coherent and publication-relevant, but the manuscript is not yet submission-ready because several reporting and positioning requirements remain incomplete.

## Major issues

### 1. Literature positioning and novelty are not yet demonstrated
The current manuscript intentionally leaves the literature-review citations incomplete. Before submission, the Introduction and Related Work must establish:
- what prior PPE studies report under same-domain evaluation;
- which prior studies perform external/cross-dataset validation;
- whether any prior PPE work uses multi-seed bidirectional cross-domain testing;
- how safety-critical false-negative analysis differs from conventional mAP reporting.

Without this evidence, novelty cannot yet be defended.

### 2. Dataset provenance, licensing, and annotation semantics must be explicit
The manuscript must document:
- original source and license/permission for each dataset;
- how the nine harmonized classes were mapped from the original taxonomies;
- whether the positive/negative PPE labels have equivalent annotation semantics across domains;
- all exclusions introduced during harmonization.

This is essential because annotation-policy mismatch is a plausible contributor to cross-domain failure.

### 3. Training configuration needs exact reproducible reporting
The six completed YOLO11m runs must be described using values taken from the actual frozen manifests/logs, including all available items such as:
- pretrained initialization;
- optimizer and learning-rate schedule;
- batch size;
- augmentation settings;
- epoch count;
- image size;
- software versions;
- hardware;
- deterministic settings.

No value should be inferred or reconstructed from memory.

### 4. Revised scope must be transparent
The original 2-architecture plan was not completed. The final paper must state that incomplete RF-DETR runs were excluded before the final held-out analysis and must avoid any architecture-superiority claim.

### 5. Statistical claims must remain bounded
Three seeds support descriptive reproducibility, not broad population-level inference. Mean ± SD and seed-level paired gaps are defensible. Strong significance language should be avoided unless an additional prespecified inferential analysis is added.

### 6. Safety-class interpretation requires denominator visibility
The manuscript should report the number of ground-truth objects for each safety class alongside recall/FNR so that readers can distinguish severe failure from unstable estimates caused by small support. The Stage 7B consensus table already provides these denominators and should be retained.

## Minor issues

- Use one notation consistently: mAP50:95 or mAP@0.50:0.95.
- Clearly distinguish the AP confidence floor (0.001) from the fixed safety operating threshold (0.25).
- State that the stored 640×640 geometry is a property of the frozen derivatives and does not imply the original source images shared identical acquisition geometry.
- Avoid describing class imbalance or object size as the confirmed cause of domain shift.
- Report the exact definition of small/medium/large normalized area bins because these are study-specific, not COCO area categories.
- Label inference timing as descriptive only unless hardware is controlled and fully reported.
- In figures, show error bars only where they represent across-seed variability and define SD in captions.

## Strengths that should be preserved

- protocol frozen before held-out evaluation;
- final-epoch checkpoint policy fixed across all six models;
- no post-test threshold tuning;
- bidirectional cross-domain evaluation;
- three independent seeds per source domain;
- safety-focused fixed operating-point analysis;
- deterministic, non-cherry-picked consensus failure audit;
- explicit distinction between association and causality in the diagnostic analysis.

## Submission gate

The manuscript should not be submitted until the following are complete:
1. literature review and citation integration;
2. exact dataset provenance/licensing and harmonization description;
3. exact Stage 5 training configuration from frozen evidence;
4. final figures/captions and table numbering;
5. funding, competing interests, author contributions, and data/code availability wording;
6. final consistency audit against repository outputs.
