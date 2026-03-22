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


def get_safe_log_directory(base_dir: Path) -> Path:
    """
    Safely create and return a writable log directory.
    Falls back to /tmp/logs if the primary directory is not writable.
    
    Args:
        base_dir: The Django BASE_DIR path to use as the primary location.
        
    Returns:
        Path: The absolute path to a writable log directory.
    """
    primary_dir = base_dir / 'logs'
    fallback_dir = Path('/tmp/logs')
    
    for current_dir in [primary_dir, fallback_dir]:
        try:
            current_dir.mkdir(parents=True, exist_ok=True)
            # Ensure proper permissions (owner read/write/execute)
            if os.name != 'nt':  # Skip on Windows
                os.chmod(current_dir, 0o755)
                
            # Test write access by creating a temporary file
            test_file = current_dir / '.write_test'
            test_file.touch()
            test_file.unlink()
            
            return current_dir
        except (OSError, PermissionError) as e:
            import sys
            print(
                f"WARNING: Cannot use log directory '{current_dir}': {e}",
                file=sys.stderr,
            )
            continue
            
    # Absolute last resort fallback (should rarely happen)
    return Path('/tmp')


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
