# ocr.py

import os
import tempfile
from pathlib import Path

import pytesseract
from pdf2image import convert_from_path


# ============================================================
# CONFIGURATION
# ============================================================

# 150 DPI is a good balance between OCR speed and accuracy.
OCR_DPI = 150

# Tesseract configuration
TESSERACT_CONFIG = "--oem 3 --psm 6"


# ============================================================
# TESSERACT PATH
# ============================================================

# Windows:
# If Tesseract is already added to PATH, you don't need this.
#
# Otherwise uncomment and change the path:
#
# pytesseract.pytesseract.tesseract_cmd = (
#     r"C:\Program Files\Tesseract-OCR\tesseract.exe"
# )


# ============================================================
# OCR SINGLE IMAGE
# ============================================================

def ocr_image(image):
    """
    Extract text from a single PIL image using Tesseract OCR.
    """

    # Convert image to grayscale.
    # This reduces processing and usually works well for resumes.
    image = image.convert("L")

    text = pytesseract.image_to_string(
        image,
        config=TESSERACT_CONFIG
    )

    return text.strip()


# ============================================================
# OCR PDF
# ============================================================

def ocr_pdf(pdf_path):
    """
    Convert a scanned/image-based PDF into images
    and extract text using OCR.

    Parameters
    ----------
    pdf_path : str or Path
        Path to the PDF file.

    Returns
    -------
    str
        Extracted text from the complete PDF.
    """

    pdf_path = Path(pdf_path)

    if not pdf_path.exists():
        raise FileNotFoundError(
            f"PDF file not found: {pdf_path}"
        )

    print(f"[OCR] Processing: {pdf_path.name}")
    print(f"[OCR] DPI: {OCR_DPI}")

    # Convert PDF pages to images.
    #
    # 150 DPI is much faster than 300 DPI
    # and is usually sufficient for resume OCR.
    pages = convert_from_path(
        str(pdf_path),
        dpi=OCR_DPI,
        grayscale=True
    )

    extracted_text = []

    total_pages = len(pages)

    for page_number, page in enumerate(pages, start=1):

        print(
            f"[OCR] Processing page "
            f"{page_number}/{total_pages}..."
        )

        text = pytesseract.image_to_string(
            page,
            config=TESSERACT_CONFIG
        )

        if text.strip():
            extracted_text.append(
                f"\n--- Page {page_number} ---\n"
                f"{text.strip()}"
            )

        # Release the PIL image from memory
        page.close()

    result = "\n".join(extracted_text)

    print(
        f"[OCR] Completed. "
        f"Extracted {len(result)} characters."
    )

    return result


# ============================================================
# OCR WITH FALLBACK
# ============================================================

def extract_text_with_ocr(pdf_path):
    """
    Main OCR function.

    This is the function you can import
    from Resume_loaders.py.
    """

    try:
        return ocr_pdf(pdf_path)

    except Exception as e:
        print(f"[OCR ERROR] {e}")
        raise


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    # Put your test PDF path here.
    pdf_path = r"D:\Resume-Analyzer\test_resume.pdf"

    text = extract_text_with_ocr(pdf_path)

    print("\n" + "=" * 60)
    print("EXTRACTED TEXT")
    print("=" * 60)

    print(text)