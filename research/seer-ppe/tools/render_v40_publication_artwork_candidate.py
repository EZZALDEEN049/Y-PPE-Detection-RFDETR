#!/usr/bin/env python3
"""Offline publication artwork candidate. Uses existing validated numeric maps.
No inference, no source photo access, no raw target/source IDs in artwork.
Run privately, inspect outputs, do not upload without rights/author approval.
"""
from copy import deepcopy
import argparse
import json
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import render_v34b_scientific_figures as renderer

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", type=Path, default=renderer.SOURCE_DEFAULT)
    ap.add_argument("--output-dir", type=Path, required=True)
    args = ap.parse_args()
    original = renderer.validate_and_prepare(json.loads(args.source.read_text(encoding="utf-8")))
    safe = deepcopy(original)
    labels = {}
    for index, item in enumerate(safe, 1):
        meta = item["meta"]
        source_key = meta["image_key"]
        if source_key not in labels:
            labels[source_key] = f"image:H{len(labels)+1:02d}"
        meta["image_key"] = labels[source_key]
        meta["target_id"] = f"H{index:02d}"
    displayed = np.concatenate([np.concatenate([x["fine"].ravel(), x["direct"].ravel()]) for x in safe])
    scale = float(np.percentile(np.abs(displayed), renderer.SCALE_PERCENTILE, method="linear"))
    assert len(safe) == 10
    for a,b in zip(original,safe):
        for key in ("fine","direct","pooled"):
            assert np.array_equal(a[key],b[key]), key
        for key in ("rho_recomputed","tau_recomputed","overlap","top_direct","top_pooled"):
            assert a[key] == b[key], key
    args.output_dir.mkdir(parents=True, exist_ok=True)
    # Existing renderer writes to the extension of output_path; PDFs retain vector text.
    f = renderer.render_summary(safe,args.output_dir/"Figure_1.pdf")
    plt.close(f)
    for index,item in enumerate(safe,1):
        f = renderer.render_target(item,scale,args.output_dir/f"Figure_S{index}.pdf")
        plt.close(f)
    print("11 candidate PDF artworks created; visual/privacy and effective-resolution QA pending.")

if __name__ == "__main__":
    main()
