# EcoSafe — private original-capture provenance request and verification checklist

**Created 2026-10-18. Template only; NO original site/camera IDs were supplied, fabricated or committed.** Store the filled sensitive table in authorized PRIVATE institutional storage. Publish only aggregate counts and nonidentifying leakage risk summaries. The frozen Stage5 nine-class validation manifest lacks verified original site/recording grouping.

## Evidence needed from the dataset owner / field collection steward

Provide, **in a privately stored and access-controlled table**, one row per original capture or exported image family. Recommended columns:

| Column | Meaning / permitted format |
|---|---|
| \`private_image_key\` | Stable internal image reference, securely mapped to the original export (never public worker name). |
| \`original_family_key\` | Groups all crops, augmentations, duplicates, consecutive frames or re-exports descending from the same original. |
| \`worksite_group_key\` | Anonymous stable worksite ID; required to claim generalization across independent construction sites. |
| \`camera_group_key\` | Anonymous fixed camera/recorder group; if unknown, explicitly \`UNKNOWN\`. |
| \`session_group_key\` | Anonymous recording session or date-time segment group; \`UNKNOWN\` if not traced. |
| \`sequence_group_key\` | Video/near-adjacent frames from the same recording; \`UNKNOWN\` if unresolvable. |
| \`original_capture_time_available\` | True/False; avoid publishing precise private worker location/time. |
| \`source_rights_status\` | One of \`documented_authorized\`, \`uncertain\`, \`not_authorized\`. No unstated permission. |
| \`split_membership\` | \`train\`, \`val\`, or \`test\` from original frozen metadata; **never inspect test images or labels to build model policies**. |
| \`audit_method\` | Explanation: existing source manifest, dataset owner attestation, image family map or controlled private visual review. |
| \`evidence_reference_private\` | Private, nonpublic evidence pointer; never GitHub raw original sensitive identifiers. |

Anonymize site/camera keys *consistently* across splits; changing IDs for the same real site in each split defeats independence checks. Do not treat hashes of images as original-capture provenance, and do not infer original-family or worksite identities from filenames or low-resolution perceptual hashes alone.

## Split-integrity examination BEFORE test-policy evaluation

- Join protected original-source registry to original train/val split manifests; measure source-family, worksite and sequence overlap. Document UNKNOWN rows; no sample means 'unknown' rather than 'independent'.
- For held-out split integrity, ideally ask the **data steward** (not the router developer) to compute aggregate source-group intersection counts and a signed attestation without handing over held-out images, labels, prediction scores or sample identifiers. This keeps held-out performance unseen for methodology freeze.
- Flag site/session/near-frame leakage in any split. Fix group treatment **prospectively** through an approved pre-analysis plan; do not silently reshuffle or discard held-out examples to improve a score.
- If one dataset contains a substantial fraction of unidentified source groups, limit empirical claims to the observed exported images. Do not report bootstrap intervals as independent-site confidence intervals.
- Preserve the separate 17-class Roboflow export audit and its evidence; do not reuse its reported exact train/test collision as though it arose within the distinct Stage5-harmonized nine-class validation files.
- Raw face/worker images, original field recording timestamps, GPS/location info, private source keys and API credentials MUST stay outside public GitHub.

## Decision authority and status

| Responsible party | Requested evidence | Status (2026-10-18) |
|---|---|---|
| Dataset owner/collection steward | Source-worksite/session/sequence grouping plus split-independent hash/near-duplicate assessment | **PENDING; no authenticated group map found** |
| Institution/ethics or rights holder | Permission to analyze private test imagery and publish derived counts; consent/anonymization handling if applicable | **PENDING; never presumed** |
| Safety-domain supervisor or qualified reviewer | Externally justified minimum PPE violation recall per class and acceptable false-alert rate | **PENDING; do not invent target** |
| Research team | Exact frozen test plan, statistical family, code/data lock before first held-out performance access | **DRAFT, NOT APPROVED** |
| Hardware measurement lead | Actual metered machine, software lock, trace acquisition/replicate plan | **PENDING; not measured** |

**No-go** for a statement that multiple independent construction sites were validated unless a filled, verified source-group registry supports it. Private group data may be summarized anonymously in the paper, but must not be committed to the PR.
