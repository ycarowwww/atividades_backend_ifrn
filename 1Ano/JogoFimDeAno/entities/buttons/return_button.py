import pygame as pg
from entities.buttons.button import Button
from typing import Callable

class ReturnButton(Button):
    def __init__(self, size: tuple[int, int], topleft: tuple[int, int], action: Callable, color: tuple[int, int, int]):
        super().__init__(size, topleft, action)
        self._color = color
        self._triangle_points = [
            self._hitbox.topright,
            self._hitbox.bottomright,
            (self._hitbox.left, self._hitbox.centery)
        ]
    
    def update(self) -> None:
        self._action()
    
    def draw(self, screen: pg.Surface) -> None:
        pg.draw.polygon(screen, self._color, self._triangle_points)
    
    def check_clicked(self, mouse_pos: tuple[int, int]) -> bool:
        checking: bool = self._hitbox.collidepoint(mouse_pos)

        if checking:
            self.update()

        return checking

    def update_by_event(self, event: pg.event.Event) -> None:
        if event.type == pg.MOUSEBUTTONDOWN:
            self.check_clicked(event.pos)
