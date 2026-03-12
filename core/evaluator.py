"""
Evaluator
Orchestrates similarity scoring and keyword matching for a given answer.
"""

import json
import os

from config.settings import BENCHMARKS_DIR
from nlp.similarity import tfidf_similarity
from nlp.keyword_matcher import match_keywords


# ── Lazy-loaded benchmark data ───────────────────────────────────────────────
_ideal_answers = None
_keywords = None


def _load_ideal_answers() -> dict:
    global _ideal_answers
    if _ideal_answers is None:
        path = os.path.join(BENCHMARKS_DIR, "ideal_answers.json")
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        _ideal_answers = data.get("ideal_answers", {})
    return _ideal_answers


def _load_keywords() -> dict:
    global _keywords
    if _keywords is None:
        path = os.path.join(BENCHMARKS_DIR, "keywords.json")
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        _keywords = data.get("keywords", {})
    return _keywords


def evaluate(question_id: str, raw_answer: str) -> dict:
    """Evaluate a candidate's answer against benchmarks.
    
    Args:
        question_id: The question identifier (e.g., "ds_t1").
        raw_answer: The candidate's raw answer text.
    
    Returns:
        {
            "similarity_score": float,      # 0.0 – 1.0
            "keyword_coverage": float,       # 0.0 – 1.0
            "matched_keywords": [...],
            "missing_keywords": [...],
        }
    """
    ideal_answers = _load_ideal_answers()
    keywords = _load_keywords()

    # ── Similarity scoring ───────────────────────────────────────────────
    ideal = ideal_answers.get(question_id, "")
    sim_score = tfidf_similarity(raw_answer, ideal) if ideal else 0.0

    # ── Keyword matching ─────────────────────────────────────────────────
    expected = keywords.get(question_id, [])
    kw_result = match_keywords(raw_answer, expected) if expected else {
        "matched": [], "missing": [], "coverage_score": 0.0
    }

    return {
        "similarity_score": sim_score,
        "keyword_coverage": kw_result["coverage_score"],
        "matched_keywords": kw_result["matched"],
        "missing_keywords": kw_result["missing"],
    }
