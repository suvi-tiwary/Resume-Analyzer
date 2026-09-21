from langchain_community.document_loaders import PyPDFLoader
from ocr import ocr_pdf, ocr_image


def extract_pdf(filepath: str) -> str:
    loader = PyPDFLoader(filepath)
    documents = loader.load()

    text = "\n\n".join(
        document.page_content
        for document in documents
    ).strip()

    if text:
        return text

    return ocr_pdf(filepath)


def extract_resume(filepath: str) -> str:
    filepath = filepath.lower()

    if filepath.endswith(".pdf"):
        return extract_pdf(filepath)

    if filepath.endswith((".jpg", ".jpeg", ".png")):
        return ocr_image(filepath)

    raise ValueError(
        "Only PDF, JPG, JPEG and PNG files are supported."
    )