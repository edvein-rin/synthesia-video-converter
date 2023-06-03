import os
import datetime

import cv2

from ..settings import Settings
from ..converter import falling_key_to_note

from .detect_keyboard import detect_keyboard
from .detect_falling_keys import detect_falling_keys
from .detect_play_line import detect_play_line
from .merge_falling_keys import merge_falling_keys

settings = Settings()


def extract_musical_information_from_video(
    video_file_path: str,
) -> None:
    does_file_exist = os.path.isfile(video_file_path)

    if not does_file_exist:
        raise FileNotFoundError(
            f'File "{video_file_path}" doesn\'t exist.'
        )

    video_capture = cv2.VideoCapture(video_file_path)

    frames = video_capture.get(cv2.CAP_PROP_FRAME_COUNT)
    fps = video_capture.get(cv2.CAP_PROP_FPS)
    seconds = round(frames / fps)
    video_time = datetime.timedelta(seconds=seconds)

    if settings.debug_wait_delay is None:
        settings.debug_wait_delay = int(fps)

    if settings.is_debug:
        print("\n")
        print(f"Frames: {frames}")
        print(f"FPS: {fps}")
        print(f"Video duration: {video_time} ({seconds} seconds)\n")

    # TODO several video loops
    #
    # First one:
    # 1. Detecting keyboard position and by this defining play line.
    # 2. Defining white and black keys size.
    #
    # Second one:
    # 1. Detecting irrelevant parts of the video (intro, outro) by
    # not having a keyboard in the frame.
    #
    # Third one:
    # 1. Detecting static image background under falling keys (looking
    # for an average image) during the relevant part of the video (play part).
    #
    # Forth one:
    # 1. Detecting actual falling keys.

    play_line = detect_play_line(
        video_capture,
        settings.default_play_line_relative_position_to_top,
    )

    video_capture.open(video_file_path)
    keyboard = detect_keyboard(video_capture, play_line)

    if settings.is_debug:
        print(keyboard)

    video_capture.open(video_file_path)
    falling_keys = detect_falling_keys(video_capture, keyboard)

    if settings.is_debug:
        # print(f"{falling_keys=}")
        print(f"Number of falling keys: {len(falling_keys)}")

    merged_falling_keys = merge_falling_keys(falling_keys)

    if settings.is_debug:
        # print(f"{merged_falling_keys=}")
        print(
            "Number of falling keys after merge:"
            f" {len(merged_falling_keys)}"
        )

    notes = list(
        map(
            lambda falling_key: falling_key_to_note(falling_key),
            merged_falling_keys,
        )
    )

    if settings.is_debug:
        # print(f"{notes}")
        print(f"Number of notes = {len(notes)}")

    cv2.destroyAllWindows()
