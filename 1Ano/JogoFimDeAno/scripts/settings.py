import pygame.freetype as pgft
from json import load as json_load
from math import sin, cos, atan2, pi
from os import path

pgft.init() # Needed for the FreeType library initialize

BASE_RESOLUTION: tuple[int, int] = (800, 600) # Base Resolution of the screen

def scale_position(position: tuple[int, int], actual_resolution: tuple[int, int], new_resolution: tuple[int, int]) -> tuple[int, int]:
    return (round(position[0] / actual_resolution[0] * new_resolution[0]), round(position[1] / actual_resolution[1] * new_resolution[1]))

def scale_dimension(original_dimension: int, new_resolution: tuple[int, int], original_resolution: tuple[int, int] = BASE_RESOLUTION) -> int:
    return round(original_dimension * min(new_resolution[0] / original_resolution[0], new_resolution[1] / original_resolution[1]))

def get_file_path(file: str) -> str:
    base_dir: str = path.dirname(path.abspath(__file__))

    return path.join(base_dir, file)

def get_diagonal_line(point1: tuple[int, int], radius1: int, point2: tuple[int, int], radius2: int) -> tuple[tuple[int, int], tuple[int, int], tuple[int, int], tuple[int, int]]:
    """Returns the 4 points of a 'quadrilateral' for a 'diagonal' line from circle1 to circle2

        Pygame can only draw lines with 90º ends, creating a 'shrinking' effect when drawing a line between two circles.
        This function returns 4 points between the circles to draw in the 'pg.draw.polygon' function for a line with a 'diagonal' ending.

        Args:
            point1 (tuple): Circle1's center.
            radius1 (tuple): Circle1's radius.
            point2 (int): Circle2's center.
            radius1 (int): Circle2's radius.

        Returns:
            tuple: A tuple with 4 points positions.
    """
    pos1: tuple[int, int] = (point1[0], -point1[1]) # Flipping the y-axis because of Pygame
    pos2: tuple[int, int] = (point2[0], -point2[1]) # Flipping the y-axis because of Pygame
    angle: float = atan2(point1[0] - point2[0], point1[1] - point2[1])

    def rotate_point(rad: int, ang: float, x: int, y: int) -> tuple[int, int]:
        """Returns the point position in the circle."""
        return (int(rad * cos(ang) + x), int(rad * sin(ang) + y))
    
    points = (rotate_point(radius1, angle, pos1[0], pos1[1]), 
                rotate_point(radius1, angle + pi, pos1[0], pos1[1]), 
                rotate_point(radius2, angle + pi, pos2[0], pos2[1]), 
                rotate_point(radius2, angle, pos2[0], pos2[1]))

    return tuple([(p[0], -p[1]) for p in points]) # Unflipping the y-axis because of Pygame

def convert_decimal_to_roman(num: int) -> str | None:
    """Converts decimal numerals to roman numerals (probably just correct until the 4000s)."""
    if num <= 0: return None # Roman Numerals doesn't have 0 and negatives.

    standard_roman_numerals = { # Specific roman numerals
        1000 : "M",
        900 : "CM",
        500 : "D",
        400 : "CD",
        100 : "C",
        90 : "XC",
        50 : "L",
        40 : "XL",
        10 : "X",
        9 : "IX",
        5 : "V",
        4 : "IV",
        1 : "I"
    }

    roman_number = ""

    while num > 0:
        div = next(i for i in standard_roman_numerals.keys() if num >= i)

        roman_number += standard_roman_numerals[div] * (num // div) # Writes the same character "num // div" times.
        
        num %= div # Goes to the rest of the characters.
    
    return roman_number

INITIAL_MAX_FPS: float = 60.0
COLORS: dict[str, tuple[int, int, int, int | None]] = {
    "BLACK" : (0, 0, 0),
    "GRAY" : (20, 20, 20),
    "WHITE" : (255, 255, 255),
    "RED" : (255, 30, 30),
    "GREEN" : (30, 255, 30),
    "BLUE" : (35, 172, 255),
    "BLANK" : (0, 0, 0, 0)
}
FONT: pgft.Font = pgft.Font(get_file_path("../fonts/inter.ttf"))
OBSTACLES_HEIGHT: int = 30
INITIAL_ALPHA_TRACKER: int = 50

with open(get_file_path("../data/levels.json")) as file:
    LEVELS: dict[str, list[int]] = json_load(file)

with open(get_file_path("../data/levels_perfection.json")) as file:
    LEVELS_PERFECTION: dict[str, bool] = json_load(file)

with open(get_file_path("../data/player_perfection_levels.json")) as file:
    LEVELS_PERFECTION_UNLOCKED: dict[str, bool] = json_load(file)

with open(get_file_path("../data/achievements.json")) as file:
    ACHIEVEMENTS: dict[str, dict[str, str | bool | int]] = json_load(file)

with open(get_file_path("../data/player_achievements_unlocked.json")) as file:
    ACHIEVEMENTS_UNLOCKED: dict[str, bool] = json_load(file)
