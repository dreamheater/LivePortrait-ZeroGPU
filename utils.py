"""
utils.py

Shared utility functions for LivePortrait-ZeroGPU.
"""

from __future__ import annotations

import shutil
import tempfile
from pathlib import Path
from typing import Iterable


IMAGE_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp",
    ".webp",
}

VIDEO_EXTENSIONS = {
    ".mp4",
    ".mov",
    ".avi",
    ".mkv",
    ".webm",
}


def ensure_directory(path: Path) -> Path:
    """Create directory if it doesn't exist."""
    path.mkdir(parents=True, exist_ok=True)
    return path


def create_temp_workspace(prefix: str = "lp_") -> Path:
    """Create a temporary workspace."""
    return Path(tempfile.mkdtemp(prefix=prefix))


def cleanup_workspace(path: Path) -> None:
    """Remove temporary workspace."""
    if path.exists():
        shutil.rmtree(path, ignore_errors=True)


def copy_file(src: Path, dst: Path) -> Path:
    """Copy file preserving metadata."""
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    return dst


def find_first_file(directory: Path, extensions: Iterable[str]) -> Path | None:
    """Return first matching file."""
    for ext in extensions:
        matches = sorted(directory.glob(f"*{ext}"))
        if matches:
            return matches[0]
    return None


def is_image(path: Path) -> bool:
    return path.suffix.lower() in IMAGE_EXTENSIONS


def is_video(path: Path) -> bool:
    return path.suffix.lower() in VIDEO_EXTENSIONS
