# ocr.py

from pathlib import Path

import pytesseract
from pdf2image import convert_from_path


# ============================================================
# CONFIGURATION
# ============================================================

# Lower DPI = faster OCR
# 150 is a good starting point for resumes.
OCR_DPI = 150

# Tesseract configuration
TESSERACT_CONFIG = "--oem 3 --psm 6"


# ============================================================
# TESSERACT PATH - WINDOWS ONLY
# ============================================================

# If Tesseract is already added to PATH, leave this commented.
#
# pytesseract.pytesseract.tesseract_cmd = (
#     r"C:\Program Files\Tesseract-OCR\tesseract.exe"
# )


# ============================================================
# OCR SINGLE IMAGE
# ============================================================

def ocr_image(image):
    """
    Extract text from a single PIL image.
    """

    # Convert to grayscale
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

    Pages are processed one at a time to reduce memory usage.
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
    # Find number of pages first
    # --------------------------------------------------------

    try:
        from pypdf import PdfReader

        reader = PdfReader(str(pdf_path))
        total_pages = len(reader.pages)

    except Exception:
        total_pages = None

    if total_pages:
        print(f"[OCR] Total pages: {total_pages}")
    else:
        print("[OCR] Total pages: unknown")

    extracted_text = []

    # --------------------------------------------------------
    # Process pages one at a time
    # --------------------------------------------------------

    page_number = 1

    while True:

        print(f"[OCR] Processing page {page_number}...")

        try:

            pages = convert_from_path(
                str(pdf_path),

                # IMPORTANT:
                # Only render one page at a time
                dpi=OCR_DPI,

                first_page=page_number,
                last_page=page_number,

                grayscale=True,

                # Reduce memory usage
                thread_count=1
            )

        except Exception as e:

            # No more pages
            if page_number > 1:
                break

            raise RuntimeError(
                f"Failed to convert PDF to image: {e}"
            )

        # ----------------------------------------------------
        # Stop when there are no more pages
        # ----------------------------------------------------

        if not pages:
            break

        page = pages[0]

        # ----------------------------------------------------
        # OCR
        # ----------------------------------------------------

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

            # Release memory
            page.close()

        page_number += 1

        # If we know the page count, stop here
        if total_pages and page_number > total_pages:
            break

    # --------------------------------------------------------
    # Combine result
    # --------------------------------------------------------

    result = "\n".join(extracted_text)

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

    Import this function from Resume_loaders.py.
    """

    try:

        return ocr_pdf(pdf_path)

    except Exception as e:

        print(f"[OCR ERROR] {e}")

        raise


# ============================================================
# LOCAL TEST
# ============================================================

if __name__ == "__main__":

    pdf_path = r"D:\Resume-Analyzer\test_resume.pdf"

    text = extract_text_with_ocr(pdf_path)

    print("\n")
    print("=" * 60)
    print("EXTRACTED TEXT")
    print("=" * 60)
    print(text)