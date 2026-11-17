# SEER-PPE — Researcher sign-off queue for four Train images (v0.1)

**Prepared:** 2026-11-17 | **Researcher approval state:** `PENDING` on 4/4 cases  
**Purpose:** Independent human source-image review before `groundTruthState=complete` in Roboflow Eval Dataset `9c2679df-f2b9-4e25-b88d-9c6ac9033a95`.

## Critical separation
- These are **original Train images**. The image editor is for visual inspection; **do not save edits to existing source annotations** for this reference study.
- Review originals with detections/old labels hidden first, including the possibility of people and PPE missed in those old labels. Only then compare with source annotations and the AI visual pre-review.
- All previous AI suggestions are labeled *not independent human truth*. A human reviewer must provide their own judgment and evidence; a ChatGPT-generated sign-off would not count as a human reference.
- Maintain `POLICY_UNKNOWN` for every worker/PPE pair without applicable task/site mandate evidence. Do not make a compliance or violation decision in this sign-off.
- Before any public image sharing, adjudicate copyright/source rights and privacy. No image pixels embedded in this file.

## Case-by-case checklist

| Case | Filename | Image ID | What the researcher must verify | Current status |
|---|---|---|---|---|
| A | `image_604.jpg` | `0jRe8fpRDE5fLgAJrYvT` | Exactly one visible person? Helmet/vest/eyewear item ownership; exposed nose/mouth (visual absence of face mask), hands and feet cropped; any missed item | **PENDING** |
| B | `000760.jpg` | `0xxsYWiz1FZBYERolu4z` | Exactly two visible people? PPE ownership for foreground P001 and background P002, including glove boxes; three old `Safety Boots` labels `K,L,M` are visual footwear candidates **but safety certification is not proven**; how to label PPE state safely | **PENDING** |
| C | `Kathiah Gets a Chance03.jpg` | `0jGu9euJp1MbvkLtfBcs` | Exactly four visible people? Assign hats/vests/gloves; confirm extent of reflective vest for far-right crouched P004. Especially glove annotation `J` vs P003/P004 | **PENDING** |
| D | `h1.jpg` | `0oVmRAxL0SM1PWqZCNyM` | No person visible? Standalone yellow helmet is NOT worn; retain `UNKNOWN` item-to-person association (not worker PPE absence) | **PENDING** |

## Targeted unresolved check: glove J (Case C)
- Old source annotation: `id=J`, `class=Gloves`, center `(1163.5, 764.0)`, width `65`, height `28` px.
- Region `xyxy`: `[1131, 750, 1196, 778]` in a `2048×1365` image. In the separate provisional item inventory it is `E012`.
- Competing visually plausible person IDs: `P003` (bent-over third person from left) and `P004` (crouching far-right person). The object box lies in the gap between their *old* person boxes, so nearest-center / overlap alone is not dispositive.
- Human instruction: zoom original region, trace red glove to cuff/sleeve/wrist and body; document anatomy and occlusion. Choose `MATCHED→P003`, `MATCHED→P004`, `AMBIGUOUS→[P003,P004]`, or `UNKNOWN`, with visual reason. **Do not auto-select a label from the pre-review suggestion.**

**Researcher entry:** `J_status: __________`  `J_person_id_or_alternatives: __________`  
`J_evidence: ______________________________________________________________`

## Targeted unresolved check: boots (Case B)
Source annotations `K`, `L`, `M` are old `Safety Boots` labels; geometries in a `500×330` image:
- `K`: center `(358.64,256.02)`, size `21.82×21.14`, candidate associated with background `P002`.
- `L`: center `(284.36,284.51)`, size `23.73×22.53`, candidate associated with foreground `P001`.
- `M`: center `(217.66,284.07)`, size `32.17×21.64`, candidate associated with foreground `P001`.

**Researcher instruction:** inspect footwear presence and wearer independently. If toe/sole construction or independent product/site evidence does not establish safety-specific protection, mark safety-boot `visual_state=UNKNOWN` rather than treating an old `Safety Boots` class as proof of compliance. Keep `POLICY_UNKNOWN` unless documented task PPE rules are provided.

**Researcher entry:** `K_wearer: ____`, `L_wearer: ____`, `M_wearer: ____`  
`Boots visual safety-class evidence (or UNKNOWN): ______________________________`

## Completeness & evidence certification (one row **per case**)
Each case needs review of the *entire* image, not just detected boxes:

| Case | True visible persons / IDs | Missed persons? | Physical PPE inventory complete? | Item association and P/A/U decisions reviewed? | Rights/privacy/source family checked? | Reviewer/date | Approval |
|---|---|---|---|---|---|---|---|
| A | `_______` | `_______` | `_______` | `_______` | `_______` | `_______` | `PENDING` |
| B | `_______` | `_______` | `_______` | `_______` | `_______` | `_______` | `PENDING` |
| C | `_______` | `_______` | `_______` | `_______` | `_______` | `_______` | `PENDING` |
| D | `_______` | `_______` | `_______` | `_______` | `_______` | `_______` | `PENDING` |

A truthful reviewer can decide some fields as `UNKNOWN` or `RESTRICTED`; exhaustive visual inventory does **not** require forcing an unknown PPE state to presence or absence. If reliable individual association is unobservable, `AMBIGUOUS` or `UNKNOWN` **is** a legitimate reviewed reference, provided the reason is recorded.

## Approval gate
Complete each case only after (a) actual independent researcher review, (b) signed adjudication and updated person/PPE inventories with evidence, (c) source rights/privacy checks or documented restrictions and exclusions as appropriate, (d) referential integrity, and (e) a second review pass. Do not type `complete` into the Eval Dataset on behalf of a reviewer. Post-sign-off, import the reviewed data into the **separate** Eval Dataset Cases, leaving original data untouched. v0.3 algorithm testing is **not authorized to claim accuracy** based on this unapproved queue.

**Reference files:** [visual pre-review](WORKER_ASSOCIATION_VISUAL_PRE_REVIEW_V01.md), [item-level AI candidates](WORKER_ASSOCIATION_AI_VISUAL_PRE_REVIEW_V01.json), [human protocol](WORKER_ASSOCIATION_REFERENCE_PROTOCOL_V01.md).
