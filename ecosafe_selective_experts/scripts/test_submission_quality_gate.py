"""Only journal-format and verified aggregate checks, no real-image inference."""
from __future__ import annotations
import copy,json,unittest
from importlib.util import module_from_spec,spec_from_file_location
from pathlib import Path
sp=spec_from_file_location("editorial",Path(__file__).with_name("16_submission_quality_gate.py"))
quality=module_from_spec(sp)
sp.loader.exec_module(quality)

class SubmissionQualityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.man=quality.MAN.read_text(encoding="utf8")
        cls.hil=quality.HIL.read_text(encoding="utf8")
        cls.registry=json.loads(quality.AGG.read_text(encoding="utf8"))
        cls.fig1=quality.F1.read_text(encoding="utf8")
        cls.fig2=quality.F2.read_text(encoding="utf8")

    def test_real_repository_submission_gate_without_test_or_private_images(self):
        r=quality.evaluate(self.man,self.hil,self.registry,self.fig1,self.fig2)
        self.assertLessEqual(r["abstract_words"],250)
        self.assertEqual(r["highlights"],5)
        self.assertEqual(r["locked_experiment_cells"],12)
        self.assertEqual(r["checked_figure1_points"],12)
        self.assertEqual(r["checked_figure2_bars"],6)
        self.assertFalse(r["submission_approved"])

    def test_words_count(self):
        self.assertGreater(quality.check_abstract(self.man),160)

    def test_reject_oversized_abstract(self):
        huge=self.man.replace("## Abstract (journal-format candidate; development-only evidence)\n",
            "## Abstract (journal-format candidate; development-only evidence)\n"+"validation energy "*251+"\n",1)
        with self.assertRaises(ValueError):
            quality.check_abstract(huge)

    def test_reject_highlights_over_85(self):
        with self.assertRaises(ValueError):
            quality.check_highlights("Highlights\n"+("\u2022 "+("X"*86)+"\n")*5)

    def test_reject_two_highlights(self):
        with self.assertRaises(ValueError):
            quality.check_highlights("Highlights\n\u2022 one\n\u2022 two\n")

    def test_reject_duplicate_highlights(self):
        with self.assertRaises(ValueError):
            quality.check_highlights("Highlights\n\u2022 Same\n\u2022 Same\n\u2022 Different\n")

    def test_reject_unmeasured_energy_claim(self):
        bad=copy.deepcopy(self.registry)
        bad["real_energy_measured"]=True
        with self.assertRaises(ValueError):
            quality.check_data(bad)

    def test_reject_changed_critical_gt_support(self):
        bad=copy.deepcopy(self.registry)
        bad["rows"][0]["critical_ground_truth_objects"]=999
        with self.assertRaises(ValueError):
            quality.check_data(bad)

    def test_reject_missing_checkpoint_cell(self):
        bad=copy.deepcopy(self.registry)
        bad["rows"].pop()
        with self.assertRaises(ValueError):
            quality.check_data(bad)

    def test_reject_changed_recall_percent(self):
        bad=copy.deepcopy(self.registry)
        bad["rows"][1]["recall_percent"]+=4
        with self.assertRaises(ValueError):
            quality.check_data(bad)

    def test_reject_modified_chart_point(self):
        chart=self.fig1.replace("recall 30.72%","recall 31.72%",1)
        with self.assertRaises(ValueError):
            quality.check_figures(chart,self.fig2,quality.check_data(self.registry))

    def test_reject_modified_incremental_cost_figure(self):
        bad=self.fig2.replace("12.57  (+7 TP, +88 FP)","12.57  (+7 TP, +77 FP)")
        with self.assertRaises(ValueError):
            quality.check_figures(self.fig1,bad,quality.check_data(self.registry))

    def test_no_source_images_or_checkpoint_files_read(self):
        self.assertTrue(quality.MAN.is_file())
        self.assertTrue(quality.AGG.is_file())
        self.assertTrue(all(p.suffix in (".md",".txt",".json",".svg") for p in (quality.MAN,quality.HIL,quality.AGG,quality.F1,quality.F2)))

if __name__=="__main__":
    unittest.main()
