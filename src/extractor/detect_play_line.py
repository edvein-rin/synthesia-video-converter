import cv2

from ..entities import PlayLine


def detect_play_line(
    video_capture, default_play_line_relative_position_to_top=0.6
) -> PlayLine:
    video_height = video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT)

    # TODO implement actual detection

    play_line_y = (
        video_height
        - video_height * default_play_line_relative_position_to_top
    )
    play_line_relative_position_to_top = (
        default_play_line_relative_position_to_top
    )

    return PlayLine(play_line_y, play_line_relative_position_to_top)
