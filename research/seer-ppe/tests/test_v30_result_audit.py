"""Synthetic, model-free integrity tests for V30 numeric evidence auditing."""
import json
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE / "tools"))
from audit_v30_xai_result import audit_results, AuditError  # noqa: E402


class V30ResultAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = json.loads(
            (HERE / "V30_FROZEN_TARGETS_2026-11-22.json").read_text(encoding="utf-8")
        )

    def build_result(self, one_eligible=False):
        targets = []
        for i, t in enumerate(self.manifest["targets"]):
            reference = float(t["frozen_baseline_confidence"])
            valid = one_eligible and i == 0
            grid = [[0.0 for _ in range(8)] for _ in range(8)] if valid else [
                [None for _ in range(8)] for _ in range(8)
            ]
            if valid:
                grid[0][0] = 0.1
            trials = []
            for row in range(8):
                for col in range(8):
                    drop = (0.1 if row == 0 and col == 0 else 0.0) if valid else None
                    trials.append({
                        "row": row,
                        "col": col,
                        "status": "MATCHED" if valid else "AMBIGUOUS",
                        "score_after": reference - drop if valid else None,
                        "score_drop": drop,
                        "matched_iou": 0.9 if valid else None,
                        "area_fraction": 1 / 64,
                    })
            blur = reference / 2
            curves = {}
            for ordering in ("saliency", "random", "inverse_saliency"):
                curves[ordering] = {}
                for direction in ("deletion", "insertion"):
                    if not valid:
                        curves[ordering][direction] = {
                            "status": "NOT_RUN_MAP_AMBIGUOUS_CELL",
                            "points": [],
                            "auc": None,
                        }
                    else:
                        pts = []
                        for step in range(11):
                            f = step / 10
                            score = reference * (1 - f / 2) if direction == "deletion" else blur * (1 + f)
                            pts.append({
                                "direction": direction,
                                "ordering": ordering,
                                "requested_fraction": f,
                                "modified_fraction": f,
                                "target_confidence": score,
                                "normalized_score": score / reference,
                                "match_status": "MATCHED",
                                "matched_iou": 0.7,
                            })
                        curves[ordering][direction] = {
                            "status": "EXECUTED", "points": pts,
                            "auc": 0.75 if direction == "deletion" else 0.75,
                        }
            targets.append({
                "target_id": t["target_id"],
                "image_key": t["image_key"],
                "filename": t["filename"],
                "asset_id": t["asset_id"],
                "split": t["split"],
                "target_class": t["target_class"],
                "arms": t["arms"],
                "baseline_confidence": reference,
                "blurred_endpoint": {"score": blur, "status": "MATCHED"},
                "map_status": "RANKABLE" if valid else "AMBIGUOUS_CELL",
                "curve_status": "EXECUTED" if valid else "NOT_RUN_MAP_AMBIGUOUS_CELL",
                "importance_map": grid,
                "occlusion_trials": trials,
                "curves": curves,
            })
        baselines = {
            x["image_key"]: {
                "asset_id": x["asset_id"],
                "split": x["split"],
                "filename": x["filename"],
                "local_file_sha256": "a" * 64,
            }
            for x in self.manifest["source_images"]
        }
        summary = {}
        for arm in ("A5", "A6"):
            summary[arm] = {
                "selected_slots": 8,
                "shared_target_slots": 6,
                "unique_target_slots": 2,
                "complete_target_count": 1 if one_eligible else 0,
                **{
                    (("inverse" if o == "inverse_saliency" else o) + "_" + d + "_auc_mean"):
                    (0.75 if one_eligible else None)
                    for o in ("saliency", "random", "inverse_saliency")
                    for d in ("deletion", "insertion")
                },
            }
        extra = 8 + 512 + (54 if one_eligible else 0)
        return {
            "schema_version": "seer-ppe/v30-actual-progressive-xai-results/v0.30",
            "status": "COMPLETED",
            "model_id": "altayyar-0oflt-lafos-qqauz/2",
            "inference_settings": {"confidence": 0.2, "overlap": 0.5},
            "baseline_images": baselines,
            "baseline_preflight_model_calls_already_executed": 8,
            "model_inference_calls_this_run": extra,
            "total_v30_model_inference_calls": extra + 8,
            "curve_eligible_targets": int(one_eligible),
            "target_results": targets,
            "A5_A6_summary": summary,
            "constraints": {
                "no_test_accessed": True,
                "claims_are_descriptive_only": True,
                "source_independence_verified": False,
                "worker_compliance_measured": False,
                "human_review_dispatched": False,
                "worker_safety_scoring_ready": False,
                "original_model_or_data_modified": False,
            },
        }

    def test_all_blocked_still_valid_descriptive_evidence(self):
        record = self.build_result()
        report = audit_results(self.manifest, record)
        self.assertEqual(report["audit_status"], "PASS_NUMERIC_INTEGRITY_ONLY")
        self.assertEqual(report["rankable_curve_targets"], 0)
        self.assertEqual(report["additional_actual_model_calls"], 520)
        self.assertEqual(len(report["blocked_curve_targets"]), 10)
        self.assertEqual(len(report["shared_target_ids"]), 6)

    def test_one_eligible_auc_recomputed(self):
        report = audit_results(self.manifest, self.build_result(one_eligible=True))
        self.assertEqual(report["rankable_curve_targets"], 1)
        self.assertEqual(report["additional_actual_model_calls"], 574)
        self.assertAlmostEqual(
            report["a5_a6"]["A5"]["mean_auc_by_ordering"]["saliency_deletion"],
            0.75,
        )

    def test_call_budget_mismatch_fails_closed(self):
        record = self.build_result(one_eligible=True)
        record["model_inference_calls_this_run"] += 1
        with self.assertRaises(AuditError):
            audit_results(self.manifest, record)

    def test_wrong_curve_auc_rejected(self):
        record = self.build_result(one_eligible=True)
        record["target_results"][0]["curves"]["saliency"]["deletion"]["auc"] = 0.5
        with self.assertRaises(AuditError):
            audit_results(self.manifest, record)

    def test_blocked_target_cannot_have_fake_auc(self):
        record = self.build_result()
        record["target_results"][0]["curves"]["saliency"]["deletion"]["auc"] = 0.8
        with self.assertRaises(AuditError):
            audit_results(self.manifest, record)

    def test_false_source_independence_claim_rejected(self):
        record = self.build_result()
        record["constraints"]["source_independence_verified"] = True
        with self.assertRaises(AuditError):
            audit_results(self.manifest, record)

    def test_missing_frozen_target_rejected(self):
        record = self.build_result()
        record["target_results"].pop()
        with self.assertRaises(AuditError):
            audit_results(self.manifest, record)


if __name__ == "__main__":
    unittest.main()
