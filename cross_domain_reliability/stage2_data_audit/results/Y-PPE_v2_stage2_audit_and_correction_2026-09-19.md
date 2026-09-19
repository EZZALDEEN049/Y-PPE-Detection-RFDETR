# Y-PPE Version 2 — Stage 2 Source-Level Audit and Correction Decision

**Date:** 2026-09-19  
**Roboflow source:** `master-fylfq/altayyar-0oflt-lafos-qqauz-ty5nh`, Version 2  
**Export:** YOLOv11  
**Status:** **SOURCE COUNTS VERIFIED; CORRECTION REQUIRED BEFORE EXPERIMENTS**

## 1. Source dataset recovered successfully

Version 2 contains the original non-augmented split:

- Train: **1625 images**, **11897 instances**
- Validation: **468 images**, **3492 instances**
- Test: **234 images**, **1131 instances**
- Total: **2327 images**, **16520 instances**

These counts, including every class count in all three splits, exactly match the controlled Y-PPE split documented for the thesis benchmark. This resolves the earlier Version-1 count discrepancy: Version 1 was the augmentation-expanded export, whereas Version 2 restores the 1,625-image source training split.

## 2. Remaining integrity findings

The core audit reported **109 issues**, of which **2 are critical audit flags**. The two critical flags are two representations of the same underlying leakage event: `ppe_0466` is byte-identical and pixel-identical between Train and Test.

Issue counts:
- 1 cross-split exact-byte duplicate
- 1 cross-split exact-pixel duplicate
- 38 cross-split perceptual near-duplicate candidates
- 68 raw exact duplicate annotation rows
- 1 near-identical same-class box pair (IoU = 0.996149)

## 3. Near-duplicate adjudication

The Version-2 near-duplicate manifest is exactly the same set of 38 source-image pairs previously reviewed visually:
- **21 confirmed leakage**
- **7 not leakage**
- **10 uncertain product/source-family pairs**

For split freezing, the 10 uncertain helmet/product-family pairs are handled conservatively as one source family across splits. This is a precautionary grouping rule, not a claim that the images are proven duplicates.

## 4. Explicit source-video leakage

Three media groups span multiple splits and must be kept within a single split:

- `43_MOV`: Test 1, Validation 1
- `RPReplay_Final1667001201_MP4`: Test 1, Train 3
- `Sapi-7_mp4`: Test 2, Train 5, Validation 4

Using locked-split priority `Test > Validation > Train`, the conservative combined correction manifest contains:
- **39 source images to exclude** from lower-priority splits
  - Train: **30**
  - Validation: **9**
- **26 higher-priority source images retained** as references

If applied without replacement, the corrected split sizes would be approximately:
- Train: **1595**
- Validation: **459**
- Test: **234** (locked)

## 5. Annotation cleanup

Version 2 confirms that most Version-1 annotation duplication was augmentation-related in count amplification, but the raw source still contains real duplicates:
- **68 exact duplicate bbox rows**, all in Train and each occurring twice; remove one extra copy per group.
- **1 near-identical Safety Vests pair** in `pos_653...` (rows 1 and 2, IoU 0.996149); visual overlay confirms the same object, so retain row 1 and remove row 2.

Total confirmed source-level annotation-row removals: **69**.

## 6. Decision

Do **not** train the harmonized Q1 experiments on Version 2 as-is.

The next clean/frozen dataset should:
1. apply the conservative file correction manifest;
2. deduplicate the 68 exact annotation rows;
3. remove row B from the confirmed `pos_653` near-identical pair;
4. preserve the current Test set identities and remove lower-priority source-family/video copies;
5. rerun Stage 2 on the cleaned derivative;
6. complete semantic geometry review for `No Hard Hat`, `No Gloves`, and `No Safety Boots` before freezing the 9-class harmonized ontology.

No augmentation should be introduced during this correction/audit step.
