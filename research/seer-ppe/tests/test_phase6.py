import unittest,numpy as np
from seer_ppe.occlusion import occlusion_explain
from seer_ppe.detection_match import Detection
from seer_ppe.hardware_gate import probe

class Phase6(unittest.TestCase):
 def setUp(self):
  self.im=np.zeros((16,16,3),dtype=np.uint8)
  self.ref=Detection('Hard Hat',8,8,8,8,.9)
 def test_all_matched_zero_drop(self):
  m,t=occlusion_explain(self.im,self.ref,lambda im:[self.ref],rows=2,cols=2)
  self.assertEqual(len(t),4);self.assertTrue(np.all(m==0))
 def test_one_lost_is_nan_not_zero(self):
  def f(x):return [] if x[0,0,0]==127 else [self.ref]
  m,t=occlusion_explain(self.im,self.ref,f,rows=2,cols=2)
  self.assertEqual(t[0].status,'LOST');self.assertTrue(np.isnan(m[0,0]))
 def test_real_score_change_sign(self):
  v=Detection('Hard Hat',8,8,8,8,.3)
  m,t=occlusion_explain(self.im,self.ref,lambda x:[v],rows=1,cols=1)
  self.assertAlmostEqual(m[0,0],.6)
 def test_same_class_iou_required(self):
  x=Detection('No Hard Hat',8,8,8,8,.7)
  m,t=occlusion_explain(self.im,self.ref,lambda y:[x],rows=1,cols=1)
  self.assertEqual(t[0].status,'LOST')
 def test_image_must_be_rgb(self):
  with self.assertRaises(ValueError): occlusion_explain(np.zeros((16,16),dtype=np.uint8),self.ref,lambda x:[])
 def test_grid_too_dense(self):
  with self.assertRaises(ValueError): occlusion_explain(self.im,self.ref,lambda x:[],rows=17)
 def test_hardware_gate_does_not_invent_energy(self):
  out=probe();self.assertFalse(out['physical_energy_measurement_performed']);self.assertIsNone(out['energy_joules_measured'])
if __name__=='__main__':unittest.main()
