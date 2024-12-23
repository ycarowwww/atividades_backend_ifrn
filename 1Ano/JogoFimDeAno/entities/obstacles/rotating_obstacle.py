import pygame as pg
from entities.player import Player
from entities.obstacles.obstacle import Obstacle
from math import sqrt, pi, radians, cos, sin, asin

class RotatingObstacle(Obstacle):
    def __init__(self, x: int, y: int, width: int, height: int, speed: int, color: tuple[int, int, int], rotating_to_right: bool = True, initial_angle: int = 0):
        super().__init__(x, y, width, height, speed, color)
        self._angular_speed = radians(self._speed) * (1 if rotating_to_right else -1)
        self._circumscribed_circle_radius = sqrt(self._width ** 2 + self._height ** 2) / 2
        self._d_angle = 2 * asin((self._height / 2) / self._circumscribed_circle_radius)
        self._angle = radians(initial_angle) - self._d_angle / 2
        self._calculate_rotating_points()
    
    def update(self) -> None:
        self._y += self._speed
        self._angle += self._angular_speed

        self._calculate_rotating_points()

        self._position_tracker.append(self._points.copy())
        while len(self._position_tracker) >= self._max_positions_tracker:
            self._position_tracker.popleft()
    
    def draw(self, screen: pg.Surface) -> None:
        self._draw_tracker(screen)
        
        pg.draw.polygon(screen, self._color, self._points)
    
    def check_collision(self, player: Player) -> bool: # Need to be implemented
        return False

    def _draw_tracker(self, screen: pg.Surface) -> None:
        len_tracker: int = len(self._position_tracker)
        if len_tracker < 1: return

        ext_topleft = tuple(min(mpos) for mpos in zip(*[tuple(min(p) for p in zip(*pos)) for pos in self._position_tracker])) # What the hell is it? Idk, but works in O(n)
        ext_bottomright = tuple(max(mpos) for mpos in zip(*[tuple(max(p) for p in zip(*pos)) for pos in self._position_tracker])) # What the hell is it? Idk, but works in O(n)

        surf = pg.Surface((ext_bottomright[0] - ext_topleft[0], ext_bottomright[1] - ext_topleft[1]), flags=pg.SRCALPHA)
        surf.fill((0, 0, 0, 0))

        offset_points = [ [ (p[0] - ext_topleft[0], p[1] - ext_topleft[1]) for p in r ] for r in self._position_tracker ]

        for i in range(len_tracker):
            col = (*self._color, int(self._initial_alpha_tracker / len_tracker * (i + 1)))
            pg.draw.polygon(surf, col, offset_points[i])

            if i > 0: # Draw the "Connection lines" between the rects
                pg.draw.polygon(surf, col, (offset_points[i-1][0], offset_points[i][0], offset_points[i][3], offset_points[i-1][3]))
                pg.draw.polygon(surf, col, (offset_points[i-1][3], offset_points[i][3], offset_points[i][2], offset_points[i-1][2]))
                pg.draw.polygon(surf, col, (offset_points[i-1][0], offset_points[i][0], offset_points[i][1], offset_points[i-1][1]))
                pg.draw.polygon(surf, col, (offset_points[i-1][2], offset_points[i][2], offset_points[i][1], offset_points[i-1][1]))
        
        screen.blit(surf, ext_topleft)
    
    def _calculate_rotating_points(self) -> None:
        self._points = [
            [cos(self._angle) * self._circumscribed_circle_radius + self._x, sin(self._angle) * self._circumscribed_circle_radius + self._y], # topright
            [cos(self._angle + self._d_angle) * self._circumscribed_circle_radius + self._x, sin(self._angle + self._d_angle) * self._circumscribed_circle_radius + self._y], # bottomright
            [cos(self._angle + pi) * self._circumscribed_circle_radius + self._x, sin(self._angle + pi) * self._circumscribed_circle_radius + self._y],
            [cos(self._angle + self._d_angle + pi) * self._circumscribed_circle_radius + self._x, sin(self._angle + self._d_angle + pi) * self._circumscribed_circle_radius + self._y]
        ]
