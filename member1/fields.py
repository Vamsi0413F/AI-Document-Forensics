import re


def clean_value(value: str) -> str:
    """Clean extracted text before storing it."""

    value = re.sub(r"\s+", " ", value)
    return value.strip(" :,-")


def extract_all_matches(pattern: str, text: str) -> list:
    """Return all matching values for a regex pattern."""

    matches = re.findall(pattern, text, flags=re.IGNORECASE)

    if isinstance(matches, list):
        return [clean_value(match) for match in matches if clean_value(match)]

    return []


def extract_fields(text: str) -> dict:
    """
    Extract important document fields from OCR/PDF text.

    The function keeps all detected occurrences so that the
    consistency engine can later detect contradictions.
    """

    fields = {
        "name": [],
        "certificate_id": [],
        "issuer": [],
        "course": [],
        "date": []
    }

    # ---------------------------------------------------------
    # NAME
    # Examples:
    # Name: Harish Kumar
    # Name - Harish Kumar
    # Full Name: Harish Kumar
    # ---------------------------------------------------------

    name_pattern = (
        r"(?:full\s+name|name)"
        r"\s*[:\-]\s*"
        r"([A-Za-z][A-Za-z .'-]{1,80})"
    )

    fields["name"] = extract_all_matches(name_pattern, text)

    # ---------------------------------------------------------
    # CERTIFICATE ID
    # Examples:
    # Certificate ID: CERT-48291
    # Certificate No: CERT-48291
    # Certificate Number: CERT-48291
    # ---------------------------------------------------------

    certificate_id_pattern = (
        r"(?:certificate\s*(?:id|no|number))"
        r"\s*[:\-]\s*"
        r"([A-Za-z0-9][A-Za-z0-9_\/\-]{2,50})"
    )

    fields["certificate_id"] = extract_all_matches(
        certificate_id_pattern,
        text
    )

    # ---------------------------------------------------------
    # ISSUER
    # Examples:
    # Issuer: ABC University
    # Issued By: ABC University
    # Institution: ABC University
    # University: ABC University
    # ---------------------------------------------------------

    issuer_pattern = (
        r"(?:issuer|issued\s+by|institution|university|organization)"
        r"\s*[:\-]\s*"
        r"([A-Za-z0-9][A-Za-z0-9 .,&'()-]{2,100})"
    )

    fields["issuer"] = extract_all_matches(
        issuer_pattern,
        text
    )

    # ---------------------------------------------------------
    # COURSE
    # Examples:
    # Course: Python Programming
    # Program: B.Tech Computer Science
    # Degree: B.Tech CSE
    # ---------------------------------------------------------

    course_pattern = (
        r"(?:course|program|degree)"
        r"\s*[:\-]\s*"
        r"([A-Za-z0-9][A-Za-z0-9 .,&'()\/\-]{2,100})"
    )

    fields["course"] = extract_all_matches(
        course_pattern,
        text
    )

    # ---------------------------------------------------------
    # DATE
    # Supports:
    # 15/09/2026
    # 15-09-2026
    # 15.09.2026
    # 2026-09-15
    # ---------------------------------------------------------

    date_pattern = (
        r"\b("
        r"\d{1,2}[\/\-.]\d{1,2}[\/\-.]\d{2,4}"
        r"|"
        r"\d{4}[\/\-.]\d{1,2}[\/\-.]\d{1,2}"
        r")\b"
    )

    fields["date"] = extract_all_matches(
        date_pattern,
        text
    )

    return fields


def get_primary_fields(fields: dict) -> dict:
    """
    Return the first detected value for each field.

    This is useful for displaying the main extracted value,
    while the original lists remain available for consistency checks.
    """

    primary = {}

    for field, values in fields.items():
        if values:
            primary[field] = values[0]
        else:
            primary[field] = None

    return primary