"""Synthetic tests for safe validation-only prediction chunks. No real images/models."""
import csv
import json
import tempfile
import unittest
from pathlib import Path
from importlib.util import spec_from_file_location, module_from_spec

SRC = Path(__file__).with_name("08_export_validation_chunks.py")
spec = spec_from_file_location("ecosafe_chunked", SRC)
module = module_from_spec(spec)
spec.loader.exec_module(module)


class ChunkSafetyTests(unittest.TestCase):
    def setUp(self):
        self.t = tempfile.TemporaryDirectory()
        self.addCleanup(self.t.cleanup)
        self.root = Path(self.t.name)
        self.out = self.root / "private"
        self.plan = {
            "model_id": "Y_YOLO_s17",
            "domain": "c",
            "expected_total_validation_images": 132,
            "chunk_index": 0, "chunk_size": 16, "start": 0, "end_exclusive": 2,
            "expected_checkpoint_sha256": "synthetic_lock_not_real",
            "frozen_manifest_sha256": "synthetic_manifest_not_real",
            "images": [self.root / "a.jpg", self.root / "b.jpg"],
        }

    def test_bad_weight_hash_must_fail_before_inference(self):
        p = self.root / "last.pt"
        p.write_bytes(b"not-real-weights")
        with self.assertRaises(ValueError):
            module.plan(self.root, "y", p, "Y_YOLO_s17", 16, 0)

    def test_unknown_model_and_invalid_chunk_rejected(self):
        p = self.root / "last.pt"
        with self.assertRaises(ValueError):
            module.plan(self.root, "y", p, "UNKNOWN", 16, 0)
        with self.assertRaises(ValueError):
            module.plan(self.root, "y", p, "Y_YOLO_s17", 0, 0)

    def test_valid_zero_detection_frames_still_exported(self):
        rows = [{"image_name": "a.jpg", "n_detections": 0},
                {"image_name": "b.jpg", "n_detections": 0}]
        metadata = module.write_private_result(self.out, self.plan, rows, [], "8.4.156")
        self.assertEqual(metadata["frames_exported"], 2)
        self.assertEqual(metadata["raw_detections_exported"], 0)
        files = list(self.out.glob("*"))
        self.assertEqual(len(files), 3)
        path = next(p for p in files if p.name.endswith("_frames.csv"))
        with path.open(newline="") as f:
            self.assertEqual(len(list(csv.DictReader(f))), 2)
        self.assertFalse(metadata["heldout_test_accessed"])

    def test_existing_chunk_refuses_overwrite(self):
        rows = [{"image_name": "a.jpg", "n_detections": 0},
                {"image_name": "b.jpg", "n_detections": 0}]
        module.write_private_result(self.out, self.plan, rows, [], "8.4.156")
        with self.assertRaises(FileExistsError):
            module.write_private_result(self.out, self.plan, rows, [], "8.4.156")

    def test_frame_and_detection_must_reconcile(self):
        frames = [{"image_name": "a.jpg", "n_detections": 0},
                  {"image_name": "b.jpg", "n_detections": 0}]
        det = [{"image_name": "a.jpg", "class_id": 6, "confidence": 0.5,
                "x1n": 0.1, "y1n": 0.1, "x2n": 0.3, "y2n": 0.3}]
        with self.assertRaises(ValueError):
            module.write_private_result(self.out, self.plan, frames, det, "8.4.156")

    def test_reordered_frame_refused(self):
        frames = [{"image_name": "b.jpg", "n_detections": 0},
                  {"image_name": "a.jpg", "n_detections": 0}]
        with self.assertRaises(ValueError):
            module.write_private_result(self.out, self.plan, frames, [], "8.4.156")

    def test_nan_coordinates_refused(self):
        det = [{"class_id": 6, "confidence": 0.6, "x1n": 0.1, "y1n": 0.1,
                "x2n": float("nan"), "y2n": 0.4}]
        with self.assertRaises(ValueError):
            module.validate_detections(det)

    def test_bad_class_id_refused(self):
        det = [{"class_id": 15, "confidence": 0.8, "x1n": 0.1, "y1n": 0.1,
                "x2n": 0.5, "y2n": 0.5}]
        with self.assertRaises(ValueError):
            module.validate_detections(det)


if __name__ == "__main__":
    unittest.main()
