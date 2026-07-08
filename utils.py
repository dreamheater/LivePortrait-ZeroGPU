"""
utils.py

Shared utility functions.
"""

from __future__ import annotations

import shutil
import tempfile
from pathlib import Path


def create_temp_dir(prefix: str = "lp_") -> Path:
    """Create a temporary working directory."""
    return Path(tempfile.mkdtemp(prefix=prefix))


def remove_dir(path: Path) -> None:
    """Delete a directory recursively."""
    if path.exists():
        shutil.rmtree(path, ignore_errors=True)


def ensure_dir(path: Path) -> Path:
    """Create a directory if it does not exist."""
    path.mkdir(parents=True, exist_ok=True)
    return path


def is_image(path: Path) -> bool:
    return path.suffix.lower() in {
        ".jpg",
        ".jpeg",
        ".png",
        ".webp",
    }


def is_video(path: Path) -> bool:
    return path.suffix.lower() in {
        ".mp4",
        ".mov",
        ".avi",
        ".mkv",
        ".webm",
    }
