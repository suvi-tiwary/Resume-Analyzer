from pathlib import Path

from PIL import Image
from langchain_community.document_loaders import PyPDFLoader

from ocr import ocr_pdf, ocr_image


# ============================================================
# PDF TEXT EXTRACTION
# ============================================================

def extract_pdf(filepath: str) -> str:
    """
    Extract text from a normal PDF.

    If the PDF does not contain enough readable text,
    OCR is used as a fallback.
    """

    loader = PyPDFLoader(filepath)

    documents = loader.load()

    text = "\n\n".join(
        document.page_content
        for document in documents
    ).strip()

    print(
        f"[PDF] Extracted text characters: "
        f"{len(text)}"
    )

    # --------------------------------------------------------
    # Normal PDF
    # --------------------------------------------------------

    if len(text.strip()) > 100:

        print(
            "[PDF] Sufficient text found. "
            "Skipping OCR."
        )

        return text

    # --------------------------------------------------------
    # Scanned / image PDF
    # --------------------------------------------------------

    print(
        "[PDF] Not enough readable text. "
        "Starting OCR..."
    )

    return ocr_pdf(filepath)


# ============================================================
# MAIN RESUME EXTRACTION
# ============================================================

def extract_resume(filepath: str) -> str:
    """
    Extract text from supported resume files.
    """

    filepath = str(
        Path(filepath)
    )

    lower_filepath = filepath.lower()

    # --------------------------------------------------------
    # PDF
    # --------------------------------------------------------

    if lower_filepath.endswith(".pdf"):

        return extract_pdf(
            filepath
        )

    # --------------------------------------------------------
    # Images
    # --------------------------------------------------------

    if lower_filepath.endswith(
        (".jpg", ".jpeg", ".png")
    ):

        image = Image.open(filepath)

        try:

            return ocr_image(image)

        finally:

            image.close()

    # --------------------------------------------------------
    # Unsupported format
    # --------------------------------------------------------

    raise ValueError(
        "Only PDF, JPG, JPEG and PNG files are supported."
    )