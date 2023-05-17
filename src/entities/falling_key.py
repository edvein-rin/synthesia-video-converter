class FallingKey(object):
    def __init__(
        self,
        start_time: float,
        duration: float,
        pitch: str,
        volume: float,
        color: str,
    ):
        self.start_time = start_time
        self.duration = duration
        self.pitch = pitch
        self.volume = volume
        self.color = color
