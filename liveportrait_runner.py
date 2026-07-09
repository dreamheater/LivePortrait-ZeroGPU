from __future__ import annotations

import gc
import os
import sys
import time
import shutil
from pathlib import Path

import torch

from config import (
    LIVEPORTRAIT_DIR,
    OUTPUT_DIR,
    TEMP_DIR,
    DEFAULT_OPTIONS,
    OUTPUT_FILENAME,
)
from download_models import download_models


def _add_liveportrait_to_path() -> None:
    liveportrait_path = str(LIVEPORTRAIT_DIR)
    if liveportrait_path not in sys.path:
        sys.path.insert(0, liveportrait_path)


def _partial_fields(target_class, kwargs: dict):
    return target_class(**{k: v for k, v in kwargs.items() if hasattr(target_class, k)})


_pipeline = None


def load_pipeline():
    global _pipeline

    if _pipeline is not None:
        return _pipeline

    download_models()
    _add_liveportrait_to_path()

    from src.config.argument_config import ArgumentConfig
    from src.config.inference_config import InferenceConfig
    from src.config.crop_config import CropConfig
    from src.gradio_pipeline import GradioPipeline

    args = ArgumentConfig()
    for key, value in DEFAULT_OPTIONS.items():
        if hasattr(args, key):
            setattr(args, key, value)

    inference_cfg = _partial_fields(InferenceConfig, args.__dict__)
    crop_cfg = _partial_fields(CropConfig, args.__dict__)

    _pipeline = GradioPipeline(
        inference_cfg=inference_cfg,
        crop_cfg=crop_cfg,
        args=args,
    )

    return _pipeline


def clear_gpu_cache() -> None:
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        torch.cuda.ipc_collect()


def run_liveportrait(
    source_image_path: str | Path,
    driving_video_path: str | Path,
    output_dir: str | Path | None = None,
    progress=None,
) -> str:
    source_image_path = Path(source_image_path)
    driving_video_path = Path(driving_video_path)
    output_dir = Path(output_dir or OUTPUT_DIR)

    if not source_image_path.exists():
        raise FileNotFoundError(f"Source image not found: {source_image_path}")

    if not driving_video_path.exists():
        raise FileNotFoundError(f"Driving video not found: {driving_video_path}")

    output_dir.mkdir(parents=True, exist_ok=True)

    work_output_dir = output_dir / f"run_{int(time.time())}"
    work_output_dir.mkdir(parents=True, exist_ok=True)

    if progress:
        progress(0.05, desc="Loading LivePortrait models...")

    pipeline = load_pipeline()

    if progress:
        progress(0.25, desc="Running LivePortrait pipeline...")

    result = pipeline.execute_video(
        input_source_image_path=str(source_image_path),
        input_driving_video_path=str(driving_video_path),
        flag_normalize_lip=DEFAULT_OPTIONS["flag_normalize_lip"],
        flag_relative_input=DEFAULT_OPTIONS["flag_relative_motion"],
        flag_do_crop_input=DEFAULT_OPTIONS["flag_do_crop"],
        flag_remap_input=DEFAULT_OPTIONS["flag_pasteback"],
        flag_stitching_input=DEFAULT_OPTIONS["flag_stitching"],
        animation_region=DEFAULT_OPTIONS["animation_region"],
        driving_option_input=DEFAULT_OPTIONS["driving_option"],
        driving_multiplier=DEFAULT_OPTIONS["driving_multiplier"],
        flag_crop_driving_video_input=DEFAULT_OPTIONS["flag_crop_driving_video"],
        scale=DEFAULT_OPTIONS["scale"],
        vx_ratio=DEFAULT_OPTIONS["vx_ratio"],
        vy_ratio=DEFAULT_OPTIONS["vy_ratio"],
        scale_crop_driving_video=DEFAULT_OPTIONS["scale_crop_driving_video"],
        vx_ratio_crop_driving_video=DEFAULT_OPTIONS["vx_ratio_crop_driving_video"],
        vy_ratio_crop_driving_video=DEFAULT_OPTIONS["vy_ratio_crop_driving_video"],
        driving_smooth_observation_variance=DEFAULT_OPTIONS[
            "driving_smooth_observation_variance"
        ],
        tab_selection="Image",
        v_tab_selection="Video",
    )

    if progress:
        progress(0.9, desc="Collecting output...")

    output_path = None

    if isinstance(result, tuple):
        for item in result:
            if isinstance(item, str) and item.endswith(".mp4") and Path(item).exists():
                output_path = Path(item)
                break
    elif isinstance(result, str) and result.endswith(".mp4") and Path(result).exists():
        output_path = Path(result)

    if output_path is None:
        mp4_files = sorted(
            OUTPUT_DIR.rglob("*.mp4"),
            key=lambda p: p.stat().st_mtime,
            reverse=True,
        )
        if mp4_files:
            output_path = mp4_files[0]

    if output_path is None or not output_path.exists():
        raise RuntimeError("LivePortrait did not produce an output mp4.")

    final_output = output_dir / OUTPUT_FILENAME
    shutil.copy2(output_path, final_output)

    if progress:
        progress(1.0, desc="Done")

    return str(final_output)
