from pathlib import Path

import pytesseract
from pdf2image import convert_from_path


# ============================================================
# CONFIGURATION
# ============================================================

OCR_DPI = 150

TESSERACT_CONFIG = "--oem 3 --psm 6"


# ============================================================
# TESSERACT PATH - WINDOWS ONLY
# ============================================================

# If Tesseract is already available in PATH,
# you do NOT need to set this.

# pytesseract.pytesseract.tesseract_cmd = (
#     r"C:\Program Files\Tesseract-OCR\tesseract.exe"
# )


# ============================================================
# OCR SINGLE IMAGE
# ============================================================

def ocr_image(image):
    """
    Extract text from a PIL image using Tesseract OCR.
    """

    # Convert image to grayscale
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
    Extract text from a scanned/image-based PDF.

    The PDF is converted to images once and
    each page is processed sequentially.
    """

    pdf_path = Path(pdf_path)

    if not pdf_path.exists():
        raise FileNotFoundError(
            f"PDF file not found: {pdf_path}"
        )

    print("=" * 60)
    print(f"[OCR] Starting OCR: {pdf_path.name}")
    print(f"[OCR] DPI: {OCR_DPI}")
    print("=" * 60)

    # --------------------------------------------------------
    # Convert PDF pages to images
    # --------------------------------------------------------

    pages = convert_from_path(
        str(pdf_path),
        dpi=OCR_DPI,
        grayscale=True,
        thread_count=1
    )

    total_pages = len(pages)

    print(
        f"[OCR] Total pages: {total_pages}"
    )

    extracted_text = []

    # --------------------------------------------------------
    # OCR each page
    # --------------------------------------------------------

    for page_number, page in enumerate(
        pages,
        start=1
    ):

        print(
            f"[OCR] Processing page "
            f"{page_number}/{total_pages}..."
        )

        try:

            text = ocr_image(page)

            if text:

                extracted_text.append(
                    f"\n--- Page {page_number} ---\n"
                    f"{text}"
                )

                print(
                    f"[OCR] Page {page_number}: "
                    f"{len(text)} characters"
                )

            else:

                print(
                    f"[OCR] Page {page_number}: "
                    f"No text detected"
                )

        finally:

            # Release image memory
            page.close()

    # --------------------------------------------------------
    # Combine OCR result
    # --------------------------------------------------------

    result = "\n".join(
        extracted_text
    )

    print("=" * 60)

    print(
        f"[OCR] Completed | "
        f"Characters: {len(result)}"
    )

    print("=" * 60)

    return result


# ============================================================
# MAIN OCR FUNCTION
# ============================================================

def extract_text_with_ocr(pdf_path):
    """
    Main OCR function.
    """

    try:

        return ocr_pdf(pdf_path)

    except Exception as e:

        print(
            f"[OCR ERROR] {e}"
        )

        raise


# ============================================================
# LOCAL TEST
# ============================================================

if __name__ == "__main__":

    pdf_path = r"D:\Resume-Analyzer\test_resume.pdf"

    text = extract_text_with_ocr(
        pdf_path
    )

    print("\n")
    print("=" * 60)
    print("EXTRACTED TEXT")
    print("=" * 60)

    print(text)