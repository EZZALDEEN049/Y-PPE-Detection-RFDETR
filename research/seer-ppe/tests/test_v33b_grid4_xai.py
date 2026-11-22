import unittest

import numpy as np

from seer_ppe.detection_match import Detection
from seer_ppe.progressive_xai import gaussian_blur_baseline, progressive_curve, stable_random_order
from tools.run_v33b_grid4_xai import (
    GRID_ROWS,
    GRID_COLS,
    MAX_ADDITIONAL_CALLS,
    build_grid4_importance_map,
    expected_call_count,
    grid4_cells,
)


class V33BGrid4Tests(unittest.TestCase):
    def setUp(self):
        self.image = np.full((32, 32, 3), 200, dtype=np.uint8)
        self.reference = Detection("Hard Hat", 16, 16, 8, 8, 0.9)

    def test_budget_formula_and_hard_ceiling(self):
        self.assertEqual(expected_call_count(0), 136)
        self.assertEqual(expected_call_count(10), 496)
        self.assertEqual(MAX_ADDITIONAL_CALLS, 496)
        with self.assertRaises(ValueError):
            expected_call_count(11)

    def test_grid4_cells_partition_odd_sized_image_exactly(self):
        height, width = 37, 53
        cells = grid4_cells(height, width)
        self.assertEqual(len(cells), 16)
        coverage = np.zeros((height, width), dtype=np.uint8)
        for cell in cells:
            coverage[cell["top"]:cell["bottom"], cell["left"]:cell["right"]] += 1
        self.assertTrue(np.all(coverage == 1))
        self.assertAlmostEqual(sum(cell["area_fraction"] for cell in cells), 1.0)

    def test_grid4_importance_map_uses_16_calls_and_keeps_target_drop(self):
        calls = []

        def predict(image):
            calls.append(1)
            if np.all(image[:8, :8, :] == 127):
                return []
            return [self.reference]

        importance, trials = build_grid4_importance_map(
            self.image, self.reference, predict
        )
        self.assertEqual(len(calls), 16)
        self.assertEqual(importance.shape, (GRID_ROWS, GRID_COLS))
        self.assertEqual(len(trials), 16)
        self.assertAlmostEqual(importance[0, 0], 0.9)
        self.assertTrue(np.isfinite(importance).all())

    def test_ambiguous_cell_is_not_imputed(self):
        calls = []

        def predict(image):
            calls.append(1)
            if np.all(image[:8, :8, :] == 127):
                return [
                    Detection("Hard Hat", 16, 16, 8, 8, 0.80),
                    Detection("Hard Hat", 16.1, 16, 8, 8, 0.79),
                ]
            return [self.reference]

        importance, trials = build_grid4_importance_map(
            self.image, self.reference, predict
        )
        self.assertEqual(len(calls), 16)
        self.assertTrue(np.isnan(importance[0, 0]))
        self.assertEqual(trials[0]["status"], "AMBIGUOUS")

    def test_grid4_progressive_curve_has_nine_interior_calls(self):
        blurred, _ = gaussian_blur_baseline(self.image)
        calls = []

        def predict(image):
            calls.append(1)
            return [self.reference]

        order = [(row, col) for row in range(4) for col in range(4)]
        points, auc = progressive_curve(
            self.image, blurred, self.reference, predict, order,
            direction="deletion", ordering_name="saliency",
            blurred_score=0.9, rows=4, cols=4, step_percent=10,
        )
        self.assertEqual(len(points), 11)
        self.assertEqual(len(calls), 9)
        self.assertIsNotNone(auc)
        self.assertAlmostEqual(auc, 1.0)
        fractions = [point.modified_fraction for point in points]
        self.assertTrue(all(b > a for a, b in zip(fractions, fractions[1:])))
        self.assertEqual(fractions[0], 0.0)
        self.assertEqual(fractions[-1], 1.0)

    def test_random_order_is_stable_and_has_16_unique_cells(self):
        first = stable_random_order("v33b-target", GRID_ROWS, GRID_COLS)
        second = stable_random_order("v33b-target", GRID_ROWS, GRID_COLS)
        self.assertEqual(first, second)
        self.assertEqual(len(first), 16)
        self.assertEqual(len(set(first)), 16)

    def test_upper_bound_decomposes_to_protocol_components(self):
        self.assertEqual(8 + 8 * 16 + 10 * 2 * 2 * 9, MAX_ADDITIONAL_CALLS)


if __name__ == "__main__":
    unittest.main()
