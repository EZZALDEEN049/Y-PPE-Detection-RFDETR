import unittest
import numpy as np

from seer_ppe.detection_match import Detection
from seer_ppe.progressive_xai import (
    CurvePoint, curve_auc, gaussian_blur_baseline, occlusion_importance_map,
    progressive_curve, rank_grid_cells, stable_random_order, target_score,
)


class V30ProgressiveXAITests(unittest.TestCase):
    def setUp(self):
        self.image = np.full((32, 32, 3), 200, dtype=np.uint8)
        self.reference = Detection("Hard Hat", 16, 16, 8, 8, 0.9)

    def test_lost_target_has_defined_zero_target_score(self):
        score, status, iou = target_score(self.reference, [])
        self.assertEqual(status, "LOST")
        self.assertEqual(score, 0.0)
        self.assertIsNone(iou)

    def test_ambiguous_target_is_not_imputed(self):
        a = Detection("Hard Hat", 16, 16, 8, 8, 0.8)
        b = Detection("Hard Hat", 16.1, 16, 8, 8, 0.7)
        score, status, _ = target_score(self.reference, [a, b])
        self.assertEqual(status, "AMBIGUOUS")
        self.assertIsNone(score)

    def test_importance_map_uses_target_score_drop(self):
        def predict(img):
            if np.all(img[:8, :8] == 127):
                return []
            return [self.reference]
        importance, trials = occlusion_importance_map(
            self.image, self.reference, predict, rows=4, cols=4)
        self.assertEqual(importance.shape, (4, 4))
        self.assertEqual(len(trials), 16)
        self.assertAlmostEqual(importance[0, 0], 0.9)
        self.assertAlmostEqual(importance[1, 1], 0.0)

    def test_rank_is_deterministic_and_positive_first(self):
        order = rank_grid_cells(np.array([[0.1, 0.9], [0.4, -0.2]]))
        self.assertEqual(order[0], (0, 1))
        self.assertEqual(order[-1], (1, 1))

    def test_random_control_is_stable(self):
        self.assertEqual(stable_random_order("target-1"), stable_random_order("target-1"))
        self.assertNotEqual(stable_random_order("target-1"), stable_random_order("target-2"))

    def test_blurred_baseline_shape_and_sigma(self):
        blurred, sigma = gaussian_blur_baseline(self.image)
        self.assertEqual(blurred.shape, self.image.shape)
        self.assertGreater(sigma, 0)
        self.assertEqual(blurred.dtype, np.uint8)

    def test_progressive_curve_endpoints_and_auc(self):
        baseline, _ = gaussian_blur_baseline(self.image, sigma=3)
        def predict(img):
            altered = np.mean(np.abs(img.astype(float) - self.image.astype(float)))
            score = max(0.0, 0.9 - altered / 255.0)
            return [Detection("Hard Hat", 16, 16, 8, 8, score)] if score > 0 else []
        order = [(r, c) for r in range(4) for c in range(4)]
        blurred_score, status, _ = target_score(self.reference, predict(baseline))
        self.assertNotEqual(status, "AMBIGUOUS")
        points, auc = progressive_curve(
            self.image, baseline, self.reference, predict, order,
            direction="deletion", ordering_name="test", blurred_score=blurred_score,
            rows=4, cols=4, step_percent=25)
        self.assertEqual(len(points), 5)
        self.assertAlmostEqual(points[0].normalized_score, 1.0)
        self.assertAlmostEqual(points[-1].normalized_score, min(1.0, blurred_score / 0.9))
        self.assertIsNotNone(auc)
        self.assertGreaterEqual(auc, 0.0)
        self.assertLessEqual(auc, 1.0)

    def test_auc_blocks_ambiguous_points(self):
        points = [
            CurvePoint("deletion", "x", 0.0, 0.0, 0.9, 1.0, "BASELINE", 1.0),
            CurvePoint("deletion", "x", 1.0, 1.0, None, None, "AMBIGUOUS", None),
        ]
        self.assertIsNone(curve_auc(points))


if __name__ == "__main__":
    unittest.main()
