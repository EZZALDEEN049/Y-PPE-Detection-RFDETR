"""Regression tests use tiny fake images and never download private exports."""
import tempfile
import unittest
from pathlib import Path
from paired_export_audit import run


def mk(root, split, fname, bytestr, annotation, layout="split", names=None):
    if layout == "split":
        i = root / split / "images" / fname
        l = root / split / "labels" / (Path(fname).stem + ".txt")
    else:
        i = root / "images" / split / fname
        l = root / "labels" / split / (Path(fname).stem + ".txt")
    i.parent.mkdir(parents=True, exist_ok=True)
    l.parent.mkdir(parents=True, exist_ok=True)
    i.write_bytes(bytestr.encode())
    if annotation is not None:
        l.write_text(annotation, encoding="utf-8")


class PairedExportTests(unittest.TestCase):
    def setUp(self):
        t = tempfile.TemporaryDirectory()
        self.addCleanup(t.cleanup)
        self.root = Path(t.name)
        self.a, self.b = self.root / "a", self.root / "b"
        for root, layout in ((self.a, "split"), (self.b, "yolo")):
            for split in ("train", "valid", "test"):
                mk(root, split, split + ".jpg", "distinct_" + split,
                   "0 0.5 0.5 0.3 0.3\n", layout=layout)
            (root / "data.yaml").write_text("nc: 2\nnames: [person, helmet]\n")
            
    def test_matching_exports_have_only_preflight_evidence(self):
        r = run(self.a, self.b, expected=(1, 1, 1))
        self.assertTrue(r["all_splits_exported_byte_multisets_identical"])
        self.assertTrue(r["ontology_class_order_strings_identical"])
        self.assertTrue(r["test_annotations_agree_for_matched_exported_image_bytes"])
        self.assertTrue(r["heldout_annotation_files_parsed_when_ontologies_same"])
        self.assertTrue(r["export_a_counts_match_expectations"])
        self.assertFalse(r["common_prediction_evaluator_executed"])
        self.assertFalse(r["controlled_architecture_accuracy_comparison_established"])

    def test_label_row_order_is_not_false_mismatch(self):
        lab = self.b / "labels" / "test" / "test.txt"
        lab.write_text("1 0.50 0.5 0.2 0.2\n0 0.5 0.5 0.3 0.3\n")
        (self.a / "test" / "labels" / "test.txt").write_text(
            "0 0.5 0.5 0.3 0.3\n1 0.5 0.5 0.20 0.2\n"
        )
        self.assertTrue(run(self.a, self.b)["test_annotations_agree_for_matched_exported_image_bytes"])

    def test_differing_boxes_are_flagged(self):
        (self.b / "labels" / "test" / "test.txt").write_text("0 0.5 0.5 0.2 0.2\n")
        r = run(self.a, self.b)
        self.assertEqual(r["matched_test_image_groups_with_annotation_mismatch"], 1)
        self.assertFalse(r["test_annotations_agree_for_matched_exported_image_bytes"])

    def test_class_order_mismatch_blocks_label_comparison(self):
        (self.b / "data.yaml").write_text("nc: 2\nnames: [helmet, person]\n")
        r = run(self.a, self.b)
        self.assertFalse(r["ontology_class_order_strings_identical"])
        self.assertFalse(r["heldout_annotation_files_parsed_when_ontologies_same"])

    def test_image_byte_difference_is_not_proof_of_distinct_scene(self):
        (self.b / "images" / "test" / "test.jpg").write_bytes(b"resized distinct_test")
        r = run(self.a, self.b)
        self.assertFalse(r["all_splits_exported_byte_multisets_identical"])
        self.assertEqual(r["matched_test_image_groups_with_annotation_comparison"], 0)
        self.assertFalse(r["controlled_architecture_accuracy_comparison_established"])

    def test_missing_test_annotation_fail_closed(self):
        (self.b / "labels" / "test" / "test.txt").unlink()
        r = run(self.a, self.b)
        self.assertFalse(r["heldout_annotation_files_parsed_when_ontologies_same"])
        self.assertEqual(r["heldout_annotation_parsing_error_type"], "ValueError")
        self.assertFalse(r["test_annotations_agree_for_matched_exported_image_bytes"])

    def test_invalid_class_id_fail_closed(self):
        (self.b / "labels" / "test" / "test.txt").write_text("17 0.5 0.5 0.3 0.3\n")
        r = run(self.a, self.b)
        self.assertFalse(r["heldout_annotation_files_parsed_when_ontologies_same"])
        self.assertEqual(r["heldout_annotation_parsing_error_type"], "ValueError")

    def test_nc_mismatch_rejected(self):
        (self.a / "data.yaml").write_text("nc: 3\nnames: [person, helmet]\n")
        with self.assertRaises(ValueError):
            run(self.a, self.b)


if __name__ == "__main__":
    unittest.main()
