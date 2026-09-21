from fastapi import FastAPI, UploadFile, File, HTTPException
from pathlib import Path
import tempfile

from Resume_loaders import extract_resume
from Resume_parser import resume_parse


app = FastAPI()


@app.get("/")
def home():
    return {"message": "Resume Analyzer API is running"}


@app.post("/parse-resume")
async def parse_resume(file: UploadFile = File(...)):

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported currently."
        )

    contents = await file.read()

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".pdf"
    ) as temp_file:

        temp_file.write(contents)
        temp_path = temp_file.name

    try:
        # PDF → text
       resume_text = extract_resume(temp_path)

        if not resume_text.strip():
            raise HTTPException(
                status_code=400,
                detail="Could not extract text from the resume."
            )

        # text → structured resume
        resume = resume_parse(resume_text)

        return resume.model_dump()

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    finally:
        Path(temp_path).unlink(missing_ok=True)