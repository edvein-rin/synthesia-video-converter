from .play_line import PlayLine


class Keyboard(object):
    def __init__(
        self,
        white_key_width: int,
        black_key_width: int,
        play_line: PlayLine,
    ) -> None:
        self.white_key_width = white_key_width
        self.black_key_width = black_key_width
        self.play_line = play_line

    def __repr__(self):
        return (
            "<Keyboard"
            f" white_key_width={self.white_key_width}"
            f" black_key_width={self.black_key_width}"
            f" play_line={self.play_line} />"
        )
