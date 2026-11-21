# SEER-PPE V11 — explicit source eligibility decisions and evidence register

**21 November 2026.** A new **468-row Source-ID-keyed decision register** is derived from the frozen original Train/Valid source manifest, the V06 99-candidate queue and V08 468-image eligibility plan. It is not a relabeling of training data or a new site-family adjudication.

| Administrative disposition | Original Valid images | Meaning |
|---|---:|---|
| `RETAIN_PREEXISTING_RESEARCH_HOLD` | **5** | Previously imposed holds stay protected |
| `PENDING_INDIVIDUAL_SOURCE_LINEAGE_DECISION` | **94** | Screen-positive candidates without individual source-family signoff |
| `NO_SCREEN_FLAG_INDEPENDENCE_UNCERTIFIED` | **369** | Not flagged by current screening; independence **not proved** |
| **Total** | **468** | **0** newly signed independent-source eligibility verdicts |

The ledger preserves each Valid Source ID and image dimension, source filename, review reasons, nearest Train candidate, cosine score if saved, dHash near edges if recorded, and V10 graph component ID for flagged near-pair sources. Similarity components are **candidate clusters only**, not proven acquisition sites. Two existing held Valid records `IMG-20250416-WA0063.jpg` and `IMG-20250416-WA0051.jpg` retain the previously observed same named **22 May School – Aseefrah** site evidence, traceable to the 18 November visual audit. That record involved AI visual triage, not newly performed independent dual-human source signoff.

The authoritative human decision layer is a separate **initially empty** append-only overlay. Future per-image entries require a supported source-family verdict, concrete evidence reference, reviewer identity, dated signoff and a train-family comparison basis. An independent-source claim additionally needs documented acquisition/source family and a signed no-Train-family-overlap assertion. Neither general visual-review acceptance nor dHash nonidentity authorizes an independent-source verdict automatically. Five existing holds cannot be lifted in V11 by changing a row automatically.

**Scope integrity:** only original Train/Valid metadata; the original corrected Clean17 subset has not been fully mapped to the ledger here, so the ledger does **not** certify which original Valid IDs belong to Clean17. There has been no Test access, model inference, original split, annotation or dataset mutation. `scoring_ready=false` and all 468 images remain unapproved for source-independent scientific scoring pending source-specific evidence. Reference: [ledger JSON](SOURCE_ELIGIBILITY_DECISION_LEDGER_2026-11-21_V11.json), [signed overlay](SOURCE_LINEAGE_SIGNED_DECISIONS_2026-11-21_V11.json), [existing V10 similarity analysis](SOURCE_COMPONENTS_AND_GUARDRAIL_CONTRACT_2026-11-21_V10.md).
