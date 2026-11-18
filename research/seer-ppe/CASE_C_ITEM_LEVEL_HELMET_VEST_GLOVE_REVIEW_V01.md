# SEER-PPE — Case C source-item to person evidence review v0.1

**Date:** 2026-11-18 (Asia/Aden) | **Status:** `RESEARCHER_FINAL_ITEM_OWNER_DECISIONS_SAVED; FULL_CASE_CLEARANCE_PENDING` | **Source:** original Roboflow Train image `Kathiah Gets a Chance03.jpg`, ID `0jGu9euJp1MbvkLtfBcs` (2048×1365)

## Evidence boundaries

The image was inspected via a validated read-only Roboflow Workflow pass-through, and existing native annotation boxes were read without modification. Four visible workers were confirmed earlier by the researcher, labelled left to right `P001`, `P002`, `P003`, `P004`. The researcher earlier reported **all four** wearing hard hats, reflective vests, gloves, safety boots and traditional `العباءة`. These are *person-level preliminary PPE appearance judgments*, not approvals of the original box ID's owner or independent safety grade.

Prior user decisions **must not be rewritten**: source glove `J` / `E012` has `provisional_association.status=UNKNOWN`, `person_id=null` from an explicit earlier researcher decision. **Superseded by user's explicit approval dated 2026-11-18 as recorded below.**

## Twelve source-box association proposals — AI review only

| Original box | PPE item ID | Old source class | Candidate worker | Visual rationale | Researcher item-level decision |
|---|---|---|---|---|---|
| `F` | `E008` | Hard Hat | `P001` — **AI candidate** | Yellow helmet on far-left worker's head; native box centre (589.5,527.5) | **Researcher final `MATCHED`** |
| `E` | `E007` | Hard Hat | `P002` — **AI candidate** | Yellow helmet on second worker's head; centre (898.5,537) | **Researcher final `MATCHED`** |
| `D` | `E006` | Hard Hat | `P003` — **AI candidate** | Yellow helmet on third (leaning) worker's head; centre (1068,631.5) | **Researcher final `MATCHED`** |
| `C` | `E005` | Hard Hat | `P004` — **AI candidate** | Yellow helmet on far-right crouching worker; centre (1271.5,684.5) | **Researcher final `MATCHED`** |
| `6` | `E002` | Safety Vests | `P001` — **AI candidate** | Bright vest on far-left worker's torso; centre (581,594) | **Researcher final `MATCHED`** |
| `5` | `E001` | Safety Vests | `P002` — **AI candidate** | Bright vest on second standing worker's torso; centre (877,642.5) | **Researcher final `MATCHED`** |
| `7` | `E003` | Safety Vests | `P003` — **AI candidate** | Bright vest on third leaning worker's torso; centre (990.5,693.5) | **Researcher final `MATCHED`** |
| `8` | `E004` | Safety Vests | `P004` — **AI candidate** | Small bright reflective section on right crouching worker's torso/back; vest only partially visible; centre (1323,806) | **Researcher final `MATCHED`** |
| `H` | `E010` | Gloves | `P001` — **AI candidate** | Red glove region near far-left worker's left/outstretched hand; centre (547.5,653) | **Researcher final `MATCHED`** |
| `I` | `E011` | Gloves | `P001` — **AI candidate** | Red glove region on far-left worker's other hand; centre (604,625) | **Researcher final `MATCHED`** |
| `G` | `E009` | Gloves | `P002` — **AI candidate** | Red glove near second worker's hand; centre (871,715) | **Researcher final `MATCHED`** |
| `K` | `E013` | Gloves | `P003` — **AI candidate** | Red glove-like region near third leaning worker's hand/arm; centre (1052.5,746.5) | **Researcher final `MATCHED`** |

## Separately unresolved glove `J`

| Original box | PPE item ID | Old source class | Current person-owner decision | Context |
|---|---|---|---|---|
| `J` | `E012` | Gloves | **Researcher-final owner `UNKNOWN`; `person_id=null`** | Near extended arms of P003/P004; source coordinates centre `(1163.5,764)`, width 65 px, height 28 px; proximity does not establish actual wearer |

**Do not infer** that all workers wearing gloves supplies sufficient evidence to assign glove box `J` to P003 or P004. The historic AI alternatives were P003/P004, unapproved. If the researcher later explicitly revises the owner of J with new evidence, preserve the older UNKNOWN decision in the audit trail; otherwise retain UNKNOWN.

## Other source labels needing reconciliation

Source label boxes `Q/R/S/T` = `No Safety Boots` (**4 absence-like markers, not four physical shoes**); old C source contains **zero positive `Safety Boots` boxes**, while the researcher reports safety boots on each worker. Need crop-level/uncropped image and label-semantics review to distinguish unlabeled boots, nonvisible feet, and unsupported source absence markers. Do not turn that mismatch into a reported detector failure or PPE violation.

Source broad `No Safety Attire` `9/A/M/N` (**4**), and `No Face Mask` `O/P` (**2**), are **absence-style labels**, not physical PPE. They must not override researcher's `UNKNOWN` mask/eye states or person-level helmet/vest/glove presence. Traditional garment `العباءة` is not itself a PPE compliance category.

## Status and approval requested

Please review source image and separately approve/revise the **12** old source-box links above. The user's `UNKNOWN` owner decision for `J` remains effective even if all 12 others are approved. The old labels, model weights, splits, original Workflow and image source remain frozen.

Roboflow Eval Case C `c032f81d-64c5-44be-96f3-7e6fe9dad799` was inspected at revision `3`, with `groundTruthState=incomplete`, `groundTruth={}`. No data was written to that Case as part of this candidate-only review. Source image rights/privacy/source family and independent second pass are `UNREVIEWED`/pending, with workplace PPE requirements `POLICY_UNKNOWN`. These links and observations must not be turned into *complete, ready-to-score* ground truth without all remaining gates.


## Final researcher decision on all 13 box-owner statuses (2026-11-18)

Researcher replied **"موافق"** to the immediately preceding request to approve all **12 proposed original box→worker links** while explicitly keeping source glove `J` ownership `UNKNOWN`. This statement is **FINAL for the specified per-item ownership decisions**; it is not a final image source-rights, PPE compliance, or scientifically complete Eval Case signoff.

| Item type | Final source-box to wearer mapping |
|---|---|
| Hard hats | `F→P001`, `E→P002`, `D→P003`, `C→P004` — `MATCHED` |
| Reflective vests | `6→P001`, `5→P002`, `7→P003`, `8→P004` — `MATCHED` |
| Gloves | `H→P001`, `I→P001`, `G→P002`, `K→P003` — `MATCHED` |
| Glove `J` | `UNKNOWN`, `person_id=null`; no forced identification of P003/P004 |

Worker-level statements remain separate: user reports helmets, vests, gloves and boots PRESENT on all four, and masks/goggles UNKNOWN due occlusion. The four `No Safety Boots` legacy markers are **not proof of noncompliance** and the boot safety standard is not independently documented. `POLICY_UNKNOWN`. Source rights/privacy/source family and an independent second-pass check remain open. See the separate Roboflow Eval status after the partial reference is saved.
