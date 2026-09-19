# Stage 3 Semantic Harmonization Closure

**Date:** 2026-09-20  
**Status:** CLOSED before any harmonized training.  
**Workflow evidence:** GitHub Actions run 35474887219 completed successfully.  
**Locked-test condition:** satisfied; no Y-PPE or Construction-PPE test image entered the visual semantic audit.

## Evidence generated

The deterministic audit reconstructed the cleaned Stage-2 derivatives for both datasets and generated 108 visual sample panels: 6 examples per dataset for each of the 9 candidate shared classes. Visual evidence used only Y-PPE train+valid and Construction-PPE train+val. It also generated class-level bounding-box geometry summaries over the cleaned datasets.

## Final shared ontology decision

All nine candidate pairs are retained, but the benchmark is frozen as a **normalized bounding-box ontology**, not a raw-label concatenation. Y-PPE contains a minority of polygon annotations in eight of the nine retained classes; those polygons will be converted deterministically to their enclosing axis-aligned boxes before harmonized dataset construction. `no_gloves` is already bbox-only in Y-PPE.

| Canonical class | Y-PPE | Construction-PPE | Decision |
|---|---|---|---|
| person | Persons | Person | ACCEPT_WITH_NORMALIZATION |
| helmet | Hard Hat | helmet | ACCEPT_WITH_NORMALIZATION |
| gloves | Gloves | gloves | ACCEPT_WITH_NORMALIZATION |
| vest | Safety Vests | vest | ACCEPT_WITH_NORMALIZATION |
| boots | Safety Boots | boots | ACCEPT_WITH_NORMALIZATION |
| goggles | Goggles | goggles | ACCEPT_WITH_NORMALIZATION |
| no_helmet | No Hard Hat | no_helmet | ACCEPT_WITH_NORMALIZATION |
| no_gloves | No Gloves | no_gloves | ACCEPT |
| no_boots | No Safety Boots | no_boots | ACCEPT_WITH_NORMALIZATION |

The retained mappings localize the same physical target type in both datasets: whole person for `person`, the PPE item itself for positive PPE classes, and anatomical/PPE-negative regions for the three negative-state classes.

## Geometry evidence

The geometry audit supports comparable localization type while also showing real domain and annotation-distribution differences. Examples include median normalized target area Y-PPE vs Construction-PPE: helmet 0.0084 vs 0.0121, gloves 0.0078 vs 0.0071, vest 0.0281 vs 0.0645, boots 0.0037 vs 0.0134, goggles 0.0197 vs 0.0071, no_helmet 0.0056 vs 0.0186, no_gloves 0.0063 vs 0.0103, and no_boots 0.0163 vs 0.0065. These differences are not interpreted as automatic semantic mismatch because visual inspection confirmed the same region type; they are retained as part of the cross-domain shift.

Person-containment evidence is also generally high in both datasets for worn/localized PPE. Y-PPE contains more standalone/product-style examples for some classes, especially gloves and goggles, whereas Construction-PPE examples are more frequently person-associated. This is documented as **domain-composition shift**, not silently removed to manufacture similarity between domains.

## Important semantic guardrail for negative classes

The labels `no_helmet`, `no_gloves`, and `no_boots` are frozen as **visual PPE-negative states**, not automatically as context-validated safety violations. Direct visual evidence includes generic/non-work scenes in the source datasets. Therefore, the manuscript must not infer that every uncovered head, bare hand, or non-boot footwear instance represents a normative workplace violation unless task-context evidence independently establishes that PPE was required.

This distinction affects later safety reporting: classwise false negatives on these labels can be described as missed dataset-defined PPE-negative states. Stronger language such as missed safety violations requires explicit contextual justification.

## Classes excluded from the shared ontology

- Y-PPE `No Safety Vest`: no direct Construction-PPE no-vest counterpart.
- Construction-PPE `no_goggle`: no direct Y-PPE negative-goggle class.
- Construction-PPE `none`: no defensible one-to-one Y-PPE equivalent.

## Training gate

Stage 3 is now closed. The next valid step is to construct deterministic cleaned **9-class harmonized derivatives** from the already-clean Stage-2 datasets, remap class IDs, convert Y-PPE polygons to bounding boxes, verify per-split counts and label validity, and freeze those derivative manifests before model training.

No historical 17-class Y-PPE metric may substitute for the new harmonized in-domain baselines.
