#!/usr/bin/env python3
"""Apply the frozen Stage 4.5 whole-image exclusion policy.

The policy is annotation-only. It never decodes image pixels and never changes
annotation rows. It copies the cleaned native dataset, then removes whole
image/label pairs selected from the Stage 4.5 risk table.
"""
from __future__ import annotations

import argparse
import csv
import json
import shutil
from collections import Counter
from pathlib import Path

IMAGE_EXTS = {'.jpg', '.jpeg', '.png', '.bmp', '.tif', '.tiff', '.webp'}


def parse_reasons(text: str) -> set[str]:
    return {x for x in (text or '').split('|') if x}


def parse_classes(text: str) -> set[str]:
    return {x for x in (text or '').split('|') if x}


def should_exclude(dataset: str, risk_reasons: str, excluded_classes: str) -> tuple[bool, str]:
    reasons = parse_reasons(risk_reasons)
    classes = parse_classes(excluded_classes)

    if dataset == 'Y-PPE':
        if any(r.startswith('critical_unmatched:') for r in reasons):
            return True, 'critical_unmatched_excluded_class'
        if 'harmonized_empty' in reasons and classes != {'Animal'}:
            return True, 'unsafe_harmonized_empty_non_animal_only'
        return False, 'retain'

    if dataset == 'Construction-PPE':
        if 'critical_unmatched:none' in reasons:
            return True, 'critical_unmatched_none'
        if 'harmonized_empty' in reasons:
            return True, 'harmonized_empty'
        return False, 'retain'

    raise ValueError(dataset)


def resolve_split_dirs(root: Path, physical_split: str) -> tuple[Path, Path]:
    for images, labels in [
        (root / physical_split / 'images', root / physical_split / 'labels'),
        (root / 'images' / physical_split, root / 'labels' / physical_split),
    ]:
        if images.is_dir() and labels.is_dir():
            return images, labels
    raise FileNotFoundError(f'Could not resolve split={physical_split} under {root}')


def image_matches(images_dir: Path, stem: str) -> list[Path]:
    return sorted(
        p for p in images_dir.glob(stem + '.*')
        if p.is_file() and p.suffix.lower() in IMAGE_EXTS
    )


def count_split(root: Path, physical_split: str) -> dict[str, int]:
    images, labels = resolve_split_dirs(root, physical_split)
    image_count = sum(1 for p in images.iterdir() if p.is_file() and p.suffix.lower() in IMAGE_EXTS)
    label_count = sum(1 for p in labels.glob('*.txt') if p.is_file())
    return {'images': image_count, 'labels': label_count}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument('--dataset', required=True, choices=['Y-PPE', 'Construction-PPE'])
    ap.add_argument('--root', required=True)
    ap.add_argument('--risk-csv', required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('--summary-out', required=True)
    ap.add_argument('--expected-train-removals', type=int)
    ap.add_argument('--expected-val-removals', type=int)
    ap.add_argument('--expected-test-removals', type=int)
    args = ap.parse_args()

    src = Path(args.root).resolve()
    out = Path(args.out).resolve()
    risk_csv = Path(args.risk_csv).resolve()
    summary_path = Path(args.summary_out).resolve()

    if out.exists():
        shutil.rmtree(out)
    shutil.copytree(src, out)

    rows = list(csv.DictReader(risk_csv.open(encoding='utf-8')))
    removals = []
    reason_counts = Counter()
    split_counts = Counter()

    for row in rows:
        exclude, decision_reason = should_exclude(
            args.dataset,
            row.get('risk_reasons', ''),
            row.get('excluded_classes', ''),
        )
        if not exclude:
            continue

        logical = row['logical_split']
        physical = row['physical_split']
        stem = row['file_stem']
        images_dir, labels_dir = resolve_split_dirs(out, physical)
        matches = image_matches(images_dir, stem)
        label = labels_dir / f'{stem}.txt'

        if len(matches) != 1:
            raise RuntimeError(f'{args.dataset} {logical}:{stem}: expected exactly one image, found {matches}')
        if not label.exists():
            raise RuntimeError(f'{args.dataset} {logical}:{stem}: missing label {label}')

        # Removing a file does not decode or visually inspect its image pixels.
        matches[0].unlink()
        label.unlink()

        reason_counts[decision_reason] += 1
        split_counts[logical] += 1
        removals.append({
            'dataset': args.dataset,
            'logical_split': logical,
            'physical_split': physical,
            'file_stem': stem,
            'decision_reason': decision_reason,
            'audit_risk_reasons': row.get('risk_reasons', ''),
            'excluded_classes': row.get('excluded_classes', ''),
        })

    expected = {
        'train': args.expected_train_removals,
        'val': args.expected_val_removals,
        'test': args.expected_test_removals,
    }
    for split, exp in expected.items():
        if exp is not None and split_counts[split] != exp:
            raise RuntimeError(
                f'{args.dataset} {split}: expected {exp} removals, observed {split_counts[split]}'
            )

    physical_by_logical = {}
    for row in rows:
        physical_by_logical.setdefault(row['logical_split'], row['physical_split'])

    final_counts = {
        logical: count_split(out, physical)
        for logical, physical in sorted(physical_by_logical.items())
    }
    for logical, counts in final_counts.items():
        if counts['images'] != counts['labels']:
            raise RuntimeError(f'{args.dataset} {logical}: image/label mismatch after policy: {counts}')

    manifest_path = summary_path.with_name(summary_path.stem + '_removals.csv')
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    with manifest_path.open('w', newline='', encoding='utf-8') as f:
        fields = [
            'dataset', 'logical_split', 'physical_split', 'file_stem',
            'decision_reason', 'audit_risk_reasons', 'excluded_classes'
        ]
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(removals)

    summary = {
        'stage': '4.5',
        'dataset': args.dataset,
        'source_root': str(src),
        'output_root': str(out),
        'risk_csv': str(risk_csv),
        'policy': {
            'whole_image_exclusion_only': True,
            'annotation_rows_relabelled': False,
            'model_outputs_used': False,
            'test_pixels_decoded_or_visually_opened': False,
            'Y-PPE': 'exclude any critical_unmatched:*; exclude harmonized_empty unless excluded classes are exactly Animal',
            'Construction-PPE': 'exclude critical_unmatched:none and all harmonized_empty images',
        },
        'removals_by_split': dict(split_counts),
        'removals_by_reason': dict(reason_counts),
        'final_counts': final_counts,
        'removal_manifest': str(manifest_path),
    }
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.write_text(json.dumps(summary, indent=2), encoding='utf-8')
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
