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

    if settings.is_debug:
        print(f"Average white key width: {average_white_key_width}")
        print(f"Average black key width: {average_black_key_width}")

    # TODO
    # For video 2 perfect parameters should be:
    # inner_offset, white_key_width = (14, 25)
    inner_offset, white_key_width = (
        __detect_inner_offset_and_white_key_width(
            falling_rectangles,
            average_white_key_width,
        )
    )

    if settings.is_debug:
        print(f"Inner offset: {inner_offset}")
        print(f"White key width: {white_key_width}")

    # TODO calculate it? Actually white key size can be used as it covers
    # full area between black keys
    black_key_width = average_black_key_width

    return Keyboard(
        video_width,
        white_key_width,
        black_key_width,
        inner_offset,
        play_line,
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

    count_mean = key_widths_value_counts.mean()

    mean_key_widths_value_counts = pd.Series()
    for key_width, count in key_widths_value_counts.items():
        if count >= count_mean:
            mean_key_widths_value_counts[key_width] = count

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

    average_white_key_width = None
    average_black_key_width = None

    mean_key_widths = np.sort(
        mean_key_widths_value_counts.index.to_numpy()
    )

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

    return average_black_key_width, average_white_key_width


def __get_white_rectangles_from_falling_rectangles(
    falling_rectangles: [FallingRectangle],
    average_white_key_width: float,
) -> [FallingRectangle]:
    filtered_falling_rectangles = []

    for falling_rectangle in falling_rectangles:
        if (
            falling_rectangle.width <= average_white_key_width * 1.25
            and falling_rectangle.width
            >= average_white_key_width * 0.75
        ):
            filtered_falling_rectangles.append(falling_rectangle)

    return filtered_falling_rectangles


def __detect_inner_offset_and_white_key_width(
    falling_rectangles: [FallingRectangle],
    average_white_key_width: float,
) -> tuple[float, float]:
    """
    Calculates inner_offset and white key width.

    Conditions that should match:
    1) 0 <= inner_offset <= white_key_width
    2) average_white_key_width <= white_key_width <=
    <= average_white_key_width * C,
    where C = 1.5

    And for each rectangle in a testing group (rec):
    1) inner_offset + n * white_key_width <= rectangle.x <=
    <= inner_offset + (n + 1) * white_key_width
    2) inner_offset + n * white_key_width <= rec.right_x <=
    <= inner_offset + (n + 1) * white_key_width
    """

    # TODO refactor

    NUMBER_OF_WHITE_KEYS = 52

    white_rectangles = __get_white_rectangles_from_falling_rectangles(
        falling_rectangles, average_white_key_width
    )

    MAX_NUMBER_OF_DIFFERENT_WHITE_FALLING_RECTANGLES = (
        NUMBER_OF_WHITE_KEYS - 1
    )

    different_white_falling_rectangles: [FallingRectangle] = []
    for white_rectangle in white_rectangles:
        if (
            len(different_white_falling_rectangles)
            >= MAX_NUMBER_OF_DIFFERENT_WHITE_FALLING_RECTANGLES
        ):
            break

        if len(different_white_falling_rectangles) == 1:
            different_white_falling_rectangles.append(white_rectangle)
            continue

        if all(
            [
                white_rectangle.x
                + white_rectangle.width
                - (
                    different_white_falling_rectangle.x
                    + different_white_falling_rectangle.width
                )
                >= average_white_key_width
                for different_white_falling_rectangle in different_white_falling_rectangles
            ]
        ):
            different_white_falling_rectangles.append(white_rectangle)

    white_key_width = None
    inner_offset = None
    max_fitted_falling_rectangles = 0

    MAYBE_WHITE_KEY_PARAMETER = 1.5
    MAYBE_WHITE_KEY_STEP = 0.1
    MAYBE_INNER_OFFSET_STEP = 0.1

    for maybe_white_key_width in np.arange(
        average_white_key_width,
        average_white_key_width * MAYBE_WHITE_KEY_PARAMETER,
        MAYBE_WHITE_KEY_STEP,
    ):
        for maybe_inner_offset in np.arange(
            0, maybe_white_key_width, MAYBE_INNER_OFFSET_STEP
        ):
            number_of_fitted_falling_rectangles = 0

            for (
                different_white_falling_rectangle
            ) in different_white_falling_rectangles:
                for n in range(NUMBER_OF_WHITE_KEYS):
                    if (
                        maybe_inner_offset + n * maybe_white_key_width
                        <= different_white_falling_rectangle.x
                        and different_white_falling_rectangle.x
                        <= maybe_inner_offset
                        + (n + 1) * maybe_white_key_width
                        and maybe_inner_offset
                        + n * maybe_white_key_width
                        <= different_white_falling_rectangle.right_x
                        and different_white_falling_rectangle.right_x
                        <= maybe_inner_offset
                        + (n + 1) * maybe_white_key_width
                    ):
                        number_of_fitted_falling_rectangles += 1
                        break
                    else:
                        continue

            if (
                number_of_fitted_falling_rectangles
                >= max_fitted_falling_rectangles
            ):
                if (
                    number_of_fitted_falling_rectangles
                    > max_fitted_falling_rectangles
                ):
                    # print(
                    #     inner_offset,
                    #     white_key_width,
                    #     number_of_fitted_falling_rectangles,
                    # )
                    inner_offset = maybe_inner_offset
                    white_key_width = maybe_white_key_width
                    max_fitted_falling_rectangles = (
                        number_of_fitted_falling_rectangles
                    )
                elif (
                    inner_offset is None
                    or maybe_inner_offset < inner_offset
                ):
                    # print(
                    #     inner_offset,
                    #     white_key_width,
                    #     number_of_fitted_falling_rectangles,
                    #     maybe_inner_offset,
                    #     maybe_white_key_width,
                    # )
                    inner_offset = maybe_inner_offset
                    white_key_width = maybe_white_key_width

    if white_key_width is None:
        white_key_width = average_white_key_width
    if inner_offset is None:
        inner_offset = 0

    return inner_offset, white_key_width
