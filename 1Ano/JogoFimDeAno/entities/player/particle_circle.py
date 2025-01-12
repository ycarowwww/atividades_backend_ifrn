import pygame as pg
from math import cos, sin, radians

class CircleParticle:
    def __init__(self, start_pos: tuple[float, float], speed: float, angle: float, radius: float, lifetime: float, color: tuple[int, int, int]) -> None:
        self._pos = list(start_pos)
        self._speed = speed
        self._angle = angle
        self._radius = radius
        self._velocity = pg.Vector2(cos(radians(self._angle)), sin(radians(self._angle))) * self._speed
        self._decrease_rate = self._radius / lifetime
        self._color = color
    
    def update(self, dt: float) -> None:
        self._radius -= self._decrease_rate * dt
        self._pos[0] += self._velocity.x * dt
        self._pos[1] += self._velocity.y * dt
    
    def draw(self, screen: pg.Surface) -> None:
        self._draw_shadow(screen)
        
        pg.draw.circle(screen, self._color, [round(i) for i in self._pos], round(self._radius))

    def _draw_shadow(self, screen: pg.Surface) -> None:
        shadow_rad = round(self._radius * 1.5)

        surf = pg.Surface((shadow_rad * 2, shadow_rad * 2))
        surf.set_colorkey((0, 0, 0))
        surf.set_alpha(100)
        pg.draw.circle(surf, self._color, (shadow_rad, shadow_rad), shadow_rad)

        screen.blit(surf, surf.get_rect(center=[round(i) for i in self._pos]))
    
    def change_angle(self, new_angle: float) -> None:
        self._angle = new_angle
        self._velocity = pg.Vector2(cos(radians(self._angle)), sin(radians(self._angle))) * self._speed
    
    def check_visible(self) -> bool:
        return self._radius > 0
