"""
Tests for the API endpoints.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Set in-memory DB *before* importing/creating the app
os.environ["DATABASE_URL"] = "sqlite:///:memory:"

import unittest
import json
from app import create_app


class TestAPI(unittest.TestCase):
    """Integration tests for Flask API endpoints."""

    def setUp(self):
        self.app = create_app()
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()

        with self.app.app_context():
            from database.db import db
            db.drop_all()
            db.create_all()

    def _login(self):
        """Create a test user and log in via the signup endpoint."""
        with self.app.app_context():
            from database.crud import create_user
            create_user("testuser", "test@example.com", "testpass123")

        self.client.post("/login", data={
            "username": "testuser",
            "password": "testpass123",
        })

    def test_index_page(self):
        """Landing page should return 200 after login."""
        self._login()
        res = self.client.get("/")
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"IntlQ", res.data)

    def test_index_page_redirects_when_not_logged_in(self):
        """Landing page should redirect to login when not authenticated."""
        res = self.client.get("/")
        self.assertEqual(res.status_code, 302)

    def test_get_roles(self):
        """GET /api/roles should return role list."""
        res = self.client.get("/api/roles")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertIn("roles", data)
        self.assertGreater(len(data["roles"]), 0)

    def test_start_interview(self):
        """POST /api/start should create a session."""
        self._login()
        res = self.client.post("/api/start", json={
            "role_id": "data_scientist",
            "candidate_name": "Test User",
            "question_count": 3,
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 201)
        self.assertIn("session_id", data)
        self.assertIn("questions", data)

    def test_start_interview_invalid_role(self):
        """Invalid role should return 404."""
        self._login()
        res = self.client.post("/api/start", json={
            "role_id": "nonexistent_role",
            "question_count": 3,
        })
        self.assertEqual(res.status_code, 404)

    def test_submit_answer(self):
        """Submit an answer and verify evaluation response."""
        self._login()

        # First start a session
        start_res = self.client.post("/api/start", json={
            "role_id": "software_engineer",
            "candidate_name": "Tester",
            "question_count": 1,
        })
        start_data = json.loads(start_res.data)
        session_id = start_data["session_id"]
        question_id = start_data["questions"][0]["id"]

        # Submit an answer
        res = self.client.post("/api/submit", json={
            "session_id": session_id,
            "question_id": question_id,
            "answer_text": "SOLID principles are important for clean code and maintainability.",
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertIn("score", data)
        self.assertIn("feedback", data)
        self.assertIn("evaluation", data)


if __name__ == "__main__":
    unittest.main()

