#!/usr/bin/env python3
"""Stage 11E2: image-cluster bootstrap CIs for mAP50:95 domain gaps.

Inference-only. Re-runs the six primary last.pt checkpoints under the exact
Stage 6 AP settings, archives Ultralytics per-image ranked prediction statistics,
verifies archive reconstruction against validator mAP, then bootstraps images.
"""
from __future__ import annotations

import argparse
import csv
import gc
import json
from pathlib import Path

import numpy as np
import pandas as pd
import torch
from ultralytics import YOLO
from ultralytics.models.yolo.detect import DetectionValidator
from ultralytics.utils.metrics import ap_per_class

CLASSES = [
    "person", "helmet", "gloves", "vest", "boots", "goggles",
    "no_helmet", "no_gloves", "no_boots",
]
RUNS = [
    ("Y_YOLO_s17", "Y", 17),
    ("Y_YOLO_s42", "Y", 42),
    ("Y_YOLO_s2026", "Y", 2026),
    ("C_YOLO_s17", "C", 17),
    ("C_YOLO_s42", "C", 42),
    ("C_YOLO_s2026", "C", 2026),
]


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--stage5-root", required=True, type=Path)
    p.add_argument("--y-data", required=True, type=Path)
    p.add_argument("--c-data", required=True, type=Path)
    p.add_argument("--out", required=True, type=Path)
    p.add_argument("--device", default="0")
    p.add_argument("--batch", type=int, default=8)
    p.add_argument("--imgsz", type=int, default=640)
    p.add_argument("--ap-conf", type=float, default=0.001)
    p.add_argument("--nms-iou", type=float, default=0.70)
    p.add_argument("--bootstrap-reps", type=int, default=2000)
    p.add_argument("--bootstrap-seed", type=int, default=20261009)
    return p.parse_args()


def obj_array(values):
    a = np.empty(len(values), dtype=object)
    a[:] = values
    return a


class ArchiveValidator(DetectionValidator):
    archive_path: Path | None = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._image_archive = []

    def update_metrics(self, preds, batch):
        before = len(self.metrics.stats["tp"])
        super().update_metrics(preds, batch)
        names = [Path(x).name for x in batch["im_file"]]
        after = len(self.metrics.stats["tp"])
        if after - before != len(names):
            raise RuntimeError(
                f"Per-image stat alignment failure: appended={after-before}, images={len(names)}"
            )
        for j, name in enumerate(names):
            idx = before + j
            self._image_archive.append(
                {
                    "im_name": name,
                    "tp": np.asarray(self.metrics.stats["tp"][idx], dtype=bool),
                    "conf": np.asarray(self.metrics.stats["conf"][idx], dtype=float),
                    "pred_cls": np.asarray(self.metrics.stats["pred_cls"][idx], dtype=float),
                    "target_cls": np.asarray(self.metrics.stats["target_cls"][idx], dtype=float),
                }
            )

    def get_stats(self):
        if self.archive_path is None:
            raise RuntimeError("ArchiveValidator.archive_path was not set.")
        p = Path(self.archive_path)
        p.parent.mkdir(parents=True, exist_ok=True)
        np.savez_compressed(
            p,
            im_name=np.asarray([r["im_name"] for r in self._image_archive], dtype=object),
            tp=obj_array([r["tp"] for r in self._image_archive]),
            conf=obj_array([r["conf"] for r in self._image_archive]),
            pred_cls=obj_array([r["pred_cls"] for r in self._image_archive]),
            target_cls=obj_array([r["target_cls"] for r in self._image_archive]),
        )
        return super().get_stats()


def load_archive(path: Path):
    z = np.load(path, allow_pickle=True)
    out = []
    for i, name in enumerate(z["im_name"].tolist()):
        out.append(
            {
                "im_name": str(name),
                "tp": np.asarray(z["tp"][i], dtype=bool).reshape(-1, 10),
                "conf": np.asarray(z["conf"][i], dtype=float).reshape(-1),
                "pred_cls": np.asarray(z["pred_cls"][i], dtype=float).reshape(-1),
                "target_cls": np.asarray(z["target_cls"][i], dtype=float).reshape(-1),
            }
        )
    return out


def concat_stat(records, key, empty_shape=None):
    vals = [r[key] for r in records]
    if vals:
        return np.concatenate(vals, axis=0)
    if empty_shape is not None:
        return np.empty(empty_shape)
    return np.empty((0,))


def map_from_records(records):
    tp = concat_stat(records, "tp", (0, 10))
    conf = concat_stat(records, "conf")
    pred_cls = concat_stat(records, "pred_cls")
    target_cls = concat_stat(records, "target_cls")
    if target_cls.size == 0:
        return np.nan
    result = ap_per_class(
        tp,
        conf,
        pred_cls,
        target_cls,
        plot=False,
        names={i: n for i, n in enumerate(CLASSES)},
    )
    ap = np.asarray(result[5], dtype=float)
    return float(ap.mean()) if ap.size else np.nan


def ensure_same_names(archives):
    base = [r["im_name"] for r in archives[0]]
    if len(set(base)) != len(base):
        raise RuntimeError("Duplicate image names inside one archive.")
    for a in archives[1:]:
        names = [r["im_name"] for r in a]
        if names != base:
            raise RuntimeError("Image ordering/membership differs across seed archives.")
    return base


def full_class_set(records):
    t = concat_stat(records, "target_cls")
    return set(t.astype(int).tolist())


def sampled_records(records, idx):
    return [records[int(i)] for i in idx]


def sample_all_classes(rng, records, nclasses=9, max_tries=10000):
    n = len(records)
    for _ in range(max_tries):
        idx = rng.integers(0, n, size=n)
        if len(full_class_set(sampled_records(records, idx))) == nclasses:
            return idx
    raise RuntimeError("Could not draw a bootstrap sample containing all canonical classes.")


def percentile_ci(x):
    x = np.asarray(x, dtype=float)
    return float(np.percentile(x, 2.5)), float(np.percentile(x, 97.5))


def main():
    a = parse_args()
    a.stage5_root = a.stage5_root.resolve()
    a.y_data = a.y_data.resolve()
    a.c_data = a.c_data.resolve()
    a.out = a.out.resolve()
    a.out.mkdir(parents=True, exist_ok=True)
    archive_dir = a.out / "prediction_archives"
    archive_dir.mkdir(exist_ok=True)

    tests = {"Y": a.y_data, "C": a.c_data}
    all_archives = {}
    validation_rows = []

    for run_id, train_domain, seed in RUNS:
        weights = (a.stage5_root / run_id / "train" / "weights" / "last.pt").resolve()
        if not weights.is_file():
            raise FileNotFoundError(weights)
        model = YOLO(str(weights))
        for test_domain in ("Y", "C"):
            eval_id = f"{run_id}__TEST_{test_domain}"
            apath = archive_dir / f"{eval_id}.npz"
            ArchiveValidator.archive_path = apath
            print(f"[Stage11E2] ARCHIVE START {eval_id}", flush=True)
            metrics = model.val(
                validator=ArchiveValidator,
                data=str(tests[test_domain]),
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
                project=str(a.out / "ultralytics"),
                name=eval_id,
                exist_ok=True,
            )
            records = load_archive(apath)
            reconstructed = map_from_records(records)
            validator_map = float(metrics.box.map)
            delta = reconstructed - validator_map
            if not np.isfinite(reconstructed) or abs(delta) > 1e-10:
                raise RuntimeError(
                    f"Archive reconstruction mismatch {eval_id}: "
                    f"archive={reconstructed}, validator={validator_map}, delta={delta}"
                )
            all_archives[(run_id, test_domain)] = records
            validation_rows.append(
                {
                    "eval_id": eval_id,
                    "run_id": run_id,
                    "train_domain": train_domain,
                    "test_domain": test_domain,
                    "seed": seed,
                    "n_images": len(records),
                    "validator_map50_95": validator_map,
                    "archive_map50_95": reconstructed,
                    "delta": delta,
                }
            )
            print(f"[Stage11E2] ARCHIVE PASS {eval_id}: mAP={validator_map:.6f}", flush=True)
            del metrics
            gc.collect()
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
        del model
        gc.collect()
        if torch.cuda.is_available():
            torch.cuda.empty_cache()

    pd.DataFrame(validation_rows).to_csv(a.out / "stage11e2_archive_validation.csv", index=False)

    y_runs = [r[0] for r in RUNS if r[1] == "Y"]
    c_runs = [r[0] for r in RUNS if r[1] == "C"]
    y_names = ensure_same_names([all_archives[(r, "Y")] for r in y_runs + c_runs])
    c_names = ensure_same_names([all_archives[(r, "C")] for r in y_runs + c_runs])
    if len(y_names) != 186 or len(c_names) != 138:
        raise RuntimeError(f"Frozen test counts changed: Y={len(y_names)}, C={len(c_names)}")

    point = {}
    for source, run_ids, in_test, cross_test in [
        ("Y", y_runs, "Y", "C"),
        ("C", c_runs, "C", "Y"),
    ]:
        in_maps = [map_from_records(all_archives[(r, in_test)]) for r in run_ids]
        cr_maps = [map_from_records(all_archives[(r, cross_test)]) for r in run_ids]
        point[source] = {
            "in_domain_mean": float(np.mean(in_maps)),
            "cross_domain_mean": float(np.mean(cr_maps)),
            "gap": float(np.mean(in_maps) - np.mean(cr_maps)),
        }

    rng = np.random.default_rng(a.bootstrap_seed)
    reps = []
    y_reference = all_archives[(y_runs[0], "Y")]
    c_reference = all_archives[(y_runs[0], "C")]

    for b in range(a.bootstrap_reps):
        y_idx = sample_all_classes(rng, y_reference)
        c_idx = sample_all_classes(rng, c_reference)

        y_in = np.mean(
            [map_from_records(sampled_records(all_archives[(r, "Y")], y_idx)) for r in y_runs]
        )
        y_cross = np.mean(
            [map_from_records(sampled_records(all_archives[(r, "C")], c_idx)) for r in y_runs]
        )
        c_in = np.mean(
            [map_from_records(sampled_records(all_archives[(r, "C")], c_idx)) for r in c_runs]
        )
        c_cross = np.mean(
            [map_from_records(sampled_records(all_archives[(r, "Y")], y_idx)) for r in c_runs]
        )
        reps.append(
            {
                "replicate": b + 1,
                "Y_in_domain_mean": float(y_in),
                "Y_cross_domain_mean": float(y_cross),
                "Y_gap": float(y_in - y_cross),
                "C_in_domain_mean": float(c_in),
                "C_cross_domain_mean": float(c_cross),
                "C_gap": float(c_in - c_cross),
            }
        )
        if (b + 1) % 100 == 0:
            print(f"[Stage11E2] bootstrap {b+1}/{a.bootstrap_reps}", flush=True)

    rep_df = pd.DataFrame(reps)
    rep_df.to_csv(a.out / "stage11e2_map_bootstrap_replicates.csv", index=False)

    summary = []
    for source in ("Y", "C"):
        for metric, col in [
            ("in_domain_mean_map50_95", f"{source}_in_domain_mean"),
            ("cross_domain_mean_map50_95", f"{source}_cross_domain_mean"),
            ("domain_gap_map50_95", f"{source}_gap"),
        ]:
            lo, hi = percentile_ci(rep_df[col].to_numpy())
            pkey = {
                "in_domain_mean_map50_95": "in_domain_mean",
                "cross_domain_mean_map50_95": "cross_domain_mean",
                "domain_gap_map50_95": "gap",
            }[metric]
            summary.append(
                {
                    "source_train_domain": source,
                    "metric": metric,
                    "point_estimate": point[source][pkey],
                    "ci95_low": lo,
                    "ci95_high": hi,
                    "bootstrap_reps": a.bootstrap_reps,
                    "bootstrap_seed": a.bootstrap_seed,
                    "bootstrap_unit": "image",
                }
            )
    pd.DataFrame(summary).to_csv(a.out / "stage11e2_map_bootstrap_summary.csv", index=False)

    status = {
        "status": "STAGE11E2_MAP_BOOTSTRAP_COMPLETE",
        "training_performed": False,
        "checkpoint_policy": "primary_last.pt",
        "test_informed_tuning": False,
        "bootstrap_reps": a.bootstrap_reps,
        "bootstrap_seed": a.bootstrap_seed,
        "archive_reconstruction_tolerance": 1e-10,
        "n_eval_cells_archived": len(validation_rows),
    }
    (a.out / "stage11e2_status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    print("STAGE11E2_MAP_BOOTSTRAP: PASS", flush=True)
    print(pd.DataFrame(summary).to_string(index=False), flush=True)


if __name__ == "__main__":
    main()
