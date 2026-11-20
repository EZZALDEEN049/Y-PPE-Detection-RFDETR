# SEER-PPE — Case B human-review handoff (21 Nov 2026)

**Read-only reviewer intake — decisions not invented, no Roboflow edits.** Case B `000760.jpg` (Train Source ID `0xxsYWiz1FZBYERolu4z`), in Eval Dataset `9c2679df-f2b9-4e25-b88d-9c6ac9033a95` at saved revision **2**.

**Preserved:** four researcher-final matched source PPE→worker links; original boxes `9/A/K/L/M` stay wearer-owner `UNKNOWN`. There are two existing worker records (`P001`, `P002`). Missing state rows are **not** already `UNKNOWN`, and are certainly not evidence of `ABSENT`.

## Four explicit person×PPE questions

| Worker | PPE | Current Eval status | Evidence to inspect in source photo |
|---|---|---|---|
| `P001` | `face_mask` | **MISSING_REVIEW** | Foreground worker; verify actual visible nose/mouth and whether mask region can be assessed without relying on 'No Face Mask' detector class. |
| `P001` | `safety_boot` | **MISSING_REVIEW** | Foreground worker; old source boxes L/M have human-final UNKNOWN wearer ownership, and visible footwear cannot establish certified safety grade. |
| `P002` | `face_mask` | **MISSING_REVIEW** | Smaller/rear worker; face visibility may be limited by scale or occlusion; do not infer absence from no detection. |
| `P002` | `safety_boot` | **MISSING_REVIEW** | Rear worker; old source box K human-final UNKNOWN wearer ownership; visually distinguish ordinary shoes and verified safety-grade footwear. |

### Review procedure

1. Identify each worker and the relevant face/feet region in the **original Train photo**, preferably before looking at predicted labels. Note crop, pose and visibility.
2. After human assessment, enter a **worker-level visual state** `PRESENT`, `ABSENT` or `UNKNOWN` **with justification**. For footwear, safety certification is a separate question that may remain unknown even when footwear is clearly worn.
3. Keep item ownership evidence separate from PPE visibility: boxes `K/L/M` ownership remain unconfirmed, so they cannot be reassigned to `P001`/`P002` using geometric overlap alone.
4. Keep **task/site mandate `POLICY_UNKNOWN`** until an applicable dated requirement is documented. Even a genuine visual `ABSENT` is *not* by itself a PPE policy violation.
5. Complete `source_review` and person/item completeness audit for all A–D independently; do not change a Case's Eval state to `complete` before explicit curator approval.

## Reviewer entry form (not yet filled)

| Worker/PPE | Review decision | Evidence and visibility | Reviewer & review date |
|---|---|---|---|
| `P001:face_mask` | **Pending** | Pending | Pending |
| `P001:safety_boot` | **Pending** | Pending | Pending |
| `P002:face_mask` | **Pending** | Pending | Pending |
| `P002:safety_boot` | **Pending** | Pending | Pending |

[Machine-readable unfilled review sheet](CASE_B_HUMAN_REVIEW_HANDOFF_2026-11-21_V01.json) · [Live source-status audit](PERSON_PPE_LIVE_READINESS_2026-11-21_V01.md) · [Human-reference issue #18](https://github.com/EZZALDEEN049/Y-PPE-Detection-RFDETR/issues/18).
