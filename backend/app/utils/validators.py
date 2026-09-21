import os
from fastapi import UploadFile, HTTPException

MAX_FILE_SIZE_MB = int(os.getenv("MAX_FILE_SIZE_MB", "10"))
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024

SUPPORTED_EXTENSIONS = {".pdf", ".jpg", ".jpeg", ".png"}
SUPPORTED_MIME_TYPES = {
    "application/pdf",
    "image/jpeg",
    "image/pjpeg",
    "image/png",
    "application/octet-stream",  # some clients send this, handled if extension matches
}


async def validate_uploaded_file(file: UploadFile) -> tuple[bytes, str]:
    """
    Validates uploaded file type, size, and content.
    Returns a tuple of (file_bytes, normalized_file_type) where normalized_file_type is 'pdf' or 'image'.
    Raises HTTPException(400) if validation fails.
    """
    if not file or not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No file was uploaded."
        )

    filename_lower = file.filename.lower()
    ext = os.path.splitext(filename_lower)[1]

    # Validate file extension
    if ext not in SUPPORTED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file type. Please upload a PDF, JPG, JPEG, or PNG file."
        )

    # Validate MIME type if available
    content_type = file.content_type.lower() if file.content_type else ""
    if content_type and content_type not in SUPPORTED_MIME_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file type. Please upload a PDF, JPG, JPEG, or PNG file."
        )

    # Read uploaded file contents into memory
    contents = await file.read()

    # Check for empty file
    if not contents or len(contents) == 0:
        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty."
        )

    # Check file size limit
    if len(contents) > MAX_FILE_SIZE_BYTES:
        raise HTTPException(
            status_code=400,
            detail=f"File size exceeds maximum allowed limit of {MAX_FILE_SIZE_MB} MB."
        )

    file_type = "pdf" if ext == ".pdf" else "image"
    return contents, file_type
