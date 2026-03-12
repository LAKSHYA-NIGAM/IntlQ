"""
Feedback Engine
Generates structured, actionable feedback based on evaluation results.
"""


def generate_feedback(eval_result: dict, score_result: dict) -> dict:
    """Generate human-readable feedback for a candidate's answer.
    
    Args:
        eval_result: Output from evaluator.evaluate().
        score_result: Output from scoring.calculate_score().
    
    Returns:
        {
            "strengths": [...],
            "improvements": [...],
            "tips": [...],
            "overall_comment": str,
        }
    """
    total = score_result["total_score"]
    sim = score_result["breakdown"]["similarity_score"]
    kw = score_result["breakdown"]["keyword_score"]
    matched = eval_result.get("matched_keywords", [])
    missing = eval_result.get("missing_keywords", [])

    strengths = []
    improvements = []
    tips = []

    # ── Strengths ────────────────────────────────────────────────────────
    if sim >= 70:
        strengths.append("Your answer closely aligns with the expected response — strong conceptual understanding.")
    elif sim >= 40:
        strengths.append("You covered several relevant points in your answer.")

    if kw >= 70:
        strengths.append(f"Excellent keyword coverage — you mentioned {len(matched)} key concepts.")
    elif kw >= 40:
        strengths.append(f"Good concept coverage — you mentioned {len(matched)} out of {len(matched) + len(missing)} key terms.")

    if not strengths:
        strengths.append("You attempted the question, which is a good starting point.")

    # ── Improvements ─────────────────────────────────────────────────────
    if sim < 40:
        improvements.append("Your answer diverges significantly from the expected response. Focus on core concepts.")

    if missing:
        if len(missing) <= 3:
            improvements.append(f"Consider mentioning: {', '.join(missing)}.")
        else:
            improvements.append(f"Key concepts missing: {', '.join(missing[:4])} and {len(missing) - 4} more.")

    if kw < 40:
        improvements.append("Try to use more technical terminology relevant to the topic.")

    # ── Tips ─────────────────────────────────────────────────────────────
    if total < 50:
        tips.append("Structure your answer with a clear introduction, explanation, and examples.")
        tips.append("Review the fundamental concepts for this topic before your next attempt.")
    elif total < 70:
        tips.append("Add concrete examples or real-world scenarios to strengthen your answer.")
        tips.append("Try to cover both breadth and depth — mention key concepts and explain them.")
    else:
        tips.append("Excellent work! To go even further, consider discussing edge cases or trade-offs.")
        tips.append("Adding real-world experience or specific project examples would make your answer stand out.")

    # ── Overall comment ──────────────────────────────────────────────────
    if total >= 80:
        comment = f"Outstanding answer! You scored {total}/100 ({score_result['grade']}). You demonstrated strong understanding of the topic."
    elif total >= 60:
        comment = f"Good answer — {total}/100 ({score_result['grade']}). You're on the right track with room for improvement."
    elif total >= 40:
        comment = f"Decent attempt — {total}/100 ({score_result['grade']}). Focus on the missing concepts to improve your score."
    else:
        comment = f"Score: {total}/100 ({score_result['grade']}). This topic needs more study. Review the key concepts and try again."

    return {
        "strengths": strengths,
        "improvements": improvements,
        "tips": tips,
        "overall_comment": comment,
    }
