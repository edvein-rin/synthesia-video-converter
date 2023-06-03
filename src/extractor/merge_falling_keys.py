from ..entities import FallingKey

# TODO should be determined automatically via fps
MAX_INTERVAL_TO_BE_MERGED = (
    0.034  # 1 / 3 / 10 + removal of floating error
)


def merge_falling_keys(falling_keys: [FallingKey]) -> [FallingKey]:
    """
    Merges falling keys that too close to each other.
    """

    falling_keys_by_absolute_note = {}
    for falling_key in falling_keys:
        absolute_note = falling_key.note + str(falling_key.octave)

        if absolute_note not in falling_keys_by_absolute_note:
            falling_keys_by_absolute_note[absolute_note] = [
                falling_key
            ]
        else:
            falling_keys_by_absolute_note[absolute_note].append(
                falling_key
            )

    merged_falling_keys = []

    for absolute_note in falling_keys_by_absolute_note:
        falling_keys_of_the_same_absolute_note = (
            falling_keys_by_absolute_note[absolute_note]
        )

        i = 0
        while True:
            if i == len(falling_keys_of_the_same_absolute_note):
                break

            falling_key = falling_keys_of_the_same_absolute_note[i]
            previous_falling_key = (
                falling_keys_of_the_same_absolute_note[i - 1]
                if i > 0
                else None
            )

            if previous_falling_key is not None:
                if (
                    previous_falling_key.start_time
                    + previous_falling_key.duration
                    + MAX_INTERVAL_TO_BE_MERGED
                    >= falling_key.start_time
                ):
                    previous_falling_key.duration = (
                        falling_key.start_time
                        + falling_key.duration
                        - previous_falling_key.start_time
                    )
                    falling_keys_of_the_same_absolute_note.pop(i)

                    i = i - 1
                    continue

            i += 1

        merged_falling_keys += falling_keys_of_the_same_absolute_note

    return merged_falling_keys
