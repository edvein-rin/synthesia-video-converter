import os

from ..extractor import extract_musical_information_from_video

ROOT_FOLDER_PATH = os.path.abspath(
    os.path.join(os.path.realpath(__file__), "../../../")
)

VIDEO_FILE_NAMES = (
    "Marioverehrer | Sweden - Minecraft.mp4",  # Simple one
    "PianoDeuss | Naruto OST - The Raising Fighting Spirit.mp4",  # With sparkles
    (  # With huge sparkles and small notes
        "Patrik Pietschmann | Harry Potter - Hedwig's Theme.mp4"
    ),
    (  # With static background below falling keys
        "Sergio Midi Piano | The Daydream I Miss You.mp4"
    ),
)
VIDEO_FILE_NAME = VIDEO_FILE_NAMES[1]

VIDEO_FILE_PATH = os.path.join(
    ROOT_FOLDER_PATH, "tests/data/" + VIDEO_FILE_NAME
)


def main() -> None:
    extract_musical_information_from_video(VIDEO_FILE_PATH)
