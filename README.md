# IntlQ — AI-Powered Interview Simulator

> Practice real interviews. Get instant AI evaluation. Improve with actionable feedback.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Flask](https://img.shields.io/badge/Flask-3.0-green)
![NLP](https://img.shields.io/badge/NLP-NLTK%20%2B%20scikit--learn-orange)

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Application
```bash
python app.py
```

### 3. Open in Browser
Navigate to https://intl-q.vercel.app/

---

## 🏗️ Architecture

```
User → Select Job Role
     → Interview Engine generates questions
     → User answers (text / voice)
     → Answer Evaluation Engine (NLP)
     → Scoring + Feedback
     → Performance Dashboard
```

## 📁 Project Structure

| Module | Path | Description |
|--------|------|-------------|
| Config | `config/` | App settings, role definitions |
| Data | `data/` | Question banks, ideal answers, keywords |
| NLP | `nlp/` | Text cleaning, TF-IDF similarity, keyword matching |
| Core | `core/` | Interview engine, evaluator, scoring, feedback |
| Database | `database/` | SQLite + SQLAlchemy ORM |
| API | `api/` | Flask routes + Pydantic schemas |
| Frontend | `frontend/` | Jinja2 templates + CSS + JS |
| Utils | `utils/` | Logger, text/date helpers |
| Tests | `tests/` | Unit + integration tests |

## 🧪 Running Tests

```bash
python -m pytest tests/ -v
```

## 🎤 Voice Input

Voice input uses the browser's built-in **Web Speech API** — no API keys needed. Works best in Chrome or Edge.

## 📊 Scoring Formula

| Component | Weight | Method |
|-----------|--------|--------|
| Similarity | 60% | TF-IDF cosine similarity vs ideal answer |
| Keywords | 40% | Concept coverage matching |

## 📜 License

MIT
