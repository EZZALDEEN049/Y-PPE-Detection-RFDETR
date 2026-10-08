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

## S3. Training-control rationale
The experiment was designed to estimate domain-transfer reliability rather than maximize within-domain accuracy. The same architecture, image size, training duration, and execution policy were retained across source domains and seeds.

## S4. Fixed operating point
AP metrics were supplemented with a frozen confidence threshold of 0.25 to obtain directly interpretable TP/FP/FN, recall, F1, and safety-class false-negative behavior. The threshold was not selected after inspecting held-out results.

## S5. Consensus false negatives
For each transfer direction, a safety-class ground-truth instance was defined as a consensus false negative if it was missed by all three independently trained source-domain seeds at the frozen operating point.

## S6. Diagnostic audit
The post-evaluation diagnostic analysis quantified class support, class imbalance, normalized bounding-box area, study-specific object-size strata, stored image geometry, and deterministic example failures. These analyses were interpretive and did not alter the frozen Stage 6 quantitative results.
