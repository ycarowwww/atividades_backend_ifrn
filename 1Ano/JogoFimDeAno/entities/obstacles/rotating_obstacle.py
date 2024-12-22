import pygame as pg
from entities.obstacles.obstacle import Obstacle
from math import sqrt, pi, radians, cos, sin, asin

class RotatingObstacle(Obstacle): # It's Incomplete
    def __init__(self, x: int, y: int, width: int, height: int, speed: int, color: tuple[int, int, int], initial_angle: int = 0):
        super().__init__(x, y, width, height, speed, color)
        self._angle = radians(initial_angle)
        self._calculate_difference_angle()
        self._calculate_rotating_points()
    
    def update(self) -> None:
        keys = pg.key.get_pressed()

        if keys[pg.K_a]:
            self._center[0] -= self._speed
        if keys[pg.K_d]:
            self._center[0] += self._speed
        if keys[pg.K_w]:
            self._center[1] -= self._speed
        if keys[pg.K_s]:
            self._center[1] += self._speed

        if keys[pg.K_LEFT]:
            self._angle -= radians(self._speed)
        if keys[pg.K_RIGHT]:
            self._angle += radians(self._speed)

        self._calculate_rotating_points()

        self._position_tracker.append(list(self._rect.topleft))
        while len(self._position_tracker) >= self._max_positions_tracker:
            self._position_tracker.popleft()
    
    def draw(self, screen: pg.Surface) -> None:
        pg.draw.polygon(screen, self._color, self._points)
    
    def _calculate_difference_angle(self) -> None:
        self._center = [(self._x + (self._x + self._width)) / 2, (self.y + (self.y + self._height)) / 2]
        self._circumscribed_circle_radius = sqrt(self._width ** 2 + self._height ** 2) / 2
        self._d_angle = 2 * asin((self._height / 2) / self._circumscribed_circle_radius)
        self._angle -= self._d_angle / 2
    
    def _calculate_rotating_points(self) -> None:
        self._points = [
            [cos(self._angle) * self._circumscribed_circle_radius + self._center[0], sin(self._angle) * self._circumscribed_circle_radius + self._center[1]],
            [cos(self._angle  + self._d_angle) * self._circumscribed_circle_radius + self._center[0], sin(self._angle + self._d_angle) * self._circumscribed_circle_radius + self._center[1]],
            [cos(self._angle + pi) * self._circumscribed_circle_radius + self._center[0], sin(self._angle + pi) * self._circumscribed_circle_radius + self._center[1]],
            [cos(self._angle + self._d_angle + pi) * self._circumscribed_circle_radius + self._center[0], sin(self._angle + self._d_angle + pi) * self._circumscribed_circle_radius + self._center[1]]
        ]
