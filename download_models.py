from pathlib import Path

MODEL_FILES = [

    "liveportrait/base_models/appearance_feature_extractor.pth",

    "liveportrait/base_models/motion_extractor.pth",

    "liveportrait/base_models/spade_generator.pth",

    "liveportrait/base_models/warping_module.pth",

    "liveportrait/retargeting_models/stitching_retargeting_module.pth",
]


def check_models(root):

    root = Path(root)

    missing = []

    for model in MODEL_FILES:

        f = root / model

        if not f.exists():

            missing.append(str(f))

    return missing
