def cut_frame_vertically(frame, vertical_cut_percentage):
    # TODO automatically detect static parts of the video and remove them

    frame_height = len(frame)

    cut_from = int(
        frame_height - frame_height * (vertical_cut_percentage)
    )
    cut_to = cut_from + 1

    cut_frame = frame[cut_from:cut_to]

    return cut_frame, cut_from
