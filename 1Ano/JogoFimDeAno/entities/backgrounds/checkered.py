import pygame as pg
from math import cos, sin

class Checkered:
    def __init__(self, size: tuple[int, int], amount_rects: int, fgcolor: tuple[int, int, int], bgcolor: tuple[int, int, int], speed_mult: float = 1.0, angle: float = 0.0):
        self._amount = amount_rects
        self._fgcolor = fgcolor
        self._bgcolor = bgcolor
        self._speed_mult = speed_mult
        self._angle = angle
        self._size = size
        self._rect_size = tuple(s / self._amount for s in self._size)
        self._velocity = (self._rect_size[0] * cos(self._angle), self._rect_size[1] * sin(self._angle))
        self._draw_rects()
    
    def update(self, dt: float) -> None:
        ...
    
    def draw(self, screen: pg.Surface) -> None:
        ...
    
    def resize(self, new_size: tuple[int, int]) -> None:
        ...
    
    def _draw_rects(self) -> None:
        self._surface = pg.Surface(tuple(self._size[i] + 4 * self._rect_size[i] for i in range(2)))
        self.points_x = tuple(
            self._rect_size[0] * i for i in range(self._amount + 4)
        )
        self.points_y = tuple(
            self._rect_size[1] * i for i in range(self._amount + 4)
        )

    @staticmethod
    def _draw_rect(surface: pg.Surface, points_x: list[tuple[int, int]], points_y: list[tuple[int, int]]) -> None:
        ...
