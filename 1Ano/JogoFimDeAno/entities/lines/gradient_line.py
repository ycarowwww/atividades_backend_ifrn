import pygame as pg
from scripts import scale_dimension, scale_position, BASE_RESOLUTION
from math import sqrt, atan2, pi

class GradientLine:
    """Create a Gradient Line between two points."""
    def __init__(self, colors: list[tuple[int, int, int, int]], point1: tuple[int, int], point2: tuple[int, int], radius: int) -> None:
        self._amount_colors = len(colors)
        self._colors = colors
        self._points = (point1, point2)
        self._radius = radius
        self._surface, self._surface_rect = self._create_surface()

        self._save_values = ([list(i).copy() for i in self._points], self._radius)
    
    def draw(self, screen: pg.Surface) -> None:
        screen.blit(self._surface, self._surface_rect)
    
    def resize(self, new_resolution: tuple[int, int]) -> None:
        self._points = (
            scale_position(self._save_values[0][0], BASE_RESOLUTION, new_resolution),
            scale_position(self._save_values[0][1], BASE_RESOLUTION, new_resolution)
        )
        self._radius = scale_dimension(self._save_values[1], new_resolution)
        self._surface, self._surface_rect = self._create_surface()

    def _create_surface(self) -> tuple[pg.Surface, pg.Rect]:
        self._center = tuple((self._points[0][i] + self._points[1][i]) // 2 for i in range(2))

        distance = round(sqrt((self._points[0][0] - self._points[1][0]) ** 2 + (self._points[0][1] - self._points[1][1]) ** 2))
        surf = pg.Surface((1, self._amount_colors), pg.SRCALPHA)
        for i, color in enumerate(self._colors):
            surf.set_at((0, i), color)
        surf = pg.transform.smoothscale(surf, (distance, self._radius)) # Smooth colors expanding

        angle = pi - atan2(self._points[0][1] - self._points[1][1], self._points[0][0] - self._points[1][0])
        surf = pg.transform.rotate(surf, angle * 180 / pi)
        surf_rect = surf.get_rect(center=self._center)

        return (surf, surf_rect)
