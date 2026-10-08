from pathlib import Path


SUPPORTED_EXTENSIONS = {".pdf", ".png", ".jpg", ".jpeg"}


def validate_document(file_path: str) -> dict:
    """
    Validate whether the uploaded document is a supported file type.
    """

    path = Path(file_path)

    if not path.exists():
        return {
            "valid": False,
            "filename": path.name,
            "file_type": None,
            "error": "File does not exist."
        }

    extension = path.suffix.lower()

    if extension not in SUPPORTED_EXTENSIONS:
        return {
            "valid": False,
            "filename": path.name,
            "file_type": extension,
            "error": "Unsupported file type."
        }

    file_type = extension.replace(".", "")

    return {
        "valid": True,
        "filename": path.name,
        "file_type": file_type,
        "error": None
    }