import fitz


def analyze_visual_elements(file_path: str) -> dict:
    """Analyze embedded visual elements and their positions in a PDF."""

    document = fitz.open(file_path)

    images = []

    for page_number, page in enumerate(document, start=1):
        image_list = page.get_images(full=True)

        for image in image_list:
            xref = image[0]
            rectangles = page.get_image_rects(xref)

            for rect in rectangles:
                images.append({
                    "page": page_number,
                    "xref": xref,
                    "bbox": [
                        rect.x0,
                        rect.y0,
                        rect.x1,
                        rect.y1
                    ]
                })

    document.close()

    return {
        "image_count": len(images),
        "images": images,
    }