"""
Tests for the Evaluator module.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import unittest
from core.evaluator import evaluate


class TestEvaluator(unittest.TestCase):
    """Tests for core/evaluator.py"""

    def test_evaluate_good_answer(self):
        """A strong answer should score high on both similarity and keywords."""
        result = evaluate(
            "ds_t1",
            "The bias-variance tradeoff is fundamental in machine learning. "
            "Bias means the model is too simple causing underfitting, while "
            "high variance means overfitting to training data. Regularization "
            "and cross-validation help find the right complexity for better generalization."
        )
        self.assertIn("similarity_score", result)
        self.assertIn("keyword_coverage", result)
        self.assertGreater(result["similarity_score"], 0.1)
        self.assertGreater(result["keyword_coverage"], 0.3)
        self.assertIsInstance(result["matched_keywords"], list)

    def test_evaluate_poor_answer(self):
        """An irrelevant answer should score low."""
        result = evaluate(
            "ds_t1",
            "I like pizza and going to the beach on weekends."
        )
        self.assertLess(result["similarity_score"], 0.3)
        self.assertLess(result["keyword_coverage"], 0.2)

    def test_evaluate_empty_answer(self):
        """Empty answer should return zeros."""
        result = evaluate("ds_t1", "")
        self.assertEqual(result["similarity_score"], 0.0)

    def test_evaluate_unknown_question(self):
        """Unknown question ID should still return a result with zero scores."""
        result = evaluate("nonexistent_q99", "Some answer text here.")
        self.assertEqual(result["similarity_score"], 0.0)
        self.assertEqual(result["keyword_coverage"], 0.0)


if __name__ == "__main__":
    unittest.main()
