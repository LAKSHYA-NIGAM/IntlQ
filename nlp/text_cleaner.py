"""
NLP Text Cleaning Pipeline
Handles tokenization, stopword removal, and lemmatization.
"""

import re
import string

import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize


# ── Lazy-loaded resources ────────────────────────────────────────────────────
_lemmatizer = None
_stop_words = None


def _get_lemmatizer():
    global _lemmatizer
    if _lemmatizer is None:
        _lemmatizer = WordNetLemmatizer()
    return _lemmatizer


def _get_stop_words():
    global _stop_words
    if _stop_words is None:
        _stop_words = set(stopwords.words("english"))
    return _stop_words


def clean_text(text: str) -> str:
    """Lowercase, remove HTML tags, special characters, and extra whitespace."""
    if not text or not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r"<[^>]+>", "", text)          # strip HTML
    text = re.sub(r"[^\w\s\-/]", " ", text)       # keep hyphens and slashes for terms like "CI/CD"
    text = re.sub(r"\s+", " ", text).strip()
    return text


def remove_stopwords(tokens: list[str]) -> list[str]:
    """Remove English stopwords from a list of tokens."""
    stop = _get_stop_words()
    return [t for t in tokens if t not in stop and len(t) > 1]


def lemmatize(tokens: list[str]) -> list[str]:
    """Lemmatize tokens to their base form."""
    lem = _get_lemmatizer()
    return [lem.lemmatize(t) for t in tokens]


def preprocess(text: str) -> str:
    """Full preprocessing pipeline: clean → tokenize → stopwords → lemmatize.
    
    Returns a single cleaned string (for TF-IDF vectorization).
    """
    cleaned = clean_text(text)
    if not cleaned:
        return ""
    tokens = word_tokenize(cleaned)
    tokens = remove_stopwords(tokens)
    tokens = lemmatize(tokens)
    return " ".join(tokens)


def tokenize(text: str) -> list[str]:
    """Full preprocessing pipeline returning a token list (for keyword matching)."""
    cleaned = clean_text(text)
    if not cleaned:
        return []
    tokens = word_tokenize(cleaned)
    tokens = remove_stopwords(tokens)
    tokens = lemmatize(tokens)
    return tokens
