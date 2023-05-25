from ..meta.singleton import SingletonMeta


class Settings(metaclass=SingletonMeta):
    is_debug = True
    default_play_line_relative_position_to_top = 0.6
