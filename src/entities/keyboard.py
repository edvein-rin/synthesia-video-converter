import cv2

from ..midi import WHITE_NOTES

from .note import Note
from .play_line import PlayLine


class Keyboard(object):
    def __init__(
        self,
        width: int,
        number_of_white_keys: int,  # 1-52
        white_key_width: int,
        black_key_width: int,
        play_line: PlayLine,
        white_key_x_offset: float = 0,
        black_key_x_offset: float = 0,
    ) -> None:
        self.width = width
        self.number_of_white_keys = number_of_white_keys
        self.white_key_width = white_key_width
        self.black_key_width = black_key_width
        self.play_line = play_line
        self.white_key_x_offset = white_key_x_offset
        self.black_key_x_offset = black_key_x_offset

    def __repr__(self):
        return (
            "<Keyboard"
            f" width={self.width}"
            f" number_of_white_keys={self.number_of_white_keys}"
            f" white_key_width={self.white_key_width}"
            f" black_key_width={self.black_key_width}"
            f" white_key_x_offset={self.white_key_x_offset}"
            f" black_key_y_offset={self.black_key_x_offset}"
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
            for n in range(self.number_of_white_keys):
                if (
                    n
                    <= (x - self.white_key_x_offset)
                    / self.white_key_width
                    and (x - self.white_key_x_offset)
                    / self.white_key_width
                    < n + 1
                ):
                    if self.number_of_white_keys == 52:
                        black_key_number = n + 1

                        if black_key_number <= 2:
                            if black_key_number == 1:
                                return Note("A", 0)
                            else:
                                return Note("B", 0)
                        else:
                            octave = (black_key_number - 2) // 7 + 1
                            position_in_octave = (
                                black_key_number - 2
                            ) % 7

                            note = WHITE_NOTES[position_in_octave - 1]

                            # print(
                            #     "WHITE | Octave ="
                            #     f" {octave} | Position in"
                            #     f" octave = {position_in_octave} |"
                            #     f" Note {note}"
                            # )

                            return Note(note, octave)
                    else:
                        raise NotImplementedError()

            raise Exception(
                f"Key is out of keyboard range (x = {x},"
                f" keyboard_width = {self.width})"
            )

        for n in range(self.number_of_white_keys):
            if (
                n
                <= (
                    x
                    - self.white_key_x_offset
                    - self.white_key_width / 2
                )
                / self.white_key_width
                and (
                    x
                    - self.white_key_x_offset
                    - self.white_key_width / 2
                )
                / self.white_key_width
                < n + 1
            ):
                if self.number_of_white_keys == 52:
                    black_key_number = n + 1

                    if black_key_number <= 1:
                        return Note("A#", 0)
                    else:
                        octave = (black_key_number - 1) // 7 + 1
                        position_in_octave = (
                            black_key_number - 1
                        ) % 7

                        if (
                            position_in_octave == 3
                            or position_in_octave == 0
                        ):
                            print(
                                "WARNING This black key does not exist (n ="
                                f" {n}, black_key_number ="
                                f" {black_key_number}, octave ="
                                f" {octave}, position_in_octave ="
                                f" {position_in_octave})."
                            )
                            return None

                        note = (
                            WHITE_NOTES[position_in_octave - 1] + "#"
                        )

                        # print(
                        #     "BLACK | Octave ="
                        #     f" {octave} | Position in"
                        #     f" octave = {position_in_octave} |"
                        #     f" Note {note}"
                        # )

                        return Note(note, octave)
                else:
                    raise NotImplementedError()

        raise Exception(
            f"Key is out of keyboard range (x = {x},"
            f" keyboard_width = {self.width})"
        )

    def draw(self, image):
        key_height = 128

        for n in range(self.number_of_white_keys):
            x = int(
                self.white_key_x_offset + (self.white_key_width) * n
            )
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
