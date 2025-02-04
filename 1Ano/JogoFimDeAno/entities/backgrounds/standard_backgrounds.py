from scripts import COLORS
from . import Checkered, Lines
from random import randint, uniform, getrandbits

def get_backgrounds_list(screen_size: tuple[int, int]) -> list[Checkered | Lines]: 
    return [
        Lines(randint(10, 20), screen_size, uniform(0.5, 2), COLORS["GRAY"], COLORS["BLACK"], bool(getrandbits(1)), bool(getrandbits(1))), # bool(getrandbits(1)) = random generate between "True" and "False" relatively fast.
        Checkered(screen_size, randint(10, 20), COLORS["GRAY"], COLORS["BLACK"], uniform(0.5, 2), uniform(0, 360))
    ]
