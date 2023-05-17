import cv2


def find_frame_contours(frame):
    frame_contours, _ = cv2.findContours(
        frame, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
    )

    return frame_contours
