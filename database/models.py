"""
Database Models
ORM models for users, interview sessions, and answer records.
"""

import json
from datetime import datetime, timezone

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from database.db import db


class User(UserMixin, db.Model):
    """Registered user account."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    college = db.Column(db.String(200), nullable=True)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationship
    sessions = db.relationship("InterviewSession", backref="user", lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class InterviewSession(db.Model):
    """Represents a single interview session."""

    __tablename__ = "interview_sessions"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    candidate_name = db.Column(db.String(100), nullable=False, default="Anonymous")
    role_id = db.Column(db.String(50), nullable=False)
    difficulty = db.Column(db.String(20), nullable=True)
    question_count = db.Column(db.Integer, default=5)
    overall_score = db.Column(db.Float, nullable=True)
    overall_grade = db.Column(db.String(5), nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    completed_at = db.Column(db.DateTime, nullable=True)

    # Proctoring fields
    tab_violations = db.Column(db.Integer, default=0)
    gaze_violations = db.Column(db.Integer, default=0)
    terminated = db.Column(db.Boolean, default=False)

    # Relationship
    answers = db.relationship("AnswerRecord", backref="session", lazy=True, cascade="all, delete-orphan")

    # Store question IDs as JSON string
    question_ids_json = db.Column(db.Text, nullable=True)

    @property
    def question_ids(self):
        return json.loads(self.question_ids_json) if self.question_ids_json else []

    @question_ids.setter
    def question_ids(self, ids):
        self.question_ids_json = json.dumps(ids)


class AnswerRecord(db.Model):
    """Stores a single answer and its evaluation."""

    __tablename__ = "answer_records"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    session_id = db.Column(db.Integer, db.ForeignKey("interview_sessions.id"), nullable=False)
    question_id = db.Column(db.String(20), nullable=False)
    question_text = db.Column(db.Text, nullable=True)
    answer_text = db.Column(db.Text, nullable=False)
    similarity_score = db.Column(db.Float, default=0.0)
    keyword_score = db.Column(db.Float, default=0.0)
    total_score = db.Column(db.Float, default=0.0)
    grade = db.Column(db.String(5), nullable=True)
    feedback_json = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    @property
    def feedback(self):
        return json.loads(self.feedback_json) if self.feedback_json else {}

    @feedback.setter
    def feedback(self, data):
        self.feedback_json = json.dumps(data)
