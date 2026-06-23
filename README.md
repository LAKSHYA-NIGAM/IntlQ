<div align="center">

# 🤖 IntlQ
### AI-Powered Interview Simulator

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikitlearn&logoColor=white)
![NLTK](https://img.shields.io/badge/NLTK-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Vercel](https://img.shields.io/badge/Vercel-000000?style=for-the-badge&logo=vercel&logoColor=white)

**Practice real interviews. Get instant AI evaluation. Improve with actionable feedback.**

[🚀 Live Demo](https://intl-q.vercel.app/) · [Report Bug](https://github.com/LAKSHYA-NIGAM/IntlQ/issues) · [Request Feature](https://github.com/LAKSHYA-NIGAM/IntlQ/issues)

</div>

---

## 📌 About The Project

IntlQ is a full-stack AI-powered interview simulator that generates role-specific interview questions and evaluates candidate responses using a dual NLP pipeline — combining **TF-IDF cosine similarity** with **keyword concept coverage matching** for meaningful, instant feedback.

Built with a production-grade architecture: full user authentication, session persistence, proctoring system (tab + gaze violation detection), admin dashboard, and a clean NLP evaluation engine backed by NLTK lemmatization and scikit-learn vectorization.

Supports **8 job roles**, **3 difficulty levels**, and **3 question categories** — with a curated question bank and ideal answer benchmarks for every role.

---

## ✨ Core Features

### 🧠 Dual NLP Evaluation Engine
- **TF-IDF Cosine Similarity (60%)** — vectorizes candidate and ideal answers using scikit-learn's `TfidfVectorizer`, runs NLTK-based preprocessing (tokenization, stopword removal, lemmatization), and computes cosine similarity
- **Keyword Concept Coverage (40%)** — matches multi-word technical concepts (e.g. "decision tree", "CI/CD") against curated expected concept lists per question
- **Grading System** — A+ to F grades with structured score breakdown per answer

### 🎯 8 Supported Job Roles
| Role | Categories |
|---|---|
| Software Engineer | Technical, Behavioral, System Design |
| Data Scientist | Technical, Behavioral, Case Study |
| ML Engineer | Technical, Behavioral, Case Study |
| DevOps Engineer | Technical, Behavioral, Case Study |
| Cloud Architect | Technical, Behavioral, Case Study |
| Cybersecurity Analyst | Technical, Behavioral, Case Study |
| Product Manager | Technical, Behavioral, Case Study |
| Frontend Developer | Technical, Behavioral, Case Study |

### 🔐 Full Authentication System
- User registration and login with hashed passwords (Werkzeug)
- Flask-Login session management
- Admin panel with full user and session oversight

### 🛡️ Proctoring System
- **Tab switch violation tracking** — detects and records every time a candidate leaves the interview tab
- **Gaze violation detection** — monitors candidate attention via `proctor.js`
- Violations logged per session; admin can view and terminate flagged sessions

### 🎤 Voice Input
- Browser-native **Web Speech API** — no API keys required
- Speech-to-text transcript cleaning pipeline (capitalisation, punctuation normalisation)
- Works best in Chrome and Edge

### 📊 Performance Dashboard
- Per-question score breakdown (similarity + keyword scores)
- Matched vs. missing keywords highlighted
- Actionable strengths, improvements, and tips from feedback engine
- Full session history with grades

### 🗄️ Database & Admin
- SQLAlchemy ORM with SQLite (local) / PostgreSQL (production)
- Admin dashboard: view all users, all sessions, platform-wide stats
- Admin session termination for flagged/violated interviews

---

## 🏗️ How The NLP Pipeline Works

```
Candidate Answer
      │
      ▼
NLP Text Cleaner (NLTK)
  ├── Lowercasing + HTML strip
  ├── Tokenization (punkt)
  ├── Stopword removal
  └── Lemmatization (WordNetLemmatizer)
      │
      ├──────────────────────────────┐
      ▼                              ▼
TF-IDF Similarity              Keyword Matcher
(scikit-learn)                 (concept coverage)
  └── vs. Ideal Answer           └── vs. expected_concepts[]
  └── Cosine Similarity          └── multi-word matching
  └── Score: 0.0–1.0             └── Score: 0.0–1.0
      │                              │
      └──────────┬───────────────────┘
                 ▼
         Scoring Engine
    (similarity × 0.60) + (keywords × 0.40)
         = Total Score (0–100)
         = Grade (A+ to F)
                 │
                 ▼
         Feedback Engine
    Strengths + Improvements + Tips
```

---

## 📊 Scoring Formula

| Component | Weight | Method |
|---|---|---|
| **Similarity Score** | 60% | TF-IDF cosine similarity vs ideal answer |
| **Keyword Coverage** | 40% | Multi-word concept matching |

**Grade Boundaries:**

| Grade | Score | Label |
|---|---|---|
| A+ | ≥ 90 | Exceptional |
| A | ≥ 80 | Excellent |
| B+ | ≥ 70 | Very Good |
| B | ≥ 60 | Good |
| C+ | ≥ 50 | Above Average |
| C | ≥ 40 | Average |
| D | ≥ 30 | Below Average |
| F | < 30 | Needs Significant Improvement |

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.9+, Flask, Flask-Login |
| NLP | scikit-learn (TF-IDF, cosine similarity), NLTK (tokenization, lemmatization, stopwords) |
| Database | SQLite (dev), PostgreSQL (prod), SQLAlchemy ORM |
| Auth | Werkzeug password hashing, Flask-Login sessions |
| Validation | Pydantic schemas |
| Frontend | Jinja2 templates, HTML5, CSS3, JavaScript |
| Voice | Web Speech API (browser-native) |
| Proctoring | Custom JS (tab detection, gaze tracking) |
| Testing | pytest (unit + integration) |
| Deployment | Vercel (frontend), Render (backend), Docker-ready |

---

## 🚀 Getting Started

> **Try it live:** [intl-q.vercel.app](https://intl-q.vercel.app/)

### Prerequisites
- Python 3.9+
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/LAKSHYA-NIGAM/IntlQ.git
cd IntlQ

# Install dependencies
pip install -r requirements.txt

# Initialize the database
python init_db.py

# Run the application
python app.py
```

Open [http://localhost:5000](http://localhost:5000) in your browser.

### Environment Variables

```env
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///intlq.db   # or postgresql://... for production
```

### Running Tests

```bash
python -m pytest tests/ -v
```

---

## 📂 Project Structure

| Module | Path | Description |
|---|---|---|
| Config | `config/` | App settings, roles config JSON, scoring weights |
| Data | `data/questions/` | Role-specific question banks (8 JSON files) |
| Benchmarks | `data/benchmarks/` | Ideal answers + expected keywords per question |
| NLP | `nlp/` | Text cleaner, TF-IDF similarity, keyword matcher |
| Core | `core/` | Interview engine, evaluator, scoring, feedback engine |
| Database | `database/` | SQLAlchemy models (User, InterviewSession, AnswerRecord), CRUD |
| API | `api/` | Flask Blueprint routes + Pydantic schemas |
| Frontend | `frontend/` | Jinja2 templates (index, interview, results, history, admin, login) |
| Services | `services/` | Speech-to-text transcript cleaner, resume parser (stub) |
| Utils | `utils/` | Logger, text helpers, date utils |
| Tests | `tests/` | Unit + integration tests (API, evaluator, scoring, admin) |
| Deployment | `deployment/` | Dockerfile + start.sh |

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

---

<div align="center">
Made with ❤️ by <a href="https://github.com/LAKSHYA-NIGAM">Lakshya Nigam</a>
<br/>
<a href="https://intl-q.vercel.app/">intl-q.vercel.app</a>
</div>
EOF
echo "Done"
