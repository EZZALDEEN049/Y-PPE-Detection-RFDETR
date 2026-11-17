# SEER-PPE — Case B headgear and glove item-to-worker review v0.1

**Review date:** 2026-11-17 | **Image:** `000760.jpg` (Train, 500×330) | **Stage:** `AI_SOURCE_IMAGE_RECHECK_COMPLETE — RESEARCHER_ITEM_SIGNOFF_PENDING`

## Source and integrity

Source image read using a validated **read-only** Roboflow Workflow pass-through. Native annotation boxes read from `softyyemen/altayyar-0oflt-lafos-qqauz` without any annotation writes, and compared with [full inventory](RESEARCHER_FULL_INVENTORY_MATRIX_V01.json) and [item audit](ITEM_LEVEL_ASSOCIATION_EVIDENCE_AUDIT_V01.json). There are **two persons**, previously confirmed by the researcher: `P001` in foreground, `P002` in background.

User previously **confirmed visual person-level states**: `P001` hard hat `PRESENT`, glove `PRESENT`; `P002` hard hat `PRESENT`, glove `UNKNOWN`. This confirmation **did not separately approve item box IDs**. Other user decisions: no reflective vests on either worker; eye protection not visible; face masks unknown; safety footwear reported in scene but exact boxes `K/L/M` **person attribution `UNKNOWN`**, with no certification evidence. All applicable workplace PPE rules remain `POLICY_UNKNOWN`.

## Six item-box attribution proposals, for explicit researcher adjudication

| Native annotation | Native class | Centre (px) | Dimensions (px) | AI item-wearer proposal | Confidence/visibility rationale | Researcher box-level approval |
|---|---|---|---|---|---|---|
| `3` / `E001` | `Hard Hat` | `(235.23,55.42)` | `37.93×43.64` | `P001` / `MATCHED_CANDIDATE` | Foreground worker's blue headgear visible on head | **PENDING** |
| `4` / `E002` | `Hard Hat` | `(309.08,92.04)` | `24.66×22.72` | `P002` / `MATCHED_CANDIDATE` | Rear smaller worker's purple/blue headgear visible; source person boxes overlap geometrically, requiring head/body continuity rather than centre containment alone | **PENDING** |
| `6` / `E003` | `Gloves` | `(240.68,141.93)` | `28.64×22.95` | `P001` / `MATCHED_CANDIDATE` | Yellow glove by foreground worker's hand near torso | **PENDING** |
| `7` / `E004` | `Gloves` | `(145.00,63.30)` | `30.00×27.50` | `P001` / `MATCHED_CANDIDATE` | Yellow glove at foreground worker's raised hand contacting vertical column | **PENDING** |
| `9` / `E005` | `Gloves` | `(346.92,133.06)` | `14.27×13.53` | `UNKNOWN_CANDIDATE`, `person_id=null` | Old glove-labeled box near distant rear worker's arm; wearer/item type cannot be verified reliably at 500×330 | **PENDING** |
| `A` / `E006` | `Gloves` | `(336.43,171.88)` | `11.71×11.31` | `UNKNOWN_CANDIDATE`, `person_id=null` | Small lower arm/hand-region box; occlusion and image resolution prevent reliable physical glove classification or owner confirmation | **PENDING** |

**Important semantics:** `MATCHED_CANDIDATE` and `UNKNOWN_CANDIDATE` are **AI visual recheck suggestions**, not item-level `MATCHED` or human-decided `UNKNOWN` gold labels. The current main matrix item `provisional_association.status` remains `NOT_HUMAN_ADJUDICATED` on all six, with `person_id=null`. The researcher's prior **P002 glove visual state = UNKNOWN** does not in itself settle whether native boxes `9` or `A` are actual gloves. Historical AI guesses `9/A → P002` are not currently endorsed.

## Preserve separate footwear determination

| Native boot box | Researcher's preliminary owner decision | Previous geometric AI-only hypothesis |
|---|---|---|
| `K` / `E007` | `UNKNOWN`, `person_id=null` | `P002`, historical unapproved only |
| `L` / `E008` | `UNKNOWN`, `person_id=null` | `P001`, historical unapproved only |
| `M` / `E009` | `UNKNOWN`, `person_id=null` | `P001`, historical unapproved only |

Boot protection grade is not independently verified. The user's report of scene-level footwear and different trousers does **not** establish per-box boot ownership. Do not infer compliance or noncompliance.

## Review decision requested

After inspecting the [original Roboflow image](https://source.roboflow.com/jKwqROZgEDNWeNDWEgqAnytu2ZC3/0xxsYWiz1FZBYERolu4z/original.jpg), the researcher can approve, revise or choose `UNKNOWN` **separately for item IDs** `3`, `4`, `6`, `7`, `9`, `A`. A review answer approving `3→P001`, `4→P002`, `6→P001`, `7→P001` **with** `9/A UNKNOWN` would be a new explicit researcher item-level decision; it has **not yet been given** at the time this audit was written.

Even with person-item approval, **separate Roboflow Eval Case B remains `incomplete`** until the ground-truth content, source rights/privacy/family, and second review are ready. No original Roboflow labels/splits/trained model/Workflow have been edited. Do not claim model accuracy or safety outcomes.
