import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from nlp.star_method_evaluator import evaluate_star_completeness


class TestStarEvaluator(unittest.TestCase):
    def test_complete_star_response(self):
        text = (
            "At my previous company, our team was handling high latency API queries. "
            "My goal was to reduce p99 response times below 200ms. "
            "I designed and implemented a Redis caching layer and optimized SQL indexing. "
            "As a result, we reduced query latency by 65% and successfully delivered the feature."
        )

        res = evaluate_star_completeness(text)
        self.assertEqual(res['completeness_score'], 1.0)
        self.assertEqual(len(res['pillars_present']), 4)
        self.assertTrue(res['is_well_structured'])
        self.assertEqual(len(res['missing_pillars']), 0)

    def test_partial_star_response(self):
        # Action only
        text = "I developed a new feature using React and Node.js."
        res = evaluate_star_completeness(text)
        self.assertEqual(res['completeness_score'], 0.25)
        self.assertIn('action', res['pillars_present'])
        self.assertIn('result', res['missing_pillars'])


if __name__ == '__main__':
    unittest.main()
