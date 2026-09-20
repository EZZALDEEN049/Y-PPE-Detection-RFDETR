#!/usr/bin/env python3
"""Reconstruct the exact final Stage 4.5-corrected Stage 5 datasets.

The script reproduces the successful conservative freeze using only source
annotations for membership decisions. It never uses model predictions and the
Stage 4.5 audit never opens test image pixels. Raw/intermediate data are written
only below --out-root. Execution stops unless the final frozen fingerprints and
split counts are reproduced exactly.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
PY = sys.executable
EXPECTED = {
    "Y-PPE-h9-v2": "82c08766d5c5e50e93d41d21c4751fd686a3932ea6a8cb24ffd2838d9e30fba8",
    "Construction-PPE-h9-v2": "59469299ba67355dbcb0e725851f73d244a7ad6e93522d44601be3c8323d3c14",
}
EXPECTED_COUNTS = {
    "Y-PPE-h9-v2": {"train": 1236, "val": 356, "test": 186},
    "Construction-PPE-h9-v2": {"train": 1046, "val": 132, "test": 138},
}


def run(*args: str) -> None:
    print("+", " ".join(args), flush=True)
    subprocess.run(args, check=True, cwd=REPO)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out-root", required=True)
    ap.add_argument("--overwrite", action="store_true")
    args = ap.parse_args()

    if not os.environ.get("ROBOFLOW_API_KEY"):
        raise SystemExit("ROBOFLOW_API_KEY is required in the environment; never place it in source code")

    out = Path(args.out_root).resolve()
    if out.exists():
        if not args.overwrite:
            raise SystemExit(f"Output exists: {out}. Use --overwrite only if intentional.")
        shutil.rmtree(out)
    out.mkdir(parents=True)
    meta = out / "meta"; meta.mkdir()

    stage2 = REPO / "cross_domain_reliability" / "stage2_data_audit"
    stage3 = REPO / "cross_domain_reliability" / "stage3_semantic_harmonization"
    stage45 = REPO / "cross_domain_reliability" / "stage4_5_label_completeness"
    stage5 = REPO / "cross_domain_reliability" / "stage5_in_domain_baselines"

    # 1) Reconstruct audited clean Y-PPE Version 2.
    y_download = out / "downloads" / "y_ppe"
    run(PY, str(stage2 / "download_roboflow_dataset.py"),
        "--workspace", "master-fylfq", "--project", "altayyar-0oflt-lafos-qqauz-ty5nh",
        "--version", "2", "--format", "yolov11", "--out", str(y_download),
        "--metadata-out", str(meta / "y_download_metadata.json"))
    y_src = Path(json.loads((meta / "y_download_metadata.json").read_text(encoding="utf-8"))["dataset_location"])
    y_clean = out / "clean" / "Y-PPE"
    run(PY, str(stage2 / "apply_y_ppe_stage2_corrections.py"),
        "--root", str(y_src), "--out", str(y_clean),
        "--file-manifest", str(stage2 / "results" / "Y-PPE_v2_conservative_file_correction_manifest_2026-09-19.csv"),
        "--near-box-manifest", str(stage2 / "results" / "Y-PPE_v2_near_box_removal_manifest_2026-09-19.csv"),
        "--expected-exclusions", "39", "--expected-exact-row-removals", "68",
        "--expected-near-box-removals", "1", "--summary-out", str(meta / "y_stage2_correction_summary.json"))
    y_yaml_candidates = list(y_clean.rglob("data.yaml")) + list(y_clean.rglob("dataset.yaml"))
    if not y_yaml_candidates:
        raise SystemExit("Could not locate cleaned Y-PPE data.yaml")
    y_clean_yaml = y_yaml_candidates[0]

    # 2) Reconstruct audited clean Construction-PPE from pinned official source.
    c_download = out / "downloads" / "construction_ppe"
    run(PY, str(stage2 / "download_ultralytics_construction_ppe.py"),
        "--out", str(c_download), "--metadata-out", str(meta / "c_download_metadata.json"))
    c_src = Path(json.loads((meta / "c_download_metadata.json").read_text(encoding="utf-8"))["dataset_root"])
    c_source_yaml = meta / "construction-ppe.yaml"
    urllib.request.urlretrieve(
        "https://raw.githubusercontent.com/ultralytics/ultralytics/42044baf5eda3d52aa4bd7d8a098375d2c7fdad7/ultralytics/cfg/datasets/construction-ppe.yaml",
        c_source_yaml,
    )
    c_clean = out / "clean" / "Construction-PPE"
    run(PY, str(stage2 / "apply_construction_ppe_stage2_corrections.py"),
        "--root", str(c_src), "--out", str(c_clean),
        "--file-manifest", str(stage2 / "results" / "Construction-PPE_conservative_file_correction_manifest_2026-09-20.csv"),
        "--orphan-label-manifest", str(stage2 / "results" / "Construction-PPE_orphan_label_removal_manifest_2026-09-20.csv"),
        "--expected-exclusions", "64", "--expected-orphan-removals", "10",
        "--expected-exact-row-removals", "1", "--summary-out", str(meta / "c_stage2_correction_summary.json"))

    # 3) Recompute the frozen annotation-only Stage 4.5 risk tables.
    audit_root = out / "stage45_audit"
    y_audit, c_audit = audit_root / "Y-PPE", audit_root / "Construction-PPE"
    audit = stage45 / "stage4_5_label_completeness_audit.py"
    run(PY, str(audit), "--dataset", "Y-PPE", "--root", str(y_clean),
        "--names-yaml", str(y_clean_yaml), "--splits", "train:train,val:valid,test:test", "--out", str(y_audit))
    run(PY, str(audit), "--dataset", "Construction-PPE", "--root", str(c_clean),
        "--names-yaml", str(c_source_yaml), "--splits", "train:train,val:val,test:test", "--out", str(c_audit))

    # 4) Apply exactly the conservative whole-image filter used in successful run 35536050231.
    policy = stage45 / "apply_stage4_5_conservative_filter.py"
    corrected_root = out / "clean_stage45"
    y_corrected, c_corrected = corrected_root / "Y-PPE", corrected_root / "Construction-PPE"
    run(PY, str(policy), "--root", str(y_clean), "--splits", "train:train,val:valid,test:test",
        "--risk-csv", str(y_audit / "image_risk_table.csv"), "--out", str(y_corrected),
        "--summary-out", str(meta / "y_stage45_policy_summary.json"),
        "--exclusion-manifest-out", str(meta / "y_stage45_exclusion_manifest.csv"),
        "--expected-exclusions", "510")
    run(PY, str(policy), "--root", str(c_clean), "--splits", "train:train,val:val,test:test",
        "--risk-csv", str(c_audit / "image_risk_table.csv"), "--out", str(c_corrected),
        "--summary-out", str(meta / "c_stage45_policy_summary.json"),
        "--exclusion-manifest-out", str(meta / "c_stage45_exclusion_manifest.csv"),
        "--expected-exclusions", "36")

    # 5) Build the final nine-class derivatives.
    h9_root = out / "h9_v2"
    y_h9, c_h9 = h9_root / "Y-PPE-h9-v2", h9_root / "Construction-PPE-h9-v2"
    builder = stage3 / "build_harmonized_detection_dataset.py"
    ontology = stage3 / "ontology_frozen_v1.yaml"
    run(PY, str(builder), "--root", str(y_corrected), "--data-yaml", str(y_clean_yaml),
        "--ontology", str(ontology), "--dataset-key", "Y-PPE",
        "--splits", "train:train,valid:val,test:test", "--out", str(y_h9),
        "--summary-out", str(meta / "y_h9_v2_summary.json"))
    run(PY, str(builder), "--root", str(c_corrected), "--data-yaml", str(c_source_yaml),
        "--ontology", str(ontology), "--dataset-key", "Construction-PPE",
        "--splits", "train:train,val:val,test:test", "--out", str(c_h9),
        "--summary-out", str(meta / "c_h9_v2_summary.json"))

    observed = {
        "Y-PPE-h9-v2": sha256_file(y_h9 / "manifest.jsonl"),
        "Construction-PPE-h9-v2": sha256_file(c_h9 / "manifest.jsonl"),
    }
    if observed != EXPECTED:
        raise SystemExit(f"Final Stage 4.5 fingerprint reproduction failed: {observed} != {EXPECTED}")

    for name, summary_path in (("Y-PPE-h9-v2", meta / "y_h9_v2_summary.json"),
                               ("Construction-PPE-h9-v2", meta / "c_h9_v2_summary.json")):
        s = json.loads(summary_path.read_text(encoding="utf-8"))
        counts = {k: v["images"] for k, v in s["splits"].items()}
        if counts != EXPECTED_COUNTS[name]:
            raise SystemExit(f"Unexpected {name} split counts: {counts} != {EXPECTED_COUNTS[name]}")
        if any(v.get("empty_label_images", 0) != 0 for v in s["splits"].values()):
            raise SystemExit(f"Unexpected harmonized-empty image in {name}")

    # 6) Create byte-preserving RF-DETR layout views.
    rf_root = out / "rfdetr_views"
    for name, root in (("Y-PPE-h9-v2", y_h9), ("Construction-PPE-h9-v2", c_h9)):
        run(PY, str(stage5 / "make_rfdetr_yolo_view.py"), "--source-root", str(root),
            "--out", str(rf_root / name), "--expected-fingerprint", EXPECTED[name])

    summary = {
        "status": "PASS",
        "stage4_5_policy_closed": True,
        "freeze_run_id": 35536050231,
        "frozen_fingerprints": observed,
        "frozen_counts": EXPECTED_COUNTS,
        "yolo_roots": {"Y-PPE-h9-v2": str(y_h9), "Construction-PPE-h9-v2": str(c_h9)},
        "rfdetr_roots": {"Y-PPE-h9-v2": str(rf_root / "Y-PPE-h9-v2"),
                         "Construction-PPE-h9-v2": str(rf_root / "Construction-PPE-h9-v2")},
        "test_membership_policy": "annotation-only conservative whole-image exclusion; frozen before Stage 5",
        "test_pixels_opened_for_membership": False,
        "model_predictions_used_for_membership": False,
        "raw_data_committed_to_git": False,
    }
    (meta / "stage5_dataset_materialization_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
