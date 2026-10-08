import fitz


def extract_metadata(file_path: str) -> dict:
    """Extract document metadata from a PDF."""

    document = fitz.open(file_path)

    metadata = document.metadata

    result = {
        "title": metadata.get("title"),
        "author": metadata.get("author"),
        "subject": metadata.get("subject"),
        "keywords": metadata.get("keywords"),
        "creator": metadata.get("creator"),
        "producer": metadata.get("producer"),
        "creation_date": metadata.get("creationDate"),
        "modification_date": metadata.get("modDate"),
        "page_count": len(document),
    }

    document.close()

    return result