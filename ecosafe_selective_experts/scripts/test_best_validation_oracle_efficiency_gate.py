"""Synthetic-only, CPU, no private frames: privileged opportunity gate invariants."""
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import unittest

sp=spec_from_file_location(
    "best_oracle",Path(__file__).with_name("13_best_validation_oracle_efficiency_gate.py"))
gate=module_from_spec(sp)
sp.loader.exec_module(gate)


def pred(cls, confidence, xyxy):
    return {"class_id":cls,"confidence":confidence,"box":xyxy}


class OpportunityTests(unittest.TestCase):
    def setUp(self):
        self.a=(.1,.1,.3,.3)
        self.b=(.6,.6,.8,.8)

    def test_auc_ties_reversal_absent_classes(self):
        self.assertEqual(gate.auc_rank([False,True],[0,1]),1.0)
        self.assertEqual(gate.auc_rank([False,True],[1,0]),0.0)
        self.assertEqual(gate.auc_rank([False,True],[.5,.5]),.5)
        self.assertIsNone(gate.auc_rank([True,True],[.1,.2]))
        self.assertIsNone(gate.auc_rank([False,False],[.1,.2]))

    def test_nan_fails_closed(self):
        with self.assertRaises(ValueError):
            gate.auc_rank([True,False],[float("nan"),.5])

    def test_complete_frame_union_complementarity(self):
        from object_level_safety_oracle import matched_gt_indices
        from importlib.util import module_from_spec, spec_from_file_location
        sp=spec_from_file_location(
            "best_fusion",Path(__file__).with_name("12_best_validation_fusion_report.py"))
        fusion=module_from_spec(sp)
        sp.loader.exec_module(fusion)
        gt=[{"class_id":6,"box":self.a},{"class_id":7,"box":self.b}]
        a=pred(6,.9,self.a)
        b=pred(7,.8,self.b)
        result=gate.score_frame(gt,[a],[b],matched_gt_indices,fusion.class_nms)
        self.assertEqual(result["primary_tp"],1)
        self.assertEqual(result["joint_tp"],2)
        self.assertEqual(result["joint_fp"],0)
        report=gate.summarise([result])
        self.assertEqual(report["positive_delta_frames"],1)
        self.assertEqual(report["privileged_gt_oracle"]["secondary_calls_to_score_every_positive_gain_frame"],1)
        self.assertTrue(report["privileged_gt_oracle"]["not_deployable"])

    def test_false_alert_on_nonactionable_negative_frame(self):
        from object_level_safety_oracle import matched_gt_indices
        from importlib.util import module_from_spec, spec_from_file_location
        sp=spec_from_file_location(
            "best_fusion2",Path(__file__).with_name("12_best_validation_fusion_report.py"))
        fusion=module_from_spec(sp)
        sp.loader.exec_module(fusion)
        g=[{"class_id":6,"box":self.a}]
        first=gate.score_frame(g,[pred(6,.9,self.a)],[pred(8,.7,self.b)],
                               matched_gt_indices,fusion.class_nms)
        self.assertEqual(first["joint_tp"],first["primary_tp"])
        report=gate.summarise([first])
        self.assertEqual(report["positive_delta_frames"],0)
        self.assertEqual(report["joint_fp_change_outside_positive_delta_frames"],1)

    def test_gt_privileged_gate_avoids_harmful_nms_frame(self):
        rows=[{"gt":2,"primary_tp":1,"joint_tp":2,"concat_upper_tp":2,
               "primary_fp":0,"joint_fp":2,
               "uncertainty_all":.3,"uncertainty_safety":.4},
              {"gt":1,"primary_tp":1,"joint_tp":0,"concat_upper_tp":1,
               "primary_fp":0,"joint_fp":2,
               "uncertainty_all":.5,"uncertainty_safety":.6}]
        r=gate.summarise(rows)
        self.assertEqual(r["negative_delta_frames"],1)
        self.assertEqual(r["always_joint_tp"],2)
        self.assertEqual(r["privileged_gt_oracle"]["total_tp_by_only_escalating_positive_gain_frames"],3)
        self.assertEqual(r["privileged_gt_oracle"]["minimal_calls_to_match_total_always_joint_tp"],0)

    def test_fixed_grid_zero_cutoff_equals_always_joint(self):
        frames=[{"gt":2,"primary_tp":1,"joint_tp":2,"concat_upper_tp":2,
                 "primary_fp":0,"joint_fp":3,
                 "uncertainty_all":.3,"uncertainty_safety":.4},
                {"gt":1,"primary_tp":1,"joint_tp":1,"concat_upper_tp":1,
                 "primary_fp":0,"joint_fp":0,
                 "uncertainty_all":.8,"uncertainty_safety":1.0}]
        report=gate.summarise(frames)
        for method in ("uncertainty_all","uncertainty_safety"):
            grid=report["fixed_development_only_signal_threshold_grid"][method]
            self.assertEqual([r["threshold"] for r in grid],[0.,.25,.5,.75,1.])
            self.assertEqual(grid[0]["secondary_invocations"],2)
            self.assertEqual(grid[0]["operational_tp"],report["always_joint_tp"])
            self.assertEqual(grid[0]["operational_fp"],report["always_joint_fp"])
            self.assertTrue(grid[0]["no_posthoc_threshold_selected"])

    def test_no_safety_gt_is_not_a_recall_benchmark(self):
        rows=[{"gt":0,"primary_tp":0,"joint_tp":0,"concat_upper_tp":0,
               "primary_fp":0,"joint_fp":0,"uncertainty_all":1,"uncertainty_safety":1}]
        with self.assertRaises(ValueError):
            gate.summarise(rows)

    def test_same_rate_random_baseline_is_expectation_not_sample(self):
        rows=[{"gt":2,"primary_tp":1,"joint_tp":2,"concat_upper_tp":2,
               "primary_fp":0,"joint_fp":0,"uncertainty_all":0,"uncertainty_safety":.1},
              {"gt":1,"primary_tp":0,"joint_tp":0,"concat_upper_tp":0,
               "primary_fp":0,"joint_fp":0,"uncertainty_all":1,"uncertainty_safety":1}]
        z=gate.summarise(rows)
        self.assertAlmostEqual(z["same_rate_random_routing_expected_tp"],1.5)


if __name__=="__main__":
    unittest.main()
