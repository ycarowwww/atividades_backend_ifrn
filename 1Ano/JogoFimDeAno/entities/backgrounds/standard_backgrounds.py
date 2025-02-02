from scripts import COLORS
from . import Checkered, Lines
from random import randint, uniform

def get_backgrounds_list(screen_size: tuple[int, int]) -> list[Checkered | Lines]: 
    return [
        Lines(screen_size, 30, COLORS["GRAY"]), Checkered(screen_size, randint(10, 20), COLORS["GRAY"], COLORS["BLACK"], uniform(0.5, 2), uniform(0, 360))
    ]
