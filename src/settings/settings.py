from ..meta.singleton import SingletonMeta


class Settings(metaclass=SingletonMeta):
    default_play_line_relative_position_to_top: float = 0.6
    is_debug: bool = True
    # TODO add possibility to set parameters below from ENVs
    debug_wait_delay: float | None = 1
    debug_skip_rendering: bool = True
