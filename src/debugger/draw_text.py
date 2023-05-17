import cv2


def draw_text(image, text: str, coordinates: (int, int)) -> None:
    cv2.putText(
        image,
        text,
        coordinates,
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2,
    )
