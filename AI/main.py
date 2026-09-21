import os
import time
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
    "http://localhost:3000",
    "http://localhost:5173",
    "https://resume-analyser-3195c.web.app",
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

        print("=" * 60)
        print(f"[API] Processing resume: {file.filename}")
        print(f"[API] Temporary file: {temp_path}")
        print("=" * 60)

        # ----------------------------------------------------
        # Extract resume text
        # ----------------------------------------------------

        print("[API] Extracting resume text...")

        extraction_start = time.time()

        resume_text = extract_resume(temp_path)

        extraction_time = time.time() - extraction_start

        print(
            f"[TIME] Resume extraction: "
            f"{extraction_time:.2f} seconds"
        )

        # ----------------------------------------------------
        # Validate extracted text
        # ----------------------------------------------------

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

        parsing_start = time.time()

        resume = resume_parse(resume_text)

        parsing_time = time.time() - parsing_start

        print(
            f"[TIME] AI parsing: "
            f"{parsing_time:.2f} seconds"
        )

        print("=" * 60)
        print(
            f"[TIME] TOTAL: "
            f"{time.time() - extraction_start:.2f} seconds "
            f"(from extraction start)"
        )
        print("[API] Resume parsed successfully.")
        print("=" * 60)

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
                    "[WARNING] Could not delete temporary file: "
                    f"{cleanup_error}"
                )


# ============================================================
# START SERVER
# ============================================================

if __name__ == "__main__":

    port = int(
        os.environ.get("PORT", 8000)
    )

    print(
        f"[API] Starting server on port {port}"
    )

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port
    )