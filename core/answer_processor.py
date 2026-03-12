"""
Answer Processor
Entry point for preprocessing candidate answers before evaluation.
"""

from nlp.text_cleaner import preprocess, tokenize


def process_answer(raw_text: str) -> dict:
    """Process a raw answer text through the NLP pipeline.
    
    Args:
        raw_text: The candidate's raw answer (from text input or speech-to-text).
    
    Returns:
        {
            "raw": original text,
            "cleaned": preprocessed string for TF-IDF,
            "tokens": token list for keyword matching,
            "word_count": number of words in original
        }
    """
    if not raw_text or not raw_text.strip():
        return {
            "raw": "",
            "cleaned": "",
            "tokens": [],
            "word_count": 0,
        }

    return {
        "raw": raw_text.strip(),
        "cleaned": preprocess(raw_text),
        "tokens": tokenize(raw_text),
        "word_count": len(raw_text.split()),
    }
