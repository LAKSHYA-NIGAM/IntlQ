"""
Tests for the API endpoints.
"""

import os
os.environ["DATABASE_URL"] = "sqlite:///:memory:"
os.environ["SECRET_KEY"] = "test-secret-key"

import unittest
import json
from app import create_app
from database.db import db
from database.crud import create_user


class TestAPI(unittest.TestCase):
    """Integration tests for Flask API endpoints."""

    def setUp(self):
        self.app = create_app()
        self.app.config["TESTING"] = True
        self.app.config["WTF_CSRF_ENABLED"] = False
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.drop_all()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def _login(self):
        """Create a test user and log in."""
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
