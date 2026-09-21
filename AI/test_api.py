import argparse
import json
from pathlib import Path

import requests


def test_parse_resume(pdf_path: str, api_url: str) -> None:
    path = Path(pdf_path)

    if not path.is_file():
        raise FileNotFoundError(f"PDF not found: {path}")

    if path.suffix.lower() != ".pdf":
        raise ValueError("The selected file must be a PDF.")

    endpoint = f"{api_url.rstrip('/')}/parse-resume"

    with path.open("rb") as pdf_file:
        response = requests.post(
            endpoint,
            files={"file": (path.name, pdf_file, "application/pdf")},
            timeout=180,
        )

    print(f"HTTP {response.status_code}")

    try:
        print(json.dumps(response.json(), indent=2))
    except ValueError:
        print(response.text)

    response.raise_for_status()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Upload a PDF to the Resume Analyzer API."
    )
    parser.add_argument("pdf_path", help="Path to the PDF resume")
    parser.add_argument(
        "--url",
        default="https://resume-analyzer-1-l0rv.onrender.com",
        help="API base URL",
    )
    args = parser.parse_args()

    test_parse_resume(args.pdf_path, args.url)