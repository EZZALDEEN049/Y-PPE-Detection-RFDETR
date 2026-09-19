#!/usr/bin/env python3
"""Download a Roboflow dataset version without exposing the API key in CLI arguments.

The API key is read only from the ROBOFLOW_API_KEY environment variable.
This script is intended for GitHub Actions or a local shell where the secret is
stored outside source control.
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from roboflow import Roboflow


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--workspace", required=True)
    ap.add_argument("--project", required=True)
    ap.add_argument("--version", required=True, type=int)
    ap.add_argument("--format", default="yolov11")
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--metadata-out", type=Path)
    args = ap.parse_args()

    api_key = os.environ.get("ROBOFLOW_API_KEY")
    if not api_key:
        raise SystemExit("ROBOFLOW_API_KEY is not set.")

    args.out.mkdir(parents=True, exist_ok=True)
    old_cwd = Path.cwd()
    os.chdir(args.out)
    try:
        rf = Roboflow(api_key=api_key)
        project = rf.workspace(args.workspace).project(args.project)
        version = project.version(args.version)
        dataset = version.download(args.format)
        location = Path(dataset.location).resolve()
    finally:
        os.chdir(old_cwd)

    metadata = {
        "workspace": args.workspace,
        "project": args.project,
        "version": args.version,
        "format": args.format,
        "dataset_location": str(location),
    }
    if args.metadata_out:
        args.metadata_out.parent.mkdir(parents=True, exist_ok=True)
        args.metadata_out.write_text(json.dumps(metadata, indent=2), encoding="utf-8")

    # GitHub Actions can consume the final line without ever printing the secret.
    print(json.dumps(metadata))


if __name__ == "__main__":
    main()
