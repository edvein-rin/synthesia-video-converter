from src.extractor.merge_falling_keys import merge_falling_keys
from src.entities import FallingKey

from falling_keys import falling_keys


def test_merge_falling_keys():
    assert merge_falling_keys(falling_keys) == [
        FallingKey(
            start_time=4.0,
            duration=0.4666666666666668,
            note="G",
            octave=3,
            volume=100,
            color="#faf",
        ),
        FallingKey(
            start_time=4.0,
            duration=0.36666666666666625,
            note="E",
            octave=3,
            volume=100,
            color="#faf",
        ),
        FallingKey(
            start_time=4.0,
            duration=0.833333333333333,
            note="E",
            octave=2,
            volume=100,
            color="#faf",
        ),
    ]
