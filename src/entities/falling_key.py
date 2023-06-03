class FallingKey(object):
    def __init__(
        self,
        start_time: float,  # In seconds
        duration: float,  # In milliseconds
        note: str,  # C | C# | D | D# | E | F | F# | G | G# | A | A# | B
        octave: int,
        volume: float,  # 0-127, as per the MIDI standard
        color: str,  # HEX
    ):
        self.start_time = start_time
        self.duration = duration
        self.note = note
        self.octave = octave
        self.volume = volume
        self.color = color

    def __repr__(self):
        return (
            "<FallingKey"
            f" start_time={self.start_time}"
            f" duration={self.duration}"
            f" note={self.note}"
            f" octave={self.octave}"
            f" volume={self.volume}"
            f" color={self.color} />"
        )

    # Used for copying structure for creating instances
    # def __repr__(self):
    #     return (
    #         f"FallingKey(start_time={self.start_time},"
    #         f" duration={self.duration},"
    #         f' note="{self.note}",'
    #         f" octave={self.octave},"
    #         f" volume={self.volume},"
    #         f' color="{self.color}")'
    #     )

    def __eq__(self, other):
        return (
            self.start_time == other.start_time
            and self.duration == other.duration
            and self.note == other.note
            and self.octave == other.octave
            and self.volume == other.volume
            and self.color == other.color
        )
