import pygame as pg
from . import CircleParticle
from random import uniform
# Maybe we need to set a new resolution method
class PlayerParticleManager:
    def __init__(self, start_pos: tuple[float, float], amount: int, main_speed: float, main_size: float, color: tuple[int, int, int]) -> None:
        self._color = color
        self._amount = amount
        self._particles = [ # Add Sparkles and Shockwaves later
            CircleParticle(start_pos, main_speed * uniform(1, 2), uniform(0, 360), main_size * uniform(1, 3), 1, color)
            for _ in range(self._amount)
        ] # Maybe also a way to define what to add and a base particle class like the "Obstacle".
    
    def update(self, dt: float) -> None:
        for i in self._particles:
            i.update(dt)
    
        for i in range(len(self._particles)-1, -1, -1):
            if not self._particles[i].check_visible():
                self._particles.pop(i)
    
    def draw(self, screen: pg.Surface) -> None:
        for i in self._particles:
            i.draw(screen)
