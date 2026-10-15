#!/usr/bin/env python3
"""Audit the immutable frozen dual-domain data package without extracting it.

Reports split sizes, class counts, safety-violation prevalence, and exact
cross-domain image duplicates. This script does not read model predictions and
never changes dataset contents.
"""

from __future__ import annotations

import argparse
import collections
import hashlib
import json
import zipfile
from pathlib import Path

DATASETS = ["Y-PPE-h9-v2", "Construction-PPE-h9-v2"]
SPLITS = ["train", "valid", "test"]
CLASSES = ["person", "helmet", "gloves", "vest", "boots", "goggles", "no_helmet", "no_gloves", "no_boots"]
SAFETY = {6, 7, 8}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--zip", required=True)
    p.add_argument("--out", required=True)
    args = p.parse_args()

    summary = {}
    by_hash = collections.defaultdict(list)

    with zipfile.ZipFile(args.zip) as z:
        names = set(z.namelist())
        for ds in DATASETS:
            summary[ds] = {}
            manifest = json.loads(z.read(f"{ds}/PACKAGE_MANIFEST.json"))
            summary[ds]["package_manifest"] = manifest

            for split in SPLITS:
                lp = f"{ds}/{split}/labels/"
                labels = sorted(n for n in names if n.startswith(lp) and n.endswith(".txt"))
                counts = collections.Counter()
                safety_frames = 0
                safety_presence = collections.Counter()
                boxes = 0

                for name in labels:
                    ids = []
                    text = z.read(name).decode("utf-8", errors="replace")
                    for line in text.splitlines():
                        parts = line.split()
                        if len(parts) < 5:
                            continue
                        cid = int(float(parts[0]))
                        ids.append(cid)
                        counts[cid] += 1
                        boxes += 1
                    if any(cid in SAFETY for cid in ids):
                        safety_frames += 1
                    for cid in SAFETY:
                        if cid in ids:
                            safety_presence[cid] += 1

                summary[ds][split] = {
                    "frames": len(labels),
                    "boxes": boxes,
                    "class_counts": {CLASSES[i]: counts[i] for i in range(len(CLASSES))},
                    "safety_frames": safety_frames,
                    "safety_frame_fraction": safety_frames / len(labels) if labels else None,
                    "safety_frame_presence_counts": {CLASSES[i]: safety_presence[i] for i in sorted(SAFETY)},
                    "safety_box_count": sum(counts[i] for i in SAFETY),
                }

                ip = f"{ds}/{split}/images/"
                for name in names:
                    if name.startswith(ip) and not name.endswith("/"):
                        digest = hashlib.sha256(z.read(name)).hexdigest()
                        by_hash[digest].append((ds, split, name))

        cross = []
        for digest, items in by_hash.items():
            if len({x[0] for x in items}) > 1:
                cross.append({"sha256": digest, "items": items})
        summary["exact_cross_domain_duplicate_hash_groups"] = len(cross)
        summary["exact_cross_domain_duplicates"] = cross

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(f"FROZEN_DATA_AUDIT_COMPLETE -> {out}")


if __name__ == "__main__":
    main()
