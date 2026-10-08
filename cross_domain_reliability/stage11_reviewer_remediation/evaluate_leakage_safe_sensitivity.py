#!/usr/bin/env python3
"""Stage 11 leakage-safe held-out and checkpoint-sensitivity evaluation.

Post-hoc sensitivity analysis only. No training, fine-tuning, adaptation, threshold
selection, or model reselection is performed.

It evaluates both final-epoch last.pt and validation-selected best.pt checkpoints
on leakage-safe held-out subsets defined solely by the image-similarity audit.
"""
from __future__ import annotations

import argparse
import csv
import gc
import importlib.util
import json
import shutil
from collections import defaultdict
from pathlib import Path

import numpy as np
import pandas as pd
import torch
import yaml
from ultralytics import YOLO

HERE = Path(__file__).resolve()
REPO = HERE.parents[2]
S6_PATH = REPO / "cross_domain_reliability" / "stage6_heldout_evaluation" / "evaluate_yolo_cross_domain.py"
spec = importlib.util.spec_from_file_location("stage6_eval", S6_PATH)
s6 = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(s6)

CLASSES = s6.CLASSES
RUNS = s6.RUNS
SAFETY = {"no_helmet", "no_gloves", "no_boots"}


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--stage5-root", required=True, type=Path)
    p.add_argument("--y-data", required=True, type=Path)
    p.add_argument("--c-data", required=True, type=Path)
    p.add_argument("--exclusions", required=True, type=Path)
    p.add_argument("--out", required=True, type=Path)
    p.add_argument("--device", default="0")
    p.add_argument("--batch", type=int, default=8)
    p.add_argument("--imgsz", type=int, default=640)
    p.add_argument("--ap-conf", type=float, default=0.001)
    p.add_argument("--operating-conf", type=float, default=0.25)
    p.add_argument("--nms-iou", type=float, default=0.70)
    p.add_argument("--match-iou", type=float, default=0.50)
    return p.parse_args()


def runtime_root_and_split(yaml_path: Path, split: str) -> Path:
    d = s6.read_yaml(yaml_path)
    root = Path(d.get("path", "."))
    if not root.is_absolute():
        root = (yaml_path.parent / root).resolve()
    target = Path(d[split])
    return target if target.is_absolute() else (root / target).resolve()


def make_leakage_safe_dataset(
    source_yaml: Path,
    dataset_name: str,
    excluded_names: set[str],
    expected_original_n: int,
    expected_safe_n: int,
    out_root: Path,
):
    source_yaml = source_yaml.resolve()
    test_dir = runtime_root_and_split(source_yaml, "test")
    train_dir = runtime_root_and_split(source_yaml, "train")
    val_dir = runtime_root_and_split(source_yaml, "val")
    images = s6.image_files(test_dir)
    if len(images) != expected_original_n:
        raise RuntimeError(
            f"{dataset_name}: expected original test n={expected_original_n}, got {len(images)}"
        )
    unknown = excluded_names.difference({p.name for p in images})
    if unknown:
        raise RuntimeError(f"{dataset_name}: exclusion names not found in test split: {sorted(unknown)}")

    subset = out_root / dataset_name
    if subset.exists():
        shutil.rmtree(subset)
    (subset / "images" / "test").mkdir(parents=True)
    (subset / "labels" / "test").mkdir(parents=True)

    kept = []
    for image in images:
        if image.name in excluded_names:
            continue
        label = s6.label_path_for_image(image)
        if not label.is_file():
            raise FileNotFoundError(label)
        dst_i = subset / "images" / "test" / image.name
        dst_l = subset / "labels" / "test" / label.name
        try:
            dst_i.symlink_to(image)
            dst_l.symlink_to(label)
        except OSError:
            shutil.copy2(image, dst_i)
            shutil.copy2(label, dst_l)
        kept.append(dst_i.resolve())

    if len(kept) != expected_safe_n:
        raise RuntimeError(
            f"{dataset_name}: expected leakage-safe n={expected_safe_n}, got {len(kept)}"
        )

    data = {
        "path": str(subset.resolve()),
        "train": str(train_dir),
        "val": str(val_dir),
        "test": "images/test",
        "names": CLASSES,
        "nc": 9,
    }
    yaml_path = subset / "data.yaml"
    yaml_path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
    return yaml_path, sorted(kept)


def fixed_with_object_records(
    model: YOLO,
    test_images: list[Path],
    device: str,
    imgsz: int,
    conf: float,
    nms_iou: float,
    match_iou: float,
    batch_size: int,
):
    counts = defaultdict(lambda: {"tp": 0, "fp": 0, "fn": 0})
    object_records = []

    for start in range(0, len(test_images), batch_size):
        chunk = test_images[start:start + batch_size]
        results = model.predict(
            source=[str(p) for p in chunk],
            conf=conf,
            iou=nms_iou,
            imgsz=imgsz,
            device=device,
            verbose=False,
            augment=False,
        )
        for res in results:
            h, w = res.orig_shape
            ip = Path(res.path).resolve()
            gt_cls, gt_boxes = s6.load_gt_xyxy(s6.label_path_for_image(ip), w, h)
            if res.boxes is None or len(res.boxes) == 0:
                pred_cls = np.empty((0,), dtype=int)
                pred_boxes = np.empty((0, 4), dtype=float)
                pred_conf = np.empty((0,), dtype=float)
            else:
                pred_cls = res.boxes.cls.detach().cpu().numpy().astype(int)
                pred_boxes = res.boxes.xyxy.detach().cpu().numpy().astype(float)
                pred_conf = res.boxes.conf.detach().cpu().numpy().astype(float)

            for c, cname in enumerate(CLASSES):
                gi = np.where(gt_cls == c)[0]
                pi = np.where(pred_cls == c)[0]
                gboxes = gt_boxes[gi]
                order = pi[np.argsort(-pred_conf[pi])] if len(pi) else np.empty((0,), dtype=int)
                used = set()
                for pidx in order:
                    ious = s6.iou_one_to_many(pred_boxes[pidx], gboxes)
                    best_local = -1
                    best_iou = -1.0
                    for j, v in enumerate(ious):
                        if j not in used and float(v) > best_iou:
                            best_iou = float(v)
                            best_local = j
                    if best_local >= 0 and best_iou >= match_iou:
                        counts[c]["tp"] += 1
                        used.add(best_local)
                    else:
                        counts[c]["fp"] += 1
                counts[c]["fn"] += max(0, len(gboxes) - len(used))

                if cname in SAFETY:
                    for local_idx, full_gt_idx in enumerate(gi):
                        object_records.append({
                            "image": ip.name,
                            "class": cname,
                            "gt_index": int(full_gt_idx),
                            "detected": bool(local_idx in used),
                        })

        del results
        gc.collect()
        if torch.cuda.is_available():
            torch.cuda.empty_cache()

    per_class = {}
    total = {"tp": 0, "fp": 0, "fn": 0}
    for c, name in enumerate(CLASSES):
        d = counts[c]
        p, r, f1 = s6.safe_prf(d["tp"], d["fp"], d["fn"])
        per_class[name] = {**d, "precision": p, "recall": r, "f1": f1}
        for k in total:
            total[k] += d[k]
    mp, mr, mf1 = s6.safe_prf(total["tp"], total["fp"], total["fn"])
    fixed = {
        "micro": {**total, "precision": mp, "recall": mr, "f1": mf1},
        "per_class": per_class,
    }
    return fixed, object_records


def validation_trajectory_summary(stage5_root: Path):
    rows = []
    for run_id, train_domain, seed in RUNS:
        p = stage5_root / run_id / "train" / "results.csv"
        df = pd.read_csv(p)
        df.columns = [x.strip() for x in df.columns]
        metric = "metrics/mAP50-95(B)"
        m50 = "metrics/mAP50(B)"
        best_idx = df[metric].astype(float).idxmax()
        best = df.loc[best_idx]
        final = df.iloc[-1]
        rows.append({
            "run_id": run_id,
            "train_domain": train_domain,
            "seed": seed,
            "best_validation_map50_95_epoch": int(best["epoch"]),
            "best_validation_map50_95": float(best[metric]),
            "best_validation_map50": float(best[m50]),
            "final_epoch": int(final["epoch"]),
            "final_validation_map50_95": float(final[metric]),
            "final_validation_map50": float(final[m50]),
            "best_minus_final_map50_95": float(best[metric] - final[metric]),
        })
    return pd.DataFrame(rows)


def main():
    a = parse_args()
    a.stage5_root = a.stage5_root.resolve()
    a.out = a.out.resolve()
    a.out.mkdir(parents=True, exist_ok=True)

    exclusion_spec = json.loads(a.exclusions.read_text(encoding="utf-8"))
    subset_root = a.out / "_leakage_safe_subsets"

    yinfo = exclusion_spec["Y-PPE-h9-v2"]
    cinfo = exclusion_spec["Construction-PPE-h9-v2"]
    y_yaml, y_images = make_leakage_safe_dataset(
        a.y_data,
        "Y-PPE-h9-v2",
        set(yinfo["excluded_test_images"]),
        int(yinfo["original_test_n"]),
        int(yinfo["leakage_safe_test_n"]),
        subset_root,
    )
    c_yaml, c_images = make_leakage_safe_dataset(
        a.c_data,
        "Construction-PPE-h9-v2",
        set(cinfo["excluded_test_images"]),
        int(cinfo["original_test_n"]),
        int(cinfo["leakage_safe_test_n"]),
        subset_root,
    )

    validation = validation_trajectory_summary(a.stage5_root)
    validation.to_csv(a.out / "stage11_validation_checkpoint_sensitivity.csv", index=False)

    tests = {
        "Y": (y_yaml, y_images, "Y-PPE-h9-v2"),
        "C": (c_yaml, c_images, "Construction-PPE-h9-v2"),
    }

    rows = []
    object_rows = []
    for checkpoint_policy in ("last", "best"):
        for run_id, train_domain, seed in RUNS:
            weights = (
                a.stage5_root / run_id / "train" / "weights" / f"{checkpoint_policy}.pt"
            ).resolve()
            if not weights.is_file():
                raise FileNotFoundError(weights)
            model = YOLO(str(weights))

            for test_domain in ("Y", "C"):
                data_yaml, imgs, test_name = tests[test_domain]
                eval_id = f"{run_id}__{checkpoint_policy.upper()}__TEST_{test_domain}"
                domain_type = "in_domain" if train_domain == test_domain else "cross_domain"
                print(f"[Stage11] START {eval_id}: AP", flush=True)
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
                    project=str(a.out / "validator_runs"),
                    name=eval_id,
                    exist_ok=True,
                )
                ap = s6.metrics_to_dict(metrics)
                del metrics
                gc.collect()
                if torch.cuda.is_available():
                    torch.cuda.empty_cache()

                print(f"[Stage11] START {eval_id}: fixed operating point", flush=True)
                fixed, obj = fixed_with_object_records(
                    model, imgs, a.device, a.imgsz, a.operating_conf,
                    a.nms_iou, a.match_iou, a.batch
                )

                rows.append({
                    "eval_id": eval_id,
                    "checkpoint_policy": checkpoint_policy,
                    "run_id": run_id,
                    "train_domain": train_domain,
                    "test_domain": test_domain,
                    "domain_type": domain_type,
                    "seed": seed,
                    "n_test_images": len(imgs),
                    "map50_95": ap["map50_95"],
                    "map50": ap["map50"],
                    "map75": ap["map75"],
                    "precision_fixed": fixed["micro"]["precision"],
                    "recall_fixed": fixed["micro"]["recall"],
                    "f1_fixed": fixed["micro"]["f1"],
                    "no_helmet_recall": fixed["per_class"]["no_helmet"]["recall"],
                    "no_gloves_recall": fixed["per_class"]["no_gloves"]["recall"],
                    "no_boots_recall": fixed["per_class"]["no_boots"]["recall"],
                })
                for r in obj:
                    object_rows.append({
                        **r,
                        "checkpoint_policy": checkpoint_policy,
                        "run_id": run_id,
                        "train_domain": train_domain,
                        "test_domain": test_domain,
                        "domain_type": domain_type,
                        "seed": seed,
                    })
                print(f"[Stage11] COMPLETE {eval_id}", flush=True)

            del model
            gc.collect()
            if torch.cuda.is_available():
                torch.cuda.empty_cache()

    raw = pd.DataFrame(rows)
    raw.to_csv(a.out / "stage11_24cell_leakage_safe_summary.csv", index=False)

    group = (
        raw.groupby(["checkpoint_policy", "train_domain", "test_domain", "domain_type"])
        .agg(
            n_seeds=("seed", "count"),
            map50_95_mean=("map50_95", "mean"),
            map50_95_sd=("map50_95", "std"),
            map50_mean=("map50", "mean"),
            map50_sd=("map50", "std"),
            map75_mean=("map75", "mean"),
            map75_sd=("map75", "std"),
            precision_mean=("precision_fixed", "mean"),
            precision_sd=("precision_fixed", "std"),
            recall_mean=("recall_fixed", "mean"),
            recall_sd=("recall_fixed", "std"),
            f1_mean=("f1_fixed", "mean"),
            f1_sd=("f1_fixed", "std"),
            no_helmet_recall_mean=("no_helmet_recall", "mean"),
            no_helmet_recall_sd=("no_helmet_recall", "std"),
            no_gloves_recall_mean=("no_gloves_recall", "mean"),
            no_gloves_recall_sd=("no_gloves_recall", "std"),
            no_boots_recall_mean=("no_boots_recall", "mean"),
            no_boots_recall_sd=("no_boots_recall", "std"),
        )
        .reset_index()
    )
    group.to_csv(a.out / "stage11_group_summary.csv", index=False)

    # Paired domain gaps for each seed and checkpoint policy.
    gap_rows = []
    for policy in ("last", "best"):
        for train_domain in ("Y", "C"):
            g = raw[(raw.checkpoint_policy == policy) & (raw.train_domain == train_domain)]
            for seed in sorted(g.seed.unique()):
                s = g[g.seed == seed]
                ind = s[s.domain_type == "in_domain"].iloc[0]
                cross = s[s.domain_type == "cross_domain"].iloc[0]
                gap_rows.append({
                    "checkpoint_policy": policy,
                    "train_domain": train_domain,
                    "seed": int(seed),
                    "map50_95_gap_in_minus_cross": float(ind.map50_95 - cross.map50_95),
                    "f1_gap_in_minus_cross": float(ind.f1_fixed - cross.f1_fixed),
                })
    gaps = pd.DataFrame(gap_rows)
    gaps.to_csv(a.out / "stage11_seed_domain_gaps.csv", index=False)

    # Best-vs-last paired sensitivity on the same leakage-safe images.
    pivot = raw.pivot_table(
        index=["run_id", "train_domain", "test_domain", "domain_type", "seed", "n_test_images"],
        columns="checkpoint_policy",
        values=["map50_95", "recall_fixed", "f1_fixed",
                "no_helmet_recall", "no_gloves_recall", "no_boots_recall"],
    )
    pivot.columns = [f"{metric}_{policy}" for metric, policy in pivot.columns]
    pivot = pivot.reset_index()
    for metric in ["map50_95", "recall_fixed", "f1_fixed",
                   "no_helmet_recall", "no_gloves_recall", "no_boots_recall"]:
        pivot[f"{metric}_best_minus_last"] = pivot[f"{metric}_best"] - pivot[f"{metric}_last"]
    pivot.to_csv(a.out / "stage11_best_vs_last_paired.csv", index=False)

    # Consensus FN: failure persistence across the three seed realizations.
    obj = pd.DataFrame(object_rows)
    obj.to_csv(a.out / "stage11_safety_object_detection_records.csv", index=False)
    consensus = (
        obj.groupby(
            ["checkpoint_policy", "train_domain", "test_domain", "domain_type",
             "image", "class", "gt_index"]
        )
        .agg(n_seeds=("seed", "nunique"), detected_seeds=("detected", "sum"))
        .reset_index()
    )
    if not (consensus.n_seeds == 3).all():
        raise RuntimeError("Consensus audit expected exactly three seed outcomes per GT object.")
    consensus["consensus_fn"] = consensus.detected_seeds == 0
    consensus.to_csv(a.out / "stage11_consensus_object_records.csv", index=False)
    csum = (
        consensus.groupby(
            ["checkpoint_policy", "train_domain", "test_domain", "domain_type", "class"]
        )
        .agg(
            gt_objects=("consensus_fn", "size"),
            consensus_fn_objects=("consensus_fn", "sum"),
        )
        .reset_index()
    )
    csum["consensus_fn_rate"] = csum.consensus_fn_objects / csum.gt_objects
    csum.to_csv(a.out / "stage11_consensus_fn_summary.csv", index=False)

    status = {
        "status": "STAGE11_LEAKAGE_SAFE_CHECKPOINT_SENSITIVITY_COMPLETE",
        "training_performed": False,
        "leakage_safe_test_counts": {"Y": len(y_images), "C": len(c_images)},
        "checkpoint_policies": ["last", "best"],
        "evaluation_cells": int(len(raw)),
        "settings": {
            "imgsz": a.imgsz,
            "ap_conf": a.ap_conf,
            "operating_conf": a.operating_conf,
            "nms_iou": a.nms_iou,
            "match_iou": a.match_iou,
            "test_time_augmentation": False,
        },
    }
    (a.out / "stage11_status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    print("STAGE11_LEAKAGE_SAFE_SENSITIVITY: PASS")


if __name__ == "__main__":
    main()
