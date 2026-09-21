import easyocr
from pdf2image import convert_from_path
import numpy as np


# ============================================================
# LOAD OCR MODEL
# ============================================================

reader = easyocr.Reader(
    ["en"],
    gpu=False
)


# ============================================================
# IMAGE OCR
# ============================================================

def ocr_image(image_path: str) -> str:
    """
    Extract text from JPG / JPEG / PNG.
    """

    result = reader.readtext(
        image_path,
        detail=0
    )

    return "\n".join(result)


# ============================================================
# SCANNED PDF OCR
# ============================================================

def ocr_pdf(pdf_path: str) -> str:
    """
    Convert PDF pages into images
    and extract text using EasyOCR.
    """

    pages = convert_from_path(
        pdf_path,
        dpi=300
    )

    extracted_text = []

    for page in pages:

        # PIL image → NumPy array
        page_array = np.array(page)

        result = reader.readtext(
            page_array,
            detail=0
        )

        extracted_text.extend(result)

    return "\n".join(extracted_text)