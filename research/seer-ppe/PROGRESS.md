# SEER-PPE active progress tracker — v0.4 (2026-11-06)

| Step | Deliverable | Verified status | Remaining gate |
|---|---|---|---|
| 01 | Research question and protocol | DESIGN COMPLETE | Novelty and journal confirmation |
| 02 | ALTAYYAR hosted 17-class inference + routing prototype | ENGINEERING COMPLETE; 3 smoke images, 23 prior unit tests | Local gradient-XAI |
| 03 | Image-independence and identity-matching utilities | ENGINEERING COMPLETE; 40 prior tests | Execute on actual clean17 files |
| **04A** | Complete raw Roboflow original metadata audit | **DONE:** 2,327/2,327 IDs scanned, 31 cross-split filename groups, person/helmet support quantified | Filename flags need image review |
| **04B** | Pilot review preparation | **DONE:** 30 dev images selected (16 train, 14 valid); 396 saved boxes geometry checked, 89 model-assisted metadata | Check clean17 membership and rights; blind A/B annotation |
| **04C** | Physical clean17 archive frozen, SHA and site group independence | **OPEN:** prior CI reports 2,288 images; physical ZIP unavailable to hash | Acquire package, source groups, run audit |
| 05 | Validated worker-level expert GT | OPEN, **0 adjudications** | Annotator A/B + expert reconcile |
| 06 | Local detector XAI and fidelity | OPEN | Download/load exact checkpoint, differentiable forward |
| 07 | Hardware electrical energy measurement | OPEN | Instrument device, capture watt traces |
| 08 | Prespecified calibration and final test | OPEN | Lock source-independent final test after audit |
| 09 | New empirical results/figures | NOT RUN | Real safe evaluation only |

**Current artifact:** `PHASE4_REPORT.md` and `evidence/PHASE4_INDEX_AUDIT_2026-11-06.json`; companion *private* 30-image pilot CSV queues. Do not commit image binaries or potential third-party photos to GitHub. Original dataset, its historical model and all prior papers remain unchanged.
