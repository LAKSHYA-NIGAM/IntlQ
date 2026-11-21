"""
Comprehensive Candidate Evaluation Rubric Compiler
Aggregates dimension scores (Technical Depth, Problem Solving, Communication, Culture Add)
and generates weighted hiring decisions: Strong Hire, Hire, Leaning Hire, Leaning No Hire, Strong No Hire.
"""

from typing import Dict, Any

WEIGHTS = {
  'technical_depth': 0.35,
  'problem_solving': 0.30,
  'communication': 0.20,
  'culture_add': 0.15,
}


def compile_candidate_rubric(scores: Dict[str, float]) -> Dict[str, Any]:
  if not scores or not isinstance(scores, dict):
    return {'overall_score': 0.0, 'recommendation': 'STRONG_NO_HIRE'}

  weighted_sum = 0.0
  total_weight = 0.0
  breakdown = {}

  for dim, weight in WEIGHTS.items():
    raw_score = float(scores.get(dim, 1.0))
    # Clamp score to 1.0 - 5.0
    clamped = max(1.0, min(5.0, raw_score))
    weighted_sum += clamped * weight
    total_weight += weight
    breakdown[dim] = clamped

  composite = round(weighted_sum / total_weight, 2) if total_weight > 0 else 1.0

  if composite >= 4.2:
    rec = 'STRONG_HIRE'
  elif composite >= 3.5:
    rec = 'HIRE'
  elif composite >= 3.0:
    rec = 'LEANING_HIRE'
  elif composite >= 2.3:
    rec = 'LEANING_NO_HIRE'
  else:
    rec = 'STRONG_NO_HIRE'

  return {
    'overall_score': composite,
    'recommendation': rec,
    'dimension_breakdown': breakdown,
    'is_hire': rec in ('STRONG_HIRE', 'HIRE', 'LEANING_HIRE'),
  }
