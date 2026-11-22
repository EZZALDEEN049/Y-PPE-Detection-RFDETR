import unittest

import numpy as np

from tools.render_v34b_scientific_figures import build_target_arrays


class TestV34BScientificFigures(unittest.TestCase):
    def test_reconstructs_all_64_fine_cells_and_two_coarse_maps(self):
        cells = []
        expected = np.zeros((8, 8), dtype=float)
        for row in range(4):
            for col in range(4):
                children = []
                for dr in range(2):
                    for dc in range(2):
                        rr, cc = 2 * row + dr, 2 * col + dc
                        area = 1.0 / 64.0
                        density = float(rr * 8 + cc + 1)
                        children.append({
                            "row_8x8": rr, "col_8x8": cc,
                            "area_fraction": area,
                            "score_drop": density * area,
                        })
                        expected[rr, cc] = density
                cells.append({"fine_children": children})
        record = {
            "aligned_cells": cells,
            "direct_4x4_signed_drop_per_area_row_major": list(range(16)),
            "pooled_8x8_signed_drop_per_area_row_major": list(range(16, 32)),
        }
        fine, direct, pooled = build_target_arrays(record)
        np.testing.assert_array_equal(fine, expected)
        np.testing.assert_array_equal(direct, np.arange(16).reshape(4, 4))
        np.testing.assert_array_equal(pooled, np.arange(16, 32).reshape(4, 4))

    def test_rejects_missing_or_duplicate_fine_cell(self):
        record = {
            "aligned_cells": [
                {"fine_children": [
                    {"row_8x8": 0, "col_8x8": 0, "area_fraction": 1/64, "score_drop": 0.1}
                ] * 4}
            ] * 16,
            "direct_4x4_signed_drop_per_area_row_major": [0.0] * 16,
            "pooled_8x8_signed_drop_per_area_row_major": [0.0] * 16,
        }
        with self.assertRaises(AssertionError):
            build_target_arrays(record)


if __name__ == "__main__":
    unittest.main()
