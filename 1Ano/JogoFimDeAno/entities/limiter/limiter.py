import pygame as pg
from scripts import scale_dimension, scale_position, BASE_RESOLUTION
from math import sqrt
from typing import Any, Callable

class Limiter:
    def __init__(self, size: tuple[float, float], position: tuple[float, float], attr_pos: str, bg_color: tuple[int, int, int], fg_color: tuple[int, int, int], lowerbound: float, upperbound: float, start_value: float = 0, action: Callable[[float], Any] = lambda v: None) -> None:
        self._size = size
        self._position = position
        self._attr_pos = attr_pos
        self._hitbox_rect = pg.Rect((0, 0), size)
        setattr(self._hitbox_rect, self._attr_pos, self._position)
        self._lowerbound = lowerbound
        self._upperbound = upperbound
        self._actual_percentage = self._get_percentage_by_value(start_value)
        self._actual_position = self._get_actual_pos(self._actual_percentage)
        self._actual_value = min(max(start_value, self._lowerbound), self._upperbound)
        self._bg_color = bg_color
        self._fg_color = fg_color
        self._is_pressing = False
        self._action = action
        self._base_size = self._size
        self._base_position = self._position
        self._base_resolution = BASE_RESOLUTION
    
    def update(self, dt: float) -> None:
        if not self._is_pressing: return

        mx = pg.mouse.get_pos()[0]

        self._actual_percentage = self._get_percentage_x(mx) # Calculates new position of the actual
        self._actual_position = self._get_actual_pos(self._actual_percentage)
        self._actual_value = self._calculate_actual_value(self._actual_percentage)
        self._do_action()
    
    def draw(self, screen: pg.Surface) -> None:
        pg.draw.rect(screen, self._bg_color, self._hitbox_rect)
        pg.draw.circle(screen, self._bg_color, (self._hitbox_rect.left, self._actual_position[1]), self._size[1] / 2)
        pg.draw.circle(screen, self._bg_color, (self._hitbox_rect.right, self._actual_position[1]), self._size[1] / 2)
        pg.draw.circle(screen, self._fg_color, self._actual_position, self._size[1] / 2)
    
    def update_by_event(self, event: pg.Event) -> None:
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1: # "1" == left mouse button
            if self._hitbox_rect.collidepoint(*event.pos) or self._check_collision_circle(event.pos):
                self._is_pressing = True
        
        if event.type == pg.MOUSEBUTTONUP and event.button == 1:
            self._is_pressing = False

    def _do_action(self) -> None:
        """Executes some function passing the actual value when it changes."""
        self._action(self._actual_value)

    def get_actual_value(self) -> float: return self._actual_value

    def _calculate_actual_value(self, percentage: float) -> float:
        return (self._upperbound - self._lowerbound) * percentage + self._lowerbound

    def _check_collision_circle(self, pos: tuple[float, float]) -> bool:
        return sqrt((pos[0] - self._actual_position[0]) ** 2 + (pos[1] - self._actual_position[1]) ** 2) <= self._size[1] / 2
    
    def _get_actual_pos(self, percentage: float) -> tuple[float, float]:
        return (
            (self._hitbox_rect.right - self._hitbox_rect.left) * percentage + self._hitbox_rect.left,
            self._hitbox_rect.top + self._size[1] / 2
        )

    def _get_percentage_x(self, mx: float) -> float:
        mx_delimitered = min(max(mx, self._hitbox_rect.left), self._hitbox_rect.right)
        return (mx_delimitered - self._hitbox_rect.left) / self._size[0]

    def _get_percentage_by_value(self, val: float) -> float:
        return (val - self._lowerbound) / (self._upperbound - self._lowerbound)

    def resize(self, new_resolution: tuple[int, int]) -> None:
        self._position = scale_position(self._base_position, self._base_resolution, new_resolution)
        self._size = tuple(scale_dimension(self._base_size[i], new_resolution) for i in range(2))
        self._hitbox_rect.width = self._size[0]
        self._hitbox_rect.height = self._size[1]
        setattr(self._hitbox_rect, self._attr_pos, self._position)
        self._actual_position = self._get_actual_pos(self._actual_percentage)
