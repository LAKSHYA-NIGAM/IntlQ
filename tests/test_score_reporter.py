import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from core.score_reporter import InterviewScoreReporter


class TestInterviewScoreReporter(unittest.TestCase):
    def test_strong_hire_recommendation(self):
        evals = [
            {"question_id": "q1", "topic": "System Design", "score": 90.0},
            {"question_id": "q2", "topic": "System Design", "score": 85.0},
            {"question_id": "q3", "topic": "DSA", "score": 90.0}
        ]
        res = InterviewScoreReporter.evaluate_interview_session("Alice Chen", "Senior Engineer", evals)
        self.assertEqual(res["recommendation"], "STRONG_HIRE")
        self.assertAlmostEqual(res["overall_score"], 88.3, places=1)
        self.assertIn("System Design", res["strengths"])
        self.assertIn("DSA", res["strengths"])
        self.assertEqual(len(res["areas_for_growth"]), 0)

    def test_no_hire_recommendation_with_weak_topics(self):
        evals = [
            {"question_id": "q1", "topic": "Concurrency", "score": 40.0},
            {"question_id": "q2", "topic": "Databases", "score": 45.0}
        ]
        res = InterviewScoreReporter.evaluate_interview_session("Bob", "Backend Dev", evals)
        self.assertEqual(res["recommendation"], "NO_HIRE")
        self.assertAlmostEqual(res["overall_score"], 42.5)
        self.assertIn("Concurrency", res["areas_for_growth"])
        self.assertIn("Databases", res["areas_for_growth"])

    def test_empty_evaluations_safe_handling(self):
        res = InterviewScoreReporter.evaluate_interview_session("Charlie", "Intern", [])
        self.assertEqual(res["recommendation"], "NO_EVALUATIONS_RECORDED")
        self.assertEqual(res["overall_score"], 0.0)


if __name__ == "__main__":
    unittest.main()
