class PlayLine(object):
    def __init__(self, y: int, relative_position_to_top: float):
        self.y = int(y)
        self.relative_position_to_top = relative_position_to_top

    def __repr__(self):
        return (
            f"<PlayLine y={self.y} relative_position_to_top="
            f"{self.relative_position_to_top} />"
        )
