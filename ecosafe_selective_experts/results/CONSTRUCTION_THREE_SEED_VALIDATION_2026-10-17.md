# EcoSafe — Construction-PPE validation: all three frozen seeds

**Analysis date:** 2026-10-17. **STATUS: development-only evidence, NOT a held-out test or energy benchmark.**

## Frozen resources and validation

- Data: Construction-PPE-h9-v2, 132 validation images, 27 safety-positive frames and 98 safety GT boxes; class breakdown: 43 no_helmet, 51 no_gloves, 4 no_boots.
- Frozen manifest SHA-256: `59469299ba67355dbcb0e725851f73d244a7ad6e93522d44601be3c8323d3c14`.
- Six Stage 5 last.pt checkpoint SHA-256 digests were independently verified against the immutable checkpoint lock; three seed-matched Y-vs-Construction pairs were run.
- Detector input 640, export confidence 0.001, individual NMS IoU 0.70; operating confidence 0.25; class-aware one-to-one GT matching IoU >=0.50; candidate operational class-aware joint NMS IoU 0.70.
- Seeds 42 and 2026: each model exported **all 132** frames in 9 integrity-checked 16-image chunks (including final 4-frame chunk); each chunk CSV rehashed and compared with private manifest; absent detections correctly retained as zero-frame records. A separate NetworkX implementation agreed with all **528/528** frame/policy matching cardinalities **per seed** (1,056/1,056 in total). The preceding seed17 Construction pilot reported 396 independently agreeing matched cardinalities, with a previously verified zero-detection frame.
- No test images, training changes, private filenames/GT/crops or model binaries were written to the public repository.

## Fixed-confidence safety detection (object-level)

**Same set of 98 annotated safety objects used for every seed.** Entries are TP / 98 unless otherwise noted.

| Seed | Y model TP | Construction model TP | Joint NMS TP | Concat oracle TP | Joint NMS FP | Gain over best single TP |
|---|---:|---:|---:|---:|---:|---:|
| 17 | 7 | 8 | 13 | 14 | 67 | +5 |
| 42 | 9 | 5 | 13 | 13 | 68 | +4 |
| 2026 | 8 | 7 | 14 | 14 | 74 | +6 |

Per-seed joint-NMS recall: **13.27%, 13.27%, 14.29%**, respectively.
Descriptive three-seed mean joint-NMS recall: **13.61%** (SD **0.59 percentage points**, computed over the three completed training seeds, **not** independent sites). Mean Y-expert recall: **8.16%**; mean Construction-expert recall: **6.80%**.

Joint-NMS precision: **16.25%, 16.05%, 15.91%** for seeds 17, 42, 2026 (mean 16.07%). In other words, complementary TP recovery came at a large false-alarm cost. Mean values are **descriptive repeated-model summaries on the same validation cases**, not a population safety estimate.

### Rare-class warning

Construction validation has **only four** no_boots GT objects. Joint NMS matched 1 no_boots object for seed42 and **zero** for seed2026. This alone invalidates broad assertions of protection against all PPE violation types. Aggregate improvements cannot substitute for class-specific safety criteria and uncertainty.

## Contrast with Y-PPE domain: seed 17 only

In 356 frozen Y-PPE validation images containing 345 safety GT objects, Y expert = 106 TP, Construction expert = 1 TP, and joint NMS = 106 TP. Joint NMS added two FPs relative to Y alone, with **no new matched safety GT on any of 356 images**. No claim is yet possible for seeds 42 or 2026 on this second development domain.

This is a **domain- and direction-dependent complementarity hypothesis**, not evidence that an adaptive router has achieved a performance/compute frontier or generalizes to field sites.

## Exploratory frame bootstrap (not source-group uncertainty)

A separate 5,000-resample *paired image-level bootstrap* explored the difference in recall (joint NMS minus individual expert) on Construction development data. For seed17, joint minus Construction: +5.10 percentage points, nominal 95% frame percentile interval [0.00, 9.40] percentage points. For seed42, joint minus Y: +4.08 points, interval [0.97, 7.81] points. These intervals are **not valid source/site-cluster confidence intervals**, because the frozen manifest lacks adjudicated independent scene/source group IDs. They are development diagnostics only and must not underpin claims of non-inferiority or statistical generalization.

## GO / MODIFY / NO-GO scientific implications

- **Descriptive oracle gate:** some secondary detections do recover safety objects on Construction in all three seeds (+4 to +6 matched objects over the best individual model), but absolute joint recall is around 13–14%. This is inadequate for a deployment-level safety claim.
- **Router hypothesis:** basic primary-confidence-only escalation did not yet deliver substantial reduction in expert execution while retaining the already weak fused reference. No router is trained or selected.
- **Sustainability gate:** no instrumented joules/image, RAM, p95 latency, wall-power baseline or carbon intensity has been measured. Fewer invocations only define a *potential compute proxy*, not greener inference.
- **Test gate:** the held-out tests remain locked until both development domains and all three seeds are analyzed, fusion and routing protocols frozen, and a defensible absolute safety criterion established.

## Provenance and code

- Paired object recovery code: `scripts/object_level_safety_oracle.py`.
- Immutable validation chunk code: `scripts/08_export_validation_chunks.py`.
- Actual class-aware NMS fusion: `scripts/09_validation_fusion_report.py`.
- Exploratory confidence-routing frontiers: `scripts/10_validation_routing_frontier.py`.
- The exploratory source report is anonymized and reproducible from privately retained model predictions; raw image/prediction records are not public.

**Research integrity:** All analysis on validation only. No GPU retraining, test access or CO2 savings claims. The original cross-domain manuscript and the separate Y-PPE 17-class data audit remain independent research tracks.
