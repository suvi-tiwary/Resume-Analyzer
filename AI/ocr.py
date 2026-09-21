import easyocr
import numpy as np
from pdf2image import convert_from_path


def ocr_image(image_path: str) -> str:

    reader = easyocr.Reader(
        ["en"],
        gpu=False
    )

    result = reader.readtext(
        image_path,
        detail=0
    )

    return "\n".join(result).strip()


def ocr_pdf(pdf_path: str) -> str:

    reader = easyocr.Reader(
        ["en"],
        gpu=False
    )

    pages = convert_from_path(
        pdf_path,
        dpi=200
    )

    extracted_text = []

    for page in pages:

        page_array = np.array(page)

        result = reader.readtext(
            page_array,
            detail=0
        )

        extracted_text.extend(result)

    return "\n".join(extracted_text).strip()