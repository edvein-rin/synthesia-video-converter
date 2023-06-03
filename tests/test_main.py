import os

from src.cli.main import main

DATA_FOLDER_PATH = os.path.abspath(
    os.path.join(os.path.realpath(__file__), "../data")
)

TEST_VIDEO_FILE_NAMES = {
    # Simple and the most common situation
    1: "Marioverehrer | Sweden - Minecraft.mp4",
    # With sparkles
    2: "PianoDeuss | Naruto OST - The Raising Fighting Spirit.mp4",
    # With huge sparkles and small notes
    3: "Patrik Pietschmann | Harry Potter - Hedwig's Theme.mp4",
    # With static background below falling keys
    4: "Sergio Midi Piano | The Daydream I Miss You.mp4",
    # With big keys
    5: "Betacustic | Married Life.mp4",
    # With big keys and intro
    6: "PHianonize | Frank Sinatra - Fly Me To The Moon.mp4",
}
TEST_VIDEO_FILE_NAME = TEST_VIDEO_FILE_NAMES[1]

TEST_VIDEO_FILE_PATH = os.path.join(
    DATA_FOLDER_PATH, TEST_VIDEO_FILE_NAME
)


def test_main():
    main(TEST_VIDEO_FILE_PATH, True)
