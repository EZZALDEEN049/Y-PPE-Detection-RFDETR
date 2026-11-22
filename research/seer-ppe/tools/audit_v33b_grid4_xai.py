#!/usr/bin/env python3
"""Independent, read-only numeric audit of the completed V33-B 4x4 XAI run.

This script makes no model calls. It verifies the archived call ledger, frozen
target identity, curve points/AUCs, 4x4-vs-8x8 pairing and descriptive A5/A6
composition against the V30 manifest and V30 numeric archive.
"""
from __future__ import annotations

import argparse
import json
import math
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean, median

ROOT = Path(__file__).resolve().parents[1]
RESULT_DEFAULT = ROOT / "V33_B_GRID4_ACTUAL_RESULTS_2026-11-22.json"
V30_DEFAULT = ROOT / "V30_ACTUAL_PROGRESSIVE_XAI_RESULTS_2026-11-22.json"
MANIFEST_DEFAULT = ROOT / "V30_FROZEN_TARGETS_2026-11-22.json"
OUTPUT_DEFAULT = ROOT / "V33_B_GRID4_NUMERIC_AUDIT_2026-11-22.json"
MODEL_ID = "altayyar-0oflt-lafos-qqauz/2"
EXPECTED_CALLS = 496
TOL = 1e-12


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def auc_from_points(points: list[dict]) -> float | None:
    if len(points) != 11:
        raise ValueError("each progressive curve must contain eleven points")
    if any(point.get("normalized_score") is None for point in points):
        return None
    x = [float(point["modified_fraction"]) for point in points]
    y = [float(point["normalized_score"]) for point in points]
    if not all(math.isfinite(value) for value in x + y):
        return None
    if abs(x[0]) > TOL or abs(x[-1] - 1.0) > TOL:
        return None
    if any(right <= left for left, right in zip(x, x[1:])):
        return None
    return sum((y[i] + y[i + 1]) * (x[i + 1] - x[i]) / 2.0
               for i in range(len(x) - 1))


def metric(target: dict, ordering: str, direction: str) -> float | None:
    value = target["curves"][ordering][direction]["auc"]
    return None if value is None else float(value)


def descriptive(values: list[float]) -> dict:
    if not values:
        return {"n": 0, "mean": None, "median": None, "min": None, "max": None}
    return {
        "n": len(values),
        "mean": float(mean(values)),
        "median": float(median(values)),
        "min": float(min(values)),
        "max": float(max(values)),
        "positive": sum(value > 0 for value in values),
        "negative": sum(value < 0 for value in values),
        "zero": sum(value == 0 for value in values),
    }


def advantage_summary(targets: list[dict], direction: str) -> dict:
    advantages = []
    unscored = 0
    for target in targets:
        saliency = metric(target, "saliency", direction)
        random = metric(target, "random", direction)
        if saliency is None or random is None:
            unscored += 1
            continue
        advantages.append(random - saliency if direction == "deletion"
                          else saliency - random)
    summary = descriptive(advantages)
    summary.update({
        "favorable_saliency_targets": sum(value > 0 for value in advantages),
        "unfavorable_saliency_targets": sum(value < 0 for value in advantages),
        "unscored_targets": unscored,
        "absolute_margin_below_0_01": sum(abs(value) < 0.01 for value in advantages),
        "margin_above_0_05": sum(value > 0.05 for value in advantages),
        "definition": "random minus saliency for deletion; saliency minus random for insertion",
    })
    return summary


def paired_grid_delta(targets: list[dict], old_by_id: dict, ordering: str,
                      direction: str) -> dict:
    deltas = []
    for target in targets:
        old = metric(old_by_id[target["target_id"]], ordering, direction)
        new = metric(target, ordering, direction)
        if old is not None and new is not None:
            deltas.append(new - old)
    return descriptive(deltas)


def advantage_sign_agreement(targets: list[dict], old_by_id: dict,
                              direction: str) -> dict:
    same = changed = unavailable = 0
    for target in targets:
        old_target = old_by_id[target["target_id"]]
        new_s = metric(target, "saliency", direction)
        new_r = metric(target, "random", direction)
        old_s = metric(old_target, "saliency", direction)
        old_r = metric(old_target, "random", direction)
        if None in (new_s, new_r, old_s, old_r):
            unavailable += 1
            continue
        new_adv = new_r - new_s if direction == "deletion" else new_s - new_r
        old_adv = old_r - old_s if direction == "deletion" else old_s - old_r
        if (new_adv > 0) == (old_adv > 0) and (new_adv < 0) == (old_adv < 0):
            same += 1
        else:
            changed += 1
    return {
        "same_direction": same,
        "changed_direction": changed,
        "not_comparable": unavailable,
        "definition": "sign of saliency advantage over the single deterministic random order",
    }


def audit(result: dict, v30: dict, manifest: dict) -> dict:
    require(result.get("status") == "COMPLETED", "V33-B result is not COMPLETED")
    require(result.get("schema_version") == "seer-ppe/v33b-grid4-actual-results/v0.33b",
            "unexpected V33-B result schema")
    require(result.get("model_id") == MODEL_ID, "V33-B model ID mismatch")
    settings = result.get("inference_settings", {})
    require(settings.get("confidence") == 0.20 and settings.get("overlap") == 0.50,
            "V33-B inference settings mismatch")
    require(result.get("grid", {}).get("rows") == 4 and result.get("grid", {}).get("cols") == 4,
            "V33-B grid is not 4x4")

    require(v30.get("status") == "COMPLETED" and v30.get("model_id") == MODEL_ID,
            "V30 comparator archive is not a completed matching run")
    require(manifest.get("model_id") == MODEL_ID, "frozen manifest model ID mismatch")
    require(len(manifest.get("source_images", [])) == 8, "manifest must have eight images")
    require(len(manifest.get("targets", [])) == 10, "manifest must have ten targets")
    require(len(result.get("target_results", [])) == 10, "V33-B must contain ten target rows")
    require(len(v30.get("target_results", [])) == 10, "V30 must contain ten target rows")

    manifest_targets = {row["target_id"]: row for row in manifest["targets"]}
    new_targets = {row["target_id"]: row for row in result["target_results"]}
    old_targets = {row["target_id"]: row for row in v30["target_results"]}
    require(len(new_targets) == 10 and len(old_targets) == 10, "duplicate target IDs found")
    require(set(new_targets) == set(manifest_targets) == set(old_targets),
            "V33-B, V30 and frozen manifest target IDs differ")

    frozen = result.get("frozen_inputs", {})
    require(frozen.get("source_images") == 8 and frozen.get("targets") == 10,
            "frozen input counts mismatch")
    require(frozen.get("source_hashes_matched_to_v30_bundle") == 8,
            "not all eight source hashes match the V30 bundle")
    hash_records = frozen.get("source_hash_records", {})
    require(len(hash_records) == 8, "eight source hash records are required")
    require(all(row.get("matches_v30_cloud_runner_bundle_hash") is True
                for row in hash_records.values()), "one or more V30 bundle hash checks failed")
    require(all(row.get("independent_source_hash_available") is False
                for row in hash_records.values()),
            "hash provenance boundary changed; inspect before reporting")
    require(frozen.get("target_ids_match_v30") is True, "target IDs were not reused")
    require(frozen.get("original_baseline_calls_reused") == 8,
            "original baseline call reuse count mismatch")

    image_rows = manifest["source_images"]
    require(sum(row["split"].lower() == "train" for row in image_rows) == 4,
            "expected four Train images")
    require(sum(row["split"].lower() == "valid" for row in image_rows) == 4,
            "expected four Valid images")

    constraints = result.get("constraints", {})
    for key in ("no_test_accessed", "no_retraining",
                "original_images_annotations_splits_unchanged"):
        require(constraints.get(key) is True, f"constraint not affirmed: {key}")
    for key in ("source_independence_verified", "worker_compliance_measured",
                "worker_safety_scoring_ready", "causal_faithfulness_proven"):
        require(constraints.get(key) is False, f"unsupported claim flag changed: {key}")
    require(constraints.get("claims_are_descriptive_only") is True,
            "interpretation boundary is not descriptive-only")

    budget = result.get("additional_call_budget", {})
    eligible = budget.get("curve_eligible_targets")
    require(eligible == 10, "expected all ten targets to be curve-eligible")
    expected_calls = 8 + 8 * 16 + 36 * eligible
    require(expected_calls == EXPECTED_CALLS, "protocol call formula mismatch")
    require(budget.get("maximum") == EXPECTED_CALLS, "hard call cap mismatch")
    require(budget.get("actual_attempts") == EXPECTED_CALLS, "actual attempt count mismatch")
    require(budget.get("successful_calls") == EXPECTED_CALLS, "successful call count mismatch")
    require(budget.get("expected_from_eligible_targets") == EXPECTED_CALLS,
            "reported expected call count mismatch")
    require(budget.get("automatic_retries") is False, "automatic retry flag must be false")

    ledger = result.get("call_ledger", [])
    require(len(ledger) == EXPECTED_CALLS, "call ledger length mismatch")
    require([row.get("call_index") for row in ledger] == list(range(1, EXPECTED_CALLS + 1)),
            "call ledger indices are not contiguous")
    require(all(row.get("status") == "SUCCEEDED" for row in ledger),
            "call ledger contains a non-success status")
    phases = Counter(row.get("phase") for row in ledger)
    require(phases == Counter({
        "gaussian_blur_endpoint": 8,
        "grid4_single_cell_occlusion": 128,
        "curve_intermediate": 360,
    }), "phase-specific call counts mismatch")

    curve_calls = Counter()
    for row in ledger:
        if row.get("phase") == "curve_intermediate":
            key = (row.get("target_id"), row.get("ordering"), row.get("direction"))
            curve_calls[key] += 1
    expected_contexts = {
        (target_id, ordering, direction)
        for target_id in new_targets
        for ordering in ("saliency", "random")
        for direction in ("deletion", "insertion")
    }
    require(set(curve_calls) == expected_contexts, "curve call contexts differ from frozen targets")
    require(all(count == 9 for count in curve_calls.values()),
            "each curve must have exactly nine intermediate model calls")

    curve_counts = {}
    ambiguity_records = []
    auc_recompute_max_error = 0.0
    for target_id, target in new_targets.items():
        frozen_target = manifest_targets[target_id]
        old_target = old_targets[target_id]
        require(target.get("image_key") == frozen_target.get("image_key"),
                f"image key mismatch for {target_id}")
        require(target.get("target_class") == frozen_target.get("target_class"),
                f"class mismatch for {target_id}")
        require(target.get("arms") == frozen_target.get("arms"),
                f"A5/A6 assignment mismatch for {target_id}")
        require(target.get("arms") == old_target.get("arms"),
                f"V30 A5/A6 assignment mismatch for {target_id}")
        require(target.get("map_status") == "RANKABLE", f"4x4 map not rankable: {target_id}")
        require(target.get("grid_rows") == 4 and target.get("grid_cols") == 4,
                f"target grid mismatch for {target_id}")
        importance = target.get("importance_map", [])
        require(len(importance) == 4 and all(len(row) == 4 for row in importance),
                f"importance map shape mismatch for {target_id}")
        require(all(math.isfinite(float(value)) for row in importance for value in row),
                f"non-finite importance value for {target_id}")
        trials = target.get("occlusion_trials", [])
        require(len(trials) == 16, f"expected sixteen cell trials for {target_id}")
        require(abs(sum(float(row["area_fraction"]) for row in trials) - 1.0) <= TOL,
                f"4x4 cells do not sum to full image area for {target_id}")

        for ordering in ("saliency", "random"):
            for direction in ("deletion", "insertion"):
                curve = target["curves"][ordering][direction]
                points = curve.get("points", [])
                require(len(points) == 11, f"curve point count mismatch: {target_id}/{ordering}/{direction}")
                requested = [float(point["requested_fraction"]) for point in points]
                require(all(abs(a - b) <= TOL for a, b in zip(requested, [i / 10 for i in range(11)])),
                        f"requested curve fractions mismatch: {target_id}/{ordering}/{direction}")
                computed = auc_from_points(points)
                stored = curve.get("auc")
                if stored is None:
                    require(computed is None, f"stored null AUC but points integrate for {target_id}/{ordering}/{direction}")
                    ambiguity_records.extend([
                        {"target_id": target_id, "image_key": target["image_key"],
                         "target_class": target["target_class"], "ordering": ordering,
                         "direction": direction, "point": point}
                        for point in points if point.get("normalized_score") is None
                    ])
                else:
                    require(computed is not None, f"stored AUC exists but curve is incomplete: {target_id}/{ordering}/{direction}")
                    error = abs(float(stored) - computed)
                    auc_recompute_max_error = max(auc_recompute_max_error, error)
                    require(error <= TOL, f"AUC recomputation mismatch for {target_id}/{ordering}/{direction}")
                key = ordering + "_" + direction
                curve_counts.setdefault(key, {"curves": 0, "valid_auc": 0, "null_auc": 0})
                curve_counts[key]["curves"] += 1
                curve_counts[key]["valid_auc"] += int(stored is not None)
                curve_counts[key]["null_auc"] += int(stored is None)

    require(sum(row["valid_auc"] for row in curve_counts.values()) == 39,
            "expected 39 valid AUCs out of 40 curves")
    require(len(ambiguity_records) == 1,
            "expected exactly one non-imputed ambiguous curve point")

    map_status_matches = 0
    for target_id, target in new_targets.items():
        if target.get("map_status") == old_targets[target_id].get("map_status"):
            map_status_matches += 1
    require(map_status_matches == 10, "V30/V33-B map status mismatch")

    advantage = {
        "deletion": advantage_summary(list(new_targets.values()), "deletion"),
        "insertion": advantage_summary(list(new_targets.values()), "insertion"),
    }
    require(advantage["deletion"]["favorable_saliency_targets"] == 8
            and advantage["deletion"]["unfavorable_saliency_targets"] == 1
            and advantage["deletion"]["unscored_targets"] == 1,
            "unexpected deletion saliency-vs-random target counts")
    require(advantage["insertion"]["favorable_saliency_targets"] == 10
            and advantage["insertion"]["unfavorable_saliency_targets"] == 0
            and advantage["insertion"]["unscored_targets"] == 0,
            "unexpected insertion saliency-vs-random target counts")

    paired = {
        "saliency_deletion_auc_4x4_minus_8x8":
            paired_grid_delta(list(new_targets.values()), old_targets, "saliency", "deletion"),
        "saliency_insertion_auc_4x4_minus_8x8":
            paired_grid_delta(list(new_targets.values()), old_targets, "saliency", "insertion"),
        "random_deletion_auc_4x4_minus_8x8":
            paired_grid_delta(list(new_targets.values()), old_targets, "random", "deletion"),
        "random_insertion_auc_4x4_minus_8x8":
            paired_grid_delta(list(new_targets.values()), old_targets, "random", "insertion"),
    }
    sign_agreement = {
        direction: advantage_sign_agreement(list(new_targets.values()), old_targets, direction)
        for direction in ("deletion", "insertion")
    }
    require(sign_agreement["deletion"]["same_direction"] == 6
            and sign_agreement["deletion"]["changed_direction"] == 3
            and sign_agreement["deletion"]["not_comparable"] == 1,
            "unexpected deletion advantage sign agreement")
    require(sign_agreement["insertion"]["same_direction"] == 9
            and sign_agreement["insertion"]["changed_direction"] == 1,
            "unexpected insertion advantage sign agreement")

    shared = [row for row in new_targets.values() if set(row["arms"]) == {"A5", "A6"}]
    a5_unique = [row for row in new_targets.values() if row["arms"] == ["A5"]]
    a6_unique = [row for row in new_targets.values() if row["arms"] == ["A6"]]
    require(len(shared) == 6 and len(a5_unique) == 2 and len(a6_unique) == 2,
            "A5/A6 target overlap composition changed")
    shared_del = [metric(row, "saliency", "deletion") for row in shared]
    shared_del = [value for value in shared_del if value is not None]
    shared_ins = [metric(row, "saliency", "insertion") for row in shared]
    require(len(shared_del) == 5 and len(shared_ins) == 6,
            "shared-target AUC availability mismatch")
    shared_summary = {
        "shared_target_count": 6,
        "a5_unique_target_ids": [row["target_id"] for row in a5_unique],
        "a6_unique_target_ids": [row["target_id"] for row in a6_unique],
        "shared_saliency_deletion_auc": {"n": 5, "mean": float(mean(shared_del))},
        "shared_saliency_insertion_auc": {"n": 6, "mean": float(mean(shared_ins))},
        "policy_superiority_claim_supported": False,
    }

    return {
        "schema_version": "seer-ppe/v33b-grid4-independent-numeric-audit/v0.33b",
        "status": "PASSED",
        "model_id": MODEL_ID,
        "grid": {"rows": 4, "cols": 4},
        "source_population": {"images": 8, "train": 4, "valid": 4, "targets": 10},
        "call_accounting": {
            "maximum": EXPECTED_CALLS,
            "attempted": budget["actual_attempts"],
            "successful": budget["successful_calls"],
            "failed": 0,
            "phase_counts": dict(phases),
            "curve_contexts": len(curve_calls),
            "intermediate_calls_per_curve": 9,
            "ledger_indices_contiguous": True,
            "automatic_retries": False,
        },
        "map_status": {
            "rankable_4x4": 10,
            "same_categorical_status_as_8x8": map_status_matches,
            "warning": "Categorical rankability agreement is not a spatial saliency-map rank-correlation measure.",
        },
        "curves": curve_counts,
        "auc_recomputation": {
            "valid_auc_count": 39,
            "total_curve_count": 40,
            "max_absolute_error": auc_recompute_max_error,
            "ambiguous_points_not_imputed": ambiguity_records,
        },
        "saliency_vs_single_random": advantage,
        "paired_grid_resolution_deltas": paired,
        "saliency_advantage_sign_agreement_4x4_vs_8x8": sign_agreement,
        "A5_A6_overlap": shared_summary,
        "interpretation_boundary": (
            "Descriptive within-target resolution robustness on eight development-exposed images; "
            "not causal faithfulness, independent generalization, a randomized test, worker compliance, "
            "or evidence of A5/A6 policy superiority."
        ),
        "guardrails": {
            "no_test_accessed": True,
            "no_retraining": True,
            "original_images_annotations_splits_unchanged": True,
            "source_independence_verified": False,
            "worker_compliance_measured": False,
            "worker_safety_scoring_ready": False,
            "causal_faithfulness_proven": False,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--results", type=Path, default=RESULT_DEFAULT)
    parser.add_argument("--v30-results", type=Path, default=V30_DEFAULT)
    parser.add_argument("--manifest", type=Path, default=MANIFEST_DEFAULT)
    parser.add_argument("--output", type=Path, default=OUTPUT_DEFAULT)
    args = parser.parse_args()

    report = audit(load_json(args.results), load_json(args.v30_results),
                   load_json(args.manifest))
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": report["status"],
        "calls": report["call_accounting"],
        "map_status": report["map_status"],
        "curves": report["curves"],
        "saliency_vs_random": report["saliency_vs_single_random"],
        "paired_grid_resolution_deltas": report["paired_grid_resolution_deltas"],
        "saliency_advantage_sign_agreement_4x4_vs_8x8": report["saliency_advantage_sign_agreement_4x4_vs_8x8"],
        "output": str(args.output),
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
