import cv2
import numpy as np


def perform_morphological_open_with_frame(frame):
    kernel = np.ones((5, 5), np.uint8)

    return cv2.morphologyEx(frame, cv2.MORPH_OPEN, kernel)
