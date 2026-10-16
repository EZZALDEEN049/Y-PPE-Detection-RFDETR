#!/usr/bin/env python3
"""Conservative audit of two pre-existing Roboflow model-linked exports.

Inputs are private on disk. Emits ONLY counts and booleans: no image content,
hashes, file paths, labels, source IDs or credentials. Requires PyYAML.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from collections import Counter
from decimal import Decimal, InvalidOperation
from pathlib import Path

from split_integrity import assess as byte_audit, scan, SPLITS, ALIASES


def class_names(root: Path) -> list[str]:
    import yaml
    candidates = [p for p in (root / "data.yaml", root / "dataset.yaml") if p.is_file()]
    if len(candidates) != 1:
        raise ValueError("One unambiguous data.yaml or dataset.yaml is required.")
    data = yaml.safe_load(candidates[0].read_text(encoding="utf-8"))
    if not isinstance(data, dict) or "names" not in data:
        raise ValueError("Class ontology missing.")
    names = data["names"]
    if isinstance(names, dict):
        if sorted(names) != list(range(len(names))):
            raise ValueError("Class name keys must be consecutive integer IDs.")
        names = [names[i] for i in range(len(names))]
    if not isinstance(names, list) or not names or any(
        not isinstance(name, str) or not name.strip() for name in names
    ):
        raise ValueError("Class ontology must be a list of nonempty names.")
    if len(set(names)) != len(names):
        raise ValueError("Duplicate ontology class names.")
    if "nc" in data and int(data["nc"]) != len(names):
        raise ValueError("nc and ontology name count differ.")
    return names


def locate_split_image_dir(root: Path, split: str) -> Path:
    candidates = []
    for alias in ALIASES[split]:
        for candidate in (root / alias / "images", root / "images" / alias):
            if candidate.is_dir() and candidate not in candidates:
                candidates.append(candidate)
    if len(candidates) != 1:
        raise ValueError("Ambiguous image layout.")
    return candidates[0]


def canonical_label(path: Path, nc: int) -> str:
    if not path.exists():
        raise ValueError("Missing label file for a test image.")
    if not path.is_file():
        raise ValueError("Label path is not a file.")
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        tokens = line.split()
        if not tokens:
            continue
        if len(tokens) != 5:
            raise ValueError("Non-five-column YOLO detection row found.")
        if not tokens[0].isdigit() or not 0 <= int(tokens[0]) < nc:
            raise ValueError("Class ID out of range.")
        try:
            coords = [Decimal(s) for s in tokens[1:]]
        except InvalidOperation as exc:
            raise ValueError("Non-numeric box coordinate.") from exc
        if not all(c.is_finite() and 0 <= c <= 1 for c in coords):
            raise ValueError("Nonfinite or out-of-range box coordinate.")
        if coords[2] <= 0 or coords[3] <= 0:
            raise ValueError("Zero-size annotation box.")
        if coords[0] - coords[2] / 2 < 0 or coords[0] + coords[2] / 2 > 1:
            raise ValueError("Box extends horizontally beyond image.")
        if coords[1] - coords[3] / 2 < 0 or coords[1] + coords[3] / 2 > 1:
            raise ValueError("Box extends vertically beyond image.")
        rows.append((int(tokens[0]), *(str(c.normalize()) for c in coords)))
    rows.sort()
    return hashlib.sha256(json.dumps(rows, separators=(",", ":")).encode()).hexdigest()


def test_annotations(root: Path, files: dict[str, dict[str, str]], nc: int) -> dict:
    test_dir = locate_split_image_dir(root, "test")
    if test_dir.parent.name == "images":
        label_dir = root / "labels" / test_dir.name
    else:
        label_dir = test_dir.parent / "labels"
    records = {}
    for rel, image_sha in files["test"].items():
        label_sha = canonical_label(label_dir / Path(rel).with_suffix(".txt"), nc)
        records.setdefault(image_sha, []).append(label_sha)
    return {key: Counter(sigs) for key, sigs in records.items()}


def run(dataset_a: Path, dataset_b: Path, expected=(4875, 468, 234)) -> dict:
    # Existing split-integrity audit preserves exported-image multiplicity.
    base = byte_audit(dataset_a, dataset_b)
    names_a, names_b = class_names(dataset_a), class_names(dataset_b)
    files_a, files_b = scan(dataset_a), scan(dataset_b)
    ontologies_same = names_a == names_b
    label_readable = False
    labels_agree_on_exact_images = False
    matched_image_hashes = base["same_split_matching_byte_hash_counts"]["test"]
    label_groups_compared = 0
    differing_annotation_groups = 0
    label_error_type = None
    try:
        # Only meaningful for matched class IDs; never silently align different classes.
        if ontologies_same:
            ann_a = test_annotations(dataset_a, files_a, len(names_a))
            ann_b = test_annotations(dataset_b, files_b, len(names_b))
            label_readable = True
            common = ann_a.keys() & ann_b.keys()
            label_groups_compared = len(common)
            differing_annotation_groups = sum(ann_a[k] != ann_b[k] for k in common)
            labels_agree_on_exact_images = bool(common) and differing_annotation_groups == 0
    except (OSError, ValueError) as exc:
        # No raw annotations or filenames in CI log or report.
        label_error_type = type(exc).__name__
    expected_counts = {split: n for split, n in zip(SPLITS, expected)}
    counts_expected_a = all(base["dataset_a"][s]["files"] == n for s, n in expected_counts.items())
    counts_expected_b = all(base["dataset_b"][s]["files"] == n for s, n in expected_counts.items())
    return {
        "study": "Y-PPE two-model exported-data identity preflight",
        "inputs": "YOLO11m-linked export v1 vs RF-DETR-Small-linked export v2",
        "actual_datasets_examined": True,
        "model_inference_or_training_performed": False,
        "expected_counts_per_export_from_repository_documentation": expected_counts,
        "export_a_counts_match_expectations": counts_expected_a,
        "export_b_counts_match_expectations": counts_expected_b,
        "export_a_counts": base["dataset_a"],
        "export_b_counts": base["dataset_b"],
        "ontology_a_class_count": len(names_a),
        "ontology_b_class_count": len(names_b),
        "ontology_class_order_strings_identical": ontologies_same,
        "all_splits_exported_byte_multisets_identical": base["all_splits_exported_byte_multisets_identical"],
        "no_detected_exact_byte_cross_split_overlap": base["no_detected_exact_byte_cross_split_overlap"],
        "exact_byte_cross_split_overlap_counts": {
            "within_a": base["within_a_cross_split_byte_hash_overlap"],
            "within_b": base["within_b_cross_split_byte_hash_overlap"],
            "between_tracks": base["across_tracks_different_split_byte_hash_overlap"]
        },
        "test_matching_distinct_exported_byte_hashes": matched_image_hashes,
        "heldout_annotation_files_parsed_when_ontologies_same": label_readable,
        "matched_test_image_groups_with_annotation_comparison": label_groups_compared,
        "matched_test_image_groups_with_annotation_mismatch": differing_annotation_groups,
        "test_annotations_agree_for_matched_exported_image_bytes": labels_agree_on_exact_images,
        "heldout_annotation_parsing_error_type": label_error_type,
        "original_source_group_membership_verified": False,
        "common_prediction_evaluator_executed": False,
        "controlled_architecture_accuracy_comparison_established": False,
        "energy_or_latency_measured": False,
        "limitations": [
            "Observed agreement is only exported-byte/label/ontology-string evidence; "
            "resized/augmented variants and site/source group leakage need adjudication.",
            "No fine-tuned model checkpoints or predictions were compared.",
            "Absent SHA match is not evidence of different source photographs.",
            "No identifiable image metadata, filenames or label contents are output."
        ]
    }


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dataset-a", type=Path, required=True)
    ap.add_argument("--dataset-b", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()
    try:
        report = run(args.dataset_a, args.dataset_b)
    except (OSError, ValueError) as exc:
        # Only class/status of an error; never print private paths/names/content.
        raise SystemExit("PAIR AUDIT BLOCKED: " + type(exc).__name__)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "a_expected_counts": report["export_a_counts_match_expectations"],
        "b_expected_counts": report["export_b_counts_match_expectations"],
        "identical_exported_bytes": report["all_splits_exported_byte_multisets_identical"],
        "same_ontology": report["ontology_class_order_strings_identical"],
        "source_groups_verified": False,
        "head_to_head_claim_proven": False,
    }, indent=2))
    # Do not raise for legitimate mismatches: produce auditable outcomes.


if __name__ == "__main__":
    main()
