import pygame as pg
from entities.buttons.button import Button
from scripts.settings import scale_dimension, scale_position
from typing import Callable

class ImageButton(Button):
    def __init__(self, size: tuple[int, int], position: tuple[int, int], attr_pos: str, action: Callable, img_path: str, padding: int = 0, border_size: int = 0, border_radius: int = 0, border_color: tuple[int, int, int] = None):
        self._base_image = pg.transform.scale(pg.image.load(img_path).convert_alpha(), size)
        self._image = pg.transform.scale(pg.image.load(img_path).convert_alpha(), size)
        self._border_color = border_color
        if self._border_color:
            self._base_padding = padding
            self._base_border_size = border_size
            self._base_border_radius = border_radius
            surf_size = [i + (self._base_padding + self._base_border_size) * 2 for i in size]
            self._surface = pg.Surface(surf_size)
            super().__init__(surf_size, position, attr_pos, action)
            pg.draw.rect(self._surface, self._border_color, pg.Rect((0, 0), surf_size), self._base_border_size, self._base_border_radius)
            self._surface.blit(self._image, self._image.get_rect(center=self._surface.get_rect().center))
        else:
            super().__init__(size, position, attr_pos, action)
            self._surface = pg.Surface(self._size)
            self._surface.blit(self._image, (0, 0))
        self._surface.set_colorkey((0, 0, 0))
    
    def draw(self, screen: pg.Surface):
        screen.blit(self._surface, self._hitbox.topleft)

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
        self._surface = pg.Surface(self._size)
        if self._border_color:
            padding = scale_dimension(self._base_padding, new_resolution)
            border_size = scale_dimension(self._base_border_size, new_resolution)
            border_radius = scale_dimension(self._base_border_radius, new_resolution)
            pg.draw.rect(self._surface, self._border_color, pg.Rect((0, 0), self._size), border_size, border_radius)
            self._image = pg.transform.scale(self._base_image, [i - (border_size + padding) * 2 for i in self._size])
            self._surface.blit(self._image, self._image.get_rect(center=self._surface.get_rect().center))
        else:
            self._image = pg.transform.scale(self._base_image, self._size)
            self._surface.blit(self._image, (0, 0))
        self._surface.set_colorkey((0, 0, 0))
