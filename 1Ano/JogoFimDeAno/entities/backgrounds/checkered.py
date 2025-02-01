import pygame as pg
from math import cos, sin, radians

class Checkered:
    """A Checkered Background."""
    def __init__(self, size: tuple[int, int], amount_rects: int, fgcolor: tuple[int, int, int], bgcolor: tuple[int, int, int], speed_mult: float = 1.0, angle: float = 0.0) -> None:
        """
        size: Screen's resolution.
        amount_rects: amount of columns and lines.
        fgcolor: Rects' Colors.
        bgcolor: Background Color.
        speed_mult: The Speed of the rects is equal to 1 rect size per second in each dimension, this number will multiply the speed.
        angle: The Angle that the rects are going to go.
        """
        self._amount = amount_rects
        self._fgcolor = fgcolor
        self._bgcolor = bgcolor
        self._speed_mult = speed_mult
        self._angle = radians(angle)
        self._size = size
        self._rect_size = tuple(s / self._amount for s in self._size)
        self._velocity = pg.Vector2(self._rect_size[0] * cos(self._angle) * self._speed_mult, self._rect_size[1] * sin(self._angle) * self._speed_mult)
        self._draw_rects()
        self._position = pg.Vector2(-2 * self._rect_size[0], -2 * self._rect_size[1])
        self._dts = pg.Vector2(0, 0)
    
    def update(self, dt: float) -> None:
        """Updates the actual position of the Checkered."""
        self._dts += (dt, dt)
        self._position += self._velocity * dt
        self._position.x %= -2 * self._rect_size[0]
        self._position.y %= -2 * self._rect_size[1]
        self._dts.x %= self._velocity.x / -2 * self._rect_size[0] # Maybe this isn't working for the "resize"
        self._dts.y %= self._velocity.y / -2 * self._rect_size[0]
    
    def draw(self, screen: pg.Surface) -> None:
        """Draws the Checkered Background on the 'screen'."""
        screen.blit(self._surface, self._position)
    
    def resize(self, new_size: tuple[int, int]) -> None:
        """Resize the Checkered Background for a new resolution 'new_size'."""
        self._size = new_size
        self._rect_size = tuple(s / self._amount for s in self._size)
        self._velocity = pg.Vector2(self._rect_size[0] * cos(self._angle) * self._speed_mult, self._rect_size[1] * sin(self._angle) * self._speed_mult)
        self._draw_rects()
        self._position.x += self._velocity.x * self._dts.x # Theoretically keeps the position of the checkered in the new resolution.
        self._position.y += self._velocity.y * self._dts.y
    
    def _draw_rects(self) -> None:
        """Create the surface and draws the checkered background on it. This surface will be move in relation to the screen to looks like that the background is moving."""
        self._surface = pg.Surface(tuple(self._size[i] + 4 * self._rect_size[i] for i in range(2)))
        self._surface.fill(self._bgcolor)
        points_x = [
            self._rect_size[0] * i for i in range(self._amount + 4)
        ]
        points_y = [
            self._rect_size[1] * i for i in range(self._amount + 4)
        ]
        self._draw_checkered(points_x, points_y)
    
    def _draw_checkered(self, points_x: list[tuple[int, int]], points_y: list[tuple[int, int]]) -> None:
        """Draws all the rects of the Checkered background on the surface."""
        for i in range(0, len(points_x), 2):
            for j in range(0, len(points_y), 2):
                self._draw_rect(points_x, points_y, i, j)

        for i in range(1, len(points_x), 2):
            for j in range(1, len(points_y), 2):
                self._draw_rect(points_x, points_y, i, j)

    def _draw_rect(self, points_x: list[tuple[int, int]], points_y: list[tuple[int, int]], index_x: int, index_y: int) -> None:
        """Draws a specific rect with the points."""
        pg.draw.rect(self._surface, self._fgcolor, pg.Rect((points_x[index_x], points_y[index_y]), self._rect_size))
