import unittest
from object_level_safety_oracle import frame_oracle, iou, matched_gt_indices


def obj(cid, b):
    return {"class_id": cid, "box": b}


class ObjectLevelOracleTests(unittest.TestCase):
    def test_different_missed_objects_cancel_in_legacy_counts(self):
        g = [
            obj(6, (0.1, 0.1, 0.3, 0.3)),
            obj(6, (0.6, 0.6, 0.8, 0.8)),
        ]
        p = [g[0]]
        s = [g[1]]
        r = frame_oracle(g, p, s)
        self.assertEqual((r["primary_fn"], r["secondary_fn"]), (1, 1))
        self.assertEqual(r["legacy_recovery_by_fn_count_difference"], 0)
        self.assertEqual(r["concat_oracle_fn"], 0)
        self.assertEqual(r["object_recovery_vs_primary_count"], 1)
        self.assertEqual(r["secondary_exclusively_recovers_primary_missed_objects"], 1)

    def test_no_new_recovery_if_same_object_matched(self):
        g = [obj(6, (0.1, 0.1, 0.3, 0.3)), obj(7, (0.6, 0.6, 0.8, 0.8))]
        r = frame_oracle(g, [g[0]], [g[0]])
        self.assertEqual(r["object_recovery_vs_primary_count"], 0)

    def test_wrong_class_never_matched(self):
        g = [obj(6, (0.1, 0.1, 0.3, 0.3))]
        p = [obj(7, (0.1, 0.1, 0.3, 0.3))]
        self.assertEqual(frame_oracle(g, p, [])["primary_fn"], 1)

    def test_nonsafety_gt_not_counted(self):
        g = [obj(0, (0.1, 0.1, 0.3, 0.3))]
        r = frame_oracle(g, [], [])
        self.assertEqual(r["gt_safety_objects"], 0)
        self.assertEqual(r["routing_recovery_positive"], 0)

    def test_iou_exact(self):
        self.assertAlmostEqual(iou((0.0, 0.0, 0.5, 0.5), (0, 0, 0.5, 0.5)), 1.0)

    def test_greedy_iou_can_miss_second_object(self):
        # One detection can match both objects, the second only GT 1:
        # max-cardinality must recover two GTs.
        g = [obj(6, (0.10, 0.10, 0.50, 0.50)),
             obj(6, (0.30, 0.10, 0.70, 0.50))]
        p = [obj(6, (0.20, 0.10, 0.60, 0.50)),
             obj(6, (0.37, 0.10, 0.77, 0.50))]
        # overlap: primary pred0 ~ .60 both; pred1 ~ .23 with GT0, .70 with GT1
        self.assertEqual(len(matched_gt_indices(g, p, threshold=0.5)), 2)

    def test_invalid_nonfinite_box_rejected(self):
        with self.assertRaises(ValueError):
            frame_oracle([obj(6, (0.1, 0.1, float("nan"), 0.4))], [], [])

    def test_no_operational_fusion_claim(self):
        g = [obj(8, (0.1, 0.1, 0.3, 0.3))]
        self.assertFalse(frame_oracle(g, [g[0]], [])["actual_merged_operational_predictions_evaluated"])


if __name__ == "__main__":
    unittest.main()
