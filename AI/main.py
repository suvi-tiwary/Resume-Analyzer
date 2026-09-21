import os
import tempfile
from pathlib import Path

import uvicorn
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from Resume_loaders import extract_resume
from Resume_parser import resume_parse


# ============================================================
# FASTAPI APP
# ============================================================

app = FastAPI(
    title="Resume Analyzer API",
    description="AI-powered resume parsing API",
    version="1.0.0"
)


# ============================================================
# CORS CONFIGURATION
# ============================================================

origins = [
    # Local development
    "http://localhost:3000",
    "http://localhost:5173/",

    # Firebase Hosting
    "https://resume-analyser-3195c.web.app"
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# ROOT ROUTE
# ============================================================

@app.get("/")
def home():
    return {
        "message": "Resume Analyzer API is running",
        "status": "success"
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


# ============================================================
# RESUME PARSER
# ============================================================

@app.post("/parse-resume")
async def parse_resume(file: UploadFile = File(...)):

    # --------------------------------------------------------
    # Validate file
    # --------------------------------------------------------

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No file was uploaded."
        )

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported currently."
        )

    # --------------------------------------------------------
    # Read uploaded file
    # --------------------------------------------------------

    contents = await file.read()

    if not contents:
        raise HTTPException(
            status_code=400,
            detail="Uploaded PDF is empty."
        )

    # --------------------------------------------------------
    # Create temporary PDF
    # --------------------------------------------------------

    temp_path = None

    try:

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".pdf"
        ) as temp_file:

            temp_file.write(contents)
            temp_path = temp_file.name

        print(f"[API] Processing resume: {file.filename}")
        print(f"[API] Temporary file: {temp_path}")

        # ----------------------------------------------------
        # Extract text from resume
        # ----------------------------------------------------

        print("[API] Extracting resume text...")

        resume_text = extract_resume(temp_path)

        if not resume_text:
            raise HTTPException(
                status_code=400,
                detail="Could not extract text from the resume."
            )

        if not resume_text.strip():
            raise HTTPException(
                status_code=400,
                detail="Resume contains no readable text."
            )

        print(
            f"[API] Resume text extracted successfully "
            f"({len(resume_text)} characters)"
        )

        # ----------------------------------------------------
        # Parse resume using AI
        # ----------------------------------------------------

        print("[API] Parsing resume with AI...")

        resume = resume_parse(resume_text)

        print("[API] Resume parsed successfully.")

        # ----------------------------------------------------
        # Return structured response
        # ----------------------------------------------------

        return resume.model_dump()

    # --------------------------------------------------------
    # Expected HTTP errors
    # --------------------------------------------------------

    except HTTPException:
        raise

    # --------------------------------------------------------
    # Unexpected errors
    # --------------------------------------------------------

    except Exception as e:

        print("=" * 60)
        print("[ERROR] Resume parsing failed")
        print(f"[ERROR TYPE] {type(e).__name__}")
        print(f"[ERROR MESSAGE] {str(e)}")
        print("=" * 60)

        raise HTTPException(
            status_code=500,
            detail=f"Resume processing failed: {str(e)}"
        )

    # --------------------------------------------------------
    # Always delete temporary file
    # --------------------------------------------------------

    finally:

        if temp_path:
            try:
                Path(temp_path).unlink(missing_ok=True)
                print("[API] Temporary file deleted.")
            except Exception as cleanup_error:
                print(
                    f"[WARNING] Could not delete temporary file: "
                    f"{cleanup_error}"
                )


# ============================================================
# START SERVER
# ============================================================

if __name__ == "__main__":

    port = int(
        os.environ.get("PORT", 8000)
    )

    print(f"[API] Starting server on port {port}")

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port
    )