"""
CRUD Operations
Database create/read operations for users, sessions, and answers.
"""

import json
from datetime import datetime, timezone

from database.db import db
from database.models import User, InterviewSession, AnswerRecord


# ── Users ─────────────────────────────────────────────────────────────────────

def create_user(username: str, email: str, password: str, phone: str | None = None, college: str | None = None) -> User:
    """Create a new user account."""
    user = User(username=username, email=email, phone=phone, college=college)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return user


def get_user_by_id(user_id: int) -> User | None:
    """Get a user by ID."""
    return db.session.get(User, user_id)


def get_user_by_username(username: str) -> User | None:
    """Get a user by username."""
    return User.query.filter_by(username=username).first()


def get_user_by_email(email: str) -> User | None:
    """Get a user by email."""
    return User.query.filter_by(email=email).first()


def get_all_users() -> list[User]:
    """Get all users ordered by creation date (newest first)."""
    return User.query.order_by(User.created_at.desc()).all()


def make_admin(user_id: int) -> User | None:
    """Promote a user to admin."""
    user = get_user_by_id(user_id)
    if user:
        user.is_admin = True
        db.session.commit()
    return user


def get_admin_stats() -> dict:
    """Get summary statistics for the admin dashboard."""
    from sqlalchemy import func
    total_users = User.query.count()
    total_sessions = InterviewSession.query.count()
    completed_sessions = InterviewSession.query.filter(InterviewSession.completed_at.isnot(None)).count()
    avg_score_result = db.session.query(func.avg(InterviewSession.overall_score)).filter(
        InterviewSession.overall_score.isnot(None)
    ).scalar()
    avg_score = round(avg_score_result, 1) if avg_score_result else 0.0

    return {
        "total_users": total_users,
        "total_sessions": total_sessions,
        "completed_sessions": completed_sessions,
        "avg_score": avg_score,
    }


# ── Sessions ─────────────────────────────────────────────────────────────────

def create_session(candidate_name: str, role_id: str, difficulty: str | None, question_ids: list[str], user_id: int | None = None) -> InterviewSession:
    """Create a new interview session."""
    session = InterviewSession(
        user_id=user_id,
        candidate_name=candidate_name or "Anonymous",
        role_id=role_id,
        difficulty=difficulty,
        question_count=len(question_ids),
    )
    session.question_ids = question_ids
    db.session.add(session)
    db.session.commit()
    return session


def get_session(session_id: int) -> InterviewSession | None:
    """Get a session by ID."""
    return db.session.get(InterviewSession, session_id)


def complete_session(session_id: int, overall_score: float, overall_grade: str) -> InterviewSession | None:
    """Mark a session as completed with final scores."""
    session = get_session(session_id)
    if session:
        session.overall_score = overall_score
        session.overall_grade = overall_grade
        session.completed_at = datetime.now(timezone.utc)
        db.session.commit()
    return session


def get_all_sessions() -> list[InterviewSession]:
    """Get all sessions ordered by creation date (newest first)."""
    return InterviewSession.query.order_by(InterviewSession.created_at.desc()).all()


def get_user_sessions(user_id: int) -> list[InterviewSession]:
    """Get all sessions for a specific user (newest first)."""
    return InterviewSession.query.filter_by(user_id=user_id).order_by(InterviewSession.created_at.desc()).all()


def record_violation(session_id: int, violation_type: str) -> InterviewSession | None:
    """Record a proctoring violation (tab_switch or gaze)."""
    session = get_session(session_id)
    if session:
        if violation_type == "tab_switch":
            session.tab_violations = (session.tab_violations or 0) + 1
        elif violation_type == "gaze":
            session.gaze_violations = (session.gaze_violations or 0) + 1
        db.session.commit()
    return session


def terminate_session(session_id: int) -> InterviewSession | None:
    """Mark a session as terminated due to proctoring violations."""
    session = get_session(session_id)
    if session:
        session.terminated = True
        session.completed_at = datetime.now(timezone.utc)
        db.session.commit()
    return session


# ── Answers ──────────────────────────────────────────────────────────────────

def save_answer(
    session_id: int,
    question_id: str,
    question_text: str,
    answer_text: str,
    similarity_score: float,
    keyword_score: float,
    total_score: float,
    grade: str,
    feedback: dict,
) -> AnswerRecord:
    """Save an answer and its evaluation results."""
    record = AnswerRecord(
        session_id=session_id,
        question_id=question_id,
        question_text=question_text,
        answer_text=answer_text,
        similarity_score=similarity_score,
        keyword_score=keyword_score,
        total_score=total_score,
        grade=grade,
    )
    record.feedback = feedback
    db.session.add(record)
    db.session.commit()
    return record


def get_session_answers(session_id: int) -> list[AnswerRecord]:
    """Get all answers for a given session."""
    return AnswerRecord.query.filter_by(session_id=session_id).all()


def get_session_results(session_id: int) -> dict | None:
    """Get complete session results including all answers and feedback."""
    session = get_session(session_id)
    if not session:
        return None

    answers = get_session_answers(session_id)

    return {
        "session": {
            "id": session.id,
            "candidate_name": session.candidate_name,
            "role_id": session.role_id,
            "difficulty": session.difficulty,
            "question_count": session.question_count,
            "overall_score": session.overall_score,
            "overall_grade": session.overall_grade,
            "created_at": session.created_at.isoformat() if session.created_at else None,
            "completed_at": session.completed_at.isoformat() if session.completed_at else None,
            "tab_violations": session.tab_violations or 0,
            "gaze_violations": session.gaze_violations or 0,
            "terminated": session.terminated or False,
        },
        "answers": [
            {
                "question_id": a.question_id,
                "question_text": a.question_text,
                "answer_text": a.answer_text,
                "similarity_score": a.similarity_score,
                "keyword_score": a.keyword_score,
                "total_score": a.total_score,
                "grade": a.grade,
                "feedback": a.feedback,
            }
            for a in answers
        ],
    }
