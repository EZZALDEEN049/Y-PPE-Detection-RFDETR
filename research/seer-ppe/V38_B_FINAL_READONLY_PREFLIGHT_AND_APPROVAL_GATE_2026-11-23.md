# V38-B — Final zero-inference preflight verdict and author cost/approval gate

**Recorded:** 23 November 2026. **Target paper:** *Cross-Resolution Consistency of Target-Matched Perturbation Sensitivity Maps for Personal Protective Equipment Detection*. **Model:** frozen `altayyar-0oflt-lafos-qqauz/2`; original dataset, source labels, train/validation/test splits and all V26–V37 findings unchanged.

## Verified preflight status: PASS FOR READ-ONLY INPUTS, NOT AUTHORIZED FOR MODEL INFERENCE

The completed [zero-inference GitHub Actions check](https://github.com/EZZALDEEN049/Y-PPE-Detection-RFDETR/actions/runs/45082932157) returned `completed/success` and archived the [EXIF-aware 24-image source and model-free QA ledger](V38_B_CURRENT_SOURCE_EXIF_AWARE_SHA256_PREFLIGHT_2026-11-23.json). Contents verified after archive:

- 24/24 selected Valid image IDs present on Roboflow, all with matching current metadata dimensions.
- 24/24 source originals fetched **read-only**, decoded in ephemeral memory and SHA-256 fingerprinted; all 24 raw-byte hashes distinct.
- 23/24 unrotated JPEG dimensions match original V26 geometry; the remaining image `DDf9S1yCGLJlqesYanSY` has EXIF orientation 6, raw pixels 3840×2160, canonical oriented pixels 2160×3840. **24/24 canonical images match** after mandatory `Pillow.ImageOps.exif_transpose`.
- 48/48 frozen targets' class, baseline confidence, geometry and same-class V26 author-reference IoU≥0.50 cross-checked against 12 archived V26 shards. V13 historical original/export SHA comparison Boolean flags also available for 24/24. **The old V26 actual byte hashes were not saved**, so current SHA checks are fresh execution fingerprints, not historical byte-hash equality.
- 8×8/4×4 exact pixel-area masks and coarse-fine alignment pass. Ten deterministic SHA-256-seeded random orders per selected random-curve target pass.
- Static prototype hard-stop simulated 5,200 intended call reservations plus 800 retry reservations, correctly rejecting attempted call #6001. **This is NOT proof of a wired runtime hard-stop for future Roboflow inference**: the future paid execution code must integrate and test it before any author-approved run.
- No hosted model calls, Test images, model training, Roboflow project mutations, source-photo upload or copied source pixels in GitHub artifacts.
- First strict raw-image size check was held on one EXIF rotated photo; retained as [the failure record](V38_B_CURRENT_SOURCE_READONLY_SHA256_PREFLIGHT_2026-11-23.json). No target was removed, swapped or hidden after this discovery.

## Public pricing verification (does not establish account-specific balance)

Current official [Roboflow Serverless model pricing](https://docs.roboflow.com/deployment/roboflow-cloud/serverless-api/model-pricing) lists RF-DETR **Small** at `0.1875 Roboflow credits/1,000 processed images` for standard usage. [Current general pricing](https://roboflow.com/pricing) lists additional prepaid credits **starting at $4 per credit** and on-demand credits at **$6 per credit** (USD). [Roboflow credit rules](https://roboflow.com/credits) describe included, prepaid and Flex overage. Thus:

| Phase/ceiling | Model-image calls | Public standard credit equivalent | $4 prepaid-credit marginal equivalent | $6 on-demand marginal equivalent |
|---|---:|---:|---:|---:|
| Intended protocol | 5,200 | 0.975 | USD 3.90 | USD 5.85 |
| Hard ceiling | 6,000 | 1.125 | USD 4.50 | USD 6.75 |

These are *marginal usage estimates*, not workspace billing account quotes. The connected Roboflow tools provide project/models/image records but do **not** expose the workspace's remaining credit balance, plan-specific agreement or Flex billing toggle. Cost may be covered by existing credits, discounted under a volume plan, or unavailable when Flex billing is disabled. **No purchase or paid inference has been initiated.**

## Required explicit signoff after account verification

1. Author reviews actual remaining credits and Flex-billing settings in `Roboflow workspace → Settings → Plan & Billing`; make sure at least 1.125 incremental credits are available or agree on how a plan-specific shortfall would be handled; do not disclose passwords, payment cards or API keys.
2. Author supplies clear, scoped approval for **at most 6,000 attempted model-image inference calls** on **24 frozen Valid images / 48 frozen detections**, using `altayyar-0oflt-lafos-qqauz/2`, Test excluded, no retraining, and any applicable financial exposure. **No inference authorization is implicit in the earlier V38-B sample-design approval.**
3. Before execution, an actual Roboflow experiment runner must be built and separately tested with the EXIF-corrected SHA fingerprints and a durable pre-request hard-stop ledger; add one-time execution authorization only after all technical and financial gates pass, with no implicit retries that evade the attempt cap.
4. Raw source photograph rights, site independence and safety-outcome scientific claims remain separate publication gates; this source check does not make the new Validation cohort independent.

**Verdict:** Read-only data identity/geometry and budget-prototype audit **PASS**. Cost/public unit tariff **VERIFIED**; current workspace balance **UNKNOWN**. Paid experiment runner integration **PENDING**. **NO-GO for hosted execution until author-approved account cost and a separately QA-tested actual runner.**
