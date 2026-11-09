"""Energy computations for actual power measurements, not hypothetical values."""
import csv
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class EnergyReport:
    duration_seconds: float
    gross_joules: float
    idle_adjusted_joules: float
    joules_per_image: float
    idle_adjusted_joules_per_image: float


def integrate_power(samples, images: int, idle_watts: float = 0.0,
                    max_sample_gap_seconds: float = 2.0) -> EnergyReport:
    """Trapezoidal power integration; timestamps must be measured not simulated.

    Input samples: (elapsed_seconds, device_power_watts). Reports measurement
    scope supplied by user; do not mislabel GPU-only as whole-system energy.
    """
    points = [(float(t), float(p)) for t,p in samples]
    if images <= 0 or len(points) < 2 or idle_watts < 0 or max_sample_gap_seconds <= 0:
        raise ValueError("requires image count, 2+ samples, valid idle and gap")
    if any(p < 0 for _,p in points):
        raise ValueError("negative power")
    total, baseline = 0.0, 0.0
    for (t0,p0),(t1,p1) in zip(points, points[1:]):
        dt = t1-t0
        if dt <= 0 or dt > max_sample_gap_seconds:
            raise ValueError("nonincreasing timestamps or unacceptably sparse sampling")
        total += dt*(p0+p1)/2
        baseline += dt*(max(0,p0-idle_watts)+max(0,p1-idle_watts))/2
    return EnergyReport(points[-1][0]-points[0][0],total,baseline,
                        total/images,baseline/images)


def read_meter_csv(path: str):
    with Path(path).open(newline="",encoding="utf-8") as fd:
        return [(float(row["elapsed_seconds"]), float(row["power_watts"]))
                for row in csv.DictReader(fd)]
