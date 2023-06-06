from pathlib import Path
from typing import Optional

import typer
from typing_extensions import Annotated

from ..extractor import extract_notes_from_video
from ..converter import midi_to_sheet_music_pdf
from ..io import save_notes_to_midi_file
from ..settings import Settings


def main(
    video: Annotated[
        Optional[Path],
        typer.Argument(
            exists=True,
            file_okay=True,
            dir_okay=False,
            writable=False,
            readable=True,
        ),
    ],
    output: Annotated[
        Optional[Path],
        typer.Argument(
            file_okay=True,
            dir_okay=False,
            writable=True,
        ),
    ] = None,
    debug: bool = False,
) -> None:
    video_file_path = str(video)

    settings = Settings()
    settings.is_debug = debug

    output_midi_file_path = (
        # TODO use pathlib to set extension
        ".".join(video_file_path.split(".")[:-1]) + ".midi"
        if output is None
        else output
    )

    notes = extract_notes_from_video(video_file_path)

    save_notes_to_midi_file(notes, output_midi_file_path)

    output_sheet_music_pdf_file_path = (
        # TODO use pathlib to set extension
        ".".join(output_midi_file_path.split(".")[:-1])
        + ".pdf"
    )

    # TODO check is LilyPond installed

    midi_to_sheet_music_pdf(
        output_midi_file_path, output_sheet_music_pdf_file_path
    )
