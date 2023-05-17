from ..meta.singleton import SingletonMeta


class Settings(metaclass=SingletonMeta):
    is_debug = True
    default_play_line_position = 0.6
