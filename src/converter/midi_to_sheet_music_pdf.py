import pathlib

import music21


def midi_to_sheet_music_pdf(
    midi_file_path: str, sheet_music_pdf_file_path: str
):
    # TODO rethrow an error if LilyPond is not installed

    stream = music21.converter.parse(midi_file_path)

    sheet_music_pdf_folder_path = pathlib.Path(
        sheet_music_pdf_file_path
    ).parent

    # TODO add header in the sheet music PDF
    # TODO silence output
    stream.write(
        "lily.pdf",
        fp=sheet_music_pdf_folder_path.joinpath("temp"),
    )

    sheet_music_pdf_folder_path.joinpath("temp").unlink()
    sheet_music_pdf_folder_path.joinpath("temp.pdf").rename(
        sheet_music_pdf_file_path
    )
