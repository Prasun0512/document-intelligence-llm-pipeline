# Security and Privacy

This document complements `docs/security-and-governance.md`.

## Privacy Boundaries

- Use synthetic OCR text and sanitized examples only.
- Redact PII/PHI before LLM calls, logs, indexing, or downstream workflow updates.
- Do not commit real PDFs, scans, claim forms, medical records, credentials, or private endpoints.

## Production Controls

- Store raw files separately from sanitized derived text.
- Apply role-based access to raw artifacts.
- Use managed identity and a secret manager for cloud deployments.
- Keep audit logs useful without storing raw sensitive content.

## Review Policy

Low-confidence or policy-sensitive documents should route to human review before business-system updates.
