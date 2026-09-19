import json
import os
import sys
from inference_sdk import InferenceHTTPClient, InferenceConfiguration

MODEL_ID = "altayyar-0oflt-lafos-qqauz-ty5nh/1"
API_URL = "https://serverless.roboflow.com"


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python scripts/roboflow_inference.py path/to/image.jpg")

    api_key = os.getenv("ROBOFLOW_API_KEY")
    if not api_key:
        raise SystemExit("ROBOFLOW_API_KEY is not set.")

    image_path = sys.argv[1]
    client = InferenceHTTPClient(
        api_url=API_URL,
        api_key=api_key,
    ).configure(
        InferenceConfiguration(api_key_transport="header")
    )

    result = client.infer(image_path, model_id=MODEL_ID)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
