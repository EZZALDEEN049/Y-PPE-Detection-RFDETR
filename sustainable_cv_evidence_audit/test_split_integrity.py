"""Tests use synthetic byte strings, not actual photographs."""
import csv
import tempfile
import unittest
from pathlib import Path
from split_integrity import assess


def write_export(root, contents, layout="roboflow"):
    for split, files in contents.items():
        directory = root / split / "images" if layout == "roboflow" else root / "images" / split
        directory.mkdir(parents=True, exist_ok=True)
        for name, text in files.items():
            p = directory / name
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes(text.encode("utf-8"))


def write_mapping(path, triples):
    with path.open("w", newline="", encoding="utf-8") as f:
        rows = csv.writer(f)
        rows.writerow(["split", "file", "source_id"])
        rows.writerows(triples)


class SplitIntegrityTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.base = Path(tmp.name)
        self.a, self.b = self.base / "a", self.base / "b"
        content = {
            "train": {"t.jpg": "training"}, "valid": {"v.jpg": "validation"},
            "test": {"x.jpg": "test"}
        }
        write_export(self.a, content)
        write_export(self.b, content, layout="yolo")

    def test_matching_bytes_do_not_certify_comparison(self):
        r = assess(self.a, self.b)
        self.assertTrue(r["all_splits_exported_byte_multisets_identical"])
        self.assertTrue(r["no_detected_exact_byte_cross_split_overlap"])
        self.assertFalse(r["controlled_architecture_comparison_established"])

    def test_test_image_mismatch(self):
        (self.b / "images" / "test" / "x.jpg").write_bytes(b"different")
        self.assertFalse(assess(self.a, self.b)["all_splits_exported_byte_multisets_identical"])

    def test_exact_byte_leakage(self):
        (self.b / "images" / "test" / "x.jpg").write_bytes(b"training")
        r = assess(self.a, self.b)
        self.assertEqual(r["within_b_cross_split_byte_hash_overlap"]["train_vs_test"], 1)
        self.assertFalse(r["no_detected_exact_byte_cross_split_overlap"])

    def test_same_hash_extra_copy_not_ignored(self):
        (self.a / "train" / "images" / "extra.jpg").write_bytes(b"training")
        r = assess(self.a, self.b)
        self.assertFalse(r["all_splits_exported_byte_multisets_identical"])
        self.assertEqual(r["dataset_a"]["train"]["duplicate_copies_within_split"], 1)

    def test_source_id_leakage_hidden_by_augmentation(self):
        (self.b / "images" / "test" / "x.jpg").write_bytes(b"transformed")
        am, bm = self.base / "am.csv", self.base / "bm.csv"
        write_mapping(am, [("train", "t.jpg", "idA"), ("valid", "v.jpg", "idB"),
                           ("test", "x.jpg", "idC")])
        write_mapping(bm, [("train", "t.jpg", "idA"), ("valid", "v.jpg", "idB"),
                           ("test", "x.jpg", "idA")])
        r = assess(self.a, self.b, am, bm)
        self.assertEqual(r["source_id_audit"]["within_b_source_id_overlap"]["train_vs_test"], 1)
        self.assertFalse(r["source_id_audit"]["provenance_verified"])
        self.assertFalse(r["controlled_architecture_comparison_established"])

    def test_incomplete_source_map_rejected(self):
        am, bm = self.base / "am.csv", self.base / "bm.csv"
        write_mapping(am, [("train", "t.jpg", "idA")])
        write_mapping(bm, [("train", "t.jpg", "idA")])
        with self.assertRaises(ValueError):
            assess(self.a, self.b, am, bm)

    def test_one_source_map_rejected(self):
        with self.assertRaises(ValueError):
            assess(self.a, self.b, self.base / "am.csv", None)

    def test_matching_source_ids_remain_candidate_only(self):
        am, bm = self.base / "am.csv", self.base / "bm.csv"
        rows = [("train", "t.jpg", "idA"), ("valid", "v.jpg", "idB"),
                ("test", "x.jpg", "idC")]
        write_mapping(am, rows)
        write_mapping(bm, rows)
        r = assess(self.a, self.b, am, bm)
        self.assertTrue(all(r["source_id_audit"]["candidate_matching_source_membership"].values()))
        self.assertFalse(r["source_id_audit"]["provenance_verified"])

    def test_missing_split_rejected(self):
        (self.a / "test" / "images" / "x.jpg").unlink()
        with self.assertRaises(ValueError):
            assess(self.a, self.b)

    def test_ambiguous_layout_rejected(self):
        write_export(self.a, {"train": {"dup.jpg": "extra"}}, layout="yolo")
        with self.assertRaises(ValueError):
            assess(self.a, self.b)


if __name__ == "__main__":
    unittest.main()
