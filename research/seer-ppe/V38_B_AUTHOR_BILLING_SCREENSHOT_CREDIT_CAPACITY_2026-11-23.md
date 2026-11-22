# V38-B — Author-supplied Research Plan usage screenshot: credit capacity check

**Date of record:** 23 November 2026 (Asia/Aden); snapshot applies to 1 November–1 December 2026 plan cycle. **Source:** screenshot of the connected Roboflow workspace's Usage > Breakdown interface supplied by the author in the project conversation, following a Plan & Billing screenshot that identifies the workspace's **Research Plan** with **50 monthly included credits**. This is a screenshot-derived financial preflight, not a direct billing-API response.

## Values explicitly visible in the screenshots

| Field | Screen value |
|---|---:|
| Workspace plan | Research Plan |
| Included monthly credits | 50 credits |
| Cycle | 1 Nov 2026 – 1 Dec 2026 |
| Credits Used | 2.49 |
| Usage: Dataset | 1.27 (51.1%) |
| Usage: Deploy | 1.22 (48.9%) |
| Usage: Training | 0 |
| Prepaid Balance | 0 credits |
| Estimated Flex Usage | 0 credits |

No screenshots or personal billing credentials are archived in this file. **Flex Billing enabled/disabled setting is not visible** and cannot be inferred from zero estimated Flex usage.

## Arithmetic / current capacity

- Remaining monthly included allowance **as calculated from author screenshot**: `50 − 2.49 = 47.51 credits`.
- Frozen V38-B intended 5,200 single-image model calls, public standard RF-DETR Small rate `0.1875 credit / 1000 images`: `5200 × 0.1875 / 1000 = 0.975 credits`.
- Frozen one-time **hard limit** 6,000 attempted single-image calls: `6000 × 0.1875 / 1000 = 1.125 credits`. Actual charge depends on Roboflow metering conventions, request failures, exact deployed model tariff, account plan and concurrent usage.
- Snapshot-derived monthly allowance after 6,000 theoretical calls: `47.51 − 1.125 = 46.385 credits`.
- Capacity multiple: `47.51 / 1.125 ≈ 42.23`.
- Based on the screenshot alone there is enough headroom within included monthly credits; **no extra purchase or upgrade is presently recommended**.
- Public model-specific tariff context: https://roboflow.com/blog/model-cascades-for-computer-vision and https://docs.roboflow.com/deployment/roboflow-cloud/serverless-api/model-pricing. Plan context: https://research.roboflow.com/credits.

## Remaining execution control gates (NOT yet satisfied by usage screenshot)

1. The prospective V38-B experiment is the separately frozen sample of 24 original Valid images, 48 detections, 11 classes, same RF-DETR Small `altayyar-0oflt-lafos-qqauz/2`, no Test, no retraining.
2. The EXIF-aware 24-image read-only preflight succeeded (historical V26 byte hashes unavailable; current 24 canonical RGB hashes saved). Preserve the EXIF-6 90-degree image correction in the actual runner.
3. The `6,000 attempted calls` guard has passed **offline simulation only**. The real hosted inference execution runner must implement an enforced pre-request global counter, log every attempted call including provider errors and retries, and undergo no-charge tests before any live experiment.
4. This screenshot **is evidence of available account credit capacity, NOT an explicit author instruction to spend up to 6,000 model calls**. The author previously authorized *designing* V38-B, not the paid run. Do not create an automatic paid-run workflow merely from an account usage screenshot.
5. Recheck account usage at the moment of any authorized execution, because other workspace activity or a billing-cycle transition may change headroom. Stop if metering or allowance differs materially.

**Research decision:** financial-headroom gate **PASS based on author-supplied screenshots**; planned published-standard credit burden < available monthly allowance. **Actual execution state remains HOLD**, pending implementation / QA of actual runner and separate author authorization for the one-time attempted-call ceiling.
