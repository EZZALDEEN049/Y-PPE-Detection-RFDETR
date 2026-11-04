# SEER-PPE progress — 2026-11-04 (master v0.3)

| Step | State | Evidence / next action |
|---|---|---|
| 01 Foundation | Design complete | Thesis ch3, Y-PPE 2,327 originals / 17 classes, historical model identified |
| 02 Hosted smoke and scaffold | Engineering complete | 3 existing Y-PPE hosted inferences, 23 synthetic module tests; not new benchmark |
| 03 Independence and object identity code | Engineering complete | New SHA/source-group gate and detection-class/IoU matching; 17 new tests; 40/40 synthetic unit tests pass |
| 04 Authoritative clean 17-class archive | OPEN | Obtain 2,288-image physical archive and verify image hashes + group provenance + visual near-duplicates |
| 05 Human worker-level ground truth | OPEN | Double-annotate persons/PPE wearing/requirements, include missed workers |
| 06 Local XAI | OPEN | Retrieve private checkpoint, verify checksum/class order and differentiated forward; hosted JSON is insufficient |
| 07 Physical energy benchmark | OPEN | Record device, idle/warmup and actual watts; no real joules yet |
| 08 Calibration and independent test | OPEN | Lock independent acquisition families and planned endpoints/constraints |
| 09 Paper results/figures | OPEN | No new empirical SEER results; keep Results explicitly empty |
| 10 Journal novelty audit/Q1 scope | OPEN | Full related-work matrix and specific journal/year/category validation |

**Data separation:** 17-class Stage-2 cleaned 2,288 ≠ nine-class 1,778 (the latter had reopened 2026-10 cross-scene audit). Historical detector training used V2 5,577 processed images.

**Development-exposed engineering IDs (cannot claim untouched final test):** `0it1WmTbAyqSVQrvVqz8`, `028d8mXwFsIucPHX2qeu`, `0ABzMrjnd6I0Ws6FH7qo`.

Full protocol, code and tests stored in private Drive: https://drive.google.com/drive/folders/16VyV63PTd1nwf1P4GM0kV-bAlnLFlZxq
