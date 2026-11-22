#!/usr/bin/env python3
"""V38-A exploratory leave-one-image-out sensitivity; saved V34A input only.
Run: python tools/v38_offline_image_cluster_sensitivity.py
No network, model inference, image reading, image modifications or dependency packages.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "research" / "seer-ppe"
SOURCE = ROOT / "V34A_SPATIAL_MAP_ALIGNMENT_RANK_CORRELATION_2026-11-22.json"
METRICS = {
    "spearman_rho": "spearman_rho_signed_area_normalized",
    "kendall_tau_b": "kendall_tau_b_signed_area_normalized",
    "top_four_fraction": "top4_signed_region_overlap_fraction",
}


def average(values):
    return sum(values) / len(values)


def analyze(path=SOURCE):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    pts = list(data["per_target"].values())
    group_ids = sorted({item["image_key"] for item in pts})
    assert len(pts) == 10 and len(group_ids) == 8, (len(pts), len(group_ids))
    assert data["status"] == "PASSED"
    results = {
        "schema_version": "seer-ppe/v38a-offline-image-cluster-sensitivity/v1",
        "input_file": Path(path).name,
        "method": "exact leave-one-original-image-out over 8 distinct image_keys; descriptive only",
        "n_targets": len(pts),
        "n_unique_images": len(group_ids),
        "metrics": {},
    }
    for label, field in METRICS.items():
        mean_target = average([float(p[field]) for p in pts])
        mean_image = average([
            average([float(p[field]) for p in pts if p["image_key"] == image_id])
            for image_id in group_ids
        ])
        loo = []
        for image_id in group_ids:
            kept = [p for p in pts if p["image_key"] != image_id]
            assert len(kept) in (8, 9)
            loo.append({
                "left_out_image": image_id,
                "remaining_targets": len(kept),
                "mean": average([float(p[field]) for p in kept]),
            })
        results["metrics"][label] = {
            "target_weighted_full_mean": mean_target,
            "image_equal_weight_mean": mean_image,
            "leave_one_image_out_min": min(row["mean"] for row in loo),
            "leave_one_image_out_max": max(row["mean"] for row in loo),
            "leave_one_image_out": loo,
        }
    assert abs(results["metrics"]["spearman_rho"]["target_weighted_full_mean"] - 0.541565901847459) < 1e-12
    assert abs(results["metrics"]["kendall_tau_b"]["target_weighted_full_mean"] - 0.4238764616398565) < 1e-12
    assert abs(results["metrics"]["top_four_fraction"]["target_weighted_full_mean"] - 0.65) < 1e-12
    return results


if __name__ == "__main__":
    print(json.dumps(analyze(), ensure_ascii=False, indent=2))
