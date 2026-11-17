# SEER-PPE — item-level attribution and legacy-label integrity audit v0.1

**Date:** 2026-11-17 | **Type:** AI-assisted read-only evidence triage, **not human-approved reference or scientific accuracy**.

## Verified inputs and scope

Original Roboflow native annotation boxes (4 Train images) were checked against the separate [human review matrix](RESEARCHER_FULL_INVENTORY_MATRIX_V01.json), including item IDs, source class, geometry, source person-box membership, historic AI wearer proposals, and explicit provisional researcher statements. There was **no change** to original labels, images, splits, trained model, deployments, or base Workflow.

| Audit category | Count | Interpretation |
|---|---:|---|
| Original source positive PPE boxes | **26** | Candidate physical items, not independent verified ground truth |
| Researcher preliminary owner `UNKNOWN` or no visible wearer | **5** | B `K/L/M`, C `J`, D standalone `1` — remain unassigned |
| Additional glove-box uncertainty identified by AI | **2** | B `9/A` — old `Gloves` labels do not prove rear gloves are worn |
| Other historic AI candidate matches awaiting item-level human review | **19** | Do not automatically promote to `MATCHED` |
| Old absence-like annotation boxes | **14** | Not physical PPE; not proof of noncompliance |
| Approved box-to-worker attributions | **0** | Person-level visual confirmation is a **different variable** |
| Roboflow human-complete Eval Cases | **0/4** | Cases remain `groundTruth={}` / `incomplete` |

The `5 + 2 + 19 = 26` categories are **item-level review routing states**, not measured model detection/association performance. The 38 previously affirmed person×PPE visual-state observations and one confirmed D standalone item remain separate. A positive item can be worn visually while its particular source annotation is not reliably attributable. Protective certification, where applicable, is not independently established by these pixels.

## Item-by-item reviewer queue

Columns: **old box** = ID in original Roboflow training source; **historic AI target** = unapproved assistant hypothesis only; **triage status** = current decision for what to review, never scored ground truth.

### Case A — `image_604.jpg`

One visible person; wearer of each old boxed item still requires explicit item-level review

| Old box | Equipment class | Historic AI wearer | Current item-level status | Reviewer focus |
|---|---|---|---|---|
| `1` / `E001` | Safety Vests | `P001` | `PENDING — AI candidate only` | Worker visual-state PRESENT; source box still unconfirmed |
| `2` / `E002` | Goggles | `P001` | `PENDING — AI candidate only` | Worker visual-state PRESENT; source box still unconfirmed |
| `3` / `E003` | Hard Hat | `P001` | `PENDING — AI candidate only` | Worker visual-state PRESENT; source box still unconfirmed |

Old absence-like source markers: `5` (No Face Mask).

### Case B — `000760.jpg`

Two visible people; rear gloves and three boots need special review

| Old box | Equipment class | Historic AI wearer | Current item-level status | Reviewer focus |
|---|---|---|---|---|
| `3` / `E001` | Hard Hat | `P001` | `PENDING — AI candidate only` | Worker visual-state PRESENT; source box still unconfirmed |
| `4` / `E002` | Hard Hat | `P002` | `PENDING — AI candidate only` | Worker visual-state PRESENT; source box still unconfirmed |
| `6` / `E003` | Gloves | `P001` | `PENDING — AI candidate only` | Worker visual-state PRESENT; source box still unconfirmed |
| `7` / `E004` | Gloves | `P001` | `PENDING — AI candidate only` | Worker visual-state PRESENT; source box still unconfirmed |
| `9` / `E005` | Gloves | `P002` | `UNKNOWN? — AI source recheck` | Rear worker hand small/occluded; review and allow UNKNOWN — AI_SOURCE_RECHECK_COULD_NOT_CONFIRM_REAR_GLOVES, P002_GLOVE_VISUAL_UNKNOWN |
| `A` / `E006` | Gloves | `P002` | `UNKNOWN? — AI source recheck` | Rear worker hand small/occluded; review and allow UNKNOWN — AI_SOURCE_RECHECK_COULD_NOT_CONFIRM_REAR_GLOVES, P002_GLOVE_VISUAL_UNKNOWN |
| `K` / `E007` | Safety Boots | `P002` | `UNKNOWN — researcher/no wearer` | Preserve prior researcher UNKNOWN; do not force MATCHED — RESEARCHER_OWNER_UNKNOWN, SAFETY_GRADE_UNVERIFIED |
| `L` / `E008` | Safety Boots | `P001` | `UNKNOWN — researcher/no wearer` | Preserve prior researcher UNKNOWN; do not force MATCHED — RESEARCHER_OWNER_UNKNOWN, SAFETY_GRADE_UNVERIFIED |
| `M` / `E009` | Safety Boots | `P001` | `UNKNOWN — researcher/no wearer` | Preserve prior researcher UNKNOWN; do not force MATCHED — RESEARCHER_OWNER_UNKNOWN, SAFETY_GRADE_UNVERIFIED |

Old absence-like source markers: `8` (No Safety Attire); `N` (No Safety Vest); `O` (No Safety Vest).

### Case C — `Kathiah Gets a Chance03.jpg`

Four visible workers; source boots absence markers conflict with researcher visual reports

| Old box | Equipment class | Historic AI wearer | Current item-level status | Reviewer focus |
|---|---|---|---|---|
| `5` / `E001` | Safety Vests | `P002` | `PENDING — AI candidate only` | Worker visual-state PRESENT; source box still unconfirmed |
| `6` / `E002` | Safety Vests | `P001` | `PENDING — AI candidate only` | Worker visual-state PRESENT; source box still unconfirmed |
| `7` / `E003` | Safety Vests | `P003` | `PENDING — AI candidate only` | Worker visual-state PRESENT; source box still unconfirmed |
| `8` / `E004` | Safety Vests | `P004` | `PENDING — AI candidate only` | Worker visual-state PRESENT; source box still unconfirmed |
| `C` / `E005` | Hard Hat | `P004` | `PENDING — AI candidate only` | Worker visual-state PRESENT; source box still unconfirmed |
| `D` / `E006` | Hard Hat | `P003` | `PENDING — AI candidate only` | Worker visual-state PRESENT; source box still unconfirmed |
| `E` / `E007` | Hard Hat | `P002` | `PENDING — AI candidate only` | Worker visual-state PRESENT; source box still unconfirmed |
| `F` / `E008` | Hard Hat | `P001` | `PENDING — AI candidate only` | Worker visual-state PRESENT; source box still unconfirmed |
| `G` / `E009` | Gloves | `P002` | `PENDING — AI candidate only` | Worker visual-state PRESENT; source box still unconfirmed |
| `H` / `E010` | Gloves | `P001` | `PENDING — AI candidate only` | Worker visual-state PRESENT; source box still unconfirmed |
| `I` / `E011` | Gloves | `P001` | `PENDING — AI candidate only` | Worker visual-state PRESENT; source box still unconfirmed |
| `J` / `E012` | Gloves | `—` | `UNKNOWN — researcher/no wearer` | Preserve prior researcher UNKNOWN; do not force MATCHED — RESEARCHER_OWNER_UNKNOWN, BOX_CENTER_IN_PERSON_GAP_NEEDS_REVIEW |
| `K` / `E013` | Gloves | `P003` | `PENDING — AI candidate only` | Worker visual-state PRESENT; source box still unconfirmed |

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

1. For each of the **19 historic AI matches**, independently identify the visible body wearer *and original item box*; request the researcher's explicit per-item approval, correction, or `UNKNOWN`. The six images' previous worker-level present/absent reports do not suffice as box-level matches.
2. Resolve, or explicitly retain, the **seven review-priority uncertain items** (B `9/A`, B `K/L/M`, C `J`, D `1`). Prior researcher's `UNKNOWN` remains the operative preliminary decision for B `K/L/M`, C `J`, and D unworn item; B `9/A` remain AI-only uncertainties.
3. Revisit the **14 absence-like markers** separately from positive PPE. For C, compare the four `No Safety Boots` and four broad `No Safety Attire` markers with actual visible PPE, and document what each old class intended.
4. Exhaustively look for *unboxed physical PPE*: most notably the four pairs of boots the researcher reports in C despite **zero positive `Safety Boots` source boxes**. Do not invent box coordinates or create training annotations.
5. Before setting `groundTruthState=complete`, finish item coverage, source rights/privacy/source family, documented worksite task mandates (or explicit `POLICY_UNKNOWN`), independent review pass and case-level researcher approval in the **separate Roboflow Eval Dataset** only.

## Supporting machine-readable audit

[`ITEM_LEVEL_ASSOCIATION_EVIDENCE_AUDIT_V01.json`](ITEM_LEVEL_ASSOCIATION_EVIDENCE_AUDIT_V01.json) includes 26 item records (original annotation ID/normalized coordinates, historic candidate, researcher preliminary decision, a geometry-only check, source annotation match, and next review action) plus the 14 negative-marker records. Center containment is geometry only: it cannot prove ownership, especially for reaching, occluded or truncated body parts.
