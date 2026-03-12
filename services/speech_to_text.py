"""
Speech-to-Text Service (Stub)
Voice input is handled client-side via the Web Speech API.
This module provides a utility for cleaning up raw transcripts.
"""


def process_transcript(raw_transcript: str) -> str:
    """Clean up a raw speech-to-text transcript.
    
    Args:
        raw_transcript: Raw text from the Web Speech API.
    
    Returns:
        Cleaned transcript string.
    """
    if not raw_transcript:
        return ""

    text = raw_transcript.strip()
    # Capitalize first letter
    text = text[0].upper() + text[1:] if len(text) > 1 else text.upper()
    # Ensure ends with period
    if text and text[-1] not in ".!?":
        text += "."
    return text
