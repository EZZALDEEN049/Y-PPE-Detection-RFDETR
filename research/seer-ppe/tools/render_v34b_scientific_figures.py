#!/usr/bin/env python3
"""Render reproducible V34-B scientific heatmaps from the archived V34-A data.

Offline-only: reads the frozen V34-A JSON and writes figures, CSV, JSON manifest
and a multi-page PDF. It does not call a detector or mutate source data.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
import math
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.colors import TwoSlopeNorm
from matplotlib.patches import Rectangle

from tools.analyze_v34a_spatial_map_alignment import kendall_tau_b, spearman, top_k_indices

ROOT = Path(__file__).resolve().parents[1]
SOURCE_DEFAULT = ROOT / "V34A_SPATIAL_MAP_ALIGNMENT_RANK_CORRELATION_2026-11-22.json"
OUTPUT_DEFAULT = ROOT / "figures" / "V34B_2026-11-22"
SOURCE_GIT_BLOB_SHA = "0b1ce69853b275baafe9e0abc1474a29dbd84b69"
SCALE_PERCENTILE = 97.5
GOLD = "#D99A00"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def build_target_arrays(map_record: dict) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Reconstruct native 8x8 child densities and direct/pooled 4x4 maps."""
    fine = np.full((8, 8), np.nan, dtype=float)
    seen: set[tuple[int, int]] = set()
    cells = map_record["aligned_cells"]
    require(len(cells) == 16, "each target must contain 16 aligned coarse cells")
    for coarse in cells:
        children = coarse["fine_children"]
        require(len(children) == 4, "each 4x4 region must have four 8x8 children")
        for child in children:
            row, col = int(child["row_8x8"]), int(child["col_8x8"])
            require(0 <= row < 8 and 0 <= col < 8, "fine cell index outside 8x8 grid")
            require((row, col) not in seen, "duplicate 8x8 child cell")
            area = float(child["area_fraction"])
            require(area > 0, "fine cell area must be positive")
            fine[row, col] = float(child["score_drop"]) / area
            seen.add((row, col))
    require(len(seen) == 64 and np.isfinite(fine).all(), "8x8 map must contain 64 finite cells")
    direct = np.asarray(map_record["direct_4x4_signed_drop_per_area_row_major"], dtype=float).reshape(4, 4)
    pooled = np.asarray(map_record["pooled_8x8_signed_drop_per_area_row_major"], dtype=float).reshape(4, 4)
    require(np.isfinite(direct).all() and np.isfinite(pooled).all(), "4x4 maps must be finite")
    return fine, direct, pooled


def ordered_targets(metadata: dict[str, dict]) -> list[str]:
    order = [
        ("train:A", "No Face Mask"), ("train:B", "Gloves"),
        ("train:C", "No Safety Boots"), ("train:C", "Face Masks"),
        ("train:D", "Hard Hat"), ("valid:07BnOpgFJyNaOhuzvh5i", "No Gloves"),
        ("valid:09WO3iVNf9jOt21QAxmb", "Safety Boots"),
        ("valid:0ABzMrjnd6I0Ws6FH7qo", "No Face Mask"),
        ("valid:0ABzMrjnd6I0Ws6FH7qo", "Safety Vests"),
        ("valid:0aGYjxE5LmocXyvuLHs8", "No Safety Boots"),
    ]
    ids = []
    for image_key, target_class in order:
        matches = [tid for tid, item in metadata.items()
                   if item["image_key"] == image_key and item["target_class"] == target_class]
        require(len(matches) == 1, f"expected one target for {image_key} / {target_class}")
        ids.append(matches[0])
    return ids


def display_label(image_key: str) -> str:
    return "Train " + image_key.split(":", 1)[1] if image_key.startswith("train:") else "Valid " + image_key.split(":", 1)[1]


def safe_slug(value: str) -> str:
    return "".join(ch.lower() if ch.isalnum() else "_" for ch in value).strip("_")


def validate_and_prepare(data: dict) -> list[dict]:
    require(data.get("status") == "PASSED", "V34-A archive is not marked PASSED")
    require(data.get("execution_mode") == "offline_only_no_model_inference",
            "V34-A archive is not the expected offline analysis")
    summaries = {x["target_id"]: x for x in data["per_target"]}
    maps = {x["target_id"]: x for x in data["per_target_aligned_maps"]}
    require(len(summaries) == 10 and len(maps) == 10, "expected ten unique target summaries and maps")
    require(set(summaries) == set(maps), "target IDs differ between summaries and aligned maps")
    prepared = []
    for target_id in ordered_targets(summaries):
        meta, record = summaries[target_id], maps[target_id]
        fine, direct, pooled = build_target_arrays(record)
        direct_flat, pooled_flat = direct.ravel().tolist(), pooled.ravel().tolist()
        top_direct, top_pooled = top_k_indices(direct_flat, 4), top_k_indices(pooled_flat, 4)
        require(top_direct == record["top4_direct_4x4_row_major_indices"],
                f"{target_id}: direct top-4 differs from archive")
        require(top_pooled == record["top4_pooled_8x8_row_major_indices"],
                f"{target_id}: pooled top-4 differs from archive")
        rho, tau = spearman(direct_flat, pooled_flat), kendall_tau_b(direct_flat, pooled_flat)
        require(rho is not None and math.isclose(rho, meta["spearman_rho_signed_area_normalized"], abs_tol=1e-10),
                f"{target_id}: Spearman does not reproduce V34-A")
        require(tau is not None and math.isclose(tau, meta["kendall_tau_b_signed_area_normalized"], abs_tol=1e-10),
                f"{target_id}: Kendall tau-b does not reproduce V34-A")
        overlap = len(set(top_direct) & set(top_pooled))
        require(overlap == meta["top4_signed_region_overlap_count"],
                f"{target_id}: top-4 overlap does not reproduce V34-A")
        require(np.allclose(pooled, np.asarray(record["pooled_8x8_signed_drop_per_area_row_major"]).reshape(4, 4),
                            rtol=0, atol=1e-12), f"{target_id}: pooled map mismatch")
        prepared.append({
            "meta": meta, "record": record, "fine": fine, "direct": direct, "pooled": pooled,
            "top_direct": top_direct, "top_pooled": top_pooled,
            "rho_recomputed": float(rho), "tau_recomputed": float(tau), "overlap": overlap,
        })
    return prepared


def render_target(item: dict, scale: float, output_path: Path):
    meta, fine, direct = item["meta"], item["fine"], item["direct"]
    norm = TwoSlopeNorm(vmin=-scale, vcenter=0.0, vmax=scale)
    fig, axes = plt.subplots(1, 2, figsize=(12.8, 7.8), constrained_layout=False)
    fig.subplots_adjust(left=0.07, right=0.86, top=0.83, bottom=0.23, wspace=0.24)
    title = f'{display_label(meta["image_key"])} — {meta["target_class"]}'
    fig.suptitle(title, fontsize=18, fontweight="bold", y=0.96)
    fig.text(0.5, 0.915, "V34-B | paired signed spatial sensitivity maps from archived perturbation data",
             ha="center", fontsize=10.5)
    images = []
    for ax, grid, n, panel_title in (
        (axes[0], fine, 8, "Aligned 8×8 map (native fine cells)"),
        (axes[1], direct, 4, "Direct 4×4 map"),
    ):
        im = ax.imshow(grid, cmap="RdBu_r", norm=norm, interpolation="nearest", origin="upper")
        images.append(im)
        ax.set_title(panel_title, fontsize=12, pad=12, fontweight="bold")
        ax.set_xticks(np.arange(n), labels=np.arange(1, n + 1))
        ax.set_yticks(np.arange(n), labels=np.arange(1, n + 1))
        ax.set_xlabel("Grid column")
        ax.set_ylabel("Grid row")
        ax.set_xticks(np.arange(-0.5, n, 1), minor=True)
        ax.set_yticks(np.arange(-0.5, n, 1), minor=True)
        ax.grid(which="minor", color="#333333", linewidth=0.55, alpha=0.72)
        ax.tick_params(which="minor", bottom=False, left=False)
        ax.set_aspect("equal")
    for idx in item["top_pooled"]:
        row, col = divmod(idx, 4)
        axes[0].add_patch(Rectangle((2 * col - 0.5, 2 * row - 0.5), 2, 2,
                                    fill=False, edgecolor=GOLD, linewidth=2.2))
    for idx in item["top_direct"]:
        row, col = divmod(idx, 4)
        axes[1].add_patch(Rectangle((col - 0.5, row - 0.5), 1, 1,
                                    fill=False, edgecolor=GOLD, linewidth=2.2))
    cbar = fig.colorbar(images[0], ax=axes, fraction=0.035, pad=0.035, shrink=0.88, extend="both")
    cbar.set_label("Signed score-drop density\n(score drop / exact pixel-area fraction)", fontsize=9.5)
    cbar.ax.tick_params(labelsize=8.5)
    overlap_pct = 100.0 * item["overlap"] / 4.0
    metrics = (f'Spearman ρ = {item["rho_recomputed"]:.3f}     '
               f'Kendall τ-b = {item["tau_recomputed"]:.3f}     '
               f'Top-4 overlap = {item["overlap"]}/4 ({overlap_pct:.0f}%)')
    fig.text(0.5, 0.145, metrics, ha="center", va="center", fontsize=11.2,
             bbox=dict(boxstyle="round,pad=0.55", facecolor="white", edgecolor="#333333", linewidth=0.8))
    fig.text(0.5, 0.095,
             "Gold outlines: top four regions in each map; left outlines are 2×2 fine-cell footprints.",
             ha="center", fontsize=8.7)
    fig.text(0.5, 0.061,
             f"Common display scale: ±{scale:.4g}; saturated cells are clipped for display only. "
             "Ranks and metrics use un-clipped archived values.",
             ha="center", fontsize=8.2)
    fig.text(0.5, 0.025,
             f'Target ID: {meta["target_id"]} | Source image: {meta["image_key"]} | '
             f'Original dimensions: {meta["image_width"]}×{meta["image_height"]} px',
             ha="center", fontsize=7.8, color="#444444")
    fig.savefig(output_path, dpi=300, bbox_inches="tight", facecolor="white")
    return fig


def render_summary(prepared: list[dict], output_path: Path):
    labels = [f'{display_label(x["meta"]["image_key"])} — {x["meta"]["target_class"]}' for x in prepared]
    rhos = [x["rho_recomputed"] for x in prepared]
    taus = [x["tau_recomputed"] for x in prepared]
    overlaps = [x["overlap"] for x in prepared]
    order = np.argsort(rhos)
    y = np.arange(len(order))

    fig = plt.figure(figsize=(12.2, 7.2))
    grid = fig.add_gridspec(1, 2, width_ratios=[0.84, 0.16], wspace=0.03)
    ax = fig.add_subplot(grid[0, 0])
    ax_overlap = fig.add_subplot(grid[0, 1], sharey=ax)

    ax.barh(y - 0.18, np.asarray(rhos)[order], height=0.34, label="Spearman ρ")
    ax.barh(y + 0.18, np.asarray(taus)[order], height=0.34, label="Kendall τ-b")
    ax.set_yticks(y, labels=np.asarray(labels)[order])
    ax.set_xlim(-0.03, 0.74)
    ax.set_ylim(-0.65, len(order) - 0.35)
    ax.set_xlabel("Rank-correlation coefficient")
    ax.set_title("Spatial rank correlation by frozen target", fontsize=14, fontweight="bold")
    ax.grid(axis="x", alpha=0.25)
    ax.legend(loc="lower right")

    ax_overlap.set_xlim(0, 1)
    ax_overlap.set_ylim(ax.get_ylim())
    ax_overlap.set_title("Top-4\nshared", fontsize=10, fontweight="bold")
    ax_overlap.tick_params(left=False, labelleft=False, bottom=False, labelbottom=False)
    for spine in ax_overlap.spines.values():
        spine.set_visible(False)
    for yi, idx in enumerate(order):
        ax_overlap.text(0.02, yi, f'{overlaps[idx]}/4', va="center", ha="left", fontsize=9)

    fig.suptitle("V34-B | spatial rank agreement across ten frozen targets",
                 fontsize=16, fontweight="bold", y=0.99)
    fig.text(0.5, 0.015, "Descriptive target-level comparisons; eight source images, ten targets. "
             "No inferential p-values or external-generalization claim.", ha="center", fontsize=8.5)
    fig.tight_layout(rect=(0, 0.045, 1, 0.96))
    fig.savefig(output_path, dpi=300, bbox_inches="tight", facecolor="white")
    return fig

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, default=SOURCE_DEFAULT)
    parser.add_argument("--output-dir", type=Path, default=OUTPUT_DEFAULT)
    args = parser.parse_args()
    data = json.loads(args.source.read_text(encoding="utf-8"))
    prepared = validate_and_prepare(data)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    source_sha256 = hashlib.sha256(args.source.read_bytes()).hexdigest()
    displayed = np.concatenate([np.concatenate([x["fine"].ravel(), x["direct"].ravel()]) for x in prepared])
    require(np.isfinite(displayed).all(), "display values contain non-finite numbers")
    scale = float(np.percentile(np.abs(displayed), SCALE_PERCENTILE, method="linear"))
    require(scale > 0, "robust shared color scale must be positive")
    saturated_count = int(np.count_nonzero(np.abs(displayed) > scale))

    rows, manifest_targets = [], []
    pdf_path = args.output_dir / "V34B_PAIRED_HEATMAPS_2026-11-22.pdf"
    summary_path = args.output_dir / "V34B_SPATIAL_AGREEMENT_SUMMARY_2026-11-22.png"
    summary_fig = render_summary(prepared, summary_path)
    with PdfPages(pdf_path, metadata={
        "Title": "SEER-PPE V34-B paired spatial sensitivity maps",
        "Author": "SEER-PPE research workflow",
        "Subject": "Data-derived 8x8 and 4x4 spatial sensitivity heatmaps",
    }) as pdf:
        pdf.savefig(summary_fig, bbox_inches="tight")
        plt.close(summary_fig)
        for index, item in enumerate(prepared, start=1):
            meta = item["meta"]
            label = f'{display_label(meta["image_key"])}_{meta["target_class"]}'
            filename = f"V34B_F{index:02d}_{safe_slug(label)}.png"
            figure_path = args.output_dir / filename
            fig = render_target(item, scale, figure_path)
            pdf.savefig(fig, bbox_inches="tight")
            plt.close(fig)
            overlap_pct = item["overlap"] / 4.0
            rows.append({
                "figure": filename, "target_id": meta["target_id"], "image_key": meta["image_key"],
                "split": meta["split"], "target_class": meta["target_class"],
                "image_width": meta["image_width"], "image_height": meta["image_height"],
                "spearman_rho": item["rho_recomputed"], "kendall_tau_b": item["tau_recomputed"],
                "top4_overlap_count": item["overlap"], "top4_overlap_fraction": overlap_pct,
                "top4_direct_4x4_indices_row_major": ";".join(map(str, item["top_direct"])),
                "top4_pooled_8x8_indices_row_major": ";".join(map(str, item["top_pooled"])),
                "scale_limit_abs": scale,
            })
            manifest_targets.append({
                "figure": filename, "target_id": meta["target_id"], "image_key": meta["image_key"],
                "split": meta["split"], "target_class": meta["target_class"],
                "original_dimensions_px": [meta["image_width"], meta["image_height"]],
                "spearman_rho_recomputed": item["rho_recomputed"],
                "kendall_tau_b_recomputed": item["tau_recomputed"],
                "top4_direct_4x4_indices_row_major": item["top_direct"],
                "top4_pooled_8x8_indices_row_major": item["top_pooled"],
                "top4_overlap_count": item["overlap"], "top4_overlap_fraction": overlap_pct,
                "figure_caption": (
                    f'Paired signed sensitivity maps for {meta["target_class"]} in {meta["image_key"]}. '
                    "Left: native 8x8 child-cell densities; gold outlines show the 2x2 fine-cell "
                    "footprints of the four highest-ranked pooled 4x4 regions. Right: direct 4x4 "
                    "densities; gold outlines show its four highest-ranked regions. Correlations "
                    "are computed across the 16 aligned coarse regions using un-clipped archived values."
                ),
            })

    csv_path = args.output_dir / "V34B_FIGURE_METRICS_2026-11-22.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    manifest = {
        "schema_version": "seer-ppe/v34b-data-derived-figures/v1.0",
        "status": "PASSED", "analysis_date": data["analysis_date"],
        "execution_mode": "offline_only_no_model_inference",
        "source_archive": SOURCE_DEFAULT.name, "source_archive_git_blob_sha": SOURCE_GIT_BLOB_SHA,
        "source_archive_sha256": source_sha256, "source_archive_schema": data["schema_version"],
        "source_target_count": len(prepared), "source_unique_images": data["sample"]["unique_images"],
        "figure_count": len(manifest_targets), "summary_figure": summary_path.name,
        "multipage_pdf": pdf_path.name, "metrics_csv": csv_path.name,
        "display": {
            "colormap": "RdBu_r", "center": 0.0, "shared_symmetric_abs_limit": scale,
            "scale_percentile_of_absolute_displayed_values": SCALE_PERCENTILE,
            "displayed_cell_value_count": int(displayed.size),
            "saturated_cell_value_count": saturated_count,
            "saturated_fraction": saturated_count / int(displayed.size),
            "clipping_affects_display_only": True,
            "all_rankings_and_metrics_use_unclipped_archived_values": True,
            "top4_left_panel": "four 2x2 fine-cell footprints for top-ranked pooled 4x4 regions",
            "top4_right_panel": "four highest-ranked direct 4x4 regions",
        },
        "reproducibility_checks": {
            "target_ids_matched": True, "all_10_targets_rendered": len(manifest_targets) == 10,
            "spearman_recomputed_against_archive": True, "kendall_tau_b_recomputed_against_archive": True,
            "top4_sets_recomputed_against_archive": True, "top4_overlap_recomputed_against_archive": True,
            "fine_cells_per_target": 64, "aligned_coarse_regions_per_target": 16,
            "new_model_inference_calls": 0, "test_split_accessed": False,
            "dataset_or_annotation_mutations": 0,
        },
        "targets": manifest_targets,
    }
    manifest_path = args.output_dir / "V34B_FIGURES_MANIFEST_2026-11-22.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    report = [
        "# V34-B — Data-derived scientific figures", "",
        "**Status:** PASSED; all ten figures generated from archived V34-A numeric maps.",
        "**Execution:** offline only; zero detector/model calls; no Test access or dataset mutation.", "",
        f"- Source archive SHA-256: {source_sha256}",
        f"- Common diverging color scale: ±{scale:.8g} (97.5th percentile of absolute displayed values).",
        f"- Displayed values saturated at scale limit: {saturated_count}/{displayed.size} "
        f"({100*saturated_count/displayed.size:.2f}%). Saturation affects display only.",
        "- All rank statistics and top-four selections are recomputed from un-clipped archived values.",
        "- Spearman, Kendall tau-b and top-four overlap were recomputed and matched the V34-A archive for all ten targets.",
        "", "## Outputs", "",
        f"- Multi-page PDF: {pdf_path.name} (summary page plus ten target figures).",
        f"- Summary PNG: {summary_path.name}", f"- Metrics CSV: {csv_path.name}",
        f"- Full provenance and target manifest: {manifest_path.name}", "",
        "## Scientific interpretation boundary", "",
        "These figures visualize signed detector-response sensitivity under the frozen gray-occlusion protocol. "
        "They are not source photographs, human-grounded explanation maps, causal proof, worker-compliance labels, "
        "or evidence of A5/A6 superiority. The top-four boxes on the 8x8 panel represent 2x2 fine-cell footprints "
        "of the pooled 4x4 regions used for the spatial-rank comparison.",
    ]
    report_path = args.output_dir / "V34B_FIGURE_GENERATION_REPORT_2026-11-22.md"
    report_path.write_text("\n".join(report) + "\n", encoding="utf-8")
    require(len(list(args.output_dir.glob("V34B_F*.png"))) == 10, "expected ten individual target PNGs")
    print(json.dumps({
        "status": "PASSED", "targets": len(prepared), "shared_scale_abs_limit": scale,
        "saturated_cells": saturated_count, "displayed_cells": int(displayed.size),
        "outputs": sorted(p.name for p in args.output_dir.iterdir()), "model_inference_calls": 0,
    }, indent=2))


if __name__ == "__main__":
    main()
