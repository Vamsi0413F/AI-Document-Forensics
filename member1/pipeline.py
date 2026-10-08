from pathlib import Path

from .ingestion import validate_document
from .extraction import extract_text
from .fields import extract_fields, get_primary_fields
from .consistency import analyze_consistency


def process_document(file_path: str) -> dict:
    """
    Run the complete Member 1 document-processing pipeline.

    Flow:
        ingestion
        -> text/OCR extraction
        -> field extraction
        -> consistency analysis
    """

    path = Path(file_path)

    # ---------------------------------------------------------
    # STEP 1: DOCUMENT INGESTION
    # ---------------------------------------------------------

    ingestion_result = validate_document(file_path)

    if not ingestion_result["valid"]:
        return {
            "success": False,
            "stage": "ingestion",
            "document": ingestion_result,
            "extraction": None,
            "fields": None,
            "consistency": None,
            "error": ingestion_result["error"]
        }

    # ---------------------------------------------------------
    # STEP 2: TEXT / OCR EXTRACTION
    # ---------------------------------------------------------

    extraction_result = extract_text(file_path)

    if not extraction_result["success"]:
        return {
            "success": False,
            "stage": "extraction",
            "document": ingestion_result,
            "extraction": extraction_result,
            "fields": None,
            "consistency": None,
            "error": extraction_result["error"]
        }

    # ---------------------------------------------------------
    # STEP 3: FIELD EXTRACTION
    # ---------------------------------------------------------

    extracted_text = extraction_result["text"]

    fields = extract_fields(extracted_text)

    primary_fields = get_primary_fields(fields)

    # ---------------------------------------------------------
    # STEP 4: CONTENT CONSISTENCY ANALYSIS
    # ---------------------------------------------------------

    consistency_result = analyze_consistency(fields)

    # ---------------------------------------------------------
    # FINAL RESULT
    # ---------------------------------------------------------

    return {
        "success": True,
        "stage": "complete",

        "document": {
            "filename": path.name,
            "file_type": ingestion_result["file_type"]
        },

        "extraction": {
            "method": extraction_result["method"],
            "page_count": extraction_result["page_count"],
            "text": extraction_result["text"],
            "pages": extraction_result["pages"]
        },

        "fields": {
            "all_detected": fields,
            "primary": primary_fields
        },

        "consistency": consistency_result
    }