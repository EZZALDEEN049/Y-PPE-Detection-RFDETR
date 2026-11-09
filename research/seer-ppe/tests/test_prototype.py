import math, unittest
import numpy as np
from seer_ppe.routing import RuntimeEvidence, ExperimentalPolicy, Route, SafetyState, route_case
from seer_ppe.safety_metrics import AdjudicatedCase, risk_counts, clopper_pearson_upper
from seer_ppe.energy import integrate_power
from seer_ppe.explanation_eval import attribution_fraction_in_mask, target_score_drop
from seer_ppe.preflight import ResearchGates

P=ExperimentalPolicy()
def e(**kwargs):
    x=dict(case_id="case",ppe_required=True,visible_person=True,ppe_worn=True,
           confidence=.95,association_status="unique",visibility="clear")
    x.update(kwargs)
    return RuntimeEvidence(**x)

class TestRouting(unittest.TestCase):
    def test_clear_strong_visible_unique(self):
        d=route_case(e(),P)
        self.assertEqual(d.route,Route.BASIC);self.assertEqual(d.safety_state,SafetyState.SUPPORTED_CLEAR)
    def test_unknown_policy_fails_closed(self):
        d=route_case(e(ppe_required=None),P)
        self.assertEqual(d.route,Route.REVIEW)
    def test_occlusion_fails_closed(self):
        d=route_case(e(visibility="occluded"),P)
        self.assertEqual(d.route,Route.REVIEW)
    def test_ambiguous_assignment_fails_closed(self):
        self.assertEqual(route_case(e(association_status="ambiguous"),P).route,Route.REVIEW)
    def test_no_person_does_not_clear(self):
        self.assertEqual(route_case(e(visible_person=False),P).route,Route.REVIEW)
    def test_low_confidence_review(self):
        self.assertEqual(route_case(e(confidence=.3),P).route,Route.REVIEW)
    def test_intermediate_requests_explain_but_no_clear(self):
        d=route_case(e(confidence=.7),P)
        self.assertEqual(d.route,Route.EXPLAIN)
        self.assertEqual(d.safety_state,SafetyState.UNCERTAIN_REVIEW)
    def test_not_required_requires_runtime_policy(self):
        d=route_case(e(ppe_required=False),P)
        self.assertEqual(d.safety_state,SafetyState.NOT_REQUIRED)
    def test_explicit_nonppe_flag(self):
        d=route_case(e(ppe_worn=False,explicit_non_ppe=True),P)
        self.assertEqual(d.safety_state,SafetyState.POTENTIAL_ALERT)
    def test_absence_does_not_equal_violation(self):
        self.assertNotEqual(route_case(e(ppe_worn=False,explicit_non_ppe=False),P).safety_state,SafetyState.POTENTIAL_ALERT)
    def test_invalid_confidence_rejected(self):
        with self.assertRaises(ValueError):e(confidence=2)

class TestMetrics(unittest.TestCase):
    def test_false_clear_and_omissions(self):
        rr=[AdjudicatedCase("a",True,True,SafetyState.SUPPORTED_CLEAR),
            AdjudicatedCase("b",True,False,SafetyState.UNCERTAIN_REVIEW),
            AdjudicatedCase("c",True,True,SafetyState.POTENTIAL_ALERT),
            AdjudicatedCase("d",False,True,SafetyState.SUPPORTED_CLEAR)]
        z=risk_counts(rr)
        self.assertEqual(z["verified_violations"],3)
        self.assertEqual(z["false_clear"],1)
        self.assertEqual(z["uncontained"],2)
    def test_no_violation_no_divzero(self):
        self.assertIsNone(risk_counts([])["false_clear_rate"])
    def test_exact_zero_error_bound(self):
        # 1 - alpha ** (1/n) at k=0
        self.assertAlmostEqual(clopper_pearson_upper(0,100),1-.05**(1/100),places=12)
    def test_zero_sample_not_certification(self):
        self.assertIsNone(clopper_pearson_upper(0,0))
    def test_invalid_ci(self):
        with self.assertRaises(ValueError):clopper_pearson_upper(2,1)

class TestEnergy(unittest.TestCase):
    def test_integrate_known_synthetic_power(self):
        r=integrate_power([(0,10),(.5,10),(1,10),(1.5,10),(2,10)],images=2,idle_watts=6)
        self.assertAlmostEqual(r.gross_joules,20)
        self.assertAlmostEqual(r.idle_adjusted_joules,8)
        self.assertAlmostEqual(r.joules_per_image,10)
    def test_reject_sparse_samples(self):
        with self.assertRaises(ValueError):integrate_power([(0,10),(6,10)],images=1)
    def test_reject_negative_power(self):
        with self.assertRaises(ValueError):integrate_power([(0,-1),(1,5)],images=1)

class TestExplanation(unittest.TestCase):
    def test_positive_attribution_mass(self):
        a=np.array([[1,0],[0,3]])
        m=np.array([[False,False],[False,True]])
        self.assertAlmostEqual(attribution_fraction_in_mask(a,m),.75)
    def test_zero_mass_unknown(self):
        self.assertIsNone(attribution_fraction_in_mask(np.zeros((2,2)),np.ones((2,2),bool)))
    def test_matched_score_drop(self):
        self.assertAlmostEqual(target_score_drop(.8,.5),.3)

class TestGates(unittest.TestCase):
    def test_requires_all_evidence(self):
        g=ResearchGates(True,False,False,False,False,False)
        self.assertFalse(g.ready_for_final_test)
        self.assertEqual(len(g.open_gates()),5)

if __name__=="__main__":unittest.main()
