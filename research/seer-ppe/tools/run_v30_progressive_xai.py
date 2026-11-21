#!/usr/bin/env python3
"""Execute the frozen SEER-PPE V30 progressive XAI pilot on local source images.

Images are read-only inputs. No image, URL, credential, annotation, model weight,
or Test asset is written to the repository. The full run requires explicit
confirmation of its frozen maximum 1,068-model-call budget.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import tempfile
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
from PIL import Image
from inference_sdk import InferenceConfiguration, InferenceHTTPClient

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = ROOT / "V30_FROZEN_TARGETS_2026-11-22.json"
MODEL_ID = "altayyar-0oflt-lafos-qqauz/2"
API_URL = "https://serverless.roboflow.com"
CONFIDENCE = 0.20
OVERLAP = 0.50
ROWS = 8
COLS = 8
STEP_PERCENT = 10
MAX_MODEL_CALLS = 1068

sys.path.insert(0, str(ROOT))
from seer_ppe.detection_match import Detection, match_target  # noqa: E402
from seer_ppe.progressive_xai import (  # noqa: E402
    gaussian_blur_baseline, progressive_curve, rank_grid_cells,
    stable_random_order, target_score,
)


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--images-dir", type=Path, required=True,
                        help="Local read-only folder containing the eight original V30 images.")
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--output", type=Path,
                        default=ROOT / "V30_ACTUAL_PROGRESSIVE_XAI_RESULTS_2026-11-22.json")
    parser.add_argument("--dry-run", action="store_true",
                        help="Validate manifest and image files without model calls.")
    parser.add_argument("--preflight-only", action="store_true",
                        help="Run only the eight original-image baseline checks.")
    parser.add_argument("--confirm-model-call-budget", type=int, default=None,
                        help=f"Required exact maximum confirmation value {MAX_MODEL_CALLS} for the full run.")
    return parser.parse_args()


def read_rgb(path: Path) -> np.ndarray:
    with Image.open(path) as image:
        return np.asarray(image.convert("RGB"), dtype=np.uint8)


def as_detection_rows(result: dict) -> list[Detection]:
    predictions = result.get("predictions")
    if not isinstance(predictions, list):
        raise RuntimeError("Inference response has no predictions list")
    detections = []
    for prediction in predictions:
        class_name = prediction.get("class") or prediction.get("class_name")
        detections.append(Detection(
            str(class_name), float(prediction["x"]), float(prediction["y"]),
            float(prediction["width"]), float(prediction["height"]),
            float(prediction["confidence"]),
        ))
    return detections


class HostedPredictor:
    def __init__(self, api_key: str):
        configuration = InferenceConfiguration(
            api_key_transport="header",
            confidence_threshold=CONFIDENCE,
            iou_threshold=OVERLAP,
        )
        self.client = InferenceHTTPClient(
            api_url=API_URL, api_key=api_key
        ).configure(configuration)
        self.calls = 0

    def __call__(self, image: np.ndarray) -> list[Detection]:
        with tempfile.NamedTemporaryFile(suffix=".jpg") as temporary:
            Image.fromarray(image).save(temporary.name, format="JPEG", quality=95)
            result = self.client.infer(temporary.name, model_id=MODEL_ID)
        self.calls += 1
        return as_detection_rows(result)


def frozen_reference(row: dict) -> Detection:
    box = row["bbox_center_xywh"]
    return Detection(
        row["target_class"], float(box["x"]), float(box["y"]),
        float(box["width"]), float(box["height"]),
        float(row["frozen_baseline_confidence"]),
    )


def group_targets(manifest: dict):
    groups = defaultdict(list)
    for row in manifest["targets"]:
        groups[row["image_key"]].append(row)
    return groups


def validate_local_inputs(manifest: dict, images_dir: Path):
    missing, mismatches = [], []
    for image in manifest["source_images"]:
        path = images_dir / image["filename"]
        if not path.is_file():
            missing.append(str(path))
            continue
        rgb = read_rgb(path)
        expected_hw = (int(image["image_height"]), int(image["image_width"]))
        if rgb.shape[:2] != expected_hw:
            mismatches.append({
                "filename": image["filename"],
                "expected_hw": expected_hw,
                "actual_hw": tuple(rgb.shape[:2]),
            })
    if missing or mismatches:
        raise RuntimeError(json.dumps({
            "missing_images": missing,
            "dimension_mismatches": mismatches,
        }, default=list))


def build_predictor():
    api_key = os.getenv("ROBOFLOW_API_KEY")
    if not api_key:
        raise SystemExit("ROBOFLOW_API_KEY is not set; no inference was started.")
    return HostedPredictor(api_key)


def prepare_references(manifest: dict, images_dir: Path, predict):
    """Run one baseline inference per source image and verify every frozen target."""
    prepared, baseline_records = {}, {}
    targets_by_image = group_targets(manifest)
    for image in manifest["source_images"]:
        image_key = image["image_key"]
        image_path = images_dir / image["filename"]
        rgb = read_rgb(image_path)
        predictions = predict(rgb)
        baseline_records[image_key] = {
            "filename": image["filename"],
            "sha256": hashlib.sha256(image_path.read_bytes()).hexdigest(),
            "prediction_count": len(predictions),
        }
        references = {}
        for row in targets_by_image[image_key]:
            frozen = frozen_reference(row)
            matched = match_target(frozen, predictions, min_iou=0.50, ambiguity_margin=0.03)
            if matched.status != "MATCHED":
                raise RuntimeError(
                    f"Baseline reproduction blocked for {row['target_id']}: {matched.status}"
                )
            if abs(float(matched.score_after) - frozen.score) > 0.08:
                raise RuntimeError(f"Baseline confidence drift >0.08 for {row['target_id']}")
            references[row["target_id"]] = Detection(
                frozen.class_name, frozen.x, frozen.y, frozen.width, frozen.height,
                float(matched.score_after),
            )
        prepared[image_key] = {"image": rgb, "references": references}
    return prepared, baseline_records


def run_preflight(manifest, images_dir, predictor, output_path):
    prepared, baseline = prepare_references(manifest, images_dir, predictor)
    result = {
        "schema_version": "seer-ppe/v30-baseline-preflight/v0.30",
        "status": "BASELINE_REPRODUCTION_PASSED",
        "model_id": MODEL_ID,
        "inference_settings": {"confidence": CONFIDENCE, "overlap": OVERLAP},
        "baseline_images": baseline,
        "verified_targets": sum(len(item["references"]) for item in prepared.values()),
        "model_inference_calls": predictor.calls,
        "progressive_xai_executed": False,
        "no_test_accessed": True,
        "original_model_or_data_modified": False,
    }
    output_path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


def run_full(manifest, images_dir, predictor, output_path):
    prepared, baseline_records = prepare_references(manifest, images_dir, predictor)
    targets_by_image = group_targets(manifest)
    target_results = []
    curve_eligible_targets = 0

    for image in manifest["source_images"]:
        image_key = image["image_key"]
        rgb = prepared[image_key]["image"]
        references = prepared[image_key]["references"]
        height, width = rgb.shape[:2]
        blurred, blur_sigma = gaussian_blur_baseline(rgb)
        blurred_predictions = predictor(blurred)
        blurred_scores = {}
        for target_id, reference in references.items():
            score, status, iou = target_score(reference, blurred_predictions)
            blurred_scores[target_id] = {
                "score": None if score is None else float(score),
                "status": status,
                "iou": iou,
            }

        maps = {target_id: np.full((ROWS, COLS), np.nan, dtype=float) for target_id in references}
        map_trials = {target_id: [] for target_id in references}
        # One masked inference per image/cell; share predictions across targets in that image.
        for row in range(ROWS):
            for col in range(COLS):
                top, bottom = row * height // ROWS, (row + 1) * height // ROWS
                left, right = col * width // COLS, (col + 1) * width // COLS
                altered = rgb.copy()
                altered[top:bottom, left:right, :] = 127
                predictions = predictor(altered)
                area_fraction = ((bottom - top) * (right - left)) / float(height * width)
                for target_id, reference in references.items():
                    score, status, iou = target_score(reference, predictions)
                    drop = None if score is None else float(reference.score - score)
                    if drop is not None:
                        maps[target_id][row, col] = drop
                    map_trials[target_id].append({
                        "row": row, "col": col, "status": status,
                        "score_after": score, "score_drop": drop,
                        "matched_iou": iou, "area_fraction": area_fraction,
                    })

        for row in targets_by_image[image_key]:
            target_id = row["target_id"]
            reference = references[target_id]
            importance = maps[target_id]
            if not np.isfinite(importance).all():
                map_status = "AMBIGUOUS_CELL"
            elif float(np.maximum(importance, 0.0).sum()) <= 0:
                map_status = "NO_POSITIVE_DROP"
            else:
                map_status = "RANKABLE"

            block_reason = None
            if map_status != "RANKABLE":
                block_reason = "MAP_" + map_status
            elif blurred_scores[target_id]["score"] is None:
                block_reason = "AMBIGUOUS_BLURRED_ENDPOINT"

            curves = {}
            if block_reason is not None:
                for ordering_name in ("saliency", "random", "inverse_saliency"):
                    curves[ordering_name] = {}
                    for direction in ("deletion", "insertion"):
                        curves[ordering_name][direction] = {
                            "points": [], "auc": None,
                            "status": "NOT_RUN_" + block_reason,
                        }
                curve_status = "NOT_RUN_" + block_reason
            else:
                saliency_order = rank_grid_cells(importance)
                orderings = {
                    "saliency": saliency_order,
                    "random": stable_random_order(target_id, ROWS, COLS),
                    "inverse_saliency": list(reversed(saliency_order)),
                }
                curve_eligible_targets += 1
                for ordering_name, ordering in orderings.items():
                    curves[ordering_name] = {}
                    for direction in ("deletion", "insertion"):
                        points, auc = progressive_curve(
                            rgb, blurred, reference, predictor, ordering,
                            direction=direction, ordering_name=ordering_name,
                            blurred_score=blurred_scores[target_id]["score"],
                            rows=ROWS, cols=COLS, step_percent=STEP_PERCENT,
                        )
                        curves[ordering_name][direction] = {
                            "points": [point.__dict__ for point in points],
                            "auc": auc,
                            "status": "EXECUTED" if auc is not None else "EXECUTED_AUC_BLOCKED_BY_AMBIGUOUS_POINT",
                        }
                curve_status = "EXECUTED"

            target_results.append({
                "target_id": target_id,
                "image_key": image_key,
                "filename": row["filename"],
                "asset_id": row["asset_id"],
                "split": row["split"],
                "target_class": row["target_class"],
                "arms": row["arms"],
                "baseline_confidence": reference.score,
                "blurred_endpoint": blurred_scores[target_id],
                "blur_sigma_px": blur_sigma,
                "map_status": map_status,
                "curve_status": curve_status,
                "importance_map": importance.tolist(),
                "occlusion_trials": map_trials[target_id],
                "curves": curves,
            })

    expected_actual_calls = 8 + 8 + 512 + 54 * curve_eligible_targets
    if predictor.calls != expected_actual_calls or predictor.calls > MAX_MODEL_CALLS:
        raise RuntimeError(
            f"Inference call-count mismatch: expected {expected_actual_calls} from "
            f"{curve_eligible_targets} curve-eligible targets, observed {predictor.calls}"
        )

    def mean_or_none(values):
        finite = [float(value) for value in values if value is not None and np.isfinite(value)]
        return None if not finite else float(np.mean(finite))

    arm_summary = {}
    for arm in ("A5", "A6"):
        selected = [result for result in target_results if arm in result["arms"]]
        arm_summary[arm] = {
            "selected_slots": len(selected),
            "shared_target_slots": sum(set(result["arms"]) == {"A5", "A6"} for result in selected),
            "unique_target_slots": sum(len(result["arms"]) == 1 for result in selected),
            "saliency_deletion_auc_mean": mean_or_none([
                result["curves"]["saliency"]["deletion"]["auc"] for result in selected]),
            "saliency_insertion_auc_mean": mean_or_none([
                result["curves"]["saliency"]["insertion"]["auc"] for result in selected]),
            "random_deletion_auc_mean": mean_or_none([
                result["curves"]["random"]["deletion"]["auc"] for result in selected]),
            "random_insertion_auc_mean": mean_or_none([
                result["curves"]["random"]["insertion"]["auc"] for result in selected]),
            "inverse_deletion_auc_mean": mean_or_none([
                result["curves"]["inverse_saliency"]["deletion"]["auc"] for result in selected]),
            "inverse_insertion_auc_mean": mean_or_none([
                result["curves"]["inverse_saliency"]["insertion"]["auc"] for result in selected]),
            "complete_target_count": sum(
                all(result["curves"][ordering][direction]["auc"] is not None
                    for ordering in ("saliency", "random", "inverse_saliency")
                    for direction in ("deletion", "insertion"))
                for result in selected),
        }

    result = {
        "schema_version": "seer-ppe/v30-actual-progressive-xai-results/v0.30",
        "run_date_utc": datetime.now(timezone.utc).isoformat(),
        "status": "COMPLETED" if len(target_results) == 10 else "INCOMPLETE",
        "protocol": "V30_FROZEN_PROGRESSIVE_XAI_PROTOCOL_2026-11-22.md",
        "target_manifest": manifest["schema_version"],
        "model_id": MODEL_ID,
        "inference_settings": {"confidence": CONFIDENCE, "overlap": OVERLAP},
        "explainer": manifest["explainer"],
        "curve_settings": manifest["curves"],
        "baseline_images": baseline_records,
        "model_inference_calls": predictor.calls,
        "planned_model_inference_calls_max": MAX_MODEL_CALLS,
        "curve_eligible_targets": curve_eligible_targets,
        "target_results": target_results,
        "A5_A6_summary": arm_summary,
        "constraints": {
            "no_test_accessed": True,
            "original_model_or_data_modified": False,
            "source_independence_verified": False,
            "worker_compliance_measured": False,
            "human_review_dispatched": False,
            "worker_safety_scoring_ready": False,
            "claims_are_descriptive_only": True,
        },
    }
    output_path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": result["status"],
        "model_inference_calls": predictor.calls,
        "planned_model_inference_calls_max": MAX_MODEL_CALLS,
        "curve_eligible_targets": curve_eligible_targets,
        "A5_A6_summary": arm_summary,
        "output": str(output_path),
    }, indent=2))


def main():
    args = parse_args()
    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    if manifest.get("model_id") != MODEL_ID or len(manifest.get("targets", [])) != 10:
        raise SystemExit("Frozen V30 manifest/model/target count check failed")
    if len(manifest.get("source_images", [])) != 8:
        raise SystemExit("Frozen V30 manifest must contain eight target-bearing source images")
    validate_local_inputs(manifest, args.images_dir)
    if args.dry_run:
        print(json.dumps({
            "status": "DRY_RUN_INPUTS_VALID",
            "source_images": len(manifest["source_images"]),
            "unique_targets": len(manifest["targets"]),
            "planned_model_inference_calls_max": MAX_MODEL_CALLS,
            "no_model_calls_made": True,
        }, indent=2))
        return
    predictor = build_predictor()
    if args.preflight_only:
        run_preflight(manifest, args.images_dir, predictor, args.output)
        return
    if args.confirm_model_call_budget != MAX_MODEL_CALLS:
        raise SystemExit(
            f"Full run blocked: pass --confirm-model-call-budget {MAX_MODEL_CALLS} "
            "after reviewing the frozen maximum call budget. No inference was started."
        )
    run_full(manifest, args.images_dir, predictor, args.output)


if __name__ == "__main__":
    main()
