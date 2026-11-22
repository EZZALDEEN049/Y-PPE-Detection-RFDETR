#!/usr/bin/env python3
"""Run the frozen SEER-PPE V33-B 4x4 grid robustness experiment.

This runner is deliberately separate from V30. It reuses the exact V30
source bundle, target IDs, target geometry, original-image baseline scores,
model ID and inference thresholds. It never reads Test and never mutates the
Roboflow project, annotations, splits or model.

No hosted inference is possible without the explicit
--confirm-additional-call-budget 496 argument. Dry-run and preflight modes
make zero model calls. Failed calls are logged before the request and are
never automatically retried.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Sequence

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from seer_ppe.detection_match import Detection  # noqa: E402
from seer_ppe.progressive_xai import (  # noqa: E402
    cell_bounds,
    gaussian_blur_baseline,
    progressive_curve,
    rank_grid_cells,
    stable_random_order,
    target_score,
)

MODEL_ID = "altayyar-0oflt-lafos-qqauz/2"
CONFIDENCE = 0.20
OVERLAP = 0.50
GRID_ROWS = 4
GRID_COLS = 4
STEP_PERCENT = 10
EXPECTED_IMAGES = 8
EXPECTED_TARGETS = 10
BLUR_ENDPOINT_CALLS = EXPECTED_IMAGES
GRID_OCCLUSION_CALLS = EXPECTED_IMAGES * GRID_ROWS * GRID_COLS
CURVE_CALLS_PER_TARGET = 2 * 2 * 9  # saliency/random x deletion/insertion x 9 interior points
MAX_CURVE_TARGETS = EXPECTED_TARGETS
MAX_ADDITIONAL_CALLS = (
    BLUR_ENDPOINT_CALLS + GRID_OCCLUSION_CALLS +
    CURVE_CALLS_PER_TARGET * MAX_CURVE_TARGETS
)
MANIFEST_DEFAULT = ROOT / "V30_FROZEN_TARGETS_2026-11-22.json"
PREFLIGHT_DEFAULT = ROOT / "V30_BASELINE_PREFLIGHT_ACTUAL_2026-11-22.json"
V30_RESULTS_DEFAULT = ROOT / "V30_ACTUAL_PROGRESSIVE_XAI_RESULTS_2026-11-22.json"
OUTPUT_DEFAULT = ROOT / "V33_B_GRID4_ACTUAL_RESULTS_2026-11-22.json"


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json_atomic(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def read_rgb(path: Path) -> np.ndarray:
    with Image.open(path) as image:
        return np.asarray(image.convert("RGB"), dtype=np.uint8)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def expected_call_count(curve_eligible_targets: int) -> int:
    if not isinstance(curve_eligible_targets, int) or not 0 <= curve_eligible_targets <= EXPECTED_TARGETS:
        raise ValueError("curve_eligible_targets must be an integer from 0 through 10")
    return BLUR_ENDPOINT_CALLS + GRID_OCCLUSION_CALLS + CURVE_CALLS_PER_TARGET * curve_eligible_targets


def grid4_cells(height: int, width: int) -> list[dict]:
    """Return all 16 nonempty row-major cells with exact pixel bounds and areas."""
    if height < GRID_ROWS or width < GRID_COLS:
        raise ValueError("image is too small for the frozen 4x4 grid")
    cells = []
    for row in range(GRID_ROWS):
        for col in range(GRID_COLS):
            top, bottom, left, right = cell_bounds(
                height, width, GRID_ROWS, GRID_COLS, row, col
            )
            cells.append({
                "row": row, "col": col,
                "top": top, "bottom": bottom, "left": left, "right": right,
                "area_fraction": ((bottom - top) * (right - left)) / float(height * width),
            })
    if len(cells) != 16 or abs(sum(c["area_fraction"] for c in cells) - 1.0) > 1e-12:
        raise RuntimeError("4x4 cells do not partition the source image exactly")
    return cells


def build_grid4_importance_map(
    image: np.ndarray,
    reference: Detection,
    predict: Callable[[np.ndarray], Sequence[Detection]],
    before_cell: Callable[[int, int], None] | None = None,
) -> tuple[np.ndarray, list[dict]]:
    """Build one target map using 16 cell inferences; ambiguous cells stay NaN."""
    rgb = np.asarray(image)
    if rgb.ndim != 3 or rgb.shape[2] != 3 or rgb.dtype != np.uint8:
        raise ValueError("uint8 RGB image with shape HxWx3 required")
    height, width = rgb.shape[:2]
    importance = np.full((GRID_ROWS, GRID_COLS), np.nan, dtype=np.float64)
    trials = []
    for cell in grid4_cells(height, width):
        row, col = cell["row"], cell["col"]
        altered = rgb.copy()
        altered[cell["top"]:cell["bottom"], cell["left"]:cell["right"], :] = 127
        if before_cell is not None:
            before_cell(row, col)
        score_after, status, iou = target_score(reference, predict(altered))
        score_drop = None if score_after is None else float(reference.score - score_after)
        if score_drop is not None:
            importance[row, col] = score_drop
        trials.append({
            "row": row, "col": col, "status": status,
            "score_after": score_after, "score_drop": score_drop,
            "matched_iou": iou, "area_fraction": cell["area_fraction"],
        })
    return importance, trials


def _frozen_reference(target: dict) -> Detection:
    box = target["bbox_center_xywh"]
    return Detection(
        target["target_class"], float(box["x"]), float(box["y"]),
        float(box["width"]), float(box["height"]),
        float(target["frozen_baseline_confidence"]),
    )


def validate_and_prepare(
    manifest: dict, preflight: dict, v30: dict, images_dir: Path
) -> tuple[dict, dict]:
    """Fail closed unless the eight local images and ten targets match V30 exactly."""
    if manifest.get("schema_version") != "seer-ppe/v30-frozen-progressive-xai-targets/v0.30":
        raise ValueError("unexpected frozen V30 target manifest")
    if manifest.get("model_id") != MODEL_ID:
        raise ValueError("frozen manifest model ID mismatch")
    if len(manifest.get("source_images", [])) != EXPECTED_IMAGES:
        raise ValueError("frozen manifest must contain exactly eight source images")
    if len(manifest.get("targets", [])) != EXPECTED_TARGETS:
        raise ValueError("frozen manifest must contain exactly ten targets")
    if preflight.get("status") != "PASSED":
        raise ValueError("V30 original-image connector preflight did not pass")
    model = preflight.get("model", {})
    if model.get("model_id") != MODEL_ID:
        raise ValueError("V30 preflight model ID mismatch")
    if model.get("confidence_threshold") != CONFIDENCE or model.get("overlap_threshold") != OVERLAP:
        raise ValueError("V30 preflight confidence/overlap settings mismatch")
    summary = preflight.get("summary", {})
    if summary.get("source_images_inferred") != EXPECTED_IMAGES:
        raise ValueError("V30 preflight did not infer exactly eight frozen images")
    if summary.get("targets_reproduced_exactly") != EXPECTED_TARGETS:
        raise ValueError("V30 preflight did not reproduce all ten frozen targets")
    if summary.get("targets_with_geometry_mismatch") != 0 or summary.get("targets_with_confidence_mismatch") != 0:
        raise ValueError("V30 preflight reports a target mismatch")
    if not preflight.get("guardrails", {}).get("no_test_accessed", False):
        raise ValueError("V30 preflight does not affirm the protected Test boundary")

    if v30.get("status") != "COMPLETED" or v30.get("model_id") != MODEL_ID:
        raise ValueError("V30 actual XAI archive is not a completed matching experiment")
    if v30.get("total_v30_model_inference_calls") != 1068:
        raise ValueError("V30 archived inference-call ledger is not the frozen 1,068-call run")
    if v30.get("inference_settings", {}).get("confidence") != CONFIDENCE:
        raise ValueError("V30 archived confidence threshold mismatch")
    if v30.get("inference_settings", {}).get("overlap") != OVERLAP:
        raise ValueError("V30 archived overlap threshold mismatch")
    if not v30.get("constraints", {}).get("no_test_accessed", False):
        raise ValueError("V30 archive does not affirm the protected Test boundary")

    preflight_images = {row["image_key"]: row for row in preflight.get("source_images", [])}
    v30_images = v30.get("baseline_images", {})
    if len(preflight_images) != EXPECTED_IMAGES or len(v30_images) != EXPECTED_IMAGES:
        raise ValueError("V30 preflight/archive must contain exactly eight unique image records")
    v30_targets = {row["target_id"]: row for row in v30.get("target_results", [])}
    if len(v30_targets) != EXPECTED_TARGETS:
        raise ValueError("V30 archive must contain exactly ten unique target records")

    targets_by_image: dict[str, list[dict]] = {}
    for target in manifest["targets"]:
        targets_by_image.setdefault(target["image_key"], []).append(target)
    if set(targets_by_image) != {row["image_key"] for row in manifest["source_images"]}:
        raise ValueError("target/image grouping does not match the frozen eight-image manifest")

    prepared = {}
    hash_records = {}
    for image in manifest["source_images"]:
        image_key = image["image_key"]
        path = images_dir / image["filename"]
        if not path.is_file():
            raise FileNotFoundError(f"frozen source image is missing: {image['filename']}")
        rgb = read_rgb(path)
        if rgb.shape[:2] != (int(image["image_height"]), int(image["image_width"])):
            raise ValueError(f"source image dimensions changed for {image['filename']}")
        digest = sha256_file(path)

        archived = v30_images.get(image_key)
        if archived is None:
            raise ValueError(f"V30 archived source hash missing for {image_key}")
        expected_identity = {
            "filename": image["filename"], "asset_id": image["asset_id"],
            "split": image["split"], "width": int(image["image_width"]),
            "height": int(image["image_height"]),
        }
        for key, expected in expected_identity.items():
            if archived.get(key) != expected:
                raise ValueError(f"V30 archived {key} mismatch for {image_key}")
        if archived.get("local_file_sha256") != digest:
            raise ValueError(f"local source SHA-256 does not match the frozen V30 bundle for {image_key}")

        remote = preflight_images.get(image_key)
        if remote is None:
            raise ValueError(f"V30 connector preflight is missing {image_key}")
        for key, expected in expected_identity.items():
            if remote.get(key) != expected:
                raise ValueError(f"V30 connector preflight {key} mismatch for {image_key}")
        if not remote.get("source_url"):
            raise ValueError(f"V30 connector preflight source URL is missing for {image_key}")

        remote_targets = {row["target_id"]: row for row in remote.get("targets", [])}
        references = {}
        for target in targets_by_image[image_key]:
            target_id = target["target_id"]
            remote_target = remote_targets.get(target_id)
            archived_target = v30_targets.get(target_id)
            if remote_target is None or archived_target is None:
                raise ValueError(f"frozen target {target_id} is missing from V30 evidence")
            if remote_target.get("status") != "MATCHED" or not remote_target.get("geometry_exact") or not remote_target.get("confidence_exact"):
                raise ValueError(f"V30 original-image target reproduction is not exact for {target_id}")
            if remote_target.get("class") != target["target_class"]:
                raise ValueError(f"V30 preflight target class mismatch for {target_id}")
            for key, value in target["bbox_center_xywh"].items():
                if abs(float(remote_target["bbox_center_xywh"][key]) - float(value)) > 1e-9:
                    raise ValueError(f"V30 preflight target geometry mismatch for {target_id}")
            confidence = float(target["frozen_baseline_confidence"])
            if abs(float(remote_target["confidence"]) - confidence) > 1e-9:
                raise ValueError(f"V30 preflight target confidence mismatch for {target_id}")
            if archived_target.get("image_key") != image_key or archived_target.get("target_class") != target["target_class"]:
                raise ValueError(f"V30 archived target identity mismatch for {target_id}")
            if archived_target.get("arms") != target.get("arms"):
                raise ValueError(f"V30 archived A5/A6 arm assignment mismatch for {target_id}")
            if abs(float(archived_target.get("baseline_confidence", -1)) - confidence) > 1e-9:
                raise ValueError(f"V30 archived target baseline mismatch for {target_id}")
            references[target_id] = _frozen_reference(target)

        prepared[image_key] = {"image": rgb, "references": references}
        hash_records[image_key] = {
            **expected_identity, "sha256": digest,
            "matches_v30_cloud_runner_bundle_hash": True,
            "independent_source_hash_available": False,
        }

    return prepared, hash_records


def _prediction_rows(response: dict) -> list[Detection]:
    predictions = response.get("predictions")
    if not isinstance(predictions, list):
        raise RuntimeError("hosted inference response has no predictions list")
    rows = []
    for prediction in predictions:
        class_name = prediction.get("class") or prediction.get("class_name")
        rows.append(Detection(
            str(class_name), float(prediction["x"]), float(prediction["y"]),
            float(prediction["width"]), float(prediction["height"]),
            float(prediction["confidence"]),
        ))
    return rows


class BudgetedHostedPredictor:
    """Hosted predictor with write-ahead per-call logging and no retry path."""
    def __init__(self, output_path: Path, max_calls: int = MAX_ADDITIONAL_CALLS):
        api_key = os.getenv("ROBOFLOW_API_KEY")
        if not api_key:
            raise RuntimeError("ROBOFLOW_API_KEY is not set; no inference was started")
        from inference_sdk import InferenceConfiguration, InferenceHTTPClient
        configuration = InferenceConfiguration(
            api_key_transport="header",
            confidence_threshold=CONFIDENCE,
            iou_threshold=OVERLAP,
        )
        self.client = InferenceHTTPClient(
            api_url="https://serverless.roboflow.com", api_key=api_key
        )
        self.client.configure(configuration)
        self.max_calls = max_calls
        self.calls_attempted = 0
        self.calls_succeeded = 0
        self.call_ledger: list[dict] = []
        self.context: dict = {}
        self.context_sequence = 0
        self.partial_path = output_path.with_name(output_path.name + ".partial.json")

    def set_context(self, **context) -> None:
        self.context = dict(context)
        self.context_sequence = 0

    def persist_partial(self, run_status: str = "IN_PROGRESS", failure_type: str | None = None) -> None:
        write_json_atomic(self.partial_path, {
            "schema_version": "seer-ppe/v33b-grid4-call-ledger/v0.33b",
            "status": run_status,
            "calls_attempted": self.calls_attempted,
            "calls_succeeded": self.calls_succeeded,
            "calls_failed": sum(row["status"] == "FAILED" for row in self.call_ledger),
            "max_additional_call_budget": self.max_calls,
            "failure_type": failure_type,
            "call_ledger": self.call_ledger,
            "no_test_accessed": True,
            "automatic_retries": False,
        })

    def __call__(self, image: np.ndarray) -> list[Detection]:
        if self.calls_attempted >= self.max_calls:
            raise RuntimeError("hard V33-B additional-call budget reached; refusing another inference")
        self.calls_attempted += 1
        entry = {
            "call_index": self.calls_attempted,
            **self.context,
            "context_sequence": self.context_sequence,
            "status": "STARTED",
        }
        self.context_sequence += 1
        self.call_ledger.append(entry)
        self.persist_partial()
        try:
            with tempfile.NamedTemporaryFile(suffix=".png") as temporary:
                Image.fromarray(np.asarray(image, dtype=np.uint8)).save(temporary.name, format="PNG")
                response = self.client.infer(temporary.name, model_id=MODEL_ID)
            detections = _prediction_rows(response)
            entry["status"] = "SUCCEEDED"
            self.calls_succeeded += 1
            return detections
        except Exception as error:
            entry["status"] = "FAILED"
            entry["error_type"] = type(error).__name__
            raise
        finally:
            self.persist_partial()


def _mean(values: list[float]) -> float | None:
    finite = [float(value) for value in values if value is not None and np.isfinite(value)]
    return None if not finite else float(np.mean(finite))


def _auc(row: dict, ordering: str, direction: str) -> float | None:
    try:
        value = row["curves"][ordering][direction]["auc"]
        return None if value is None else float(value)
    except (KeyError, TypeError, ValueError):
        return None


def compare_with_v30(target_results: list[dict], v30: dict) -> dict:
    """Pair 4x4 and archived 8x8 outcomes by the exact frozen target IDs."""
    old_rows = {row["target_id"]: row for row in v30["target_results"]}
    comparisons = []
    metric_deltas = {
        "saliency_deletion_auc": [],
        "saliency_insertion_auc": [],
        "random_deletion_auc": [],
        "random_insertion_auc": [],
        "deletion_advantage": [],
        "insertion_advantage": [],
    }
    eligibility_matches = 0
    for new in target_results:
        old = old_rows[new["target_id"]]
        new_sd, new_si = _auc(new, "saliency", "deletion"), _auc(new, "saliency", "insertion")
        new_rd, new_ri = _auc(new, "random", "deletion"), _auc(new, "random", "insertion")
        old_sd, old_si = _auc(old, "saliency", "deletion"), _auc(old, "saliency", "insertion")
        old_rd, old_ri = _auc(old, "random", "deletion"), _auc(old, "random", "insertion")
        values = {
            "saliency_deletion_auc": (new_sd, old_sd),
            "saliency_insertion_auc": (new_si, old_si),
            "random_deletion_auc": (new_rd, old_rd),
            "random_insertion_auc": (new_ri, old_ri),
            "deletion_advantage": (None if new_sd is None or new_rd is None else new_rd - new_sd,
                                  None if old_sd is None or old_rd is None else old_rd - old_sd),
            "insertion_advantage": (None if new_si is None or new_ri is None else new_si - new_ri,
                                   None if old_si is None or old_ri is None else old_si - old_ri),
        }
        deltas = {}
        for name, (current, previous) in values.items():
            delta = None if current is None or previous is None else current - previous
            deltas[name + "_4x4_minus_8x8"] = delta
            if delta is not None:
                metric_deltas[name].append(delta)
        same_eligibility = new["map_status"] == old["map_status"]
        eligibility_matches += int(same_eligibility)
        comparisons.append({
            "target_id": new["target_id"],
            "image_key": new["image_key"],
            "target_class": new["target_class"],
            "v30_8x8_map_status": old["map_status"],
            "v33b_4x4_map_status": new["map_status"],
            "map_status_exact_match": same_eligibility,
            **deltas,
        })
    return {
        "paired_target_count": len(comparisons),
        "map_status_exact_matches": eligibility_matches,
        "map_status_exact_match_rate": eligibility_matches / len(comparisons) if comparisons else None,
        "mean_paired_deltas": {key: _mean(values) for key, values in metric_deltas.items()},
        "per_target": comparisons,
        "interpretation_boundary": (
            "Descriptive within-target grid-resolution robustness only; not a randomized "
            "comparison, causal faithfulness proof, independent generalization or safety outcome."
        ),
    }


def summarize_arms(target_results: list[dict]) -> dict:
    summary = {}
    for arm in ("A5", "A6"):
        selected = [row for row in target_results if arm in row["arms"]]
        summary[arm] = {
            "selected_target_count": len(selected),
            "shared_target_count": sum(set(row["arms"]) == {"A5", "A6"} for row in selected),
            "unique_target_count": sum(len(row["arms"]) == 1 for row in selected),
            "curve_complete_target_count": sum(row["curve_status"] == "EXECUTED" for row in selected),
            "saliency_deletion_auc_mean": _mean([_auc(row, "saliency", "deletion") for row in selected]),
            "saliency_insertion_auc_mean": _mean([_auc(row, "saliency", "insertion") for row in selected]),
            "random_deletion_auc_mean": _mean([_auc(row, "random", "deletion") for row in selected]),
            "random_insertion_auc_mean": _mean([_auc(row, "random", "insertion") for row in selected]),
        }
    return summary


def run_experiment(
    manifest: dict, prepared: dict, hash_records: dict, v30: dict,
    predictor: BudgetedHostedPredictor, output_path: Path
) -> dict:
    targets_by_image: dict[str, list[dict]] = {}
    for target in manifest["targets"]:
        targets_by_image.setdefault(target["image_key"], []).append(target)

    target_results = []
    curve_eligible_targets = 0
    for image in manifest["source_images"]:
        image_key = image["image_key"]
        rgb = prepared[image_key]["image"]
        references = prepared[image_key]["references"]
        blurred, blur_sigma = gaussian_blur_baseline(rgb)
        predictor.set_context(phase="gaussian_blur_endpoint", image_key=image_key)
        blurred_predictions = predictor(blurred)
        blurred_scores = {}
        for target_id, reference in references.items():
            score, status, iou = target_score(reference, blurred_predictions)
            blurred_scores[target_id] = {
                "score": None if score is None else float(score),
                "status": status, "iou": iou,
            }

        maps = {target_id: np.full((GRID_ROWS, GRID_COLS), np.nan, dtype=float)
                for target_id in references}
        trials = {target_id: [] for target_id in references}
        for cell in grid4_cells(rgb.shape[0], rgb.shape[1]):
            altered = rgb.copy()
            altered[cell["top"]:cell["bottom"], cell["left"]:cell["right"], :] = 127
            predictor.set_context(
                phase="grid4_single_cell_occlusion", image_key=image_key,
                grid_row=cell["row"], grid_col=cell["col"],
            )
            predictions = predictor(altered)
            for target_id, reference in references.items():
                score, status, iou = target_score(reference, predictions)
                drop = None if score is None else float(reference.score - score)
                if drop is not None:
                    maps[target_id][cell["row"], cell["col"]] = drop
                trials[target_id].append({
                    "row": cell["row"], "col": cell["col"], "status": status,
                    "score_after": score, "score_drop": drop, "matched_iou": iou,
                    "area_fraction": cell["area_fraction"],
                })

        for target in targets_by_image[image_key]:
            target_id = target["target_id"]
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
                for ordering in ("saliency", "random"):
                    curves[ordering] = {}
                    for direction in ("deletion", "insertion"):
                        curves[ordering][direction] = {
                            "points": [], "auc": None, "status": "NOT_RUN_" + block_reason,
                        }
                curve_status = "NOT_RUN_" + block_reason
            else:
                saliency_order = rank_grid_cells(importance)
                orderings = {
                    "saliency": saliency_order,
                    "random": stable_random_order(target_id, GRID_ROWS, GRID_COLS),
                }
                curve_eligible_targets += 1
                for ordering_name, ordering in orderings.items():
                    curves[ordering_name] = {}
                    for direction in ("deletion", "insertion"):
                        predictor.set_context(
                            phase="curve_intermediate", image_key=image_key,
                            target_id=target_id, ordering=ordering_name, direction=direction,
                        )
                        points, auc = progressive_curve(
                            rgb, blurred, reference, predictor, ordering,
                            direction=direction, ordering_name=ordering_name,
                            blurred_score=blurred_scores[target_id]["score"],
                            rows=GRID_ROWS, cols=GRID_COLS, step_percent=STEP_PERCENT,
                        )
                        curves[ordering_name][direction] = {
                            "points": [point.__dict__ for point in points],
                            "auc": auc,
                            "status": "EXECUTED" if auc is not None else "EXECUTED_AUC_BLOCKED_BY_AMBIGUOUS_POINT",
                        }
                curve_status = (
                    "EXECUTED" if all(curves[o][d]["auc"] is not None
                                      for o in ("saliency", "random")
                                      for d in ("deletion", "insertion"))
                    else "EXECUTED_WITH_AMBIGUOUS_CURVE_POINT"
                )

            target_results.append({
                "target_id": target_id, "image_key": image_key,
                "asset_id": target["asset_id"], "split": target["split"],
                "target_class": target["target_class"], "arms": target["arms"],
                "baseline_confidence": reference.score,
                "blurred_endpoint": blurred_scores[target_id],
                "blur_sigma_px": blur_sigma, "grid_rows": GRID_ROWS, "grid_cols": GRID_COLS,
                "map_status": map_status, "curve_status": curve_status,
                "importance_map": importance.tolist(),
                "occlusion_trials": trials[target_id], "curves": curves,
            })

    expected = expected_call_count(curve_eligible_targets)
    if predictor.calls_attempted != expected or predictor.calls_succeeded != expected:
        raise RuntimeError(
            f"call-ledger mismatch: expected {expected}, attempted {predictor.calls_attempted}, "
            f"succeeded {predictor.calls_succeeded}"
        )
    if predictor.calls_attempted > MAX_ADDITIONAL_CALLS:
        raise RuntimeError("V33-B exceeded its hard additional-call ceiling")

    result = {
        "schema_version": "seer-ppe/v33b-grid4-actual-results/v0.33b",
        "run_date_utc": datetime.now(timezone.utc).isoformat(),
        "status": "COMPLETED",
        "protocol": "V33_B_GRID4_PROSPECTIVE_PROTOCOL_2026-11-22.md",
        "model_id": MODEL_ID,
        "inference_settings": {"confidence": CONFIDENCE, "overlap": OVERLAP},
        "grid": {"rows": GRID_ROWS, "cols": GRID_COLS, "fill_rgb": [127, 127, 127],
                 "step_percent": STEP_PERCENT},
        "frozen_inputs": {
            "source_images": EXPECTED_IMAGES, "targets": EXPECTED_TARGETS,
            "source_hashes_matched_to_v30_bundle": len(hash_records),
            "source_hash_records": hash_records,
            "target_ids_match_v30": True,
            "original_baseline_calls_reused": 8,
        },
        "additional_call_budget": {
            "maximum": MAX_ADDITIONAL_CALLS,
            "actual_attempts": predictor.calls_attempted,
            "successful_calls": predictor.calls_succeeded,
            "expected_from_eligible_targets": expected,
            "curve_eligible_targets": curve_eligible_targets,
            "automatic_retries": False,
        },
        "call_ledger": predictor.call_ledger,
        "target_results": target_results,
        "A5_A6_summary": summarize_arms(target_results),
        "comparison_with_v30_8x8": compare_with_v30(target_results, v30),
        "constraints": {
            "no_test_accessed": True,
            "no_retraining": True,
            "original_images_annotations_splits_unchanged": True,
            "source_independence_verified": False,
            "worker_compliance_measured": False,
            "worker_safety_scoring_ready": False,
            "causal_faithfulness_proven": False,
            "claims_are_descriptive_only": True,
        },
    }
    write_json_atomic(output_path, result)
    if predictor.partial_path.exists():
        predictor.partial_path.unlink()
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--images-dir", type=Path, required=True,
                        help="Directory containing the exact eight V30 original image downloads.")
    parser.add_argument("--manifest", type=Path, default=MANIFEST_DEFAULT)
    parser.add_argument("--baseline-preflight", type=Path, default=PREFLIGHT_DEFAULT)
    parser.add_argument("--v30-results", type=Path, default=V30_RESULTS_DEFAULT)
    parser.add_argument("--output", type=Path, default=OUTPUT_DEFAULT)
    parser.add_argument("--dry-run", action="store_true",
                        help="Validate all frozen inputs and hashes; makes zero model calls.")
    parser.add_argument("--preflight-only", action="store_true",
                        help="Write a zero-inference readiness record after all frozen checks.")
    parser.add_argument("--confirm-additional-call-budget", type=int, default=None,
                        help="Required explicit authorization value: 496 additional hosted calls.")
    args = parser.parse_args()

    if args.dry_run and args.preflight_only:
        parser.error("choose either --dry-run or --preflight-only")
    manifest = read_json(args.manifest)
    preflight = read_json(args.baseline_preflight)
    v30 = read_json(args.v30_results)
    prepared, hash_records = validate_and_prepare(manifest, preflight, v30, args.images_dir)

    readiness = {
        "status": "READY_NO_MODEL_CALLS",
        "source_images": EXPECTED_IMAGES,
        "targets": EXPECTED_TARGETS,
        "source_hashes_matched_to_v30_bundle": len(hash_records),
        "expected_max_additional_calls": MAX_ADDITIONAL_CALLS,
        "call_count_formula": "8 blur endpoints + 128 grid cells + 36 per curve-eligible target",
        "no_model_calls_made": True,
        "no_test_accessed": True,
    }
    if args.dry_run:
        print(json.dumps(readiness, indent=2))
        return 0
    if args.preflight_only:
        readiness["schema_version"] = "seer-ppe/v33b-grid4-readiness/v0.33b"
        readiness["source_hash_records"] = hash_records
        write_json_atomic(args.output, readiness)
        print(json.dumps({**readiness, "output": str(args.output)}, indent=2))
        return 0
    if args.confirm_additional_call_budget != MAX_ADDITIONAL_CALLS:
        print(json.dumps({
            "status": "BLOCKED_NO_MODEL_CALLS",
            "reason": "explicit 496-call authorization is required",
            "required_flag": f"--confirm-additional-call-budget {MAX_ADDITIONAL_CALLS}",
            **readiness,
        }, indent=2))
        return 2

    try:
        predictor = BudgetedHostedPredictor(args.output, MAX_ADDITIONAL_CALLS)
    except Exception as error:
        print(json.dumps({
            "status": "BLOCKED_NO_MODEL_CALLS",
            "error_type": type(error).__name__,
            "reason": "hosted predictor could not be initialized; no inference was started",
            "no_test_accessed": True,
        }, indent=2))
        return 2

    try:
        result = run_experiment(manifest, prepared, hash_records, v30, predictor, args.output)
    except Exception as error:
        predictor.persist_partial("FAILED_NO_AUTOMATIC_RETRY", type(error).__name__)
        print(json.dumps({
            "status": "FAILED_NO_AUTOMATIC_RETRY",
            "error_type": type(error).__name__,
            "calls_attempted": predictor.calls_attempted,
            "calls_succeeded": predictor.calls_succeeded,
            "partial_ledger": str(predictor.partial_path),
            "no_test_accessed": True,
        }, indent=2))
        return 1

    print(json.dumps({
        "status": result["status"],
        "additional_calls": result["additional_call_budget"],
        "output": str(args.output),
        "no_test_accessed": True,
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
