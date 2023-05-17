import cv2


def grayscale_frame(frame):
    return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
