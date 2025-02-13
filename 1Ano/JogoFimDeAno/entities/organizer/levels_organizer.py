import pygame as pg
import pygame.freetype as pgft
from scripts import scale_dimension, scale_position, BASE_RESOLUTION, LEVELS, convert_decimal_to_roman
from ..buttons import LevelButton
from math import ceil
from typing import Callable

class LevelsOrganizer:
    """A big surface that organizes the level buttons."""
    def __init__(self, width: int, midtop: tuple[int, int], level_button_width: int, max_amount_line: int, level_button_event: Callable[[int], Callable[..., None]], font: pgft.Font, amount: int = len(LEVELS)) -> None:
        if level_button_width * max_amount_line > width: raise ValueError("Levels Organizer : The Width of the Level Buttons cannot be Greater than the Width of the Level Organizer!")
        
        self._amount = amount
        self._width = width
        self._midtop = midtop
        self._button_width = level_button_width
        self._button_max = max_amount_line
        self._gap = (self._width - self._button_width * self._button_max) / (self._button_max + 1)
        self._buttons: list[LevelButton] = []
        self._level_button_function = level_button_event
        self._font = font
        self._surface = self._create_surface()
        self._mouse_wheel_speed = 5

        self._base_values = [self._width, self._midtop, self._button_width, self._mouse_wheel_speed]
        self._actual_resolution = BASE_RESOLUTION
    
    def update(self, dt: float) -> None: # Do something here later
        ...

    def draw(self, screen: pg.Surface) -> None:
        screen.blit(self._surface, self._surface.get_rect(midtop=self._midtop))
    
    def update_by_event(self, event: pg.Event) -> None:
        for btn in self._buttons:
            btn.update_by_event(event)

        if event.type == pg.VIDEORESIZE:
            self.resize(event.size)
        
        if event.type == pg.MOUSEWHEEL and self._surface.get_rect(midtop=self._midtop).collidepoint(pg.mouse.get_pos()):
            self._moving_y(event.y)

    def resize(self, new_resolution: tuple[int, int]) -> None:
        self._width = scale_dimension(self._base_values[0], new_resolution)
        self._midtop = scale_position(self._base_values[1], BASE_RESOLUTION, new_resolution)
        self._button_width = round(self._base_values[2] / self._base_values[0] * self._width)
        self._gap = (self._width - self._button_width * self._button_max) / (self._button_max + 1)
        self._mouse_wheel_speed = round(self._base_values[3] / self._base_values[0] * self._width)
        self._actual_resolution = new_resolution
        self._surface = self._create_surface()

    def _create_surface(self) -> pg.Surface:
        surf = pg.Surface((self._width, self._button_width * ceil(self._amount / 3) + self._gap * (1 + ceil(self._amount / 3))))
        surf.set_colorkey((0, 0, 0))

        surf_topleft = surf.get_rect(midtop=self._midtop).topleft
        start_pos = [self._gap, self._gap]

        for i in range(self._amount):
            btn_event = self._level_button_function(i+1)
            btn = LevelButton(
                self._button_width,
                convert_decimal_to_roman(i+1),
                btn_event,
                (255, 255, 255),
                (0, 0, 0),
                self._button_width // 15,
                self._font,
                self._button_width // 2,
                [start_pos[i] + surf_topleft[i] for i in range(2)]
            )
            self._buttons.append(btn)

            surf.blit(btn.get_surface(), start_pos)

            start_pos[0] += self._button_width + self._gap # Next button will be more to the left

            if start_pos[0] >= self._button_max * self._button_width + (self._button_max + 1) * self._gap: # If exceeds the max amount per line will be more down
                start_pos[0] = self._gap
                start_pos[1] += self._button_width + self._gap
        
        return surf

    def _moving_y(self, mouse_wheel_value: int) -> None:
        """Moves the surface in the 'y' direction in relation to the mouse wheel button (UP or DOWN)."""
        if self._surface.height <= self._actual_resolution[1]: return
        if mouse_wheel_value > 0 and self._midtop[1] >= 0: return
        if mouse_wheel_value < 0 and self._surface.get_rect(midtop=self._midtop).bottom < self._actual_resolution[1]: return

        shiftness = abs(self._mouse_wheel_speed * mouse_wheel_value)

        if mouse_wheel_value < 0:
            shiftness *= -1

        self._midtop = (self._midtop[0], self._midtop[1] + shiftness)

        for btn in self._buttons:
            btn.increase_y(shiftness)
