# Evaluation Strategy

Document intelligence systems should be evaluated at every stage because OCR, redaction, extraction, validation, and review routing can fail independently.

## What To Evaluate

- OCR normalization quality on sanitized samples.
- PII/PHI redaction coverage.
- Required-field extraction accuracy.
- Schema validation errors.
- Confidence scoring behavior.
- Human-review routing for incomplete or ambiguous documents.

## Local Checks

```bash
python -m unittest discover -s tests
python -m src.demo
```

## Quality Gates

- No unredacted sensitive values should appear in logs or sample outputs.
- Missing required fields must fail validation.
- Low-confidence documents must route to review.
- Deterministic extraction should pass before adding an LLM provider.

## Future Improvements

- Add field-level precision/recall reports.
- Add layout-specific OCR fixtures.
- Add Azure Document Intelligence adapter contract tests.
