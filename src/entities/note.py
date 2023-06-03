from ..midi import (
    midi_number_to_note_and_octave,
    note_and_octave_to_midi_number,
    NOTES,
)


class Note(object):
    def __init__(
        self,
        note: str,  # C | C# | D | D# | E | F | F# | G | G# | A | A# | B
        octave: int,  # 0-11
        time: float = 0,
        duration: float = 0,
        volume: float = None,  # 0-127
        channel: int = 0,  # 0-15
    ):
        self.note = note
        self.octave = octave
        self.channel = channel
        self.time = time
        self.duration = duration
        self.volume = volume

    @classmethod
    def from_midi_number(cls, number: int):  # 0-127
        note, octave = midi_number_to_note_and_octave(number)

        return cls(note, octave)

    @property
    def note(self):
        return self._note

    @note.setter
    def note(self, value):
        assert value in NOTES, f"Value {value} is not a note."
        self._note = value

    @property
    def midi_number(self):
        return note_and_octave_to_midi_number(self.note, self.octave)

    def __repr__(self):
        return (
            "<Note"
            f" note={self.note}"
            f" octave={self.octave}"
            f" midi_number={self.midi_number}"
            f" channel={self.channel}"
            f" time={self.time}"
            f" duration={self.duration}"
            f" volume={self.volume} />"
        )
