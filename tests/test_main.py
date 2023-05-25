import os

from src.cli.main import main

DATA_FOLDER_PATH = os.path.abspath(
    os.path.join(os.path.realpath(__file__), "../data")
)

TEST_VIDEO_FILE_NAMES = (
    "Marioverehrer | Sweden - Minecraft.mp4",  # Simple one
    "PianoDeuss | Naruto OST - The Raising Fighting Spirit.mp4",  # With sparkles
    (  # With huge sparkles and small notes
        "Patrik Pietschmann | Harry Potter - Hedwig's Theme.mp4"
    ),
    (  # With static background below falling keys
        "Sergio Midi Piano | The Daydream I Miss You.mp4"
    ),
)
TEST_VIDEO_FILE_NAME = TEST_VIDEO_FILE_NAMES[0]

TEST_VIDEO_FILE_PATH = os.path.join(
    DATA_FOLDER_PATH, TEST_VIDEO_FILE_NAME
)


def test_main():
    main(TEST_VIDEO_FILE_PATH, True)
