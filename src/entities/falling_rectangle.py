import cv2


class FallingRectangle(object):
    def __init__(
        self,
        right_x: int,
        top_y: int,
        width: int,
        height: int,
    ) -> None:
        self.width = width
        self.right_x = right_x
        self.top_y = top_y
        self.height = height
        self.color = None

    @property
    def center_x(self):
        return self.right_x - self.width / 2

    def draw(self, image):
        cv2.rectangle(
            image,
            (self.right_x, self.top_y),
            (self.right_x + self.width, self.top_y + self.height),
            (0, 255, 0),
            2,
        )

    def __repr__(self):
        return (
            "<FallingRectangle"
            f" right_x={self.right_x}"
            f" top_y={self.top_y}"
            f" width={self.width}"
            f" height={self.height}"
            f" color={self.color} />"
        )
