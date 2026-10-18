# EcoSafe — mandatory object-level recovery correction (pre-execution amendment)

**Status: scientific gate / proposed amendment, not a revised tested EcoSafe manuscript.**
**Date: 2026-10-17.** No model predictions, held-out test images or GPU training
are run by the new files. Existing six immutable YOLO11m checkpoint locks stay
unchanged.

## Critical defect in the current experimental draft

The former development dataset builder calculates recovery as
max(0, primary_safety_fn - secondary_safety_fn). This is not object-level
recovery. Example: a primary detector catches object A and misses B, while
the secondary misses A but detects B. Both have one FN, giving a zero
count-based recovery, although combining their detections could recover B.

The existing selective simulation also substitutes secondary FN counts when
escalating; it is therefore a **switching/replacement policy**, not an
always-run-both/fusion reference. Treating that as "always both" would bias
the comparison and invalidate the proposed interpretation of compute savings
for a safety-oriented selective ensemble.

## Safe correction implemented

object_level_safety_oracle.py provides class-aware, maximum-cardinality
GT-to-detection matching at a pre-fixed IoU threshold. It compares:
- primary detector alone;
- secondary detector alone;
- prediction **concatenation** upper-bound oracle (both sets are available).

The oracle counts additional ground-truth safety objects matched when both
prediction sets are available. It detects complementarity hidden by equal FN
totals and prevents accidental conflation with the secondary-replacement rule.

**This is NOT an operational fusion method.** Concatenating detections can
double-count the same object and worsen false positives. A published real
always-both reference must freeze and implement a proper deterministic
merger/deduplication policy (e.g. class-aware NMS/WBF with fixed thresholds)
before test evaluation. The concatenation oracle establishes only a
safety-recall ceiling under this matching convention, not a deployable system
or a measured model improvement.

## GO/NO-GO order

1. Keep all six last.pt checkpoint identities and Y-PPE-h9-v2 /
   Construction-PPE-h9-v2 frozen splits unchanged.
2. Regenerate validation-only per-image predictions from the exact checkpoints.
3. Compare object-level primary/secondary/concat oracle per validation frame.
4. Quantify positive/negative recovery and the rare no_boots class; separate
   domains, model directions, and all three seeds.
5. Only if the oracle improves meaningfully over the best single expert,
   pre-specify the actual fusion policy, router feature/target, cost metric and
   loss margin delta **without inspecting held-out test labels**.
6. Fit the router with development-only out-of-fold predictions; freeze a
   threshold against the ACTUAL reference fusion, not the switching baseline.
7. After freezing, evaluate held-out performance. Report paired/clustered
   uncertainty, safety false negatives, execution fraction and measured latency/
   energy (not merely GPU call count).

## Publication language

Prohibited: "an adaptive ensemble saves X% energy" derived from invocation
fraction; "always-run-both" when the secondary simply replaced the primary;
"recovers object errors" based on global difference of false-negative counts.

Permitted for now: "A synthetic-code-tested object-level matching method was
implemented as a pre-execution audit. Real EcoSafe complementarity, selective
routing outcomes, and energy consumption remain unmeasured."

## Testing and boundaries

Only artificial geometries are used in unit tests. Detector outputs,
image names, GT annotations, checkpoint weights, and API keys are not
uploaded. No regression suite for the earlier paper is modified.
