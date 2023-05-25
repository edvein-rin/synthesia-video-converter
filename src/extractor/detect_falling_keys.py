import cv2

from ..settings import Settings
from ..entities import Keyboard, FallingRectangle
from .. import debugger

from .frame_helpers import (
    blur_frame,
    cut_frame_vertically,
    find_frame_contours,
    frame_contours_to_falling_rectangles,
    grayscale_frame,
    increase_frame_contrast,
    perform_morphological_open_with_frame,
    threshold_frame,
)

settings = Settings()


def detect_falling_keys(
    video_capture,
    keyboard: Keyboard,
    wait_delay: int,
):
    falling_keys = []

    video_capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
    while video_capture.isOpened():
        retrieve, frame = video_capture.read()

        has_stream_ended = not retrieve
        if has_stream_ended:
            break

        frame_number = video_capture.get(cv2.CAP_PROP_POS_FRAMES)
        fps = video_capture.get(cv2.CAP_PROP_FPS)
        frame_time = frame_number / fps

        falling_rectangles = __extract_falling_rectangles_from_frame(
            frame, keyboard, frame_number, wait_delay
        )

        falling_keys.append(
            __convert_falling_rectangles_to_falling_keys(
                falling_rectangles, keyboard, frame_time
            )
        )

        if settings.is_debug and cv2.waitKey(wait_delay) == ord("q"):
            break
    video_capture.release()

    # TODO combine close falling_keys

    return falling_keys


def __extract_falling_rectangles_from_frame(
    frame, keyboard: Keyboard, frame_number: int, wait_delay: int
):
    screen_height = len(frame)

    # TODO remove static background below keys
    prepared_frame = perform_morphological_open_with_frame(
        threshold_frame(
            blur_frame(
                grayscale_frame(increase_frame_contrast(frame))
            )
        )
    )

    cut_prepared_frame, play_line_y = cut_frame_vertically(
        prepared_frame,
        settings.default_play_line_relative_position_to_top,
    )

    frame_contours = find_frame_contours(cut_prepared_frame)

    falling_rectangles = frame_contours_to_falling_rectangles(
        frame_contours, play_line_y
    )

    # TODO add color into falling_rectangles

    falling_rectangles = __filter_falling_rectangles(
        falling_rectangles, keyboard
    )

    if settings.is_debug:
        frame_to_draw = frame

        number_of_falling_rectangles = len(falling_rectangles)

        for i, falling_key in enumerate(falling_rectangles):
            falling_key.draw(frame_to_draw)

            debugger.draw_text(
                frame_to_draw,
                str(number_of_falling_rectangles),
                (16, screen_height - 16),
            )
        cv2.imshow("frame", frame_to_draw)

    return falling_rectangles


def __filter_falling_rectangles(
    falling_rectangles: [FallingRectangle], keyboard: Keyboard
) -> [FallingRectangle]:
    filtered_falling_rectangles = []

    for falling_rectangle in falling_rectangles:
        if (
            falling_rectangle.width <= keyboard.white_key_width * 1.5
            and falling_rectangle.width
            >= keyboard.black_key_width * 0.5
        ):
            filtered_falling_rectangles.append(falling_rectangle)

    return filtered_falling_rectangles


def __convert_falling_rectangles_to_falling_keys(
    falling_rectangles: [FallingRectangle],
    keyboard: Keyboard,
    frame_time: float,
):
    falling_keys = []

    for falling_rectangle in falling_rectangles:
        print(frame_time, falling_rectangle)
        # TODO convert falling rectangles into falling keys

    return falling_keys
