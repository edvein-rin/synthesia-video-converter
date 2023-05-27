import cv2


class FallingRectangle(object):
    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
    ) -> None:
        self.width = width
        self.x = x
        self.y = y
        self.height = height
        self.color = None

    def __repr__(self):
        return (
            "<FallingRectangle"
            f" x={self.center_x}"
            f" y={self.y}"
            f" width={self.width}"
            f" height={self.height}"
            f" center_x={self.center_x}"
            f" color={self.color} />"
        )

    @property
    def center_x(self):
        return self.x + self.width / 2

    def draw(self, image, color=(0, 255, 0)):
        cv2.rectangle(
            image,
            (self.x, self.y),
            (self.x + self.width, self.y + self.height),
            self.color if self.color else color,
            2,
        )

    def is_white_key(
        self, white_key_width: float, black_key_width: float
    ) -> bool:
        white_key_width_difference = abs(white_key_width - self.width)
        black_key_width_difference = abs(black_key_width - self.width)

        is_white = (
            white_key_width_difference < black_key_width_difference
        )

        return is_white
