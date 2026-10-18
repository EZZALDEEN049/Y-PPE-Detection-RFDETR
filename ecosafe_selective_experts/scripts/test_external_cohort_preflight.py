"""Synthetic-only external source eligibility tests. No real images or test scores."""
from importlib.util import module_from_spec,spec_from_file_location
from pathlib import Path
import unittest

spec=spec_from_file_location("cohort",Path(__file__).with_name("15_external_cohort_preflight.py"))
mod=module_from_spec(spec)
spec.loader.exec_module(mod)


def row(n,site):
    return dict(sha256=f"{n:064x}",original_family_key=f"family-{n}",
                site_key=site,camera_key=f"camera-{n}",session_key=f"session-{n}")


def fixtures():
    hist={"source_origin":"old_stage5","source_group_namespace":"original-source-keys",
          "records":[row(1,"OLD"),row(2,"OLD")]}
    a=row(11,"NEW_A")
    b=row(12,"NEW_B")
    a["gt_critical_count"]={"no_helmet":1,"no_gloves":2,"no_boots":1}
    b["gt_critical_count"]={"no_helmet":1,"no_gloves":1,"no_boots":2}
    new={"source_origin":"new_external_capture",
         "source_group_namespace":"original-source-keys",
         "rights_review":"research_use_documented",
         "object_geometry_review":"confirmed_comparable_no_helmet_no_gloves_no_boots",
         "annotation_quality_review":"completed_before_inference",
         "policy_lock":"independent_external_confirmatory_not_used_for_model_selection",
         "historical_stage6_excluded":True,
         "original_capture_attestation":"verified_with_dataset_steward",
         "records":[a,b]}
    return new,hist


class CohortTests(unittest.TestCase):
    def fail_when(self,edit):
        new,old=fixtures()
        edit(new,old)
        with self.assertRaises(ValueError):
            mod.evaluate(new,old)

    def test_fixture_is_metadata_only(self):
        a,b=fixtures()
        report=mod.evaluate(a,b)
        self.assertEqual(report["critical_gt_counts"]["no_boots"],3)
        self.assertEqual(report["verified_site_group_count"],2)
        self.assertFalse(report["claim_is_independently_validated"])
        self.assertTrue(report["no_model_inference"])
        self.assertNotIn("records",report)

    def test_known_old_hash(self):
        self.fail_when(lambda n,o:n["records"][0].update(sha256=o["records"][0]["sha256"]))
    def test_known_old_site(self):
        self.fail_when(lambda n,o:n["records"][0].update(site_key="OLD"))
    def test_known_old_camera(self):
        self.fail_when(lambda n,o:n["records"][0].update(camera_key="camera-1"))
    def test_single_site(self):
        self.fail_when(lambda n,o:n["records"][1].update(site_key="NEW_A"))
    def test_missing_session(self):
        self.fail_when(lambda n,o:n["records"][1].update(session_key="UNKNOWN"))
    def test_missing_boots_class(self):
        self.fail_when(lambda n,o:n["records"][0]["gt_critical_count"].pop("no_boots"))
    def test_non_equivalent_no_shoes_class(self):
        self.fail_when(lambda n,o:n["records"][0]["gt_critical_count"].update(no_shoes=1))
    def test_zero_support(self):
        self.fail_when(lambda n,o:[r["gt_critical_count"].update(no_boots=0) for r in n["records"]])
    def test_one_site_only_for_critical_class(self):
        self.fail_when(lambda n,o:n["records"][0]["gt_critical_count"].update(no_helmet=0))
    def test_bool_count(self):
        self.fail_when(lambda n,o:n["records"][0]["gt_critical_count"].update(no_boots=True))
    def test_missing_research_use_documentation(self):
        self.fail_when(lambda n,o:n.update(rights_review="not_checked"))
    def test_model_selection_goal(self):
        self.fail_when(lambda n,o:n.update(policy_lock="select_best_model"))
    def test_group_namespace_mismatch(self):
        self.fail_when(lambda n,o:n.update(source_group_namespace="new-random-namespace"))
    def test_bad_sha(self):
        self.fail_when(lambda n,o:n["records"][0].update(sha256="bad"))
    def test_duplicate_candidate_image_hash(self):
        self.fail_when(lambda n,o:n["records"][1].update(sha256=n["records"][0]["sha256"]))

if __name__=="__main__":
    unittest.main()
