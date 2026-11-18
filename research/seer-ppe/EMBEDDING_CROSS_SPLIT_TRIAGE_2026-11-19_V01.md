# SEER-PPE — Roboflow visual-embedding cross-split candidate screen (v0.1)

**Date:** 2026-11-19 | **Status:** `EMBEDDING_TRIAGE_ONLY_NOT_PIXEL_HASH_VERIFICATION`

## Coverage and safeguards
Read-only RoboQL indexed-image query from `softyyemen/altayyar-0oflt-lafos-qqauz`: Train **1625**, Valid **468**; embeddings **768-d**; cosine scores for **760500** Train–Valid candidate pairs.
**No Test image, Test embedding, or Test label was requested.** No model inference, annotation edit, split change, or training was performed.

Roboflow's embedding version is unspecified by the API response. Similarity measures appearance/semantics and is **not a cryptographic hash or a pixel-level duplicate test**. Scores may be high for different photos from the same scene or for generic products. The threshold counts below are descriptive only; they are **not** auto-duplicate labels, not estimated leakage rates, and not a new validation eligibility policy.

## Exploratory highest-score neighbor counts

| Minimum cosine score | Valid items with at least one Train neighbor |
|---:|---:|
| ≥ 0.999 | 0 |
| ≥ 0.995 | 1 |
| ≥ 0.99 | 4 |
| ≥ 0.98 | 7 |
| ≥ 0.95 | 52 |
| ≥ 0.9 | 192 |

## Pre-registered earlier visually reviewed pairs

| Valid file | Train file | Cosine similarity |
|---|---|---:|
| `cf8fc8d6c849430e927fd6fa13b6ba79.jpg` | `cf8fc8d6c849430e927fd6fa13b6ba79.jpg` | 0.980171 |
| `d3febe75f2cb4cb5875ff430dcdb2b95.jpg` | `d3febe75f2cb4cb5875ff430dcdb2b95.jpg` | 0.896492 |
| `IMG-20250416-WA0063.jpg` | `IMG-20250416-WA0067.jpg` | 0.906803 |
| `IMG-20250416-WA0026.jpg` | `IMG-20250416-WA0079.jpg` | 0.881212 |
| `IMG-20250416-WA0033.jpg` | `IMG-20250416-WA0048.jpg` | 0.846469 |

## Highest-ranked Train–Valid candidates (descriptive)

| Rank | Valid image ID / filename | Nearest Train image ID / filename | Cosine |
|---:|---|---|---:|
| 1 | `HRYvLu8UFRgGlQQoJN7G` — `Safety-Glasses-Toolbox-Talk.jpg` | `nhXMHxaCM0f7kNLOKU8Z` — `image_719.jpg` | 0.998663 |
| 2 | `sPdt3S9xyB3XzrWa3DaE` — `Sapi 7_mp4-223.jpg` | `x4li7ZpEZqRlWEFBMom3` — `Sapi 7_mp4-224.jpg` | 0.99238 |
| 3 | `FamTszkxp5aOfuAcZwtn` — `v126.jpg` | `ol5tvzeJJtiq9Ng0oFqC` — `v125.jpg` | 0.99105 |
| 4 | `V7nP50xtllhmv7ex0OZf` — `v141.jpg` | `8vE1Ov0KTilzHRh7gtpq` — `v140.jpg` | 0.990562 |
| 5 | `qealvsJAhBFs6A668kak` — `construction-worker-wearing-safety-equipment-19672694.jpg` | `ngf3QT4XU6cS6p2Kegzy` — `image_798.jpg` | 0.985266 |
| 6 | `rjjkVbdcd3dCIoxywUJE` — `h39.jpg` | `y1pL7pvPcML2CbzYYqdy` — `h34.jpg` | 0.982068 |
| 7 | `qBtfzUgi6Mpg3A5TE0ln` — `cf8fc8d6c849430e927fd6fa13b6ba79.jpg` | `NAzs8sLreuFWQeOYDa2w` — `cf8fc8d6c849430e927fd6fa13b6ba79.jpg` | 0.980171 |
| 8 | `VoxtMSBDU2XW3WLRyUtx` — `v99.jpg` | `930aFf45w1CvKrfYoonN` — `v74.jpg` | 0.979143 |
| 9 | `K1hITffRQtdL69x6W3WF` — `image_1372.jpg` | `jOqfE2KetI3hANjQbkDZ` — `image_1342.jpg` | 0.978564 |
| 10 | `DXPjbo9xT1UjLzOkeB6l` — `v16.jpg` | `24DyXrfQsknLjzqUaQZm` — `v15.jpg` | 0.978558 |
| 11 | `DiNSDQBhYtmZBBYx92JU` — `pos_401.jpg` | `2ct5Jp59ACtQ0hbkUJxB` — `pos_440.jpg` | 0.975313 |
| 12 | `nDva2lsHrXl7UAgGq2Nx` — `h54.jpg` | `w9VxWK9GW7fmH4J6ATFo` — `h46.jpg` | 0.974638 |
| 13 | `XKxOHVSOitlv2lbJPtv7` — `v10.jpg` | `lGItUWeUToGtFQuK1VBj` — `v28.jpg` | 0.974201 |
| 14 | `RmZzo1PiJ1OCVI9ziOuW` — `v103.jpg` | `KnYaRNvLntDoIrN5bOuv` — `v104.jpg` | 0.973859 |
| 15 | `pDFh3U4Tpa9rB1fYWGOQ` — `h38.jpg` | `DNfkZRQDetlemze06T6r` — `h36.jpg` | 0.972941 |
| 16 | `A3hFGqTOFfC4VH2IA1Lt` — `------12-_png.jpg` | `w8Ja8qHQTcfvAnJ7VRbg` — `------12-_png.jpg` | 0.972618 |
| 17 | `4NJYe4cbpEy8uCopUQq3` — `1000_F_685781687_mFglvrw8421PMRPg8UzaVLGbnBCiVsBk.jpg` | `OPDPeBipt6t4OLusdkc7` — `1000_F_685781708_okbs0gJJ2GhCdFIfJlmcNhndvhJoz8pn.jpg` | 0.972596 |
| 18 | `zs0ICbiboEbpAnE4v5ff` — `h47.jpg` | `EDSDuokCx8gyug1gAruj` — `h53.jpg` | 0.970356 |
| 19 | `INAgeZi7bwiF5utRk97U` — `------6-_png.jpg` | `mUj7WmfxH9Vbb23nIdyi` — `------6-_png.jpg` | 0.968764 |
| 20 | `Z1vJiJW0OnVZMlr0SIvJ` — `v19.jpg` | `lGItUWeUToGtFQuK1VBj` — `v28.jpg` | 0.967865 |
| 21 | `exRlvnSBoSB4EW71NGaf` — `87.jpg` | `oKrokq5e0WLBBB7relPM` — `93.jpg` | 0.967592 |
| 22 | `DvuTj6lOacAoKGpbzDTF` — `472863178_122158768826320679_4044938397851373251_n.jpg` | `AVkS5L1lYndBMr5TBHrm` — `472701427_122158768796320679_3383190418969739057_n.jpg` | 0.966324 |
| 23 | `SlMNfdbpvClsUZin1RcK` — `v150.jpg` | `RXPMol7W1P613i0j9iJz` — `v149.jpg` | 0.965398 |
| 24 | `7S5o6ul4Q1LlmNiVs4mC` — `v105.jpg` | `elAhEYrK2fTQcWn78ck6` — `v96.jpg` | 0.965274 |
| 25 | `QNy1J29vY62jBvRJLZcv` — `v95.jpg` | `Jdnwl2WNEp2b5jo4WA9h` — `v12.jpg` | 0.963208 |
| 26 | `028d8mXwFsIucPHX2qeu` — `v124.jpg` | `ol5tvzeJJtiq9Ng0oFqC` — `v125.jpg` | 0.962995 |
| 27 | `g4Mlhl0AUNtsmolYc1CW` — `76.jpg` | `M5eZeyBnh7ovew4nTpmL` — `77.jpg` | 0.962123 |
| 28 | `grt6fZBL0Z050Ov9p2Do` — `20.jpg` | `AmiD6dzDEWAVUi9qNeFl` — `19.jpg` | 0.96079 |
| 29 | `MK8ALewnMHJpsuyZRVdw` — `------6-_png.jpg` | `mUj7WmfxH9Vbb23nIdyi` — `------6-_png.jpg` | 0.960427 |
| 30 | `0Rdh8tDdfnRtMMldwpae` — `image_211.jpg` | `ZZVGcNOOZzsUbuoZSv29` — `image_1139.jpg` | 0.958732 |

## Interpretation and next evidence

1. Cross-check candidate pairs against earlier site-family and shoe-source holds; keep those holds unchanged.
2. Acquire **original image bytes**, indexed by unique Roboflow image ID (not filename alone), and compute SHA-256 plus decoded-pixel perceptual signatures (pHash/dHash). Track byte-identical, pixel-identical, near-image, shared-site, and visually distinct as separate verdicts.
3. Confirm near-duplicate flags with two-person or documented researcher review when material to evaluation; never promote embedding rank alone to a leakage finding.
4. Establish independently adjudicated Person–PPE gold data before scoring; do not reopen Test to tune a threshold.

Full per-Valid top-three neighbor register: [JSON](EMBEDDING_CROSS_SPLIT_TRIAGE_2026-11-19_V01.json).

**Retained prior status:** five specific source/site-related Valid holds; independent validation and final scoring remain blocked.
