import pygame as pg
from scripts import scale_dimension, scale_position, BASE_RESOLUTION, get_diagonal_line

class Line:
    """A line class that supports drawing diagonal lines and resizing them."""
    def __init__(self, point1: tuple[int, int], point2: tuple[int, int], width_p1: int, width_p2: int, color: tuple[int, int, int]) -> None:
        self._points = (point1, point2)
        self._widths = (width_p1, width_p2)
        self._line_points = get_diagonal_line(self._points[0], self._widths[0], self._points[1], self._widths[1])
        self._color = color
        
        self._save_values = (self._points, self._widths)
    
    def draw(self, screen: pg.Surface) -> None:
        pg.draw.polygon(screen, self._color, self._line_points)
    
    def resize(self, new_resolution: tuple[int, int]) -> None:
        self._points = tuple(
            scale_position(i, BASE_RESOLUTION, new_resolution)
            for i in self._save_values[0]
        )
        self._widths = tuple(
            scale_dimension(i, new_resolution)
            for i in self._save_values[1]
        )
        self._line_points = get_diagonal_line(self._points[0], self._widths[0], self._points[1], self._widths[1])
