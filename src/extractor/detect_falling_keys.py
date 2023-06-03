import cv2

from ..settings import Settings
from ..entities import Keyboard, FallingRectangle, FallingKey
from .. import debugger

from .frame_helpers import (
    find_frame_contours,
    frame_contours_to_falling_rectangles,
    prepare_frame_for_analysis,
)

settings = Settings()


def detect_falling_keys(
    video_capture,
    keyboard: Keyboard,
    wait_delay: int,
):
    falling_keys = []

    video_height = video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT)

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

        falling_keys += __convert_falling_rectangles_to_falling_keys(
            falling_rectangles, keyboard, frame_time
        )

        if settings.is_debug:
            # TODO change frame to draw via keyboard
            # shortcuts through cv2 waitKey
            frame_to_draw = frame
            # frame_to_draw = prepare_frame_for_analysis(frame)

            number_of_falling_rectangles = len(falling_rectangles)

            keyboard.draw(frame_to_draw)

            for i, falling_key in enumerate(falling_rectangles):
                falling_key.draw(frame_to_draw)

            debugger.draw_text(
                frame_to_draw,
                str(number_of_falling_rectangles),
                (16, int(video_height - 16)),
            )

            cv2.imshow("frame", frame_to_draw)

        if settings.is_debug and cv2.waitKey(wait_delay) == ord("q"):
            break
    video_capture.release()

    # TODO combine close falling_keys

    return falling_keys


def __extract_falling_rectangles_from_frame(
    frame, keyboard: Keyboard, frame_number: int, wait_delay: int
):
    # TODO remove static background below keys

    prepared_for_analysis_frame = prepare_frame_for_analysis(frame)
    prepared_for_analysis_frame_line = prepared_for_analysis_frame[
        keyboard.play_line.y : keyboard.play_line.y + 1
    ]

    frame_contours = find_frame_contours(
        prepared_for_analysis_frame_line
    )

    falling_rectangles = frame_contours_to_falling_rectangles(
        frame_contours, keyboard.play_line.y
    )

    # TODO add color into falling_rectangles

    falling_rectangles = __filter_falling_rectangles(
        falling_rectangles, keyboard
    )

    return falling_rectangles


def __filter_falling_rectangles(
    falling_rectangles: [FallingRectangle], keyboard: Keyboard
) -> [FallingRectangle]:
    filtered_falling_rectangles = []

    for falling_rectangle in falling_rectangles:
        if (
            falling_rectangle.width <= keyboard.white_key_width * 1.25
            and falling_rectangle.width
            >= keyboard.black_key_width * 0.75
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
        is_white_key = falling_rectangle.is_white_key(
            keyboard.white_key_width, keyboard.black_key_width
        )

        # print(
        #     frame_time,
        #     falling_rectangle,
        #     f"{'WHITE' if is_white else 'BLACK'}",
        # )

        note = keyboard.detect_note(
            falling_rectangle.center_x, is_white_key
        )

        if note:
            start_time = frame_time
            duration = 0
            volume = 100
            color = "#faf"  # TODO

            falling_keys.append(
                FallingKey(
                    start_time,
                    duration,
                    note.note,
                    note.octave,
                    volume,
                    color,
                )
            )

    # print(falling_keys)

    return falling_keys
