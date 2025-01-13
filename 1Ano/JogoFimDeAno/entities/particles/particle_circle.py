import pygame as pg
from scripts import scale_dimension
from math import cos, sin, radians

class CircleParticle:
    def __init__(self, start_pos: tuple[float, float], speed: float, angle: float, radius: float, lifetime: float, color: tuple[int, int, int]) -> None:
        self._pos = list(start_pos)
        self._speed = speed
        self._angle = angle
        self._radius = radius
        self._velocity = pg.Vector2(cos(radians(self._angle)), sin(radians(self._angle))) * self._speed
        self._time_elapsed = 0.0
        self._decrease_rate = self._radius / lifetime
        self._color = color
        self._base_pos = self._pos.copy()
        self._base_radius = self._radius
        self._base_speed = self._speed
        self._base_decrease_rate = self._decrease_rate
    
    def update(self, dt: float) -> None:
        self._radius -= self._decrease_rate * dt
        self._pos[0] += self._velocity.x * dt
        self._pos[1] += self._velocity.y * dt
        self._time_elapsed += dt
    
    def draw(self, screen: pg.Surface) -> None:
        self._draw_brightness(screen)
        
        pg.draw.circle(screen, self._color, [round(i) for i in self._pos], round(self._radius))

    def _draw_brightness(self, screen: pg.Surface) -> None:
        brightness_rad = round(self._radius * 1.5)

        surf = pg.Surface((brightness_rad * 2, brightness_rad * 2))
        surf.set_colorkey((0, 0, 0))
        surf.set_alpha(100)
        pg.draw.circle(surf, self._color, (brightness_rad, brightness_rad), brightness_rad)

        screen.blit(surf, surf.get_rect(center=[round(i) for i in self._pos]))
    
    def change_angle(self, new_angle: float) -> None:
        self._angle = new_angle
        self._velocity = pg.Vector2(cos(radians(self._angle)), sin(radians(self._angle))) * self._speed
    
    def check_visible(self) -> bool:
        return self._radius > 0
    
    def resize(self, new_central_pos: tuple[float, float], new_resolution: tuple[int, int], original_resolution: tuple[int, int]) -> None:
        self._velocity /= self._speed
        self._decrease_rate /= self._radius
        self._speed = scale_dimension(self._base_speed, new_resolution, original_resolution)
        self._radius = scale_dimension(self._base_radius, new_resolution, original_resolution)
        self._velocity *= self._speed
        self._decrease_rate *= self._radius
        self._pos = list(new_central_pos) + self._velocity * self._time_elapsed
