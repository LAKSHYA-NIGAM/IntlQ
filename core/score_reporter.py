"""
IntlQ Candidate Interview Scorecard & Hire Decision Engine
Synthesizes multi-question evaluations into an executive candidate scorecard,
skill gap matrix, and benchmarked hiring recommendation.
"""

from typing import Dict, List, Optional


class InterviewScoreReporter:
    @classmethod
    def evaluate_interview_session(
        cls, candidate_name: str, role: str, evaluations: List[Dict]
    ) -> Dict:
        """
        Evaluates complete interview session across questions.
        evaluations: [{ question_id, topic, score (0-100), keyword_coverage (0-1.0), similarity (0-1.0) }]
        """
        if not evaluations:
            return {
                "candidate_name": candidate_name,
                "role": role,
                "overall_score": 0.0,
                "recommendation": "NO_EVALUATIONS_RECORDED",
                "strengths": [],
                "areas_for_growth": [],
                "topic_breakdown": {}
            }

        total_score = sum(float(e.get("score", 0.0)) for e in evaluations)
        overall_score = round(total_score / len(evaluations), 1)

        # Topic level aggregation
        topic_scores: Dict[str, List[float]] = {}
        for e in evaluations:
            topic = e.get("topic", "General")
            topic_scores.setdefault(topic, []).append(float(e.get("score", 0.0)))

        topic_breakdown = {
            t: round(sum(scores) / len(scores), 1) for t, scores in topic_scores.items()
        }

        strengths = [t for t, s in topic_breakdown.items() if s >= 75.0]
        areas_for_growth = [t for t, s in topic_breakdown.items() if s < 60.0]

        # Recommendation thresholds
        if overall_score >= 85.0:
            rec = "STRONG_HIRE"
        elif overall_score >= 70.0:
            rec = "HIRE"
        elif overall_score >= 55.0:
            rec = "LEAN_HIRE"
        else:
            rec = "NO_HIRE"

        return {
            "candidate_name": candidate_name,
            "role": role,
            "question_count": len(evaluations),
            "overall_score": overall_score,
            "recommendation": rec,
            "strengths": strengths,
            "areas_for_growth": areas_for_growth,
            "topic_breakdown": topic_breakdown
        }
