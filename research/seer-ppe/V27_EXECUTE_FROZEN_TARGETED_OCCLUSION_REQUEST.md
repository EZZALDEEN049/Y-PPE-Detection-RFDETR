# V27 execution request — actual original-model target-box occlusion and A5/A6 matched-budget comparison

The frozen [V27 protocol](V27_FROZEN_TARGETED_OCCLUSION_AND_A6_COMPARATOR_PROTOCOL_2026-11-21.md) defines the nine original development images, 10 unique A5/A6 target boxes, seven preselected non-target controls, A6 class-FDR comparator, fixed geometry filters, BlurVisualization kernel/padding and 27-call model budget.

First generate and verify `V27_FROZEN_TARGETS_2026-11-21.json` with `tools/build_v27_frozen_targets.mjs`. Then validate the Roboflow Workflow template using `workflow_specs_validate`. Only after those two checks, run the 10 pre-frozen target-specific Workflows on their exact original Roboflow Source image URLs. Save only numeric inference outputs and source IDs; never save original pixels or signed URLs. If target isolation does not return exactly one detection, fail closed. Do not access Test or modify original model, dataset, annotations or splits.

Primary comparison is A5 versus A6, both one target per image, one proposed review slot per image, identical box-occlusion settings. A2 is context only. The five Valid targets may be joined to V23 TP/FP outcomes only after target selection. Do not dispatch human review or claim worker safety, independent generalization, XAI faithfulness beyond the measured perturbation, or Joule savings.

Target-freeze CI trigger: regenerate the manifest from the already committed V16/V23/V25/V26 artifacts and verify all 10 A5/A6 targets before any new model call.
