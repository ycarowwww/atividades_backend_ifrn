import pygame as pg
from scripts import scale_dimension, scale_position, BASE_RESOLUTION
from enum import IntEnum, auto

class OrganizerDirection(IntEnum):
    HORIZONTAL = auto()
    VERTICAL = auto()

class OrganizerOrientation(IntEnum):
    TOP = auto()
    MIDDLE = auto()
    BOTTOM = auto()

class Organizer:
    """organizes a list of surfaces that are relatively close together."""
    def __init__(self, surfaces: list[pg.Surface], direction: int, orientation: int, gap: int, pos_attr: str, pos_value: tuple[int, int]) -> None:
        self._surfaces = surfaces # List of images of the Organizer
        self._direction = direction # Vertical or Horizontal
        self._orientation = orientation # orientation of the opposite side of the direction
        self._gap = gap # Spacing between the Images
        self._pos_attr = pos_attr
        self._pos_value = pos_value
        self._create_surface()
        self._save_values = [self._pos_attr, self._pos_value, self._surface_rect.size, self._surface.copy()] # Save some values for resizing.
        self._current_resolution = BASE_RESOLUTION

    def _create_surface(self) -> None:
        """Draws each one of the surfaces in a main surface. Also creates it too."""
        if self._direction == OrganizerDirection.HORIZONTAL:
            width = sum(i.width for i in self._surfaces) + self._gap * (len(self._surfaces) - 1)
            height = max(i.height for i in self._surfaces)

            surf = pg.Surface((width, height))

            initial_left = 0

            if self._orientation == OrganizerOrientation.TOP:
                y_attr = "top"
                y_val = 0
            elif self._orientation == OrganizerOrientation.MIDDLE:
                y_attr = "centery"
                y_val = height // 2
            else:
                y_attr = "bottom"
                y_val = height
            
            for s in self._surfaces: # Positioning each surface in the main surface.
                s_rect = s.get_rect(left=initial_left)
                setattr(s_rect, y_attr, y_val)
                surf.blit(s, s_rect)
                initial_left += s_rect.width + self._gap
        else:
            width = max(i.width for i in self._surfaces)
            height = sum(i.height for i in self._surfaces) + self._gap * (len(self._surfaces) - 1)

            surf = pg.Surface((width, height))

            initial_top = 0

            if self._orientation == OrganizerOrientation.TOP:
                x_attr = "left"
                x_val = 0
            elif self._orientation == OrganizerOrientation.MIDDLE:
                x_attr = "centerx"
                x_val = width // 2
            else:
                x_attr = "right"
                x_val = width
            
            for s in self._surfaces: # Positioning each surface in the main surface.
                s_rect = s.get_rect(top=initial_top)
                setattr(s_rect, x_attr, x_val)
                surf.blit(s, s_rect)
                initial_top += s_rect.height + self._gap
        
        self._surface = surf
        self._surface.set_colorkey((0, 0, 0))
        self._surface_rect = self._surface.get_rect()
        setattr(self._surface_rect, self._pos_attr, self._pos_value)

    def draw(self, screen: pg.Surface) -> None:
        screen.blit(self._surface, self._surface_rect)

    def resize(self, new_resolution: tuple[int, int]) -> None:
        self._pos_value = scale_position(self._save_values[1], BASE_RESOLUTION, new_resolution)
        new_size = (
            scale_dimension(self._save_values[2][0], new_resolution, BASE_RESOLUTION),
            scale_dimension(self._save_values[2][1], new_resolution, BASE_RESOLUTION)
        )
        self._surface = pg.transform.scale(self._save_values[3], new_size)
        self._surface_rect = self._surface.get_rect()
        setattr(self._surface_rect, self._pos_attr, self._pos_value)
        self._current_resolution = new_resolution # Maybe this can be improved

    def change_surfaces(self, new_surfaces: list[pg.Surface]) -> None:
        self._surfaces = new_surfaces
        self._create_surface()
        self._save_values[2] = self._surface.size
        self._save_values[3] = self._surface.copy()
        self.resize(self._current_resolution)
