# V40 batch 02 — technical evidence and release boundaries

2026-11-24. Zero new model calls. No final packages, submission or Zenodo release.

## Artwork binary headers
13 PNGs directly fetched via GitHub base64 and IHDR/pHYs parsed. Nominal x/y 299.9994 dpi (300 rounded):
- Figure_1: 3970×2174 px.
- Figure_2: 3784×1564 px.
- Figure_3: 3784×1474 px.
- Figure_S1 through Figure_S10: each 3377×2255 px.

Original V34-B renderer validates archived values but prints source-image and target identifiers in plots. S1 text now uses pseudonyms; artwork needs new render. Candidate offline renderer deep-copies validated maps, substitutes aliases, verifies numerical arrays and ranks unchanged, and writes individual PDFs; not executed. Check all 13 files visually, remove raw identifiers where necessary, verify effective raster resolution/vector fonts at actual reproduction size, and obtain rights clearance. Existing files not approved for publication. General Elsevier guidance: https://www.elsevier.com/about/policies-and-standards/author/artwork-and-media-instructions/artwork-sizing ; https://www.elsevier.com/about/policies-and-standards/author/artwork-and-media-instructions/artwork-overview . Distinguish 300 dpi halftone, 500 combination, 1000 bitmapped line art. Full journal guide still not verified.

## Bibliography screen
All fourteen DOI identifiers have matching indexed title evidence (publisher or bibliography; not exhaustive resolver/metadata validation):
- 10.1109/DASA68193.2025.11499131; 10.1109/DASA68193.2025.11498849; 10.1109/ESMARTA70636.2026.11652079; 10.1109/ESMARTA70636.2026.11652190.
- 10.1016/j.rineng.2024.103498; 10.3390/computers15060388; 10.1016/j.engappai.2026.115725; 10.3390/jimaging12050195; 10.1109/ICCV.2017.371.
- 10.1093/biomet/30.1-2.81; 10.52202/079017-1765; 10.2307/1412159; 10.3389/fbuil.2026.1976288; 10.1016/j.aei.2026.104612.

The source contains 18 references: 14 DOI identifiers and 4 non-DOI URLs (Adebayo, Hooker, Petsiuk and Robinson).
RF-DETR official ICLR page: https://proceedings.iclr.cc/paper_files/paper/2026/hash/5bed8703db85ab27dc32f6a42f8fbdb6-Abstract-Conference.html . Final metadata, citation matching and exact guide reference style require verification.

## Technical version
Verified V38-B runner at immutable commit d76ebc595cff628f21231b45dab51170dc82b405. This is a technical anchor, not a clean public archive; do not use as final data-sharing statement until rights/metadata audit and licensing are resolved. Existing requirements-min.txt lists minimum NumPy and SciPy versions only, not a complete environment lock. No root LICENSE filename seen in listing. Do not infer open-source license from public visibility.

## Ethics and author approvals
Author answers for sole authorship, prior publication of new XAI results and exclusivity are retained. Not evidence of institutional ethics determination, copyright/privacy consent, funding, conflicts, actual CRediT contributions, or final human review. AI policy https://www.elsevier.com/about/policies-and-standards/generative-ai-policies-for-journals (updated June 2026). Methods and pre-References disclosure updated; author must confirm complete use and scientific review. No claim of final approval.
