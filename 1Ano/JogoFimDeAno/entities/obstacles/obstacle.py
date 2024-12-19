import pygame as pg
from entities.player import Player
from scripts.settings import MAX_POSITIONS_TRACKER, INITIAL_ALPHA_TRACKER
from collections import deque

# Could add some JSON recognition for the levels

class Obstacle:
    """Obstacle Template Class for the others Obstacles."""
    def __init__(self, x: int, y: int, width: int, height: int, speed: int, color: tuple[int, int, int]):
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._speed = speed
        self._color = color
        self._position_tracker = deque()
        self._max_positions_tracker = MAX_POSITIONS_TRACKER
        self._initial_alpha_tracker = INITIAL_ALPHA_TRACKER
    
    def update(self) -> None: pass
    
    def draw(self, screen: pg.Surface) -> None: pass
    
    def check_collision(self, player: Player) -> None: pass

    def _draw_tracker(self, screen: pg.Surface) -> None: pass

    def get_x(self) -> int: return self._x

    def get_y(self) -> int: return self._y
