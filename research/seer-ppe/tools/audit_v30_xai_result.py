#!/usr/bin/env python3
"""Read-only audit of V30 actual progressive XAI numeric evidence.

No model inference, no Roboflow credentials, no image downloads, no Test access.
This is an independent *numeric integrity* audit, not a claim of independent
image provenance, worker-level compliance, or causal safety efficacy.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
DIRECTIONS = ("deletion", "insertion")
ORDERS = ("saliency", "random", "inverse_saliency")
ARMS = ("A5", "A6")
SOURCE_COUNTS = {"train": 4, "valid": 4}


class AuditError(ValueError):
    pass


def fail(message):
    raise AuditError(message)


def numeric(value, label, *, low=None, high=None):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        fail(f"{label} must be a finite numeric value")
    x = float(value)
    if low is not None and x < low - 1e-8:
        fail(f"{label} is below {low}")
    if high is not None and x > high + 1e-8:
        fail(f"{label} exceeds {high}")
    return x


def check_auc_points(points, recorded, reference, blurred, direction, label):
    if len(points) != 11:
        fail(f"{label}: expected eleven 0..100% points")
    if any(p.get("direction") != direction for p in points):
        fail(f"{label}: direction does not match")
    xs = []
    ys = []
    incomplete = False
    for i, p in enumerate(points):
        requested = numeric(p.get("requested_fraction"), f"{label} requested[{i}]", low=0, high=1)
        if not math.isclose(requested, i / 10, abs_tol=1e-9):
            fail(f"{label}: altered curve step order")
        x = numeric(p.get("modified_fraction"), f"{label} area[{i}]", low=0, high=1)
        if xs and x <= xs[-1]:
            fail(f"{label}: nonincreasing pixel-area fractions")
        xs.append(x)
        score = p.get("target_confidence")
        norm = p.get("normalized_score")
        if score is None or norm is None:
            if score is not None or norm is not None or p.get("match_status") != "AMBIGUOUS":
                fail(f"{label}: missing score must be explicitly AMBIGUOUS")
            incomplete = True
            ys.append(None)
        else:
            s = numeric(score, f"{label} score[{i}]", low=0, high=1)
            n = numeric(norm, f"{label} normalized[{i}]", low=0, high=1)
            if not math.isclose(n, min(1.0, max(0.0, s / reference)), abs_tol=1e-7):
                fail(f"{label}: normalized score differs from raw score")
            ys.append(n)
    if not math.isclose(xs[0], 0.0, abs_tol=1e-9) or not math.isclose(xs[-1], 1, abs_tol=1e-9):
        fail(f"{label}: invalid endpoints")
    expected0 = reference if direction == "deletion" else blurred
    expected1 = blurred if direction == "deletion" else reference
    for idx, expected in ((0, expected0), (-1, expected1)):
        if points[idx].get("target_confidence") is None or not math.isclose(
                float(points[idx]["target_confidence"]), expected, abs_tol=1e-7):
            fail(f"{label}: the fixed endpoint is not reused")
    if incomplete:
        if recorded is not None:
            fail(f"{label}: AUC is reported despite ambiguous point")
        return None
    calc = sum((ys[i] + ys[i + 1]) * (xs[i + 1] - xs[i]) / 2
               for i in range(10))
    if recorded is None or not math.isclose(
            numeric(recorded, f"{label} AUC", low=0, high=1),
            calc, abs_tol=1e-8):
        fail(f"{label}: AUC differs from independently recomputed trapezoids")
    return calc


def audit_results(manifest, result):
    if result.get("schema_version") != "seer-ppe/v30-actual-progressive-xai-results/v0.30":
        fail("Unrecognized actual-results schema")
    if result.get("status") != "COMPLETED":
        fail("Run does not declare COMPLETED; not eligible for a result claim")
    if manifest.get("model_id") != result.get("model_id") != "altayyar-0oflt-lafos-qqauz/2":
        fail("Model ID mismatch")
    if result.get("inference_settings") != {"confidence": 0.2, "overlap": 0.5}:
        fail("Frozen inference settings changed")
    refs = {t["target_id"]: t for t in manifest.get("targets", [])}
    images = {x["image_key"]: x for x in manifest.get("source_images", [])}
    rows = result.get("target_results", [])
    if len(refs) != 10 or len(images) != 8 or len(rows) != 10:
        fail("Frozen images/targets or actual result count mismatch")
    if set(x.get("target_id") for x in rows) != set(refs):
        fail("Result target IDs are not exactly the ten frozen IDs")
    if len(set(x.get("target_id") for x in rows)) != 10:
        fail("Duplicated actual target ID")
    if len(result.get("baseline_images", {})) != 8:
        fail("Must preserve all eight original-image baseline sources")
    for key, source in images.items():
        b = result["baseline_images"].get(key)
        if not b or any(b.get(k) != source.get(s) for k, s in
                        (("asset_id", "asset_id"), ("split", "split"),
                         ("filename", "filename"))):
            fail(f"Baseline source mismatch for {key}")
        h = b.get("local_file_sha256", "")
        if len(h) != 64 or any(c not in "0123456789abcdef" for c in h):
            fail(f"No complete SHA-256 for source {key}")
    count_split = {k: sum(x.get("split") == k for x in images.values()) for k in SOURCE_COUNTS}
    if count_split != SOURCE_COUNTS:
        fail("Frozen source split is not 4 Train + 4 Valid")
    constraints = result.get("constraints", {})
    for k in ("no_test_accessed", "claims_are_descriptive_only"):
        if constraints.get(k) is not True:
            fail(f"Missing strict constraint {k}")
    for k in ("source_independence_verified", "worker_compliance_measured", "human_review_dispatched",
              "worker_safety_scoring_ready", "original_model_or_data_modified"):
        if constraints.get(k) is not False:
            fail(f"Unsafe scientific flag {k}")
    eligible = 0
    blocked = []
    auc_by_target = {}
    for t in rows:
        target = refs[t["target_id"]]
        tid = t["target_id"]
        for k, ref_k in (("image_key", "image_key"), ("filename", "filename"),
                         ("asset_id", "asset_id"), ("split", "split"),
                         ("target_class", "target_class"), ("arms", "arms")):
            if t.get(k) != target[ref_k]:
                fail(f"Frozen target property changed: {tid}/{k}")
        reference = numeric(t.get("baseline_confidence"), f"{tid} baseline", low=1e-12, high=1)
        if not math.isclose(reference, float(target["frozen_baseline_confidence"]), abs_tol=1e-9):
            fail(f"Baseline confidence differs from frozen record: {tid}")
        grid = t.get("importance_map", [])
        trials = t.get("occlusion_trials", [])
        if len(grid) != 8 or any(len(row) != 8 for row in grid) or len(trials) != 64:
            fail(f"Grid or 64 occlusion trials missing: {tid}")
        coords = set()
        finite_drops = []
        ambiguous = False
        for cell in trials:
            pos = (cell.get("row"), cell.get("col"))
            if (not all(isinstance(z, int) and not isinstance(z, bool) and 0 <= z < 8 for z in pos)
                    or pos in coords):
                fail(f"Duplicated or invalid grid coordinates: {tid}")
            coords.add(pos)
            drop = cell.get("score_drop")
            if drop is None:
                ambiguous = True
                if cell.get("status") != "AMBIGUOUS":
                    fail(f"Missing grid score without ambiguous status: {tid}")
                if grid[pos[0]][pos[1]] is not None:
                    fail(f"Ambiguous grid cell must have an explicit missing score: {tid}")
                continue
            drop = numeric(drop, f"{tid} cell confidence-drop", low=-1, high=1)
            after = numeric(cell.get("score_after"), f"{tid} occlusion score", low=0, high=1)
            if not math.isclose(reference - after, drop, abs_tol=1e-7):
                fail(f"Grid score drop not reproducible: {tid}")
            actual = numeric(grid[pos[0]][pos[1]], f"{tid} grid map value", low=-1, high=1)
            if not math.isclose(actual, drop, abs_tol=1e-7):
                fail(f"Grid importance not equal to recorded trial: {tid}")
            finite_drops.append(drop)
        map_status = t.get("map_status")
        if ambiguous:
            if map_status != "AMBIGUOUS_CELL":
                fail(f"Ambiguous grid must block ranking: {tid}")
        elif not any(d > 0 for d in finite_drops):
            if map_status != "NO_POSITIVE_DROP":
                fail(f"No-positive-drop map status incorrect: {tid}")
        elif map_status != "RANKABLE":
            fail(f"Eligible positive map not ranked: {tid}")
        blurred_entry = t.get("blurred_endpoint", {})
        blurred = blurred_entry.get("score")
        if blurred is not None:
            blurred = numeric(blurred, f"{tid} blur score", low=0, high=1)
        skip = map_status != "RANKABLE" or blurred is None
        curves = t.get("curves", {})
        auc_by_target[tid] = {}
        for ordering in ORDERS:
            for direction in DIRECTIONS:
                label = f"{tid} {ordering}/{direction}"
                curve = curves.get(ordering, {}).get(direction)
                if not isinstance(curve, dict):
                    fail(f"Missing curve record {label}")
                if skip:
                    if curve.get("auc") is not None or curve.get("points") != [] or not str(curve.get("status", "")).startswith("NOT_RUN_"):
                        fail(f"Blocked target was scored: {label}")
                    auc_by_target[tid][(ordering, direction)] = None
                    continue
                pts = curve.get("points", [])
                val = check_auc_points(pts, curve.get("auc"), reference, blurred, direction, label)
                auc_by_target[tid][(ordering, direction)] = val
        if skip:
            blocked.append({"target_id": tid, "reason": t.get("curve_status")})
        else:
            eligible += 1
    if eligible != result.get("curve_eligible_targets"):
        fail("Eligible target count mismatch")
    expected_extra = 8 + 8 * 64 + eligible * 54
    if (result.get("baseline_preflight_model_calls_already_executed") != 8
            or result.get("model_inference_calls_this_run") != expected_extra
            or result.get("total_v30_model_inference_calls") != expected_extra + 8
            or expected_extra > 1060):
        fail("Actual model-call ledger does not match frozen 1,068-call budget")
    arms_report = {}
    for arm in ARMS:
        selected = [t for t in rows if arm in t["arms"]]
        if len(selected) != 8:
            fail(f"Expected eight {arm} slots")
        stat = result.get("A5_A6_summary", {}).get(arm, {})
        if stat.get("selected_slots") != 8 or stat.get("shared_target_slots") != 6 or stat.get("unique_target_slots") != 2:
            fail(f"Arm slot structure invalid: {arm}")
        arm_detail = {"selected_target_slots": 8, "shared_target_slots": 6,
                      "unique_target_slots": 2, "valid_auc_counts": {},
                      "mean_auc_by_ordering": {}}
        for order in ORDERS:
            for direction in DIRECTIONS:
                values = [auc_by_target[t["target_id"]][(order, direction)] for t in selected]
                values = [v for v in values if v is not None]
                order_field = "inverse" if order == "inverse_saliency" else order
                name = f"{order_field}_{direction}_auc_mean"
                result_mean = stat.get(name)
                mean = sum(values) / len(values) if values else None
                if (mean is None) != (result_mean is None):
                    fail(f"Incorrect arm-mean nullability: {arm}/{name}")
                if mean is not None and not math.isclose(
                        numeric(result_mean, f"{arm}/{name}", low=0, high=1),
                        mean, abs_tol=1e-8):
                    fail(f"Arm mean does not match constituent targets: {arm}/{name}")
                arm_detail["valid_auc_counts"][order+"_"+direction] = len(values)
                arm_detail["mean_auc_by_ordering"][order+"_"+direction] = mean
        arms_report[arm] = arm_detail
    unique_a5 = [t["target_id"] for t in rows if t["arms"] == ["A5"]]
    unique_a6 = [t["target_id"] for t in rows if t["arms"] == ["A6"]]
    shared = [t["target_id"] for t in rows if set(t["arms"]) == {"A5", "A6"}]
    if len(unique_a5) != 2 or len(unique_a6) != 2 or len(shared) != 6:
        fail("Shared versus arm-unique target composition is invalid")
    return {
        "audit_schema": "seer-ppe/v30-independent-numeric-audit/v1",
        "audit_status": "PASS_NUMERIC_INTEGRITY_ONLY",
        "unique_targets": 10,
        "frozen_source_images": 8,
        "train_images": 4,
        "valid_images": 4,
        "test_images": 0,
        "rankable_curve_targets": eligible,
        "blocked_curve_targets": blocked,
        "additional_actual_model_calls": expected_extra,
        "v30_total_model_calls": expected_extra + 8,
        "a5_a6": arms_report,
        "shared_target_ids": shared,
        "a5_unique_target_ids": unique_a5,
        "a6_unique_target_ids": unique_a6,
        "claim_boundary": (
            "Development-exposed descriptive frozen-target occlusion experiment only. "
            "A5 and A6 share six of eight selected targets and are not independent groups. "
            "No source-independent generalization, person-level compliance, energy, or "
            "real-world safety efficacy conclusion follows."
        ),
    }


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--results", type=Path, required=True)
    p.add_argument("--manifest", type=Path,
                   default=HERE / "V30_FROZEN_TARGETS_2026-11-22.json")
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    try:
        manifest = json.loads(args.manifest.read_text(encoding="utf-8"),
                              parse_constant=lambda x: fail(f"Non-standard numeric constant {x}"))
        # The ongoing V30 runner may emit literal NaN for a deliberately
        # AMBIGUOUS map cell. Preserve it as a missing/null value; do not
        # impute a confidence or calculate AUC for that cell.
        encoding_notes = []
        def parse_legacy_nonfinite(token):
            if token != "NaN":
                fail(f"Non-standard numeric constant {token}")
            encoding_notes.append("Legacy NaN normalized to null; rankability/AUC still fail closed")
            return None
        result = json.loads(args.results.read_text(encoding="utf-8"),
                            parse_constant=parse_legacy_nonfinite)
        report = audit_results(manifest, result)
        report["legacy_nonstandard_nan_cells_normalized"] = len(encoding_notes)
        report["encoding_warning"] = (encoding_notes[0] if encoding_notes else None)
    except (OSError, ValueError, TypeError, KeyError) as exc:
        raise SystemExit(f"V30 numeric audit FAILED (no model calls made): {exc}") from exc
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2,
                                      allow_nan=False) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
