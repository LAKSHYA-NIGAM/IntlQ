"""
STAR Method Behavioral Interview Response Evaluator
Analyzes candidate answers for presence of all 4 pillars:
- Situation (context, setting, company background)
- Task (objective, challenge, problem statement)
- Action (steps taken, leadership, engineering implementation)
- Result (quantifiable impact, business outcomes, key learnings)
"""

import re
from typing import Dict, Any

PILLAR_KEYWORDS = {
  'situation': ['when i was', 'at my previous', 'our team was', 'the client had', 'project background', 'context'],
  'task': ['my goal was', 'the objective was', 'i was responsible for', 'we needed to', 'challenge was', 'my task'],
  'action': ['i developed', 'i implemented', 'i designed', 'i initiated', 'i built', 'i coordinated', 'i refactored'],
  'result': ['as a result', 'we increased', 'reduced by', 'improved', 'successfully delivered', 'outcome was', '%', 'saved'],
}


def evaluate_star_completeness(response_text: str) -> Dict[str, Any]:
  if not response_text or not isinstance(response_text, str) or len(response_text.strip()) == 0:
    return {'completeness_score': 0.0, 'pillars_present': [], 'missing_pillars': ['situation', 'task', 'action', 'result']}

  text_lower = response_text.lower()
  present = []
  missing = []

  for pillar, keywords in PILLAR_KEYWORDS.items():
    matched = any(kw in text_lower for kw in keywords)
    if matched:
      present.append(pillar)
    else:
      missing.append(pillar)

  score = round(len(present) / 4.0, 2)

  return {
    'completeness_score': score,
    'completeness_pct': f"{int(score * 100)}%",
    'pillars_present': present,
    'missing_pillars': missing,
    'is_well_structured': score >= 0.75,
  }
