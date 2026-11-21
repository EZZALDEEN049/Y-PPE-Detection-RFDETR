# SEER-PPE V17 — paired fixed-detector / conservative routing pre-freeze protocol

**Status: EXECUTABLE TRAIN-ONLY OFFLINE DESIGN, NOT SCIENTIFIC VALIDATION.** 21 November 2026.

## Fixed evidence and split firewall

The original hosted RF-DETR Small model `altayyar-0oflt-lafos-qqauz/2` was already run in read-only form on **four Train examples A/B/C/D**. V17 does **not** run inference, modify weights or annotations, read Test, or score Validation. Its deterministic tool consumes only: (i) original numeric model outputs V16; (ii) geometry proposals V16; (iii) source-readiness summary V15; and (iv) the still-closed V11 Validation-freeze contract. The human visual reference and V16 human-contradiction report are **not** input to the online/proposed routing logic.

Input identity, model/workflow version, case identity and split, box counts, original detection IDs/scores, confidence-band consistency, person IDs, conservative no-clearance semantics and source/freeze status are checked. The output pins SHA-256 digests of its four source files. The run uses **zero new detector calls, XAI calls, review dispatches, images, image URLs, measured joules or field interventions.**

## Matched input arms (engineering trace only)

- **A0 (detector only):** exactly the saved raw numeric class/box/confidence detections. It has no worker-compliance policy, no XAI, and **must not be reinterpreted as an unsafe-clearance policy**. In particular, A0 is not a worker-level safety predictor.
- **A5 (SEER policy proposal):** an offline conservative post-processing view of the **identical original V16 detection IDs**, without running a different detector. Positive and `No ...` PPE cues are evidence for review, never automatic verified presence/absence. All detected persons have unverified scene coverage and unknown applicable occupational mandate. Each typed cue therefore produces `ABSTAIN_AND_SUGGEST_HUMAN_REVIEW_NOT_DISPATCHED` with audit reasons. Geometry is tentative only; one strong overlap is **not** a signed owner match. A PPE box with no detected person (Train D) **cannot** clear the scene or prove no people are present.
- Neither arm yields actual human review completion, compliance or safety outcomes, nor evidence that one policy improves safety or energy. The same original detections guarantee input alignment, **not** measured comparative policy effectiveness.

Every individual A0–A5 cue pairing is keyed by the **same detection ID in the same case**. Reject changed splits, duplicate IDs, mismatched scores/classes, synthetic author signatures, a forged safety clearance, or an unexpectedly open Validation freeze. Expose the D no-person exception rather than coercing it to zero-worker safety.

## Research comparator plan for post-gate Validation (NOT executed)

1. Complete per-image original-source independence attestations and the separate original-Valid/459 Clean17 mapping; retain historical holds, six technical quarantines and unknown groups unless individually decided. An unflagged source is **not** an attested independent source.
2. Obtain signed human scene/person coverage and person–PPE visual `PRESENT / ABSENT / UNKNOWN` with documented item ownership. Separate independently supported `REQUIRED / NOT_REQUIRED / POLICY_UNKNOWN` mandate labels. A single researcher reference must not be presented as independent multi-rater gold.
3. Freeze inclusion/exclusion criteria, worker-level matching, detector confidence and association thresholds, full-catalogue abstention/overflow rules, outcome denominators, uncertainty intervals, severity and cost definitions **before** making scientific claims on Validation. Do not choose thresholds from protected Test.
4. Establish comparable actual *decision* policy adapters for A0 and A5, and compare A5 with a **prespecified strong selective comparator** (candidate A2 confidence-only, or a Validation-selected alternative fixed before Test) under the **same safety requirements, review capacity and compute/XAI budget**. Raw A0 remains detection context, not a manufactured autonomous safe-clearance classifier.
5. A priori evaluate (in order) safety gate (false clearances among adjudicated requirement+visual cases, uncontained confirmed-violation rate, review overflow and queue status, faithfulness if XAI is executed); only then comparative incremental explanation compute. Cluster intervals by image and known source family, report source-unknown sensitivity and rare-violation denominator, and record all no-decision/unknown cases. Never equate `PENDING_REVIEW` with completed protective action.
6. Collect actual XAI instance-matched perturbation fidelity, repeated latency/memory and detector+secondary-check calls if available. Call counts may be a computational proxy only if preregistered; **no electrical energy savings in Joules** without genuine metering. Record human review operations separately from simulated review suggestions.
7. Freeze one primary comparator, endpoint, margin, confidence procedure, budget limits, multiplicity rule, full analysis script version and source cohort before historical Test. The historical Test was development-exposed, hence cannot be described as independent unseen external evaluation.

## V17 observed boundary

Saved V16 has 4 Train inputs, 51 detected boxes, 7 Person candidates, 38 typed PPE cues, 34 tentative single-person geometric proposals and 4 ambiguous/unassigned typed cues. V17 proposes **38 review-item traces**, not 38 delivered human-review tasks or verified PPE associations. The 6 remaining non-person boxes are context-only. **All four scenes remain coverage-unverified**, and no person/scenery is marked compliant. There are **0 signed independent Valid source images** and **0 signed complete Valid person-level references** according to the current tracked evidence. The derived V17 JSON is intended to be regenerated and integrity-checked by GitHub Actions, not interpreted as measured comparative performance.

V16 qualitative four `No Safety Boots` versus historical human `PRESENT` contradictions stay in a separate *post hoc* diagnostic file; they are never online routing inputs. The four missing B human cells and unsigned D zero-person review remain unsolved. This protocol does **not** create reviewer decisions or relax `scoring_ready=false`.
