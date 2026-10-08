import fitz
import pytesseract
from PIL import Image


def extract_pdf_text(file_path: str) -> dict:
    """
    Extract selectable text from a PDF using PyMuPDF.
    """

    try:
        document = fitz.open(file_path)

        pages = []
        full_text = []

        for page_number, page in enumerate(document):
            text = page.get_text("text").strip()

            pages.append({
                "page": page_number + 1,
                "text": text
            })

            if text:
                full_text.append(text)

        document.close()

        return {
            "success": True,
            "method": "pdf_text",
            "page_count": len(pages),
            "text": "\n".join(full_text),
            "pages": pages,
            "error": None
        }

    except Exception as error:
        return {
            "success": False,
            "method": "pdf_text",
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