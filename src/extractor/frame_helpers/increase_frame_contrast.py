import cv2
# import numpy as np


def increase_frame_contrast(frame):
    contrast = 2  # From 0 to 127
    brightness = 1.0  # From 0 to 100

    return cv2.addWeighted(frame, contrast, frame, 0, brightness)
