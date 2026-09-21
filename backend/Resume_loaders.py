"""
Legacy loader module kept for backward compatibility.
New code should import services directly from app.services.
"""
from pathlib import Path
from app.services.pdf_extractor import extract_text_from_pdf


def exatract_pdf(filepath: str) -> str:
    """Legacy helper function with original typo kept for backwards compatibility."""
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {filepath}")
    with open(path, "rb") as f:
        return extract_text_from_pdf(f.read())


def extract_pdf(filepath: str) -> str:
    """Extracts text from PDF at given filepath."""
    return exatract_pdf(filepath)
