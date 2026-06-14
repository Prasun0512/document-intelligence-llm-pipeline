# Security and Governance

## Data Protection

- Redact PII/PHI before LLM calls, indexing, logs, and examples.
- Store raw documents separately from sanitized text and derived outputs.
- Use short retention for temporary artifacts.
- Encrypt storage and use managed identity in production.

## Governance Controls

- Version extraction schemas and prompts.
- Capture model/provider, prompt version, schema version, confidence score, and validation errors.
- Route missing or low-confidence fields to human review.
- Keep all examples synthetic and sanitized.

## Operational Risks

- OCR errors can produce incorrect extraction; validation must catch impossible values.
- LLM output must be schema-validated before workflow updates.
- Review queues need SLA and escalation policy in real deployments.
- Audit logs should avoid storing unredacted document content.
