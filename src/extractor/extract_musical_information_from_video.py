import os
import datetime

import cv2

from .process_frame import process_frame
from ..settings import Settings

settings = Settings()


def extract_musical_information_from_video(
    VIDEO_FILE_PATH: str,
) -> None:
    does_file_exist = os.path.isfile(VIDEO_FILE_PATH)

    if not does_file_exist:
        raise FileNotFoundError(
            f'File "{VIDEO_FILE_PATH}" doesn\'t exist.'
        )

    video_capture = cv2.VideoCapture(VIDEO_FILE_PATH)

    frames = video_capture.get(cv2.CAP_PROP_FRAME_COUNT)
    fps = video_capture.get(cv2.CAP_PROP_FPS)
    seconds = round(frames / fps)
    video_time = datetime.timedelta(seconds=seconds)

    wait_delay = int(fps) if settings.is_debug else 1

    if settings.is_debug:
        print(f"Frames: {frames}")
        print(f"FPS: {fps}")
        print(f"Video duration: {video_time} ({seconds} seconds)")

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
    while video_capture.isOpened():
        ret, frame = video_capture.read()

        has_stream_ended = not ret
        if has_stream_ended:
            print("Stream ended.")
            break

        process_frame(frame)

        if settings.is_debug and cv2.waitKey(wait_delay) == ord("q"):
            break

    video_capture.release()
    cv2.destroyAllWindows()
