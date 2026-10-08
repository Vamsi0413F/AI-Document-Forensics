import pymupdf


def analyze_visual_elements(file_path: str) -> dict:
    """Analyze embedded images and their positions in a PDF."""

    document = pymupdf.open(file_path)

    images = []

    for page_number, page in enumerate(document, start=1):
        page_width = page.rect.width
        page_height = page.rect.height
        page_area = page_width * page_height

        image_list = page.get_images(full=True)

        for image in image_list:
            xref = image[0]

            # An image can appear more than once on a page.
            rectangles = page.get_image_rects(xref)

            for rect in rectangles:
                width = rect.width
                height = rect.height
                area = width * height

                # Percentage of the page occupied by the image.
                area_ratio = area / page_area if page_area else 0

                images.append({
                    "page": page_number,
                    "xref": xref,
                    "width": round(width, 2),
                    "height": round(height, 2),
                    "area_ratio": round(area_ratio, 4),
                    "bbox": [
                        round(rect.x0, 2),
                        round(rect.y0, 2),
                        round(rect.x1, 2),
                        round(rect.y1, 2),
                    ],
                })

    document.close()

    return {
        "image_count": len(images),
        "images": images,
    }