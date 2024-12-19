import pygame as pg
import pygame.freetype as pgft
from entities.buttons.button import Button
from typing import Callable

class TextButton(Button):
    def __init__(self, topleft: tuple[int, int], action: Callable, text: str, font: pgft.Font, fgcolor: tuple[int, int, int] | None, bgcolor: tuple[int, int, int] | None = None, style: int = pgft.STYLE_DEFAULT, rotation: int = 0, size_font: float = 0, padding: int = 0):
        text_surf, text_rect = font.render(text, fgcolor, None, style, rotation, size_font)
        self._box_surf = pg.Surface(text_rect.inflate(padding, padding).size)
        self._box_surf.set_colorkey((0, 0, 0))
        text_rect.center = self._box_surf.get_rect().center
        if bgcolor:
            self._box_surf.fill(bgcolor)
        self._box_surf.blit(text_surf, text_rect)
        super().__init__(self._box_surf.get_size(), topleft, action)
    
    def update(self) -> None:
        print("Clickado")
        self._action()
    
    def draw(self, screen: pg.Surface) -> None:
        screen.blit(self._box_surf, self._topleft)
    
    def check_clicked(self, mouse_pos: tuple[int, int]) -> bool:
        checking: bool = self._hitbox.collidepoint(mouse_pos)

        if checking:
            self.update()

        return checking

    def update_by_event(self, event: pg.event.Event) -> None:
        if event.type == pg.MOUSEBUTTONDOWN:
            self.check_clicked(event.pos)
