"""Artificial fixed-signal tests. No private data, checkpoints or held-out test."""
import importlib.util
import unittest
from pathlib import Path

p=Path(__file__).with_name("10_validation_routing_frontier.py")
s=importlib.util.spec_from_file_location("routing_frontier",p)
m=importlib.util.module_from_spec(s)
s.loader.exec_module(m)


def obj(cid,box,conf):
    return {"class_id":cid,"box":box,"confidence":conf}


class RoutingFrontierTests(unittest.TestCase):
    def setUp(self):
        self.a=obj(6,(0.1,0.1,0.3,0.3),.9)
        self.b=obj(7,(0.6,0.6,0.8,0.8),.5)
        self.gt={"frame1":[{"class_id":6,"box":self.a["box"]},
                           {"class_id":7,"box":self.b["box"]}],
                 "frame2":[{"class_id":6,"box":self.a["box"]}]}
        self.primary={"frame1":[self.a],"frame2":[]}
        self.secondary={"frame1":[self.b],"frame2":[self.a]}

    def test_true_always_run_both_includes_primary(self):
        r=m.calculate_frontier(self.gt,self.primary,self.secondary)
        self.assertEqual(r["primary_alone"]["tp"],1)
        self.assertEqual(r["always_run_both"]["tp"],3)
        self.assertEqual(r["always_run_both"]["expert_executions_proxy_per_image"],2)
        self.assertFalse(r["router_trained"])
        self.assertFalse(r["inference_energy_measured"])

    def test_primary_only_score_no_gt_or_secondary(self):
        signal=m.primary_score([self.a],"all_confidence_uncertainty")
        self.assertAlmostEqual(signal,.1)
        self.assertEqual(m.primary_score([],"safety_confidence_uncertainty"),1.0)

    def test_threshold_one_recovers_only_zero_primary_predictions(self):
        r=m.calculate_frontier(self.gt,self.primary,self.secondary)
        row=r["frontiers"]["all_confidence_uncertainty"][-1]
        self.assertEqual(row["escalated_frames"],1)
        self.assertEqual(row["tp"],2)
        self.assertAlmostEqual(row["escalation_rate"],.5)

    def test_zero_threshold_is_always_both(self):
        r=m.calculate_frontier(self.gt,self.primary,self.secondary)
        first=r["frontiers"]["all_confidence_uncertainty"][0]
        self.assertEqual(first["tp"],r["always_run_both"]["tp"])
        self.assertEqual(first["fp"],r["always_run_both"]["fp"])

    def test_mismatched_frames_rejected(self):
        with self.assertRaises(ValueError):
            m.calculate_frontier(self.gt,{"frame1":[]},self.secondary)

    def test_unknown_primary_signal_rejected(self):
        with self.assertRaises(ValueError):
            m.primary_score([self.a],"GT_ORACLE")

    def test_random_reference_is_expected_only(self):
        r=m.calculate_frontier(self.gt,self.primary,self.secondary)
        for row in r["frontiers"]["all_confidence_uncertainty"]:
            self.assertTrue(0<=row["expected_random_routing_recall_at_same_rate"]<=1)


if __name__=="__main__":
    unittest.main()
