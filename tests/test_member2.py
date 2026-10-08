import unittest
from pathlib import Path

from member2.fingerprint import generate_sha256
from member2.metadata import extract_metadata
from member2.formatting import analyze_formatting
from member2.visual import analyze_visual_elements


class TestMember2Forensics(unittest.TestCase):

    AUTHENTIC_PDF = Path("authentic.pdf")
    MODIFIED_PDF = Path("modified.pdf")
    IMAGE_PDF = Path("image_sample.pdf")

    def test_fingerprint(self):
        """Different documents should produce different fingerprints."""

        authentic_hash = generate_sha256(self.AUTHENTIC_PDF)
        modified_hash = generate_sha256(self.MODIFIED_PDF)

        self.assertEqual(len(authentic_hash), 64)
        self.assertEqual(len(modified_hash), 64)
        self.assertNotEqual(authentic_hash, modified_hash)

    def test_metadata(self):
        """Metadata extraction should return document information."""

        result = extract_metadata(self.AUTHENTIC_PDF)

        self.assertIn("page_count", result)
        self.assertIn("has_metadata", result)
        self.assertEqual(result["page_count"], 1)

    def test_formatting(self):
        """Formatting analysis should detect unusual formatting."""

        result = analyze_formatting(self.MODIFIED_PDF)

        self.assertIn("fonts", result)
        self.assertIn("font_sizes", result)
        self.assertIn("text_blocks", result)
        self.assertIn("anomalies", result)

        self.assertGreater(len(result["anomalies"]), 0)

    def test_visual_elements(self):
        """Visual analysis should detect embedded images."""

        result = analyze_visual_elements(self.IMAGE_PDF)

        self.assertIn("image_count", result)
        self.assertIn("images", result)

        self.assertGreater(result["image_count"], 0)


if __name__ == "__main__":
    unittest.main()