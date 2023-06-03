from pathlib import Path
from typing import Optional

import typer
from typing_extensions import Annotated

from ..extractor import extract_notes_from_video
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
    debug: bool = False,
) -> None:
    video_file_path = str(video)

    settings = Settings()
    settings.is_debug = debug

    notes = extract_notes_from_video(video_file_path)
