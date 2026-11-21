# SEER-PPE V12 — Verified provisional Valid-to-Clean17 candidate mapping

**21 November 2026; real metadata-only execution, not model scoring.**

The exact original-Source and Clean17 historical metadata artifacts were downloaded into a temporary GitHub Actions runner, and 468 original Valid Source IDs were compared to 459 Clean17 Valid export filenames (no Test photo bytes). The result contains **426 distinct normalized-name candidates**, **33 previously ambiguous names with an unambiguous closest dHash candidate**, and **9 historically excluded images without a Clean17 name match**. The 459 candidate assignments cover exactly 459 distinct Clean17 Valid export filenames.

For all 33 ambiguous cases, nearest-vs-second-nearest dHash margin was at least **15**, and maximum nearest dHash distance was **6**. Such metadata evidence is **not a verified source image identity or an independently signed Clean17 membership**. The original/export image bytes did not match as raw SHA, and the source/clean pixel-hash conventions and resize/encoding paths differ. The only authorized classification here is *candidate*, never *verified*.

All five previous Valid research holds remain in place; 0 per-image source-independence human signoffs were added; no Test photo, original dataset, annotation, split or RF-DETR model was touched. **Scientific scoring remains blocked**. Future exact identity confirmation requires a documented image-content or acquisition-lineage check, without rewriting the protected Test.

[JSON source-ID ledger](SEER_PPE_VALID_TO_CLEAN17_PROVISIONAL_V12.json) · [CSV overview](SEER_PPE_VALID_TO_CLEAN17_PROVISIONAL_V12.csv) · [Reproducible ranking code](tools/refine_valid_clean17_candidates_v12.py) · [V12 initial hash/name run](https://github.com/EZZALDEEN049/Y-PPE-Detection-RFDETR/actions/runs/44842423862).
