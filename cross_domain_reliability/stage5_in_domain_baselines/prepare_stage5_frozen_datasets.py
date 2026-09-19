#!/usr/bin/env python3
"""Reconstruct the exact Stage 5 frozen datasets on a training machine.

Requires internet access and ROBOFLOW_API_KEY in the environment. Raw datasets,
clean derivatives, and harmonized derivatives are written only to --out-root;
nothing is committed to GitHub. The script reuses the audited Stage 2/4
correction manifests and refuses to finish unless the Stage 4 fingerprints are
reproduced exactly.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
PY = sys.executable
EXPECTED = {
    "Y-PPE-h9": "db49295a0ef2c9eec73b14c620966ed00bf12dac253866b65bab9b50af9db896",
    "Construction-PPE-h9": "bd706ae34aa77507f119a9a4d5cd443d4cb84ee6cd2020b9b8ee6e086350880e",
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
    meta = out / "meta"
    meta.mkdir()

    stage2 = REPO / "cross_domain_reliability" / "stage2_data_audit"
    stage3 = REPO / "cross_domain_reliability" / "stage3_semantic_harmonization"
    stage5 = REPO / "cross_domain_reliability" / "stage5_in_domain_baselines"

    # 1) Y-PPE Version 2 raw export.
    y_download = out / "downloads" / "y_ppe"
    run(
        PY, str(stage2 / "download_roboflow_dataset.py"),
        "--workspace", "master-fylfq",
        "--project", "altayyar-0oflt-lafos-qqauz-ty5nh",
        "--version", "2",
        "--format", "yolov11",
        "--out", str(y_download),
        "--metadata-out", str(meta / "y_download_metadata.json"),
    )
    y_src = Path(json.loads((meta / "y_download_metadata.json").read_text(encoding="utf-8"))["dataset_location"])

    y_clean = out / "clean" / "Y-PPE"
    run(
        PY, str(stage2 / "apply_y_ppe_stage2_corrections.py"),
        "--root", str(y_src),
        "--out", str(y_clean),
        "--file-manifest", str(stage2 / "results" / "Y-PPE_v2_conservative_file_correction_manifest_2026-09-19.csv"),
        "--near-box-manifest", str(stage2 / "results" / "Y-PPE_v2_near_box_removal_manifest_2026-09-19.csv"),
        "--expected-exclusions", "39",
        "--expected-exact-row-removals", "68",
        "--expected-near-box-removals", "1",
        "--summary-out", str(meta / "y_correction_summary.json"),
    )
    y_yaml_candidates = list(y_clean.rglob("data.yaml")) + list(y_clean.rglob("dataset.yaml"))
    if not y_yaml_candidates:
        raise SystemExit("Could not locate cleaned Y-PPE data.yaml")
    y_clean_yaml = y_yaml_candidates[0]

    # 2) Pinned official Construction-PPE archive + audited corrections.
    c_download = out / "downloads" / "construction_ppe"
    run(
        PY, str(stage2 / "download_ultralytics_construction_ppe.py"),
        "--out", str(c_download),
        "--metadata-out", str(meta / "c_download_metadata.json"),
    )
    c_meta = json.loads((meta / "c_download_metadata.json").read_text(encoding="utf-8"))
    c_src = Path(c_meta["dataset_root"])

    # Use the exact pinned class-order YAML already frozen by Stage 4.
    import urllib.request
    pinned_yaml_url = "https://raw.githubusercontent.com/ultralytics/ultralytics/42044baf5eda3d52aa4bd7d8a098375d2c7fdad7/ultralytics/cfg/datasets/construction-ppe.yaml"
    c_source_yaml = meta / "construction-ppe.yaml"
    urllib.request.urlretrieve(pinned_yaml_url, c_source_yaml)

    c_clean = out / "clean" / "Construction-PPE"
    run(
        PY, str(stage2 / "apply_construction_ppe_stage2_corrections.py"),
        "--root", str(c_src),
        "--out", str(c_clean),
        "--file-manifest", str(stage2 / "results" / "Construction-PPE_conservative_file_correction_manifest_2026-09-20.csv"),
        "--orphan-label-manifest", str(stage2 / "results" / "Construction-PPE_orphan_label_removal_manifest_2026-09-20.csv"),
        "--expected-exclusions", "64",
        "--expected-orphan-removals", "10",
        "--expected-exact-row-removals", "1",
        "--summary-out", str(meta / "c_correction_summary.json"),
    )

    # 3) Rebuild frozen h9 derivatives.
    h9_root = out / "h9"
    y_h9 = h9_root / "Y-PPE-h9"
    c_h9 = h9_root / "Construction-PPE-h9"
    ontology = stage3 / "ontology_frozen_v1.yaml"
    builder = stage3 / "build_harmonized_detection_dataset.py"

    run(
        PY, str(builder), "--root", str(y_clean), "--data-yaml", str(y_clean_yaml),
        "--ontology", str(ontology), "--dataset-key", "Y-PPE",
        "--splits", "train:train,valid:val,test:test", "--out", str(y_h9),
        "--summary-out", str(meta / "y_harmonization_summary.json"),
    )
    run(
        PY, str(builder), "--root", str(c_clean), "--data-yaml", str(c_source_yaml),
        "--ontology", str(ontology), "--dataset-key", "Construction-PPE",
        "--splits", "train:train,val:val,test:test", "--out", str(c_h9),
        "--summary-out", str(meta / "c_harmonization_summary.json"),
    )

    observed = {
        "Y-PPE-h9": sha256_file(y_h9 / "manifest.jsonl"),
        "Construction-PPE-h9": sha256_file(c_h9 / "manifest.jsonl"),
    }
    if observed != EXPECTED:
        raise SystemExit(f"Stage 4 fingerprint reproduction failed: {observed} != {EXPECTED}")

    # 4) Layout-only RF-DETR views; manifests remain byte-identical.
    rf_root = out / "rfdetr_views"
    for name, root in (("Y-PPE-h9", y_h9), ("Construction-PPE-h9", c_h9)):
        run(
            PY, str(stage5 / "make_rfdetr_yolo_view.py"),
            "--source-root", str(root),
            "--out", str(rf_root / name),
            "--expected-fingerprint", EXPECTED[name],
        )

    summary = {
        "status": "PASS",
        "frozen_fingerprints": observed,
        "yolo_roots": {
            "Y-PPE-h9": str(y_h9),
            "Construction-PPE-h9": str(c_h9),
        },
        "rfdetr_roots": {
            "Y-PPE-h9": str(rf_root / "Y-PPE-h9"),
            "Construction-PPE-h9": str(rf_root / "Construction-PPE-h9"),
        },
        "raw_data_committed_to_git": False,
    }
    (meta / "stage5_dataset_materialization_summary.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
