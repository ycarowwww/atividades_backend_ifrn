import pygame as pg
import pygame.freetype as pgft
from scripts import convert_decimal_to_roman, LEVELS_PERFECTION_UNLOCKED, COLORS
from typing import Callable

class LevelButton:
    def __init__(self, width: int, level: int, click_event: Callable[[], None], fgcolor: tuple[int, int, int], bgcolor: tuple[int, int, int], border_width: int, font: pgft.Font, font_size: int, topleft: tuple[int, int]):
        self._topleft = topleft
        self._width = width
        self._text = convert_decimal_to_roman(level)
        self._click_event = click_event
        self._border_width = border_width
        self._fgcolor = fgcolor
        self._bgcolor = bgcolor
        self._font = font
        self._font_size = font_size
        self._click_event = click_event
        self._is_perfect = LEVELS_PERFECTION_UNLOCKED.get(str(level))
        self._surface = self._generate_surface()
    
    def update_by_event(self, event: pg.Event) -> None:
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            if self._surface.get_rect(topleft=self._topleft).collidepoint(*event.pos):
                self._click_event()
    
    def _generate_surface(self) -> pg.Surface:
        surf = pg.Surface((self._width, self._width))
        surf.fill(self._bgcolor)

        pg.draw.rect(surf, self._fgcolor, pg.Rect((0, 0), (self._width, self._width)), self._border_width)

        if self._is_perfect:
            points = (
                (round(self._width / 5 * 3), 0),
                (round(self._width / 5 * 4), 0),
                (round(self._width), round(self._width / 5)),
                (round(self._width), round(self._width / 5 * 2))
            )
            pg.draw.polygon(surf, COLORS["GREEN"], points)

        text_surf, text_rect = self._font.render(self._text, self._fgcolor, size=self._font_size)
        text_rect.center = tuple(i // 2 for i in surf.size)
        surf.blit(text_surf, text_rect)

        return surf

    def increase_y(self, y_value: int) -> None: 
        self._topleft = (self._topleft[0], self._topleft[1] + y_value)

    def get_surface(self) -> pg.Surface: return self._surface
