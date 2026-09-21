import requests
import json

resume_path = r"AI/Suvi Tiwary Resume.pdf"

with open(resume_path, "rb") as file:
    response = requests.post(
        "http://127.0.0.1:8000/parse-resume",
        files={"file": file}
    )

response.raise_for_status()

result = response.json()

print(json.dumps(result, indent=4, ensure_ascii=False))