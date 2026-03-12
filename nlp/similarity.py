"""
TF-IDF Cosine Similarity
Compares a candidate answer against an ideal reference answer.
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from nlp.text_cleaner import preprocess


def tfidf_similarity(answer: str, ideal_answer: str) -> float:
    """Compute TF-IDF cosine similarity between an answer and an ideal answer.
    
    Args:
        answer: The candidate's raw answer text.
        ideal_answer: The reference/ideal answer text.
    
    Returns:
        A float between 0.0 (no similarity) and 1.0 (identical).
    """
    processed_answer = preprocess(answer)
    processed_ideal = preprocess(ideal_answer)

    if not processed_answer.strip() or not processed_ideal.strip():
        return 0.0

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([processed_answer, processed_ideal])

    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
    return round(float(similarity[0][0]), 4)
