# Scene- and object-family overlap audit — 2026-10-29

**Source:** Researcher's Y-PPE nine-class, 1,778-image ZIP from connected Drive; images were inspected locally and **are not uploaded to GitHub**.  
**Status:** VISUAL OVERLAP FOUND; independent-site/scene gate **NOT CLOSED**.  
**Scope:** This is a more sensitive second pass, not a replacement for provenance-based audit.

## Methods
1. Read all 1,778 JPEGs and compute 64-bit pHash using grayscale LANCZOS resampling to 32×32, orthonormal 2D DCT and median threshold on the low-frequency 8×8 block excluding the DC cell from the median.
2. Enumerate all image pairs across the three original ZIP partitions, and screen at Hamming distance <=4,6,8,10,12.
3. Manually inspect all cross-partition pHash<=8 candidates (10 pairs: 5 train–test, 2 valid–test, 3 train–valid), conservatively distinguishing same scene / near-identical product image from superficial similarities in different product photographs.
4. Audit raw `no_helmet` class annotation count for the affected distinct test images.

## pHash candidate pair counts (screening, NOT ground-truth leakage)
| Comparison | <=4 | <=6 | <=8 | <=10 | <=12 |
|---|---:|---:|---:|---:|---:|
| train–test | 1 | 2 | 5 | 12 | 23 |
| valid–test | 0 | 1 | 2 | 5 | 9 |
| train–valid | 0 | 3 | 3 | 10 | 39 |

## Visual adjudication at pHash<=8
- **Train–test:** 4 of the 5 candidate **pairs** visibly depict the same scene at slightly different moments, or the same exact product photograph with cropping/transform differences. These involve **3 distinct test images**; the fifth pair depicts different goggle products and is **not confirmed leakage**.
  - Same outdoor masonry construction scene, train versus test (pHash distance 4).
  - Same construction worker in rock-pile scene, two train frames versus the same test frame (distances 6 and 8).
  - Same blue-black safety-boot product photograph with small framing differences, train versus test (distance 8).
- **Train–valid:** 2 of the 3 pairs depict the same construction scene or the same boot photograph. One pair depicts different goggle products.
- **Valid–test:** 2 screened pairs depict different goggle products or helmets of different colors; no match was confirmed visually.
- Affected three distinct test image label files contain **0 `no_helmet` annotations**. The test has 14 such annotations overall, but that count is *not* an independent confirmed violation sample.

## Quarantine sensitivity, **not a new official split**
Preserving the source ZIP intact, the three visually related unique test images account for **15 object labels** (2 person, 2 helmet, 2 gloves, 2 vest, 6 boots, 1 goggles, 0 no_helmet). Excluding these three images *as a temporary sensitivity screen* changes the test denominator from **186 to 183 images**, and object-label count from **693 to 678**; test `no_helmet` remains **14 boxes in 12 images**, but their independence remains unproved.

The two visually related unique validation images account for **8 object labels** (1 person, 1 helmet, 2 gloves, 1 vest, 3 boots, 0 no_helmet). Their temporary removal would change validation counts from **356 to 354 images** and **2,122 to 2,114 boxes**. **No adjusted evaluation was run.** Do not treat these screened candidates as a finalized versioned, leak-free dataset.

## Research consequence
- The current 186-image test partition must **NOT** be described as fully independent of training or as proving cross-site generalization.
- Temporarily quarantine the **3 identified test images** (and any further correlated source family images discovered later). Do **not** silently delete or rewrite the original frozen dataset or erase the original test reference.
- Re-audit by source/video/session family, preserve a correction manifest and immutable dataset derivation hash; then retest method comparisons only on a documented eligible evaluation population.
- Although the limited screen found three test images, absence of matches at pHash<=8 **does not** rule out more severe scene overlap under larger viewpoint, lighting or camera changes.
- Product photo duplicates and actual construction-scene overlap should be **reported separately**; both matter for generic object-detection independence, but product photos may be irrelevant to worker-level site-safety evaluation.

## Distinguish existing Stage 2/h9 freeze
Earlier repository Stage 2/Stage 4 documented source-family leakage corrections and clean derivatives. **This audit concerns a separately packaged 1,778-image RF-DETR nine-class ZIP**; do not assume its manifest is the same as the earlier 2,288-image cleaned Y-PPE version. A prior clean-dataset declaration must not be transplanted to an unverified artifact.

## Privacy and reproducibility
No original images, identities, or private collection metadata are embedded in this public audit record. Reproducible pHash computation script: [tools/phash_overlap_audit.py](tools/phash_overlap_audit.py). This audit used a particular ZIP artifact: future claims require archive/checksum provenance and recorded pair-wise review decisions.
