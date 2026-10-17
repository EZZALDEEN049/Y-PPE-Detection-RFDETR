"""Synthetic ONLY: test wall-power trace auditing with fabricated input data.

Passing these tests is NOT evidence that real site power was measured.
"""
from __future__ import annotations
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import tempfile
import unittest

sp=spec_from_file_location("power",Path(__file__).with_name("14_audit_measured_wall_power.py"))
power=module_from_spec(sp)
sp.loader.exec_module(power)


def fake_manifest():
    data={
        "source_type":"measured_wall_ac_power",
        "trace_provenance":"external_physical_power_meter",
        "unit":"watt","time_unit":"second",
        "benchmark_mode":"single_stream_batch1",
        "energy_claim_status":"internal_unreviewed_measurement",
        "meter_model":"SYNTHETIC-METER-DO-NOT-REPORT",
        "meter_identifier":"synthetic-test-unit",
        "system_identifier":"synthetic-test-system",
        "run_identifier":"synthetic-test-run",
        "software_stack":"synthetic-test-stack",
        "image_source_fingerprint":"synthetic-test-data-lock",
        "evaluation_commit_sha":"synthetic-sha-not-production",
        "checkpoint_variant":"last.pt","domain":"y",
        "policy":"selective","seed":17,"frames_processed":10,
        "start_state":"preloaded_warm","router_overhead_included":True,
        "real_trace_authorized_for_research":True,
        "claimed_mlperf_compliance":False,
    }
    return data


class SyntheticWallPowerTests(unittest.TestCase):
    def setUp(self):
        self.t=tempfile.TemporaryDirectory()
        self.addCleanup(self.t.cleanup)
        self.root=Path(self.t.name)

    def trace(self,text):
        p=self.root/"synthetic.csv"
        p.write_text("timestamp_s,power_w\n"+text,encoding="utf-8")
        return power.parse_trace(p)

    def test_trapezoid_linear_samples(self):
        d=self.trace("0,10\n1,20\n2,30\n")
        self.assertEqual(d["samples"],3)
        self.assertAlmostEqual(d["gross_energy_j"],40)
        self.assertAlmostEqual(d["average_wall_power_w"],20)
        z=power.summarise_power(d,fake_manifest())
        self.assertAlmostEqual(z["gross_wall_joules_per_frame"],4)
        self.assertIsNone(z["co2e_kg"])
        self.assertIsNone(z["energy_savings_percentage"])
        self.assertFalse(z["mlperf_certified"])

    def test_negative_power_fails(self):
        with self.assertRaises(ValueError):
            self.trace("0,10\n1,-1\n")

    def test_duplicate_timestamp_fails(self):
        with self.assertRaises(ValueError):
            self.trace("0,10\n0,20\n")

    def test_nonfinite_power_fails(self):
        with self.assertRaises(ValueError):
            self.trace("0,10\n1,nan\n")

    def test_too_few_samples_fails(self):
        with self.assertRaises(ValueError):
            self.trace("0,10\n")

    def test_no_meter_provenance_fails(self):
        d=fake_manifest()
        d["source_type"]="estimated_gpu_tdp"
        with self.assertRaises(ValueError):
            power.validate_manifest(d)

    def test_no_selective_router_overhead_fails(self):
        d=fake_manifest()
        d["router_overhead_included"]=False
        with self.assertRaises(ValueError):
            power.validate_manifest(d)

    def test_explicit_no_mlperf_claim(self):
        d=fake_manifest()
        d["claimed_mlperf_compliance"]=True
        with self.assertRaises(ValueError):
            power.validate_manifest(d)

    def test_bool_frame_count_not_accepted(self):
        d=fake_manifest()
        d["frames_processed"]=True
        with self.assertRaises(ValueError):
            power.validate_manifest(d)

    def test_idle_subtraction_negative_not_clamped(self):
        d=self.trace("0,10\n1,10\n")
        idle=dict(d,average_wall_power_w=20)
        r=power.summarise_power(d,fake_manifest(),idle)
        self.assertEqual(r["net_above_idle_joules"],-10)
        self.assertTrue(any("Negative" in v for v in r["warnings"]))
        self.assertEqual(r["gross_wall_energy_joules"],10)

    def test_header_must_match_meter_trace_schema(self):
        p=self.root/"bad.csv"
        p.write_text("time_s,gpu_tdp\n0,10\n1,20\n",encoding="utf-8")
        with self.assertRaises(ValueError):
            power.parse_trace(p)


if __name__=="__main__":
    unittest.main()
