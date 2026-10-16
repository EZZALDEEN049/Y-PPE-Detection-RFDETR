#!/usr/bin/env python3
"""Reproduce a conservative evidence audit. No ML packages, GPU, API keys, or model training."""
import argparse
import json
from pathlib import Path

METRICS = ("map50", "precision", "recall")
RESOURCE_FIELDS = (
    "latency_ms_p50", "latency_ms_p95", "energy_joules_per_image",
    "peak_memory_mb", "hardware_total_cost_usd",
)
DEPLOYMENT_FIELDS = (
    "offline_inference_demonstrated", "independent_field_test_demonstrated",
    "critical_class_false_negative_rate",
)
CONTROLS = (
    "identical_heldout_test_membership_verified", "common_metric_evaluator_verified",
    "common_inference_hardware_verified", "controlled_power_measurements_available",
)


def validate(data):
    if not isinstance(data, dict):
        raise ValueError("Evidence must be a JSON object.")
    models = data.get("models")
    if not isinstance(models, list) or len(models) < 2:
        raise ValueError("At least two separate documented model tracks required.")
    names = [m.get("model_id") for m in models]
    if any(not n or not isinstance(n, str) for n in names) or len(set(names)) != len(names):
        raise ValueError("Each model must have a unique nonempty model_id.")
    controls = data.get("comparison_controls", {})
    if set(controls) != set(CONTROLS) or any(type(v) is not bool for v in controls.values()):
        raise ValueError("All four comparison controls must explicitly be Boolean.")
    for model in models:
        if not model.get("provenance_url", "").startswith("https://"):
            raise ValueError("Each model needs an HTTPS provenance URL.")
        if not model.get("metric_kind"):
            raise ValueError("Every source metric needs an evidence qualifier.")
        metrics = model.get("reported_metrics_pct", {})
        if set(metrics) != set(METRICS):
            raise ValueError("Exactly mAP50, precision and recall are expected.")
        if any(type(v) not in (int, float) or not 0 <= v <= 100 for v in metrics.values()):
            raise ValueError("Percentages must be numeric values between 0 and 100.")
        resources = model.get("measured_resource_metrics", {})
        deployment = model.get("deployment_metrics", {})
        if set(resources) != set(RESOURCE_FIELDS) or set(deployment) != set(DEPLOYMENT_FIELDS):
            raise ValueError("Missing or unexpected evidence fields.")
        for field, val in resources.items():
            if val is not None and (type(val) not in (int, float) or val < 0):
                raise ValueError("Invalid resource measurement: " + field)
        for field, val in deployment.items():
            if field == "critical_class_false_negative_rate":
                if val is not None and (type(val) not in (int, float) or not 0 <= val <= 1):
                    raise ValueError("Critical class false-negative rate must be between 0 and 1.")
            elif val is not None and type(val) is not bool:
                raise ValueError("Deployment demonstration must be true/false/null.")
    return models, controls


def assess(data):
    models, controls = validate(data)
    comparable_accuracy = all(controls[k] for k in (
        "identical_heldout_test_membership_verified", "common_metric_evaluator_verified"
    ))
    comparable_energy = (
        comparable_accuracy
        and controls["common_inference_hardware_verified"]
        and controls["controlled_power_measurements_available"]
        and all(m["measured_resource_metrics"]["energy_joules_per_image"] is not None for m in models)
    )
    comparable_deployment = (
        comparable_accuracy and
        all(m["deployment_metrics"]["independent_field_test_demonstrated"] is True for m in models)
    )
    table = []
    for model in models:
        row = {
            "model_id": model["model_id"],
            "architecture": model["architecture"],
            "provenance_url": model["provenance_url"],
            "metric_qualifier": model["metric_kind"],
            "reported_metrics_pct": model["reported_metrics_pct"],
            "resource_evidence_fields_documented": sorted(
                k for k, v in model["measured_resource_metrics"].items() if v is not None
            ),
            "resource_evidence_fields_not_documented": sorted(
                k for k, v in model["measured_resource_metrics"].items() if v is None
            ),
            "deployment_evidence_fields_documented": sorted(
                k for k, v in model["deployment_metrics"].items() if v is not None
            ),
            "deployment_evidence_fields_not_documented": sorted(
                k for k, v in model["deployment_metrics"].items() if v is None
            ),
        }
        table.append(row)
    return {
        "study_id": data["study_id"],
        "snapshot_date": data["evidence_snapshot_date"],
        "independent_training_performed": False,
        "independent_inference_experiment_performed": False,
        "controlled_accuracy_comparison_established": comparable_accuracy,
        "controlled_energy_comparison_established": comparable_energy,
        "comparative_deployment_claim_established": comparable_deployment,
        "claim_policy": (
            "Descriptive attribution of separately reported platform metrics is permissible. "
            "Do not rank architecture accuracy on a common test, claim energy savings, carbon "
            "savings, deployment readiness, or generalization without the respective gate evidence."
        ),
        "model_evidence": table,
        "unresolved_discordant_claims": data.get("discordant_claims", []),
    }


def markdown(report):
    lines = [
        "# Evidence Audit — auto-generated",
        "",
        "Snapshot: " + report["snapshot_date"],
        "",
        "This is an audit of reported evidence, **not** a new model training or inference experiment.",
        "",
        "| Architecture | Reported mAP@50 | Reported precision | Reported recall |",
        "|---|---:|---:|---:|",
    ]
    for m in report["model_evidence"]:
        v = m["reported_metrics_pct"]
        lines.append("| " + m["architecture"] + " | " +
                     " | ".join(f"{v[k]:.1f}%" for k in METRICS) + " |")
    lines.extend([
        "",
        "All percentages above are attributed to separate public Roboflow model-overview pages.",
        "They **must not** be interpreted as a controlled head-to-head comparison.",
        "",
        "## Claim gates",
    ])
    for key in (
        "controlled_accuracy_comparison_established",
        "controlled_energy_comparison_established",
        "comparative_deployment_claim_established",
    ):
        lines.append("- " + key + ": " + ("established" if report[key] else "NOT ESTABLISHED"))
    lines.extend(["", "## Audited evidence availability"])
    for m in report["model_evidence"]:
        lines.extend([
            "",
            "### " + m["architecture"],
            "- Metric source: " + m["provenance_url"],
            "- Resource measurements not documented in this source audit: " +
            ", ".join(m["resource_evidence_fields_not_documented"]),
            "- Deployment measurements not documented in this source audit: " +
            ", ".join(m["deployment_evidence_fields_not_documented"]),
        ])
    lines.extend([
        "",
        "## Publication integrity limitation",
        "",
        report["claim_policy"],
        "",
        "Missing documentation is coded as unknown/not established, not as evidence of poor model performance.",
        "See PROTOCOL.md for validation and measurement requirements.",
        "",
    ])
    return "\n".join(lines)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--evidence", type=Path, default=Path(__file__).parent / "evidence" / "records.json")
    p.add_argument("--out-dir", type=Path, default=Path(__file__).parent / "outputs")
    args = p.parse_args()
    result = assess(json.loads(args.evidence.read_text(encoding="utf-8")))
    args.out_dir.mkdir(parents=True, exist_ok=True)
    (args.out_dir / "audit_results.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    (args.out_dir / "audit_results.md").write_text(markdown(result), encoding="utf-8")
    print(json.dumps({
        "controlled_accuracy_comparison_established": result["controlled_accuracy_comparison_established"],
        "controlled_energy_comparison_established": result["controlled_energy_comparison_established"],
        "comparative_deployment_claim_established": result["comparative_deployment_claim_established"],
    }, indent=2))


if __name__ == "__main__":
    main()
