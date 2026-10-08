def check_field_consistency(fields: dict) -> list:
    """
    Check extracted document fields for conflicting values.
    """

    findings = []

    for field_name, values in fields.items():
        if not values:
            continue

        # Remove duplicates while preserving order
        unique_values = list(dict.fromkeys(values))

        if len(unique_values) > 1:
            findings.append({
                "type": f"{field_name}_inconsistency",
                "severity": "high",
                "field": field_name,
                "values": unique_values,
                "evidence": (
                    f"Multiple different {field_name.replace('_', ' ')} "
                    f"values were detected: {', '.join(unique_values)}."
                )
            })

    return findings


def check_required_fields(fields: dict) -> list:
    """
    Identify important fields that could not be extracted.
    """

    findings = []

    required_fields = [
        "name",
        "certificate_id",
        "issuer",
        "date"
    ]

    for field_name in required_fields:
        if not fields.get(field_name):
            findings.append({
                "type": "missing_field",
                "severity": "medium",
                "field": field_name,
                "values": [],
                "evidence": (
                    f"No {field_name.replace('_', ' ')} "
                    "could be extracted from the document."
                )
            })

    return findings


def analyze_consistency(fields: dict) -> dict:
    """
    Run all content consistency checks and return structured findings.
    """

    findings = []

    findings.extend(check_field_consistency(fields))
    findings.extend(check_required_fields(fields))

    high_count = sum(
        1 for finding in findings
        if finding["severity"] == "high"
    )

    medium_count = sum(
        1 for finding in findings
        if finding["severity"] == "medium"
    )

    return {
        "consistent": high_count == 0,
        "findings": findings,
        "summary": {
            "total_findings": len(findings),
            "high": high_count,
            "medium": medium_count
        }
    }