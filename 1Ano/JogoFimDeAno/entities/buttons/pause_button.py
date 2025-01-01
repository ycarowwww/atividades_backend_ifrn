import pygame as pg
from entities.buttons.button import Button
from scripts.settings import scale_dimension, scale_position
from typing import Callable

class PauseButton(Button):
    def __init__(self, size: tuple[int, int], position: tuple[int, int], pos_attr: str, action: Callable, color: tuple[int, int, int], gap: int):
        super().__init__(size, position, pos_attr, action)
        self._color = color
        self._rect_gap = gap
        self.is_paused = False
        self._base_rect_gap = self._rect_gap
        self._generate_forms()
    
    def update(self) -> None:
        self.is_paused = not self.is_paused

        self._action()
    
    def draw(self, screen: pg.Surface) -> None:
        if self.is_paused:
            pg.draw.polygon(screen, self._color, self._triangle_points)
        else:
            for rect in self._rects:
                pg.draw.rect(screen, self._color, rect)
    
    def check_clicked(self, mouse_pos: tuple[int, int]) -> bool:
        checking: bool = self._hitbox.collidepoint(mouse_pos)

        if checking:
            self.update()

        return checking

    def update_by_event(self, event: pg.event.Event) -> None:
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.update()
        
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
        self._rect_gap = scale_dimension(self._base_rect_gap, new_resolution)
        self._generate_forms()
    
    def _generate_forms(self) -> None:
        rect_width = int(self._size[0] / 2 - self._rect_gap / 2)
        self._rects = [
            pg.Rect(self._hitbox.topleft, (rect_width, self._size[1])),
            pg.Rect((self._hitbox.left + rect_width + self._rect_gap, self._hitbox.top), (rect_width, self._size[1]))
        ]
        self._triangle_points = [
            self._hitbox.topleft,
            self._hitbox.bottomleft,
            (self._hitbox.right, self._hitbox.centery)
        ]
