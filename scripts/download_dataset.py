import os
from roboflow import Roboflow

WORKSPACE = "master-fylfq"
PROJECT = "altayyar-0oflt-lafos-qqauz-ty5nh"
VERSION = 1
FORMAT = "yolov11"


def main() -> None:
    api_key = os.getenv("ROBOFLOW_API_KEY")
    if not api_key:
        raise SystemExit("ROBOFLOW_API_KEY is not set.")

    rf = Roboflow(api_key=api_key)
    project = rf.workspace(WORKSPACE).project(PROJECT)
    version = project.version(VERSION)
    dataset = version.download(FORMAT)
    print(f"Dataset downloaded to: {dataset.location}")


if __name__ == "__main__":
    main()
