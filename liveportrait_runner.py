from __future__ import annotations

import gc
import sys
import time
import shutil
from pathlib import Path

import torch

from config import LIVEPORTRAIT_DIR, OUTPUT_DIR, DEFAULT_OPTIONS, OUTPUT_FILENAME
from download_models import download_models


def _add_vendor_path():
    p = str(LIVEPORTRAIT_DIR)
    if p not in sys.path:
        sys.path.insert(0, p)


def _partial_fields(target_class, kwargs: dict):
    return target_class(**{k: v for k, v in kwargs.items() if hasattr(target_class, k)})


def clear_gpu_cache():
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        torch.cuda.ipc_collect()


def run_liveportrait(source_image_path, driving_video_path, output_dir=None, progress=None) -> str:
    source_image_path = Path(source_image_path)
    driving_video_path = Path(driving_video_path)
    output_dir = Path(output_dir or OUTPUT_DIR)
    output_dir.mkdir(parents=True, exist_ok=True)

    if not source_image_path.exists():
        raise FileNotFoundError(f"Source image not found: {source_image_path}")

    if not driving_video_path.exists():
        raise FileNotFoundError(f"Driving video not found: {driving_video_path}")

    if progress:
        progress(0.05, desc="Checking models...")

    download_models()
    _add_vendor_path()

    from src.config.argument_config import ArgumentConfig
    from src.config.inference_config import InferenceConfig
    from src.config.crop_config import CropConfig
    from src.live_portrait_pipeline import LivePortraitPipeline

    run_dir = output_dir / f"run_{int(time.time())}"
    run_dir.mkdir(parents=True, exist_ok=True)

    args = ArgumentConfig()
    args.source = str(source_image_path)
    args.driving = str(driving_video_path)
    args.output_dir = str(run_dir)

    for k, v in DEFAULT_OPTIONS.items():
        if hasattr(args, k):
            setattr(args, k, v)

    inference_cfg = _partial_fields(InferenceConfig, args.__dict__)
    crop_cfg = _partial_fields(CropConfig, args.__dict__)

    if progress:
        progress(0.25, desc="Loading LivePortrait...")

    pipeline = LivePortraitPipeline(
        inference_cfg=inference_cfg,
        crop_cfg=crop_cfg,
    )

    if progress:
        progress(0.45, desc="Generating video...")

    pipeline.execute(args)

    mp4_files = sorted(
        run_dir.rglob("*.mp4"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )

    if not mp4_files:
        mp4_files = sorted(
            output_dir.rglob("*.mp4"),
            key=lambda p: p.stat().st_mtime,
            reverse=True,
        )

    if not mp4_files:
        raise RuntimeError("LivePortrait did not generate an mp4 file.")

    final_output = output_dir / OUTPUT_FILENAME
    shutil.copy2(mp4_files[0], final_output)

    if progress:
        progress(1.0, desc="Done")

    clear_gpu_cache()
    return str(final_output)
