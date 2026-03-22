"""
Logging Utilities for Sea Cox V2
================================
Helper functions for setting up and managing the logging infrastructure.
Ensures log directories exist and provides convenience functions for
obtaining configured loggers throughout the application.
"""

import os
import logging
from pathlib import Path
from typing import Optional
from django.conf import settings


def ensure_log_directory():
    """
    Create the log directory (and any parent directories) if they don't exist.
    
    This function is called automatically during Django startup via the
    LOGGING configuration in settings.py. It can also be called manually
    if needed (e.g., in management commands or scripts).
    
    Returns:
        Path: The absolute path to the log directory.
    """
    log_dir = getattr(settings, 'LOG_DIR', Path(settings.BASE_DIR) / 'logs')
    log_dir = Path(log_dir)

    try:
        log_dir.mkdir(parents=True, exist_ok=True)
        # Ensure proper permissions (owner read/write/execute)
        if os.name != 'nt':  # Skip on Windows
            os.chmod(log_dir, 0o755)
    except OSError as e:
        # Fall back to stderr if we can't create the log directory
        import sys
        print(
            f"WARNING: Could not create log directory '{log_dir}': {e}",
            file=sys.stderr,
        )

    return log_dir


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """
    Get a configured logger instance.
    
    Usage:
        from core.logging_utils import get_logger
        logger = get_logger(__name__)
        
        logger.info("Something happened")
        logger.error("Something went wrong", exc_info=True)
    
    Args:
        name: The logger name. Typically pass __name__ to use the module path.
              If None, returns the root logger.
    
    Returns:
        logging.Logger: A configured logger instance.
    """
    return logging.getLogger(name)


def log_exception(logger: logging.Logger, message: str, exc: Optional[Exception] = None):
    """
    Log an exception with full traceback.
    
    Args:
        logger: The logger instance to use.
        message: A human-readable description of the error context.
        exc: The exception instance (optional, can also use exc_info=True).
    """
    if exc:
        logger.exception(f"{message}: {exc}")
    else:
        logger.exception(message)
