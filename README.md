# Y-PPE Detection Research Repository

> **Latest research — V30 protocol frozen; implementation ready; actual inference pending (22 November 2026):** [V30 progressive XAI protocol](research/seer-ppe/V30_FROZEN_PROGRESSIVE_XAI_PROTOCOL_2026-11-22.md) · [frozen 10-target manifest](research/seer-ppe/V30_FROZEN_TARGETS_2026-11-22.json) · [V30 checkpoint](research/seer-ppe/DUAL_TRACK_CHECKPOINT_2026-11-22_V30.md) · [pre-inference gate](research/seer-ppe/V30_PREINFERENCE_GATE_2026-11-22.json). Manuscript remains v0.27; no V30 model inference or AUC is claimed yet.

> **V30:** Frozen 8×8 target-specific occlusion maps and progressive deletion/insertion protocol for 10 unique targets in eight target-bearing development images; A5/A6 remain eight slots each. Synthetic tests: 9 passed locally and in CI; source/reference readiness passed. Maximum execution budget: 1,068 original-model calls; actual V30 calls so far: 0 (fewer if any target is unrankable). No Test, model, or source-data changes.
>
> **V27:** 10 frozen target detections, 27 original-model passes, 9/10 target detections lost after Gaussian box blur; mean target drop 0.622325 vs control drop 0.008304. A5/A6 each used eight slots; no worker-safety superiority claim.
>
> **V28:** 30 archived repeat passes plus 30 unarchived first-attempt passes; black deletion lost 10/10, target-only insertion retained 7/10. These are one-step box perturbations, not progressive Faithfulness curves.
>
> **V29:** 10 direct hosted timing calls; mean request round-trip 1.5206 s, median 1.469 s. No provider-reported model time, process memory, Joules or financial usage available. Across V27–V29, 97 actual model calls were made; 30 first-attempt V28 outputs were not persisted and are excluded from analysis.

**Researcher:** Ezzaldeen Nabil Ghaleb Obadi Al-Tayar  
**Degree:** Master of Engineering Project Management  
**Institution:** Taiz University, Republic of Yemen

## Project Overview

This repository supports comparative research on AI-assisted Personal Protective Equipment (PPE) compliance monitoring for construction and occupational-safety applications. Two Roboflow projects are intentionally retained because they represent separate trained-model tracks over the Y-PPE data: a YOLOv11 Medium track and an RF-DETR Small track.

## Y-PPE Data

Both public Roboflow projects expose 17 object-detection classes and currently report 5,577 images for the model-linked dataset version. The Universe overview shows 2,327 source images. Generated/versioned image counts must therefore be distinguished from original source-image counts in academic reporting.

## Experimental Track A — YOLOv11 Medium

Public project:

https://universe.roboflow.com/master-fylfq/altayyar-0oflt-lafos-qqauz-ty5nh

- Workspace: `master-fylfq`
- Project: `altayyar-0oflt-lafos-qqauz-ty5nh`
- Model ID: `altayyar-0oflt-lafos-qqauz-ty5nh/1`
- Dataset version: `1`
- Architecture: YOLOv11 Object Detection (Medium)
- Classes: 17
- Roboflow overview metrics: mAP@50 92.2%, Precision 95.3%, Recall 87.2%

## Experimental Track B — RF-DETR Small

Public project:

https://universe.roboflow.com/softyyemen/altayyar-0oflt-lafos-qqauz

- Workspace: `softyyemen`
- Project: `altayyar-0oflt-lafos-qqauz`
- Model ID: `altayyar-0oflt-lafos-qqauz/2`
- Dataset version: `2`
- Architecture: RF-DETR (Small)
- Classes: 17
- Roboflow overview metrics: mAP@50 94.0%, Precision 94.4%, Recall 88.0%

## Publicly Verified Dataset Configuration

The public Roboflow dataset pages report the same configuration for both model-linked dataset versions:

- Total generated images: 5,577
- Train: 4,875 images (88%)
- Validation: 468 images (8%)
- Test: 234 images (4%)
- Preprocessing: Auto-Orient applied
- Resize: Stretch to 640 × 640
- Augmentation outputs per training example: 3
- Mosaic augmentation: applied

## Important Research Note

The two links are deliberately preserved as separate trained-model experiments. Do not overwrite one with the other or report them as a single model. Matching split counts and preprocessing settings strongly improve comparability, but they do not by themselves prove that the exact same image files belong to each train/validation/test partition.

For a defensible head-to-head comparison, verify split membership directly and use a common evaluation protocol. The detailed protocol is documented in `docs/comparison_protocol.md`.

## Run Inference

Install dependencies:

```bash
pip install -r requirements.txt
```

Set your private Roboflow API key as an environment variable.

Windows PowerShell:

```powershell
$env:ROBOFLOW_API_KEY="YOUR_PRIVATE_API_KEY"
```

Linux/macOS:

```bash
export ROBOFLOW_API_KEY="YOUR_PRIVATE_API_KEY"
```

Run YOLOv11 inference:

```bash
python scripts/roboflow_inference.py --model yolo path/to/image.jpg
```

Run RF-DETR inference:

```bash
python scripts/roboflow_inference.py --model rfdetr path/to/image.jpg
```

## Download a Dataset Version

YOLOv11-linked project:

```bash
python scripts/download_dataset.py --project yolo
```

RF-DETR-linked project:

```bash
python scripts/download_dataset.py --project rfdetr
```

The scripts keep the two Roboflow project identifiers separate so their provenance is preserved.

## Verify Identical Train/Validation/Test Membership

After exporting/downloading both dataset versions into separate directories, run:

```bash
python scripts/compare_splits.py path/to/yolo_dataset path/to/rfdetr_dataset
```

The script calculates SHA-256 hashes for image files in each split and reports the intersection and mismatch counts. A strict controlled comparison should show identical membership for train, validation, and test, or both models should be re-evaluated on one common held-out test set.

## Metric Reporting Caution

The RF-DETR Universe overview currently reports mAP@50 = 94.0%. A separate free-text project description mentions 96.2% mAP@50 on an independent test set. The 96.2% figure should not be used as the principal comparison result until its evaluation artifact, test set, and procedure are documented.

## Security

Never commit Roboflow API keys, access tokens, passwords, or `.env` files to GitHub. Use environment variables or GitHub Actions secrets instead.

## Citation and Reporting

When reporting results, cite the exact Roboflow Universe project/model used and record the model ID, dataset version, split, preprocessing/augmentation settings, evaluation thresholds, and date of evaluation. Keep YOLOv11, RF-DETR, and any later XAI results as separate experimental records.

## Current SRAC-PPE Research Progress

The current **Trustworthy and Risk-Aware Vision Transformers for PPE Compliance Monitoring Under Domain Shift and Limited Data** project is tracked in [SRAC-PPE Research Progress Hub](research/srac-ppe/README.md). The canonical, dated status and remaining experimental gates are documented in [PROJECT.md](research/srac-ppe/PROJECT.md). This public tracking page does **not** include the full unpublished manuscript, private data, or model credentials.


### SEER-PPE continuation V04 — 21 November 2026

Latest **read-only** research checkpoint: [source-triage expansion, Train Case D preflight, and safe path gate](research/seer-ppe/DUAL_TRACK_CHECKPOINT_2026-11-21_V04.md). Three further Train↔Valid candidates were AI-screened (no pixel identity verdict); the four Train pilot Eval Cases remain incomplete; original RF-DETR data/model and sealed Test are untouched. [Path-hardened original-byte audit tool](research/seer-ppe/tools/source_pixel_hash_audit.py) has added negative tests, verified passing in [GitHub Actions run 44830713403](https://github.com/EZZALDEEN049/Y-PPE-Detection-RFDETR/actions/runs/44830713403). The actual original-image audit is still pending. **Research scoring gate remains CLOSED**.

### SEER-PPE V05 original Source-byte audit — 21 November 2026

**Verified:** The [six-image original Roboflow Source pilot](research/seer-ppe/SOURCE_ORIGINAL_PIXEL_PILOT_2026-11-21_V01.md) successfully measured real raw SHA-256, decoded RGB SHA-256 and dHash on 3 Train↔Valid pairs. All 6 originals decoded; none of those 3 pairs matched raw bytes or decoded RGB pixels. A [complete 2,093-image Train/Valid original audit](https://github.com/EZZALDEEN049/Y-PPE-Detection-RFDETR/actions/runs/44834307184) was triggered and remained **unverified/in progress at V05 checkpoint**. [V05 checkpoint](research/seer-ppe/DUAL_TRACK_CHECKPOINT_2026-11-21_V05.md). No Test accessed, model or annotations changed, or scoring readiness claimed.

### SEER-PPE V06 — full original Source audit verified (21 November 2026)

The [full read-only original-Source audit](research/seer-ppe/SOURCE_ORIGINAL_FULL_AUDIT_2026-11-21_V01.md) verified **2,093/2,093** Train/Valid originals, 0 missing/decode errors, no byte/RGB-equal Train↔Valid pairs, and **46** perceptually close pairs across 31 Valid images. The [merged 99-Valid-source curator queue](research/seer-ppe/SOURCE_FAMILY_REVIEW_QUEUE_2026-11-21_V06.md), [person-PPE handoff](research/seer-ppe/PERSON_PPE_HUMAN_REVIEW_HANDOFF_2026-11-21_V06.md), [paper v0.8](research/seer-ppe/MANUSCRIPT_MASTER.md) and [V06 checkpoint](research/seer-ppe/DUAL_TRACK_CHECKPOINT_2026-11-21_V06.md) are updated. **Five** previous source holds remain, **19** human worker links preserved, **Test** uninspected, and **scientific scoring not authorized**.

### SEER-PPE V09 — four Train-only conservative Workflow preflight calls completed

The original frozen RF-DETR 17-class model ran through the existing read-only [Conservative Review Cues v0.2 Workflow on four original Train cases](research/seer-ppe/TRAIN_ONLY_UNSCORED_PREFLIGHT_2026-11-21_V09.md). Predictions per case A/B/C/D: 5/16/29/1; person candidates 1/2/4/0. All associations/policies remain UNKNOWN; 19 researcher-approved wearer-item links and 38/42 saved human visual states were preserved ([readback snapshot](research/seer-ppe/PERSON_PPE_REFERENCE_LIVE_SNAPSHOT_2026-11-21_V09.md)). The [V09 remote CI gate passed](research/seer-ppe/GITHUB_ACTIONS_V09_VERIFIED_2026-11-21_V01.md); [paper v0.9](research/seer-ppe/MANUSCRIPT_MASTER.md) and [V09 checkpoint](research/seer-ppe/DUAL_TRACK_CHECKPOINT_2026-11-21_V09.md) are current. **Engineering only:** no mAP/F1/compliance/energy scores, no Test access and no original data/model mutations.
