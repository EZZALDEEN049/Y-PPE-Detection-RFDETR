# SRAC-PPE software corrections (research-only)

**Status:** local prototype validated by unit tests; **not an installed production system**. The previously delivered ZIP has **not** been overwritten. These unified patches make the exact changes independently reviewable.

## Apply patches to a local copy of the frozen-model integration v2 package

From the directory that contains `srac_ppe/risk.py`, apply in order:

```bash
patch --dry-run -p1 < 0001-fix-coverage-denominator.patch
patch -p1 < 0001-fix-coverage-denominator.patch
patch --dry-run -p1 < 0002-separate-runtime-policy-and-ground-truth.patch
patch -p1 < 0002-separate-runtime-policy-and-ground-truth.patch
python -m unittest discover -s tests -v
```

Use the actual relative or absolute paths to patches. The second patch targets the **first-patched** `risk.py`. Do not try to apply these to an unrelated version of the package. Keep an immutable source ZIP checksum.

## Interface change in patch 0002 (BREAKING)

The former `ppe_required` column is replaced by:
- `policy_helmet_requirement`: **REQUIRED**, **NOT_REQUIRED**, **UNKNOWN**; available *before prediction* via a documented site/task policy.
- `policy_source_id`: identifiable, independently reviewable policy authority. Required when policy is not UNKNOWN.
- `gt_ppe_required`: independent offline human/regulatory adjudication used **only in risk denominators and reported discrepancy counts**.

Other columns remain: `site_id,image_id,worker_gt_id,cluster_id,gt_state,detected,evidence_ok,p_violation`.

Runtime decisions never read `gt_state` or `gt_ppe_required`; an UNKNOWN policy routes detected workers to REVIEW. The offline `UNDETECTED` state is still used to account for missed ground-truth workers.

### Revised research risk definition
- FC: **CLEAR** among independently adjudicated true helmet-rule violations.
- UC: **CLEAR OR UNDETECTED OR erroneous NOT_REQUIRED** among independently adjudicated true helmet-rule violations.

A mistaken NOT_REQUIRED policy on a truly violating worker must not disappear from the broader missed-or-uncontained numerator. Such a policy/GT disagreement is separately reported as `n_policy_gt_requirement_disagreements`.

## Validation done in local integration package
- Original v2 package: 14 unit tests passed.
- After corrected coverage and five additional regression cases: 19 passed.
- After independent runtime-policy vs GT separation and five additional regression cases: **24 passed**.
- An independently implemented scene/source split gate has 8 synthetic tests passed locally. Its GitHub Actions CI workflow has been committed, but a remote execution result has **not yet been verified**.

All of these are **software tests**, not proof of model detection quality, policy source validity, field-site generalization, or real-world risk control.

## Still required before actual experiments
Validate site-policy source independence; verify frozen model score provenance; collect worker-level truth on held-out sites; confirm site/camera/source clusters; fit any worker score only on score-fit partitions; run risk calibration and independently locked tests. The schema change requires downstream CSV producers, annotation codebook, CLI examples and user-facing manuscript definitions to be reviewed for v3 compatibility before publication.
