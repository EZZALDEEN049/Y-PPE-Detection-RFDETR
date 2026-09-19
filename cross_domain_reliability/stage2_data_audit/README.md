# Stage 2 — Data, Annotation, and Leakage Audit

**Status:** documentary checks are complete; the raw-data audit is still open.

Stage 2 must be closed before any harmonized baseline, zero-shot transfer, calibration, or adaptation experiment is treated as valid.

## What this stage checks

- image/label pairing and orphan labels;
- malformed YOLO annotation rows;
- class-ID validity;
- normalized box geometry and out-of-image boxes;
- duplicate annotation rows and nearly identical same-class boxes;
- exact image duplication across `train`, `val`, and `test` using SHA-256;
- decoded-pixel exact duplication across splits;
- perceptual near-duplicate candidates using dHash;
- filename/stem overlap across splits;
- source-URL, site, project, or video-group leakage when such metadata exist;
- semantic compatibility of the primary missing-PPE classes before ontology freeze.

## Important rule on class order

Do **not** infer numeric class IDs from a list of class names. The authoritative numeric order must come from each dataset's actual `data.yaml` (or equivalent source metadata). Until that file is available, audit by `--num-classes` only; output classes will be named `class_0`, `class_1`, etc.

## Primary strict mapping to be audited

| Y-PPE | Construction-PPE |
|---|---|
| Persons | Person |
| Hard Hat | helmet |
| Gloves | gloves |
| Safety Vests | vest |
| Safety Boots | boots |
| Goggles | goggles |
| No Hard Hat | no_helmet |
| No Gloves | no_gloves |
| No Safety Boots | no_boots |

`No Safety Vest`, `no_goggle`, and `none` are not included in the strict 9-class primary mapping because no direct counterpart is currently established.

## Run the audit

Install dependencies:

```bash
pip install -r requirements.txt
```

Preferred command when `data.yaml` is available:

```bash
python stage2_dataset_audit.py \
  --dataset-name Y-PPE \
  --root /path/to/y-ppe \
  --data-yaml /path/to/y-ppe/data.yaml \
  --out outputs/y-ppe
```

If the dataset metadata are not yet available but the number of classes is known:

```bash
python stage2_dataset_audit.py \
  --dataset-name Y-PPE \
  --root /path/to/y-ppe \
  --num-classes 17 \
  --out outputs/y-ppe
```

The script is read-only. It produces:

- `summary.json`
- `image_manifest.json`
- `issues.json`

It exits with code `2` when critical integrity/leakage problems are detected.

## Stage 2 pass gate

The primary Y-PPE ↔ Construction-PPE experiment may proceed only when:

1. both raw annotation audits pass or documented corrections are completed;
2. no unresolved exact cross-split duplicates remain;
3. perceptual near-duplicate candidates are manually adjudicated;
4. numeric class-ID order is frozen from actual dataset metadata;
5. the missing-PPE geometry/policy audit is completed for `no_helmet`, `no_gloves`, and `no_boots` counterparts;
6. harmonized per-class split counts are exported and frozen.

SH17 is secondary and does not block the primary experiment once the two primary datasets pass.
