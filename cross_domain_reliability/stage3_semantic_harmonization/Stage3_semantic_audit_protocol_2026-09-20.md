# Stage 3 Semantic Harmonization Audit Protocol

**Date:** 2026-09-20  
**Status:** pre-training semantic audit; no harmonized model has been trained.  
**Purpose:** decide which label pairs can legitimately share one cross-domain detection ontology.

## Frozen principle
A pair is not accepted because its names look similar. It must satisfy all of the following:

1. **Object/state meaning:** both datasets must refer to the same operational PPE object, human object, or explicit non-compliance state.
2. **Localization target:** both annotations must localize the same physical region type (for example PPE item, anatomical absence region, or whole person), rather than one dataset boxing a PPE item and the other boxing an entire worker.
3. **Bounding-box extent:** representative annotations must be sufficiently comparable for one detector class to be evaluated under the same IoU-based rule. Geometry statistics are diagnostic evidence, not an automatic equivalence test.
4. **Annotation-policy consistency:** systematic differences in occlusion, partial visibility, or polygon-vs-box representation must be documented and normalized before training where defensible.

## Locked-test rule
Semantic contact sheets use only Y-PPE `train` + `valid` and Construction-PPE `train` + `val`. Test images are not sampled or opened during this audit. This protects the target test sets from qualitative test exposure before the experiment.

## Candidate nine-class ontology

| Canonical class | Y-PPE | Construction-PPE | Initial status |
|---|---|---|---|
| person | Persons | Person | Pending evidence |
| helmet | Hard Hat | helmet | Pending evidence |
| gloves | Gloves | gloves | Pending evidence |
| vest | Safety Vests | vest | Pending evidence |
| boots | Safety Boots | boots | Pending evidence |
| goggles | Goggles | goggles | Pending evidence |
| no_helmet | No Hard Hat | no_helmet | Pending evidence |
| no_gloves | No Gloves | no_gloves | Pending evidence |
| no_boots | No Safety Boots | no_boots | Pending evidence |

The following are excluded from the candidate shared ontology at this stage: Y-PPE `No Safety Vest`; Construction-PPE `no_goggle`; Construction-PPE `none`.

## Y-PPE annotation evidence already documented
The thesis defines `Hard Hat`, `Gloves`, `Goggles`, `Safety Boots`, and `Safety Vests` as compliant PPE classes and `No Hard Hat`, `No Gloves`, and `No Safety Boots` as explicit violation classes. It also states that object instances are annotated using YOLO-style bounding boxes and shows item/region-level PPE annotations in worksite scenes. Stage 2 additionally established that the cleaned Y-PPE source contains both bounding-box rows and a minority of polygon rows; during semantic geometry inspection polygons are represented only by their enclosing axis-aligned boxes without changing the source data.

## Construction-PPE evidence status
The pinned official Ultralytics YAML supplies the ordered class taxonomy but does not itself provide a sufficiently detailed annotation manual for object/absence-region geometry. Therefore the Stage 3 decision will be based on direct visual annotation evidence plus class-level geometry summaries from the cleaned official archive.

## Decision labels after visual adjudication
Each candidate pair will receive one of:

- **ACCEPT:** semantic object/state and localization geometry are sufficiently aligned for the shared ontology.
- **ACCEPT_WITH_NORMALIZATION:** semantics align, but a documented representation normalization is required before training.
- **EXCLUDE:** the pair is not defensibly equivalent.
- **UNRESOLVED:** more annotation-source evidence is required; no training involving the pair is allowed.

No class will be silently forced into the nine-class benchmark if the audit evidence does not support equivalence.
