import argparse
import os

from roboflow import Roboflow

PROJECTS = {
    "yolo": {
        "workspace": "master-fylfq",
        "project": "altayyar-0oflt-lafos-qqauz-ty5nh",
        "version": 1,
    },
    "rfdetr": {
        "workspace": "softyyemen",
        "project": "altayyar-0oflt-lafos-qqauz",
        "version": 2,
    },
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Download one of the two Y-PPE Roboflow project versions."
    )
    parser.add_argument(
        "--project",
        choices=PROJECTS,
        default="rfdetr",
        help="Project track to download: yolo or rfdetr (default: rfdetr).",
    )
    parser.add_argument(
        "--format",
        default="yolov11",
        help="Roboflow export format (default: yolov11).",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    api_key = os.getenv("ROBOFLOW_API_KEY")
    if not api_key:
        raise SystemExit("ROBOFLOW_API_KEY is not set.")

    cfg = PROJECTS[args.project]
    rf = Roboflow(api_key=api_key)
    project = rf.workspace(cfg["workspace"]).project(cfg["project"])
    version = project.version(cfg["version"])
    dataset = version.download(args.format)

    print(f"Track: {args.project}")
    print(f"Workspace: {cfg['workspace']}")
    print(f"Project: {cfg['project']}")
    print(f"Version: {cfg['version']}")
    print(f"Dataset downloaded to: {dataset.location}")


if __name__ == "__main__":
    main()
