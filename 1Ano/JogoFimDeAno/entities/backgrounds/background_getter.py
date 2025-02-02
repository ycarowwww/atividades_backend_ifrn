from . import get_backgrounds_list
from random import choice

class BackgroundGetter:
    @staticmethod
    def random_background(screen_size: tuple[int, int]) -> None:
        return choice(get_backgrounds_list(screen_size))
