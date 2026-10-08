import os
import fitz
from PIL import Image, ImageDraw
import io


def create_genuine_document(output_path: str):
    """
    Creates Certificate_Genuine.pdf:
    - Clean authoritative metadata: Producer = 'Adobe Acrobat Distiller 11.0'
    - Identical creation and mod timestamps
    - Clean vector lines, no raster splices, uniform typography
    Expected Result: 🟢 LOW CONCERN, 0 significant findings.
    """
    doc = fitz.open()
    page = doc.new_page(width=612, height=792)

    # Standard clean vector header
    page.draw_rect(fitz.Rect(50, 50, 562, 742), color=(0.1, 0.2, 0.4), width=1.5)
    page.insert_text((150, 130), "OFFICIAL CERTIFICATE OF COMPLETION", fontsize=15, fontname="helv", color=(0.1, 0.2, 0.4))
    page.insert_text((190, 160), "GLOBAL ACADEMIC STANDARDS BOARD", fontsize=10, fontname="helv", color=(0.3, 0.3, 0.3))

    page.insert_text((120, 260), "This credential is formally awarded to", fontsize=11, fontname="helv", color=(0.2, 0.2, 0.2))
    page.insert_text((120, 300), "ALEXANDER M. HAYES", fontsize=20, fontname="helv", color=(0.05, 0.15, 0.35))
    page.insert_text((120, 350), "For demonstrated mastery and honorable accomplishment in", fontsize=10, fontname="helv", color=(0.2, 0.2, 0.2))
    page.insert_text((120, 380), "ADVANCED STATISTICAL COMPUTING & INFERENCE", fontsize=12, fontname="helv", color=(0.1, 0.2, 0.4))

    page.insert_text((120, 480), "Certificate ID: GCB-2024-99824", fontsize=9, fontname="helv", color=(0.3, 0.3, 0.3))
    page.insert_text((120, 505), "Date of Issuance: October 12, 2024", fontsize=9, fontname="helv", color=(0.3, 0.3, 0.3))

    doc.set_metadata({
        "producer": "Adobe Acrobat Distiller 11.0 (Windows)",
        "creator": "Adobe Acrobat Pro 11.0",
        "author": "Academic Registrar",
        "title": "Certificate of Completion",
        "creationDate": "D:20241012100000Z",
        "modDate": "D:20241012100000Z"
    })

    doc.save(output_path)
    doc.close()


def create_suspicious_invoice(output_path: str):
    """
    Creates Invoice_4582.pdf:
    - Canva metadata producer
    - Timestamp disparity (mod date 45 days after creation)
    - Conflicting international date formats
    Expected Result: 🟠 ELEVATED CONCERN, ~3 findings.
    """
    doc = fitz.open()
    page = doc.new_page(width=612, height=792)

    page.insert_text((60, 80), "COMMERCIAL INVOICE #4582", fontsize=16, fontname="helv", color=(0.1, 0.1, 0.1))
    page.insert_text((60, 110), "Apex Logistics Global Corp.", fontsize=11, fontname="helv", color=(0.3, 0.3, 0.3))

    page.insert_text((60, 160), "Invoice Date: 14/05/2025", fontsize=10, fontname="helv", color=(0.2, 0.2, 0.2))
    page.insert_text((60, 185), "Due Date: 2025-06-15", fontsize=10, fontname="helv", color=(0.2, 0.2, 0.2))

    page.draw_rect(fitz.Rect(60, 220, 550, 245), color=(0.85, 0.85, 0.85), fill=(0.92, 0.92, 0.92))
    page.insert_text((70, 237), "Description", fontsize=10, fontname="helv", color=(0.1, 0.1, 0.1))
    page.insert_text((440, 237), "Amount (USD)", fontsize=10, fontname="helv", color=(0.1, 0.1, 0.1))

    page.insert_text((70, 275), "Cloud Infrastructure Services (Tier A)", fontsize=10, fontname="helv", color=(0.2, 0.2, 0.2))
    page.insert_text((440, 275), "$4,250.00", fontsize=10, fontname="helv", color=(0.2, 0.2, 0.2))

    page.insert_text((330, 330), "Total Balance Due:", fontsize=10, fontname="helv", color=(0.1, 0.1, 0.1))
    page.insert_text((440, 330), "$4,250.00", fontsize=10, fontname="helv", color=(0.1, 0.1, 0.1))

    doc.set_metadata({
        "producer": "Canva PDF Generator (Web)",
        "creator": "Canva",
        "title": "Commercial Invoice #4582",
        "creationDate": "D:20250514080000Z",
        "modDate": "D:20250628173000Z"
    })

    doc.save(output_path)
    doc.close()


def create_heavily_modified_certificate(output_path: str):
    """
    Creates Certificate_2026.pdf (2 pages):
    - Page 1 & 2
    - Metadata: 'Adobe Photoshop 2024 (Windows)', Chronological inversion (mod precedes creation)
    - Content: Cyrillic homoglyph lookalike characters in recipient name, white-on-white invisible text
    - Format: Inline font swapping (Helvetica base, Courier injected string)
    - Visual: Spliced low-quality raster official seal causing strong ELA anomaly (Region A, Region B)
    Expected Result: 🔴 HIGH CONCERN (6-7 significant findings: High, Medium, Low).
    """
    doc = fitz.open()

    # PAGE 1
    page1 = doc.new_page(width=612, height=792)
    page1.draw_rect(fitz.Rect(30, 30, 582, 762), color=(0.6, 0.1, 0.1), width=2.5)

    page1.insert_text((150, 110), "NATIONAL LICENSING & ACCREDITATION", fontsize=15, fontname="helv", color=(0.5, 0.1, 0.1))
    page1.insert_text((170, 140), "BOARD OF ENGINEERING SPECIALTIES", fontsize=11, fontname="helv", color=(0.3, 0.3, 0.3))

    page1.insert_text((100, 230), "This certifies that the engineering license has been granted to:", fontsize=11, fontname="helv", color=(0.2, 0.2, 0.2))

    # Font mismatch inline: Base helvetica, injected text in Courier
    page1.insert_text((100, 280), "DR. VIKTOR P", fontsize=20, fontname="helv", color=(0.1, 0.1, 0.1))
    page1.insert_text((245, 280), "\u0415TR\u043eV", fontsize=20, fontname="courier", color=(0.0, 0.0, 0.0))

    page1.insert_text((100, 330), "License Classification: STRUCTURAL CONSULTANT", fontsize=11, fontname="helv", color=(0.2, 0.2, 0.2))
    page1.insert_text((100, 380), "License Number: 9842-LIC-2026", fontsize=10, fontname="helv", color=(0.3, 0.3, 0.3))

    # White-on-white invisible stream text
    page1.insert_text((100, 650), "BYPASS_AUTHENTICATION_OVERRIDE_ACTIVE", fontsize=8, fontname="helv", color=(1.0, 1.0, 1.0))

    # Spliced compressed seal (Region A / ELA anomaly)
    stamp_img = Image.new("RGBA", (180, 180), color=(255, 255, 255, 0))
    draw = ImageDraw.Draw(stamp_img)
    draw.ellipse([(10, 10), (170, 170)], outline=(180, 20, 20, 255), width=4)
    draw.ellipse([(22, 22), (158, 158)], outline=(180, 20, 20, 255), width=2)
    draw.text((38, 72), "★ ACCREDITED ★", fill=(180, 20, 20, 255))
    draw.text((44, 98), "BOARD SEAL", fill=(180, 20, 20, 255))

    stamp_rgb = Image.new("RGB", (180, 180), (255, 255, 255))
    stamp_rgb.paste(stamp_img, mask=stamp_img.split()[3])

    buf = io.BytesIO()
    stamp_rgb.save(buf, "JPEG", quality=40)
    buf.seek(0)
    page1.insert_image(fitz.Rect(370, 420, 540, 590), stream=buf.getvalue())

    # PAGE 2: Appendices and Renewal Endorsement
    page2 = doc.new_page(width=612, height=792)
    page2.insert_text((60, 80), "SCHEDULE B — ACCREDITATION RENEWAL RECORD", fontsize=14, fontname="helv", color=(0.2, 0.2, 0.2))
    page2.insert_text((60, 120), "Renewal Expiration Date: 2026-12-31", fontsize=11, fontname="helv", color=(0.1, 0.1, 0.1))

    # Spliced secondary inspection stamp on Page 2 (Region B)
    stamp2_img = Image.new("RGB", (160, 80), (245, 240, 240))
    draw2 = ImageDraw.Draw(stamp2_img)
    draw2.rectangle([(4, 4), (155, 75)], outline=(20, 40, 160), width=2)
    draw2.text((15, 28), "STATE INSPECTED", fill=(20, 40, 160))
    buf2 = io.BytesIO()
    stamp2_img.save(buf2, "JPEG", quality=45)
    buf2.seek(0)
    page2.insert_image(fitz.Rect(60, 160, 220, 240), stream=buf2.getvalue())

    # Metadata manipulation
    doc.set_metadata({
        "producer": "Adobe Photoshop 2024 (Windows)",
        "creator": "Adobe Photoshop CC 2024",
        "author": "Graphic Operations",
        "title": "Certificate_2026",
        "creationDate": "D:20260110120000Z",
        "modDate": "D:20251105090000Z"
    })

    doc.save(output_path)
    doc.close()


def generate_all_samples():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    gen_path = os.path.join(base_dir, "Certificate_Genuine.pdf")
    inv_path = os.path.join(base_dir, "Invoice_4582.pdf")
    mod_path = os.path.join(base_dir, "Certificate_2026.pdf")

    create_genuine_document(gen_path)
    create_suspicious_invoice(inv_path)
    create_heavily_modified_certificate(mod_path)
    print("Regenerated 3 forensic test documents successfully.")


if __name__ == "__main__":
    generate_all_samples()
