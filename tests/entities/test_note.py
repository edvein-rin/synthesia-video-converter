from src.entities import Note


class TestNote:
    def test_middle_c(self):
        A0 = Note("A", 0)
        assert A0.midi_number == 21

        C3 = Note("C", 3)
        assert C3.midi_number == 48
