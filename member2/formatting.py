import fitz
from collections import Counter


def analyze_formatting(file_path: str) -> dict:
    """Analyze text formatting and layout properties of a PDF."""

    document = fitz.open(file_path)

    fonts = []
    font_sizes = []
    text_blocks = []

    for page_number, page in enumerate(document, start=1):
        page_data = page.get_text("dict")

        for block in page_data["blocks"]:
            if "lines" not in block:
                continue

            for line in block["lines"]:
                for span in line["spans"]:
                    fonts.append(span["font"])
                    font_sizes.append(span["size"])

                    text_blocks.append({
                        "page": page_number,
                        "text": span["text"],
                        "font": span["font"],
                        "size": span["size"],
                        "bbox": span["bbox"],
                    })

    document.close()

    font_counts = Counter(fonts)
    size_counts = Counter(round(size, 2) for size in font_sizes)

    return {
        "fonts": dict(font_counts),
        "font_sizes": dict(size_counts),
        "text_blocks": text_blocks,
    }