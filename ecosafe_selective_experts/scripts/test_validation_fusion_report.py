"""CPU-only synthetic invariants: policies, FP tradeoff and complete coverage."""
import tempfile
import unittest
from pathlib import Path
from importlib.util import spec_from_file_location, module_from_spec

spec=spec_from_file_location("fusion_report",Path(__file__).with_name("09_validation_fusion_report.py"))
m=module_from_spec(spec)
spec.loader.exec_module(m)


def obj(cls, box, confidence=0.9):
    return {"class_id":cls,"box":box,"confidence":confidence}


class ValidationFusionTests(unittest.TestCase):
    def setUp(self):
        self.a=obj(6,(0.1,0.1,0.3,0.3))
        self.b=obj(7,(0.6,0.6,0.8,0.8))
        self.gt={"frame.jpg":[{"class_id":6,"box":self.a["box"]},
                              {"class_id":7,"box":self.b["box"]}]}

    def test_object_level_union_detects_complementarity_hidden_by_fn_count(self):
        result=m.evaluate_validation(self.gt,{"frame.jpg":[self.a]},{"frame.jpg":[self.b]})
        self.assertEqual(result["critical_gt_objects"],2)
        self.assertEqual(result["policy_result"]["Y"]["tp"],1)
        self.assertEqual(result["policy_result"]["C"]["tp"],1)
        self.assertEqual(result["policy_result"]["joint_nms"]["tp"],2)
        self.assertEqual(result["policy_result"]["concat_oracle"]["tp"],2)
        self.assertEqual(result["oracle_additional_objects_vs_primary"]["Y"],1)
        self.assertEqual(result["legacy_fn_difference_additional_objects_proxy"]["Y"],0)
        self.assertEqual(result["improvement_frames_missed_by_legacy"]["Y"],1)
        self.assertFalse(result["heldout_test_accessed"])
        self.assertFalse(result["energy_measured"])

    def test_joint_nms_suppresses_same_class_high_overlap(self):
        a2=obj(6,(0.1,0.1,0.3,0.3),0.7)
        kept=m.class_nms([self.a,a2],0.70)
        self.assertEqual(len(kept),1)

    def test_joint_nms_keeps_different_class_even_when_boxes_identical(self):
        alt=obj(7,self.a["box"],0.9)
        kept=m.class_nms([self.a,alt],0.70)
        self.assertEqual(len(kept),2)

    def test_false_positive_tradeoff_reported(self):
        extra=obj(8,(0.35,0.35,0.55,0.55))
        result=m.evaluate_validation(self.gt,{"frame.jpg":[self.a,extra]},
                                      {"frame.jpg":[self.b]})
        self.assertEqual(result["policy_result"]["Y"]["fp"],1)
        self.assertEqual(result["policy_result"]["joint_nms"]["fp"],1)
        self.assertEqual(result["policy_result"]["joint_nms"]["tp"],2)

    def test_unmatched_image_ids_fail_closed(self):
        with self.assertRaises(ValueError):
            m.evaluate_validation(self.gt,{},{"frame.jpg":[self.b]})

    def test_absent_all_safety_ground_truth_fail_closed(self):
        with self.assertRaises(ValueError):
            m.evaluate_validation({"frame.jpg":[]},{"frame.jpg":[]},{"frame.jpg":[]})

    def test_empty_chunk_directory_fails_closed(self):
        with tempfile.TemporaryDirectory() as d:
            names=[f"image_{i:03d}.jpg" for i in range(132)]
            with self.assertRaises(ValueError):
                m.read_complete_chunks(Path(d),"C_YOLO_s17","c",names)

    def test_wrong_ontology_label_is_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"im.txt"
            p.write_text("11 0.5 0.5 0.2 0.2\n",encoding="utf-8")
            with self.assertRaises(ValueError):
                m.read_labels(p)

    def test_wrong_threshold_rejected(self):
        with self.assertRaises(ValueError):
            m.evaluate_validation(self.gt,{"frame.jpg":[self.a]},
                                  {"frame.jpg":[self.b]},conf=-1)


if __name__=="__main__":
    unittest.main()
