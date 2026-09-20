#!/usr/bin/env python3
"""Apply the frozen Stage 4.5 conservative label-completeness filter.

The filter is annotation-only. It never decodes image pixels. Images are excluded
when Stage 4.5 structural audit marks them as either:
  * harmonized_empty, or
  * critical_unmatched:<source class>

This creates a filtered native-label derivative that can be passed to the frozen
Stage 4 harmonization builder. Test membership decisions therefore depend only on
source annotations/geometry and never on test pixels or model predictions.
"""
from __future__ import annotations

import argparse
import csv
import json
import shutil
from collections import Counter, defaultdict
from pathlib import Path

IMAGE_EXTS = {'.jpg', '.jpeg', '.png', '.bmp', '.tif', '.tiff', '.webp'}


def parse_split_map(text: str) -> dict[str, str]:
    out: dict[str, str] = {}
    for item in text.split(','):
        logical, physical = item.split(':', 1)
        out[logical.strip()] = physical.strip()
    return out


def resolve_split_dirs(root: Path, physical_split: str) -> tuple[Path, Path]:
    candidates = [
        (root / physical_split / 'images', root / physical_split / 'labels'),
        (root / 'images' / physical_split, root / 'labels' / physical_split),
    ]
    for images, labels in candidates:
        if images.is_dir() and labels.is_dir():
            return images, labels
    raise SystemExit(f'Could not resolve split={physical_split} under {root}')


def should_exclude(risk_reasons: str) -> bool:
    tokens = [x.strip() for x in (risk_reasons or '').split('|') if x.strip()]
    return 'harmonized_empty' in tokens or any(x.startswith('critical_unmatched:') for x in tokens)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', required=True)
    ap.add_argument('--splits', required=True,
                    help='logical:physical mapping, e.g. train:train,val:valid,test:test')
    ap.add_argument('--risk-csv', required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('--summary-out', required=True)
    ap.add_argument('--exclusion-manifest-out', required=True)
    ap.add_argument('--expected-exclusions', type=int)
    args = ap.parse_args()

    root = Path(args.root).resolve()
    out = Path(args.out).resolve()
    risk_csv = Path(args.risk_csv).resolve()
    split_map = parse_split_map(args.splits)

    excluded: dict[str, dict[str, str]] = defaultdict(dict)
    with risk_csv.open(newline='', encoding='utf-8') as f:
        for row in csv.DictReader(f):
            logical = row['logical_split'].strip()
            if logical not in split_map:
                raise SystemExit(f'Risk CSV contains unexpected logical split: {logical}')
            stem = row['file_stem'].strip()
            if should_exclude(row.get('risk_reasons', '')):
                excluded[logical][stem] = row.get('risk_reasons', '')

    total_exclusions = sum(len(v) for v in excluded.values())
    if args.expected_exclusions is not None and total_exclusions != args.expected_exclusions:
        raise SystemExit(
            f'Exclusion-count drift: observed={total_exclusions}, expected={args.expected_exclusions}'
        )

    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)

    split_summary: dict[str, dict] = {}
    manifest_rows: list[dict] = []

    for logical, physical in split_map.items():
        src_images, src_labels = resolve_split_dirs(root, physical)
        dst_images = out / 'images' / physical
        dst_labels = out / 'labels' / physical
        dst_images.mkdir(parents=True, exist_ok=True)
        dst_labels.mkdir(parents=True, exist_ok=True)

        counts = Counter()
        image_files = sorted(
            p for p in src_images.iterdir()
            if p.is_file() and p.suffix.lower() in IMAGE_EXTS
        )
        for image in image_files:
            label = src_labels / f'{image.stem}.txt'
            if not label.exists():
                raise SystemExit(f'Missing label for source image: {image}')
            counts['source_images'] += 1
            reason = excluded.get(logical, {}).get(image.stem)
            if reason is not None:
                counts['excluded_images'] += 1
                manifest_rows.append({
                    'logical_split': logical,
                    'physical_split': physical,
                    'file_stem': image.stem,
                    'image_name': image.name,
                    'label_name': label.name,
                    'risk_reasons': reason,
                })
                continue
            shutil.copy2(image, dst_images / image.name)
            shutil.copy2(label, dst_labels / label.name)
            counts['retained_images'] += 1

        expected_split_exclusions = len(excluded.get(logical, {}))
        if counts['excluded_images'] != expected_split_exclusions:
            raise SystemExit(
                f'Split exclusion mismatch {logical}: copied logic saw {counts["excluded_images"]}, '
                f'risk table selected {expected_split_exclusions}'
            )
        split_summary[logical] = dict(counts)

    manifest_path = Path(args.exclusion_manifest_out)
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    fields = ['logical_split', 'physical_split', 'file_stem', 'image_name', 'label_name', 'risk_reasons']
    with manifest_path.open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(sorted(manifest_rows, key=lambda r: (r['logical_split'], r['file_stem'])))

    summary = {
        'policy': 'exclude_harmonized_empty_or_any_critical_unmatched_image',
        'source_root': str(root),
        'filtered_root': str(out),
        'risk_csv': str(risk_csv),
        'total_exclusions': total_exclusions,
        'split_summary': split_summary,
        'test_pixels_opened': False,
        'model_predictions_used': False,
        'image_pixels_decoded_by_filter': False,
        'membership_rule_uses_only_source_annotation_metadata': True,
        'exclusion_manifest': str(manifest_path),
    }
    sp = Path(args.summary_out)
    sp.parent.mkdir(parents=True, exist_ok=True)
    sp.write_text(json.dumps(summary, indent=2), encoding='utf-8')
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
