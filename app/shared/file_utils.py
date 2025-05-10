"""
File management utilities for Telegram Insight Agent.
"""

import os
import logging
from typing import Optional, List

logger = logging.getLogger("telegram_insight_agent.file_utils")

def safe_remove_file(path: str) -> bool:
    """
    Remove a file if it exists. Logs errors.

    Args:
        path: File path to remove.

    Returns:
        True if file was removed, False if not found or error.
    """
    logger.debug(f"Attempting to remove file: {path}")
    try:
        if os.path.exists(path):
            os.remove(path)
            logger.info(f"Removed file: {path}")
            return True
        logger.info(f"File does not exist: {path}")
        return False
    except Exception as e:
        logger.error(f"Error removing file {path}: {e}")
        return False

def list_files_in_dir(directory: str, suffix: Optional[str] = None) -> List[str]:
    """
    List files in a directory, optionally filtered by suffix.

    Args:
        directory: Path to directory.
        suffix: Optional file suffix (e.g., '.txt').

    Returns:
        List of file paths.
    """
    logger.debug(f"Listing files in directory: {directory} (suffix={suffix})")
    try:
        files = [
            os.path.join(directory, f)
            for f in os.listdir(directory)
            if os.path.isfile(os.path.join(directory, f)) and (not suffix or f.endswith(suffix))
        ]
        logger.info(f"Found {len(files)} files in {directory}")
        return files
    except Exception as e:
        logger.error(f"Error listing files in {directory}: {e}")
        return []

# --- Pytest skeleton ---

"""
import tempfile
from app.shared.file_utils import safe_remove_file, list_files_in_dir

def test_safe_remove_file(tmp_path):
    file = tmp_path / "foo.txt"
    file.write_text("bar")
    assert safe_remove_file(str(file)) is True
    assert safe_remove_file(str(file)) is False

def test_list_files_in_dir(tmp_path):
    (tmp_path / "a.txt").write_text("a")
    (tmp_path / "b.txt").write_text("b")
    files = list_files_in_dir(str(tmp_path), suffix=".txt")
    assert len(files) == 2
"""