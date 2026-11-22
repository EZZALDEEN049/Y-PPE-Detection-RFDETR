#!/usr/bin/env python3
"""V38-B read-only identity and executable-protocol preflight.

No model inference, API credentials, training, Test, model SDK, image uploads,
or saving image pixels outside ephemeral memory. Full-image SHA-256 computed
on current Roboflow original bytes; the V26 archive did NOT save source bytes
hashes, so this is a *new source fingerprint*, NOT a historical SHA match.
"""
from __future__ import annotations
import argparse
from collections import Counter
import hashlib
import io
import json
import math
from pathlib import Path
from urllib.parse import urlsplit
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "V38_B_FROZEN_CANDIDATE_SAMPLE_2026-11-23.json"
V13 = ROOT / "ORIGINAL_CLEAN17_VALID_IMAGE_CONTENT_V13.json"
V30_PREFLIGHT = ROOT / "V30_BASELINE_PREFLIGHT_ACTUAL_2026-11-22.json"
V30_TARGETS = ROOT / "V30_FROZEN_TARGETS_2026-11-22.json"
MAX_IMAGE_BYTES = 40 * 1024 * 1024
MAX_ATTEMPTED = 6000
EXPECTED_INTENDED = 5200
MODEL = "altayyar-0oflt-lafos-qqauz/2"


def read(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf8"))


def bbox_iou(a: dict, b: dict) -> float:
    def edges(box):
        return (float(box["x"]) - float(box["width"]) / 2,
                float(box["y"]) - float(box["height"]) / 2,
                float(box["x"]) + float(box["width"]) / 2,
                float(box["y"]) + float(box["height"]) / 2)
    ax1, ay1, ax2, ay2 = edges(a)
    bx1, by1, bx2, by2 = edges(b)
    intersection = max(0., min(ax2, bx2) - max(ax1, bx1)) * max(0., min(ay2, by2) - max(ay1, by1))
    union = (ax2 - ax1) * (ay2 - ay1) + (bx2 - bx1) * (by2 - by1) - intersection
    return intersection / union if union > 0 else 0.


def cells(height: int, width: int, n: int):
    out = []
    for row in range(n):
        for col in range(n):
            a, b = (row * height) // n, ((row + 1) * height) // n
            c, d = (col * width) // n, ((col + 1) * width) // n
            assert a < b and c < d
            out.append((a, b, c, d))
    assert sum((b - a) * (d - c) for a, b, c, d in out) == height * width
    return out


def assert_grid_alignment(height: int, width: int):
    fine, coarse = cells(height, width, 8), cells(height, width, 4)
    for coarse_row in range(4):
        for coarse_col in range(4):
            cr = coarse_row * 4 + coarse_col
            c = coarse[cr]
            f = [fine[(coarse_row * 2 + dr) * 8 + coarse_col * 2 + dc]
                 for dr in (0, 1) for dc in (0, 1)]
            assert min(x[0] for x in f) == c[0] and max(x[1] for x in f) == c[1]
            assert min(x[2] for x in f) == c[2] and max(x[3] for x in f) == c[3]
            assert sum((b - a) * (d - cc) for a, b, cc, d in f) == (c[1] - c[0]) * (c[3] - c[2])
    return {"cells_8x8": len(fine), "cells_4x4": len(coarse),
            "pixel_area_partition_pass": True, "coarse_to_fine_exact_partition_pass": True}


class AttemptCap:
    """Executable offline budget guard prototype; NOT a hosted inference runner."""
    def __init__(self, max_attempted=MAX_ATTEMPTED):
        self.max_attempted = max_attempted
        self.attempted = 0

    def reserve(self):
        if self.attempted >= self.max_attempted:
            raise RuntimeError("V38B hard-stop: attempted call count would exceed cap")
        self.attempted += 1  # reserve before remote request, including failures
        return self.attempted


def random_orders(target_id: str):
    import random
    orders = []
    for index in range(10):
        # SHA256-based explicit independent seed for each frozen target and comparison index.
        digest = hashlib.sha256(
            ("V38B-8x8-random|" + target_id + "|" + str(index)).encode()
        ).digest()
        ordering = list(range(64))
        random.Random(int.from_bytes(digest, "big")).shuffle(ordering)
        orders.append(tuple(ordering))
    assert len(orders) == len(set(orders)) == 10
    assert all(sorted(o) == list(range(64)) for o in orders)
    return orders


def static_preflight():
    m = read(MANIFEST)
    assert m["schema_version"] == "seer-ppe/v38b-prospective-candidate-freeze/v1"
    assert m["status"] == "FROZEN_CANDIDATES_AND_BUDGET_ONLY_NO_NEW_MODEL_CALLS"
    assert m["model"]["id"] == MODEL
    assert m["model"]["confidence"] == .20 and m["model"]["overlap"] == .50
    assert m["budget"]["hard_maximum_new_hosted_model_calls_including_retries"] == MAX_ATTEMPTED
    assert m["budget"]["actual_new_model_calls_in_this_freeze"] == 0
    assert m["release_gate"].startswith("HOLD_NEW_INFERENCE_")
    assert m["selection_guards"]["protected_test"] == "NOT_ACCESSED"
    images, targets = m["images"], m["targets"]
    assert len(images) == 24 and len(targets) == 48
    assert all(x["image_key"] == "valid:" + x["source_id"] for x in images)
    ids = [x["source_id"] for x in images]
    assert len(ids) == len(set(ids)) == 24
    target_ids = [x["target_id"] for x in targets]
    assert len(target_ids) == len(set(target_ids)) == 48
    assert len({x["class_name"] for x in targets}) == 11
    assert all(4 <= n <= 5 for n in Counter(x["class_name"] for x in targets).values())
    per_image = {x["source_id"]: [] for x in images}
    for t in targets:
        per_image[t["source_id"]].append(t)
    assert all(len(t) == 2 and t[0]["class_name"] != t[1]["class_name"] for t in per_image.values())
    assert len(m["random_progressive_target_ids_12_different_images"]) == 12
    assert len(m["alternative_fill_image_ids_8"]) == 8
    assert all(t["target_id"] in target_ids for t in targets)
    a = m["budget"]["calls_by_phase_max"]
    assert a["primary_single_cell_maps_24_images_x_64_plus_16"] == 1920
    assert a["new_original_and_full_blur_baselines_24_x_2"] == 48
    assert a["seeded_random_8x8_progressive_12_targets_x_11_orders_x_2_dirs_x_9_points"] == 2376
    assert a["saliency_4x4_progressive_12_targets_x_2_dirs_x_9_points"] == 216
    assert a["alternative_fill_maps_8_images_x_64_plus_16"] == 640
    assert sum(a.values()) == EXPECTED_INTENDED
    assert m["budget"]["technical_retry_reserve_only"] == 800

    # Test the actual guard prototype with ALL intended calls and the full reserve.
    guard = AttemptCap()
    for _ in range(EXPECTED_INTENDED):
        guard.reserve()
    for _ in range(MAX_ATTEMPTED - EXPECTED_INTENDED):
        guard.reserve()
    assert guard.attempted == MAX_ATTEMPTED
    try:
        guard.reserve()
    except RuntimeError:
        pass
    else:
        raise AssertionError("Budget guard failed to stop the 6,001st attempt")

    v13 = read(V13)
    v13_by_id = {row["source_id"]: row for row in v13["results"]}
    assert v13["source_and_export_sha_verified"] == 459
    v30 = read(V30_TARGETS)
    old_ids = {x["source_id"] for x in v30["source_images"] if x.get("source_id")}
    assert not set(ids).intersection(old_ids)

    by_id = {}
    historic_n = 0
    for shard_number in range(12):
        shard = read(ROOT / f"V26_ORIGINAL_VALID_GEOMETRY_SHARD_{shard_number:02d}_OF_12.json")
        assert shard["shard_index"] == shard_number and shard["original_model_id"] == MODEL
        assert shard["hosted_confidence_floor"] == .20 and shard["hosted_overlap_threshold"] == .50
        historic_n += len(shard["rows"])
        for row in shard["rows"]:
            if row["source_id"] in ids:
                assert row["source_id"] not in by_id
                by_id[row["source_id"]] = row
    assert historic_n == 459 and len(by_id) == 24

    geom_checks = []
    random_order_digests = []
    for item in images:
        sid = item["source_id"]
        row = by_id[sid]
        assert row["status"] == "SCORED_INPUT_ACQUIRED"
        assert not row["previously_reused_in_v23_pilot"]
        assert (row["image_width"], row["image_height"]) == (item["width"], item["height"])
        record = v13_by_id[sid]
        assert record["original_sha_verified"] and record["export_sha_verified"]
        assert record["original_dimensions"] == [item["width"], item["height"]]
        grid = assert_grid_alignment(item["height"], item["width"])
        geom_checks.append(grid)
        predictions = {x["id"]: x for x in row["model_predictions"]}
        for target in per_image[sid]:
            p = predictions[target["target_id"]]
            assert p["cls"] == target["class_name"]
            assert abs(float(p["confidence"]) - target["baseline_confidence_from_v26"]) <= 1e-12
            assert target["baseline_confidence_from_v26"] >= .55
            box = target["bbox_xywh"]
            for dim in ("x", "y", "width", "height"):
                assert math.isfinite(box[dim])
                assert abs(float(p[dim]) - float(box[dim])) <= 1e-12
            assert box["width"] >= 16 and box["height"] >= 16
            assert box["width"] * box["height"] >= .0003 * item["width"] * item["height"]
            best = max([0.] + [bbox_iou(gt, box) for gt in row["current_author_boxes"] if gt["cls"] == target["class_name"]])
            assert best >= .5
            assert abs(best - target["baseline_author_reference_iou"]) < 1e-12
    for target_id in m["random_progressive_target_ids_12_different_images"]:
        orders = random_orders(target_id)
        random_order_digests.append({
            "target_id": target_id,
            "ten_orders_digest_sha256": hashlib.sha256(str(orders).encode()).hexdigest(),
        })
    return {
        "status": "PASS_OFFLINE_PROTOCOL_AND_V26_V13_IDENTITY_CHAIN",
        "all_459_v26_rows_rechecked": historic_n,
        "chosen_images": len(images),
        "chosen_targets": len(targets),
        "v13_prior_original_and_export_sha_verification_flags_matched": 24,
        "v26_historical_box_class_confidence_matches": 48,
        "geometry_checks_passed": len(geom_checks),
        "distinct_sha256_random_orders_per_selected_target": 10,
        "random_curve_target_count": len(random_order_digests),
        "random_order_plan_digests": random_order_digests,
        "actual_hosted_model_calls": 0,
        "technical_retry_reserve": 800,
        "intended_calls": EXPECTED_INTENDED,
        "hard_attempted_call_max": MAX_ATTEMPTED,
        "budget_cap_rejects_attempt_6001": True,
        "runner_integration_verified": False,
        "note": "Static preflight proves archived IDs/geometry and simulated cap only; no new model runtime authorization. V13 SHA verification flags do NOT expose old digest values.",
    }


def get_allowed_source_namespace():
    old = read(V30_PREFLIGHT)
    assert old["status"] == "PASSED"
    paths = set()
    for item in old["source_images"]:
        u = urlsplit(item["source_url"])
        assert u.scheme == "https" and u.hostname == "source.roboflow.com"
        assert not (u.username or u.password or u.query or u.fragment)
        parts = u.path.strip("/").split("/")
        assert len(parts) == 3 and parts[1] == item["asset_id"] and parts[2] == "original.jpg"
        paths.add(parts[0])
    assert len(paths) == 1
    return next(iter(paths))


def download_one(namespace: str, record: dict) -> dict:
    from PIL import Image, ImageOps, UnidentifiedImageError
    import warnings
    Image.MAX_IMAGE_PIXELS = 30_000_000
    sid = record["source_id"]
    assert all(c.isalnum() for c in sid) and 10 <= len(sid) <= 40
    url = f"https://source.roboflow.com/{namespace}/{sid}/original.jpg"
    p = urlsplit(url)
    assert p.scheme == "https" and p.hostname == "source.roboflow.com"
    request = Request(url, headers={"User-Agent": "SEER-PPE-V38B-No-Inference-Identity-Preflight/1.0"})
    with urlopen(request, timeout=60) as response:
        effective = urlsplit(response.geturl())
        if effective.scheme != "https" or effective.hostname != "source.roboflow.com":
            raise RuntimeError("Unapproved redirected download origin")
        if getattr(response, "status", 200) != 200:
            raise RuntimeError("Unexpected HTTP status for original media")
        length = response.headers.get("Content-Length")
        if length and int(length) > MAX_IMAGE_BYTES:
            raise RuntimeError("Original media exceeds byte cap")
        raw = response.read(MAX_IMAGE_BYTES + 1)
    if len(raw) < 128 or len(raw) > MAX_IMAGE_BYTES:
        raise RuntimeError("Downloaded original missing or oversized")
    with warnings.catch_warnings():
        warnings.simplefilter("error", Image.DecompressionBombWarning)
        with Image.open(io.BytesIO(raw)) as img:
            img.verify()
        with Image.open(io.BytesIO(raw)) as img:
            observed_size = img.size
            exif_orientation = img.getexif().get(274)
            corrected = ImageOps.exif_transpose(img)
            corrected_size = corrected.size
            # Only decode in memory; no image pixels are sent to model or saved.
            rgb_sha = hashlib.sha256(img.convert("RGB").tobytes()).hexdigest()
            corrected_rgb_sha = hashlib.sha256(corrected.convert("RGB").tobytes()).hexdigest()
    exact = observed_size == (record["width"], record["height"])
    orientation_matches = corrected_size == (record["width"], record["height"])
    return {
        "source_id": sid,
        "archived_v26_width": record["width"], "archived_v26_height": record["height"],
        "current_raw_width": observed_size[0], "current_raw_height": observed_size[1],
        "current_exif_corrected_width": corrected_size[0],
        "current_exif_corrected_height": corrected_size[1],
        "exif_orientation_tag": exif_orientation,
        "download_size_bytes": len(raw),
        "new_current_source_raw_sha256": hashlib.sha256(raw).hexdigest(),
        "new_current_decoded_rgb_sha256": rgb_sha,
        "new_current_exif_corrected_rgb_sha256": corrected_rgb_sha,
        "matches_v26_dimensions": exact,
        "matches_v26_dimensions_after_exif": orientation_matches,
        "same_sha_as_original_v26_download": None,  # V26 didn't archive raw SHA
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["static", "source-readonly"], required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    audit = static_preflight()
    if args.mode == "source-readonly":
        namespace = get_allowed_source_namespace()
        from PIL import Image
        image_rows = []
        for record in read(MANIFEST)["images"]:
            image_rows.append(download_one(namespace, record))
        assert len(image_rows) == 24
        different_sha_count = len({x["new_current_source_raw_sha256"] for x in image_rows})
        mismatch_rows = [x for x in image_rows if not x["matches_v26_dimensions"]]
        audit.update({
            "status": ("PASS_24_CURRENT_SOURCE_IMAGE_BYTES_AND_STATIC_PROTOCOL"
                       if not mismatch_rows and different_sha_count == 24
                       else "HOLD_CURRENT_SOURCE_IMAGE_IDENTITY_MISMATCH"),
            "current_source_images_retrieved_readonly": 24,
            "current_source_images_exact_dimension_matches": 24 - len(mismatch_rows),
            "current_source_images_exif_corrected_matches": sum(x["matches_v26_dimensions_after_exif"] for x in image_rows),
            "current_source_images_distinct_raw_sha256": different_sha_count,
            "current_source_mismatch_image_ids": [x["source_id"] for x in mismatch_rows],
            "current_source_image_sha256": image_rows,
            "historical_v26_raw_sha256_available": False,
            "historical_v26_raw_sha256_matched": None,
            "raw_images_saved_or_uploaded": False,
            "roboflow_images_modified": False,
            "actual_hosted_model_calls": 0,
        })
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf8")
    print(json.dumps({k: v for k, v in audit.items() if k not in ("current_source_image_sha256", "random_order_plan_digests")}, indent=2))


if __name__ == "__main__":
    main()
