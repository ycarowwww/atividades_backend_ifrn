import pygame as pg
import pygame.freetype as pgft
from scripts import scale_dimension, scale_position, BASE_RESOLUTION, FONT, LEVELS_PERFECTION
from math import sin, cos, pi
from random import uniform
from typing import Callable

class PerfectionDrawer:
    def __init__(self, center: tuple[int, int], radius: int, perfect_color: tuple[int, int, int], imperfect_color: tuple[int, int, int], text_color: tuple[int, int, int], current_level: int, angular_speed: float = uniform(-2 * pi, 2 * pi), difference_expansion: float = 0, repetition_time: float = 0, font: pgft.Font = FONT) -> None:
        self._center = center
        self._radius = radius
        self._current_radius = self._radius
        self._colors = (perfect_color, imperfect_color, text_color)
        self._is_perfect = True
        self._triangle_color = self._colors[0]
        self._movements = LEVELS_PERFECTION.get(str(current_level))
        self._expansion_form = self._get_difference_expansion(difference_expansion, repetition_time)
        self._angle = 0.0
        self._time = 0
        self._angular_speed = angular_speed
        self._font = font
        self._saves_values = (self._center, difference_expansion, repetition_time, self._radius)
        self._text = self._generate_text()
    
    def update(self, dt: float) -> None:
        self._time += dt
        self._time %= 1
        self._current_radius = self._radius + self._expansion_form(self._time)
        self._angle += self._angular_speed * dt
        self._angle %= 2 * pi
    
    def draw(self, screen: pg.Surface) -> None:
        pg.draw.polygon(screen, self._triangle_color, self._get_points())
        screen.blit(self._text[0], self._text[1])
    
    def resize(self, new_resolution: tuple[int, int]) -> None:
        self._center = scale_position(self._saves_values[0], BASE_RESOLUTION, new_resolution)
        self._expansion_form = self._get_difference_expansion(scale_dimension(self._saves_values[1], new_resolution), self._saves_values[2])
        self._radius = scale_dimension(self._saves_values[3], new_resolution)
        self._text = self._generate_text()

    def _generate_text(self) -> tuple[pg.Surface, pg.Rect]:
        text_surf, text_rect = self._font.render(str(self._movements), self._colors[2], style=pgft.STYLE_STRONG, size=self._radius//2)
        text_rect.center = self._center
        return text_surf, text_rect

    def update_movements(self) -> None:
        if self._movements > 0 and self._is_perfect:
            self._movements -= 1
        else:
            self._movements += 1
            self._triangle_color = self._colors[1]
            self._is_perfect = False
        
        self._text = self._generate_text()
        self.set_new_rotation()

    def set_new_rotation(self) -> None:
        self._angular_speed = uniform(-2 * pi, 2 * pi)
    
    def reset(self, new_level: int) -> None:
        self._movements = LEVELS_PERFECTION.get(str(new_level))
        self._triangle_color = self._colors[0]
        self._is_perfect = True
        self._text = self._generate_text()

    def get_is_perfect(self) -> None: return self._is_perfect

    def _get_points(self) -> None:
        d_ang = 2 * pi / 3
        return [
            (self._current_radius * cos(d_ang * i + self._angle) + self._center[0], self._current_radius * sin(d_ang * i + self._angle) + self._center[1])
            for i in range(3)
        ]
    
    @staticmethod
    def _get_difference_expansion(difference: float, repetition: float) -> Callable[[float], float]:
        if difference == 0:
            return lambda t: 0
        
        def dif(t: float) -> float:
            min_dif = -difference / 2
            max_div = difference / 2

            return (max_div - min_dif) * (cos(2 * pi * t / repetition) + 1) / 2 + min_dif

        return dif
