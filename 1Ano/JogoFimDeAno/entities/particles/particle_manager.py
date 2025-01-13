import pygame as pg
from . import CircleParticle, ShockwaveParticle
from random import uniform
# Maybe we need to set a new resolution method
class ParticleManager:
    def __init__(self, start_pos: tuple[float, float], amount: int, main_speed: float, main_size: float, color: tuple[int, int, int], original_resolution: tuple[int, int]) -> None:
        self._central_pos = start_pos
        self._color = color
        self._amount = amount
        self._particles: list[CircleParticle | ShockwaveParticle] = [ # Add Sparkles and Shockwaves later
            CircleParticle(self._central_pos, main_speed * uniform(1, 2), uniform(0, 360), main_size * uniform(1, 3), 0.5, color) # 0.5 == event time | Maybe change this later
            for _ in range(self._amount)
        ] # Maybe also a way to define what to add and a base particle class like the "Obstacle".
        self._particles.append(ShockwaveParticle(self._central_pos, 0, main_size * 5, main_speed * 1.5, 0.5, self._color))
        self._original_resolution = original_resolution
    
    def update(self, dt: float) -> None:
        for i in self._particles:
            i.update(dt)
    
        for i in range(len(self._particles)-1, -1, -1):
            if not self._particles[i].check_visible():
                self._particles.pop(i)
    
    def draw(self, screen: pg.Surface) -> None:
        for i in self._particles:
            i.draw(screen)
    
    def resize(self, new_pos: tuple[float, float], new_resolution: tuple[int, int]) -> None: # Needs to be improved because that "Original Resolution" needs to be the "BASE_RESOLUTION"
        self._central_pos = new_pos

        for p in self._particles:
            p.resize(self._central_pos, new_resolution, self._original_resolution)
    
    def get_start_pos(self) -> tuple[float, float]: return self._central_pos
