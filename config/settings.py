import os
import json

from dotenv import load_dotenv

load_dotenv()


# ── Paths ────────────────────────────────────────────────────────────────────
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_DIR = os.path.join(BASE_DIR, "data")
QUESTIONS_DIR = os.path.join(DATA_DIR, "questions")
BENCHMARKS_DIR = os.path.join(DATA_DIR, "benchmarks")
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")

# ── Flask ────────────────────────────────────────────────────────────────────
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
DEBUG = os.getenv("DEBUG", "True").lower() in ("true", "1", "yes")

# ── Database ─────────────────────────────────────────────────────────────────
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///intlq.db")

# ── Scoring Weights ──────────────────────────────────────────────────────────
SIMILARITY_WEIGHT = 0.60
KEYWORD_WEIGHT = 0.40

# ── Roles ────────────────────────────────────────────────────────────────────
ROLES_CONFIG_PATH = os.path.join(os.path.dirname(__file__), "roles_config.json")


def load_roles_config():
    """Load roles configuration from JSON."""
    with open(ROLES_CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)
