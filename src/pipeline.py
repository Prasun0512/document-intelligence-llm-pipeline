from __future__ import annotations

import re
from dataclasses import dataclass, field


EMAIL_RE = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
PHONE_RE = re.compile(r"(?<!\d)(?:\+?\d[\d\s().-]{7,}\d)(?!\d)")
AMOUNT_RE = re.compile(r"(?:rs\.?|inr|\$)\s?([0-9][0-9,]*(?:\.[0-9]{2})?)", re.I)
REFERENCE_RE = re.compile(
    r"\b(?:claim|case|invoice|policy)[ -]?(?:id|no|number)[:# ]+([A-Z0-9-]{4,})\b",
    re.I,
)


@dataclass(frozen=True)
class ExtractedRecord:
    case_type: str
    requester: str
    summary: str
    confidence: float
    route_to_review: bool
    fields: dict[str, str] = field(default_factory=dict)
    validation_errors: list[str] = field(default_factory=list)
    audit: list[str] = field(default_factory=list)


def redact(text: str) -> str:
    text = EMAIL_RE.sub("[EMAIL]", text)
    return PHONE_RE.sub("[PHONE]", text)


def normalize_ocr_text(text: str) -> str:
    replacements = {
        "\u2018": "'",
        "\u2019": "'",
        "\u201c": '"',
        "\u201d": '"',
        "|": " ",
    }
    for source, target in replacements.items():
        text = text.replace(source, target)
    return " ".join(text.split())


def detect_case_type(text: str) -> str:
    lowered = text.lower()
    if any(term in lowered for term in ("claim", "reimbursement", "policy")):
        return "claim"
    if any(term in lowered for term in ("invoice", "payment", "purchase order")):
        return "invoice"
    return "general"


def extract_fields(text: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    email_match = EMAIL_RE.search(text)
    amount_match = AMOUNT_RE.search(text)
    reference_match = REFERENCE_RE.search(text)
    if email_match:
        fields["requester_email"] = email_match.group(0)
    if amount_match:
        fields["amount"] = amount_match.group(1).replace(",", "")
    if reference_match:
        fields["reference_id"] = reference_match.group(1).upper()
    return fields


def validate_record(case_type: str, fields: dict[str, str]) -> list[str]:
    errors: list[str] = []
    if case_type == "general":
        errors.append("case_type_unclear")
    if "requester_email" not in fields:
        errors.append("requester_missing")
    if case_type in {"claim", "invoice"} and "reference_id" not in fields:
        errors.append("reference_id_missing")
    return errors


def score_confidence(case_type: str, fields: dict[str, str], errors: list[str]) -> float:
    score = 0.42
    if case_type != "general":
        score += 0.2
    if "requester_email" in fields:
        score += 0.16
    if "reference_id" in fields:
        score += 0.14
    if "amount" in fields:
        score += 0.06
    score -= 0.08 * len(errors)
    return round(max(0.1, min(score, 0.96)), 2)


def extract_record(text: str, threshold: float = 0.75) -> ExtractedRecord:
    normalized = normalize_ocr_text(text)
    fields = extract_fields(normalized)
    case_type = detect_case_type(normalized)
    errors = validate_record(case_type, fields)
    confidence = score_confidence(case_type, fields, errors)
    redacted_summary = redact(normalized)[:180]
    audit = [
        "ocr:normalized",
        "pii:redacted",
        f"case_type:{case_type}",
        f"confidence:{confidence}",
    ]
    if confidence < threshold or errors:
        audit.append("route:human_review")
    else:
        audit.append("route:straight_through_processing")
    return ExtractedRecord(
        case_type=case_type,
        requester=fields.get("requester_email", "unknown"),
        summary=redacted_summary,
        confidence=confidence,
        route_to_review=confidence < threshold or bool(errors),
        fields=fields,
        validation_errors=errors,
        audit=audit,
    )
