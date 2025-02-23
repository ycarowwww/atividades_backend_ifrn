import pygame as pg
from scripts import get_file_path, scale_dimension, scale_position, BASE_RESOLUTION
from ..mousehandler import MouseHandler
from math import sqrt
from typing import Callable

class CircularImageButton:
    def __init__(self, pos: tuple[int, int], pos_attr: str, img_path: str, img_size: tuple[int, int], padding: int, border_size: int, border_color: tuple[int, int, int], hover_time: float, hover_color: tuple[int, int, int], action: Callable[[], None]) -> None:
        self._pos = pos
        self._pos_attr = pos_attr
        self._original_image = pg.image.load(get_file_path(f"../images/{img_path}")).convert_alpha()
        self._img_size = img_size
        self._padding = padding
        self._border_size = border_size
        self._colors = (border_color, hover_color)
        self._action = action
        self._surface, self._surface_rect, self._radius = self._generate_surface()
        self._hover_time = hover_time
        self._current_hover_process = 0
        self._is_hovered = False

        self._save_values = (self._pos, self._img_size, self._padding, self._border_size)

    def update(self, dt: float) -> None:
        if self._is_hovered:
            MouseHandler.change_cursor(pg.SYSTEM_CURSOR_HAND)
            self._current_hover_process += dt / self._hover_time

            if self._current_hover_process > 1:
                self._current_hover_process = 1
        else:
            self._current_hover_process -= dt / self._hover_time

            if self._current_hover_process < 0:
                self._current_hover_process = 0

    def draw(self, screen: pg.Surface) -> None:
        hovers = self._generate_hover_surface()
        screen.blit(hovers[0], hovers[1])
        
        screen.blit(self._surface, self._surface_rect)
    
    def update_by_event(self, event: pg.Event) -> None:
        if event.type == pg.VIDEORESIZE:
            self.resize(event.size)
        
        if event.type == pg.MOUSEMOTION:
            self._check_hover(event.pos)

        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1: # 1 == Left Button
            self._do_action()

    def resize(self, new_resolution: tuple[int, int]) -> None:
        self._pos = scale_position(self._save_values[0], BASE_RESOLUTION, new_resolution)
        img_size_ratio = self._save_values[1][1] / self._save_values[1][0]
        img_size_width = scale_dimension(self._save_values[1][0], new_resolution)
        self._img_size = (img_size_width, img_size_width * img_size_ratio)
        self._padding = scale_dimension(self._save_values[2], new_resolution)
        self._border_size = scale_dimension(self._save_values[3], new_resolution)
        self._surface, self._surface_rect, self._radius = self._generate_surface()

    def _check_hover(self, pos: tuple[int, int]) -> None:
        self._is_hovered = False
        distance = sqrt((self._pos[0] - pos[0]) ** 2 + (self._pos[1] - pos[1]) ** 2)

        if distance <= self._radius:
            self._is_hovered = True

    def _do_action(self) -> None:
        if self._is_hovered:
            self._action()

    def _generate_surface(self) -> tuple[pg.Surface, pg.Rect, float]:
        img = pg.transform.scale(self._original_image, self._img_size)
        total_radius = sqrt(img.width ** 2 + img.height ** 2) / 2 + self._padding + self._border_size

        surf = pg.Surface((total_radius * 2, total_radius * 2), pg.SRCALPHA)
        
        if self._border_size > 0:
            pg.draw.circle(surf, self._colors[0], (total_radius, total_radius), total_radius, self._border_size)
        surf.blit(img, img.get_rect(center=(total_radius, total_radius)))

        surf_rect = surf.get_rect()
        setattr(surf_rect, self._pos_attr, self._pos)

        return (surf, surf_rect, total_radius)

    def _generate_hover_surface(self) -> tuple[pg.Surface, pg.Rect]:
        if self._current_hover_process <= 0:
            return (pg.Surface((0, 0)), pg.Rect(0, 0, 0, 0))
        
        size = self._radius - self._border_size
        surf = pg.Surface((size * 2, size * 2), pg.SRCALPHA)

        pg.draw.circle(surf, (*self._colors[1], 255 * self._current_hover_process), (size, size), size)
        surf_rect = surf.get_rect(center=self._surface_rect.center)
        
        return (surf, surf_rect)
