"""
Keyword / Concept Coverage Matcher
Checks how many expected keywords appear in the candidate's answer.
"""

from nlp.text_cleaner import clean_text


def match_keywords(answer: str, expected_keywords: list[str]) -> dict:
    """Check how many expected keywords/concepts appear in the answer.
    
    Uses cleaned (lowercased) full-text matching so multi-word concepts
    like "decision tree" or "A/B testing" are detected properly.
    
    Args:
        answer: The candidate's raw answer text.
        expected_keywords: List of expected keyword strings.
    
    Returns:
        {
            "matched": [...],
            "missing": [...],
            "coverage_score": float  # 0.0 – 1.0
        }
    """
    cleaned_answer = clean_text(answer)

    matched = []
    missing = []

    for keyword in expected_keywords:
        keyword_lower = keyword.lower()
        if keyword_lower in cleaned_answer:
            matched.append(keyword)
        else:
            missing.append(keyword)

    total = len(expected_keywords)
    coverage = len(matched) / total if total > 0 else 0.0

    return {
        "matched": matched,
        "missing": missing,
        "coverage_score": round(coverage, 4),
    }
