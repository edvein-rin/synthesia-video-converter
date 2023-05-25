from .blur_frame import blur_frame
from .grayscale_frame import grayscale_frame
from .increase_frame_contrast import increase_frame_contrast
from .perform_morphological_open_with_frame import (
    perform_morphological_open_with_frame,
)
from .threshold_frame import threshold_frame


def prepare_frame_for_analysis(frame):
    return perform_morphological_open_with_frame(
        threshold_frame(
            blur_frame(
                grayscale_frame(increase_frame_contrast(frame))
            )
        )
    )
