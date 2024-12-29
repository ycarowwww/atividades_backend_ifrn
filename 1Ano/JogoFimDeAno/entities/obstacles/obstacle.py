import pygame as pg
from entities.player import Player
from scripts.settings import INITIAL_ALPHA_TRACKER
from collections import deque

# Could add some JSON recognition for the levels

class Obstacle:
    """Obstacle Template Class for the others Obstacles."""
    def __init__(self, x: float, y: float, width: float, height: float, speed: float, spacing_mult: float, color: tuple[int, int, int]):
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._speed = speed
        self._color = color
        self._spacing_mult = spacing_mult
        self._position_tracker = deque()
        self._position_tracker_times = deque()
        self._position_tracker_lifetime = 0.2 # seconds
        self._initial_alpha_tracker = INITIAL_ALPHA_TRACKER
        self._base_width = self._width
        self._base_height = self._height
    
    def update(self, dt: float) -> None: pass
    
    def draw(self, screen: pg.Surface) -> None: pass
    
    def check_collision(self, player: Player) -> bool: pass

    def set_new_resolution(self, new_resolution: tuple[int, int]) -> None: pass

    def _update_tracker(self, dt: float) -> None: pass

    def _draw_tracker(self, screen: pg.Surface) -> None: pass

    def set_x(self, new_x: float) -> None: self._x = new_x

    def set_y(self, new_y: float) -> None: self._y = new_y

    def set_speed(self, new_speed: float) -> None: self._speed = new_speed

    def get_x(self) -> int: return self._x

    def get_y(self) -> int: return self._y

    def get_spacing_mult(self) -> float: return self._spacing_mult
