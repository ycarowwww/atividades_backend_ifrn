import pygame as pg
import pygame.freetype as pgft
from entities.buttons.button import Button
from scripts.settings import scale_dimension, scale_position
from typing import Callable

class TextButton(Button):
    def __init__(self, position: tuple[int, int], attr_pos: str, action: Callable, text: str, font: pgft.Font, fgcolor: tuple[int, int, int] | None, bgcolor: tuple[int, int, int] | None = None, style: int = pgft.STYLE_DEFAULT, rotation: int = 0, size_font: float = 0, padding: int = 0):
        self._font_size = size_font
        self._padding = padding
        self._generate_text = lambda size: font.render(text, fgcolor, None, style, rotation, size)
        text_surf, text_rect = self._generate_text(self._font_size)
        self._box_surf = pg.Surface(text_rect.inflate(self._padding, self._padding).size)
        self._box_surf.set_colorkey((0, 0, 0))
        text_rect.center = self._box_surf.get_rect().center
        self._bg_color = bgcolor
        if self._bg_color:
            self._box_surf.fill(self._bg_color)
        self._box_surf.blit(text_surf, text_rect)
        super().__init__(self._box_surf.get_size(), position, attr_pos, action)
        self._base_font_size = self._font_size
        self._base_padding = self._padding
        self._base_position = self._position
    
    def draw(self, screen: pg.Surface) -> None:
        screen.blit(self._box_surf, self._hitbox.topleft)

    def update_by_event(self, event: pg.event.Event) -> None:
        if event.type == pg.MOUSEBUTTONDOWN:
            self.check_clicked(event.pos)
        
        if event.type == pg.VIDEORESIZE:
            self.resize(event.size)

    def resize(self, new_resolution: tuple[int, int]) -> None:
        self._padding = scale_dimension(self._base_padding, new_resolution)
        self._font_size = scale_dimension(self._base_font_size, new_resolution)
        text_surf, text_rect = self._generate_text(self._font_size)
        self._box_surf = pg.Surface(text_rect.inflate(self._padding, self._padding).size)
        self._box_surf.set_colorkey((0, 0, 0))
        text_rect.center = self._box_surf.get_rect().center
        if self._bg_color:
            self._box_surf.fill(self._bg_color)
        self._box_surf.blit(text_surf, text_rect)
        self._size = self._box_surf.get_size()
        self._hitbox.size = self._size
        self._position = scale_position(self._base_position, self._base_resolution, new_resolution)
        self.set_position_attr(self._attr_pos, self._position)
