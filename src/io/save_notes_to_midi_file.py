from midiutil import MIDIFile


from ..settings import Settings
from ..entities import Note


settings = Settings()


def save_notes_to_midi_file(
    notes: [Note], midi_file_path: str
) -> None:
    midi_file = MIDIFile()

    track = 0
    # TODO detect BPM automatically
    bpm = 120
    tempo = bpm

    midi_file.addTempo(track, 0, tempo)

    for note in notes:
        channel = note.channel
        pitch = note.midi_number
        time = note.time * tempo / 60
        duration = note.duration * tempo / 60
        volume = note.volume

        midi_file.addNote(
            track, channel, pitch, time, duration, volume
        )

    with open(midi_file_path, "wb") as midi_file_handle:
        midi_file.writeFile(midi_file_handle)

    return None
