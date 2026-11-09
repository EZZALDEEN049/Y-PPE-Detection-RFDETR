import unittest
from seer_ppe.independence import ImageRecord,audit_split_independence
from seer_ppe.detection_match import Detection,box_iou,match_target

H1="a"*64;H2="b"*64

def rec(i,s,g,h,rights="VERIFIED"):
    return ImageRecord(i,s,g,h,rights)

def det(c="Hard Hat",x=100,y=100,w=30,h=30,score=.91):
    return Detection(c,x,y,w,h,score)

class TestIndependence(unittest.TestCase):
    def test_valid_distinct_groups(self):
        z=audit_split_independence([rec('a','train','cam1',H1),rec('b','test','cam2',H2)])
        self.assertTrue(z['technical_split_gate_pass'])
        self.assertTrue(z['requires_perceptual_and_manual_scene_audit'])
    def test_reject_cross_split_group(self):
        z=audit_split_independence([rec('a','train','video1',H1),rec('b','test','video1',H2)])
        self.assertFalse(z['technical_split_gate_pass'])
        self.assertIn('video1',z['overlapping_acquisition_groups'])
    def test_reject_cross_split_exact_bytes(self):
        z=audit_split_independence([rec('a','train','cam1',H1),rec('b','test','cam2',H1)])
        self.assertFalse(z['technical_split_gate_pass'])
        self.assertIn(H1,z['overlapping_hashes'])
    def test_reject_unknown_group(self):
        self.assertFalse(audit_split_independence([rec('a','test','unknown',H1)])['technical_split_gate_pass'])
    def test_rights_separately_from_integrity(self):
        z=audit_split_independence([rec('a','valid','cam1',H1,'RESTRICTED')])
        self.assertTrue(z['technical_split_gate_pass'])
        self.assertFalse(z['rights_release_gate_pass'])
    def test_empty_not_pass(self):
        self.assertFalse(audit_split_independence([])['technical_split_gate_pass'])
    def test_invalid_hash_rejected(self):
        self.assertFalse(audit_split_independence([rec('a','train','cam1','123')])['technical_split_gate_pass'])
    def test_duplicate_image_id_rejected(self):
        z=audit_split_independence([rec('same','train','cam1',H1),rec('same','valid','cam2',H2)])
        self.assertIn('same:duplicate_image_id',z['issues'])

class TestDetectionMatch(unittest.TestCase):
    def test_iou_identical(self):
        self.assertEqual(box_iou(det(),det()),1)
    def test_iou_disjoint(self):
        self.assertEqual(box_iou(det(),det(x=400)),0)
    def test_match_same_class(self):
        m=match_target(det(),[det(score=.5)])
        self.assertEqual(m.status,'MATCHED');self.assertEqual(m.score_after,.5)
    def test_reject_other_class(self):
        self.assertEqual(match_target(det(),[det(c='Goggles')]).status,'LOST')
    def test_reject_low_iou(self):
        self.assertEqual(match_target(det(),[det(x=130)]).status,'LOST')
    def test_ambiguous_matches(self):
        self.assertEqual(match_target(det(),[det(score=.5),det(score=.7)]).status,'AMBIGUOUS')
    def test_lost_score_is_none(self):
        self.assertIsNone(match_target(det(),[]).score_after)
    def test_bad_detection(self):
        with self.assertRaises(ValueError): det(w=0)
    def test_bad_threshold(self):
        with self.assertRaises(ValueError): match_target(det(),[],min_iou=1.5)

if __name__=='__main__':unittest.main()
