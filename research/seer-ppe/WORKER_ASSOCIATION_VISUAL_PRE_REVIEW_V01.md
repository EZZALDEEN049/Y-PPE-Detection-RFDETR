# SEER-PPE — four-case visual pre-review & researcher sign-off queue
**Date:** 2026-11-17 | **Status:** `AI_ASSISTED_PROPOSALS_ONLY` — NOT approved human ground truth

This document records AI visual inspection of four **original** Roboflow Train images. Source box coordinates were read from the existing Roboflow annotation geometry; the human-reference dataset is deliberately **still 0/4 complete**. It is unsafe to rebrand these suggestions as independently reviewed ground truth, new SEER algorithm performance, or worker compliance.

## Visually observed case inventory

| Case | Image | Visible people (AI) | PPE-labeled positive boxes in old annotations | Original absence-marker boxes | Main researcher adjudication |
| --- | --- | ---: | ---: | ---: | --- |
| A | `image_604.jpg` | 1 | 3 | 1 | Verify helmet, goggles, vest wearer; uncovered nose/mouth; hands/feet outside crop |
| B | `000760.jpg` | 2 | 9 | 3 | Separate foreground/background ownership and gloves; distinguish ordinary work footwear from **certified** safety boots |
| C | `Kathiah Gets a Chance03.jpg` | 4 | 13 | 10 | Four helmets/reflective garments; check far-right reflective patch; distinguish glove `J` between P003 and P004 |
| D | `h1.jpg` | 0 | 1 | 0 | Standalone yellow hard hat; no wearer visible; keep ownership `UNKNOWN` |

**Summary:** 7 visually observed people, 26 original positive PPE-labeled objects proposed for item review, and 14 original *No ...* labels excluded from physical PPE inventory. The 26 are **not 26 verified PPE items** and not a new accuracy measurement. `Pants` and `No Safety Attire` have no automatic PPE policy verdict. The PPE approval/certification of work boots cannot be read directly from the photo.

## Suggested per-worker visual-state review (not human-confirmed)

### Case A — one person
- `P001`: hard hat `PRESENT`, goggles `PRESENT`, reflective vest `PRESENT`, face mask `ABSENT` (nose and mouth visible without one), gloves and safety boots `UNKNOWN` because hands/feet are out of frame.
- Positive item proposals: old annotation `1` vest → P001; `2` goggles → P001; `3` hard hat → P001. Review the visual item type and ownership before treating any as `MATCHED`.
- Source/task mandate `POLICY_UNKNOWN`: do **not** label a face-mask violation solely because the face is uncovered.

### Case B — two people
- `P001` (foreground, left): helmet visible, gloves visible; safety vest, safety-boot rating, and face-mask state unresolved. Suggested old annotation IDs: hard hat `3`, gloves `6` and `7`, footwear boxes `L` and `M`.
- `P002` (background, right): helmet visible, glove details/torso/face/footwear remain uncertain because person is small or partly occluded. Suggested old IDs: hard hat `4`, gloves `9` and `A` (confirm visually), footwear box `K` (safety rating unverified).
- `No Safety Vest` labels `N` and `O` are *old annotation markers*; these are not human-confirmed worker PPE absence or policy violations.

### Case C — four people from left to right
- `P001`: yellow hard hat, high-visibility vest, red gloves visible; face mask/boots unresolved.
- `P002`: yellow hard hat, high-visibility vest, red glove(s) visible; face mask/boots unresolved.
- `P003`: yellow hard hat and reflective vest visible; glove attribution needs care because adjacent hands/arms are close; face mask/boots unresolved.
- `P004`: yellow hard hat visible; only a partial reflective segment is clear and may not establish a complete safety vest; glove assignment and face/boots unresolved.
- Particularly inspect original glove annotation `J` (`Gloves`, near between P003 and P004). Its preliminary label is `AMBIGUOUS_CANDIDATE` with alternatives `P003,P004`. **This is not an algorithmic `AMBIGUOUS` output, nor an adjudicated truth label.**
- The four old `No Safety Boots` and two `No Face Mask` labels are excluded from actual absence judgments until independently visually confirmed; no task mandate has been provided.

### Case D — standalone item
- No person is visible. One physical yellow hard hat (`E001`) is a detached/unworn item. Proposed association: `UNKNOWN_CANDIDATE`, `person_id=null`. This checks an orphan-item branch; it is **not** evidence of PPE absence on any worker.

## Item-level working record
The JSON file [`WORKER_ASSOCIATION_AI_VISUAL_PRE_REVIEW_V01.json`](WORKER_ASSOCIATION_AI_VISUAL_PRE_REVIEW_V01.json) includes every originally annotated positive PPE candidate box with stable within-case `E###` IDs, normalized image coordinates, source annotation IDs, suggested `MATCHED_CANDIDATE`/`AMBIGUOUS_CANDIDATE`/`UNKNOWN_CANDIDATE`, per-worker proposed visual states, and all old negative-marker boxes separately. The record is marked `human_verified:false` throughout.

## Human single-curator sign-off protocol
1. In the existing Roboflow source image, perform a fresh human pass **without assuming the model annotations are correct**. Record people missed by original `Persons` boxes, occlusion, cropped body parts, and any real positive PPE items missed.
2. Assign item-to-person ownership based on tracing the item to the wearer's head/torso/hand/foot, not just geometric IoU. Explicitly keep `AMBIGUOUS` for competing people and `UNKNOWN` for orphan/insufficient evidence.
3. For every visible worker × PPE type, decide `PRESENT`, `ABSENT`, `UNKNOWN` using visual criteria. Record evidence. Do not confuse detector `No ...` with observed absence, or no detection with absence.
4. Keep all task/site PPE mandates `POLICY_UNKNOWN` unless documentation makes a specific item `REQUIRED` or `NOT_REQUIRED` for that person, task, site, and date.
5. Review rights/privacy/source-family group before permitting public image sharing or statistical evaluation.
6. Save approved review only in the **separate** Eval Dataset (`9c2679df-f2b9-4e25-b88d-9c6ac9033a95`), with real curator/date and evidence. Do not click **Save** in the source-image annotation editor unless you explicitly intend to change the original dataset. Completion of each Eval Case requires real review, not these AI suggestions.

**Stop condition:** Until researcher sign-off, `groundTruthState=incomplete` for all 4 Cases; no v0.3 association-quality evaluation, Validation calibration, old Test benchmarking, violations, or XAI/energy metrics are justified.
