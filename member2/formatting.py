import pymupdf
from collections import Counter


def analyze_formatting(file_path: str) -> dict:
    """Analyze PDF formatting and identify unusual formatting patterns."""

    document = pymupdf.open(file_path)

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
                    font = span["font"]
                    size = round(span["size"], 2)

                    fonts.append(font)
                    font_sizes.append(size)

                    text_blocks.append({
                        "page": page_number,
                        "text": span["text"],
                        "font": font,
                        "size": size,
                        "bbox": list(span["bbox"]),
                    })

    document.close()

    font_counts = Counter(fonts)
    size_counts = Counter(font_sizes)

    anomalies = []

    if not text_blocks:
        return {
            "fonts": {},
            "font_sizes": {},
            "text_blocks": [],
            "anomalies": [],
        }

    dominant_font = font_counts.most_common(1)[0][0]
    dominant_size = size_counts.most_common(1)[0][0]

    for index, block in enumerate(text_blocks):

        # Ignore the first few blocks because they commonly contain
        # titles, headers, or introductory information.
        if index < 4:
            continue

        reasons = []

        font_is_different = block["font"] != dominant_font
        size_is_different = block["size"] != dominant_size

        previous_blocks = text_blocks[max(0, index - 2):index]
        next_blocks = text_blocks[index + 1:index + 3]

        surrounding_blocks = previous_blocks + next_blocks

        if surrounding_blocks:
            dominant_surrounding_font = Counter(
                item["font"] for item in surrounding_blocks
            ).most_common(1)[0][0]

            dominant_surrounding_size = Counter(
                item["size"] for item in surrounding_blocks
            ).most_common(1)[0][0]

            surrounding_font_matches = sum(
                item["font"] == dominant_surrounding_font
                for item in surrounding_blocks
            )

            surrounding_size_matches = sum(
                item["size"] == dominant_surrounding_size
                for item in surrounding_blocks
            )

            if (
                font_is_different
                and block["font"] != dominant_surrounding_font
                and surrounding_font_matches >= 2
            ):
                reasons.append(
                    f"Unusual font ({block['font']})"
                )

            if (
                size_is_different
                and block["size"] != dominant_surrounding_size
                and surrounding_size_matches >= 2
            ):
                reasons.append(
                    f"Unusual font size ({block['size']})"
                )

        if reasons:
            anomalies.append({
                "page": block["page"],
                "text": block["text"],
                "font": block["font"],
                "size": block["size"],
                "bbox": block["bbox"],
                "reasons": reasons,
            })

    return {
        "fonts": dict(font_counts),
        "font_sizes": dict(size_counts),
        "dominant_font": dominant_font,
        "dominant_font_size": dominant_size,
        "text_blocks": text_blocks,
        "anomalies": anomalies,
    }