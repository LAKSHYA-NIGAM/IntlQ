"""
Logger Utility
Configured Python logger with file + console handlers.
"""

import logging
import os
import sys


def get_logger(name: str = "intlq", log_file: str = "intlq.log") -> logging.Logger:
    """Create a configured logger instance.
    
    Args:
        name: Logger name.
        log_file: Path to the log file.
    
    Returns:
        Configured logging.Logger.
    """
    logger = logging.getLogger(name)

    if logger.handlers:
        return logger  # Already configured

    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler
    try:
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    except OSError:
        logger.warning(f"Could not create log file: {log_file}")

    return logger
