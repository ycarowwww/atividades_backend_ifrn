import pygame as pg
from scripts.settings import BASE_RESOLUTION
from typing import Callable

class Button:
    """Button Template Class for the others Buttons."""
    def __init__(self, size: tuple[int, int], position: tuple[int, int], attr_pos: str, action: Callable, base_resolution: tuple[int, int] = BASE_RESOLUTION):
        self._size = size
        self._position = position
        self._attr_pos = attr_pos
        self._hitbox = pg.Rect(self._position, self._size)
        self.set_position_attr(self._attr_pos, self._position)
        self._action = action
        self._base_size = self._size
        self._base_position = self._position
        self._base_resolution = base_resolution
    
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

    def update_by_event(self, event: pg.event.Event) -> None: pass

    def resize(self, new_resolution: tuple[int, int]) -> None: pass

    def _draw_animation(self, screen: pg.Surface) -> None: pass

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
        self._position = new_pos
        setattr(self._hitbox, attr_pos, self._position)
