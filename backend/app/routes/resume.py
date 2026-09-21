import logging
from fastapi import APIRouter, UploadFile, File, HTTPException, status
from ..schemas.resume import ResumeResponse
from ..utils.validators import validate_uploaded_file
from ..services.pdf_extractor import extract_text_from_pdf
from ..services.ocr_service import (
    extract_text_from_image,
    extract_text_from_scanned_pdf,
    OCRError,
)
from ..services.resume_parser import parse_resume_text

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/resume", tags=["Resume"])


@router.post(
    "/parse",
    response_model=ResumeResponse,
    status_code=status.HTTP_200_OK,
    summary="Extract and parse resume information",
    description=(
        "Upload a resume file in PDF, JPG, JPEG, or PNG format. "
        "The endpoint extracts raw text via direct extraction or OCR, "
        "and returns structured JSON with personal details, skills, education, and work experience."
    ),
    responses={
        200: {
            "description": "Successfully parsed resume into structured JSON.",
            "model": ResumeResponse,
        },
        400: {
            "description": "Unsupported file format, empty file, or unreadable document.",
        },
        422: {
            "description": "OCR processing error or missing OCR engine.",
        },
        500: {
            "description": "Internal server error during document processing.",
        },
    },
)
async def parse_resume(
    file: UploadFile = File(
        ...,
        description="Resume file to parse (supported: PDF, JPG, JPEG, PNG, max 10MB)",
    )
) -> ResumeResponse:
    # 1. Validate file format, size, and presence
    file_bytes, file_type = await validate_uploaded_file(file)

    raw_text = ""

    # 2. Process based on document type
    try:
        if file_type == "pdf":
            # Step A: Attempt direct digital text extraction
            raw_text = extract_text_from_pdf(file_bytes)

            # Step B: If digital text is insufficient or empty, attempt OCR on scanned pages
            if not raw_text.strip():
                logger.info("Direct text extraction yielded no text; attempting OCR on PDF pages.")
                raw_text = extract_text_from_scanned_pdf(file_bytes)

        elif file_type == "image":
            # Direct OCR on image bytes
            raw_text = extract_text_from_image(file_bytes)

    except OCRError as ocr_err:
        logger.warning("OCR processing error: %s", ocr_err)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=str(ocr_err)
        )
    except Exception as e:
        logger.exception("Unexpected error during text extraction: %s", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while extracting text from the file."
        )

    # 3. Check if any text could be extracted
    if not raw_text or not raw_text.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unable to extract readable text from this file."
        )

    # 4. Parse extracted text into structured resume model
    try:
        parsed_resume = parse_resume_text(raw_text)
        return parsed_resume
    except Exception as e:
        logger.exception("Error parsing resume text: %s", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while structuring the resume data."
        )
