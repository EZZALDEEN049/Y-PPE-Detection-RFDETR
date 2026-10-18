# Construction-PPE — development-only confidence-threshold sensitivity across three seeds

**Date:** 2026-10-17. **Status:** exploratory fixed grid, no threshold selected; no new inference, no detector training, no held-out test images/labels accessed.

Existing low-confidence (0.001) frozen seed17/42/2026 Construction validation prediction CSVs were re-evaluated against the same 132 annotated validation images and 98 ground-truth safety objects. Both exact original last.pt model identities were locked for every seed; the seeds 42/2026 detection CSVs had checksum-validated manifests and complete frame coverage. Class-aware, one-to-one maximum cardinality safety-object matching used GT IoU >=0.50; joint class-aware NMS IoU 0.70.

**The confidence grid `[0.05,0.10,0.25,0.50]` is a development diagnostic, NOT a pre-registered sensitivity analysis or a threshold chosen for the final test.** Do not choose the best-looking row post hoc and present it as confirmatory.

| Confidence threshold | Seed17 joint TP / 98 | Seed42 joint TP / 98 | Seed2026 joint TP / 98 | Seed17 joint FP | Seed42 joint FP | Seed2026 joint FP |
|---|---:|---:|---:|---:|---:|---:|
| 0.05 | 17 | 19 | 14 | 105 | 97 | 107 |
| 0.10 | 14 | 16 | 14 | 89 | 83 | 90 |
| 0.25 | 13 | 13 | 14 | 67 | 68 | 74 |
| 0.50 | 8 | 9 | 13 | 51 | 55 | 62 |

At `conf=0.05`, joint-NMS critical-object recalls were 17.35%, 19.39%, and 14.29% across seeds. The corresponding fixed-point precisions were 13.93%, 16.38%, and 11.57%, illustrating the significant false-positive cost. Even the retrospective raw-concatenation matching oracle at `conf=0.05` matched only 18/98, 19/98 and 15/98 GT objects across the three seeds (18.37%, 19.39%, 15.31% recall). This is an upper bound **at this confidence floor and fixed matching convention**, not an upper bound on every possible model or future operating point.

**Technical crosscheck:** Results at conf=0.25 reproduce the independently archived three-seed NMS TP and FP table exactly; lowering/raising confidence used the same raw checkpoint outputs, not additional training or an alternate test set.

## Scientific implications

The low safety recall is **not explained away by the default 0.25 cutoff** within this screened confidence range: confidence 0.05 increases TP for some seeds but still leaves most critical violations undetected and increases false alerts. This is a GO/NO-GO warning for the intended safety-first adaptive inference contribution, NOT a claim that confidence 0.05 is optimal or that all other thresholds are impossible.

A manuscript claiming sustainability from fewer secondary invocations is not credible without both (i) an externally justified absolute safety standard and (ii) instrumented energy/latency measurements on deployment-like hardware. The current frozen checkpoint versions may be insufficient for worksite monitoring at the tested operating points, even if a router preserves their own weak reference recall. `best.pt` sensitivity, improved annotation governance and any different inference model would constitute *separately declared sensitivity or changed-model experiments*, not a silent replacement for the frozen last.pt primary results.

No CO2 savings, deployment suitability, Q1 statistical superiority, or cross-site population confidence intervals are established.
