# SEER-PPE V11 checkpoint — source eligibility and executable Person–PPE contract

**21 November 2026 — implemented; scientific scoring still blocked.**

The new [468-row source eligibility ledger](SOURCE_ELIGIBILITY_DECISION_LEDGER_2026-11-21_V11.json) preserves five previous source holds, 94 additional source-lineage cases awaiting individual signoff and 369 unflagged but uncertified Valid images. Its separate [human adjudication overlay](SOURCE_LINEAGE_SIGNED_DECISIONS_2026-11-21_V11.json) has **zero** signatures, so no new independent-Validation eligibility is asserted.

The new [Validation-only Person–PPE gate](tools/validate_v11_source_and_person_ppe_gate.mjs) has a defined [input contract](PERSON_PPE_EVAL_INPUT_CONTRACT_2026-11-21_V11.json) and [unsigned freeze](VALIDATION_PERSON_PPE_SCORING_FREEZE_2026-11-21_V11.json). It tests source-ID lineage and human reference completeness, handles abstention/UNKNOWN distinctly from absence, and supports conditional visual status and pre-aligned item-owner metrics *only after* all permissions and research evidence are signed. No real scores are produced in V11.

**Unchanged:** Train A–D 0/4 complete, 19 links, 38/42 visual cells, four B missing, D no-person unsigned; model `altayyar-0oflt-lafos-qqauz/2` not retrained; original images, annotation, splits and Test untouched. Original-valid to Clean17 membership mapping still requires verification. No new mAP/F1, false-clearance rate, XAI fidelity, occupational compliance or Joules. `scoring_ready=false`.

[Source decision protocol](SOURCE_ELIGIBILITY_DECISION_PROTOCOL_2026-11-21_V11.md) · [Person–PPE executable protocol](PERSON_PPE_EXECUTABLE_EVALUATION_PROTOCOL_2026-11-21_V11.md) · [V10 checkpoint](DUAL_TRACK_CHECKPOINT_2026-11-21_V10.md).
