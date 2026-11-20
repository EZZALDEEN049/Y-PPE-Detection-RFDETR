# SEER-PPE — Five high-similarity Train↔Valid original-image pre-reviews (21 Nov 2026)

**Type:** Read-only **AI visual candidate triage**, NOT a person-identification system, original-file hash, human-approved source family, detector inference, or scientific evaluation. The image interpretations below follow **ten separate** Roboflow image analyses and fresh read-back of ten original saved annotation records; the five pair cosines were already recorded on 19 November.

## Original images examined: five Valid → Train pairs

| Valid → Train | Cosine | Read-only visual evidence | Research-only disposition |
|---|---:|---|---|
| `Safety-Glasses-Toolbox-Talk.jpg` → `image_719.jpg` | **0.998663** | Both show close-up yellow hard-hat, clear-glasses, white-mask portraits with blurred industrial backdrop. Same **1200×800** dimensions, and identical *five* source-annotation class counts | **High priority:** possible shared/cropped portrait; not proven identical |
| `v126.jpg` → `v125.jpg` | **0.991050** | Both show clear front-facing protective glasses on white, with a distinctive oval **Anti-Fog Lens** sticker on viewer-right lens; image dimensions differ slightly | **High priority:** possibly shared product asset |
| `v141.jpg` → `v140.jpg` | **0.990562** | Both show clear protective glasses in a three-quarter studio view on white, **700×700**, one source `Goggles` each | **Review:** generic product similarity is not pixel-identity evidence |
| `construction-worker-wearing-safety-equipment-19672694.jpg` → `image_798.jpg` | **0.985266** | Similar white-background PPE stock portrait: yellow hat, white mask, orange reflective vest, glove raised to hat brim. Stock photo watermarks are described in both individual analyses, but dimensions differ | **High priority:** possible derivative of shared stock photograph |
| `h39.jpg` → `h34.jpg` | **0.982068** | White-background helmet marketing graphics with Thai writing; **yellow vs orange** helmet in independent image descriptions, both 300×300 | **Likely visually different products** despite high cosine; no duplicate verdict |

## Method and research implications

- All ten image Source IDs were resolved to Train or Valid in Roboflow. Ten original existing annotation readbacks reported `annotation_valid=true`; original `No ...` class markers are **not** human-confirmed missing equipment.
- The distinctive observations (including the PPE portraits and product-sticker text) are **AI scene descriptions only**. The system did **not** directly align two pixel arrays or compute original-image SHA-256/decoded pixel SHA-256/dHash.
- Shared stock/retail source groups may create cross-split overlap even for images **without people**. Avoid treating product-photo similarity as a construction-site conflict; classify image use (worker/standalone item/negative control) separately from source-group independence.
- A high cosine need not mean duplicate pixels: `h39/h34` has cosine >0.98 while AI vision reports **different helmet colors**. Conversely known named worksite overlap or stock photo variants can have cosine far below 0.98. No single cosine threshold can declare independence.
- **No new holds** were automatically created, and the earlier five research-hold Valid IDs remain intact. All five Valid IDs here already belonged to the **83-image review queue**; queue total remains **83**.
- No Test image, annotation or embedding was opened; original Roboflow source annotations, splits and RF-DETR model are unchanged. Human original-image pair adjudication and genuine original-byte hashing remain required.

## Next evidence

1. Obtain original bytes and run deterministic SHA-256, EXIF-corrected RGB pixel comparison and dHash under stable Source IDs.
2. Have human reviewers compare each paired original and assign **same image / derivative / shared media session / distinct product or location / uncertain** with evidence. Preserve uncertainty rather than forcing a yes/no.
3. Require explicit review of source-family independence before the held-out evaluation, without rewriting Roboflow datasets or creating new compliance labels.

[Machine register of all ten original IDs and read-only label summaries](EMBEDDING_HIGH_SIM_VISUAL_TRIAGE_2026-11-21_V01.json) · [Previous media-family review](SOURCE_MEDIA_PAIR_VISUAL_TRIAGE_2026-11-21_V02.md) · [Current 83-image review queue](UNIFIED_TRAIN_VALID_TRIAGE_2026-11-21_V02.md).
