import cv2

from ..settings import Settings
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


# TODO def process_frame(frame, white_key_size, black_key_size):
def process_frame(frame):
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
        prepared_frame, settings.default_play_line_position
    )

    frame_contours = find_frame_contours(cut_prepared_frame)

    falling_rectangles = frame_contours_to_falling_rectangles(
        frame_contours, play_line_y
    )
    # TODO filter keys that twice bigger than average
    number_of_falling_keys = len(falling_rectangles)

    frame_to_draw = frame

    for i, falling_key in enumerate(falling_rectangles):
        if settings.is_debug:
            falling_key.draw(frame_to_draw)

            debugger.draw_text(
                frame_to_draw,
                str(number_of_falling_keys),
                (16, screen_height - 16),
            )

    if settings.is_debug:
        cv2.imshow("frame", frame_to_draw)
