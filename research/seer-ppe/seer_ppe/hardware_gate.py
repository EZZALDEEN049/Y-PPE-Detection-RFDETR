"""Truthful physical-meter capability inventory; no inferred joules."""
from __future__ import annotations
import importlib.util,json,platform
from pathlib import Path

def probe() -> dict:
    try:
        import torch
        gpu=bool(torch.cuda.is_available())
        torch_version=torch.__version__
        gpu_name=torch.cuda.get_device_name(0) if gpu else None
    except ImportError:
        gpu=False;torch_version=None;gpu_name=None
    rapl=list(Path('/sys/class/powercap').glob('intel-rapl*/energy_uj')) if Path('/sys/class/powercap').exists() else []
    # Presence of a module alone does not prove a working meter.
    nvml_available=bool(importlib.util.find_spec('pynvml'))
    usable_power_sources=[]
    for p in rapl:
        try:
            p.read_text()
            usable_power_sources.append(str(p))
        except (PermissionError,OSError):
            pass
    return {
        'os':platform.platform(), 'cpu_processor':platform.processor(),
        'torch_version':torch_version,'torch_cuda_available':gpu,
        'cuda_device':gpu_name,'rapl_readable_sources':usable_power_sources,
        'nvml_package_installed':nvml_available,
        'physical_energy_measurement_performed':False,
        'energy_joules_measured':None,
        'status':'PENDING_MEASURABLE_HARDWARE',
        'note':'No numeric energy saving or joule estimate can be inferred from this probe.',
    }

if __name__=='__main__':print(json.dumps(probe(),indent=2))
