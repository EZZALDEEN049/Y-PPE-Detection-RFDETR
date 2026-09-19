# Stage 4 Harmonized Dataset Freeze — Closure

**Date:** 2026-09-20  
**Status:** CLOSED successfully before any harmonized model training.  
**Successful GitHub Actions run:** `35476544896` (`Stage 4 Harmonized Dataset Freeze #2`)  
**Head commit used by the successful run:** `fb20f78fba4ed2731980cb7a22692f4fb69ecacb`

## Frozen shared ontology

The benchmark is frozen to nine canonical classes, in this exact order:

0. `person`
1. `helmet`
2. `gloves`
3. `vest`
4. `boots`
5. `goggles`
6. `no_helmet`
7. `no_gloves`
8. `no_boots`

No historical 17-class Y-PPE result may substitute for a new harmonized nine-class baseline.

## Y-PPE-h9 frozen derivative

Clean split sizes preserved from Stage 2:

- train: **1,595 images**, **8,304 retained shared-class instances**
- validation: **459 images**, **2,500 retained instances**
- test: **234 images**, **814 retained instances**
- total retained shared-class instances: **11,618**

Class totals over all splits:

- person: 2,351
- helmet: 1,959
- gloves: 1,310
- vest: 1,391
- boots: 1,608
- goggles: 826
- no_helmet: 256
- no_gloves: 1,373
- no_boots: 544

Y-PPE polygon accounting is closed and exact:

- polygon rows seen in the cleaned 17-class source: **436**
- retained shared-class polygon rows converted to enclosing axis-aligned boxes: **309**
- polygon rows dropped because their classes are outside the shared ontology: **127**
- invariant: `436 = 309 + 127`

Frozen derivative fingerprint:

`db49295a0ef2c9eec73b14c620966ed00bf12dac253866b65bab9b50af9db896`

## Construction-PPE-h9 frozen derivative

Clean split sizes preserved from Stage 2:

- train: **1,077 images**, **7,767 retained shared-class instances**
- validation: **134 images**, **984 retained instances**
- test: **141 images**, **1,153 retained instances**
- total retained shared-class instances: **9,904**

Class totals over all splits:

- person: 2,180
- helmet: 1,671
- gloves: 1,339
- vest: 1,553
- boots: 1,518
- goggles: 487
- no_helmet: 485
- no_gloves: 556
- no_boots: 115

Construction-PPE has no polygon rows in the pinned official source used here. The two nonshared classes `none` and `no_goggle` were excluded, accounting for 1,205 dropped instances.

Frozen derivative fingerprint:

`bd706ae34aa77507f119a9a4d5cd443d4cb84ee6cd2020b9b8ee6e086350880e`

## Integrity and leakage gates

Both harmonized derivatives passed the Stage 2 structural audit with **0 critical issues**.

- Y-PPE-h9 source/video cross-split groups: **0**
- Construction-PPE-h9 source/video cross-split groups: **0**
- missing label files: **0** for both derivatives
- canonical class order read from `data.yaml`: correct for both derivatives
- target test images were not opened for visual adjudication during Stage 3 or Stage 4

Residual dHash candidates reported by the generic audit are previously adjudicated noncritical visual false positives and do not represent confirmed cross-split leakage.

## Stage 4 technical correction history

Run #1 failed only because its invariant incorrectly required every source polygon row to be converted. That was an accounting error because nonshared-class polygons are intentionally removed with their classes. The harmonizer and workflow were corrected before Run #2 to require:

`polygon_rows_seen = polygon_rows_converted + polygon_rows_dropped_nonshared`

Run #2 passed this corrected invariant and all remaining gates.

## Training gate

Stage 4 is now closed. The next scientific stage is **harmonized in-domain baseline training** using the frozen nine-class derivatives. The primary baseline matrix must begin with:

- Y-PPE-h9 train -> Y-PPE-h9 test
- Construction-PPE-h9 train -> Construction-PPE-h9 test

for the selected architectures under one prespecified training/evaluation protocol. Only after those in-domain references are available should zero-shot cross-domain transfer be evaluated.

The frozen dataset fingerprints above must be carried into every experiment record so later runs can be traced to the exact derivative manifests used here.
