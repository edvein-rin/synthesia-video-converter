import os

from src.converter.midi_to_sheet_music_pdf import (
    midi_to_sheet_music_pdf,
)

DATA_FOLDER_PATH = os.path.abspath(
    os.path.join(os.path.realpath(__file__), "../data")
)

TEST_MIDI_FILE_PATH = os.path.join(
    DATA_FOLDER_PATH, "Marioverehrer | Sweden - Minecraft.midi"
)

TEST_SHEET_MUSIC_FILE_PATH = os.path.join(
    DATA_FOLDER_PATH, "Marioverehrer | Sweden - Minecraft.pdf"
)


def test_midi_to_sheet_music_pdf():
    midi_to_sheet_music_pdf(
        TEST_MIDI_FILE_PATH,
        os.path.join(DATA_FOLDER_PATH, TEST_SHEET_MUSIC_FILE_PATH),
    )
