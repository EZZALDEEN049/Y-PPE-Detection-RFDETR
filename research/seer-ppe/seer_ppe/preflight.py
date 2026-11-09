"""Blocks invalid claims until independent dataset and hardware evidence exist."""
from dataclasses import dataclass

@dataclass(frozen=True)
class ResearchGates:
    original_model_verified: bool
    image_source_groups_verified: bool
    cleaned_17class_artifact_hash_verified: bool
    worker_gt_adjudicated: bool
    differentiable_xai_verified: bool
    measured_hardware_energy: bool

    def open_gates(self):
        return [key for key,val in vars(self).items() if not val]

    @property
    def ready_for_final_test(self):
        return not self.open_gates()
