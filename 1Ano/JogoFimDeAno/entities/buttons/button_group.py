import pygame as pg
from . import Button
from scripts import scale_dimension, scale_position, BASE_RESOLUTION

class ButtonGroup:
    def __init__(self, center: tuple[int, int], start_buttons: list[Button], gap: float, is_horizontal: bool = True) -> None:
        self._center = center
        self._buttons = start_buttons
        self._gap = gap
        self._is_horizontal = is_horizontal
        self._set_positions()
        self._base_gap = self._gap
        self._base_center = self._center
    
    def draw(self, screen: pg.Surface) -> None:
        for btn in self._buttons:
            btn.draw(screen)
        
    def update_by_event(self, event: pg.event.Event) -> None:
        if event.type == pg.VIDEORESIZE:
            self.resize(event.size)
            return
        
        for btn in self._buttons:
            btn.update_by_event(event)
    
    def resize(self, new_resolution: tuple[int, int]) -> None:
        for btn in self._buttons:
            btn.resize(new_resolution)
        
        self._gap = scale_dimension(self._base_gap, new_resolution)
        self._center = scale_position(self._base_center, BASE_RESOLUTION, new_resolution)
        self._set_positions()
    
    def add_button(self, new_button: Button) -> None:
        self._buttons.append(new_button)
        self._set_positions()
    
    def pop_button(self, index: int = -1) -> None:
        self._buttons.pop(index)
        self._set_positions()
    
    def _set_positions(self) -> None:
        if self._is_horizontal: # Need to better this later
            half_total_length = (sum(btn.get_size()[0] for btn in self._buttons) + self._gap * (len(self._buttons) - 1)) / 2

            start_left = self._center[0] - half_total_length

            self._buttons[0].set_position_attr("midleft", (start_left, self._center[1]))
            acc_size = 0

            for i in range(1, len(self._buttons)):
                acc_size += self._buttons[i-1].get_size()[0] + self._gap
                left = start_left + acc_size
                self._buttons[i].set_position_attr("midleft", (left, self._center[1]))
        else:
            half_total_length = (sum(btn.get_size()[1] for btn in self._buttons) + self._gap * (len(self._buttons) - 1)) / 2

            start_top = self._center[1] - half_total_length

            self._buttons[0].set_position_attr("midtop", (self._center[0], start_top))
            acc_size = 0

            for i in range(1, len(self._buttons)):
                acc_size += self._buttons[i-1].get_size()[1] + self._gap
                top = start_top + acc_size
                self._buttons[i].set_position_attr("midtop", (self._center[0], top))
