import unittest

from src.pipeline import extract_record, redact


class PipelineTests(unittest.TestCase):
    def test_redaction_masks_sensitive_values(self) -> None:
        text = redact("Email user@example.com and call +91 8793147065")
        self.assertIn("[EMAIL]", text)
        self.assertIn("[PHONE]", text)

    def test_claim_routes_without_review_when_confident(self) -> None:
        record = extract_record("Claim number CLM-7788 request from user@example.com for INR 12000")
        self.assertEqual(record.case_type, "claim")
        self.assertFalse(record.route_to_review)
        self.assertEqual(record.fields["reference_id"], "CLM-7788")
        self.assertEqual(record.fields["amount"], "12000")

    def test_unclear_document_routes_to_review(self) -> None:
        record = extract_record("Hello team, please check this attachment.")
        self.assertTrue(record.route_to_review)
        self.assertIn("case_type_unclear", record.validation_errors)


if __name__ == "__main__":
    unittest.main()
