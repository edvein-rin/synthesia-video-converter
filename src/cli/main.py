from pathlib import Path
from typing import Optional

import typer
from typing_extensions import Annotated

from ..extractor import extract_musical_information_from_video
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
    settings = Settings()
    settings.is_debug = debug

    extract_musical_information_from_video(str(video))
