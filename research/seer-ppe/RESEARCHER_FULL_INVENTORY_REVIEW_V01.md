# SEER-PPE full person/PPE inventory — human review handoff v0.1
**Date:** 2026-11-17  
**Review status:** `AI_PRE_REVIEW_ONLY`; no case is approved human ground truth. **No original Roboflow image/annotation/model change.**

## Scope, evidence and meaning
The four **Train** source images were displayed as raw, unmodified pixel images inside Roboflow using a validated read-only pass-through Workflow. Existing native annotations and earlier provisional AI reviews were independently re-read. Result: **7 visually discernible person candidates**, **26 original positive PPE-labeled item boxes**, **14 old absence-marker boxes**, and **42 person × six-PPE review cells**. These are intake/workload quantities, **not verified person recall, detector accuracy, association accuracy, or statistical efficacy**. All images still require an exhaustive human search for missed persons or PPE.

The six PPE categories per person are hard hat, safety vest, eye protection, face mask, glove, and safety boot. `P?` = AI suggests visually present; `A?` = AI suggests visually absent on visibly inspected anatomy; `U?` = unknown, occluded, out of crop, certification unclear, or not yet assessed. **Every symbol carries a question mark because a researcher has not signed it off.** `UNKNOWN` is the only allowed decision when sufficient visual/ownership evidence is unavailable; do not infer true negative/violation from a `No …` class or missing box. None of this determines a site PPE requirement: `POLICY_UNKNOWN` everywhere.

## Case-wide image inventory

| Case | Image | AI-visible persons | Old positive PPE item boxes | Old `No ...` class boxes | Main unresolved review work |
|---|---|---:|---:|---:|---|
| A | `image_604.jpg` | 1 | 3 | 1 | Hands/feet outside crop; verify three physically worn items and uncovered face; goggles vs generic protective glasses |
| B | `000760.jpg` | 2 | 9 | 3 | Small distant worker; four glove annotations; user cannot confirm ownership of boots K/L/M, safety rating unproven |
| C | `Kathiah Gets a Chance03.jpg` | 4 | 13 | 10 | Four people, far-right partial reflective material, glove J user cannot confirm, feet/faces largely occluded |
| D | `h1.jpg` | 0 | 1 | 0 | Standalone unoccupied hard hat only; zero visible people, no wearer assignment |

### Six-category per-person provisional visual-state matrix

| Case | Person | Hard hat | Safety vest | Eye protection | Face mask | Gloves | Safety boots |
|---|---|---|---|---|---|---|---|
| A | P001 | P? | P? | P? | A? | U? | U? |
| B | P001 | P? | U? | U? (not yet assessed) | U? | P? | U? |
| B | P002 | P? | U? | U? (not yet assessed) | U? | U? | U? |
| C | P001 | P? | P? | U? (not yet assessed) | U? | P? | U? |
| C | P002 | P? | P? | U? (not yet assessed) | U? | P? | U? |
| C | P003 | P? | P? | U? (not yet assessed) | U? | U? | U? |
| C | P004 | P? | U? | U? (not yet assessed) | U? | U? | U? |

The matrix has **42 provisional cells** (six categories × seven people). Missing assessment entries are explicitly `U? (not yet assessed)`; they are not imputed `ABSENT`. For face masks, visual absence (`A?`) does **not** mean policy violation. A visually shod foot does **not** prove footwear conforms to a safety standard. `P?` for head protection or eyewear refers only to visible equipment appearance, not certified grade.

## Existing source-annotation item IDs by case (all require human item confirmation)

**Case A — `image_604.jpg`:** Safety Vests: `1`; Goggles: `2`; Hard Hat: `3`.

**Case B — `000760.jpg`:** Hard Hat: `3`, `4`; Gloves: `6`, `7`, `9`, `A`; Safety Boots: `K`, `L`, `M`.

**Case C — `Kathiah Gets a Chance03.jpg`:** Safety Vests: `5`, `6`, `7`, `8`; Hard Hat: `C`, `D`, `E`, `F`; Gloves: `G`, `H`, `I`, `J`, `K`.

**Case D — `h1.jpg`:** Hard Hat: `1`.

- Old absence-marker boxes: 1 in A, 3 in B and 10 in C. They are **not** physical PPE items, reliable absence facts or policy determinations.
- Old `Pants` (one box in B) is recorded as non-PPE clothing context, not an automatic protective-equipment compliance criterion.
- The image D (standalone helmet) is an **orphan-equipment/no-person control**, not a worker-level negative or missing-helmet ground-truth example.

## Preserved preliminary researcher statements (not final gold labels)

| Case and item | Researcher's current provisional ownership status | Reason | Does not mean |
|---|---|---|---|
| C / `J` / `E012` (glove) | `UNKNOWN`, no confirmed wearer | Researcher cannot establish person from available evidence | Not a confirmed `AMBIGUOUS` tie, not P003/P004 matched |
| B / `K` / `E007` (shoe) | `UNKNOWN`, no confirmed wearer | Researcher cannot verify shoe-to-person linkage | Not automatically P002 or certified Safety Boots |
| B / `L` / `E008` (shoe) | `UNKNOWN`, no confirmed wearer | Same limitation | Not automatically P001 or certified Safety Boots |
| B / `M` / `E009` (shoe) | `UNKNOWN`, no confirmed wearer | Same limitation | Not automatically P001 or certified Safety Boots |

The earlier AI guesses for these four objects remain **historical unapproved candidates only**, not operative person IDs. The original `h1.jpg` object has **no visible person**; its present AI item assignment candidate is also `UNKNOWN`, but the researcher has not individually signed it off.

## Exact next human review work, without forcing unverifiable answers

1. **Person completeness:** confirm the actual discernible persons (A 1, B 2, C 4, D 0 or correct them), all partially cropped/occluded humans, and stable left-to-right IDs; ensure no missed person boxes. Record exceptions.
2. **Item completeness:** review all 26 old positive boxes and search outside them for missed physical items. Check item class, wearer, anatomical evidence (head, torso, wrist/hand, ankle/foot), and whether old segmentation/box is actually visible.
3. **Six PPE states per person:** confirm or revise every `P?/A?/U?` in the 42-cell matrix; it is legitimate to approve a **visually undecidable** status `UNKNOWN` with an evidence reason. Inspect both gloves/boots and visibility separately where relevant.
4. **Unresolved sources:** researcher decision remains `UNKNOWN` for J/K/L/M unless new adequate visual evidence; verify P004 reflective patch in C, small P002 gloves in B, and safety classification of the boots (no certification evidence yet).
5. **Policy & rights:** without documented PPE mandate, `POLICY_UNKNOWN`; source provenance/rights/privacy and possible near-duplicate source-family are `UNREVIEWED` and may require exclusion from eligible scientific analysis.
6. **Researcher approval:** sign/review each case; only then store approved `persons[]`, `ppe_items[]`, `worker_ppe_states[]`, `associations[]`, `task_mandates[]` and `source_review` in the **separate Roboflow Eval Dataset**, with genuine `groundTruthState=complete`. Until then, keep `groundTruth={}` and `incomplete`.

## Reproducibility and limitations

- Machine-readable expanded matrix: [`RESEARCHER_FULL_INVENTORY_MATRIX_V01.json`](RESEARCHER_FULL_INVENTORY_MATRIX_V01.json), containing unapproved 42 cells and traceable source annotation IDs, **no source image pixels**.
- Earlier [AI visual prereview](WORKER_ASSOCIATION_AI_VISUAL_PRE_REVIEW_V01.json), [researcher preliminary sign-off statements](RESEARCHER_SIGNOFF_QUEUE_V01.md) and [review protocol](WORKER_ASSOCIATION_REFERENCE_PROTOCOL_V01.md) retain provenance. If an AI proposal conflicts with a researcher preliminary `UNKNOWN`, the latter prevails for review routing while both stay unapproved for scoring.
- All four Workflow Eval Cases remain **0/4 complete**; no `MATCHED` or `AMBIGUOUS` scores, Validation calibration, old-Test evaluation, policy violation, XAI faithfulness or Joules measurements are claimed.
