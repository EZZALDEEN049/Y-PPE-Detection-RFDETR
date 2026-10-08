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
Images were excluded if nine-class harmonization would leave them empty or if critical unmatched source annotations triggered the prespecified structural rule. Model predictions were not used to determine dataset membership.

## S3. Training-control rationale
The experiment was designed to estimate domain-transfer reliability rather than maximize within-domain accuracy. The same architecture, image size, training duration, and execution policy were retained across source domains and seeds.

## S4. Fixed operating point
AP metrics were supplemented with a frozen confidence threshold of 0.25 to obtain directly interpretable TP/FP/FN, recall, F1, and safety-class false-negative behavior. The threshold was not selected after inspecting held-out results.

## S5. Consensus false negatives
For each transfer direction, a safety-class ground-truth instance was defined as a consensus false negative if it was missed by all three independently trained source-domain seeds at the frozen operating point.

## S6. Diagnostic audit
The post-evaluation diagnostic analysis quantified class support, class imbalance, normalized bounding-box area, study-specific object-size strata, stored image geometry, and deterministic example failures. These analyses were interpretive and did not alter the frozen Stage 6 quantitative results.
