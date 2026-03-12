"""
Interview Engine
Loads questions from JSON, filters by role/difficulty/category, and returns a randomized set.
"""

import json
import os
import random

from config.settings import QUESTIONS_DIR


def _load_questions(role_id: str) -> list[dict]:
    """Load question bank for a given role from its JSON file."""
    path = os.path.join(QUESTIONS_DIR, f"{role_id}.json")
    if not os.path.exists(path):
        raise FileNotFoundError(f"No question file found for role: {role_id}")
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("questions", [])


def get_questions(
    role_id: str,
    difficulty: str | None = None,
    category: str | None = None,
    count: int = 5,
) -> list[dict]:
    """Select a set of interview questions.
    
    Args:
        role_id: Identifier for the job role (e.g., "data_scientist").
        difficulty: Optional filter — "easy", "medium", or "hard".
        category: Optional filter — "technical", "behavioral", etc.
        count: Number of questions to return.
    
    Returns:
        A list of question dicts with id, text, category, difficulty, expected_concepts.
    """
    questions = _load_questions(role_id)

    # Apply filters
    if difficulty:
        questions = [q for q in questions if q["difficulty"] == difficulty]
    if category:
        questions = [q for q in questions if q["category"] == category]

    # Randomize and cap
    random.shuffle(questions)
    return questions[:count]


def get_question_by_id(role_id: str, question_id: str) -> dict | None:
    """Retrieve a single question by its ID."""
    questions = _load_questions(role_id)
    for q in questions:
        if q["id"] == question_id:
            return q
    return None
