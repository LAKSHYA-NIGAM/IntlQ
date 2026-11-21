"""
IntlQ - NLP Text Processing and Similarity Edge Case Tests
---------------------------------------------------------
Validates text cleaning defenses, empty inputs, null safety,
and cosine similarity robustness.
"""
import os
import sys
import unittest

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
if PROJECT_DIR not in sys.path:
    sys.path.insert(0, PROJECT_DIR)

from nlp.text_cleaner import clean_text, preprocess, tokenize
from nlp.similarity import tfidf_similarity
from nlp.keyword_matcher import match_keywords


class TestNLPEdgeCases(unittest.TestCase):
    def test_01_clean_text_null_and_empty(self):
        """clean_text should safely handle None, empty, and non-string inputs."""
        self.assertEqual(clean_text(None), "")
        self.assertEqual(clean_text(""), "")
        self.assertEqual(clean_text(12345), "")

    def test_02_clean_text_strips_html_and_preserves_slashes(self):
        """clean_text strips HTML tags and retains technical terms like CI/CD."""
        result = clean_text("<p>Experience with <b>CI/CD</b> and Docker!</p>")
        self.assertIn("ci/cd", result)
        self.assertNotIn("<p>", result)
        self.assertNotIn("<b>", result)

    def test_03_preprocess_null_and_empty(self):
        """preprocess should return empty string for null or whitespace text."""
        self.assertEqual(preprocess(None), "")
        self.assertEqual(preprocess("   "), "")

    def test_04_tokenize_null_and_empty(self):
        """tokenize should return empty list for null or whitespace text."""
        self.assertEqual(tokenize(None), [])
        self.assertEqual(tokenize("   "), [])

    def test_05_similarity_empty_inputs(self):
        """tfidf_similarity should safely return 0.0 when either answer is empty or null."""
        self.assertEqual(tfidf_similarity("", "ideal answer"), 0.0)
        self.assertEqual(tfidf_similarity("my answer", ""), 0.0)
        self.assertEqual(tfidf_similarity(None, "ideal answer"), 0.0)
        self.assertEqual(tfidf_similarity("my answer", None), 0.0)

    def test_06_similarity_identical_texts(self):
        """tfidf_similarity of identical text should approach 1.0."""
        text = "RESTful APIs use HTTP methods like GET POST PUT and DELETE for CRUD operations"
        sim = tfidf_similarity(text, text)
        self.assertAlmostEqual(sim, 1.0, places=2)

    def test_07_keyword_matcher_null_safe(self):
        """match_keywords should return empty match for empty inputs."""
        result = match_keywords("", ["python", "django"])
        self.assertEqual(len(result["matched"]), 0)
        self.assertEqual(len(result["missing"]), 2)
        self.assertEqual(result["coverage_score"], 0.0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
