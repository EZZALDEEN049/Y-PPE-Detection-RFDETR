# Frozen Data Audit — EcoSafe Selective Experts

This audit was run on the reconstructed immutable `RFDETR_Roboflow_h9_v2_COMPLETE.zip` package. The package SHA-256 matched the archived reassembly record:

`cf562fed2c6e2a1c3771a7f2cfa196b4ac96a9bf836689c1731311419553cf63`

The embedded dataset manifests match the Stage 5 frozen fingerprints:
- Y-PPE-h9-v2: `82c08766d5c5e50e93d41d21c4751fd686a3932ea6a8cb24ffd2838d9e30fba8`
- Construction-PPE-h9-v2: `59469299ba67355dbcb0e725851f73d244a7ad6e93522d44601be3c8323d3c14`

## Split counts

| Dataset | Train | Valid | Test |
|---|---:|---:|---:|
| Y-PPE-h9-v2 | 1,236 | 356 | 186 |
| Construction-PPE-h9-v2 | 1,046 | 132 | 138 |

## Safety-relevant validation support

Safety classes are `no_helmet`, `no_gloves`, and `no_boots`.

| Dataset | Valid frames | Safety-positive frames | Safety boxes |
|---|---:|---:|---:|
| Y-PPE-h9-v2 | 356 | 126 (35.4%) | 345 |
| Construction-PPE-h9-v2 | 132 | 27 (20.5%) | 98 |
| Combined development pool | 488 | 153 | 443 |

Because the development pool is modest, the router should remain simple and use cross-fitting/OOF threshold selection rather than a high-capacity neural router.

## Validation safety class counts

| Dataset | no_helmet | no_gloves | no_boots |
|---|---:|---:|---:|
| Y-PPE-h9-v2 | 40 | 251 | 54 |
| Construction-PPE-h9-v2 | 43 | 51 | 4 |

The strong imbalance—especially only four `no_boots` objects in the Construction validation split—means per-class conclusions must report counts and uncertainty; aggregate safety recall should not hide rare-class behavior.

## Exact cross-domain overlap

SHA-256 scanning of all packaged image bytes found **0 exact cross-domain duplicate hash groups** between Y-PPE-h9-v2 and Construction-PPE-h9-v2.

This is an exact-byte check only. The prior study's near-duplicate sensitivity analysis remains the stronger guard against visually similar leakage.

## Test-lock consequence

The complete package contains test images and labels, but EcoSafe router training, calibration, feature selection, and threshold selection must use only the train/valid material. Test data remain untouched until the routing policy is frozen.
