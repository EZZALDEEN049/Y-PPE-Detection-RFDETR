"""Regression checks for public, source-group independence gate."""
import importlib.util
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "group_independence_gate.py"
spec = importlib.util.spec_from_file_location("group_independence_gate", SCRIPT)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
audit = mod.audit


def r(i, split, group, h, site="A"):
    return {"image_id": str(i), "site_id": site, "acquisition_group_id": group,
            "sha256": h * 64, "split": split}


class GroupGate(unittest.TestCase):
    def test_disjoint_clusters(self):
        self.assertEqual(audit([r(1,"train","camera1","a"), r(2,"test","camera2","b")])["status"], "PASS")

    def test_related_frames_rejected(self):
        x=audit([r(1,"train","video1","a"),r(2,"test","video1","b")])
        self.assertEqual(x["status"],"FAIL")
        self.assertEqual(len(x["acquisition_group_conflicts"]),1)

    def test_same_hash_across_splits_rejected(self):
        self.assertEqual(len(audit([r(1,"train","a","a"),r(2,"test","b","a")])["exact_image_hash_conflicts"]),1)

    def test_same_group_name_at_distinct_sites_allowed(self):
        self.assertEqual(audit([r(1,"train","video1","a","A"),r(2,"test","video1","b","B")])["status"],"PASS")

    def test_unknown_provenance_fails_closed(self):
        with self.assertRaisesRegex(ValueError,"unknown provenance"):
            audit([r(1,"test","unknown","a")])

    def test_invalid_sha_rejected(self):
        with self.assertRaisesRegex(ValueError,"invalid SHA"):
            audit([r(1,"test","camera1","z")])

    def test_duplicate_image_id_rejected(self):
        self.assertEqual(audit([r(1,"train","a","a"),r(1,"train","b","b")])["status"],"FAIL")

    def test_empty_rejected(self):
        with self.assertRaisesRegex(ValueError,"Empty manifest"):
            audit([])


if __name__ == "__main__":
    unittest.main()
