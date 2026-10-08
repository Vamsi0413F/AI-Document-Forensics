import os
import fitz
import pytesseract
from PIL import Image


# Windows Tesseract path
if os.name == "nt":
    tesseract_path = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

    if os.path.exists(tesseract_path):
        pytesseract.pytesseract.tesseract_cmd = tesseract_path


def extract_pdf_text(file_path: str) -> dict:
    """
    Extract text from a PDF.

    First tries normal PDF text extraction.
    If a page has no selectable text, OCR is used as a fallback.
    """

    try:
        document = fitz.open(file_path)

        pages = []
        full_text = []

        for page_number, page in enumerate(document):

            # Normal PDF text extraction
            text = page.get_text("text").strip()

            # OCR fallback for scanned/image-only pages
            if not text:
                pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))

                image = Image.frombytes(
                    "RGB",
                    [pix.width, pix.height],
                    pix.samples
                )

                text = pytesseract.image_to_string(image).strip()

                method = "ocr"
            else:
                method = "pdf_text"

            pages.append({
                "page": page_number + 1,
                "text": text,
                "method": method
            })

            if text:
                full_text.append(text)

        document.close()

        return {
            "success": True,
            "method": "pdf_text_or_ocr",
            "page_count": len(pages),
            "text": "\n".join(full_text),
            "pages": pages,
            "error": None
        }

    except Exception as error:
        return {
            "success": False,
            "method": "pdf_text_or_ocr",
            "page_count": 0,
            "text": "",
            "pages": [],
            "error": str(error)
        }


def extract_image_text(file_path: str) -> dict:
    """
    Extract text from PNG/JPG/JPEG images using Tesseract OCR.
    """

    try:
        image = Image.open(file_path)

        text = pytesseract.image_to_string(image).strip()

        return {
            "success": True,
            "method": "ocr",
            "page_count": 1,
            "text": text,
            "pages": [
                {
                    "page": 1,
                    "text": text
                }
            ],
            "error": None
        }

    except Exception as error:
        return {
            "success": False,
            "method": "ocr",
            "page_count": 0,
            "text": "",
            "pages": [],
            "error": str(error)
        }


def extract_text(file_path: str) -> dict:
    """
    Automatically choose the appropriate extraction method
    based on the document type.
    """

    file_path_lower = file_path.lower()

    if file_path_lower.endswith(".pdf"):
        return extract_pdf_text(file_path)

    if file_path_lower.endswith((".png", ".jpg", ".jpeg")):
        return extract_image_text(file_path)

    return {
        "success": False,
        "method": None,
        "page_count": 0,
        "text": "",
        "pages": [],
        "error": "Unsupported file type."
    }