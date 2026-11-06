# SEER-PPE clean17 file-integrity audit request — 2026-11-06

Run the dedicated metadata-only GitHub Actions workflow to reconstruct from the immutable unaugmented cloned dataset `master-fylfq/altayyar-0oflt-lafos-qqauz-ty5nh/2`, apply the 39 documented exclusions and label-row corrections, and independently report 2,288 clean images / 16,300 object labels across train/valid/test. Do not train a model, upload raw photos, or publish credentials. Source/site group independence and independent human adjudication stay OPEN even if file integrity passes.

## Audit retry — 2026-11-06

Run 2 validates both standard detection boxes and normalized polygon vertex sequences. The first audit correctly reconstructed 2,288 images and 16,300 object annotations but its original *new* parser falsely rejected mixed polygon rows; this retry fixes the parser without changing raw data or the historical correction manifests.
