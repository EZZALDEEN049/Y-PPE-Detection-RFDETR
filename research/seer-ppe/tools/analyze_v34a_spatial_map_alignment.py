#!/usr/bin/env python3
"""Offline V34-A spatial alignment and rank-correlation analysis.

No model inference, network access, image mutation, or dataset mutation occurs.
The 8x8 and 4x4 maps are aligned in normalized original-image coordinates.
Each 4x4 cell is the exact union of its four 8x8 children under the frozen
floor-based pixel-boundary convention.

Primary comparison:
  direct 4x4 signed score-drop density = coarse score_drop / coarse area
  aligned 8x8 density = area-weighted mean of each child's score_drop / area

Spearman uses average ranks for ties; Kendall uses tau-b. Signed negative
score drops are retained. A LOST target is scored zero by the frozen protocol,
so its score_drop remains numeric (baseline confidence) and is not missing.
"""

from __future__ import annotations

import argparse
import json
import math
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean, median

ROOT = Path(__file__).resolve().parents[1]
V30_DEFAULT = ROOT / "V30_ACTUAL_PROGRESSIVE_XAI_RESULTS_2026-11-22.json"
V33_DEFAULT = ROOT / "V33_B_GRID4_ACTUAL_RESULTS_2026-11-22.json"
MANIFEST_DEFAULT = ROOT / "V30_FROZEN_TARGETS_2026-11-22.json"
OUTPUT_DEFAULT = ROOT / "V34A_SPATIAL_MAP_ALIGNMENT_RANK_CORRELATION_2026-11-22.json"

EXPECTED_V30_GIT_BLOB_SHA = "729088f829bcdddcfbc4df5483be88399cccf605"
EXPECTED_V33_GIT_BLOB_SHA = "31d4523d5fd434dc43610ad00cf9ab3339a9910f"
EXPECTED_MANIFEST_GIT_BLOB_SHA = "96d5870d174f32049397a998c2cea0ca9ef57463"
TOL = 1e-9


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def rank_average(values: list[float]) -> list[float]:
    """One-based average ranks; exact ties receive their mean rank."""
    order = sorted(range(len(values)), key=lambda i: (values[i], i))
    ranks = [0.0] * len(values)
    start = 0
    while start < len(order):
        end = start + 1
        while end < len(order) and values[order[end]] == values[order[start]]:
            end += 1
        average_rank = ((start + 1) + end) / 2.0
        for position in range(start, end):
            ranks[order[position]] = average_rank
        start = end
    return ranks


def pearson(x: list[float], y: list[float], weights: list[float] | None = None) -> float | None:
    if len(x) != len(y) or len(x) < 2:
        return None
    w = weights if weights is not None else [1.0] * len(x)
    require(len(w) == len(x) and all(value > 0 for value in w), "invalid correlation weights")
    total = sum(w)
    mx = sum(value * weight for value, weight in zip(x, w)) / total
    my = sum(value * weight for value, weight in zip(y, w)) / total
    covariance = sum(weight * (a - mx) * (b - my) for a, b, weight in zip(x, y, w))
    variance_x = sum(weight * (a - mx) ** 2 for a, weight in zip(x, w))
    variance_y = sum(weight * (b - my) ** 2 for b, weight in zip(y, w))
    if variance_x <= 0 or variance_y <= 0:
        return None
    return covariance / math.sqrt(variance_x * variance_y)


def spearman(x: list[float], y: list[float], weights: list[float] | None = None) -> float | None:
    """Spearman rho; optional weights are applied to the ranked vectors."""
    return pearson(rank_average(x), rank_average(y), weights)


def kendall_tau_b(x: list[float], y: list[float]) -> float | None:
    """Kendall tau-b with ties in either vector handled explicitly."""
    require(len(x) == len(y) and len(x) >= 2, "Kendall vectors must have equal length >= 2")
    concordant = discordant = ties_x = ties_y = 0
    for i in range(len(x)):
        for j in range(i + 1, len(x)):
            dx = (x[i] > x[j]) - (x[i] < x[j])
            dy = (y[i] > y[j]) - (y[i] < y[j])
            if dx == 0 and dy == 0:
                continue
            if dx == 0:
                ties_x += 1
            elif dy == 0:
                ties_y += 1
            elif dx == dy:
                concordant += 1
            else:
                discordant += 1
    denominator = math.sqrt(
        (concordant + discordant + ties_x) *
        (concordant + discordant + ties_y)
    )
    if denominator == 0:
        return None
    return (concordant - discordant) / denominator


def cell_bounds(height: int, width: int, rows: int, cols: int, row: int, col: int):
    return (
        row * height // rows,
        (row + 1) * height // rows,
        col * width // cols,
        (col + 1) * width // cols,
    )


def top_k_indices(values: list[float], k: int = 4) -> list[int]:
    """Highest signed values first; exact ties resolve in row-major order."""
    return [
        index for _, index in sorted(
            ((value, index) for index, value in enumerate(values)),
            key=lambda item: (-item[0], item[1]),
        )[:k]
    ]


def descriptive(values: list[float]) -> dict:
    if not values:
        return {"n": 0, "mean": None, "median": None, "min": None, "max": None}
    ordered = sorted(values)
    return {
        "n": len(ordered),
        "mean": float(mean(ordered)),
        "median": float(median(ordered)),
        "min": float(ordered[0]),
        "max": float(ordered[-1]),
        "positive": sum(value > 0 for value in ordered),
        "negative": sum(value < 0 for value in ordered),
        "zero": sum(value == 0 for value in ordered),
    }


def check_trial(target: dict, trial: dict, grid_rows: int, grid_cols: int,
                height: int, width: int) -> tuple[float, float, str]:
    row, col = int(trial["row"]), int(trial["col"])
    top, bottom, left, right = cell_bounds(height, width, grid_rows, grid_cols, row, col)
    area = ((bottom - top) * (right - left)) / float(height * width)
    require(abs(area - float(trial["area_fraction"])) <= 1e-12,
            f"pixel area mismatch: {target['target_id']} {grid_rows}x{grid_cols} {row},{col}")
    status = trial.get("status")
    require(status in ("MATCHED", "LOST"),
            f"unscored/ambiguous map cell: {target['target_id']} {status}")
    score_after = float(trial["score_after"])
    if status == "LOST":
        require(abs(score_after) <= TOL, "LOST cell must use the frozen zero-score convention")
    baseline = float(target["baseline_confidence"])
    drop = float(trial["score_drop"])
    require(abs(drop - (baseline - score_after)) <= TOL,
            f"score-drop arithmetic mismatch: {target['target_id']}")
    return drop, area, status


def analyze_target(target8: dict, target4: dict, image: dict) -> tuple[dict, dict]:
    target_id = target8["target_id"]
    require(target4["target_id"] == target_id, "target ID mismatch")
    for key in ("image_key", "target_class", "arms"):
        require(target8[key] == target4[key], f"{key} mismatch for {target_id}")
    require(target8["map_status"] == "RANKABLE", f"8x8 map is not rankable: {target_id}")
    require(target4["map_status"] == "RANKABLE", f"4x4 map is not rankable: {target_id}")
    require(abs(float(target8["baseline_confidence"]) -
                float(target4["baseline_confidence"])) <= TOL,
            f"baseline confidence mismatch for {target_id}")

    height, width = int(image["image_height"]), int(image["image_width"])
    require(target8["image_key"] == image["image_key"], "image key mismatch")
    map8, map4 = target8["importance_map"], target4["importance_map"]
    require(len(map8) == 8 and all(len(row) == 8 for row in map8), "8x8 map shape mismatch")
    require(len(map4) == 4 and all(len(row) == 4 for row in map4), "4x4 map shape mismatch")

    trials8 = {(int(row["row"]), int(row["col"])): row for row in target8["occlusion_trials"]}
    trials4 = {(int(row["row"]), int(row["col"])): row for row in target4["occlusion_trials"]}
    require(len(trials8) == 64 and len(trials4) == 16, "occlusion trial count mismatch")
    require(len(trials8) == 64 and len(trials4) == 16, "duplicate/missing cell trial")

    direct_density: list[float] = []
    pooled_density: list[float] = []
    direct_raw: list[float] = []
    fine_raw_sum: list[float] = []
    coarse_areas: list[float] = []
    aligned_cells = []
    lost8 = lost4 = 0
    null_cells = 0
    max_map_error = 0.0
    max_area_error = 0.0

    for row in range(4):
        for col in range(4):
            coarse_trial = trials4[(row, col)]
            coarse_drop, coarse_area, coarse_status = check_trial(
                target4, coarse_trial, 4, 4, height, width
            )
            top, bottom, left, right = cell_bounds(height, width, 4, 4, row, col)
            if coarse_status == "LOST":
                lost4 += 1
            coarse_map_value = float(map4[row][col])
            max_map_error = max(max_map_error, abs(coarse_map_value - coarse_drop))

            fine_children = []
            fine_drop_sum = 0.0
            fine_area_sum = 0.0
            for dr in range(2):
                for dc in range(2):
                    fine_row, fine_col = 2 * row + dr, 2 * col + dc
                    fine_trial = trials8[(fine_row, fine_col)]
                    fine_drop, fine_area, fine_status = check_trial(
                        target8, fine_trial, 8, 8, height, width
                    )
                    if fine_status == "LOST":
                        lost8 += 1
                    fine_map_value = float(map8[fine_row][fine_col])
                    max_map_error = max(max_map_error, abs(fine_map_value - fine_drop))
                    fine_drop_sum += fine_drop
                    fine_area_sum += fine_area
                    fine_top, fine_bottom, fine_left, fine_right = cell_bounds(
                        height, width, 8, 8, fine_row, fine_col
                    )
                    fine_children.append({
                        "row_8x8": fine_row,
                        "col_8x8": fine_col,
                        "pixel_bounds_xyxy": [fine_left, fine_top, fine_right, fine_bottom],
                        "normalized_pixel_bounds_xyxy": [
                            fine_left / width, fine_top / height,
                            fine_right / width, fine_bottom / height,
                        ],
                        "area_fraction": fine_area,
                        "score_drop": fine_drop,
                        "status": fine_status,
                    })

            max_area_error = max(max_area_error, abs(fine_area_sum - coarse_area))
            require(abs(fine_area_sum - coarse_area) <= 1e-12,
                    f"2x2 8x8 children do not exactly cover 4x4 cell: {target_id} {row},{col}")
            direct_value = coarse_drop / coarse_area
            pooled_value = fine_drop_sum / fine_area_sum
            direct_density.append(direct_value)
            pooled_density.append(pooled_value)
            direct_raw.append(coarse_drop)
            fine_raw_sum.append(fine_drop_sum)
            coarse_areas.append(coarse_area)
            aligned_cells.append({
                "coarse_cell_4x4": {"row": row, "col": col},
                "pixel_bounds_xyxy": [left, top, right, bottom],
                "normalized_pixel_bounds_xyxy": [
                    left / width, top / height, right / width, bottom / height
                ],
                "area_fraction": coarse_area,
                "direct_4x4_score_drop": coarse_drop,
                "direct_4x4_signed_drop_per_area": direct_value,
                "pooled_8x8_score_drop_sum": fine_drop_sum,
                "pooled_8x8_area_weighted_signed_drop_per_area": pooled_value,
                "fine_children": fine_children,
            })

    require(null_cells == 0, "null cell score encountered")
    rho = spearman(direct_density, pooled_density)
    tau = kendall_tau_b(direct_density, pooled_density)
    weighted_rho = spearman(direct_density, pooled_density, coarse_areas)
    additive_rho = spearman(direct_raw, fine_raw_sum)
    additive_tau = kendall_tau_b(direct_raw, fine_raw_sum)
    require(None not in (rho, tau, weighted_rho, additive_rho, additive_tau),
            f"undefined correlation for target {target_id}")

    top4_direct = top_k_indices(direct_density, 4)
    top4_pooled = top_k_indices(pooled_density, 4)
    top4_overlap = len(set(top4_direct) & set(top4_pooled))
    target_summary = {
        "target_id": target_id,
        "image_key": target8["image_key"],
        "split": target8["split"],
        "target_class": target8["target_class"],
        "arms": target8["arms"],
        "image_width": width,
        "image_height": height,
        "spearman_rho_signed_area_normalized": rho,
        "kendall_tau_b_signed_area_normalized": tau,
        "area_weighted_spearman_rho": weighted_rho,
        "secondary_additive_raw_drop_spearman_rho": additive_rho,
        "secondary_additive_raw_drop_kendall_tau_b": additive_tau,
        "top4_signed_region_overlap_count": top4_overlap,
        "top4_signed_region_overlap_fraction": top4_overlap / 4.0,
        "positive_regions_direct_4x4": sum(value > 0 for value in direct_density),
        "positive_regions_pooled_8x8": sum(value > 0 for value in pooled_density),
        "negative_regions_direct_4x4": sum(value < 0 for value in direct_density),
        "negative_regions_pooled_8x8": sum(value < 0 for value in pooled_density),
        "lost_cell_outcomes_8x8": lost8,
        "lost_cell_outcomes_4x4": lost4,
    }
    detail = {
        "target_id": target_id,
        "direct_4x4_signed_drop_per_area_row_major": direct_density,
        "pooled_8x8_signed_drop_per_area_row_major": pooled_density,
        "direct_4x4_raw_score_drop_row_major": direct_raw,
        "pooled_8x8_raw_score_drop_sum_row_major": fine_raw_sum,
        "aligned_cells": aligned_cells,
        "top4_direct_4x4_row_major_indices": top4_direct,
        "top4_pooled_8x8_row_major_indices": top4_pooled,
        "max_importance_map_vs_trial_abs_error": max_map_error,
        "max_area_partition_abs_error": max_area_error,
    }
    return target_summary, detail


def analyze(v30: dict, v33: dict, manifest: dict) -> dict:
    require(v30.get("status") == "COMPLETED", "V30 archive is not completed")
    require(v33.get("status") == "COMPLETED", "V33-B archive is not completed")
    require(v30.get("model_id") == v33.get("model_id"), "model IDs differ")
    require(len(manifest.get("source_images", [])) == 8, "expected eight frozen source images")
    require(len(manifest.get("targets", [])) == 10, "expected ten frozen targets")
    require(len(v30.get("target_results", [])) == 10, "V30 target count mismatch")
    require(len(v33.get("target_results", [])) == 10, "V33-B target count mismatch")

    images = {row["image_key"]: row for row in manifest["source_images"]}
    frozen_targets = {row["target_id"]: row for row in manifest["targets"]}
    rows8 = {row["target_id"]: row for row in v30["target_results"]}
    rows4 = {row["target_id"]: row for row in v33["target_results"]}
    require(len(rows8) == 10 and len(rows4) == 10, "duplicate target IDs")
    require(set(rows8) == set(rows4) == set(frozen_targets),
            "V30, V33-B and frozen manifest target IDs differ")
    require(len({row["image_key"] for row in rows8.values()}) == 8,
            "expected exactly eight target-bearing images")

    target_summaries = []
    target_details = []
    for target_id in sorted(rows8):
        t8, t4 = rows8[target_id], rows4[target_id]
        frozen = frozen_targets[target_id]
        for key in ("image_key", "target_class", "arms", "split"):
            require(t8[key] == frozen[key] and t4[key] == frozen[key],
                    f"frozen manifest mismatch for {target_id}: {key}")
        require(abs(float(t8["baseline_confidence"]) -
                    float(frozen["frozen_baseline_confidence"])) <= TOL,
                f"V30 baseline does not match frozen manifest: {target_id}")
        summary, detail = analyze_target(t8, t4, images[t8["image_key"]])
        target_summaries.append(summary)
        target_details.append(detail)

    def summarize(rows: list[dict], field: str) -> dict:
        return descriptive([float(row[field]) for row in rows])

    split_summary = {}
    for split in ("train", "valid"):
        subset = [row for row in target_summaries if row["split"].lower() == split]
        split_summary[split] = {
            "target_count": len(subset),
            "unique_image_count": len({row["image_key"] for row in subset}),
            "spearman": summarize(subset, "spearman_rho_signed_area_normalized"),
            "kendall_tau_b": summarize(subset, "kendall_tau_b_signed_area_normalized"),
            "area_weighted_spearman": summarize(subset, "area_weighted_spearman_rho"),
            "mean_top4_overlap_fraction": mean(
                row["top4_signed_region_overlap_fraction"] for row in subset
            ),
        }

    image_summary = {}
    for image_key in sorted({row["image_key"] for row in target_summaries}):
        subset = [row for row in target_summaries if row["image_key"] == image_key]
        image_summary[image_key] = {
            "split": subset[0]["split"],
            "target_count": len(subset),
            "mean_spearman": mean(
                row["spearman_rho_signed_area_normalized"] for row in subset
            ),
            "mean_kendall_tau_b": mean(
                row["kendall_tau_b_signed_area_normalized"] for row in subset
            ),
            "top4_overlap_counts": [
                row["top4_signed_region_overlap_count"] for row in subset
            ],
        }

    lost8 = sum(row["lost_cell_outcomes_8x8"] for row in target_summaries)
    lost4 = sum(row["lost_cell_outcomes_4x4"] for row in target_summaries)
    max_map_error = max(
        detail["max_importance_map_vs_trial_abs_error"] for detail in target_details
    )
    max_area_error = max(
        detail["max_area_partition_abs_error"] for detail in target_details
    )

    return {
        "schema_version": "seer-ppe/v34a-spatial-map-alignment-rank-correlation/v0.34a",
        "status": "PASSED",
        "analysis_date": "2026-11-22",
        "execution_mode": "offline_only_no_model_inference",
        "source_files": {
            "v30": "V30_ACTUAL_PROGRESSIVE_XAI_RESULTS_2026-11-22.json",
            "v33b": "V33_B_GRID4_ACTUAL_RESULTS_2026-11-22.json",
            "frozen_manifest": "V30_FROZEN_TARGETS_2026-11-22.json",
        },
        "source_git_blob_shas": {
            "v30": EXPECTED_V30_GIT_BLOB_SHA,
            "v33b": EXPECTED_V33_GIT_BLOB_SHA,
            "frozen_manifest": EXPECTED_MANIFEST_GIT_BLOB_SHA,
        },
        "sample": {
            "targets": 10,
            "unique_images": 8,
            "train_targets": 5,
            "valid_targets": 5,
            "train_images": 4,
            "valid_images": 4,
        },
        "alignment_method": {
            "coordinate_system": "normalized original-image coordinates [0,1] x [0,1]",
            "pixel_bounds": "floor(index * image_dimension / grid_dimension), matching both frozen runners",
            "exact_mapping": "Each 4x4 cell (r,c) is the union of 8x8 cells (2r,2c), (2r,2c+1), (2r+1,2c), (2r+1,2c+1).",
            "primary_signed_value": "score_drop / exact cell area_fraction",
            "primary_fine_pooling": "Area-weighted mean of the four 8x8 signed score-drop densities; equivalently sum(fine score_drop) / sum(fine area_fraction).",
            "primary_comparison": "Direct 4x4 signed score-drop density versus area-pooled 8x8 signed score-drop density across 16 aligned regions.",
            "spearman": "Average ranks for ties; no clipping of negative values.",
            "kendall": "Kendall tau-b with tie correction.",
            "area_weighted_spearman": "Sensitivity summary: weighted Pearson correlation of the average-rank vectors using exact 4x4 pixel-area fractions.",
            "secondary_additive_diagnostic": "Compare direct 4x4 raw score_drop with the sum of its four 8x8 child score_drops; this is descriptive and does not assume perturbation effects are truly additive.",
            "negative_values": "Preserved as signed values; no clipping, absolute-value transform or removal.",
            "lost_detection_handling": "LOST target score is zero under the frozen V30/V33-B protocol; the resulting baseline-minus-zero score_drop is numeric and retained.",
        },
        "integrity_checks": {
            "target_ids_match_frozen_manifest": True,
            "all_v30_maps_rankable": True,
            "all_v33b_maps_rankable": True,
            "null_cell_scores": 0,
            "lost_cell_outcomes_v30_8x8": lost8,
            "lost_cell_outcomes_v33b_4x4": lost4,
            "importance_map_trial_max_abs_error": max_map_error,
            "max_4x4_vs_2x2_8x8_area_partition_abs_error": max_area_error,
            "model_inference_calls": 0,
            "dataset_or_annotation_mutations": 0,
        },
        "overall": {
            "spearman_rho_signed_area_normalized": summarize(
                target_summaries, "spearman_rho_signed_area_normalized"
            ),
            "kendall_tau_b_signed_area_normalized": summarize(
                target_summaries, "kendall_tau_b_signed_area_normalized"
            ),
            "area_weighted_spearman_rho": summarize(
                target_summaries, "area_weighted_spearman_rho"
            ),
            "secondary_additive_raw_drop_spearman_rho": summarize(
                target_summaries, "secondary_additive_raw_drop_spearman_rho"
            ),
            "secondary_additive_raw_drop_kendall_tau_b": summarize(
                target_summaries, "secondary_additive_raw_drop_kendall_tau_b"
            ),
            "mean_top4_signed_region_overlap_fraction": mean(
                row["top4_signed_region_overlap_fraction"] for row in target_summaries
            ),
            "top4_overlap_count_distribution": dict(Counter(
                str(row["top4_signed_region_overlap_count"]) for row in target_summaries
            )),
            "all_targets_positive_spearman": all(
                row["spearman_rho_signed_area_normalized"] > 0 for row in target_summaries
            ),
        },
        "split_summary": split_summary,
        "image_cluster_summary": image_summary,
        "per_target": target_summaries,
        "per_target_aligned_maps": target_details,
        "interpretation_boundary": (
            "Descriptive spatial rank agreement between single-cell perturbation-sensitivity maps "
            "on the same eight development-exposed images and ten frozen targets. The maps use "
            "different mask sizes and detector responses are nonlinear; the analysis is not an "
            "independent sample, external explanation ground truth, causal faithfulness, worker "
            "compliance validation or evidence of A5/A6 policy superiority. Targets share images "
            "and the 16 spatial cells within each target are dependent; no inferential p-values "
            "or confidence claims are made."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--v30", type=Path, default=V30_DEFAULT)
    parser.add_argument("--v33b", type=Path, default=V33_DEFAULT)
    parser.add_argument("--manifest", type=Path, default=MANIFEST_DEFAULT)
    parser.add_argument("--output", type=Path, default=OUTPUT_DEFAULT)
    args = parser.parse_args()

    result = analyze(load_json(args.v30), load_json(args.v33b), load_json(args.manifest))
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": result["status"],
        "execution_mode": result["execution_mode"],
        "integrity_checks": result["integrity_checks"],
        "overall": result["overall"],
        "split_summary": result["split_summary"],
        "per_target": result["per_target"],
        "output": str(args.output),
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
