import cv2

from ..midi import WHITE_NOTES

from .note import Note
from .play_line import PlayLine


NUMBER_OF_WHITE_KEYS = 52


class Keyboard(object):
    def __init__(
        self,
        width: int,
        white_key_width: int,
        black_key_width: int,
        inner_offset: float,
        play_line: PlayLine,
    ) -> None:
        self.width = width
        self.white_key_width = white_key_width
        self.black_key_width = black_key_width
        self.inner_offset = inner_offset
        self.play_line = play_line

    def __repr__(self):
        return (
            "<Keyboard"
            f" width={self.width}"
            f" white_key_width={self.white_key_width}"
            f" black_key_width={self.black_key_width}"
            f" inner_offset={self.inner_offset}"
            f" play_line={self.play_line} />"
        )

    def detect_note(
        self, x: float, is_white_key: bool = None
    ) -> Note | None:
        if is_white_key is None:
            # TODO implement algorithm of detection without
            # previous knowledge of a key color
            raise NotImplementedError()

        if is_white_key:
            for n in range(NUMBER_OF_WHITE_KEYS):
                if (
                    n
                    <= (x - self.inner_offset) / self.white_key_width
                    and (x - self.inner_offset) / self.white_key_width
                    < n + 1
                ):
                    white_key_number = n + 1

                    if white_key_number <= 2:
                        if white_key_number == 1:
                            return Note("A", 0)
                        else:
                            return Note("B", 0)
                    else:
                        octave = (white_key_number - 2) // 7 + 1
                        position_in_octave = (
                            white_key_number - 2
                        ) % 7

                        note = WHITE_NOTES[position_in_octave - 1]

                        # print(
                        #     "WHITE | Octave ="
                        #     f" {octave} | Position in"
                        #     f" octave = {position_in_octave} |"
                        #     f" Note {note}"
                        # )

                        return Note(note, octave)

            raise Exception(
                f"White key is out of keyboard range (x = {x},"
                f" keyboard_width = {self.width})"
            )

        for n in range(NUMBER_OF_WHITE_KEYS):
            if (
                n
                <= (x - self.inner_offset - self.white_key_width / 2)
                / self.white_key_width
                and (x - self.inner_offset - self.white_key_width / 2)
                / self.white_key_width
                <= n + 1
            ):
                white_key_number = n + 1

                if white_key_number <= 1:
                    return Note("A#", 0)
                else:
                    octave = (white_key_number - 1) // 7 + 1
                    position_in_octave = (white_key_number - 1) % 7

                    if (
                        position_in_octave == 3
                        or position_in_octave == 0
                    ):
                        print(
                            "WARNING This black key does not"
                            f" exist (n = {n}, black_key_number ="
                            f" {white_key_number}, octave ="
                            f" {octave}, position_in_octave ="
                            f" {position_in_octave})."
                        )
                        return None

                    note = WHITE_NOTES[position_in_octave - 1] + "#"

                    # print(
                    #     "BLACK | Octave ="
                    #     f" {octave} | Position in"
                    #     f" octave = {position_in_octave} |"
                    #     f" Note {note}"
                    # )

                    return Note(note, octave)

        raise Exception(
            f"Black key is out of keyboard range (x = {x}, keyboard_width ="
            f" {self.width}, inner_offset = {self.inner_offset},"
            f" white_key_width = {self.white_key_width})"
        )

    def draw(self, image):
        key_height = 128

        for n in range(NUMBER_OF_WHITE_KEYS):
            x = int(self.inner_offset + (self.white_key_width) * n)
            y = self.play_line.y

            opposite_x = int(x + self.white_key_width)
            opposite_y = y + key_height

            # TODO make transparent
            cv2.rectangle(
                image,
                (x, y),
                (opposite_x, opposite_y),
                (255, 255, 255),
                1,
            )

        # TODO draw black keys
