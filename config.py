from pathlib import Path
import os

ROOT_DIR = Path(__file__).resolve().parent

VENDOR_DIR = ROOT_DIR / "vendor"
LIVEPORTRAIT_DIR = VENDOR_DIR / "LivePortrait"
PRETRAINED_DIR = LIVEPORTRAIT_DIR / "pretrained_weights"

OUTPUT_DIR = ROOT_DIR / "outputs"
TEMP_DIR = ROOT_DIR / "temp"
LOG_DIR = ROOT_DIR / "logs"

for d in [OUTPUT_DIR, TEMP_DIR, LOG_DIR]:
    d.mkdir(parents=True, exist_ok=True)

PROJECT_NAME = "LivePortrait-ZeroGPU"
PROJECT_VERSION = "1.0.0-alpha"

MODEL_REPOS = [
    os.getenv("LIVEPORTRAIT_MODEL_REPO", "KlingTeam/LivePortrait"),
    "KwaiVGI/LivePortrait",
]

OUTPUT_FILENAME = "liveportrait_result.mp4"

DEFAULT_DEVICE_ID = int(os.getenv("DEVICE_ID", "0"))
FORCE_CPU = os.getenv("FORCE_CPU", "0") == "1"

USE_HALF_PRECISION = os.getenv("USE_HALF_PRECISION", "1") == "1"

DEFAULT_OPTIONS = {
    "flag_use_half_precision": USE_HALF_PRECISION,
    "flag_crop_driving_video": True,
    "flag_force_cpu": FORCE_CPU,
    "device_id": DEFAULT_DEVICE_ID,
    "flag_normalize_lip": False,
    "flag_stitching": True,
    "flag_relative_motion": True,
    "flag_pasteback": True,
    "flag_do_crop": True,
    "driving_option": "pose-friendly",
    "driving_multiplier": 1.0,
    "animation_region": "all",
    "scale": 2.3,
    "vx_ratio": 0.0,
    "vy_ratio": -0.125,
    "scale_crop_driving_video": 2.2,
    "vx_ratio_crop_driving_video": 0.0,
    "vy_ratio_crop_driving_video": -0.1,
    "driving_smooth_observation_variance": 3e-7,
}
