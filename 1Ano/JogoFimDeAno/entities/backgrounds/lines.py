import pygame as pg

class Lines:
    """A Diagonal Lines Background."""
    def __init__(self, amount_lines: int, screen_size: tuple[int, int], speed_multiplier: float, fgcolor: tuple[int, int, int], bgcolor: tuple[int, int, int], moving_left: bool = True, inverse_vertical: bool = False) -> None:
        self._amount = amount_lines
        self._size = screen_size
        self._distance_between_lines = self._size[0] / self._amount
        self._moving_horizontal_mult = -1 if moving_left else 1
        self._inverse_vertical = inverse_vertical
        self._speed = self._distance_between_lines * speed_multiplier * self._moving_horizontal_mult
        self._fgcolor = fgcolor
        self._bgcolor = bgcolor
        self._create_background()
        self._surface_x = 0
        
    def update(self, dt: float) -> None:
        self._surface_x += self._speed * dt
        self._surface_x %= 2 * self._distance_between_lines
        self._surface_x -= 2 * self._distance_between_lines
    
    def draw(self, screen: pg.Surface) -> None:
        screen.blit(self._surface, (self._surface_x, 0))

    def resize(self, new_size: tuple[int, int]) -> None:
        self._size = new_size
        self._speed /= self._distance_between_lines
        self._distance_between_lines = self._size[0] / self._amount
        self._speed *= self._distance_between_lines
        self._create_background()
    
    def _create_background(self) -> None:
        self._surface = pg.Surface((self._size[0] + 2 * self._distance_between_lines, self._size[1])) # Creates a surface a bit longer than the screen draw one more line to the movement.
        self._surface.fill(self._bgcolor)
        # Creates points on the left and on the top of the surface equally spaced.
        points_x = [
            (
                self._size[0] * i / self._amount,
                0
            )
            for i in range(2 * self._amount + 2)
        ]
        points_y = [
            (
                0,
                self._size[1] * i / self._amount
            )
            for i in range(2 * self._amount + 2)
        ]
        # Draws trapeziums with these points.
        for i in range(0, 2 * self._amount + 2, 2):
            pg.draw.polygon(self._surface, self._fgcolor, (
                points_x[i], points_x[i+1], points_y[i+1], points_y[i]
            ))
        
        if self._inverse_vertical:
            self._surface = pg.transform.flip(self._surface, False, True)
