#!/usr/bin/env python3
"""Fail-closed source-group and exact-image overlap screening for research splits.

Input CSV columns: image_id,site_id,acquisition_group_id,sha256,split.
Reports visible input provenance only. Unknown group is an error, not evidence of independence.
Does not detect visually similar scenes; a pHash/visual audit remains mandatory.
"""
import argparse
import csv
import json
from collections import defaultdict, Counter
from pathlib import Path

REQUIRED = {"image_id", "site_id", "acquisition_group_id", "sha256", "split"}
UNKNOWN = {"", "unknown", "n/a", "none", "null", "nan", "?"}


def audit(rows):
    splits = Counter()
    groups, hashes = defaultdict(set), defaultdict(set)
    seen_image_ids, bad = set(), []
    for index, row in enumerate(rows, start=2):
        missing = REQUIRED - set(row)
        if missing:
            raise ValueError(f"Row {index}: missing columns {sorted(missing)}")
        vals = {k: str(row[k] if row[k] is not None else "").strip() for k in REQUIRED}
        if any(vals[k].lower() in UNKNOWN for k in REQUIRED):
            raise ValueError(f"Row {index}: missing or unknown provenance field")
        digest = vals["sha256"].lower()
        if len(digest) != 64 or any(x not in "0123456789abcdef" for x in digest):
            raise ValueError(f"Row {index}: invalid SHA-256 digest")
        unique = (vals["site_id"], vals["image_id"])
        if unique in seen_image_ids:
            bad.append({"row": index, "duplicate_image_id": unique})
        seen_image_ids.add(unique)
        split = vals["split"]
        splits[split] += 1
        groups[(vals["site_id"], vals["acquisition_group_id"])].add(split)
        hashes[digest].add(split)
    if not splits:
        raise ValueError("Empty manifest")
    group_conflicts = [dict(site_id=site, acquisition_group_id=group, splits=sorted(splits))
                       for (site, group), splits in groups.items() if len(splits) > 1]
    hash_conflicts = [dict(sha256=digest, splits=sorted(splits))
                      for digest, splits in hashes.items() if len(splits) > 1]
    return {"status": "FAIL" if (group_conflicts or hash_conflicts or bad) else "PASS",
            "counts_by_split": dict(sorted(splits.items())),
            "acquisition_group_conflicts": group_conflicts,
            "exact_image_hash_conflicts": hash_conflicts,
            "duplicate_image_ids": bad,
            "limitations": "Does not prove visual, site or camera independence; field provenance must be audited."}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("manifest", type=Path)
    args = p.parse_args()
    with args.manifest.open(newline="", encoding="utf-8-sig") as f:
        report = audit(csv.DictReader(f))
    print(json.dumps(report, ensure_ascii=False, indent=2))
    raise SystemExit(0 if report["status"] == "PASS" else 1)


if __name__ == "__main__":
    main()
