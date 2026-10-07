#!/usr/bin/env python3
"""Stage 6: frozen held-out cross-domain evaluation for completed YOLO11m runs.

Evaluation only. This script performs no training, fine-tuning, adaptation,
checkpoint selection, or threshold tuning.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
import torch
import yaml
from ultralytics import YOLO

CLASSES = [
    "person", "helmet", "gloves", "vest", "boots", "goggles",
    "no_helmet", "no_gloves", "no_boots",
]
SAFETY_CLASSES = {"no_helmet", "no_gloves", "no_boots"}

Y_FP = "82c08766d5c5e50e93d41d21c4751fd686a3932ea6a8cb24ffd2838d9e30fba8"
C_FP = "59469299ba67355dbcb0e725851f73d244a7ad6e93522d44601be3c8323d3c14"

RUNS = [
    ("Y_YOLO_s17", "Y", 17),
    ("Y_YOLO_s42", "Y", 42),
    ("Y_YOLO_s2026", "Y", 2026),
    ("C_YOLO_s17", "C", 17),
    ("C_YOLO_s42", "C", 42),
    ("C_YOLO_s2026", "C", 2026),
]


def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage5-root", required=True, type=Path,
                    help="Directory containing the six completed Stage5 run folders.")
    ap.add_argument("--y-data", required=True, type=Path,
                    help="Frozen Y-PPE-h9-v2 data.yaml")
    ap.add_argument("--c-data", required=True, type=Path,
                    help="Frozen Construction-PPE-h9-v2 data.yaml")
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--device", default="0",
                    help="Ultralytics device, e.g. 0 or cpu")
    ap.add_argument("--batch", type=int, default=8)
    ap.add_argument("--imgsz", type=int, default=640)
    ap.add_argument("--ap-conf", type=float, default=0.001)
    ap.add_argument("--operating-conf", type=float, default=0.25)
    ap.add_argument("--nms-iou", type=float, default=0.70)
    ap.add_argument("--match-iou", type=float, default=0.50)
    ap.add_argument("--preflight-only", action="store_true",
                    help="Verify frozen inputs/checkpoints without touching held-out test inference.")
    return ap.parse_args()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def write_runtime_yaml(source_yaml: Path, out_yaml: Path) -> Path:
    """Write a path-only adapter YAML with absolute split paths.

    Dataset bytes, labels, class order, and split membership are unchanged.
    """
    data = read_yaml(source_yaml)
    root = Path(data.get("path", "."))
    if not root.is_absolute():
        root = (source_yaml.parent / root).resolve()
    runtime = {
        "path": str(root),
        "train": str((root / data["train"]).resolve()) if not Path(data["train"]).is_absolute() else data["train"],
        "val": str((root / data["val"]).resolve()) if not Path(data["val"]).is_absolute() else data["val"],
        "test": str((root / data["test"]).resolve()) if not Path(data["test"]).is_absolute() else data["test"],
        "names": CLASSES,
        "nc": 9,
    }
    out_yaml.parent.mkdir(parents=True, exist_ok=True)
    out_yaml.write_text(yaml.safe_dump(runtime, sort_keys=False), encoding="utf-8")
    return out_yaml


def validate_stage5_inputs(stage5_root: Path) -> dict:
    expected_dataset = {"Y": "Y-PPE-h9-v2", "C": "Construction-PPE-h9-v2"}
    verified = []
    for run_id, train_domain, seed in RUNS:
        run_dir = stage5_root / run_id
        manifest = run_dir / "run_manifest_post.json"
        weights = run_dir / "train" / "weights" / "last.pt"
        if not manifest.is_file():
            raise FileNotFoundError(f"Missing Stage 5 post manifest: {manifest}")
        if not weights.is_file():
            raise FileNotFoundError(f"Missing final-epoch checkpoint: {weights}")
        meta = json.loads(manifest.read_text(encoding="utf-8"))
        checks = {
            "status": meta.get("status") == "training_completed",
            "run_id": meta.get("run_id") == run_id,
            "dataset": meta.get("dataset") == expected_dataset[train_domain],
            "model": meta.get("model") == "YOLO11m",
            "seed": int(meta.get("seed")) == seed,
            "epochs": int(meta.get("epochs")) == 100,
            "resolution": int(meta.get("resolution")) == 640,
            "primary_checkpoint_policy": meta.get("primary_checkpoint_policy") == "final_epoch",
            "heldout_not_used": meta.get("test_evaluation_performed") is False,
        }
        bad = [k for k, ok in checks.items() if not ok]
        if bad:
            raise RuntimeError(f"Stage 5 manifest validation failed for {run_id}: {bad}")
        verified.append({
            "run_id": run_id,
            "train_domain": train_domain,
            "seed": seed,
            "checkpoint": str(weights.resolve()),
            "checkpoint_size_bytes": weights.stat().st_size,
            "manifest": str(manifest.resolve()),
        })
    return {"verified_runs": verified}


def read_yaml(path: Path) -> dict:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    names = data.get("names")
    if isinstance(names, dict):
        names = [names[k] for k in sorted(names, key=lambda x: int(x))]
    if list(names or []) != CLASSES:
        raise RuntimeError(f"Class order mismatch in {path}: {names}")
    return data


def resolve_split(yaml_path: Path, split: str = "test") -> Path:
    data = read_yaml(yaml_path)
    root = Path(data.get("path", "."))
    if not root.is_absolute():
        root = (yaml_path.parent / root).resolve()
    target = data.get(split)
    if not isinstance(target, str):
        raise RuntimeError(f"Expected string '{split}' entry in {yaml_path}")
    p = Path(target)
    return p if p.is_absolute() else (root / p).resolve()


def image_files(split_path: Path) -> List[Path]:
    exts = {".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff", ".webp"}
    if split_path.is_file():
        rows = [Path(x.strip()) for x in split_path.read_text().splitlines() if x.strip()]
        return rows
    return sorted(p for p in split_path.rglob("*") if p.is_file() and p.suffix.lower() in exts)


def label_path_for_image(image_path: Path) -> Path:
    parts = list(image_path.parts)
    idxs = [i for i, v in enumerate(parts) if v == "images"]
    if not idxs:
        raise RuntimeError(f"Cannot infer label path (no 'images' segment): {image_path}")
    parts[idxs[-1]] = "labels"
    return Path(*parts).with_suffix(".txt")


def load_gt_xyxy(label_path: Path, w: int, h: int) -> Tuple[np.ndarray, np.ndarray]:
    classes, boxes = [], []
    if not label_path.exists():
        return np.empty((0,), dtype=int), np.empty((0, 4), dtype=float)
    for line in label_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        vals = line.split()
        if len(vals) < 5:
            continue
        c = int(float(vals[0]))
        cx, cy, bw, bh = map(float, vals[1:5])
        x1 = (cx - bw / 2.0) * w
        y1 = (cy - bh / 2.0) * h
        x2 = (cx + bw / 2.0) * w
        y2 = (cy + bh / 2.0) * h
        classes.append(c)
        boxes.append([x1, y1, x2, y2])
    return np.asarray(classes, dtype=int), np.asarray(boxes, dtype=float).reshape(-1, 4)


def iou_one_to_many(box: np.ndarray, boxes: np.ndarray) -> np.ndarray:
    if boxes.size == 0:
        return np.empty((0,), dtype=float)
    x1 = np.maximum(box[0], boxes[:, 0])
    y1 = np.maximum(box[1], boxes[:, 1])
    x2 = np.minimum(box[2], boxes[:, 2])
    y2 = np.minimum(box[3], boxes[:, 3])
    inter = np.maximum(0.0, x2 - x1) * np.maximum(0.0, y2 - y1)
    a = np.maximum(0.0, box[2] - box[0]) * np.maximum(0.0, box[3] - box[1])
    b = np.maximum(0.0, boxes[:, 2] - boxes[:, 0]) * np.maximum(0.0, boxes[:, 3] - boxes[:, 1])
    union = a + b - inter
    return np.divide(inter, union, out=np.zeros_like(inter), where=union > 0)


def update_counts(
    gt_cls: np.ndarray, gt_boxes: np.ndarray,
    pred_cls: np.ndarray, pred_boxes: np.ndarray, pred_conf: np.ndarray,
    counts: Dict[int, Dict[str, int]], match_iou: float,
) -> None:
    for c in range(len(CLASSES)):
        gi = np.where(gt_cls == c)[0]
        pi = np.where(pred_cls == c)[0]
        gboxes = gt_boxes[gi]
        order = pi[np.argsort(-pred_conf[pi])] if len(pi) else np.empty((0,), dtype=int)
        used = set()
        for pidx in order:
            ious = iou_one_to_many(pred_boxes[pidx], gboxes)
            best_local = -1
            best_iou = -1.0
            for j, v in enumerate(ious):
                if j not in used and v > best_iou:
                    best_iou = float(v)
                    best_local = j
            if best_local >= 0 and best_iou >= match_iou:
                counts[c]["tp"] += 1
                used.add(best_local)
            else:
                counts[c]["fp"] += 1
        counts[c]["fn"] += max(0, len(gboxes) - len(used))


def safe_prf(tp: int, fp: int, fn: int) -> Tuple[float, float, float]:
    p = tp / (tp + fp) if (tp + fp) else 0.0
    r = tp / (tp + fn) if (tp + fn) else 0.0
    f1 = 2 * p * r / (p + r) if (p + r) else 0.0
    return p, r, f1


def fixed_operating_point(
    model: YOLO, test_images: List[Path], device: str, imgsz: int,
    conf: float, nms_iou: float, match_iou: float,
) -> dict:
    counts = defaultdict(lambda: {"tp": 0, "fp": 0, "fn": 0})
    results = model.predict(
        source=[str(p) for p in test_images],
        conf=conf,
        iou=nms_iou,
        imgsz=imgsz,
        device=device,
        verbose=False,
        stream=True,
        augment=False,
    )
    for res in results:
        h, w = res.orig_shape
        ip = Path(res.path).resolve()
        gt_cls, gt_boxes = load_gt_xyxy(label_path_for_image(ip), w, h)
        if res.boxes is None or len(res.boxes) == 0:
            pred_cls = np.empty((0,), dtype=int)
            pred_boxes = np.empty((0, 4), dtype=float)
            pred_conf = np.empty((0,), dtype=float)
        else:
            pred_cls = res.boxes.cls.detach().cpu().numpy().astype(int)
            pred_boxes = res.boxes.xyxy.detach().cpu().numpy().astype(float)
            pred_conf = res.boxes.conf.detach().cpu().numpy().astype(float)
        update_counts(gt_cls, gt_boxes, pred_cls, pred_boxes, pred_conf, counts, match_iou)

    per_class = {}
    total = {"tp": 0, "fp": 0, "fn": 0}
    for c, name in enumerate(CLASSES):
        d = counts[c]
        p, r, f1 = safe_prf(d["tp"], d["fp"], d["fn"])
        per_class[name] = {**d, "precision": p, "recall": r, "f1": f1}
        for k in total:
            total[k] += d[k]
    mp, mr, mf1 = safe_prf(total["tp"], total["fp"], total["fn"])
    macro = {
        "precision": float(np.mean([v["precision"] for v in per_class.values()])),
        "recall": float(np.mean([v["recall"] for v in per_class.values()])),
        "f1": float(np.mean([v["f1"] for v in per_class.values()])),
    }
    return {
        "micro": {**total, "precision": mp, "recall": mr, "f1": mf1},
        "macro": macro,
        "per_class": per_class,
        "safety_fn": {k: per_class[k]["fn"] for k in sorted(SAFETY_CLASSES)},
    }


def metrics_to_dict(metrics) -> dict:
    box = metrics.box
    maps = [float(x) for x in box.maps]
    ap50 = getattr(box, "ap50", None)
    if ap50 is not None:
        ap50 = [float(x) for x in np.asarray(ap50).reshape(-1)]
    return {
        "map50_95": float(box.map),
        "map50": float(box.map50),
        "map75": float(box.map75),
        "per_class_ap50_95": {CLASSES[i]: maps[i] for i in range(min(len(maps), len(CLASSES)))},
        "per_class_ap50": (
            {CLASSES[i]: ap50[i] for i in range(min(len(ap50), len(CLASSES)))}
            if ap50 is not None else None
        ),
        "speed_ms_per_image": {k: float(v) for k, v in (metrics.speed or {}).items()},
    }


def main() -> None:
    a = parse_args()
    a.stage5_root = a.stage5_root.resolve()
    a.out = a.out.resolve()
    a.out.mkdir(parents=True, exist_ok=True)
    y_data, c_data = a.y_data.resolve(), a.c_data.resolve()

    # Pre-test integrity gate: verify frozen dataset fingerprints and all six completed runs.
    y_manifest = y_data.parent / "manifest.jsonl"
    c_manifest = c_data.parent / "manifest.jsonl"
    if sha256_file(y_manifest) != Y_FP:
        raise RuntimeError("Y-PPE-h9-v2 manifest fingerprint mismatch.")
    if sha256_file(c_manifest) != C_FP:
        raise RuntimeError("Construction-PPE-h9-v2 manifest fingerprint mismatch.")

    runtime_dir = a.out / "_runtime_yaml"
    y_runtime = write_runtime_yaml(y_data, runtime_dir / "Y-PPE-h9-v2_absolute.yaml")
    c_runtime = write_runtime_yaml(c_data, runtime_dir / "Construction-PPE-h9-v2_absolute.yaml")
    y_test, c_test = resolve_split(y_runtime), resolve_split(c_runtime)
    y_images, c_images = image_files(y_test), image_files(c_test)
    if len(y_images) != 186:
        raise RuntimeError(f"Y-PPE held-out test count mismatch: expected 186, got {len(y_images)}")
    if len(c_images) != 138:
        raise RuntimeError(f"Construction-PPE held-out test count mismatch: expected 138, got {len(c_images)}")

    preflight = validate_stage5_inputs(a.stage5_root)
    preflight.update({
        "status": "STAGE6_PREFLIGHT_PASS",
        "heldout_evaluation_started": False,
        "y_dataset_fingerprint": Y_FP,
        "c_dataset_fingerprint": C_FP,
        "y_test_images": len(y_images),
        "c_test_images": len(c_images),
        "runtime_yaml_note": "Absolute-path YAML adapters only; dataset bytes/classes/splits unchanged.",
        "settings": {
            "imgsz": a.imgsz,
            "ap_conf": a.ap_conf,
            "operating_conf": a.operating_conf,
            "nms_iou": a.nms_iou,
            "match_iou": a.match_iou,
            "augmentation": False,
        },
    })
    preflight_path = a.out / "stage6_preflight.json"
    preflight_path.write_text(json.dumps(preflight, indent=2), encoding="utf-8")
    print("STAGE6_PREFLIGHT_PASS")
    print(preflight_path)
    if a.preflight_only:
        return

    tests = {
        "Y": (y_runtime, y_images, "Y-PPE-h9-v2"),
        "C": (c_runtime, c_images, "Construction-PPE-h9-v2"),
    }

    # From this line onward the held-out test evaluation begins.
    preflight["heldout_evaluation_started"] = True
    preflight_path.write_text(json.dumps(preflight, indent=2), encoding="utf-8")

    rows = []
    all_json = {}
    for run_id, train_domain, seed in RUNS:
        weights = (a.stage5_root / run_id / "train" / "weights" / "last.pt").resolve()
        if not weights.is_file():
            raise FileNotFoundError(f"Missing final-epoch checkpoint: {weights}")
        model = YOLO(str(weights))

        for test_domain in ("Y", "C"):
            data_yaml, imgs, test_name = tests[test_domain]
            eval_id = f"{run_id}__TEST_{test_domain}"
            domain_type = "in_domain" if train_domain == test_domain else "cross_domain"
            out_dir = a.out / eval_id
            out_dir.mkdir(parents=True, exist_ok=True)

            metrics = model.val(
                data=str(data_yaml),
                split="test",
                imgsz=a.imgsz,
                batch=a.batch,
                device=a.device,
                conf=a.ap_conf,
                iou=a.nms_iou,
                augment=False,
                plots=False,
                save_json=False,
                verbose=False,
                project=str(a.out),
                name=eval_id,
                exist_ok=True,
            )
            ap = metrics_to_dict(metrics)
            fixed = fixed_operating_point(
                model, imgs, a.device, a.imgsz, a.operating_conf, a.nms_iou, a.match_iou
            )
            record = {
                "eval_id": eval_id,
                "run_id": run_id,
                "train_domain": train_domain,
                "test_domain": test_domain,
                "domain_type": domain_type,
                "seed": seed,
                "checkpoint": str(weights),
                "test_dataset": test_name,
                "n_test_images": len(imgs),
                "settings": {
                    "imgsz": a.imgsz,
                    "ap_conf": a.ap_conf,
                    "operating_conf": a.operating_conf,
                    "nms_iou": a.nms_iou,
                    "match_iou": a.match_iou,
                    "augmentation": False,
                },
                "ap_metrics": ap,
                "fixed_operating_point": fixed,
            }
            (out_dir / "metrics.json").write_text(
                json.dumps(record, indent=2), encoding="utf-8"
            )
            all_json[eval_id] = record
            rows.append({
                "eval_id": eval_id,
                "run_id": run_id,
                "train_domain": train_domain,
                "test_domain": test_domain,
                "domain_type": domain_type,
                "seed": seed,
                "map50_95": ap["map50_95"],
                "map50": ap["map50"],
                "map75": ap["map75"],
                "precision_fixed": fixed["micro"]["precision"],
                "recall_fixed": fixed["micro"]["recall"],
                "f1_fixed": fixed["micro"]["f1"],
                "no_helmet_fn": fixed["per_class"]["no_helmet"]["fn"],
                "no_gloves_fn": fixed["per_class"]["no_gloves"]["fn"],
                "no_boots_fn": fixed["per_class"]["no_boots"]["fn"],
                "no_helmet_recall": fixed["per_class"]["no_helmet"]["recall"],
                "no_gloves_recall": fixed["per_class"]["no_gloves"]["recall"],
                "no_boots_recall": fixed["per_class"]["no_boots"]["recall"],
                "no_helmet_fnr": 1.0 - fixed["per_class"]["no_helmet"]["recall"],
                "no_gloves_fnr": 1.0 - fixed["per_class"]["no_gloves"]["recall"],
                "no_boots_fnr": 1.0 - fixed["per_class"]["no_boots"]["recall"],
            })
            if torch.cuda.is_available():
                torch.cuda.empty_cache()

    summary_csv = a.out / "stage6_12cell_summary.csv"
    with summary_csv.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    (a.out / "stage6_all_metrics.json").write_text(
        json.dumps(all_json, indent=2), encoding="utf-8"
    )
    print(f"PASS: completed {len(rows)} frozen held-out evaluation cells")
    print(summary_csv)


if __name__ == "__main__":
    main()
