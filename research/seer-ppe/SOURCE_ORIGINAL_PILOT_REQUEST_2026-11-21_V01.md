# SEER-PPE — authorized original Source-byte pilot request (21 November 2026)

**Read-only research scope:** Exactly **three** previously queued Train↔Valid candidate pairs, **six** unique Roboflow original Source IDs from `DUAL_TRACK_CHECKPOINT_2026-11-21_V04.json`. No new Test access, no new inference, no model training, no dataset/split/annotation/Eval writes.

## Purpose
Use the existing, preconfigured repository `ROBOFLOW_API_KEY` GitHub Actions secret solely at runtime to call `Roboflow.project.image(Source ID)` and download each returned **original Source** image into ephemeral private runner memory/disk. Compute raw SHA-256, EXIF-oriented decoded-RGB SHA-256 and 64-bit dHash for the six Source IDs; compare exactly the three locked cross-split pairs. Upload only sanitized fingerprint/comparison JSON as a temporary Actions artifact, **not** raw media, Source-access URLs or API credentials.

## Hard gates
1. Frozen 2,093-image manifest requires 1,625 Train, 468 Valid, zero Test, unique safe Source IDs.
2. All six IDs, filenames, dimensions and splits must agree with the V04 documented source IDs.
3. Acquire the SDK's explicit `urls.original` field, not a generated/augmented dataset Version. Refuse an absent URL rather than fabricate a download.
4. Accept only HTTPS from `source.roboflow.com`; reject other hosts or redirects, oversized bytes, non-image content, failed decoding and mismatched source dimensions.
5. **Fail closed** on incomplete pilot; use incomplete results only to diagnose access. A successful pixel match does not itself decide media-family independence. No scientific score is authorized.

**Trigger file deliberately separate from the comprehensive 2,093-source audit.** A pilot success permits planning a full original Source-byte audit but does not complete it, and Test remains sealed.

[Workflow](../../.github/workflows/seer-ppe-source-original-pilot.yml) · [Source acquisition code](tools/source_original_acquire_pilot.py) · [V04 checkpoint](DUAL_TRACK_CHECKPOINT_2026-11-21_V04.md).
