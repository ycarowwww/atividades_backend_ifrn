import pygame as pg
from typing import Callable

class Button:
    """Button Template Class for the others Buttons."""
    def __init__(self, size: tuple[int, int], topleft: tuple[int, int], action: Callable):
        self._size = size
        self._topleft = topleft
        self._hitbox = pg.Rect(self._topleft, self._size)
        self._action = action
    
    def update(self) -> None:
        self._action()
    
    def draw(self, screen: pg.Surface) -> None:
        self._draw_animation(screen)
        pass
    
    def check_clicked(self, mouse_pos: tuple[int, int]) -> bool:
        checking: bool = self._hitbox.collidepoint(mouse_pos)

        if checking:
            self.update()

        return checking

    def _draw_animation(self, screen: pg.Surface) -> None: pass

    def update_by_event(self, event: pg.event.Event) -> None: pass

    def set_position_attr(self, attr_pos: str, new_pos: tuple[int, int]) -> None:
        """Sets a position attribute for the button's hitbox.
        
            Args:
                attr_pos : 'center/topleft/topright/bottomleft/bottomright/...'
                new_pos : tuple[int, int]
        
            E.g.:
                attr_pos : 'center'
                new_pos : '(100, 100)'

                hitbox.center = (100, 100)
        """
        setattr(self._hitbox, attr_pos, new_pos)
        self._topleft = self._hitbox.topleft
