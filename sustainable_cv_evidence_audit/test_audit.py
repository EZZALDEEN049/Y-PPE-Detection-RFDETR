"""No external dependencies or accelerator needed."""
import copy
import json
import unittest
from pathlib import Path

from audit import assess, markdown, validate

DATA = json.loads((Path(__file__).resolve().parent / "evidence" / "records.json").read_text(encoding="utf-8"))


class AuditTests(unittest.TestCase):
    def test_initial_claim_gates_blocked(self):
        result = assess(DATA)
        self.assertFalse(result["controlled_accuracy_comparison_established"])
        self.assertFalse(result["controlled_energy_comparison_established"])
        self.assertFalse(result["comparative_deployment_claim_established"])
        self.assertIn("NOT ESTABLISHED", markdown(result))

    def test_two_distinct_models_preserved(self):
        models, _ = validate(DATA)
        self.assertEqual(len(models), 2)
        self.assertEqual(models[0]["reported_metrics_pct"]["map50"], 92.2)
        self.assertEqual(models[1]["reported_metrics_pct"]["map50"], 94.0)

    def test_duplicate_model_id_refused(self):
        data = copy.deepcopy(DATA)
        data["models"][1]["model_id"] = data["models"][0]["model_id"]
        with self.assertRaises(ValueError):
            assess(data)

    def test_bad_metric_refused(self):
        data = copy.deepcopy(DATA)
        data["models"][0]["reported_metrics_pct"]["map50"] = 101
        with self.assertRaises(ValueError):
            assess(data)

    def test_metrics_do_not_unlock_claim_gates(self):
        data = copy.deepcopy(DATA)
        data["comparison_controls"]["identical_heldout_test_membership_verified"] = True
        self.assertFalse(assess(data)["controlled_accuracy_comparison_established"])

    def test_energy_gate_requires_energy_measurements(self):
        data = copy.deepcopy(DATA)
        for key in data["comparison_controls"]:
            data["comparison_controls"][key] = True
        self.assertFalse(assess(data)["controlled_energy_comparison_established"])


if __name__ == "__main__":
    unittest.main()
