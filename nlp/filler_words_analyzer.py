"""
Speech Fluency & Filler Words Analyzer
Detects filler word frequency (um, uh, like, you know, basically, sort of),
calculates filler density percentage, and provides fluency coaching rating.
"""

import re
from typing import Dict, Any

COMMON_FILLERS = ['um', 'uh', 'like', 'you know', 'basically', 'actually', 'sort of', 'kind of']


def analyze_speech_fluency(transcript_text: str) -> Dict[str, Any]:
  if not transcript_text or not isinstance(transcript_text, str):
    return {'word_count': 0, 'filler_count': 0, 'filler_density_pct': 0.0, 'fluency_rating': 'UNKNOWN'}

  clean_text = transcript_text.strip().lower()
  words = re.findall(r'\b[a-z]+\b', clean_text)
  total_words = len(words)

  if total_words == 0:
    return {'word_count': 0, 'filler_count': 0, 'filler_density_pct': 0.0, 'fluency_rating': 'UNKNOWN'}

  filler_counts = {}
  total_fillers = 0

  for filler in COMMON_FILLERS:
    # Use word boundary regex for each filler
    pattern = r'\b' + re.escape(filler) + r'\b'
    matches = len(re.findall(pattern, clean_text))
    if matches > 0:
      filler_counts[filler] = matches
      total_fillers += matches

  density_pct = round((total_fillers / total_words) * 100, 1)

  if density_pct <= 2.0:
    rating = 'EXCELLENT'
  elif density_pct <= 5.0:
    rating = 'GOOD'
  elif density_pct <= 8.0:
    rating = 'MODERATE'
  else:
    rating = 'HIGH_FILLER_USAGE'

  return {
    'word_count': total_words,
    'filler_count': total_fillers,
    'filler_density_pct': density_pct,
    'fluency_rating': rating,
    'fillers_breakdown': filler_counts,
  }
