# Worker-level PPE compliance annotation codebook v0.1

**Date:** 2026-10-29. **Status:** preregistration **draft**. No human annotations have yet been produced using this codebook.  
**Primary PPE endpoint:** safety helmet. Generalizable to other equipment only with category-specific requirements.

## Unit of analysis and identity
- **image_id**: unique immutable image identifier; **image_sha256**: identify exact bytes.
- **site_id**: actual collection site, not synonymous with dataset name.
- **acquisition_group_id**: source video / camera session / related-scene family; record enough information to group correlated frames.
- **worker_gt_id**: unique instance within image; for same worker across frames include optional `track_id`, but repeated frames are NOT independent observations.
- **worker_bbox_xyxy**: human-drawn visible-worker box, including GT workers missed by the detector. Annotation must be independent of algorithm detections.
- **annotator_id**, **adjudicator_id**, **label_version**, and **reason/comments** for provenance. Do not publish real worker identity.

## Independent variables (do not collapse until adjudication)
| Field | Allowed values | Annotation rule |
|---|---|---|
| `person_status` | WORKER / NOT_WORKER / UNRESOLVED | Site/task role must be supported by ground truth; visual appearance may be insufficient. |
| `head_visibility` | VISIBLE / PARTIAL / NOT_VISIBLE / UNRESOLVED | `NOT_VISIBLE` does not imply `NO_HELMET`. |
| `helmet_wearing` | WORN / NOT_WORN / UNCERTAIN | WORN requires visible head-wearing evidence; a helmet elsewhere in the frame is not compliance. |
| `helmet_required` | YES / NO / UNKNOWN | Determined from documented site/task safety rule, not inferred from object label or simply a construction-like backdrop. |
| `helmet_rule_source` | site_policy / supervisor / regulatory_citation / unknown | Source evidence for any YES/NO mandate. |
| `head_equipment_association` | MATCHED / CONFLICT / MULTIPLE / UNMATCHED / NOT_ASSESSABLE | One helmet may not be assigned to multiple workers without explicit adjudication. |
| `adjudication_state` | FINAL / PENDING / EXCLUDED_WITH_REASON | Unknown contexts must be reported and reviewed, not silently discarded. |

## Derived label for eligible workers
Define `A=1` if helmet_required=YES. For a GT worker with A=1:
- `gt_state=violation` only if helmet_wearing=NOT_WORN is **reliably adjudicated** and head evidence/context is sufficient.
- `gt_state=compliant` only if helmet_wearing=WORN reliably.
- Otherwise `gt_state=indeterminate`.
For helmet_required=NO, record `NOT_REQUIRED`, not compliant/noncompliant. UNKNOWN requirement must never be automatically treated as compliant.

Record **all visible workers**, including those whose head cannot be evaluated, and preserve the GT inventory for evaluating detector misses. Missing GT annotations cannot be reconstructed from the detector after testing.

## Human review protocol
1. Two independently working trained annotators label image/scene identity, workers, head visibility, helmet wearing, and rule source, **without seeing model predictions**.
2. Adjudicator resolves disagreements from original permitted imagery and verified site safety rule; if unresolved use UNCERTAIN/UNKNOWN/indeterminate.
3. Run periodic consistency checks with duplicate blind samples and class-specific disagreement summaries. Report counts of unresolved workers rather than silently omitting them.
4. Freeze final labels **before running test evaluation or adjusting the method**. Preserve immutable annotation versions and timestamps.
5. Compute prevalence, support, and agreement for rule required vs visible wearing vs final violation separately; report site-wise distributions. A single overall accuracy of human labels cannot validate the concept.

## Prohibited shortcuts
- Using YOLO `no_helmet` labels as legally meaningful rule violations.
- Labeling compliance only because no `No Hard Hat` detection exists.
- Removing missed GT workers from the denominator.
- Splitting related frames of one camera/video into separate independent calibration and test units.
- Making a site-specific occupational-safety inference where the rule source is UNKNOWN.

## Minimum data-availability gate
Before calibration count independent **adjudicated violation** acquisition units per site. A dataset with a handful of no-helmet object labels must be treated as preliminary detection evidence and cannot support strong worker-level finite-sample safety claims.

Related: [EXPERIMENT_PROTOCOL.md](EXPERIMENT_PROTOCOL.md), [DATA_AUDIT_2026-10-29.md](DATA_AUDIT_2026-10-29.md).
