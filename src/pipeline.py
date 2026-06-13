from __future__ import annotations

import re
from dataclasses import dataclass


EMAIL_RE = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
PHONE_RE = re.compile(r"(?<!\d)(?:\+?\d[\d\s().-]{7,}\d)(?!\d)")


@dataclass(frozen=True)
class ExtractedRecord:
    case_type: str
    requester: str
    summary: str
    confidence: float
    route_to_review: bool


def redact(text: str) -> str:
    text = EMAIL_RE.sub("[EMAIL]", text)
    return PHONE_RE.sub("[PHONE]", text)


def normalize_ocr_text(text: str) -> str:
    return " ".join(text.split())


def extract_record(text: str, threshold: float = 0.75) -> ExtractedRecord:
    clean = normalize_ocr_text(redact(text))
    case_type = "claim" if "claim" in clean.lower() else "general"
    requester = "[EMAIL]" if "[EMAIL]" in clean else "unknown"
    confidence = 0.86 if case_type == "claim" and requester != "unknown" else 0.62
    return ExtractedRecord(
        case_type=case_type,
        requester=requester,
        summary=clean[:140],
        confidence=confidence,
        route_to_review=confidence < threshold,
    )
