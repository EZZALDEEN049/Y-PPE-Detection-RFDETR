# Y-PPE Detection Research Repository

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

## Important Research Note

The two links are deliberately preserved as separate trained-model experiments. Do not overwrite one with the other or report them as a single model. For a defensible head-to-head comparison, verify that train/validation/test splits, preprocessing, augmentation, evaluation thresholds, and metric definitions are identical. Roboflow overview metrics are recorded here as platform-reported values and should not automatically be treated as the final paper comparison table without that verification.

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

## Security

Never commit Roboflow API keys, access tokens, passwords, or `.env` files to GitHub. Use environment variables or GitHub Actions secrets instead.

## Citation and Reporting

When reporting results, cite the exact Roboflow Universe project/model used and record the model ID, dataset version, split, preprocessing/augmentation settings, evaluation thresholds, and date of evaluation. Keep YOLOv11, RF-DETR, and any later XAI results as separate experimental records.
