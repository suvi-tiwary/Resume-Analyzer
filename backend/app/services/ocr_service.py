import io
import os
import shutil
import logging
from PIL import Image
import pytesseract

logger = logging.getLogger(__name__)


class OCRError(Exception):
    """Exception raised when OCR processing fails or OCR engine is missing."""
    pass


# Auto-configure tesseract path if found in standard Windows locations or env var
def _configure_tesseract():
    custom_cmd = os.getenv("TESSERACT_CMD")
    if custom_cmd and os.path.exists(custom_cmd):
        pytesseract.pytesseract.tesseract_cmd = custom_cmd
        return

    # Check common Windows installation locations
    standard_windows_paths = [
        r"C:\Program Files\Tesseract-OCR\tesseract.exe",
        r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
        os.path.expanduser(r"~\AppData\Local\Tesseract-OCR\tesseract.exe"),
    ]
    for path in standard_windows_paths:
        if os.path.exists(path):
            pytesseract.pytesseract.tesseract_cmd = path
            logger.info("Found Tesseract at: %s", path)
            return


_configure_tesseract()


def is_tesseract_available() -> bool:
    """Checks if tesseract executable is available."""
    cmd = pytesseract.pytesseract.tesseract_cmd
    if os.path.isabs(cmd):
        return os.path.exists(cmd)
    return shutil.which(cmd) is not None


def extract_text_from_image(image_bytes: bytes) -> str:
    """
    Extracts text from image bytes (JPG, JPEG, PNG) using OCR.
    Raises OCRError if Tesseract is unavailable or processing fails.
    """
    if not image_bytes:
        return ""

    if not is_tesseract_available():
        raise OCRError(
            "Tesseract OCR is not installed or not found in system PATH. "
            "Please install Tesseract OCR (e.g. from UB-Mannheim/tesseract) to enable OCR for images."
        )

    try:
        image = Image.open(io.BytesIO(image_bytes))
        # Convert non-RGB modes to RGB for OCR compatibility
        if image.mode in ("RGBA", "P", "LA"):
            image = image.convert("RGB")

        text = pytesseract.image_to_string(image)
        return text.strip()
    except (pytesseract.TesseractNotFoundError, FileNotFoundError) as e:
        logger.error("Tesseract not found: %s", e)
        raise OCRError(
            "Tesseract OCR engine is not available. Please verify system installation."
        ) from e
    except Exception as e:
        logger.error("OCR image extraction failed: %s", e)
        raise OCRError(f"Failed to perform OCR on image: {str(e)}") from e


def extract_text_from_scanned_pdf(file_bytes: bytes) -> str:
    """
    Extracts text from scanned PDF pages by rendering pages to images with PyMuPDF and running OCR.
    Raises OCRError if Tesseract is unavailable or processing fails.
    """
    if not file_bytes:
        return ""

    if not is_tesseract_available():
        raise OCRError(
            "Tesseract OCR is not installed or not found in system PATH. "
            "Scanned PDF requires Tesseract OCR for text extraction."
        )

    try:
        import pymupdf
        doc = pymupdf.open(stream=file_bytes, filetype="pdf")
        page_texts = []

        for page_index in range(len(doc)):
            page = doc[page_index]
            # Render page to high-res pixmap for accurate OCR
            pix = page.get_pixmap(dpi=200)
            page_img = Image.open(io.BytesIO(pix.tobytes("png")))
            page_text = pytesseract.image_to_string(page_img)
            if page_text:
                page_texts.append(page_text.strip())

        doc.close()
        return "\n\n".join(page_texts).strip()
    except (pytesseract.TesseractNotFoundError, FileNotFoundError) as e:
        raise OCRError("Tesseract OCR is not available to process scanned PDF.") from e
    except OCRError:
        raise
    except Exception as e:
        logger.error("OCR PDF extraction failed: %s", e)
        raise OCRError(f"Failed to perform OCR on scanned PDF: {str(e)}") from e
