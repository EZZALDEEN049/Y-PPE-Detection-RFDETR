# Y-PPE Detection Research Repository

**Researcher:** Ezzaldeen Nabil Ghaleb Obadi Al-Tayar  
**Degree:** Master of Engineering Project Management  
**Institution:** Taiz University, Republic of Yemen

## Project Overview

This repository supports research on AI-assisted Personal Protective Equipment (PPE) compliance monitoring for construction and occupational-safety applications. The broader research direction investigates transformer-based detection, including RF-DETR, together with explainability and risk-management considerations.

## Y-PPE Dataset

The associated Y-PPE dataset contains 17 object-detection classes covering PPE, non-compliance categories, persons, contextual hazards, and related worksite objects.

## Roboflow Universe

The current public Roboflow project is available here:

https://universe.roboflow.com/master-fylfq/altayyar-0oflt-lafos-qqauz-ty5nh

**Roboflow project:** `altayyar-0oflt-lafos-qqauz-ty5nh`  
**Published model version:** `altayyar-0oflt-lafos-qqauz-ty5nh/1`  
**Task:** Object Detection  
**Current hosted model:** YOLOv11 Medium

> Important: the model currently published on Roboflow Universe is a YOLOv11m model. This repository's wider research direction includes RF-DETR; the two should not be reported as the same trained model unless an RF-DETR experiment has been separately trained and validated.

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

## Download the Dataset

After setting `ROBOFLOW_API_KEY`, run:

```bash
python scripts/download_dataset.py
```

The download script uses workspace `master-fylfq`, project `altayyar-0oflt-lafos-qqauz-ty5nh`, version `1`, and exports the dataset in YOLOv11 format.

## Security

Never commit Roboflow API keys, access tokens, passwords, or `.env` files to GitHub. Use environment variables or GitHub Actions secrets instead.

## Citation

When using the public Roboflow dataset/model, cite the Roboflow Universe project page and the relevant research publication/thesis as appropriate. Keep dataset, baseline-model, RF-DETR, and XAI results clearly separated in academic reporting.
