# SEER-PPE V35-B — Figure integration report

**Date:** 22 November 2026  
**Canonical manuscript:** v0.37  
**Status:** **PASS — 11 figures integrated and verified against the V34-B manifest**

## 1. Work completed

- Inserted the V34-B aggregate summary heatmap into Results §4.28 as **Figure 1**.
- Inserted all ten target-specific paired heatmaps into Appendix X.1 as **Figures 2–11**.
- Added captions with the exact per-target Spearman ρ, Kendall τ-b and top-four overlap.
- Updated the manuscript version from v0.36 to **v0.37**.
- Updated the remaining-work section to reflect V35-A completion and the V35-B figure integration.

## 2. Verification

| Check | Result |
|---|---|
| Embedded images | 11/11 |
| Image paths resolve in canonical V34-B folder | PASS |
| Captions | 11/11 |
| Figure numbering | Sequential 1–11 |
| Ten target Spearman captions | 10/10 match manifest to four decimals |
| Ten target Kendall captions | 10/10 match manifest to four decimals |
| Ten top-four overlap captions | 10/10 match manifest |
| Summary caption | Matches mean ρ=0.5416, mean τ-b=0.4239 and 65% overlap |
| Root V34-B generation-report link | Verified |

The image references use the canonical manifest-adjacent directory `figures/V34B_2026-11-22/`. The ten target captions preserve the exact target class and Train/Valid image key. Train C and one Valid source each contribute two targets, so the ten maps are not represented as ten independent image acquisitions.

## 3. Canonical figure directory

The canonical directory is `figures/V34B_2026-11-22/`, because this is the directory named by the V34-B manifest, generation report and progress record, and all eleven referenced PNG files are present there. The root PDF in this folder is the canonical PDF reference for later QA.

The same 15-file set also exists in a same-named nested directory. Fourteen duplicate file blobs match exactly; the nested PDF has a different Git blob ID. The nested copy was **retained without modification** rather than silently deleted. Its cleanup or archival is deferred to V35-E after final artifact inspection.

## 4. Scientific boundaries

The inserted maps visualize the existing V34-A perturbation-response analysis. They do not add model calls, new observations, a second annotation source or independent samples. They do not establish causal explanation faithfulness, worker-level compliance, A5/A6 superiority, resolution invariance or external generalization.

No RF-DETR inference, retraining, Test access, image mutation, annotation mutation or split change occurred in V35-B.

## 5. Remaining work

- **V35-C:** complete the reference/DOI/author/venue audit and tighten the related-work and novelty boundary.
- **V35-D:** update the Word-export resource path, export the full v0.37 manuscript, and verify that all eleven images are embedded and editable.
- **V35-E:** inspect Word/PDF layout, figure numbering, captions, links, canonical PDF and duplicate archive handling.

Machine-readable checks: [V35-B figure integration JSON](V35_B_FIGURE_INTEGRATION_2026-11-22.json).
