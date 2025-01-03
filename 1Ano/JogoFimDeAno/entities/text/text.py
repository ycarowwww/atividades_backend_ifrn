import pygame as pg
import pygame.freetype as pgft
from scripts import scale_position, scale_dimension, BASE_RESOLUTION

class Text:
    def __init__(self, text: str, font: pgft.Font, color: tuple[int, int, int], pos: tuple[int, int], pos_attr: str = "topleft", size: float = 0, base_rslt: tuple[int, int] = BASE_RESOLUTION) -> None:
        self._text = text
        self._font = font
        self._color = color
        self._size = size
        self._pos = pos
        self._pos_attr = pos_attr
        self._base_size = self._size
        self._base_pos = self._pos
        self._base_resolution = base_rslt
        self.render()
    
    def render(self) -> None:
        self._text_surf, self._text_rect = self._font.render(self._text, self._color, size=self._size)
        setattr(self._text_rect, self._pos_attr, self._pos)
    
    def draw(self, screen: pg.Surface) -> None:
        screen.blit(self._text_surf, self._text_rect)
    
    def resize(self, new_resolution: tuple[int, int]) -> None:
        self._size = scale_dimension(self._base_size, new_resolution)
        self._pos = scale_position(self._base_pos, self._base_resolution, new_resolution)
        self.render()

    def set_text(self, new_text: str) -> None:
        self._text = new_text
        self.render()
