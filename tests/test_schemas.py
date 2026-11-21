"""
Unit tests for API request schemas validation (Pydantic models).
"""

import unittest
from pydantic import ValidationError
from api.schemas import StartInterviewRequest, SubmitAnswerRequest


class TestAPISchemas(unittest.TestCase):
    def test_start_interview_valid(self):
        req = StartInterviewRequest(candidate_name="Alice", role_id="software-engineer", question_count=5)
        self.assertEqual(req.candidate_name, "Alice")
        self.assertEqual(req.role_id, "software-engineer")
        self.assertEqual(req.question_count, 5)

    def test_start_interview_empty_candidate_name_defaults(self):
        req = StartInterviewRequest(candidate_name="   ", role_id="software-engineer")
        self.assertEqual(req.candidate_name, "Anonymous")

    def test_start_interview_blank_role_id_raises(self):
        with self.assertRaises(ValidationError):
            StartInterviewRequest(role_id="   ")

    def test_start_interview_invalid_question_count_raises(self):
        with self.assertRaises(ValidationError):
            StartInterviewRequest(role_id="backend", question_count=0)
        with self.assertRaises(ValidationError):
            StartInterviewRequest(role_id="backend", question_count=25)

    def test_submit_answer_valid(self):
        req = SubmitAnswerRequest(session_id=1, question_id="q1", answer_text="Docker uses cgroups and namespaces.")
        self.assertEqual(req.session_id, 1)
        self.assertEqual(req.question_id, "q1")
        self.assertEqual(req.answer_text, "Docker uses cgroups and namespaces.")

    def test_submit_answer_blank_question_id_raises(self):
        with self.assertRaises(ValidationError):
            SubmitAnswerRequest(session_id=1, question_id="   ", answer_text="answer")

    def test_submit_answer_blank_answer_text_raises(self):
        with self.assertRaises(ValidationError):
            SubmitAnswerRequest(session_id=1, question_id="q1", answer_text="   ")


if __name__ == "__main__":
    unittest.main()
