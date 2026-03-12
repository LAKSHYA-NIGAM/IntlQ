"""
Text Utilities
Shared text helper functions.
"""


def truncate(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """Truncate text to max_length, adding suffix if truncated."""
    if len(text) <= max_length:
        return text
    return text[: max_length - len(suffix)].rstrip() + suffix


def word_count(text: str) -> int:
    """Count words in a text string."""
    return len(text.split()) if text and text.strip() else 0


def format_percentage(value: float, decimals: int = 1) -> str:
    """Format a 0.0–1.0 value as a percentage string."""
    return f"{value * 100:.{decimals}f}%"
