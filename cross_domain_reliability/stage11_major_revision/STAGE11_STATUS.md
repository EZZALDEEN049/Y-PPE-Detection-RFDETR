# Stage 11 Major-Revision Status

## Completed
- Stage 11A: exact/near-duplicate and scene-dependence audit plus strict/conservative sensitivity evaluation.
- Stage 11B: separation of in-domain safety-class learnability from additional transfer degradation.
- Stage 11C: full semantic harmonization and Stage 4.5 filtering reproducibility specification.
- Stage 11E: image-cluster bootstrap intervals for safety-class recall and consensus false-negative rates.
- Stage 11F: literature expansion, novelty reframing, and figure-numbering repair.
- Stage 11G: data/code availability, image-governance wording, highlights, cover letter, and submission-positioning cleanup.
- Stage 11H: verified literature deepening with construction-PPE, dataset-bias, domain-adaptation, and natural-shift references; reference list expanded to 29 sources.
- Stage 11I: terminology aligned with the frozen ontology guardrail; no_helmet/no_gloves/no_boots are described as dataset-defined PPE-negative-state classes rather than automatically as normative safety violations.

## Pending inference-only checks
1. Stage 11D: validation-selected best.pt checkpoint sensitivity.
2. Stage 11E2: image-level bootstrap for mAP50:95/domain-gap uncertainty.

Neither pending check requires model retraining.

## Submission gate
Do **not** create the final immutable submission tag or final journal-upload package until Stage 11D and Stage 11E2 outputs are complete and incorporated.

## Current manuscript
Use:
`paper_draft/MANUSCRIPT_STAGE11I.md`

until the two pending inference-only checks are complete.
