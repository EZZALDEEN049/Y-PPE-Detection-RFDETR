#!/usr/bin/env python3
"""Deterministically freeze V38-B XAI target candidates from archived V26 files.

Zero network, zero Roboflow inference, zero raw image access and no Test reads.
Run: python tools/v38b_freeze_sample_and_budget.py --output research/seer-ppe/V38_B_FROZEN_CANDIDATE_SAMPLE_2026-11-23.json
Check: python tools/v38b_freeze_sample_and_budget.py --check research/seer-ppe/V38_B_FROZEN_CANDIDATE_SAMPLE_2026-11-23.json
"""
import argparse
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "research" / "seer-ppe"
SEED = "SEER-PPE|V38-B|2026-11-23|preregistered-v1"
CLASSES = [
    "Hard Hat", "No Hard Hat", "Safety Vests", "No Safety Vest",
    "Gloves", "No Gloves", "Safety Boots", "No Safety Boots",
    "Face Masks", "No Face Mask", "Goggles",
]
N_IMAGES, TARGETS_PER_IMAGE, RANDOM_IMAGES, ABLATION_IMAGES, RANDOM_SEEDS = 24, 2, 12, 8, 10


def fnv1a32(s):
    h = 2166136261
    for c in s:
        h ^= ord(c)
        h = (h * 16777619) & 0xffffffff
    return h


def iou(a, b):
    x_overlap = max(0.0, min(a["x"] + a["width"] / 2, b["x"] + b["width"] / 2)
                    - max(a["x"] - a["width"] / 2, b["x"] - b["width"] / 2))
    y_overlap = max(0.0, min(a["y"] + a["height"] / 2, b["y"] + b["height"] / 2)
                    - max(a["y"] - a["height"] / 2, b["y"] - b["height"] / 2))
    intersection = x_overlap * y_overlap
    union = a["width"] * a["height"] + b["width"] * b["height"] - intersection
    return intersection / union if union else 0.0


def rankable_candidates():
    frozen = json.loads((ROOT / "V30_FROZEN_TARGETS_2026-11-22.json").read_text())
    old_ids = {x["source_id"] for x in frozen["source_images"] if x.get("source_id")}
    assert frozen["model_id"] == "altayyar-0oflt-lafos-qqauz/2"
    eligible = []
    row_count = 0
    for number in range(12):
        shard = ROOT / f"V26_ORIGINAL_VALID_GEOMETRY_SHARD_{number:02d}_OF_12.json"
        j = json.loads(shard.read_text())
        assert j["shard_index"] == number
        for r in j["rows"]:
            row_count += 1
            if (r.get("status") != "SCORED_INPUT_ACQUIRED" or
                    r.get("previously_reused_in_v23_pilot") or
                    r["source_id"] in old_ids or
                    r["image_width"] < 320 or r["image_height"] < 240):
                continue
            candidates_by_class = {}
            for p in r.get("model_predictions", []):
                if (p["cls"] not in CLASSES or p["confidence"] < 0.55 or
                        p["width"] < 16 or p["height"] < 16 or
                        p["width"] * p["height"] < 0.0003 * r["image_width"] * r["image_height"]):
                    continue
                ref_iou = max([0.0] + [iou(gt, p) for gt in r.get("current_author_boxes", []) if gt["cls"] == p["cls"]])
                if ref_iou < 0.50:
                    continue
                key = fnv1a32(SEED + "|prediction|" + p["id"])
                current = candidates_by_class.get(p["cls"])
                if current is None or key < current[0]:
                    candidates_by_class[p["cls"]] = (
                        key,
                        {
                            "target_id": p["id"],
                            "class_name": p["cls"],
                            "baseline_confidence_from_v26": p["confidence"],
                            "bbox_xywh": {k: p[k] for k in ("x", "y", "width", "height")},
                            "baseline_author_reference_iou": ref_iou,
                        }
                    )
            if len(candidates_by_class) >= 2:
                eligible.append({
                    "source_id": r["source_id"],
                    "image_key": "valid:" + r["source_id"],
                    "width": r["image_width"],
                    "height": r["image_height"],
                    "candidates": [v[1] for v in candidates_by_class.values()],
                })
    assert row_count == 459, row_count
    assert len(eligible) == 225, len(eligible)
    return eligible, row_count


def value(cls, counts):
    n = counts[cls]
    return (100 + 3 * (3 - n)) if n < 3 else (12 / (n + 1))


def build():
    eligible, rows = rankable_candidates()
    counts = Counter({cls: 0 for cls in CLASSES})
    chosen = []
    seen = set()
    for rank in range(1, N_IMAGES + 1):
        best = None
        for image in eligible:
            if image["source_id"] in seen:
                continue
            candidates = image["candidates"]
            for i in range(len(candidates)):
                for j in range(i + 1, len(candidates)):
                    a, b = candidates[i], candidates[j]
                    different_polarity = a["class_name"].startswith("No ") != b["class_name"].startswith("No ")
                    score = value(a["class_name"], counts) + value(b["class_name"], counts) + (0.25 if different_polarity else 0)
                    tie = fnv1a32(SEED + "|pick|" + image["source_id"] + "|" + "|".join(sorted((a["target_id"], b["target_id"]))))
                    if best is None or score > best[0] or (score == best[0] and tie < best[1]):
                        best = (score, tie, image, a, b)
        assert best is not None
        _, _, image, a, b = best
        seen.add(image["source_id"])
        counts[a["class_name"]] += 1
        counts[b["class_name"]] += 1
        chosen.append((image, a, b))
    images = [
        {"image_plan_rank": index + 1, "source_id": im["source_id"], "image_key": im["image_key"],
         "width": im["width"], "height": im["height"], "target_ids": [a["target_id"], b["target_id"]]}
        for index, (im, a, b) in enumerate(chosen)
    ]
    targets = []
    for index, (im, a, b) in enumerate(chosen):
        for offset, target in enumerate((a, b)):
            targets.append({"target_plan_rank": index * 2 + offset + 1,
                            "image_plan_rank": index + 1,
                            "source_id": im["source_id"], "image_key": im["image_key"],
                            **target})
    assert len(images) == 24 and len(targets) == 48
    assert len({x["source_id"] for x in images}) == 24
    assert len({x["target_id"] for x in targets}) == 48
    assert sorted(counts.values()) == [4] * 7 + [5] * 4, counts
    assert len({t["class_name"] for t in targets}) == 11
    budget = {
        "primary_single_cell_maps_24_images_x_64_plus_16": 24 * (64 + 16),
        "new_original_and_full_blur_baselines_24_x_2": 24 * 2,
        "seeded_random_8x8_progressive_12_targets_x_11_orders_x_2_dirs_x_9_points": 12 * 11 * 2 * 9,
        "saliency_4x4_progressive_12_targets_x_2_dirs_x_9_points": 12 * 2 * 9,
        "alternative_fill_maps_8_images_x_64_plus_16": 8 * (64 + 16),
    }
    assert sum(budget.values()) == 5200
    result = {
        "schema_version": "seer-ppe/v38b-prospective-candidate-freeze/v1",
        "recorded_date": "2026-11-23",
        "status": "FROZEN_CANDIDATES_AND_BUDGET_ONLY_NO_NEW_MODEL_CALLS",
        "study_cohort": "previously_development_exposed_original_source_valid_internal_diagnostic_not_independent_field_generalization",
        "source_shards": [f"research/seer-ppe/V26_ORIGINAL_VALID_GEOMETRY_SHARD_{i:02d}_OF_12.json" for i in range(12)],
        "historical_source_rows": rows,
        "eligible_image_pool_count": len(eligible),
        "selection_seed": SEED,
        "selection_algorithm": "deterministic FNV1a32 tie-broken balanced greedy 24 images, two different PPE classes per image, quota >=4 each across eleven; historical V26 class-exact IoU>=.50 and prediction confidence>=.55, no XAI scores used",
        "selection_guards": {
            "original_split": "valid",
            "excluded_previous_v30_original_valid_images": True,
            "excluded_previous_v23_pilot_images": True,
            "min_image_width_height": [320, 240],
            "min_prediction_confidence": 0.55,
            "min_prediction_box_width_height": [16, 16],
            "min_prediction_relative_area": 0.0003,
            "min_prediction_to_current_author_reference_class_exact_iou": 0.50,
            "different_classes_per_image": True,
            "source_family_or_acquisition_independence": "NOT_VERIFIED",
            "raw_photograph_publication_rights": "NOT_ASSERTED",
            "protected_test": "NOT_ACCESSED"
        },
        "model": {"id": "altayyar-0oflt-lafos-qqauz/2", "confidence": 0.20,
                  "overlap": 0.50, "weights_changed": False},
        "images": images,
        "targets": targets,
        "class_distribution": dict(sorted(counts.items())),
        "random_progressive_target_ids_12_different_images": [a["target_id"] for im, a, b in chosen[:RANDOM_IMAGES]],
        "alternative_fill_image_ids_8": [im["source_id"] for im, a, b in chosen[:ABLATION_IMAGES]],
        "budget": {
            "calls_by_phase_max": budget,
            "planned_unique_call_upper_bound": sum(budget.values()),
            "technical_retry_reserve_only": 800,
            "hard_maximum_new_hosted_model_calls_including_retries": 6000,
            "actual_new_model_calls_in_this_freeze": 0,
            "other_algorithm_baselines_model_calls": 0,
            "external_xai_method_execution_authorized": False,
        },
        "release_gate": "HOLD_NEW_INFERENCE_UNTIL_SEPARATE_EXPLICIT_AUTHOR_APPROVAL_OF_6000_HARD_LIMIT_AND_READ_ONLY_SOURCE_PREFLIGHT",
        "missing_data_rules": "preserve target LOST=0, AMBIGUOUS=null; never impute null AUC or posthoc-replace frozen targets",
    }
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    parser.add_argument("--check", type=Path)
    args = parser.parse_args()
    manifest = build()
    if args.output and args.check:
        parser.error("--output and --check are mutually exclusive")
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf8")
    if args.check:
        saved = json.loads(args.check.read_text(encoding="utf8"))
        assert saved == manifest, "Candidate freeze has diverged from archived V26 sources, seed or algorithm"
    print(json.dumps({
        "result": "V38B_SAMPLE_AND_BUDGET_REPRODUCIBLE_PASS",
        "eligible_images": manifest["eligible_image_pool_count"],
        "images": len(manifest["images"]),
        "targets": len(manifest["targets"]),
        "class_distribution": manifest["class_distribution"],
        "budget": manifest["budget"],
    }, indent=2))


if __name__ == "__main__":
    main()
