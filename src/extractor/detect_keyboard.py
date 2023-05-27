import cv2
import numpy as np
import pandas as pd


from ..settings import Settings
from ..entities import Keyboard, PlayLine, FallingRectangle

from .frame_helpers import (
    prepare_frame_for_analysis,
    find_frame_contours,
    frame_contours_to_falling_rectangles,
)

settings = Settings()


def detect_keyboard(video_capture, play_line: PlayLine) -> Keyboard:
    falling_rectangles: [FallingRectangle] = []

    video_width = video_capture.get(cv2.CAP_PROP_FRAME_WIDTH)

    video_capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
    while video_capture.isOpened():
        retrieve, frame = video_capture.read()

        has_stream_ended = not retrieve
        if has_stream_ended:
            break

        falling_rectangles += __extract_falling_rectangles_from_frame(
            frame, play_line
        )
    video_capture.release()

    key_widths = [
        falling_rectangle.width
        for falling_rectangle in falling_rectangles
    ]

    average_black_key_width, average_white_key_width = (
        __find_average_black_and_white_keys_width(
            np.array(key_widths)
        )
    )

    # TODO detect
    number_of_white_keys = (
        52
        if average_white_key_width > 20
        and average_white_key_width < 26
        else None
    )

    white_key_x_offset = 0
    black_key_x_offset = 0

    white_key_width = (
        average_white_key_width
        if number_of_white_keys is None
        else video_width / number_of_white_keys
    )

    return Keyboard(
        video_width,
        number_of_white_keys,
        white_key_width,
        average_black_key_width,
        play_line,
        white_key_x_offset,
        black_key_x_offset,
    )


def __extract_falling_rectangles_from_frame(
    frame, play_line: PlayLine
) -> [FallingRectangle]:
    prepared_for_analysis_frame = prepare_frame_for_analysis(frame)
    prepared_for_analysis_frame_line = prepared_for_analysis_frame[
        play_line.y : play_line.y + 1
    ]

    frame_contours = find_frame_contours(
        prepared_for_analysis_frame_line
    )
    falling_rectangles = frame_contours_to_falling_rectangles(
        frame_contours, play_line.y
    )

    return falling_rectangles


def __find_average_black_and_white_keys_width(
    key_widths: np.array,
) -> tuple[int, int]:
    # TODO automatically detect too big keys
    filtered_key_widths = filter(
        lambda key_width: key_width < 200, key_widths
    )

    key_widths_series = pd.Series(filtered_key_widths)
    key_widths_value_counts = (
        key_widths_series.value_counts().sort_index()
    )

    if settings.is_debug:
        print("Key widths value counts:")
        print(key_widths_value_counts)

    count_mean = key_widths_value_counts.mean()

    if settings.is_debug:
        print("Count mean: ", count_mean)

    mean_key_widths_value_counts = pd.Series()
    for key_width, count in key_widths_value_counts.items():
        if count >= count_mean:
            mean_key_widths_value_counts[key_width] = count

    if settings.is_debug:
        print("Mean key widths value counts:")
        print(mean_key_widths_value_counts)

    for key_width_a, count_a in mean_key_widths_value_counts.items():
        for (
            key_width_b,
            count_b,
        ) in mean_key_widths_value_counts.items():
            if (
                key_width_a + 1 == key_width_b
                or key_width_a + 1 == key_width_b
            ):
                try:
                    if count_a > count_b:
                        mean_key_widths_value_counts = (
                            mean_key_widths_value_counts.drop(
                                key_width_b
                            )
                        )
                    else:
                        mean_key_widths_value_counts = (
                            mean_key_widths_value_counts.drop(
                                key_width_a
                            )
                        )
                except KeyError:
                    pass

    if settings.is_debug:
        print(mean_key_widths_value_counts)

    average_white_key_width = None
    average_black_key_width = None

    mean_key_widths = np.sort(
        mean_key_widths_value_counts.index.to_numpy()
    )

    if settings.is_debug:
        print(mean_key_widths)

    average_white_key_width = (
        mean_key_widths[-1]
        if -len(mean_key_widths) <= -1 < len(mean_key_widths)
        else float("inf")
    )
    average_black_key_width = (
        mean_key_widths[-2]
        if -len(mean_key_widths) <= -2 < len(mean_key_widths)
        else float("inf")
    )

    if settings.is_debug:
        print(average_white_key_width, average_black_key_width)

    return average_black_key_width, average_white_key_width
