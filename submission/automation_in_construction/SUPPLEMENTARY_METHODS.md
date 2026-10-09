# Supplementary Methods

## S1. Semantic harmonization
The source datasets used non-identical label spaces. Shared classes were retained only where object/state meaning and localization target were sufficiently aligned.

| Canonical class | Y-PPE source label | Construction-PPE source label |
|---|---|---|
| person | Persons | Person |
| helmet | Hard Hat | helmet |
| gloves | Gloves | gloves |
| vest | Safety Vests | vest |
| boots | Safety Boots | boots |
| goggles | Goggles | goggles |
| no_helmet | No Hard Hat | no_helmet |
| no_gloves | No Gloves | no_gloves |
| no_boots | No Safety Boots | no_boots |

Excluded from the shared ontology:
- Y-PPE: No Safety Vest (no direct Construction-PPE counterpart)
- Construction-PPE: no_goggle (no explicit Y-PPE negative-state counterpart)
- Construction-PPE: none (no direct semantic equivalent)

The negative-state labels represent dataset-defined visual states. Their presence does not independently establish that a particular PPE item was normatively required in every scene.

## S2. Conservative structural filtering

### S2.1 Stage 4 keep-all transformation
Stage 4 preserved all cleaned source images in their original splits, retained only annotations belonging to the nine-class shared ontology, and wrote an empty label file when an image had no retained shared annotation. Y-PPE retained polygons were converted deterministically to enclosing axis-aligned bounding boxes.

Pre-filter image counts were:
- Y-PPE: 1,595 train / 459 validation / 234 test.
- Construction-PPE: 1,077 train / 134 validation / 141 test.

### S2.2 Critical source relationships
The Stage 4.5 audit treated the following excluded-to-retained relationships as critical:

- Y-PPE `Child` → `Persons`
- Y-PPE `No Safety Attire` → `Persons`
- Y-PPE `Soft Hat` → `Hard Hat` or `No Hard Hat`
- Construction-PPE `none` → `Person`

Y-PPE `No Safety Vest`→`Safety Vests` and Construction-PPE `no_goggle`→`goggles` were informational only and did not independently trigger image exclusion.

### S2.3 Exact box-matching criterion
For every excluded box E and corresponding retained candidate box R, the excluded object was considered structurally matched if:

`IoU(E,R) >= 0.50`

or

`area(E ∩ R) / area(E) >= 0.80`.

An excluded critical annotation was flagged as `critical_unmatched:<class>` only when no candidate retained box satisfied either threshold.

### S2.4 Deterministic membership pseudocode

```text
for each source image:
    map retained shared annotations to the 9-class ontology
    harmonized_empty = (number of retained shared annotations == 0)

    critical_unmatched = false
    for each excluded annotation belonging to a prespecified critical class:
        candidates = retained annotations from the corresponding allowed class(es)
        matched = any(
            IoU(excluded_box, candidate_box) >= 0.50
            OR containment(excluded_box in candidate_box) >= 0.80
            for candidate_box in candidates
        )
        if not matched:
            critical_unmatched = true

    exclude_image = harmonized_empty OR critical_unmatched
```

The rule is based only on source annotation labels and box geometry. No model prediction, confidence, loss, or held-out performance is consulted.

### S2.5 Executed exclusions

| Dataset | Split | Pre-filter | Excluded | Final |
|---|---|---:|---:|---:|
| Y-PPE | train | 1,595 | 359 | 1,236 |
| Y-PPE | validation | 459 | 103 | 356 |
| Y-PPE | test | 234 | 48 | 186 |
| Construction-PPE | train | 1,077 | 31 | 1,046 |
| Construction-PPE | validation | 134 | 2 | 132 |
| Construction-PPE | test | 141 | 3 | 138 |

Y-PPE reason-token counts overlap because one image can carry more than one risk flag:
- harmonized_empty: 282;
- critical_unmatched:Soft Hat: 171;
- critical_unmatched:Child: 113;
- critical_unmatched:No Safety Attire: 73.

Construction-PPE excluded 36 images: 35 with `critical_unmatched:none` only and one with both `critical_unmatched:none` and `harmonized_empty`.

### S2.6 Final class support by split

| Dataset | Split | person | helmet | gloves | vest | boots | goggles | no_helmet | no_gloves | no_boots |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Y-PPE-h9-v2 | train | 1298 | 1227 | 821 | 822 | 941 | 531 | 113 | 677 | 226 |
| Y-PPE-h9-v2 | validation | 383 | 362 | 265 | 271 | 310 | 186 | 40 | 251 | 54 |
| Y-PPE-h9-v2 | test | 121 | 109 | 84 | 80 | 78 | 89 | 14 | 88 | 30 |
| Construction-PPE-h9-v2 | train | 1610 | 1234 | 1050 | 1179 | 1142 | 393 | 352 | 403 | 74 |
| Construction-PPE-h9-v2 | validation | 228 | 191 | 118 | 159 | 137 | 40 | 43 | 51 | 4 |
| Construction-PPE-h9-v2 | test | 224 | 188 | 163 | 175 | 201 | 52 | 37 | 51 | 15 |

### S2.7 Effect of filtering on class support
Whole-image exclusion changed the retained class distribution. Relative reductions from Stage 4 to final v2 were largest for Y-PPE `no_boots` (-43.0%), `no_helmet` (-34.8%), and `no_gloves` (-26.0%). For Construction-PPE, the largest reductions were `no_boots` (-19.1%), `no_helmet` (-10.9%), and `no_gloves` (-9.2%). Full before/after counts are archived in `stage11c_class_counts_before_after.csv`.

### S2.8 Test-population interpretation
The same predeclared annotation-only rule was applied to train, validation, and test before Stage 5 training. Test-image pixels were not opened for membership adjudication. Nevertheless, because source annotations influence membership, the resulting test sets represent the **structurally harmonizable subset** of each source dataset rather than the complete cleaned source population. This restriction is reported as a benchmark-selection limitation rather than as model/test leakage.

### S2.9 Reproducibility evidence
The final Stage 4.5 artifact is:
- workflow run: `35536050231`
- artifact ID: `10612876023`
- head SHA: `eb87aa14dab07d7546e713c2d5eb68ef583f2d5a`
- artifact digest: `sha256:24b5851f8eef044e17d6804272db2965fed9737098718ed229d0e5a57028786f`

The artifact contains the two exclusion manifests, structural summaries, filtering summaries, and final dataset summaries.

## S3. Training protocol and exact Ultralytics configuration

The experiment was designed to estimate domain-transfer reliability under a controlled recipe rather than maximize within-domain accuracy. The same YOLO11m architecture and training policy were used for both source domains. Three seed realizations were completed for each source dataset: 17, 42, and 2026.

### S3.1 Runtime
- GPU: NVIDIA Tesla T4
- Python: 3.13.15
- PyTorch: 2.11.0+cu128
- CUDA runtime: 12.8
- Ultralytics: 8.4.156
- pretrained model: `yolo11m.pt`

### S3.2 Recorded Ultralytics train configuration

The stored `args.yaml` for the completed runs records:

```yaml
task: detect
mode: train
model: yolo11m.pt
epochs: 100
patience: 0
batch: 8
imgsz: 640
save: true
save_period: 10
cache: false
device: "0"
workers: 2
pretrained: true
optimizer: auto
seed: 17|42|2026
deterministic: true
rect: false
cos_lr: false
resume: false
amp: true
fraction: 1.0
multi_scale: 0.0
dropout: 0.0
val: true
split: val
iou: 0.7
max_det: 300
augment: false
lr0: 0.01
lrf: 0.01
momentum: 0.937
weight_decay: 0.0005
warmup_epochs: 3.0
warmup_momentum: 0.8
warmup_bias_lr: 0.1
box: 7.5
cls: 0.5
dfl: 1.5
nbs: 64
hsv_h: 0.0
hsv_s: 0.0
hsv_v: 0.0
degrees: 0.0
translate: 0.0
scale: 0.0
shear: 0.0
perspective: 0.0
flipud: 0.0
fliplr: 0.0
bgr: 0.0
mosaic: 0.0
mixup: 0.0
cutmix: 0.0
copy_paste: 0.0
augmentations: []
```

The same configuration was used for Y-PPE-h9-v2 and Construction-PPE-h9-v2 except for the dataset path, run output path, and seed. Because `optimizer=auto`, Ultralytics resolved the optimizer internally. Representative completed-run logs from both domains resolved to AdamW with learning rate 0.000769, momentum 0.9, and weight decay 0.0005 for decayed groups. These resolved values are reported as observed framework output rather than as manually imposed hyperparameters.

The primary checkpoint policy was the final epoch `last.pt`. Validation-selected `best.pt` checkpoints were retained but excluded from the primary analysis and were subsequently evaluated in the prespecified Stage 11D checkpoint-sensitivity analysis.

## S4. Held-out evaluation and matching algorithm

The Stage 6 evaluator was frozen before held-out evaluation and used:
- image size: 640;
- AP confidence floor: 0.001;
- fixed operating confidence: 0.25;
- prediction NMS IoU: 0.70;
- class-matched TP IoU: 0.50;
- no test-time augmentation;
- batch size: 8.

The primary evaluator code SHA recorded with the Stage 6 outputs was:
`f02f7f44772ac67ff820610721ec828a38de1b1a`.

### S4.1 AP evaluation
For each checkpoint/test-domain pair, Ultralytics `model.val(..., split="test")` was executed at `imgsz=640`, `conf=0.001`, `iou=0.70`, and `augment=False`. The reported AP outcomes were mAP50:95, mAP50, mAP75, and class-level AP values.

### S4.2 Fixed operating-point TP/FP/FN assignment

Ground-truth YOLO boxes were converted to pixel-space `xyxy`. Predictions were grouped by class and sorted in descending confidence. For each class:

```text
for prediction in descending confidence:
    compute IoU with every unmatched ground-truth box of the same class
    select the unmatched ground-truth box with maximum IoU
    if best IoU >= 0.50:
        count one TP and mark that ground truth as used
    else:
        count one FP

FN = number of class ground-truth boxes not matched to any prediction
```

Each ground-truth object can therefore be matched at most once. Precision, recall, and F1 were calculated from the resulting TP/FP/FN counts. No confidence or IoU threshold was altered after test inspection.

## S5. Consensus false-negative algorithm

The qualitative PPE-negative-state audit reused the exact frozen operating point:
- confidence = 0.25;
- NMS IoU = 0.70;
- class-match IoU = 0.50;
- imgsz = 640;
- `last.pt`;
- no TTA.

For each target-domain ground-truth object in `no_helmet`, `no_gloves`, or `no_boots`, each of the three same-source seed models was checked independently. A seed detected the object when at least one prediction of the same class had IoU >= 0.50 with that ground-truth box.

A consensus false negative was defined as:

```text
consensus_FN = NOT (
    detected_by_seed_17
    OR detected_by_seed_42
    OR detected_by_seed_2026
)
```

The three seeds are repeated training realizations of the same architecture, source data, and protocol. Consensus therefore indicates persistence under training stochasticity, not independent replication across architectures or construction sites.

Qualitative examples were selected deterministically by SHA-256 ordering of `image path | class | ground-truth index`, preventing manual cherry-picking of illustrative failures.

## S6. Full primary per-seed held-out results

| Run | Test | Type | mAP50:95 | mAP50 | mAP75 | Precision | Recall | F1 | no_helmet recall | no_gloves recall | no_boots recall |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Y s17 | Y | in-domain | 0.2916 | 0.5436 | 0.2857 | 0.8797 | 0.5065 | 0.6429 | 0.2857 | 0.3295 | 0.3333 |
| Y s17 | C | cross-domain | 0.1190 | 0.2820 | 0.0791 | 0.7037 | 0.3779 | 0.4918 | 0.1351 | 0.0196 | 0.0000 |
| Y s42 | Y | in-domain | 0.2972 | 0.5712 | 0.2714 | 0.8843 | 0.5296 | 0.6625 | 0.4286 | 0.3068 | 0.3667 |
| Y s42 | C | cross-domain | 0.1194 | 0.2854 | 0.0799 | 0.7108 | 0.3689 | 0.4857 | 0.1351 | 0.0196 | 0.0000 |
| Y s2026 | Y | in-domain | 0.2839 | 0.5386 | 0.2683 | 0.8787 | 0.5123 | 0.6472 | 0.2143 | 0.2727 | 0.4000 |
| Y s2026 | C | cross-domain | 0.1244 | 0.3127 | 0.0777 | 0.7180 | 0.4005 | 0.5142 | 0.0811 | 0.0784 | 0.0000 |
| C s17 | C | in-domain | 0.2551 | 0.4674 | 0.2528 | 0.9154 | 0.5868 | 0.7152 | 0.0270 | 0.0196 | 0.0000 |
| C s17 | Y | cross-domain | 0.0828 | 0.1871 | 0.0591 | 0.7548 | 0.2266 | 0.3485 | 0.0714 | 0.0114 | 0.0000 |
| C s42 | C | in-domain | 0.2522 | 0.4698 | 0.2326 | 0.9267 | 0.5832 | 0.7159 | 0.0270 | 0.0196 | 0.0000 |
| C s42 | Y | cross-domain | 0.0864 | 0.1978 | 0.0594 | 0.7577 | 0.2121 | 0.3315 | 0.0000 | 0.0227 | 0.0000 |
| C s2026 | C | in-domain | 0.2478 | 0.4652 | 0.2390 | 0.9213 | 0.5714 | 0.7054 | 0.0270 | 0.0196 | 0.0000 |
| C s2026 | Y | cross-domain | 0.0767 | 0.1752 | 0.0522 | 0.7844 | 0.1890 | 0.3047 | 0.0000 | 0.0114 | 0.0000 |

## S7. Dataset diagnostics and train-test dependence audit

The post-evaluation dataset diagnostic audit quantified:
- class frequencies and imbalance;
- PPE-negative-state class support;
- normalized bounding-box area;
- study-specific size strata;
- stored resolution/aspect ratio.

The subsequent Stage 11A dependence audit separated:
1. exact SHA-256 duplicates;
2. transformed near-duplicate candidates;
3. scene-level dependence.

No exact byte-level cross-split duplicates were found. Four Y-PPE test images were visually confirmed as transformed near-duplicate derivatives of training images. Construction-PPE candidates were classified conservatively as related-scene dependence rather than confirmed near-duplicates.

Two sensitivity subsets were frozen before re-evaluation:
- strict: remove only the four confirmed Y-PPE near-duplicate test derivatives;
- conservative: remove all high-confidence direct train-related test images, leaving 180 Y-PPE and 115 Construction-PPE test images.

No retraining, threshold change, or checkpoint reselection was performed. Substantial aggregate cross-domain mAP50:95 gaps persisted under both scenarios.

## S8. Image-cluster bootstrap for PPE-negative-state outcomes

To avoid treating multiple objects from one image as independent observations, test images were the resampling unit. Within each transfer direction and PPE-negative-state class, images were sampled with replacement for 10,000 percentile-bootstrap replicates using deterministic seed 20261009. All objects belonging to a sampled image inherited the same sampling multiplicity.

Intervals were calculated for:
- class recall averaged over the three trained seed realizations;
- consensus false-negative rate.

These intervals quantify sampling uncertainty over the evaluated test images conditional on the already trained models. They are not site-level population intervals and do not incorporate architecture uncertainty.

Image-level bootstrap uncertainty for mAP50:95 is not reported because the original Stage 6 summary did not retain sufficient ranked per-image prediction statistics to reconstruct AP exactly. No object-level approximation was substituted.

## S9. Validation-selected checkpoint sensitivity

A prespecified sensitivity analysis evaluated the validation-selected `best.pt` checkpoint from each completed run under the exact Stage 6 evaluation settings. The analysis comprised 12 held-out evaluation cells and performed no training, target-domain adaptation, threshold tuning, or test-informed checkpoint selection.

| Training domain | Test domain | mAP50:95 mean ± SD | Recall mean ± SD | F1 mean ± SD | no_helmet recall | no_gloves recall | no_boots recall |
|---|---|---:|---:|---:|---:|---:|---:|
| Y-PPE | Y-PPE | 0.312 ± 0.006 | 0.596 ± 0.030 | 0.682 ± 0.010 | 0.262 ± 0.149 | 0.458 ± 0.046 | 0.433 ± 0.067 |
| Y-PPE | Construction-PPE | 0.122 ± 0.002 | 0.419 ± 0.018 | 0.507 ± 0.010 | 0.117 ± 0.041 | 0.046 ± 0.011 | 0.000 ± 0.000 |
| Construction-PPE | Construction-PPE | 0.269 ± 0.002 | 0.694 ± 0.021 | 0.708 ± 0.010 | 0.198 ± 0.113 | 0.092 ± 0.060 | 0.000 ± 0.000 |
| Construction-PPE | Y-PPE | 0.099 ± 0.005 | 0.344 ± 0.013 | 0.384 ± 0.014 | 0.000 ± 0.000 | 0.011 ± 0.000 | 0.000 ± 0.000 |

The resulting mean mAP50:95 domain gaps were:
- Y-PPE-trained: 0.191, approximately 61.0% relative;
- Construction-PPE-trained: 0.170, approximately 63.3% relative.

All six seed-level `best.pt` gaps remained positive. The sensitivity analysis therefore supports checkpoint robustness of the aggregate cross-domain degradation. Class-level negative-state behavior was more checkpoint-sensitive, especially for Construction-PPE no_helmet and no_gloves.

## S10. Reproducibility anchors

Final Stage 4.5 data identities:
- Y-PPE-h9-v2: `82c08766d5c5e50e93d41d21c4751fd686a3932ea6a8cb24ffd2838d9e30fba8`
- Construction-PPE-h9-v2: `59469299ba67355dbcb0e725851f73d244a7ad6e93522d44601be3c8323d3c14`

Stage 4.5 frozen evidence:
- workflow run: `35536050231`
- head SHA: `eb87aa14dab07d7546e713c2d5eb68ef583f2d5a`
- artifact ID: `10612876023`
- artifact digest: `sha256:24b5851f8eef044e17d6804272db2965fed9737098718ed229d0e5a57028786f`

Stage 6 evaluator code SHA:
- `f02f7f44772ac67ff820610721ec828a38de1b1a`

The public project repository is:
- `https://github.com/EZZALDEEN049/Y-PPE-Detection-RFDETR`

The final sensitivity-analysis code is pinned to immutable Git commit `10e7b7e116288869647c61287d0c88056bf0a972`, and the journal-facing manuscript package is preserved on the `submission-final-2026-10-09` branch.
