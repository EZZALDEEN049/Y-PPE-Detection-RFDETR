# EcoSafe — hardware power and latency benchmark protocol (NOT EXECUTED)

**Draft date: 2026-10-18. Status: PROTOCOL ONLY, zero measured energy or CPU/GPU end-to-end deployment latency.** This is an independent engineering benchmark plan, not an MLPerf-compliant submission or a confirmation of reduced carbon emissions.

Official measurement principles: [MLCommons inference power measurement policy](https://github.com/mlcommons/inference_policies/blob/master/power_measurement.adoc) requires full-system measured power with tightly paired performance logging, documented SUT and replicability. We will use these principles as guidance **without claiming MLPerf certification**. Never derive actual J/image from YOLO call count, TDP, time×claimed nominal watts or GPU telemetry alone and never describe a test lacking a meter as a measured wall-power benchmark.

## Scope: candidate experimental factors

- **Hardware:** one named fixed real CPU / edge GPU / system (SUT) with model, OS, exact driver/kernel, Python, PyTorch and Ultralytics 8.4.156, CPU threads, acceleration backend, RAM/VRAM, thermal governor, power management, CUDA/cuDNN, initial device temperature where available.
- **Power sensor:** an authorized external AC wall-power analyzer or calibrated metering hardware measuring the FULL running system, including CPU/GPU, memory, networking if active, fans, router and model initialization. Record meter make/model, calibration date if known, acquisition sampling rate, time sync and anonymized serial. GPU package-power telemetry is a **separate proxy**, never label it wall energy.
- **Inputs:** original permitted **validation-only** frames or independently authorized performance samples, locked by content hashes and same fixed traversal order for each policy. Do not use held-out test frames just to tune hardware inference/call rates. Do not publish private worker images or their identifiers.
- **Precision / operating point:** batch size one; freeze one model pair seed, domain, last.pt vs best.pt, 640 input, NMS/confidence, router rules; report the complete factor combination, not a cherry-picked faster path. The existing risk heuristic is *not safety-validated*.
- **Policies:** primary only, secondary only, **always both + same-class NMS** (real fused baseline), and actual selective primary-first call + identical merger when escalated. Do NOT replace primary predictions with secondary to simulate always-both. For any data-dependent router, include all routing computation, scheduling and model activation/loading overhead.

## Before actual measurement (NOT DONE)

1. Confirm written access to suitable meter, machine and ethically authorized images; log its meter model and calibration status. Obtain permission for publication of anonymized power trace-derived aggregates.
2. Install/check exact software and checkpoint/data integrity; record branch commit, exact model SHA and frozen input manifest. Benchmark both cold-start (models loaded inside monitored window) and steady warm-start (preloaded) **separately**.
3. Agree in advance number of repeated independent runs (recommend >=5 per policy and domain when practical), blocked or randomized order, input order, device power mode, cooldown/warmup, batch settings and number of frames. Aim for sustained traced intervals with adequate time sampling; measurement duration and sampling rate must be declared. Do not invent actual measurements.
4. Collect for each **same** run: external wall trace as CSV \`timestamp_s,power_w\` (strictly increasing measured elapsed or synchronized seconds), execution run start/end timestamps, processed frame count, per-frame *actual* end-to-end latency on device including routing/fusion, if instrumentable, and a separately measured idle trace from same hardware and setting. Preserve meter time alignment and max sampling gaps.
5. Capture memory high-water mark / host RSS, GPU peak VRAM if available, 50th/95th/99th-percentile *end-to-end* latency, throughput images/sec, and the *actual* second-expert invocation fraction per run. Use matched workload and identical duration rules across policies and fixed heat/power states; raw timings from unrelated machines are invalid direct comparisons.
6. Store raw traces and system identifiers privately. Run \`scripts/14_audit_measured_wall_power.py\` only with a genuine full-system physical meter trace and explicit provenance manifest. The script integrates the trace by the trapezoidal rule to provide **gross J/image** and optionally **net-above-idle J/image**. Gross is primary. The tool **does not** instrument a device, certify meter calibration, infer p95 latency or compute carbon.
7. Compare repeated-run paired means/medians and ranges across policies on the same instrument; do not combine lowest-energy run with fastest run from a different order. Report effect of cold loading, model background residency and idle energy honestly; if the selector starts the second model too often, the expected energy reduction may be zero or negative.
8. **CO2e is out of scope** until power evidence exists, system boundary (wall/system/network) is explicit, locale/date/time electricity carbon factor has a reliable source and the uncertainty of each factor is reported. Never back-compute emissions from expert invocations or name an arbitrary intensity without provenance.

## Trace evidence validator

\`scripts/14_audit_measured_wall_power.py\` supports:

\`\`\`bash
python ecosafe_selective_experts/scripts/14_audit_measured_wall_power.py \
  --trace /private/meter_run_001.csv \
  --idle-trace /private/idled_same_system.csv \
  --manifest /private/meter_run_001_metadata.json \
  --out /private/audits/meter_run_001_internal.json
\`\`\`

The manifest MUST explicitly record the values validated by \`REQUIRED_MANIFEST\` in the script plus **actual** \`meter_model\`, \`meter_identifier\`, \`system_identifier\`, \`run_identifier\`, \`software_stack\`, \`image_source_fingerprint\`, \`evaluation_commit_sha\`, \`checkpoint_variant\`, \`domain\`, \`policy\`, \`seed\`, \`frames_processed\`, \`start_state\`, \`router_overhead_included\`, \`real_trace_authorized_for_research=true\`, \`claimed_mlperf_compliance=false\`. These are integrity and provenance declarations, **not proof of calibration**. Synthetic traces MUST NOT be passed off as measured traces.

Input-only CSV sample schema, with deliberately **no example watt readings to avoid fabricated results**:

\`\`\`csv
timestamp_s,power_w
\`\`\`

The analyzer fails closed on non-monotone timestamps, non-numeric, NaN or negative watt records, absent permission/provenance, missing router overhead and attempts to label the run certified MLPerf. It rejects output overwrites, flags sparse/gappy power samples, clearly separates negative above-idle results from gross wall energy, and never produces a CO2e or energy-saving percentage automatically. Its synthetic unit tests only verify formulas, **not actual SUT efficiency**.

## Scientific integrity and current results

No physical watt trace, named metered hardware, idle baseline, p95 real end-to-end timing or loaded-model scheduling trace was supplied or produced. Thus **J/image, watts, hardware speedup, inferred avoided energy and CO2e are currently unavailable**. Existing EcoSafe PR#16 predicts only computational *invocation rates* and fixed-IoU violation detections; claims of measured sustainability remain **NO-GO**. Any genuine wall-meter experiment must be separately authorized and timestamped when executed; source-group and absolute safety validation remain separate prerequisites.
