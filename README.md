# Y-PPE Detection Research Repository

**Researcher:** Ezzaldeen Nabil Ghaleb Obadi Al-Tayar  
**Degree:** Master of Engineering Project Management  
**Institution:** Taiz University, Republic of Yemen

## Project Overview

This repository supports research on AI-assisted Personal Protective Equipment (PPE) compliance monitoring for construction and occupational-safety applications. The project uses a transformer-based RF-DETR object detector and supports the broader research direction of explainable AI and risk-aware safety monitoring.

## Y-PPE Dataset

The associated Y-PPE dataset contains 17 object-detection classes covering PPE, non-compliance categories, persons, contextual hazards, and related worksite objects.

The Roboflow Universe overview contains 2,327 source images. Dataset Version 2 contains 5,577 generated images after preprocessing/augmentation, split into 4,875 training, 468 validation, and 234 test images.

## Roboflow Universe

Public project:

https://universe.roboflow.com/softyyemen/altayyar-0oflt-lafos-qqauz

**Universe workspace:** `softyyemen`  
**Roboflow project:** `altayyar-0oflt-lafos-qqauz`  
**Published inference model:** `altayyar-0oflt-lafos-qqauz/2`  
**Dataset version:** `2`  
**Task:** Object Detection  
**Hosted architecture:** RF-DETR (Small)  
**Classes:** 17

Roboflow currently reports 94.0% mAP@50, 94.4% precision, and 88.0% recall on the public project overview. Any metric used in a research paper should be tied explicitly to the relevant dataset version, split, and experiment record.

## Run Roboflow Inference

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Set your Roboflow API key as an environment variable.

Windows PowerShell:

```powershell
$env:ROBOFLOW_API_KEY="YOUR_PRIVATE_API_KEY"
```

Linux/macOS:

```bash
export ROBOFLOW_API_KEY="YOUR_PRIVATE_API_KEY"
```

3. Run inference:

```bash
python scripts/roboflow_inference.py path/to/image.jpg
```

The inference script calls the deployed RF-DETR (Small) model `altayyar-0oflt-lafos-qqauz/2` through Roboflow Serverless Inference.

## Download the Dataset

After setting `ROBOFLOW_API_KEY`, run:

```bash
python scripts/download_dataset.py
```

The download script uses the public Universe workspace/project slug shown above and Dataset Version 2. The current export format remains YOLOv11 for interoperability; for local RF-DETR training, a COCO-format export is generally preferable and can be added as a separate training pipeline.

## Security

Never commit Roboflow API keys, access tokens, passwords, or `.env` files to GitHub. Use environment variables or GitHub Actions secrets instead.

## Citation

When using the public dataset/model, cite the Roboflow Universe project and the relevant thesis/publication. Keep source-image counts, generated dataset counts, model metrics, experimental splits, and XAI results explicitly separated in academic reporting.
