import pygame as pg
from entities.buttons.button import Button
from typing import Callable

class PauseButton(Button):
    def __init__(self, size: tuple[int, int], topleft: tuple[int, int], action: Callable, color: tuple[int, int, int], gap: int):
        super().__init__(size, topleft, action)
        self._color = color
        self._rect_gap = gap
        rect_width = int(self._size[0] / 2 - self._rect_gap / 2)
        self._rects = [
            pg.Rect(self._topleft, (rect_width, self._size[1])),
            pg.Rect((self._topleft[0] + rect_width + self._rect_gap, self._topleft[1]), (rect_width, self._size[1]))
        ]
        self._triangle_points = [
            self._hitbox.topleft,
            self._hitbox.bottomleft,
            (self._hitbox.right, self._hitbox.centery)
        ]
        self.is_paused = False
    
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
