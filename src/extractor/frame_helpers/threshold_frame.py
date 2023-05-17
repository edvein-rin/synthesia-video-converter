import cv2


from .blur_frame import blur_frame
from .grayscale_frame import grayscale_frame
from .increase_frame_contrast import increase_frame_contrast


def threshold_frame(frame):
    _, thresholded_frame = cv2.threshold(
        frame,
        0,
        255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU,
    )

    # # https://stackoverflow.com/questions/57283802/remove-small-whits-dots-from-binary-frame-using-opencv-python
    # # https://stackoverflow.com/questions/35854197/how-to-use-opencvs-connectedcomponentswithstats-in-python
    # _, binary_map = cv2.threshold(frame, 0, 255, 0)
    # # do connected components processing
    # nlabels, labels, stats, centroids = (
    #     cv2.connectedComponentsWithStats(
    #         binary_map, None, None, None, 8, cv2.CV_32S
    #     )
    # )
    # # get CC_STAT_AREA component as stats[label, COLUMN]
    # areas = stats[1:, cv2.CC_STAT_AREA]
    # threshold_frame = np.zeros((labels.shape), np.uint8)
    # for i in range(0, nlabels - 1):
    #     if areas[i] >= 220:  # keep
    #         threshold_frame[labels == i + 1] = 255

    # _, threshold_frame = cv2.threshold(
    #     frame, 100, 255, cv2.THRESH_BINARY
    # )

    # _, threshold_frame = cv2.threshold(
    #     frame, 0, 255, cv2.THRESH_TOZERO
    # )

    # threshold_frame = cv2.adaptiveThreshold(
    #     frame,
    #     255,
    #     cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    #     cv2.THRESH_BINARY,
    #     11,
    #     2,
    # )

    return thresholded_frame
