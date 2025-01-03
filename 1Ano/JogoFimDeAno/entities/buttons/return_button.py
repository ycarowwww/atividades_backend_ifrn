import pygame as pg
from . import Button
from scripts import scale_dimension, scale_position
from typing import Callable

class ReturnButton(Button):
    def __init__(self, size: tuple[int, int], position: tuple[int, int], attr_pos: str, action: Callable, color: tuple[int, int, int]):
        super().__init__(size, position, attr_pos, action)
        self._color = color
        self._triangle_points = [
            self._hitbox.topright,
            self._hitbox.bottomright,
            (self._hitbox.left, self._hitbox.centery)
        ]
    
    def draw(self, screen: pg.Surface) -> None:
        pg.draw.polygon(screen, self._color, self._triangle_points)

    def update_by_event(self, event: pg.event.Event) -> None:
        if event.type == pg.MOUSEBUTTONDOWN:
            self.check_clicked(event.pos)
        
        if event.type == pg.VIDEORESIZE:
            self.resize(event.size)

    def resize(self, new_resolution: tuple[int, int]) -> None:
        self._size = [scale_dimension(size, new_resolution) for size in self._base_size]
        self._position = scale_position(self._base_position, self._base_resolution, new_resolution)
        self._hitbox.width = self._size[0]
        self._hitbox.height = self._size[1]
        self.set_position_attr(self._attr_pos, self._position)
        self._generate_forms()
    
    def _generate_forms(self) -> None:
        self._triangle_points = [
            self._hitbox.topright,
            self._hitbox.bottomright,
            (self._hitbox.left, self._hitbox.centery)
        ]
