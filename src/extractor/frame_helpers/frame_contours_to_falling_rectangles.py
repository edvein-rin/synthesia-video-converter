import cv2

from ...entities import FallingRectangle


def frame_contours_to_falling_rectangles(
    frame_contours, play_line_y: int
) -> [FallingRectangle]:
    falling_keys = []
    for i, contour in enumerate(frame_contours):
        x, top_y, w, h = cv2.boundingRect(contour)

        falling_keys.append(
            FallingRectangle(x, play_line_y + top_y, w, h)
        )

    return falling_keys
