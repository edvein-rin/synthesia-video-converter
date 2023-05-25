import cv2
import numpy as np
import pandas as pd


from ..entities import Keyboard, PlayLine

from .frame_helpers import (
    prepare_frame_for_analysis,
    find_frame_contours,
    frame_contours_to_falling_rectangles,
)


def detect_keyboard(video_capture, play_line: PlayLine) -> Keyboard:
    key_widths = []

    video_capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
    while video_capture.isOpened():
        retrieve, frame = video_capture.read()

        has_stream_ended = not retrieve
        if has_stream_ended:
            break

        key_widths += __extract_key_widths_from_frame(
            frame, play_line
        )
    video_capture.release()

    average_black_key_width, average_white_key_width = (
        __find_average_black_and_white_keys_width(
            np.array(key_widths)
        )
    )

    return Keyboard(
        average_white_key_width, average_black_key_width, play_line
    )


def __extract_key_widths_from_frame(
    frame, play_line: PlayLine
) -> [float]:
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

    key_widths = [
        falling_rectangle.width
        for falling_rectangle in falling_rectangles
    ]

    return key_widths


def __find_average_black_and_white_keys_width(
    key_widths: np.array,
) -> tuple[int, int]:
    key_widths_series = pd.Series(key_widths)
    key_widths_value_counts = (
        key_widths_series.value_counts().sort_index()
    )
    print("Key widths value counts:")
    print(key_widths_value_counts)

    count_mean = key_widths_value_counts.mean()
    print("Count mean: ", count_mean)

    mean_key_widths_value_counts = pd.Series()
    for key_width, count in key_widths_value_counts.items():
        if count >= count_mean:
            mean_key_widths_value_counts[key_width] = count
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
                if count_a > count_b:
                    del mean_key_widths_value_counts[key_width_b]
                else:
                    del mean_key_widths_value_counts[key_width_a]
    print(mean_key_widths_value_counts)

    average_white_key_width = None
    average_black_key_width = None

    mean_key_widths = np.sort(
        mean_key_widths_value_counts.index.to_numpy()
    )
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
    print(average_white_key_width, average_black_key_width)

    return average_black_key_width, average_white_key_width
