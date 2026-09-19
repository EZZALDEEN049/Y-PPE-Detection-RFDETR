import argparse
import json
import os

from inference_sdk import InferenceConfiguration, InferenceHTTPClient

API_URL = "https://serverless.roboflow.com"
MODELS = {
    "yolo": "altayyar-0oflt-lafos-qqauz-ty5nh/1",
    "rfdetr": "altayyar-0oflt-lafos-qqauz/2",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run inference against either Y-PPE Roboflow deployment."
    )
    parser.add_argument(
        "image",
        help="Path to the input image.",
    )
    parser.add_argument(
        "--model",
        choices=MODELS,
        default="rfdetr",
        help="Deployment to use: yolo or rfdetr (default: rfdetr).",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    api_key = os.getenv("ROBOFLOW_API_KEY")
    if not api_key:
        raise SystemExit("ROBOFLOW_API_KEY is not set.")

    client = InferenceHTTPClient(
        api_url=API_URL,
        api_key=api_key,
    ).configure(
        InferenceConfiguration(api_key_transport="header")
    )

    model_id = MODELS[args.model]
    result = client.infer(args.image, model_id=model_id)

    output = {
        "track": args.model,
        "model_id": model_id,
        "predictions": result,
    }
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
