# V19 trigger: original author-curated annotations + computational overlap

Date: 2026-11-21. Owner's existing image annotation/inspection work is accepted. Do NOT request a new reviewer or re-inspect source images.

Run only read-only numeric archival calculations:
- Source Train A/B/C/D ground-truth snapshot: 48 saved original annotation boxes, including seven tags indicating model-assisted annotation in one case.
- Same original frozen model's previously saved V16 four Train inference outputs: 51 predictions. Perform deterministic class + IoU box comparison with explicit 0.20 hosted score floor; report the result as Train-only diagnostics and sensitivity dropping the complete assisted-label image.
- Source overlap calculations from existing 459 original Valid-to-Clean17 verified technical matches and 280 existing original Train–Valid technical comparisons. Summarize M0=459, M1=448, M2=367 and connected high similarity groups without inferring independent site/session origin.
- Fail-closed tests: no Test or Valid inference, no changes to original annotations/model/splits, no fabricated reviewer signoffs or scientific safety claims, no real XAI/energy observations.

See [V19 fixed method](V19_AUTHOR_ANNOTATION_NUMERIC_EVAL_PROTOCOL.md). GitHub Actions should preserve only numerical JSON evidence; keep protected Test untouched.