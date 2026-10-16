# Actual Y-PPE paired-export preflight: evidence record 2026-10-17

**Execution:** GitHub Actions run 38981711922, commit 222ec21cf16f067da573e9408b6037430537376f.
**Artifact:** sustainable-cv-paired-export-aggregate-preflight, ID 12080879506,
ZIP SHA-256: 6ccfaaafc61dc8963e20ee4e4704bc5b6fb878db7f425c158a2408277a080067.
**Method:** paired_export_audit.py, split_integrity.py, pinned Roboflow 1.5.0 / PyYAML 6.0.3.
**Scope:** actual exported YOLO11m-linked Y-PPE v1 (A) and RF-DETR Small-linked
Y-PPE v2 (B). Models were NOT executed or compared on a common evaluator.

## Reproduced aggregate observations

| Outcome | Export A | Export B |
|---|---:|---:|
| train image files | 4,875 | 4,875 |
| distinct train exported-image SHA-256 hashes | 4,873 | 4,873 |
| valid image files | 468 | 468 |
| test image files | 234 | 234 |
| classes | 17 | 17 |
| exact-byte train vs test overlapping distinct hashes (within export) | 1 | 1 |

- Both exported ontology class-name orders are textually equal (17 classes).
- Exact exported-byte hash **multisets** compare equal for validation and test,
  but **not** for training.
- Same-split matching distinct exported-byte hashes: train **1,623**, valid
  **468**, test **234**.
- The held-out test set has 234 matched distinct image-byte hashes.
- After normalizing standard YOLO rows and polygons to axis-aligned boxes, all
  held-out annotation files were parseable.
- Test annotation parsing counted 1,099 box rows and 32 polygon rows in each
  export.
- **Twelve matched distinct test-image byte-hash groups have differing
  canonicalized annotation signatures.**
- There is one exact-image byte hash shared between training and test *within
  each export*. Cross-project discordant-split scans also show one shared hash
  in A_train/B_test and one in A_test/B_train (counts of intersections, not a
  claim that these represent two separate original scenes).

## Interpretation and limitations

**Gate status: BLOCKED for controlled architectural accuracy comparison.**

(1) Equal test image bytes do not establish equal ground-truth annotations.
The 12 signature mismatches may reflect numeric formatting differences,
box geometry, class policy or other labeling differences. Without controlled
adjudication, do not call them 12 substantive labeling *errors*.

(2) An exact byte-identical image crossing train and test is direct exported
partition leakage evidence. Do not infer how many source sites/scenes overlap
from one hash group. Also investigate near duplicates and augmented variants.

(3) Only 1,623 shared distinct train exported hashes despite equal file counts
reflect substantial nonidentity of *exported bytes*. This does NOT by itself
prove distinct original source images, because augmentations can change bytes.

(4) Both pretrained/fine-tuned detectors still need to be run under one frozen
held-out ground-truth ontology and one common evaluator for any controlled
performance claim. No inference latency, local memory, power, joules/image,
CO2e or deployment advantage is demonstrated.

## Mandatory next adjudication gates

1. Select one version-controlled held-out test ground truth set with explicit
   permissions, independent source-group provenance and no overlap with
   training in either track, before any combined comparison.
2. Privately inspect the **12** test-label signature differences and classify
   their severity (precision-only vs genuine coordinates/class changes),
   reporting only aggregate class/geometry discrepancy counts.
3. Track and resolve the train/test exact-image cross-split hash group; run
   independent source-level, near-duplicate and video/site grouping checks.
4. Freeze ontology, evaluator, confidence, IoU and test group definition.
5. Verify local access to the EXACT two fine-tuned model versions separately
   from the six different nine-class YOLO checkpoints in EcoSafe.
6. Only then conduct matched-hardware inference and optionally calibrated
   power measurement, without retraining.

Raw images, image filenames, image hashes, annotations and API keys are
intentionally absent from this public evidence record.
