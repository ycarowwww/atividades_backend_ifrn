import pygame as pg
import pygame.freetype as pgft
from os import path

pg.init() # Needed for the FreeType library initialize

BASE_RESOLUTION: tuple[int, int] = (800, 600) # Base Resolution of the screen

def scale_position(position: tuple[int, int], actual_resolution: tuple[int, int], new_resolution: tuple[int, int]) -> tuple[int, int]:
    return (round(position[0] / actual_resolution[0] * new_resolution[0]), round(position[1] / actual_resolution[1] * new_resolution[1]))

def scale_dimension(original_dimension: int, new_resolution: tuple[int, int], original_resolution: tuple[int, int] = BASE_RESOLUTION) -> int:
    return round(original_dimension * min(new_resolution[0] / original_resolution[0], new_resolution[1] / original_resolution[1]))

def get_file_path(file: str) -> str:
    base_dir: str = path.dirname(path.abspath(__file__))

    return path.join(base_dir, file)

INITIAL_MAX_FPS: float = 60.0
COLORS: dict[str, tuple[int, int, int, int | None]] = {
    "BLACK" : (0, 0, 0),
    "GRAY" : (20, 20, 20),
    "WHITE" : (255, 255, 255),
    "RED" : (255, 30, 30),
    "GREEN" : (0, 255, 0),
    "BLUE" : (35, 172, 255),
    "BLANK" : (0, 0, 0, 0)
}
FONT: pgft.Font = pgft.Font(get_file_path("../fonts/inter.ttf"))
OBSTACLES_HEIGHT: int = 30
INITIAL_ALPHA_TRACKER: int = 50
