"""
Tests for the Admin Dashboard.
"""

import os
os.environ["DATABASE_URL"] = "sqlite:///:memory:"
os.environ["SECRET_KEY"] = "test-secret-key"

import unittest
from app import create_app
from database.db import db
from database.crud import create_user, make_admin


class TestAdminDashboard(unittest.TestCase):
    """Verify admin dashboard access workflows."""

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

    def test_admin_access_workflow(self):
        """Verify admin dashboard access, non-admin denial, and data rendering."""
        # 1. Create admin and normal user
        admin_user = create_user("admin1", "admin@example.com", "admin123")
        make_admin(admin_user.id)
        create_user("testuser", "test@example.com", "test123")

        # 2. Login as admin
        login_res = self.client.post("/login", data={
            "username": "admin1",
            "password": "admin123",
        })
        self.assertEqual(login_res.status_code, 302)

        # 3. Access admin page as admin
        admin_page_res = self.client.get("/admin")
        self.assertEqual(admin_page_res.status_code, 200)
        self.assertIn(b"Admin Dashboard", admin_page_res.data)
        self.assertIn(b"admin1", admin_page_res.data)
        self.assertIn(b"testuser", admin_page_res.data)

        # 4. Logout admin
        logout_res = self.client.get("/logout")
        self.assertEqual(logout_res.status_code, 302)

        # 5. Login as normal user
        user_login_res = self.client.post("/login", data={
            "username": "testuser",
            "password": "test123",
        })
        self.assertEqual(user_login_res.status_code, 302)

        # 6. Access admin page as non-admin -> should receive 403 Access Denied
        forbidden_page_res = self.client.get("/admin")
        self.assertEqual(forbidden_page_res.status_code, 403)
        self.assertIn(b"Access denied", forbidden_page_res.data)
