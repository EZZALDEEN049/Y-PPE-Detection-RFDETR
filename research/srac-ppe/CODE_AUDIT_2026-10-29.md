# SRAC-PPE prototype software audit — 2026-10-29

**Scope:** locally inspected frozen-model integration starter v2, not remote model execution.

## Test execution
- Original package `python -m unittest discover -s tests -v` from package root: **14/14 passed**.
- Audited `srac_ppe/risk.py`: found a reproducible reporting bug in `evaluate`.
- Added regression test and corrected a **local working copy**: **15/15 passed**.
- **Important:** the originally delivered v2 ZIP is not automatically updated, and this public repository does not claim the production risk package was patched or deployed. Apply the correction to the version subsequently used for experiments.

## Actual defect
The original `auto_clear_coverage` used:
```python
all_counts.get("CLEAR", 0) / len(known) if known else None
```
where `all_counts` includes rows with `gt_state="indeterminate"`, while `known` only includes `gt_state in {"compliant","violation"}` and `ppe_required=True`. The metric can exceed 1.

**Reproduction:** one known compliant worker and one indeterminate worker both output `CLEAR` gives **2.0 (200%)** erroneously. This is a software reporting error, NOT a new model finding.

**Correction:**
```python
known_clear = sum(
    decide(r, threshold, p.alert_threshold) == "CLEAR"
    for r in known
)
auto_clear_coverage = known_clear / len(known) if known else None
```
The same example now yields **1.0 (100%)** for *known labeled workers*, and the raw decision-count table can still report both CLEAR outcomes. The regression test verifies this.

## Extended regression status
After the originally documented 15 successful local tests, four further cases were added: (a) proper indeterminate denominator, (b) indeterminate-only coverage undefined, (c) FC/UC invariance to unknown-label rows, (d) no automatic CLEAR without a calibrated threshold; ground-truth-state decision invariance was also verified as a separate test. The revised local v2 package passed **19/19** unit tests. A [unified diff patch](software/patches/0001-fix-coverage-denominator.patch) was committed to GitHub, but the original v2 ZIP was **not modified**.

## Additional high-priority interface validity concern
The current prototype's `ppe_required` Boolean is consumed by **both** `decide()` and the offline `_violations()` denominator. The prototype does not independently validate that this field is a *pre-inference available site policy* rather than a hidden ground-truth annotation. If supplied from retrospective annotations, reported accuracy and risk may be inflated through **policy-label leakage**, even though `decide()` is otherwise invariant to `gt_state`.

**Not fixed in original v2 ZIP or the published coverage patch.** A future schema must isolate `policy_helmet_requirement` (runtime, REQUIRED/NOT_REQUIRED/UNKNOWN) from `gt_helmet_requirement` (offline, independent), and route unknown rules to REVIEW. Freeze the policy source before inference and audit discrepancies between policy and GT. See [experiment protocol](EXPERIMENT_PROTOCOL.md). This is a gate before real-world risk claims.

## Versioned policy/GT interface prototype, second local correction
A further [research-only patch](software/patches/0002-separate-runtime-policy-and-ground-truth.patch), meant to be applied **after** patch 0001, splits `ppe_required` into a pre-inference `policy_helmet_requirement` + documented `policy_source_id` and an offline-only `gt_ppe_required`. It routes UNKNOWN policy to REVIEW and records policy/ground-truth disagreements. **The broader UC numerator is deliberately expanded to include an erroneous NOT_REQUIRED decision against a true violation**; the previous paper formulation omitted this possible failure mode.

After five further regression cases, the **local patched integration package passed 24/24 software unit tests**. A patch dry-run against the expected base risk module succeeded. The unmodified distributed v2 ZIP was not replaced, and real RF-DETR, site-safety policy or risk calibration tests have not been performed. See [software migration notes](software/README.md).

## End-to-end CLI integration evidence (synthetic only)
A local v3 prototype command-line run loaded 120 independent *synthetic* calibration violation records and a separate single-row *synthetic* test containing a true required-helmet violation but incorrect policy `NOT_REQUIRED`. The CLI exited successfully with a parsed report: calibration `SUPPORTED_UNDER_ASSUMPTIONS` (conditional on invented input validity), threshold `0.02`, test `false_clearance_count=0`, `uncontained_violation_count=1`, and policy/GT disagreement count `1`. Assertions passed. These are **software integration fixture values, not dataset/model empirical results**.

## Required follow-ups
1. Transfer patch and regression test into the canonical execution package before any real evaluation.
2. Include `n_known_test`, `n_indeterminate_test`, and outcome counts among indeterminate cases explicitly in reports.
3. Do not treat an indeterminate visual compliance label as safe; deployable evidence gates must abstain based on observable information rather than consulting hidden ground truth.
4. Ensure baseline and proposed method coverage use **identical evaluable denominators**; exclude GT indeterminate for label-dependent risk, but report its frequency and review burden independently.
5. Validate the full pipeline end to end with independent actual model outputs and locked labels. The 15 software tests are neither field trials nor predictive performance estimates.
