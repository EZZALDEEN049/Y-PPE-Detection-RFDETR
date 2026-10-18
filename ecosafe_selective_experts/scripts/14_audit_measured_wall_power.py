#!/usr/bin/env python3
"""Offline EcoSafe wall-power trace audit (NO METER, NO measurements included).

Consumes externally instrumented, explicitly metadata-validated wall-AC
power samples. Never equates expert calls, CPU/GPU TDP or device estimates to
Joules. Not an MLPerf-certified measurement or a real-time instrument.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
import math
from pathlib import Path

REQUIRED_MANIFEST = {
    "source_type": "measured_wall_ac_power",
    "trace_provenance": "external_physical_power_meter",
    "unit": "watt",
    "time_unit": "second",
    "benchmark_mode": "single_stream_batch1",
    "energy_claim_status": "internal_unreviewed_measurement",
}
POLICIES = ("primary_only", "secondary_only", "always_joint", "selective")
CHECKPOINTS = ("last.pt", "best.pt")
DOMAINS = ("y", "c")


def sha256(path):
    digest=hashlib.sha256()
    with Path(path).open("rb") as h:
        for block in iter(lambda:h.read(1024*1024),b""):
            digest.update(block)
    return digest.hexdigest()


def parse_trace(file_path: Path):
    """Integrate timestamped power with trapezoids; timestamps must increase."""
    with file_path.open("r",encoding="utf-8",newline="") as handle:
        csv_reader=csv.DictReader(handle)
        if csv_reader.fieldnames != ["timestamp_s","power_w"]:
            raise ValueError("Expected exactly timestamp_s,power_w columns.")
        samples=[]
        for row in csv_reader:
            try:
                t=float(row["timestamp_s"])
                p=float(row["power_w"])
            except (ValueError,TypeError,KeyError) as exc:
                raise ValueError("Non-numeric wall power record.") from exc
            if not math.isfinite(t) or not math.isfinite(p) or t<0 or p<0:
                raise ValueError("Invalid/negative/NaN/infinite power sample.")
            if samples and t<=samples[-1][0]:
                raise ValueError("Timestamp must be strictly increasing.")
            samples.append((t,p))
    if len(samples)<2:
        raise ValueError("At least two measured power samples required.")
    duration=samples[-1][0]-samples[0][0]
    if duration<=0:
        raise ValueError("Nonpositive measurement duration.")
    energy=sum((t1-t0)*(p0+p1)/2 for (t0,p0),(t1,p1) in zip(samples,samples[1:]))
    avg=energy/duration
    return {"samples":len(samples),"duration_s":duration,"gross_energy_j":energy,
            "average_wall_power_w":avg,"max_gap_s":max(
                b[0]-a[0] for a,b in zip(samples,samples[1:]))}


def validate_manifest(info):
    if type(info) is not dict or any(info.get(k)!=v for k,v in REQUIRED_MANIFEST.items()):
        raise ValueError("Evidence-provenance manifest not explicitly physical wall measurement.")
    for field in ("meter_model","meter_identifier","system_identifier","run_identifier",
                  "software_stack","image_source_fingerprint","evaluation_commit_sha"):
        val=info.get(field)
        if type(val) is not str or not 2<=len(val)<=256 or val.strip()!=val:
            raise ValueError("Missing recorded meter/system/run/software source provenance.")
    for field,allowed in (("checkpoint_variant",CHECKPOINTS),
                          ("domain",DOMAINS),("policy",POLICIES)):
        if info.get(field) not in allowed:
            raise ValueError("Unexpected policy/checkpoint/domain factor.")
    if type(info.get("seed")) is not int or info["seed"] not in (17,42,2026):
        raise ValueError("Nonfrozen seed.")
    if type(info.get("frames_processed")) is not int or info["frames_processed"]<1:
        raise ValueError("Invalid processed frame count.")
    if info.get("start_state") not in ("preloaded_warm","including_cold_start"):
        raise ValueError("Unrecorded warm/cold start.")
    if type(info.get("router_overhead_included")) is not bool:
        raise ValueError("Router overhead must be stated explicitly.")
    if info["policy"]=="selective" and not info["router_overhead_included"]:
        raise ValueError("Selective-system energy missing router overhead.")
    if type(info.get("real_trace_authorized_for_research")) is not bool or not info["real_trace_authorized_for_research"]:
        raise ValueError("No recorded instrumentation and research authorization.")
    if info.get("claimed_mlperf_compliance") is not False:
        raise ValueError("This simple script is not MLPerf-certified.")
    return True


def summarise_power(trace, metadata, idle=None, trace_digest=None, idle_digest=None):
    validate_manifest(metadata)
    if trace["duration_s"]<=0 or trace["gross_energy_j"]<0:
        raise ValueError("No valid positive measurement duration.")
    frames=metadata["frames_processed"]
    result={
        "data_status":"user_supplied_instrumented_trace_not_independently_verified",
        "is_synthetic_unit_test_result":False,
        "mlperf_certified":False,
        "source_type":"measured_wall_ac_power",
        "run_id":metadata["run_identifier"],
        "system_identifier":metadata["system_identifier"],
        "checkpoint_variant":metadata["checkpoint_variant"],
        "domain":metadata["domain"],"seed":metadata["seed"],
        "policy":metadata["policy"],
        "start_state":metadata["start_state"],
        "router_overhead_included":metadata["router_overhead_included"],
        "frames_processed":frames,
        "trace_sha256":trace_digest,
        "n_power_samples":trace["samples"],
        "trace_duration_seconds":trace["duration_s"],
        "max_sample_gap_seconds":trace["max_gap_s"],
        "gross_wall_energy_joules":trace["gross_energy_j"],
        "gross_wall_joules_per_frame":trace["gross_energy_j"]/frames,
        "average_wall_power_watts":trace["average_wall_power_w"],
        "p95_latency_ms":None,
        "co2e_kg":None,
        "energy_savings_percentage":None,
        "power_trace_not_model_runtime_or_latency_measurement":True,
        "instrumented_energy_claim_requires_protocol_review":True,
        "warnings":[]
    }
    if trace["samples"]<30:
        result["warnings"].append("Very few power samples; review sampling coverage.")
    if trace["max_gap_s"]>1.1:
        result["warnings"].append("Power sampling gap >1.1 s; check sampler resolution and synchrony.")
    if idle is not None:
        idle_mean=idle["average_wall_power_w"]
        net=trace["gross_energy_j"]-idle_mean*trace["duration_s"]
        result.update({"idle_trace_sha256":idle_digest,
                       "idle_average_wall_power_watts":idle_mean,
                       "net_above_idle_joules":net,
                       "net_above_idle_joules_per_frame":net/frames})
        if net<0:
            result["warnings"].append(
                "Negative above-idle estimate; never clamp to zero or claim energy savings.")
        result["warnings"].append(
            "Idle subtraction is a separate incremental estimate; report gross wall energy as primary.")
    else:
        result.update({"idle_trace_sha256":None,"net_above_idle_joules":None,
                       "net_above_idle_joules_per_frame":None})
    return result


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--trace",type=Path,required=True,
                        help="Private timestamp_s,power_w CSV from physical wall meter.")
    parser.add_argument("--manifest",type=Path,required=True,
                        help="Explicitly authorized run metadata JSON.")
    parser.add_argument("--idle-trace",type=Path)
    parser.add_argument("--out",type=Path,required=True)
    args=parser.parse_args()
    try:
        if args.out.exists():
            raise ValueError("No overwriting previously produced research audit.")
        metadata=json.loads(args.manifest.read_text(encoding="utf-8"))
        validate_manifest(metadata)
        trace=parse_trace(args.trace)
        idle=parse_trace(args.idle_trace) if args.idle_trace is not None else None
        result=summarise_power(trace,metadata,idle,sha256(args.trace),
                               sha256(args.idle_trace) if args.idle_trace else None)
        args.out.parent.mkdir(parents=True,exist_ok=True)
        args.out.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
        print(json.dumps({"status":"internal_unreviewed_wall_meter_trace",
             "gross_wall_joules_per_frame":result["gross_wall_joules_per_frame"],
             "mlperf_certified":False,"co2e_kg":None}))
    except (OSError,ValueError,KeyError,TypeError) as exc:
        # Don't expose private benchmark paths, image identifiers or user metadata.
        raise SystemExit("ENERGY_EVIDENCE_REJECTED: "+type(exc).__name__)


if __name__=="__main__":
    main()
