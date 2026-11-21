# SEER-PPE V12 / V12.2 — verified GitHub Actions evidence

**Date:** 21 November 2026. **Research status:** executed provenance metadata analysis and fail-closed consistency checks; no actual model-performance scoring.

## Verified executed workflows

- [V12 original-to-Clean17 metadata-only reconciliation, run 44842423862](https://github.com/EZZALDEEN049/Y-PPE-Detection-RFDETR/actions/runs/44842423862): `completed / success`. Its job log reported 2,093 original Train/Valid fingerprints, 2,054 Clean17 Train/Valid export files, 426 provisional unique-name original-Valid candidate matches, 33 name-ambiguous original-Valid sources, 9 historical Valid exclusions, 0 raw-byte identity proofs and 0 authorized scientific scores.
- [V12 ranked Valid candidate archival, run 44842880165](https://github.com/EZZALDEEN049/Y-PPE-Detection-RFDETR/actions/runs/44842880165): `completed / success`. The workflow published the persistent [468-row source-ID mapping](SEER_PPE_VALID_TO_CLEAN17_PROVISIONAL_V12.json) with 459 distinct candidate Clean17 export files and no duplicate assignments. Every photo correspondence remains provisional.
- [V12 original source/Clean17 gate, run 44843063650](https://github.com/EZZALDEEN049/Y-PPE-Detection-RFDETR/actions/runs/44843063650): `completed / success`. Live logs included `SEER_V12_SYNTHETIC_CANDIDATE_MUTATION_GATES_PASS` and `SEER_V12_468_SOURCE_459_UNIQUE_CANDIDATE_NO_SCORING_PASS`. The existing V11 evaluator was hardened to reject unsworn Clean17 membership assertions in real `--score` input.
- [V12.2 source-eligibility crosswalk, run 44843217931](https://github.com/EZZALDEEN049/Y-PPE-Detection-RFDETR/actions/runs/44843217931): `completed / success`, including the new `Verify V12.2 Clean17 candidate and source-family hold conservation` step.
- [Public synthetic engineering tests, run 44843217935](https://github.com/EZZALDEEN049/Y-PPE-Detection-RFDETR/actions/runs/44843217935): `completed / success`.

## Final preserved V12.2 counts

The 459 provisional Clean17 Valid candidate mappings include **5 pre-existing research holds**, **87 additional source-lineage flagged unsigned**, and **367 with no screening flag but still uncertified**. The nine historical Valid exclusions comprised seven flagged and two unflagged originals. All five existing holds remain in the provisional corrected Valid image inventory; no old hold was lifted.

No authentic image/photo byte equivalence or source-family independence signoffs have been established by this metadata-only join. No new Person–PPE human labels, model inference, Test image inspection, retraining, annotations, original splits, energy measurements or accuracy results occurred. The source/reference gate remains `scoring_ready=false`.

[Scientific manuscript v0.12.2](MANUSCRIPT_MASTER.md) · [V12.2 crosswalk](VALID_CLEAN17_SOURCE_ELIGIBILITY_CROSSWALK_2026-11-21_V12.md) · [V12 checkpoint](DUAL_TRACK_CHECKPOINT_2026-11-21_V12.md).
