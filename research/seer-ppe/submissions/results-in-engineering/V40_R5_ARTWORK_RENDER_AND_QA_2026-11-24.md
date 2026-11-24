# V40-R5 — Vector scientific artwork and privacy preflight
Date: 2026-11-24. Internal working candidates; no final submission bundle or Zenodo deposit.

## Implemented
- Renderer: research/seer-ppe/tools/render_v40_r5_publication_figures.py. Inputs are the unchanged V34-A aligned maps and audited V38-B numerical summary. No hosted model requests, retraining or dataset changes.
- Output: artwork-publication/r5/ — four main and ten supplementary one-page PDFs; R5_ARTWORK_QA.json records per-file SHA-256, source hashes, page sizes, minimum text size and identifier scan. Four rendered contact sheets in qa/ are inspection materials, not journal figures.
- First workflow 45322337918 correctly rejected a rasterized colorbar. Second 45322412394 passed structure; rendered contact sheets revealed label/metric collisions in S1–S10 and mean annotations over points in Figure 3. Corrected spacing and annotations, and separated Figure 2 missing targets into their own strip. Third workflow 45322528123: completed/success. All four corrected contact sheets inspected, no remaining evident text collisions at preview scale.
- 14/14 PDFs: no embedded raster images; actual page width 180 mm; min text 8 pt in data plots, 6.63 pt in conceptual Figure 4. Scanned text for source/target IDs and UUID pattern; no match in 14 PDFs. This is figure-level privacy QA, not blanket anonymization of the repository or ethics clearance.
- H01–H10 preserve the original 10-target order and 8 historical image groups (H03/H04 share one image, H08/H09 share another). S1–S10 aligned with these aliases; no raw source IDs in new figures.
- Historical common color scale remains +/-15.470900859749108; 17/800 displayed cells saturated only for display. All correlations/overlap computed from unsaturated values. Historical mean rho 0.5415659018474591, tau 0.4238764616398565, overlap 0.65.
- Extension 48 selected/45 estimable, missing T05/T30/T47; target rho 0.6489788814589973. 14 paired gray/blur means 0.6942587984819544/0.4810924369747899. 11 targets per curve direction; mean deletion/insertion AUC contrast -0.4083778515851475/+0.3719607739808685. No changed numerical results.
- Main source updated to link Figure_1.pdf through Figure_4.pdf in r5 directory; S1 links all ten supplementary PDFs. Exact source reads verified. Main table rows and S1 historical numeric columns preserved. Corrected Figure 3 caption to describe paired scatter (not a plot of differences), and Figure 2 caption to distinguish undefined outcomes and observed ranges from confidence intervals.

## Evidence
Run: https://github.com/EZZALDEEN049/Y-PPE-Detection-RFDETR/actions/runs/45322528123
Source updates: manuscript 9f94917970eb3eb288f321d4c2e9e4bc0f4590d9; S1 dfcb8e445df7b1f4ae422f421e5f717e31141049; compliance matrix 0baf67a541cfbab003ed1ae63dfa7209bab48eeb.
Retain original source files and prior figure versions without modification. Final Word embedding/export must use the new r5 PDF files rather than previous internal candidate archive, and preserve separate vector artwork. Need final publication-size visual proof, author approval of Figure 4, official portal file-format confirmation, rights/prior-artwork review and all existing institutional and archival gates. No graphical abstract generated in this pass; it remains a separate optional task. No final package requested or produced.
