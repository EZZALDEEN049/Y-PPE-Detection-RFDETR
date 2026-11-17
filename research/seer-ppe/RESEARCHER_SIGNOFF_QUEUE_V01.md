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

**Researcher preliminary declaration (2026-11-17, reported in chat; not final sign-off):** `J_status=UNKNOWN`, `J_person_id=null`, `alternatives_not_adjudicated`. The researcher states they **cannot confirm who wears glove J**. This is an explicit insufficient-evidence choice, **not** `AMBIGUOUS` adjudication and **not** evidence that either P003 or P004 is the wearer. The former AI suggestion `AMBIGUOUS_CANDIDATE` is retained in the historical pre-review as a proposal only and superseded for decision-making by this provisional `UNKNOWN` statement. No claim that the researcher inspected the original crop, identified sleeve/wrist continuity, or finished exhaustive image review is made. The prior in-chat illustration was not the actual Roboflow target image; therefore the researcher's UNKNOWN declaration must not be construed as a direct signed review of the original J crop.

**Researcher entry:** `J_status: UNKNOWN (preliminary)`  `J_person_id_or_alternatives: NONE_CONFIRMED`  
`J_evidence: Researcher unable to establish wearer identity; needs original-image zoom and anatomical trace. Not independently corroborated.`

**Remaining review:** Check the source crop around [1131,750,1196,778] for cuff, wrist, sleeve continuity and any overlap/occlusion; keep `UNKNOWN` if insufficient. The rest of Case C, source/rights review, PPE per-person visual states, and second reviewer pass remain pending.

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


## AI source-image recheck of boots K, L, M (2026-11-17)

**Source:** Verified raw `000760.jpg` (500×330 px) from the Roboflow original source image, displayed through a validated **read-only** inline pass-through Workflow. Checked against current original source annotation centers and extents. This is **AI-assisted preliminary visual/geometry evidence**, not an independent human review or safety certification inspection.

| Original annotation ID | Original box `xyxy` pixels (approx.) | Proposed wearer | Visual/geometry observation | Equipment class certainty | Status |
|---|---|---|---|---|---|
| `K` | `[347.73,245.45,369.55,266.59]` | `P002` background worker | Box lies near the background worker's lower leg and shoe region, with limited detail from distance/occlusion | `UNKNOWN` (no safety-rating evidence) | `MATCHED_CANDIDATE` only; human check pending |
| `L` | `[272.50,273.25,296.23,295.78]` | `P001` foreground worker | Box lies near the rightward foreground boot/foot region; shoe appears present, protection standard cannot be determined | `UNKNOWN` (no safety-rating evidence) | `MATCHED_CANDIDATE` only; human check pending |
| `M` | `[201.58,273.25,233.75,294.89]` | `P001` foreground worker | Box lies near leftward foreground boot/foot region; shoe appears present, protection standard cannot be determined | `UNKNOWN` (no safety-rating evidence) | `MATCHED_CANDIDATE` only; human check pending |

The association proposals use person/foot region proximity and coarse visual alignment. Because the original image is only 500×330, no footwear certification marks, toe protections or safety-standard conformance can be independently verified. The old dataset's `Safety Boots` label must **not** be treated as approved ground truth for certified safety footwear. No site/task footwear mandate is documented; `POLICY_UNKNOWN` remains.

**Required researcher check before approval:** view the original, zoom each box, trace both feet of P001 and visible foot/feet of P002, confirm each item's wearer if possible, and record whether footwear is observable but safety-grade unknown. If a clear wearer still cannot be identified, choose `UNKNOWN` for the association too rather than accepting the AI proposal. Neither the K/L/M person matches nor the per-worker Safety Boots `PRESENT` state is signed off.

**Review fields (not yet answered by researcher):** `K_person: ______`; `L_person: ______`; `M_person: ______`; `Safety-grade evidence: UNKNOWN unless independently supplied`; `Reviewer/date: ______`. Case B still `PENDING`, and the corresponding Roboflow Eval Case must remain `incomplete`.


## Researcher preliminary decision — boots K, L, M (2026-11-17)

**Source:** Explicit researcher statement in chat: “لا أستطيع تأكيد ارتباط الأحذية K وL وM بالأشخاص. أبقِ روابطها UNKNOWN وسجّل قراري كإفادة أولية.” The researcher cannot confirm which person wears each of the three items; this is an **initial decision**, not case-wide approval, and it does not establish that the original source image was re-reviewed by the researcher.

| Annotation | Eval pre-review item ID | Researcher preliminary association | Confirmed wearer | Safety-grade status | Prior AI proposal, for historical trace only |
|---|---|---|---|---|---|
| `K` | `E007` | `UNKNOWN` | `null` | `UNKNOWN` | `P002 / MATCHED_CANDIDATE` — unapproved |
| `L` | `E008` | `UNKNOWN` | `null` | `UNKNOWN` | `P001 / MATCHED_CANDIDATE` — unapproved |
| `M` | `E009` | `UNKNOWN` | `null` | `UNKNOWN` | `P001 / MATCHED_CANDIDATE` — unapproved |

**Interpretation:** `UNKNOWN` here means insufficient evidence to confirm wearer identity, **not** a verified `AMBIGUOUS` tie between specific workers, and not absence of PPE. Neither visual safety-class certification nor mandatory site/task PPE policy is verified. Keep `POLICY_UNKNOWN`. The current researcher statements supersede AI geometric matches for review decisions; do **not** claim three correct associations or per-worker PPE compliance.

**Outstanding review for Case B:** Independently inspect the image and any missed persons/items, confirm or revise PPE visual states, record source/privacy/rights and source-family checks, supply reviewer evidence and review date, and perform final sign-off. This is not a complete human reference: Roboflow Eval Case B must remain `groundTruthState=incomplete` with no approved ground truth. Source labels/splits/model are untouched.


## Whole-image person and PPE completeness matrix handoff (2026-11-17)

Read-only Roboflow source-image review has now yielded a **six-PPE-type per visible person** checklist covering 7 AI-visible persons across four Train images (42 review cells), plus 26 old positive PPE-labeled boxes and 14 absence-marker annotations. This is not a human-adjudicated inventory and does not include asserted misses found by a researcher. Detailed per-worker draft: [`RESEARCHER_FULL_INVENTORY_REVIEW_V01.md`](RESEARCHER_FULL_INVENTORY_REVIEW_V01.md); machine-readable checklist with old source annotation IDs and explicit 4 preliminary researcher `UNKNOWN` decisions: [`RESEARCHER_FULL_INVENTORY_MATRIX_V01.json`](RESEARCHER_FULL_INVENTORY_MATRIX_V01.json).

For **each** row the researcher should verify person completeness (including missed figures), item class and physical visibility, visually owned wearers, separately visual `PRESENT / ABSENT / UNKNOWN`, task PPE mandate and source rights/privacy. No generated `P?`/`A?` code can be copied as approved truth merely because it is in the matrix. Case A has hands/feet outside crop; Case B has small/distant P002, old glove annotations and unconfirmed footwear ownership; Case C has a partial vest on P004 and red glove J unresolved; Case D has no visible persons and an unworn hard hat.

**Status remains PENDING for 4/4 cases.** Researcher preliminary ownership `UNKNOWN` for B/K/L/M and C/J is preserved, as are unapproved historic AI geometric candidates. No original annotation saves, no model changes, no per-worker compliance judgment, no Validation/Test inference and no new training occurred.


## Researcher confirmation of visible-person counts (2026-11-17)

The researcher explicitly confirmed in chat: **"نعم صحيح كل شي A=1، B=2، C=4، D=0"**, in direct response to the question whether the four images' visible-person counts are correct. Scope of the answer is **person-count confirmation**; it does **not** constitute approval of all PPE inventory, equipment ownership, worker PPE visual states, completeness of source provenance, workplace mandates, or independent image annotation review.

| Case | Filename | Researcher-confirmed visible-person count | Count review | Complete reference sign-off |
|---|---|---:|---|---|
| A | `image_604.jpg` | **1** | `COUNT_CONFIRMED` | `PENDING` |
| B | `000760.jpg` | **2** | `COUNT_CONFIRMED` | `PENDING` |
| C | `Kathiah Gets a Chance03.jpg` | **4** | `COUNT_CONFIRMED` | `PENDING` |
| D | `h1.jpg` | **0** | `COUNT_CONFIRMED` | `PENDING` |

**Preserved researcher unknown decisions:** glove `C/J` and footwear `B/K,L,M` remain `UNKNOWN` in preliminary association, without confirmed wearer. Future human review still needs equipment presence/absence and owner adjudication, missed physical PPE, rights/privacy/source-family checks, documented task policy (default `POLICY_UNKNOWN`) and final case approval. Roboflow Eval Dataset remains `groundTruthState=incomplete`; do not promote only a count confirmation to a complete scientific benchmark.


## Case A researcher confirmation of visible PPE observations (2026-11-17)

Researcher replied "تمام هي صح" when asked whether the listed Case A / image_604.jpg / P001 observations were correct. This explicitly confirms ONLY six preliminary visual observations; it does not approve the complete ground-truth case or independently establish a PPE safety standard.

| PPE type | Confirmed preliminary visual state | Caveat |
|---|---|---|
| Hard hat | `PRESENT` | Yellow hat visible; certification and task mandate unknown |
| High-visibility vest | `PRESENT` | Vest visible; protective grade and mandate unverified |
| Protective eyewear (source class Goggles) | `PRESENT` | Clear eyewear visible; specific rating unknown |
| Face mask | `ABSENT` | Nose/mouth uncovered; this is NOT a policy-violation judgment |
| Gloves | `UNKNOWN` | Hands outside crop |
| Safety boots | `UNKNOWN` | Feet outside crop; safety-grade not established |

Scope: preliminary researcher assessment of visual PPE states only; per-object wearer matching, rights/source family, person/PPE exhaustiveness, task PPE policy remain open. Keep `POLICY_UNKNOWN` and Roboflow Eval Case A `groundTruthState=incomplete` / `groundTruth={}` until complete evidence and sign-off.


## Case B helmets and gloves — AI-only source-image recheck (2026-11-17)

Read the actual existing Roboflow Train image `000760.jpg` (500×330) and six current old annotation boxes (`Hard Hat` 3/4; `Gloves` 6/7/9/A), using a validated read-only pass-through workflow. Findings below remain **AI-assisted proposals only**. The researcher has not yet explicitly confirmed helmet or glove states.

| Worker | Helmet visual state (AI proposal) | Gloves visual state (AI proposal) | Evidence / scope |
|---|---|---|---|
| `P001` (foreground) | `PRESENT` | `PRESENT` | Blue helmet-like head protection worn, two yellow glove-like objects by raised hand and near torso; old boxes 3/6/7 are possible item associations, not approved human matches |
| `P002` (background) | `PRESENT` | `UNKNOWN` | Blue/purple headgear visibly worn; old glove boxes 9/A at small, partially obscured hands are insufficient to confirm whether gloves are worn or attached |

Old glove annotations `9/A` remain candidates in original source labels, **not established physical presence**. No certified PPE grade or documented task requirement is inferred. Existing researcher decisions on boots `K/L/M` are preserved as ownership `UNKNOWN` (no confirmed wearer), with boot safety certification `UNKNOWN`; do not change those on the basis of geometric proximity.

**Researcher prompt (subsequently answered; see confirmation below):** Does the researcher agree with visual states `P001: helmet PRESENT, gloves PRESENT`; `P002: helmet PRESENT, gloves UNKNOWN`? Researcher can keep any state UNKNOWN, or correct it after inspecting the actual source image. Item-level source-box wearer mapping is a **separate** decision.

**Case B sign-off:** `PENDING` — Source and person inventory, other PPE types, source family/rights/privacy, task mandate, and second-review remain incomplete. Roboflow Eval ground truth must remain empty / `incomplete`.


## Researcher confirmation of Case B helmet and glove visual states (2026-11-17)

The researcher explicitly replied **"صح كل شي"** to a narrowly scoped question listing the following four Case B / `000760.jpg` visual states. This is the researcher's preliminary visual-state affirmation, **not** proof of source-box-to-person item associations, PPE certification, site mandate, or complete image ground truth.

| Worker | PPE | Researcher-confirmed visual state | Evidence limit |
|---|---|---|---|
| `P001` foreground | Hard hat | `PRESENT` | Blue helmet-like headgear appears worn; safety certification not independently proved |
| `P001` foreground | Gloves | `PRESENT` | Yellow glove-like hand protection appears visible |
| `P002` background | Hard hat | `PRESENT` | Blue/purple helmet-like headgear appears worn |
| `P002` background | Gloves | `UNKNOWN` | Low resolution and partly obscured hands |

Preserve earlier researcher provisional person-association decisions: boots `K`, `L`, `M` are `UNKNOWN` with `person_id=null`; safety-boot protective grade `UNKNOWN`. Glove source annotations `9/A` remain historically unverified; their source boxes have **not** been matched or approved by the researcher. Remaining PPE types (vest, eyewear, face mask, boot state) and source rights/privacy/source-family checks still require review. Keep all workplace mandates at `POLICY_UNKNOWN`, and Case B in Roboflow at `groundTruth={}` / `incomplete`.
