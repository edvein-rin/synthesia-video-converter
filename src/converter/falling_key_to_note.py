from ..entities import FallingKey, Note


def falling_key_to_note(falling_key: FallingKey) -> Note:
    return Note(
        note=falling_key.note,
        octave=falling_key.octave,
        time=falling_key.start_time,
        duration=falling_key.duration,
        volume=falling_key.volume,
        # TODO determine channel by color
        channel=0,
    )
