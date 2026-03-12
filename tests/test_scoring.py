"""
Tests for the Scoring module.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import unittest
from core.scoring import calculate_score


class TestScoring(unittest.TestCase):
    """Tests for core/scoring.py"""

    def test_perfect_score(self):
        """Both scores at 1.0 should yield 100."""
        result = calculate_score(1.0, 1.0)
        self.assertEqual(result["total_score"], 100.0)
        self.assertEqual(result["grade"], "A+")

    def test_zero_score(self):
        """Both scores at 0.0 should yield 0."""
        result = calculate_score(0.0, 0.0)
        self.assertEqual(result["total_score"], 0.0)
        self.assertEqual(result["grade"], "F")

    def test_mixed_scores(self):
        """Check weighted calculation: 0.7 sim + 0.5 kw = 0.7*60 + 0.5*40 = 62."""
        result = calculate_score(0.7, 0.5)
        self.assertAlmostEqual(result["total_score"], 62.0, places=1)
        self.assertIn(result["grade"], ["B", "B+"])

    def test_custom_weights(self):
        """Custom weights should override defaults."""
        result = calculate_score(0.8, 0.2, weights={"similarity": 0.3, "keyword": 0.7})
        # 80*0.3 + 20*0.7 = 24 + 14 = 38
        self.assertAlmostEqual(result["total_score"], 38.0, places=1)

    def test_result_has_breakdown(self):
        """Result should include score breakdown."""
        result = calculate_score(0.5, 0.5)
        self.assertIn("breakdown", result)
        self.assertIn("similarity_score", result["breakdown"])
        self.assertIn("keyword_score", result["breakdown"])


if __name__ == "__main__":
    unittest.main()
