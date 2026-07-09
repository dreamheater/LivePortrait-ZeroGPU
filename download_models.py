from pathlib import Path
from huggingface_hub import snapshot_download

from config import PRETRAINED_DIR, MODEL_REPOS


REQUIRED_FILES = [
    "liveportrait/base_models/appearance_feature_extractor.pth",
    "liveportrait/base_models/motion_extractor.pth",
    "liveportrait/base_models/spade_generator.pth",
    "liveportrait/base_models/warping_module.pth",
    "liveportrait/retargeting_models/stitching_retargeting_module.pth",
    "liveportrait/landmark.onnx",
    "insightface/models/buffalo_l/2d106det.onnx",
    "insightface/models/buffalo_l/det_10g.onnx",
]


def missing_model_files() -> list[Path]:
    missing = []
    for rel_path in REQUIRED_FILES:
        path = PRETRAINED_DIR / rel_path
        if not path.exists():
            missing.append(path)
    return missing


def models_ready() -> bool:
    return len(missing_model_files()) == 0


def download_models() -> Path:
    PRETRAINED_DIR.mkdir(parents=True, exist_ok=True)

    if models_ready():
        print("LivePortrait models already exist.")
        return PRETRAINED_DIR

    last_error = None

    for repo_id in MODEL_REPOS:
        try:
            print(f"Downloading LivePortrait models from {repo_id}...")
            snapshot_download(
                repo_id=repo_id,
                local_dir=str(PRETRAINED_DIR),
                local_dir_use_symlinks=False,
                ignore_patterns=[
                    ".git/*",
                    "*.md",
                    "docs/*",
                ],
            )

            if models_ready():
                print("LivePortrait models downloaded successfully.")
                return PRETRAINED_DIR

        except Exception as exc:
            last_error = exc
            print(f"Failed to download from {repo_id}: {exc}")

    missing = "\n".join(str(p) for p in missing_model_files())
    raise RuntimeError(
        "LivePortrait model download failed.\n\n"
        f"Missing files:\n{missing}\n\n"
        f"Last error:\n{last_error}"
    )


if __name__ == "__main__":
    download_models()
