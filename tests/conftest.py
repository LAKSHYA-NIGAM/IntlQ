"""
Shared pytest fixtures for IntlQ test suite.
"""

import os
import sys
import pytest

# Ensure project root is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

os.environ["DATABASE_URL"] = "sqlite:///:memory:"
os.environ["SECRET_KEY"] = "test-secret-key"

from app import create_app
from database.db import db as _db


@pytest.fixture(scope="session")
def app():
    """Create an application instance for the test session."""
    app = create_app()
    app.config["TESTING"] = True
    app.config["WTF_CSRF_ENABLED"] = False
    return app


@pytest.fixture(autouse=True)
def reset_db(app):
    """Reset the database before each test."""
    with app.app_context():
        _db.drop_all()
        _db.create_all()
        yield
        _db.session.rollback()


@pytest.fixture
def client(app):
    """Flask test client."""
    return app.test_client()


@pytest.fixture
def db(app):
    """Database session."""
    return _db
