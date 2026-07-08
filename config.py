"""
config.py
==========

Global configuration for LivePortrait-ZeroGPU.

Author:
    dreamheater

Version:
    v1.0.0-alpha

This file contains only project-level configuration.
Do NOT modify vendor/LivePortrait here.
"""

from pathlib import Path
import os
import torch


# ---------------------------------------------------------
# Project
# ---------------------------------------------------------

PROJECT_NAME = "LivePortrait-ZeroGPU"
PROJECT_VERSION = "1.0.0-alpha"

ROOT_DIR = Path(__file__).resolve().parent


# ---------------------------------------------------------
# Vendor
# ---------------------------------------------------------

VENDOR_DIR = ROOT_DIR / "vendor"
LIVEPORTRAIT_DIR = VENDOR_DIR / "LivePortrait"


# ---------------------------------------------------------
# Runtime directories
# ---------------------------------------------------------

ASSETS_DIR = ROOT_DIR / "assets"
TEMP_DIR = ROOT_DIR / "temp"
OUTPUT_DIR = ROOT_DIR / "outputs"
LOG_DIR = ROOT_DIR / "logs"

for directory in (
    ASSETS_DIR,
    TEMP_DIR,
    OUTPUT_DIR,
    LOG_DIR,
):
    directory.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------
# LivePortrait
# ---------------------------------------------------------

PRETRAINED_DIR = LIVEPORTRAIT_DIR / "pretrained_weights"

SOURCE_IMAGE_NAME = "source.png"
DRIVING_VIDEO_NAME = "driving.mp4"


# ---------------------------------------------------------
# Device
# ---------------------------------------------------------

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

USE_FP16 = DEVICE == "cuda"


# ---------------------------------------------------------
# Inference
# ---------------------------------------------------------

MAX_IMAGE_SIZE = 4096

MAX_VIDEO_SECONDS = 30

DEFAULT_SEED = 42


# ---------------------------------------------------------
# Logging
# ---------------------------------------------------------

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")


# ---------------------------------------------------------
# Hugging Face
# ---------------------------------------------------------

IS_SPACE = os.getenv("SPACE_ID") is not None

HF_HOME = os.getenv("HF_HOME")

HF_TOKEN = os.getenv("HF_TOKEN")


# ---------------------------------------------------------
# Validation
# ---------------------------------------------------------

if not LIVEPORTRAIT_DIR.exists():
    raise FileNotFoundError(
        f"LivePortrait not found:\n{LIVEPORTRAIT_DIR}"
    )

# Runtime

MAX_IMAGE_SIZE_MB = 20
MAX_VIDEO_SIZE_MB = 100

# Output

OUTPUT_FILENAME = "output.mp4"
