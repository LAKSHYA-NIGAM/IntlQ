"""
Technical Skills Taxonomy & Competency Depth Mapper
Matches candidate interview transcripts against standard engineering taxonomies:
- Languages (Python, Java, JavaScript, TypeScript, Go, C++)
- Frameworks (React, FastAPI, Flask, Express, Spring, Django)
- Databases (PostgreSQL, MongoDB, Redis, MySQL)
- Cloud/DevOps (Docker, Kubernetes, AWS, GCP, CI/CD)
"""

import re
from typing import Dict, Any, List

TAXONOMY = {
  'languages': ['python', 'java', 'javascript', 'typescript', 'golang', 'c++'],
  'frameworks': ['react', 'fastapi', 'flask', 'express', 'spring', 'django', 'next.js', 'vue'],
  'databases': ['postgresql', 'mongodb', 'redis', 'mysql', 'sqlite', 'elasticsearch'],
  'devops': ['docker', 'kubernetes', 'aws', 'gcp', 'ci/cd', 'git', 'linux'],
}


def map_technical_taxonomy(transcript_text: str) -> Dict[str, Any]:
  if not transcript_text or not isinstance(transcript_text, str):
    return {'categories': {}, 'total_unique_skills': 0}

  clean_text = transcript_text.lower()
  categories_matched = {}
  total_skills = set()

  for category, skills in TAXONOMY.items():
    found = []
    for skill in skills:
      # Match word or exact skill term
      pattern = r'(?:\b|_)' + re.escape(skill) + r'(?:\b|_)'
      if re.search(pattern, clean_text):
        found.append(skill)
        total_skills.add(skill)
    categories_matched[category] = found

  return {
    'categories': categories_matched,
    'total_unique_skills': len(total_skills),
    'skills_list': sorted(list(total_skills)),
  }
