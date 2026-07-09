from pathlib import Path
import os

ROOT = Path(__file__).resolve().parent

VENDOR_DIR = ROOT / "vendor"
LIVEPORTRAIT_DIR = VENDOR_DIR / "LivePortrait"

OUTPUT_DIR = ROOT / "outputs"
TEMP_DIR = ROOT / "temp"

OUTPUT_DIR.mkdir(exist_ok=True)
TEMP_DIR.mkdir(exist_ok=True)

MODEL_DIR = LIVEPORTRAIT_DIR / "pretrained_weights"

DEVICE = "cuda"

DEFAULT_ARGS = {

    "flag_do_crop": True,
    "flag_pasteback": True,
    "flag_stitching": True,
    "flag_relative_motion": True,
    "flag_crop_driving_video": True,

    "animation_region": "all",

    "driving_option": "pose-friendly",

    "driving_multiplier": 1.0,

    "scale": 2.3,
    "vx_ratio": 0.0,
    "vy_ratio": -0.125,

    "scale_crop_driving_video": 2.2,
    "vx_ratio_crop_driving_video": 0.0,
    "vy_ratio_crop_driving_video": -0.10,

    "driving_smooth_observation_variance": 3e-7,
}
