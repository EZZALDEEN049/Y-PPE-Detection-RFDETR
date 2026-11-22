# V31-A — 11-case original Train–Valid source-lineage reconciliation

**22 November 2026 · Read-only evidence synthesis.** This is not a new image review, not a human acquisition attestation and not a release of any hold. The researcher’s previous general image-review acceptance is preserved; this step only reconciles already archived Train–Valid pair evidence and previously recorded site observations.

## Verified scope

- 11 frozen original Valid Source IDs: **5 historical holds + 6 technical quarantines**.
- The archived V14 evidence contains **33 direct Train-candidate pair records** for these 11 Valid images.
- No raw-byte-identical Train–Valid pair was found in the 11 packets. This does **not** prove independent source acquisition.
- No images were re-opened, no model was run, no Test data accessed, and no source split, annotation or Roboflow object was changed.

## Important source-family reconciliation

The earlier V18 visual triage distinguishes two school sites:

- `IMG-20250416-WA0063.jpg` (Valid) and `IMG-20250416-WA0051.jpg` (Valid) show the named **مدرسة 22 مايو – عصيفرة** site, as do Train `IMG-20250416-WA0067.jpg` and `IMG-20250416-WA0066(1).jpg`. This is a confirmed *named-site cross-split* in the prior visual record. The different photographs/angles and low SSIM do not establish source-family independence. Preserve both Valid holds.
- `IMG-20250416-WA0026.jpg` (Valid) is recorded in the same prior visual triage as **مدرسة الشهيد العلفي**, explicitly a different named site from School 22 May–Aseefrah. Therefore, do **not** group WA0026 with the 22 May school merely because its filename shares the WA prefix. However, its strongest direct Train match is `IMG-20250416-WA0079.jpg`, SSIM **0.93240**, MAE **0.01974**, ORB **756/751**; that separate image-lineage relation is still unresolved. Its historical hold remains in force until a documented conflict-resolution decision.

## Eleven-case technical reconciliation

| Valid original | Strongest Train candidate | SSIM | ORB inliers / matches | Existing status | Evidence interpretation |
|---|---|---:|---:|---|---|
| WA0063 | WA0067 | 0.28551 | 7/12 | Historical hold | Same named 22 May site across Train/Valid; site overlap, not pixel duplicate |
| WA0051 | WA0067 | 0.26785 | 9/11 | Historical hold | Same named 22 May site across Train/Valid |
| WA0026 | WA0079 | 0.93240 | 751/756 | Historical hold | Different named site from 22 May; high image alignment to WA0079 remains unresolved |
| d3febe… | same filename | 0.90125 | 26/34 | Historical hold | High pixel/feature alignment; derivative plausible; raw bytes differ |
| cf8fc… | same filename | 0.82136 | 538/538 | Historical hold | Strong embedding/keypoint alignment but moderate SSIM; do not claim duplicate |
| Safety-Glasses-Toolbox-Talk | image_719 | 0.99757 | 780/780 | Technical quarantine | Extremely high image alignment; same-frame/derivative is a strong hypothesis |
| image_153-1- | image_153 | 0.98378 | 771/775 | Technical quarantine | Very high alignment; dimensions differ, crop/resize plausible |
| h20 | h2 | 0.95548 | 321/350 | Technical quarantine | High alignment; dimensions differ, derivative plausible |
| v141 | v139 | 0.93731 | 0/1 | Technical quarantine | High SSIM but weak ORB corroboration; ambiguous |
| v150 | v149 | 0.92751 | 6/13 | Technical quarantine | Two high-SSIM neighbors; limited feature corroboration |
| v9 | v31 | 0.90881 | 0/5 | Technical quarantine | Borderline SSIM and weak ORB corroboration; ambiguous |

The full machine-readable dossier includes every direct Train candidate for each of the 11 Valid IDs, not only the strongest pair, and retains each pair’s SSIM, MAE, embedding score where available, ORB counts, dimensions, byte-equality status and original technical disposition.

## Current V31-A disposition

1. Keep the **5 historical holds** and **6 technical quarantines** unchanged.
2. Preserve the confirmed 22 May school family across the two Valid and two Train records.
3. Correct the *interpretation* of WA0026: different named school from 22 May, but unresolved high-alignment Train WA0079 relationship. Do not silently release it.
4. Prioritize source-lineage clarification for the very-high-alignment pairs; retain weaker-evidence quarantine cases until the acquisition/session context is resolved.
5. Record a source-family verdict only after an actual author/reviewer attestation identifies site/project, capture session or original source asset and cross-checks the relevant Train group. No verdict can be inferred from SSIM, filename, different image angle, or a generic quality review.

**Status:** `11/11 reconciled against saved technical records; 0/11 newly human-attested; 0 releases; 0 newly eligible for scientific scoring.`

[Machine-readable V31-A dossier](V31_A_SOURCE_LINEAGE_RECONCILIATION_2026-11-22.json) · [Original V14 pair evidence](ORIGINAL_99_VALID_SOURCE_FAMILY_PAIRS_2026-11-21_V14.json) · [V15 signoff packet](SOURCE_FAMILY_EVIDENCE_PRIORITY_11_2026-11-21_V15.json) · [Prior visual site triage](VISUAL_SOURCE_FAMILY_ADJUDICATION_2026-11-18_V01.json)
