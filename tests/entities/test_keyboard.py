from src.entities import Keyboard, PlayLine


def test_keyboard():
    keyboard = Keyboard(1280, 52, 24.5, 13, PlayLine(288, 0.6))

    A0 = keyboard.detect_note(0, is_white_key=True)
    assert A0.note == "A"
    assert A0.octave == 0

    B0 = keyboard.detect_note(25, is_white_key=True)
    assert B0.note == "B"
    assert B0.octave == 0

    E2 = keyboard.detect_note(280, is_white_key=True)
    assert E2.note == "E"
    assert E2.octave == 2
