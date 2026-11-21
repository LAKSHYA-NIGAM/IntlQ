import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from nlp.feedback_rubric_compiler import compile_candidate_rubric


class TestFeedbackRubricCompiler(unittest.TestCase):
    def test_strong_hire_decision(self):
        scores = {
            'technical_depth': 4.5,
            'problem_solving': 4.5,
            'communication': 4.0,
            'culture_add': 4.5,
        }
        res = compile_candidate_rubric(scores)
        self.assertEqual(res['recommendation'], 'STRONG_HIRE')
        self.assertTrue(res['is_hire'])
        self.assertGreaterEqual(res['overall_score'], 4.2)

    def test_no_hire_decision(self):
        scores = {
            'technical_depth': 2.0,
            'problem_solving': 2.0,
            'communication': 2.5,
            'culture_add': 3.0,
        }
        res = compile_candidate_rubric(scores)
        self.assertEqual(res['recommendation'], 'STRONG_NO_HIRE')
        self.assertFalse(res['is_hire'])


if __name__ == '__main__':
    unittest.main()
