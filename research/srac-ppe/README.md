# SRAC-PPE | Research progress hub

**Updated:** 2026-10-29  
**Status:** pre-experimental validation / independent worker-level evaluation pending  
**Repository visibility:** PUBLIC — publishable research status only

## Research paper
**Title:** Trustworthy and Risk-Aware Vision Transformers for PPE Compliance Monitoring Under Domain Shift and Limited Data

**Working method:** Shift-aware Risk-Adaptive Calibration for PPE Monitoring (SRAC-PPE).

The paper is a **draft**, not an accepted/published article. Scientific novelty, final statistical claims, and journal suitability remain subject to comparative experimental evaluation.

## Project documents
- [PROJECT.md](PROJECT.md) — canonical status, verified facts, limitations, next gates.
- [MANUSCRIPT_PROGRESS.md](MANUSCRIPT_PROGRESS.md) — current paper sections and submission-readiness gaps.
- [RESEARCH_LOG.md](RESEARCH_LOG.md) — dated, evidence-qualified progress journal.
- [SYNC_PROTOCOL.md](SYNC_PROTOCOL.md) — rules for future GitHub updates and safe publication.
- [EXPERIMENT_PROTOCOL.md](EXPERIMENT_PROTOCOL.md) — prospective, not-yet-frozen experimental protocol.
- [ANNOTATION_CODEBOOK.md](ANNOTATION_CODEBOOK.md) — worker/helmet mandate and independent ground-truth adjudication codebook.
- [DATA_AUDIT_2026-10-29.md](DATA_AUDIT_2026-10-29.md) — verified image/annotation integrity summary and limitations.
- [SCENE_LEAKAGE_AUDIT_2026-10-29.md](SCENE_LEAKAGE_AUDIT_2026-10-29.md) — additional pHash + visually confirmed split-overlap audit.
- [QUARANTINE_CANDIDATES_2026-10-29.csv](QUARANTINE_CANDIDATES_2026-10-29.csv) — reproducible candidate pairs for immutable split-quarantine.
- [tools/phash_overlap_audit.py](tools/phash_overlap_audit.py) — candidate perceptual-duplicate screening.
- [tools/group_independence_gate.py](tools/group_independence_gate.py) — fail-closed source/session grouping integrity gate, with unit tests.
- [NOVELTY_AUDIT.md](NOVELTY_AUDIT.md) — closest prior work and novelty collision points.
- [CODE_AUDIT_2026-10-29.md](CODE_AUDIT_2026-10-29.md) — software metric bug, correction and test status.
- [tools/risk_budget.py](tools/risk_budget.py) — exact finite-sample planning calculator (not empirical performance).

## Frozen starting model
- Roboflow workspace/project: `softyyemen/altayyar-0oflt-lafos-qqauz`
- Model ID: `altayyar-0oflt-lafos-qqauz/2`
- Architecture: RF-DETR Small; original model has 17 classes.
- Model home: https://universe.roboflow.com/softyyemen/altayyar-0oflt-lafos-qqauz

**Do not** treat historical Roboflow metrics or the author's earlier cross-domain YOLO11m results as SRAC-PPE results. A separate harmonized nine-class dataset does not change the frozen model's original 17-class identity.

## Publication/sensitivity policy
This public folder intentionally contains a status snapshot **rather than the full unpublished manuscript or field imagery**. No credentials, private dataset, unpublished result tables, image-level identities, or model weights are mirrored here.

> Research synchronization means explicit verified updates to these files, not automatic streaming of ChatGPT conversation data. See [SYNC_PROTOCOL.md](SYNC_PROTOCOL.md).
