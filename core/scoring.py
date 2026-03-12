"""
Scoring Engine
Computes final scores using weighted formula and assigns grades.
"""

from config.settings import SIMILARITY_WEIGHT, KEYWORD_WEIGHT


# ── Grade boundaries ─────────────────────────────────────────────────────────
GRADE_THRESHOLDS = [
    (90, "A+", "Exceptional"),
    (80, "A",  "Excellent"),
    (70, "B+", "Very Good"),
    (60, "B",  "Good"),
    (50, "C+", "Above Average"),
    (40, "C",  "Average"),
    (30, "D",  "Below Average"),
    (0,  "F",  "Needs Significant Improvement"),
]


def calculate_score(
    similarity: float,
    keyword_coverage: float,
    weights: dict | None = None,
) -> dict:
    """Calculate the final weighted score for an answer.
    
    Args:
        similarity: TF-IDF cosine similarity score (0.0–1.0).
        keyword_coverage: Keyword coverage score (0.0–1.0).
        weights: Optional dict with "similarity" and "keyword" keys (0.0–1.0).
    
    Returns:
        {
            "total_score": float (0–100),
            "grade": str,
            "grade_label": str,
            "breakdown": {
                "similarity_score": float,
                "similarity_weighted": float,
                "keyword_score": float,
                "keyword_weighted": float,
            }
        }
    """
    sim_w = (weights or {}).get("similarity", SIMILARITY_WEIGHT)
    kw_w = (weights or {}).get("keyword", KEYWORD_WEIGHT)

    # Convert to 0–100 scale
    sim_pct = similarity * 100
    kw_pct = keyword_coverage * 100

    total = (sim_pct * sim_w) + (kw_pct * kw_w)
    total = round(min(total, 100), 2)

    # Determine grade
    grade, grade_label = "F", "Needs Significant Improvement"
    for threshold, g, label in GRADE_THRESHOLDS:
        if total >= threshold:
            grade, grade_label = g, label
            break

    return {
        "total_score": total,
        "grade": grade,
        "grade_label": grade_label,
        "breakdown": {
            "similarity_score": round(sim_pct, 2),
            "similarity_weighted": round(sim_pct * sim_w, 2),
            "keyword_score": round(kw_pct, 2),
            "keyword_weighted": round(kw_pct * kw_w, 2),
        },
    }
