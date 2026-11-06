# SEER-PPE Phase 4 — data-freeze and human review readiness (v0.4)

**Evidence cutoff: 6 November 2026.** Read-only audit. No source images, labels, model weights or training jobs modified. **Not a final-test clearance report.**

## 1. Data identity
- Original Roboflow 17-class dataset: **2,327** unique image IDs / **16,520** reported object labels; split 1,625 train, 468 valid, 234 original test.
- Historical clean **17-class** derivative described in 2026-09-20 GitHub CI closure: **2,288** images / **16,300** labels (1,595 train, 459 valid, 234 test), with 39 source images excluded and 69 annotation rows corrected (68 exact + 1 near-identical). The old report states CI success; **this turn did NOT obtain/read the 2,288-image binary ZIP**, so it is a *referenced, candidate derivative*, not freshly SHA-256-verified or an independently frozen archive.
- Different **9-class** archive of 1,778 images is NOT the SEER-PPE dataset and must not substitute for cleaned 17-class data.
- Roboflow v2 export was verified to be ready, ~331MB; network constraints prevented local download. It is the *augmented 5,577-image export*, not automatically the 2,288-image clean derivative.

## 2. Live complete original-index read
A read-only crawl of all three original splits returned 1,625 + 468 + 234 = **2,327** metadata records with **2,327 unique image IDs**. This is a **full metadata scan**, not full-image hashing or visual review.

| Original split | Images | With Persons annotation | Without Persons annotation | With No Hard Hat annotation | Person boxes | No Hard Hat boxes | min side < 320 px |
|---|---:|---:|---:|---:|---:|---:|---:|
| Train | 1,625 | 832 | 793 | 124 | 1,739 | 181 | 305 |
| Validation | 468 | 240 | 228 | 39 | 488 | 56 | 89 |
| Original test | 234 | 104 | 130 | 16 | 147 | 22 | 45 |

**Independence flags:** 31 groups of filenames recur across original data splits; 10 of those groups involve the test split. Recurrent names are *candidate review flags*, not proven identical-image or scene leaks. Known video/source families were previously corrected in the archived Stage2 process, but their verified exclusion and remaining same-scene overlap must be rechecked in the real clean17 files. User metadata for individual source-family/rights fields was absent in all 2,327 live original records.

## 3. Human adjudication pilot prepared
- **30 candidate development images**: 16 original train, 14 original validation, **0 original test**. Five deliberately oversampled strata: person/no-hard-hat; multi-person scenes; person with PPE; person plus contextual attire ambiguity; no-Person-annotation negative/control.
- Three previously development-exposed model-smoke image IDs excluded. Same-filename cross-split candidates and three recognized video-family filename patterns excluded **as a temporary safeguard**, not proof of clean-archive membership.
- **30 complete saved geometry records** inspected: **396 boxes**, no nonpositive, out-of-image or unreadable geometry at inspected coordinates. 89 boxes carry Roboflow attribution metadata `RFBoxPrompt/v1`; this indicates model-assist metadata in those saved labels, NOT whether they later received human verification.
- Reviewer A/B blind queues and a worker-level GT template created. **0 reviewer judgments, 0 double adjudications**. Existing labels are visible to internal sampler but **NOT exposed as truth to blinded reviewers**.
- Group provenance and rights must be checked and actual image access permitted before human reviewers use the images. All sample `clean17_archive_membership` fields remain `UNVERIFIED`.

## 4. Safety ontology
An image box named `No Hard Hat` does not by itself prove a worker violated a required hard-hat rule. GT requires an independently inventoried worker, observable wearing state, independently documented task/site PPE requirement, and associations/ambiguity recorded per worker. No cultural garment automatically constitutes a violation. Unknown becomes `UNKNOWN`/review, never implicit compliant.

## 5. Gates and honest status
| Gate | 2026-11-06 status |
|---|---|
| Raw Roboflow index integrity (counts & unique IDs) | PASS (metadata only) |
| Pilot saved box geometry (30 images, 396 boxes) | PASS (geometry only) |
| Freeze clean17 physical ZIP + checksums | OPEN (no local readable binary) |
| Source-family split and perceptual-image independence | OPEN (group IDs and binary image review unavailable) |
| Rights/provenance for sample photos | OPEN |
| Double blind worker-level GT | OPEN (zero adjudications) |
| Independent final test | NOT YET LOCKED |
| New SEER safety/explanation/energy outcomes | NOT RUN |

## 6. Next exact execution
1. Obtain a nonpublic source-authorized clean17 archive or recreate it from Roboflow v2 with archived deterministic script; compare 2,288 image/label pairs and expected 16,300 rows, compute SHA-256 for every file, store archive package fingerprint, manually adjudicate near-image/source families.
2. Use internal provenance queue to verify each selected image belongs to the clean17 derivative and has appropriate evaluation rights. Replace or drop any nonmembers; keep original 30-image proposal as an immutable snapshot.
3. Have two blinded human reviewers independently inventory all people on approved development images; separately assign person-PPE wearing and task rule; adjudicate and calculate agreement before extending the pilot.
4. Only then lock source-group-independent calibration/test partitions. No training or XAI optimization on final-test images.

**Source links:** https://universe.roboflow.com/softyyemen/altayyar-0oflt-lafos-qqauz ; https://github.com/EZZALDEEN049/Y-PPE-Detection-RFDETR/blob/main/cross_domain_reliability/stage2_data_audit/results/Y-PPE_v2_clean_stage2_closure_2026-09-20.md
