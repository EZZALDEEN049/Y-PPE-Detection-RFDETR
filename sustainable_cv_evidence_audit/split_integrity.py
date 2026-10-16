#!/usr/bin/env python3
"""Audit two exported image datasets without training, decoding or publishing image IDs."""
import argparse
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

SPLITS = ("train", "valid", "test")
ALIASES = {"train": ("train",), "valid": ("valid", "val", "validation"), "test": ("test",)}
EXT = {".jpg", ".jpeg", ".png", ".bmp", ".webp", ".tif", ".tiff"}


def digest(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for part in iter(lambda: f.read(1024 * 1024), b""):
            h.update(part)
    return h.hexdigest()


def scan(root):
    if not root.is_dir():
        raise ValueError("Dataset path must be an existing directory.")
    output = {}
    for split in SPLITS:
        candidates = []
        for alias in ALIASES[split]:
            for path in (root / alias / "images", root / "images" / alias):
                if path.is_dir() and path not in candidates:
                    candidates.append(path)
        if len(candidates) != 1:
            raise ValueError("Missing or ambiguous image directory for " + split)
        directory = candidates[0]
        images = sorted(
            (p for p in directory.rglob("*") if p.is_file() and p.suffix.lower() in EXT),
            key=lambda p: p.relative_to(directory).as_posix()
        )
        if not images:
            raise ValueError("No images in " + split)
        output[split] = {
            p.relative_to(directory).as_posix(): digest(p) for p in images
        }
    return output


def sets_by_split(items):
    return {s: set(items[s]) for s in SPLITS}


def within_split_conflicts(groups):
    return {
        f"{a}_vs_{b}": len(groups[a] & groups[b])
        for i, a in enumerate(SPLITS) for b in SPLITS[i+1:]
    }


def between_split_conflicts(a, b):
    return {
        f"a_{left}_vs_b_{right}": len(a[left] & b[right])
        for left in SPLITS for right in SPLITS if left != right
    }


def summaries(files):
    return {
        s: {
            "files": len(files[s]),
            "unique_byte_hashes": len(set(files[s].values())),
            "duplicate_copies_within_split": len(files[s]) - len(set(files[s].values()))
        } for s in SPLITS
    }


def load_map(path, files):
    aliases = {alias: split for split, values in ALIASES.items() for alias in values}
    mapping = {s: {} for s in SPLITS}
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        rows = csv.DictReader(f)
        if not rows.fieldnames or not {"split", "file", "source_id"} <= set(rows.fieldnames):
            raise ValueError("Source map needs split,file,source_id columns.")
        for row in rows:
            split = aliases.get((row.get("split") or "").strip().lower())
            name = (row.get("file") or "").strip().replace("\\", "/")
            source_id = (row.get("source_id") or "").strip()
            if not split or not name or not source_id or name not in files[split]:
                raise ValueError("Source map contains invalid/extra record.")
            if name in mapping[split]:
                raise ValueError("Source map contains duplicated record.")
            mapping[split][name] = source_id
    if any(mapping[s].keys() != files[s].keys() for s in SPLITS):
        raise ValueError("Source map is incomplete.")
    return {s: set(mapping[s].values()) for s in SPLITS}


def assess(dataset_a, dataset_b, map_a=None, map_b=None):
    if (map_a is None) != (map_b is None):
        raise ValueError("Supply two source maps or neither.")
    a, b = scan(dataset_a), scan(dataset_b)
    ah, bh = sets_by_split({s: list(a[s].values()) for s in SPLITS}), sets_by_split(
        {s: list(b[s].values()) for s in SPLITS}
    )
    ac, bc = within_split_conflicts(ah), within_split_conflicts(bh)
    cross = between_split_conflicts(ah, bh)
    equals = {
        s: Counter(a[s].values()) == Counter(b[s].values()) for s in SPLITS
    }
    report = {
        "dataset_a": summaries(a), "dataset_b": summaries(b),
        "identical_exported_byte_multisets_per_split": equals,
        "all_splits_exported_byte_multisets_identical": all(equals.values()),
        "same_split_matching_byte_hash_counts": {s: len(ah[s] & bh[s]) for s in SPLITS},
        "within_a_cross_split_byte_hash_overlap": ac,
        "within_b_cross_split_byte_hash_overlap": bc,
        "across_tracks_different_split_byte_hash_overlap": cross,
        "no_detected_exact_byte_cross_split_overlap": not any(
            list(ac.values()) + list(bc.values()) + list(cross.values())
        ),
        "source_id_audit": {"status": "not_provided", "provenance_verified": False},
        "controlled_architecture_comparison_established": False,
        "limitations": [
            "Byte hashes identify identical exported image bytes, not original scenes.",
            "Different augmentations/resizes may conceal shared original images.",
            "Operator-supplied source IDs require independent provenance adjudication.",
            "Labels, ontology, checkpoints and common metric evaluator not audited."
        ]
    }
    if map_a is not None:
        sa, sb = load_map(map_a, a), load_map(map_b, b)
        report["source_id_audit"] = {
            "status": "candidate_operator_supplied_ids_unverified_provenance",
            "candidate_matching_source_membership": {s: sa[s] == sb[s] for s in SPLITS},
            "distinct_source_id_counts_a": {s: len(sa[s]) for s in SPLITS},
            "distinct_source_id_counts_b": {s: len(sb[s]) for s in SPLITS},
            "within_a_source_id_overlap": within_split_conflicts(sa),
            "within_b_source_id_overlap": within_split_conflicts(sb),
            "across_tracks_different_split_source_id_overlap": between_split_conflicts(sa, sb),
            "provenance_verified": False
        }
    return report


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("dataset_a", type=Path)
    p.add_argument("dataset_b", type=Path)
    p.add_argument("--source-map-a", type=Path)
    p.add_argument("--source-map-b", type=Path)
    p.add_argument("--output", required=True, type=Path)
    p.add_argument("--require-identical-exported-bytes", action="store_true")
    args = p.parse_args()
    try:
        report = assess(args.dataset_a, args.dataset_b, args.source_map_a, args.source_map_b)
    except (ValueError, OSError) as exc:
        p.error(str(exc))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "byte_partition_identity": report["all_splits_exported_byte_multisets_identical"],
        "no_detected_byte_overlap": report["no_detected_exact_byte_cross_split_overlap"],
        "source_ids": report["source_id_audit"]["status"],
        "architecture_comparison_established": False
    }, indent=2))
    if args.require_identical_exported_bytes and not (
        report["all_splits_exported_byte_multisets_identical"]
        and report["no_detected_exact_byte_cross_split_overlap"]
    ):
        raise SystemExit(2)


if __name__ == "__main__":
    main()
