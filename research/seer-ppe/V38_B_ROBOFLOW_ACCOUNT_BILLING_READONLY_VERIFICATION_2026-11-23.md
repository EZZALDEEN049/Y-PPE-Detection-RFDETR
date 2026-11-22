# V38-B — Read-only Roboflow billing entitlement check (no inference)

**Date:** 2026-11-23 (Asia/Aden). **Workspace:** `softyyemen`.  
**Purpose:** Check author-requested available credits and Flex billing, without initiating the prospective 24-image/48-target, 6,000-call XAI study.

## Verified read-only account signals

A Roboflow connected-agent query explicitly could **not** read current financial balance or Flex Billing state. A second independent read-only check used the pre-existing GitHub Actions `ROBOFLOW_API_KEY` secret with the **official Roboflow Python SDK** and the Roboflow read-only serverless usage-check endpoint. Secrets were never printed. Execution: https://github.com/EZZALDEEN049/Y-PPE-Detection-RFDETR/actions/runs/45083598229

| Signal | Observed | Limits |
|---|---|---|
| Official `rfapi.get_plan_info(...)` | READ_SUCCESS | Returns only `is_enterprise`, `is_pro`, `is_trial`, `over_quota` fields; not balance |
| Account `over_quota` | `False` | Indicates not currently marked over quota; **does not prove 1.125 credits remain** |
| Read-only `GET /serverless/usage-check` | HTTP `200`, `underCap: true` | Indicates current serverless calls appear allowed, not sufficient future credit capacity |
| SDK `rfapi.get_billing_usage(...)` | `RoboflowError` | No valid billing usage/balance obtained; do not invent status or numeric results |
| Included/prepaid credits remaining | **UNKNOWN** | Not accessible with the present connected tools and read-only access path |
| Flex Billing enabled/disabled | **UNKNOWN** | Neither API path reported this setting |
| Hosted model-image inference executed by this check | **0** | No model inference, Test exposure, new training, or financial purchase |

## Public, non-account-specific estimated incremental requirements

Published Roboflow standard Serverless RF-DETR Small rate: **0.1875 credit/1,000 model-image inferences** (https://docs.roboflow.com/deployment/roboflow-cloud/serverless-api/model-pricing). The V38-B existing protocol anticipates **5,200 unique intended inference calls ≈ 0.975 credit** and a guarded maximum **6,000 attempted calls ≈ 1.125 credits**, subject to the provider's charging rules and account-specific plan.

**An active serverless endpoint does not prove availability of all 1.125 additional credits.** The final runner has not yet been wired to the audited budget prototype. Both exact remaining credit balance and Flex billing status remain unverified. The author has NOT separately given one-time execution and monetary approval. Do not execute paid inference based on these signals.

## Current decision

- **Read-only access status:** PASS for present quota and serverless allowed status.
- **Numeric remaining balance:** UNKNOWN.
- **Flex billing state:** UNKNOWN.
- **V38-B paid inference permission:** **HOLD**.
- **Recommended remaining user-only verification:** https://app.roboflow.com/softyyemen/settings/plan (Plan & Billing); inspect the currently remaining credits and Flex configuration. The ChatGPT Roboflow connector and permitted cloud SDK checks did not grant that view. Credentials and card details are not required in chat.
- Previous V38-B EXIF-aware 24/24 input preflight is PASS and recorded separately; the new script must honor canonical EXIF-corrected source hashes. No old experimental results changed.
