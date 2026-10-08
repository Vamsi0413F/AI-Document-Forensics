import pymupdf


def extract_metadata(file_path: str) -> dict:
    """Extract PDF metadata and basic document information."""

    document = pymupdf.open(file_path)

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
        "has_metadata": any(
            metadata.get(field)
            for field in [
                "title",
                "author",
                "subject",
                "keywords",
                "creator",
                "producer",
                "creationDate",
                "modDate",
            ]
        ),
    }

    document.close()

    return result