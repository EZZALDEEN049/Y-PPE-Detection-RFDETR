import unittest

from tools.analyze_v34a_spatial_map_alignment import (
    cell_bounds,
    kendall_tau_b,
    rank_average,
    spearman,
    top_k_indices,
)


class TestV34ASpatialMapAlignment(unittest.TestCase):
    def test_average_ranks_for_ties(self):
        self.assertEqual(rank_average([2.0, 2.0, 5.0, 9.0]), [1.5, 1.5, 3.0, 4.0])

    def test_spearman_perfect_and_reverse_order(self):
        x = [1.0, 2.0, 3.0, 4.0]
        self.assertAlmostEqual(spearman(x, [10.0, 20.0, 30.0, 40.0]), 1.0)
        self.assertAlmostEqual(spearman(x, [40.0, 30.0, 20.0, 10.0]), -1.0)

    def test_spearman_uses_average_ranks_for_ties(self):
        self.assertAlmostEqual(spearman([1.0, 1.0, 3.0], [2.0, 2.0, 6.0]), 1.0)

    def test_kendall_tau_b_handles_ties(self):
        self.assertAlmostEqual(kendall_tau_b([1.0, 1.0, 2.0], [1.0, 2.0, 2.0]), 2.0 / (6.0 ** 0.5))

    def test_top_k_ties_resolve_row_major(self):
        self.assertEqual(top_k_indices([3.0, 3.0, 1.0, 0.0], 2), [0, 1])

    def test_each_4x4_cell_is_exact_union_of_four_8x8_cells(self):
        for height, width in ((667, 1000), (330, 500), (1365, 2048), (903, 736),
                              (236, 166), (736, 736), (1000, 1000)):
            for row in range(4):
                for col in range(4):
                    coarse = cell_bounds(height, width, 4, 4, row, col)
                    children = [
                        cell_bounds(height, width, 8, 8, 2 * row + dr, 2 * col + dc)
                        for dr in range(2) for dc in range(2)
                    ]
                    self.assertEqual(coarse, (
                        children[0][0], children[2][1],
                        children[0][2], children[1][3],
                    ))
                    self.assertEqual(
                        sum((b - t) * (r - l) for t, b, l, r in children),
                        (coarse[1] - coarse[0]) * (coarse[3] - coarse[2]),
                    )


if __name__ == "__main__":
    unittest.main()
