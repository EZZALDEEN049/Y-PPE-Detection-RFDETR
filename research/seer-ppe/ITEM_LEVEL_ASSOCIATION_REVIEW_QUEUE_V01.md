# SEER-PPE — item-level attribution and legacy-label integrity audit v0.1

**Date:** 2026-11-17 | **Type:** Initially AI-assisted evidence triage; Case A now has explicit final human visual/item approval; the other item links are **not** approved. No scientific accuracy result.

## Verified inputs and scope

Original Roboflow native annotation boxes (4 Train images) were checked against the separate [human review matrix](RESEARCHER_FULL_INVENTORY_MATRIX_V01.json), including item IDs, source class, geometry, source person-box membership, historic AI wearer proposals, and explicit provisional researcher statements. There was **no change** to original labels, images, splits, trained model, deployments, or base Workflow.

| Audit category | Count | Interpretation |
|---|---:|---|
| Original source positive PPE boxes | **26** | Candidate physical items, not independent verified ground truth |
| Owner `UNKNOWN` (six final and D provisional) | **7** | B `9/A/K/L/M` and C `J` human-final UNKNOWN; D standalone `1` remains preliminary UNKNOWN |
| B rear glove-box identity still unverified | **2** | `9/A` now have researcher-final `UNKNOWN` owner; whether physical gloves are visible is still unconfirmed |
| Other historic AI candidate matches awaiting item-level human review | **0** | All 12 Case C candidates have now received final researcher box-owner decisions |
| Old absence-like annotation boxes | **14** | Not physical PPE; not proof of noncompliance |
| Approved box-to-worker attributions | **19** | A three, B four, C twelve human-final source item wearer matches |
| Roboflow human-complete Eval Cases | **0/4** | Case A has typed partial adjudicated ground-truth arrays but remains `incomplete`; B/C/D have empty ground truth |

The `7 UNKNOWN owner + 0 AI-only + 19 confirmed matched = 26` mutually exclusive owner-decision categories are **item-level review routing states**, not measured model detection/association performance. The 38 previously affirmed person×PPE visual-state observations and one confirmed D standalone item remain separate. A positive item can be worn visually while its particular source annotation is not reliably attributable. Protective certification, where applicable, is not independently established by these pixels.

## Item-by-item reviewer queue

Columns: **old box** = ID in original Roboflow training source; **historic AI target** = unapproved assistant hypothesis only; **triage status** = current decision for what to review, never scored ground truth.

### Case A — `image_604.jpg`

One visible person; **researcher has finally approved original boxes 1/2/3 as MATCHED to P001**. Rights/privacy/source-family and second-pass checks remain open.

| Old box | Equipment class | Historic AI wearer | Current item-level status | Reviewer focus |
|---|---|---|---|---|
| `1` / `E001` | Safety Vests | `P001` | `MATCHED — researcher final` | Individual item wearer approved; source clearance remains open |
| `2` / `E002` | Goggles | `P001` | `MATCHED — researcher final` | Individual item wearer approved; product rating remains unknown |
| `3` / `E003` | Hard Hat | `P001` | `MATCHED — researcher final` | Individual item wearer approved; source clearance remains open |

Old absence-like source markers: `5` (No Face Mask).

### Case B — `000760.jpg`

Two visible people; researcher-final box-owner matches on `3/4/6/7`; researcher-final UNKNOWN owner for `9/A/K/L/M` (source glove identity/boot grade remain unverified).

| Old box | Equipment class | Historic AI wearer | Current item-level status | Reviewer focus |
|---|---|---|---|---|
| `3` / `E001` | Hard Hat | `P001` | `MATCHED → P001 — researcher final` | Researcher-approved item attribution; source rights/policy remain open |
| `4` / `E002` | Hard Hat | `P002` | `MATCHED → P002 — researcher final` | Researcher-approved item attribution; source rights/policy remain open |
| `6` / `E003` | Gloves | `P001` | `MATCHED → P001 — researcher final` | Researcher-approved item attribution; source rights/policy remain open |
| `7` / `E004` | Gloves | `P001` | `MATCHED → P001 — researcher final` | Researcher-approved item attribution; source rights/policy remain open |
| `9` / `E005` | Gloves | `P002` | `UNKNOWN — researcher final owner status` | The item owner is unknown; old source glove identity is not independently verified |
| `A` / `E006` | Gloves | `P002` | `UNKNOWN — researcher final owner status` | The item owner is unknown; old source glove identity is not independently verified |
| `K` / `E007` | Safety Boots | `P002` | `UNKNOWN — researcher re-affirmed` | Item owner not identified; safety-boot certification unknown |
| `L` / `E008` | Safety Boots | `P001` | `UNKNOWN — researcher re-affirmed` | Item owner not identified; safety-boot certification unknown |
| `M` / `E009` | Safety Boots | `P001` | `UNKNOWN — researcher re-affirmed` | Item owner not identified; safety-boot certification unknown |

Old absence-like source markers: `8` (No Safety Attire); `N` (No Safety Vest); `O` (No Safety Vest).

### Case C — `Kathiah Gets a Chance03.jpg`

Four visible workers; researcher now approves 12 source-item wearer matches, while J owner remains UNKNOWN. Source boot absence markers still conflict with researcher visual reports.

| Old box | Equipment class | Historic AI wearer | Current item-level status | Reviewer focus |
|---|---|---|---|---|
| `5` / `E001` | Safety Vests | `P002` | `MATCHED → P002 — researcher final` | Final wearer link approved; source certification/rights still open |
| `6` / `E002` | Safety Vests | `P001` | `MATCHED → P001 — researcher final` | Final wearer link approved; source certification/rights still open |
| `7` / `E003` | Safety Vests | `P003` | `MATCHED → P003 — researcher final` | Final wearer link approved; source certification/rights still open |
| `8` / `E004` | Safety Vests | `P004` | `MATCHED → P004 — researcher final` | Final wearer link approved; source certification/rights still open |
| `C` / `E005` | Hard Hat | `P004` | `MATCHED → P004 — researcher final` | Final wearer link approved; source certification/rights still open |
| `D` / `E006` | Hard Hat | `P003` | `MATCHED → P003 — researcher final` | Final wearer link approved; source certification/rights still open |
| `E` / `E007` | Hard Hat | `P002` | `MATCHED → P002 — researcher final` | Final wearer link approved; source certification/rights still open |
| `F` / `E008` | Hard Hat | `P001` | `MATCHED → P001 — researcher final` | Final wearer link approved; source certification/rights still open |
| `G` / `E009` | Gloves | `P002` | `MATCHED → P002 — researcher final` | Final wearer link approved; source certification/rights still open |
| `H` / `E010` | Gloves | `P001` | `MATCHED → P001 — researcher final` | Final wearer link approved; source certification/rights still open |
| `I` / `E011` | Gloves | `P001` | `MATCHED → P001 — researcher final` | Final wearer link approved; source certification/rights still open |
| `J` / `E012` | Gloves | `—` | `UNKNOWN — researcher final owner` | Person remains unidentified; do not assign P003/P004 |
| `K` / `E013` | Gloves | `P003` | `MATCHED → P003 — researcher final` | Final wearer link approved; source certification/rights still open |

Old absence-like source markers: `9` (No Safety Attire); `A` (No Safety Attire); `M` (No Safety Attire); `N` (No Safety Attire); `O` (No Face Mask); `P` (No Face Mask); `Q` (No Safety Boots); `R` (No Safety Boots); `S` (No Safety Boots); `T` (No Safety Boots).

### Case D — `h1.jpg`

Standalone item, no person — do not use as a worker violation

| Old box | Equipment class | Historic AI wearer | Current item-level status | Reviewer focus |
|---|---|---|---|---|
| `1` / `E001` | Hard Hat | `—` | `UNKNOWN — researcher/no wearer` | No visible person; leave unassigned — NO_PERSON_VISIBLE, STANDALONE_EQUIPMENT_NOT_A_WORKER_VIOLATION |

Old absence-like source markers: none.

## Important source/researcher discrepancies — triage, not a verdict

**Case C / four `No Safety Boots` original boxes `Q/R/S/T`:** Researcher reported boots visually present on all four workers, whereas old source labels are absence-like. The labels may have ambiguous semantics and the actual boot grade is not independently readable. **Do not call these four human-reviewed errors or violations without independent adjudication.** Inspect the source image, full feet/crops and original box intent; document each as `LEGACY_MARKER_CONFLICT_OPEN` until settled.

**Case C / `No Safety Attire` boxes `9/A/M/N`:** Old broad class is not synonymous with absence of every PPE type. Researcher reports helmets, vests and gloves visible. Decompose by specific PPE, do not turn this broad annotation into four worker-level `ABSENT` claims.

**Case C / `No Face Mask` boxes `O/P`:** Researcher cannot see masks or eye protection due to pose; current person-level mask states remain `UNKNOWN` for all four, and absent markers cannot override that.

**Case B / gloves `9/A`:** Old classes call these gloves; AI visual recheck could not validate small background worker's hands. Researcher confirmed P002's *person-level glove state* `UNKNOWN`; keep exact box ownership as `NOT_HUMAN_ADJUDICATED` pending visual evidence.

**Case B / footwear `K/L/M`:** Researcher reports scene-level safety footwear but explicitly cannot confirm who owns each old source boot box. Remain item-owner `UNKNOWN`; safety certification unverified; worker-level visual safety boot states remain `UNKNOWN`. Trousers are context, not PPE.

**Case D / old helmet box `1`:** User confirms one yellow loose helmet and zero workers. Item is visually present but unassigned; a loose helmet cannot support an absent-worker-helmet violation.

**Case A / old `No Face Mask` box `5` and B `No Safety Vest` `N/O`:** Consistent with corresponding researcher visual `ABSENT` states, but not independent validation of marker geometry, task rule or safety violation.

## What remains before a real Eval ground-truth reference

1. The 12 Case C old source-box wearer candidates have now received final researcher decisions. **Do not re-open owner links automatically**; prioritize independent source/right/privacy/second-pass review and unresolved original class semantics.
2. Preserve final researcher `UNKNOWN` box-owner decisions for B `9/A/K/L/M` and C `J`. D stand-alone `1` remains preliminary UNKNOWN. Review *identity* of B `9/A` glove-like boxes separately; no forced match.
3. Revisit the **14 absence-like markers** separately from positive PPE. For C, compare the four `No Safety Boots` and four broad `No Safety Attire` markers with actual visible PPE, and document what each old class intended.
4. Exhaustively look for *unboxed physical PPE*: most notably footwear of all four workers as reported by the researcher in C despite **zero positive `Safety Boots` source boxes**. Do not invent box coordinates or create training annotations.
5. Before setting `groundTruthState=complete`, finish item coverage, source rights/privacy/source family, documented worksite task mandates (or explicit `POLICY_UNKNOWN`), independent review pass and case-level researcher approval in the **separate Roboflow Eval Dataset** only.

## Supporting machine-readable audit

[`ITEM_LEVEL_ASSOCIATION_EVIDENCE_AUDIT_V01.json`](ITEM_LEVEL_ASSOCIATION_EVIDENCE_AUDIT_V01.json) includes 26 item records (original annotation ID/normalized coordinates, historic candidate, researcher preliminary decision, a geometry-only check, source annotation match, and next review action) plus the 14 negative-marker records. Center containment is geometry only: it cannot prove ownership, especially for reaching, occluded or truncated body parts.


**2026-11-17 follow-up:** Researcher has finally approved Case A links `1/2/3` to `P001` and the associated six visible PPE states (mask ABSENT; gloves/boots UNKNOWN due crop). The A source-rights/second-review gate still prevents fully complete Roboflow reference. See [the updated researcher sign-off](RESEARCHER_SIGNOFF_QUEUE_V01.md).

**Roboflow separate Eval update:** Case A revision 2 contains one researcher-approved person, three item links `MATCHED`, six visual PPE states and six `POLICY_UNKNOWN` mandates. `source_review` remains unfilled and `groundTruthState=incomplete`. This supersedes older notes that Case A still has empty ground truth.


**Focused Case B item attribution review:** The source image, original pixel boxes and researcher's earlier PPE visual-state assertions are documented in [CASE_B_ITEM_LEVEL_HELMET_GLOVE_REVIEW_V01.md](CASE_B_ITEM_LEVEL_HELMET_GLOVE_REVIEW_V01.md). Researcher box-level decisions are still pending: 3→P001, 4→P002, 6→P001, 7→P001 are AI candidate links; 9/A remain AI unknown candidates, and boots K/L/M remain researcher UNKNOWN. No added gold labels or source edits.


**2026-11-18 Case B researcher-final ownership decisions:** `3→P001`, `4→P002`, `6→P001`, `7→P001` are final MATCHED item-owner links; `9/A/K/L/M` are final owner UNKNOWN, `person_id=null`. Exact physical status of B `9/A` remains uncertain, distinct from owner unknown. Case B still incomplete in Roboflow until source/rights/second-pass gates. See [dedicated Case B packet](CASE_B_ITEM_LEVEL_HELMET_GLOVE_REVIEW_V01.md).


**Roboflow Case B import (2026-11-18):** The separate Eval Case B (revision 2) now holds **four human-approved item MATCHED associations** and **eight previously confirmed person-level visual-state entries**, still `incomplete`; physical item records `9/A/K/L/M` are excluded until identity and coverage are verifiable, while their **human-approved owner UNKNOWN** status remains explicit in GitHub. Source/privacy family and policy verification remain pending.


**2026-11-18 focus on Case C source items:** See [Case C 13-item review packet](CASE_C_ITEM_LEVEL_HELMET_VEST_GLOVE_REVIEW_V01.md): 12 candidate links are AI-only until researcher approves, and original glove `J` remains prior researcher UNKNOWN (`person_id=null`). Revisit C `No Safety Boots` Q/R/S/T separately. No original training changes.


**2026-11-18 Case C final twelve ownership links:** Researcher has approved all 12 requested C wearer links, with source glove J owner remaining UNKNOWN. Historical candidate note above was superseded; box-owner decisions are final, while source classes/rights/legacy absence markers/second pass remain unresolved. See [updated C review](CASE_C_ITEM_LEVEL_HELMET_VEST_GLOVE_REVIEW_V01.md).
