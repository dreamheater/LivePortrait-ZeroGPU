from __future__ import annotations

import shutil
from pathlib import Path

import gradio as gr

try:
    import spaces
except Exception:
    class spaces:
        @staticmethod
        def GPU(func=None, **kwargs):
            if func is None:
                def wrapper(f):
                    return f
                return wrapper
            return func

from config import TEMP_DIR, OUTPUT_DIR
from liveportrait_runner import run_liveportrait, clear_gpu_cache


def prepare_file(src: str, dst: Path) -> Path:
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    return dst


@spaces.GPU
def generate(source_image, driving_video, progress=gr.Progress()):
    if source_image is None:
        raise gr.Error("請上傳人像圖片。")

    if driving_video is None:
        raise gr.Error("請上傳驅動影片。")

    work_dir = TEMP_DIR / "current"
    if work_dir.exists():
        shutil.rmtree(work_dir, ignore_errors=True)
    work_dir.mkdir(parents=True, exist_ok=True)

    source_path = prepare_file(source_image, work_dir / "source.png")
    driving_path = prepare_file(driving_video, work_dir / "driving.mp4")

    try:
        result = run_liveportrait(
            source_image_path=source_path,
            driving_video_path=driving_path,
            output_dir=OUTPUT_DIR,
            progress=progress,
        )
        return result

    except Exception as exc:
        raise gr.Error(f"產生失敗：{exc}")

    finally:
        clear_gpu_cache()


with gr.Blocks(title="LivePortrait ZeroGPU") as demo:
    gr.Markdown(
        """
# 🎭 LivePortrait ZeroGPU

上傳一張人像照片與一段驅動影片，產生 LivePortrait 動態影片。
"""
    )

    with gr.Row():
        source_image = gr.Image(
            label="人像圖片",
            type="filepath",
        )

        driving_video = gr.Video(
            label="驅動影片",
        )

    generate_btn = gr.Button(
        "Generate",
        variant="primary",
    )

    output_video = gr.Video(
        label="產生結果",
    )

    generate_btn.click(
        fn=generate,
        inputs=[source_image, driving_video],
        outputs=output_video,
    )

demo.queue(max_size=5)

if __name__ == "__main__":
    demo.launch()
