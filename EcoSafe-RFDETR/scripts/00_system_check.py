import argparse, json, platform, subprocess, sys
from pathlib import Path

def cmd(x):
    try:
        return subprocess.check_output(x, stderr=subprocess.STDOUT, text=True).strip()
    except Exception as e:
        return f"UNAVAILABLE: {e}"

p = argparse.ArgumentParser()
p.add_argument("--out", default="system.json")
a = p.parse_args()

info = {
    "python": sys.version,
    "platform": platform.platform(),
    "nvidia_smi": cmd(["nvidia-smi"]),
}
try:
    import torch
    info.update(torch=torch.__version__, cuda_available=torch.cuda.is_available(), cuda_version=torch.version.cuda)
    if torch.cuda.is_available():
        info["gpu_name"] = torch.cuda.get_device_name(0)
except Exception as e:
    info["torch_error"] = repr(e)
try:
    import importlib.metadata as im
    info["rfdetr"] = im.version("rfdetr")
except Exception:
    info["rfdetr"] = "NOT_INSTALLED"

Path(a.out).parent.mkdir(parents=True, exist_ok=True)
Path(a.out).write_text(json.dumps(info, indent=2), encoding="utf-8")
print(json.dumps(info, indent=2))
