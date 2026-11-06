# SEER-PPE cumulative CHANGELOG

## v0.4 — 2026-11-06
- Full **live original** Roboflow index read: 2,327 image IDs, source/size/split label statistics and 31 filename-collision groups reported, carefully NOT classified as proven image leaks.
- 30 deterministic candidate *development* images (16 train / 14 valid), 0 original test; 396 saved boxes geometry reviewed and 89 model-assistance-provenance markers observed.
- Private blinded reviewer A/B and provenance/clean-archive membership queues written, initially unadjudicated/unverified.
- `PHASE4_REPORT.md`, source-scope evidence JSON, `ANNOTATION_REVIEW_PROTOCOL.md`; cumulative manuscript methods appendix updated.
- Physical 17-class clean derivative verification remains OPEN; original raw v2 Roboflow export accessible remotely but not downloadable in local runtime. No claim of a newly frozen SHA-hashed archive.
- No model weights, images, proprietary raw photo contents, training, or energy metrics published; no SEER results claimed.

## v0.3 — 2026-11-04
- Created evolving manuscript, split/target safety-gate utilities and 40 synthetic unit-test baseline.

## v0.2 / v0.1 — 2026-11-04
- Hosted model engineering smoke and initial paper protocol.

## v0.5 — 2026-11-06
- Reconstructed and audited clean 17-class Y-PPE images in GitHub Actions; run #42153641457 passed file integrity, retained only checksum/evidence artifacts, not raw image archive.
- Fixed an audit-script error that initially rejected 436 valid polygon annotation rows; final result: 15,864 box + 436 polygon rows, zero invalid rows.
- Prepared metadata-only 30-image clean-derivative candidate alignment (29 name+count unique, one one-row dedupe-consistent).
- Started human-review **administrative handoff**: generated anonymized and separately shuffled A/B case queues and blank third-expert log; no human judgments yet.
- Updated working manuscript with Phase5 Appendix B; no fabricated accuracy/XAI/energy results.
