# SEER-PPE V05 — human source-family adjudication handoff (83 Valid IDs)

**Why this exists:** The frozen **83 unique Valid review Source IDs** from the Train/Valid mixed filename/site/embedding queue need an explicit **human photographic-source family** judgment before being eligible as independent evidence. This handoff does **not** invent human decisions, automatically exclude any new Valid Source or reopen the five prior holds. It preserves the original Roboflow data/splits and never accesses Test.

The [machine-readable queue](SOURCE_FAMILY_REVIEW_QUEUE_2026-11-21_V05.json) includes all **83** Valid Source IDs, prior queue rank/priority/reasons, top three Train neighbors, the five existing holds, and the newly measured **three** original-byte/RGB comparisons.

## Highest-priority handoff examples (prior five holds + strongest new signals)

| Valid Source | Top Train neighbor | Review bucket | Original byte/pixel evidence | Independent-source verdict |
|---|---|---|---|---|
| `cf8fc8d6c849430e927fd6fa13b6ba79.jpg` | `cf8fc8d6c849430e927fd6fa13b6ba79.jpg` | Prior hold | Original pixel pair not yet measured | **Pending** |
| `IMG-20250416-WA0063.jpg` | `IMG-20250416-WA0067.jpg` | Prior hold | Original pixel pair not yet measured | **Pending** |
| `d3febe75f2cb4cb5875ff430dcdb2b95.jpg` | `d3febe75f2cb4cb5875ff430dcdb2b95.jpg` | Prior hold | Original pixel pair not yet measured | **Pending** |
| `IMG-20250416-WA0026.jpg` | `IMG-20250416-WA0079.jpg` | Prior hold | Original pixel pair not yet measured | **Pending** |
| `IMG-20250416-WA0051.jpg` | `125182753_5333001493392670_6503923738393063554_n.jpg` | Prior hold | Original pixel pair not yet measured | **Pending** |
| `Safety-Glasses-Toolbox-Talk.jpg` | `image_719.jpg` | High-sim review | Original pixel pair not yet measured | **Pending** |
| `Sapi 7_mp4-223.jpg` | `Sapi 7_mp4-224.jpg` | High-sim review | Original pixel pair not yet measured | **Pending** |
| `v126.jpg` | `v125.jpg` | High-sim review | Original pixel pair not yet measured | **Pending** |
| `v141.jpg` | `v140.jpg` | High-sim review | Original pixel pair not yet measured | **Pending** |
| `construction-worker-wearing-safety-equipment-19672694.jpg` | `image_798.jpg` | High-sim review | Original pixel pair not yet measured | **Pending** |
| `h39.jpg` | `h34.jpg` | High-sim review | Original pixel pair not yet measured | **Pending** |

## Human decision protocol (to be applied case-by-case, not guessed by AI)

For every Valid source in the machine queue: inspect the original Valid image and candidate Train Source originals side by side, check distinctive objects/marks/background, and record any independent acquisition/site/session provenance already supported by evidence. Decide whether it is the exact image, decoded pixel match, derivative of one original, same source session/site, same product in different photography, independently acquired, or genuinely uncertain. Store evidence and a reviewer signoff. **Different SHA/dHash values do not establish independent source.**

For the three V05 original-file comparisons, raw SHA-256 and RGB SHA-256 mismatch; they **remain unreviewed human source-family candidates**. Use dHash distances **11, 29, 18** as descriptive signals, not clearing thresholds. Five earlier holds remain research holds even if image pixels differ.

This queue concerns **source independence only**, not whether hard hats, masks, boots, gloves or vests are compliant with a site safety policy. The Person–PPE Eval Cases and Test remain sealed/unchanged.

## Research status

- Total frozen Valid queue: **83**, including **5** prior specific research holds.
- New source-family human decisions: **0**.
- New pixels measured in this continuation: **6 original Source images / 3 pairs**, not the full 2,093.
- Complete source-image audit launched separately; its success must be verified before changing any counts.
- Scientific scoring authorization: **false**.
