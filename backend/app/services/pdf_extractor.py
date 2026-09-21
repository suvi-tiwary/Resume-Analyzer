import io
import logging
from typing import Optional

logger = logging.getLogger(__name__)


def extract_text_from_pdf(file_bytes: bytes) -> str:
    """
    Extracts text from a text-based PDF from in-memory bytes.
    Uses PyMuPDF (fitz) as primary extractor, with pypdf as fallback.
    Returns extracted text, or an empty string if the PDF is scanned or contains negligible text.
    """
    if not file_bytes:
        return ""

    text = ""

    # Primary extractor: PyMuPDF
    try:
        import pymupdf
        doc = pymupdf.open(stream=file_bytes, filetype="pdf")
        extracted_pages = []
        for page in doc:
            page_text = page.get_text("text")
            if page_text:
                extracted_pages.append(page_text)
        doc.close()
        text = "\n\n".join(extracted_pages).strip()
    except Exception as e:
        logger.warning("PyMuPDF text extraction encountered an issue: %s. Trying pypdf fallback.", e)
        text = ""

    # Fallback extractor: pypdf (if PyMuPDF returned no text or failed)
    if not text:
        try:
            import pypdf
            reader = pypdf.PdfReader(io.BytesIO(file_bytes))
            fallback_pages = []
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    fallback_pages.append(page_text)
            text = "\n\n".join(fallback_pages).strip()
        except Exception as e:
            logger.warning("pypdf extraction failed: %s", e)
            text = ""

    # Check if text is usable (more than just a few whitespace/stray characters)
    alphanumeric_count = sum(1 for c in text if c.isalnum())
    if alphanumeric_count < 30:
        logger.info("PDF contains insufficient extractable text (%d alphanumeric chars). OCR may be needed.", alphanumeric_count)
        return ""

    return text
