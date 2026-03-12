"""
Date Utilities
Date formatting helpers.
"""

from datetime import datetime, timezone


def format_timestamp(dt: datetime | None, fmt: str = "%b %d, %Y %I:%M %p") -> str:
    """Format a datetime object to a string."""
    if not dt:
        return "N/A"
    return dt.strftime(fmt)


def time_ago(dt: datetime | None) -> str:
    """Return a human-readable 'X ago' string."""
    if not dt:
        return "N/A"

    now = datetime.now(timezone.utc)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)

    diff = now - dt
    seconds = int(diff.total_seconds())

    if seconds < 60:
        return "just now"
    elif seconds < 3600:
        minutes = seconds // 60
        return f"{minutes} min{'s' if minutes > 1 else ''} ago"
    elif seconds < 86400:
        hours = seconds // 3600
        return f"{hours} hour{'s' if hours > 1 else ''} ago"
    else:
        days = seconds // 86400
        return f"{days} day{'s' if days > 1 else ''} ago"
