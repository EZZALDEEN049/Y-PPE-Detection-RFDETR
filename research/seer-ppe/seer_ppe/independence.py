"""Independent-acquisition split gate for SEER-PPE.

Never use this on a selection already tuned to test outcomes. Exact hashes do
not detect perceptually similar or same-scene images: human review is required.
"""
from collections import defaultdict
from dataclasses import dataclass
import re
from typing import Iterable

_VALID_SPLITS = {"train", "valid", "test"}
_SHA256 = re.compile(r"^[0-9a-f]{64}$")

@dataclass(frozen=True)
class ImageRecord:
    image_id: str
    split: str
    acquisition_group_id: str
    sha256: str
    source_rights_status: str  # VERIFIED, RESTRICTED or UNKNOWN


def audit_split_independence(records: Iterable[ImageRecord]) -> dict:
    """Static pretest checks; a pass is not proof of visual scene independence."""
    rows = list(records)
    issues = []
    id_groups = defaultdict(set)
    hash_groups = defaultdict(set)
    acquisition_splits = defaultdict(set)
    seen_ids = set()
    unknown_rights = 0
    for idx, row in enumerate(rows):
        if not row.image_id or not row.image_id.strip():
            issues.append(f"row_{idx}:missing_image_id")
            continue
        if row.image_id in seen_ids:
            issues.append(f"{row.image_id}:duplicate_image_id")
        seen_ids.add(row.image_id)
        if row.split not in _VALID_SPLITS:
            issues.append(f"{row.image_id}:invalid_split")
        if not row.acquisition_group_id or row.acquisition_group_id.strip().lower() in {"unknown", "n/a", "none", "unverified"}:
            issues.append(f"{row.image_id}:unknown_acquisition_group")
        else:
            acquisition_splits[row.acquisition_group_id].add(row.split)
        if not _SHA256.fullmatch(row.sha256.lower()):
            issues.append(f"{row.image_id}:invalid_sha256")
        else:
            hash_groups[row.sha256.lower()].add(row.split)
        if row.source_rights_status not in {"VERIFIED", "RESTRICTED", "UNKNOWN"}:
            issues.append(f"{row.image_id}:invalid_rights_status")
        if row.source_rights_status != "VERIFIED":
            unknown_rights += 1
        id_groups[row.image_id].add(row.split)
    overlapping_groups = sorted(g for g, splits in acquisition_splits.items() if len(splits) > 1)
    overlapping_hashes = sorted(h for h, splits in hash_groups.items() if len(splits) > 1)
    if overlapping_groups:
        issues.append(f"cross_split_acquisition_groups:{len(overlapping_groups)}")
    if overlapping_hashes:
        issues.append(f"cross_split_exact_sha256:{len(overlapping_hashes)}")
    if not rows:
        issues.append("no_images")
    return {
        "n_images": len(rows), "split_counts": {s: sum(r.split == s for r in rows) for s in sorted(_VALID_SPLITS)},
        "overlapping_acquisition_groups": overlapping_groups,
        "overlapping_hashes": overlapping_hashes,
        "rights_not_verified": unknown_rights,
        "issues": issues, "technical_split_gate_pass": not issues,
        "rights_release_gate_pass": (not issues and unknown_rights == 0),
        "requires_perceptual_and_manual_scene_audit": True,
    }
