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


## Case B — researcher clarification on vests, eyewear, boots and trousers (2026-11-17)

**Direct researcher statement (Arabic):** "لا يوجد سترات عاكسه والنظرات غير لم تشاهد بسبب وضعية العاملين احذية السلامة موجوده احدكها يلبس بنطلون والاخر لا الذي هو الامامي".

Interpretation bounded by what the researcher stated:

| Image B observation | P001 foreground | P002 background | Research status |
|---|---|---|---|
| Reflective/safety vest | `ABSENT` | `ABSENT` | Researcher reports no reflective vests; still preliminary visual state, not violation |
| Protective eyewear | `UNKNOWN` | `UNKNOWN` | Not discernible from worker postures |
| Safety footwear | `UNKNOWN` at worker level | `UNKNOWN` at worker level | Researcher says safety footwear is visible **somewhere in image**; item ownership remains uncertain and no protective standard independently verified |
| Trousers (not a PPE compliance outcome) | Researcher reports **not wearing trousers** | Researcher reports **wearing trousers** | Clothing context only, not a safety violation |

**Preserved prior association statement:** Source old safety-boot boxes `K`, `L`, `M` all remain `UNKNOWN`, `person_id=null`. An image-level statement that boots are present does not establish which worker owns each item. Historical geometric matches are not approved labels. Source-model label `Safety Boots` is not an independently verified certification mark. Face-mask states are not addressed by this turn and remain `UNKNOWN` for both persons. The headgear/glove states already confirmed by the researcher remain P001 hard hat PRESENT, gloves PRESENT; P002 hard hat PRESENT, gloves UNKNOWN.

**Remaining review:** old source annotation `Pants` is a garment-category context only; PPE source boxes must be matched separately to visible wearers; privacy/rights/source-family and workplace PPE policy remain unreviewed (`POLICY_UNKNOWN`). This chat response does **not** sign off all reference data. Keep Roboflow Eval Case B `groundTruth={}` and `groundTruthState=incomplete`.


## Case C — researcher reports all four workers' PPE and traditional abaya (2026-11-17)

**Researcher statement (Arabic):** "جميعهم لديهم خوذات وسترات وقفازات واحذيه سلامه ولديهم لبس شعبي العباءه". This addresses **Case C** / `Kathiah Gets a Chance03.jpg` with four researcher-confirmed visible persons; it reports helmets, reflective vests, gloves, safety boots, and traditional abaya outerwear for **all four**.

| Visible PPE / clothing | P001 | P002 | P003 | P004 | Research scope and limitation |
|---|---|---|---|---|---|
| Hard hat (visual) | `PRESENT` | `PRESENT` | `PRESENT` | `PRESENT` | Researcher person-level visual report; helmet certification not independently verified |
| Reflective vest (visual) | `PRESENT` | `PRESENT` | `PRESENT` | `PRESENT` | Including vest of far-right P004, previously partial/AI-uncertain |
| Gloves (person-level visual state) | `PRESENT` | `PRESENT` | `PRESENT` | `PRESENT` | Does NOT confirm who wears source glove annotation `J` |
| Safety boots (researcher visual report) | `PRESENT` | `PRESENT` | `PRESENT` | `PRESENT` | Researcher reports boots; occlusion and actual protective certification remain unverified |
| Traditional outerwear `العباءة` | reported worn | reported worn | reported worn | reported worn | Contextual garment; not a PPE item or violation by itself |

**Critical preservation:** The earlier explicit researcher decision on glove `J` / `E012` remains `UNKNOWN` with `person_id=null`. Four workers reportedly wearing gloves does **not** prove which individual's glove is boxed by annotation `J`. Similarly the person-level boot report does not establish exact boot-object associations, independent footwear safety certification, or worker policy compliance. Eye protection and face-mask states are still `UNKNOWN` unless separately assessed. `POLICY_UNKNOWN` continues to apply without a documented task/site mandate.

**Status:** preliminary researcher observations only; 16 person×PPE states reported for Case C (4 people × 4 types), no completed item-level association review, no rights/source-family evidence or final research approval. Case C Roboflow Eval `groundTruth={}` and `groundTruthState=incomplete` must be preserved, as must the original model, annotations and splits.


## Case C — non-visible eyewear and face masks (researcher confirmation, 2026-11-17)

Asked whether goggles and face masks can be clearly seen for all four Case C workers or should remain UNKNOWN because of worker poses and partially obscured faces. The researcher answered **"لم ترى"** (not visible). This is an explicit **visual non-observability statement**, NOT confirmation of absence.

| Worker | Eyewear | Face mask | Interpretation |
|---|---|---|---|
| `P001` | `UNKNOWN` | `UNKNOWN` | Neither item discernible enough to determine wear |
| `P002` | `UNKNOWN` | `UNKNOWN` | Neither item discernible enough to determine wear |
| `P003` | `UNKNOWN` | `UNKNOWN` | Neither item discernible enough to determine wear |
| `P004` | `UNKNOWN` | `UNKNOWN` | Neither item discernible enough to determine wear |

No source `No Face Mask` annotation, lack of detection, or unseen eyes/mouth shall be converted into an `ABSENT` reference without direct anatomical evidence. Previous person-level helmet, vest, glove and boot observations remain in force, as does the researcher's `UNKNOWN` wearer decision for original glove `J` / `E012`. The four cases remain `incomplete` until source-rights/privacy, source-group and full item-association review and sign-off. `POLICY_UNKNOWN` unchanged.


## Case D — researcher confirms standalone helmet and no visible worker (2026-11-17)

**Researcher statement:** Answered **"نعم"** when asked whether Case D (`h1.jpg`) has only a standalone **yellow hard hat** and **zero visible people wearing it**. This is a preliminary researcher-confirmed image-content observation, not approval of complete ground truth.

| Review component | Researcher preliminary result | Meaning |
|---|---|---|
| Visible persons | `0` | Previously confirmed in the 4-image person-count check |
| Physical hard-hat instance | `1`, `PRESENT` as standalone item | Old positive source annotation ID `1`; not PPE being worn by an observed worker |
| Wearer association | `UNKNOWN`, `person_id=null` | No visible person to attach the helmet to |
| Worker PPE/compliance outcome | **Not applicable** | No missing-PPE or violation event inferred from a standalone helmet |
| PPE certification / worksite policy | `UNKNOWN` / `POLICY_UNKNOWN` | Image provides neither independent grade evidence nor site task rules |

Original source annotations/training/model/splits are unchanged. Rights/privacy/source-family and final evidence review remain outstanding; Roboflow Eval Case D must remain `groundTruth={}` and `groundTruthState=incomplete`. **Do not increase the 38 person×PPE visual-state confirmations:** this image has zero people and only one individually acknowledged orphan equipment item.


## Automated item-level geometry/semantic audit handoff (2026-11-17)

Native read-only Roboflow annotation boxes were checked against the evolving researcher inventory matrix, producing two **non-gold reference artifacts**: [per-source-box review queue](ITEM_LEVEL_ASSOCIATION_REVIEW_QUEUE_V01.md) and [machine-readable audit](ITEM_LEVEL_ASSOCIATION_EVIDENCE_AUDIT_V01.json).

**26 physical-PPE-labeled boxes** are classified as 19 historic unverified AI wearer candidates, 2 additional B rear-glove-box AI uncertainties (`9/A`), and 5 preliminary UNKNOWN wearer items (researcher B boots `K/L/M`, researcher C glove `J`, and researcher-confirmed standalone helmet D `1` with no depicted wearer). **Zero** item-level wearer relationships have independent explicit researcher approval at this stage.

**14 negative / absence-like boxes** remain separate. Researcher reports boots on all four Case C workers but native old labels include `No Safety Boots` `Q/R/S/T` and **no positive Safety Boots boxes** in C. This is a source-label/evidence disagreement requiring item inspection, not automatic proof that either source or researcher is wrong. Likewise, the old broad `No Safety Attire` markers do not establish PPE-specific violations. Case B `No Safety Vest` labels agree with the user's initial absence observations but are not independently approved ground truth.

**Next human item-level adjudication start:** Case A source boxes `1` (Safety Vests), `2` (Goggles), `3` (Hard Hat) were associated provisionally by AI with the one visible worker `P001`. Researcher has already confirmed the relevant **visual PPE states**, but **has not yet explicitly approved each old box's precise wearer**. Ask for a separate item-to-person judgment, with `UNKNOWN` still available. Document researcher decision as provisional until source/privacy/final-case approval.

Keep original project annotations/model/splits and baseline Workflows unchanged; `0/4` Roboflow Eval Cases remain incomplete. No model correctness/performance/violation claims.


## Case A — FINAL researcher visual and item-attribution approval (2026-11-17)

**Researcher explicit final approval:** After being asked to approve original item-to-person links `1` (vest), `2` (goggles), `3` (hard hat) to Case A `P001`, the researcher answered **"نعم ويعتبر اعتماد نهاي للصورة الصورة ليس فيها قناع فقط اما الحالات الاخر غير ظاهرة لان الصورم مقصوصه"**. This constitutes **FINAL HUMAN APPROVAL FOR IMAGE A VISIBLE PERSON COUNT, THE THREE INDIVIDUAL ITEM-TO-P001 LINKS, AND SIX PPE VISUAL STATES**. Do not downgrade this to another *AI suggestion*.

| Researcher-final finding | Value | Evidence boundary |
|---|---|---|
| Visible worker | `P001` only | 1 visible person |
| Original source box `1` / vest `E001` | `MATCHED -> P001` | Researcher-final item linkage |
| Original source box `2` / goggles `E002` | `MATCHED -> P001` | Researcher-final item linkage; product rating unknown |
| Original source box `3` / hard hat `E003` | `MATCHED -> P001` | Researcher-final item linkage |
| Face mask visual status | `ABSENT` | Nose/mouth uncovered; **NO violation inference** |
| Gloves visual status | `UNKNOWN` | **Hands cropped out**; not absent |
| Safety boots visual status | `UNKNOWN` | **Feet cropped out**; not absent |
| Site/task mandate | `POLICY_UNKNOWN` | No independent site safety requirement provided |

**Two distinct approval scopes:** (1) the researcher has **finally approved this image's visible semantics and three wearable-item wearer links**; (2) **research source-rights/privacy/source-family clearance, complete source documentation, independent second-pass checks and actual Eval Case readiness remain pending**. Consequently Roboflow Eval `groundTruthState` must remain `incomplete` until its separate required evidence gates are satisfied. The human's final visual approval should **not** be erased by this administrative/scientific readiness gate.

The existing historical baseline training images, classes and boxes, splits, model weights and Workflows remain untouched. No measured PPE compliance, association accuracy, Validation/Test or product safety certification has been asserted.


## Case A Roboflow Eval partial human-reviewed reference saved (2026-11-17)

After the researcher's **final visual approval**, the **separate** Roboflow Eval Case `8f7cce94-d46e-4fac-9a0a-641bcd1f12c8` was updated atomically (revision `1 -> 2`) and re-read successfully. Stored typed ground-truth arrays: 1 `persons`, 3 `ppe_items`, 6 `worker_ppe_states`, 3 `associations` with status `MATCHED` and person `P001`, and 6 `task_mandates`, each `POLICY_UNKNOWN`. Worker PPE: hard hat/vest/goggles `PRESENT`, face mask `ABSENT`, gloves/boots `UNKNOWN` (hands/feet outside crop).

**Critical:** this is a *partial, researcher-final visual and attribution reference*, not full ready-to-score Eval ground truth. The source-review label was **deliberately left unset**, because rights/privacy/source-family and second review remain pending. `groundTruthState=incomplete` retained. Other three cases B/C/D still have unapproved full ground truth. The result must not be used to claim scientific model performance or compliance.


## Case B original-box helmet/glove wearer adjudication packet (2026-11-17)

The requested **item-level helmet and glove audit** was performed using the read-only original image plus original Roboflow 500×330 saved box coordinates. Full [Case B wearer-review packet](CASE_B_ITEM_LEVEL_HELMET_GLOVE_REVIEW_V01.md) lists each box, evidence and limits.

**AI-only candidate links (not researcher-final approval):** `Hard Hat 3→P001`, `Hard Hat 4→P002`, `Gloves 6→P001`, `Gloves 7→P001`; rear `Gloves 9/A` are `UNKNOWN_CANDIDATE` from the current AI source-image review, not verified physical glove ownership. Earlier confirmed **worker-level** visual states stay unchanged: P001 helmet/gloves PRESENT, P002 helmet PRESENT/gloves UNKNOWN.

The researcher's previous **boot person-ownership decisions B/K,L,M remain UNKNOWN** (`person_id=null`) and are not reopened. Researcher has not yet given **any box-level final match approval for Case B**; its separate Roboflow Eval `groundTruth={}` / `incomplete` status is preserved. Do not promote proposals to gold or amend training annotations.


## Case B final researcher item-link decisions (2026-11-18)

In direct response to the explicitly itemized question, the researcher said **"نعم اعتمد"**. **Final approved original source box → visible worker associations:** `3 (Hard Hat) → P001`, `4 (Hard Hat) → P002`, `6 (Gloves) → P001`, `7 (Gloves) → P001`.

**Reaffirmed/confirmed owner UNKNOWN:** Gloves `9/A` and Safety Boots `K/L/M` are all `UNKNOWN`, `person_id=null`. The original glove labels on small background boxes `9/A` do **not** establish that gloves can be reliably seen on P002; the researcher's person-level glove state for P002 remains `UNKNOWN`. Protective boot certification and per-boot ownership are unknown. Prior person-level notes (both reflective vests ABSENT, goggles UNKNOWN, masks UNKNOWN, scene-level footwear seen, trousers differences) remain unchanged.

These decisions are **final for each specified item-owner link/unknown status only**, not whole Case B researcher ground truth or legal/privacy/source clearance. Safety site policy remains `POLICY_UNKNOWN`; no workplace violation inferred. Source label geometry, base model, annotations and splits unchanged. Full item packet: [Case B item-level helmet/glove review](CASE_B_ITEM_LEVEL_HELMET_GLOVE_REVIEW_V01.md).


## Roboflow Case B partial researcher-approved association reference (2026-11-18)

Case B in the separate Roboflow Eval Dataset was saved at **revision 2**, with four user-final `MATCHED` box-to-worker associations, two source person entries, four human-approved source PPE item candidates, eight human-confirmed visual PPE states, and eight `POLICY_UNKNOWN` task-mandate entries. The five old source boxes `9/A/K/L/M` remain human-confirmed **owner UNKNOWN**, documented in GitHub and not inserted as approved physical PPE items into Roboflow ground truth. The source class on `9/A` remains physically unconfirmed.

**Readback verified** `groundTruthState=incomplete` and `source_review` unset; full task/context requirements, source rights and independent second pass are pending. Other cases were not changed, and the original data/model remain frozen.


## Case C original-box helmet/vest/glove review packet (2026-11-18)

Read the original C source image (2048×1365) read-only and reconciled 13 positive PPE boxes against the four workers. Created [Case C item-level review packet](CASE_C_ITEM_LEVEL_HELMET_VEST_GLOVE_REVIEW_V01.md).

**AI-only proposed owner links — NOT researcher-final:** hats `F→P001`, `E→P002`, `D→P003`, `C→P004`; reflective vests `6→P001`, `5→P002`, `7→P003`, `8→P004` (P004 garment partly obscured); gloves `H/I→P001`, `G→P002`, `K→P003`. Source glove `J` remains researcher's preliminary `UNKNOWN`, `person_id=null`. No new human signoff has been given for the other 12 box links.

Researcher already reports four people wearing helmets, vests, gloves, boots and traditional `العباءة`. Original source has four `No Safety Boots` boxes `Q/R/S/T` but zero positive boot boxes; this is a review priority, not an automatic false-negative or violation finding. Eye protection and masks remain `UNKNOWN`; site policy `POLICY_UNKNOWN`, rights/privacy/source family `UNREVIEWED`.

Roboflow Eval Case C remains `groundTruthState=incomplete` / `groundTruth={}`. No original annotations, splits, model or base Workflow changed.


## Case C researcher-final individual source-box wearer decisions (2026-11-18)

The researcher replied **"موافق"** after the exact twelve box-to-worker links were displayed and asked to be approved, with source glove `J` expressly kept `UNKNOWN`. These **twelve individual links are now human-final**, rather than AI suggestions: hats `F→P001`, `E→P002`, `D→P003`, `C→P004`; vests `6→P001`, `5→P002`, `7→P003`, `8→P004`; gloves `H/I→P001`, `G→P002`, `K→P003`. **Glove `J`: final owner `UNKNOWN`, `person_id=null`.**

Finality applies to **person-owner relationships only**. Worksite policy `POLICY_UNKNOWN`, safety-boot protective certification and old negative `No Safety Boots` tags `Q/R/S/T` are not settled; goggles/masks remain visual `UNKNOWN`. Source rights/privacy/family and independent verification prevent full Roboflow Eval completion. No changes to original annotations/training.


## Case C partial approved source-item reference saved to Roboflow (2026-11-18)

Separate Roboflow Eval Case C was saved at **revision 4** following the explicit researcher approval of 12 item-box wearer links. Typed partial reference: **4** visible people, **12** approved positive PPE source item boxes, **12** `MATCHED` box-to-person links, **24** pre-confirmed worker-level visual PPE states (6 PPE types × 4 people), and **24** `POLICY_UNKNOWN` mandates. The old `J` glove box, whose person owner is researcher-final `UNKNOWN`, is retained in GitHub but excluded from the approved positive-item subset in this incomplete Eval Case pending full identity/coverage checks.

No source review record was fabricated; `source_review` remains unset and Eval `groundTruthState=incomplete`. Old four C `No Safety Boots` source markers `Q/R/S/T` still need reconciliation with researcher's claimed boot presence; rights/privacy/source-family/independent second-pass checks are still pending. No compliance verdict or measured model score.


## Case C read-only source `No Safety Boots` Q/R/S/T audit (2026-11-18)

Performed read-only inspection of the **actual** Roboflow source image and four original native `No Safety Boots` boxes for Case C. Detailed evidence: [Arabic audit](CASE_C_BOOT_ABSENCE_LABEL_AUDIT_V01.md) and [machine-readable source-box audit](CASE_C_BOOT_ABSENCE_LABEL_AUDIT_V01.json). Geometric centre-to-*old source person bbox* mapping is `Q→P004`, `R→P003`, `S/T→P001`, and no box-centre for `P002`. This is **not** wearer attribution or proof of physical boot presence/absence; four markers are not four independent worker violations.

Old Case C source has **zero positive `Safety Boots` boxes**, while the researcher previously asserted `safety_boot=PRESENT` for each of four workers. This has been explicitly classified `OPEN_UNRESOLVED_SOURCE_LABEL_SEMANTICS`, not a proven mislabeling, false-negative, failed prediction, or safety non-compliance. The historical source class meaning, footwear protection specification and independent person-foot visual status require separate verification. **No original label corrected or deleted**.

Prior human link approvals (19 A/B/C physical item links), C/J owner `UNKNOWN`, B/K,L,M ownership `UNKNOWN`, person-level PPE observations and `POLICY_UNKNOWN` are preserved; the separate Eval Case C remains `incomplete` pending source rights/privacy/family, full coverage and second-pass signoff.


## Case C source-class provenance and native-pixel boot crop follow-up (2026-11-18)

Inspected read-only original pixel crops around `Q`, `R`, `S/T` and independent `P002` worker context via a validated Roboflow `AbsoluteStaticCrop` Workflow, without saving a Workflow or writing an annotation. `Q` has a partly visible tan footwear-like region beneath seated worker clothing; `R` has a light-coloured shoe-like area on the leaning worker's foot; `S/T` show tiny pale regions near P001's long hem and ground. The crops cannot establish a protective safety standard or prove absence of safety footwear.

Roboflow project metadata lists `No Safety Boots` (552 annotations in class counts) but provides no original labeling rubric. Annotation job `nzrZTe9Jg5Camjn4npwO` says the job was created when the project was forked; no original parent provenance or authoritative negative-boot definition was available in the inspected metadata. Another repo's strict `No Safety Boots -> no_boots` cross-domain mapping is **to be audited**, not source instructions.

**OPEN / SOURCE_CLASS_SEMANTICS_UNKNOWN**. Detailed evidence: [Arabic report](CASE_C_BOOT_SOURCE_SEMANTICS_AND_CROPS_V01.md) and [machine-readable record](CASE_C_BOOT_SOURCE_SEMANTICS_AND_CROPS_V01.json). Retained researcher's four visual boot PRESENT reports, 19 accepted item-wearer matches, glove C/J and boot B/K/L/M UNKNOWN owners, and original labels unchanged. No proven annotation error, boot-grade certification, policy violation or model accuracy is inferred.
