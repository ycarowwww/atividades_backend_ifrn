import pygame as pg
from math import cos, sin, pi
from random import uniform

class PlayerParticles:
    def __init__(self, start_pos: tuple[float, float], amount: int, main_speed: float, main_size: float, color: tuple[int, int, int]) -> None:
        self._amount = amount
        self._speed = [ main_speed * uniform(1, 2) for _ in range(self._amount) ]
        self._positions = [ list(start_pos).copy() for _ in range(self._amount) ]
        self._angles = [ uniform(0, 2 * pi) for _ in range(self._amount) ]
        self._sizes = [ main_size * uniform(1, 3) for _ in range(self._amount) ]
        self._size_decrease_speed = 1
        self._color = color
    
    def update(self, dt: float) -> None:
        indexes_to_delete = []
        for i in range(self._amount):
            self._positions[i][0] += cos(self._angles[i]) * self._speed[i] * dt
            self._positions[i][1] += sin(self._angles[i]) * self._speed[i] * dt
            self._sizes[i] -= self._size_decrease_speed * dt
            if self._sizes[i] <= 0:
                indexes_to_delete.append(i)
        
        for i in indexes_to_delete[::-1]:
            self._positions.pop(i)
            self._angles.pop(i)
            self._sizes.pop(i)
            self._amount -= 1
        
    def draw(self, screen: pg.Surface) -> None:
        for i in range(self._amount):
            pg.draw.circle(screen, self._color, self._positions[i], self._sizes[i])
