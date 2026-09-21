import os
from pathlib import Path
import tempfile
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware  # 1. Import CORS Middleware
import uvicorn

app = FastAPI()

# 2. Add the URLs allowed to talk to this backend
origins = [
    "http://localhost:3000",      # For local React development
    "http://localhost:5173",      # For local Vite/React development
    "https://resume-analyser-3195c.web.app/",  # Change this to your actual Vercel frontend URL
]

# 3. Apply the CORS Middleware to the app
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,          # Allows requests from your specific frontend URLs
    allow_credentials=True,
    allow_methods=["*"],            # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],            # Allows all headers
)

@app.get("/")
def home():
    return {"message": "Resume Analyzer API is running"}

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "resume-analyzer"}

@app.post("/parse-resume")
async def parse_resume(file: UploadFile = File(...)):
    from Resume_loaders import extract_resume
    from Resume_parser import resume_parse

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
        resume_text = extract_resume(temp_path)

        if not resume_text.strip():
            raise HTTPException(
                status_code=400,
                detail="Could not extract text from the resume."
            )

        resume = resume_parse(resume_text)
        return resume.model_dump()

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
    finally:
        Path(temp_path).unlink(missing_ok=True)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
