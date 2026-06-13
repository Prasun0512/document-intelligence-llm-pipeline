import unittest

from src.pipeline import extract_record, redact


class PipelineTests(unittest.TestCase):
    def test_redaction_masks_sensitive_values(self) -> None:
        text = redact("Email user@example.com and call +91 8793147065")
        self.assertIn("[EMAIL]", text)
        self.assertIn("[PHONE]", text)

    def test_claim_routes_without_review_when_confident(self) -> None:
        record = extract_record("Claim request from user@example.com")
        self.assertEqual(record.case_type, "claim")
        self.assertFalse(record.route_to_review)


if __name__ == "__main__":
    unittest.main()
