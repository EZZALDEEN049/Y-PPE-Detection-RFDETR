#!/usr/bin/env python3
"""Detect explicit same-video source groups spanning dataset splits.

This companion Stage 2 check uses exported Roboflow filenames only when they
contain an explicit media filename token followed by a frame index, e.g.
`Sapi-7_mp4-223_jpg.rf....jpg`. Such groups are treated as confirmed
source-group leakage if frames from the same media file occur in >1 split.

The script is read-only. It does not infer generic filename families such as
`h12`, `images`, or `1`, because those can collide across unrelated assets.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

MEDIA_RE = re.compile(r"^(.*?_(?:mp4|mov|avi|mkv|webm))-(\d+)(?:_|$)", re.I)


def source_media_group(filename: str):
    pre = filename.split('.rf.', 1)[0]
    m = MEDIA_RE.match(pre)
    if not m:
        return None, None
    return m.group(1), int(m.group(2))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--image-manifest', required=True, type=Path)
    ap.add_argument('--out', required=True, type=Path)
    args = ap.parse_args()

    records = json.loads(args.image_manifest.read_text(encoding='utf-8'))
    groups = defaultdict(list)
    for rec in records:
        group, frame = source_media_group(rec.get('name', ''))
        if group is None:
            continue
        groups[group].append({**rec, 'media_group': group, 'frame_index': frame})

    cross = {}
    for group, recs in sorted(groups.items()):
        split_counts = Counter(r['split'] for r in recs)
        if len(split_counts) > 1:
            cross[group] = {
                'split_counts': dict(sorted(split_counts.items())),
                'total_exported_images': len(recs),
                'frames': sorted({r['frame_index'] for r in recs}),
                'records': sorted(recs, key=lambda r: (r['split'], r['frame_index'], r['name'])),
            }

    args.out.mkdir(parents=True, exist_ok=True)
    js = args.out / 'cross_split_video_groups.json'
    js.write_text(json.dumps({
        'rule': 'explicit media filename token + frame index; same media file must not span splits',
        'cross_split_video_group_count': len(cross),
        'groups': cross,
    }, indent=2, ensure_ascii=False), encoding='utf-8')

    csv_path = args.out / 'cross_split_video_groups.csv'
    with csv_path.open('w', newline='', encoding='utf-8-sig') as f:
        w = csv.DictWriter(f, fieldnames=['media_group','frame_index','split','file','sha256','pixel_sha256'])
        w.writeheader()
        for group, info in cross.items():
            for rec in info['records']:
                w.writerow({
                    'media_group': group,
                    'frame_index': rec['frame_index'],
                    'split': rec['split'],
                    'file': rec['name'],
                    'sha256': rec.get('sha256',''),
                    'pixel_sha256': rec.get('pixel_sha256',''),
                })

    print(json.dumps({
        'cross_split_video_group_count': len(cross),
        'groups': {g: info['split_counts'] for g, info in cross.items()},
        'output_json': str(js),
        'output_csv': str(csv_path),
    }, indent=2, ensure_ascii=False))
    raise SystemExit(2 if cross else 0)


if __name__ == '__main__':
    main()
