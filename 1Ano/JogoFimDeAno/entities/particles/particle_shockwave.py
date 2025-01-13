import pygame as pg
from scripts import scale_dimension

class ShockwaveParticle:
    def __init__(self, pos: tuple[float, float], radius: float, width: float, speed_expansion: float, lifetime: float, color: tuple[int, int, int]) -> None:
        self._pos = pos
        self._radius = radius
        self._width = width
        self._speed_expansion = speed_expansion
        self._decrease_width_rate = self._width / lifetime
        self._color = color
        self._time_elapsed = 0.0
        self._base_radius = self._radius
        self._base_width = self._width
        self._base_speed_expansion = self._speed_expansion
        self._base_decrease_width_rate = self._decrease_width_rate
    
    def update(self, dt: float) -> None:
        self._radius += self._speed_expansion * dt
        self._width -= self._decrease_width_rate * dt
        self._time_elapsed += dt
    
    def draw(self, screen: pg.Surface) -> None:
        self._draw_shadow(screen)
        
        pg.draw.circle(screen, self._color, [round(i) for i in self._pos], round(self._radius), round(self._width))

    def _draw_shadow(self, screen: pg.Surface) -> None:
        shadow_rad = round(self._radius * 0.9) # Makes the "Inner Shadow" farther than the normal radius 

        surf = pg.Surface((shadow_rad * 2, shadow_rad * 2))
        surf.set_colorkey((0, 0, 0))
        surf.set_alpha(100)
        pg.draw.circle(surf, self._color, (shadow_rad, shadow_rad), shadow_rad, round(self._width * 2))

        screen.blit(surf, surf.get_rect(center=[round(i) for i in self._pos]))
    
    def check_visible(self) -> bool:
        return self._width >= 1
    
    def resize(self, new_central_pos: tuple[float, float], new_resolution: tuple[int, int], original_resolution: tuple[int, int]) -> None:
        self._pos = new_central_pos
        self._speed_expansion = scale_dimension(self._base_speed_expansion, new_resolution, original_resolution)
        self._radius = scale_dimension(self._base_radius, new_resolution, original_resolution) + self._speed_expansion * self._time_elapsed
        self._decrease_width_rate /= self._width
        self._width = scale_dimension(self._base_width, new_resolution, original_resolution)
        self._decrease_width_rate *= self._width
        self._width -= self._decrease_width_rate * self._time_elapsed
