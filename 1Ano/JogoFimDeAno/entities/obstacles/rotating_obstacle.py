import pygame as pg
from . import Obstacle
from ..player import Player
from ..stains import generate_stain
from scripts import ROTATING_OBSTACLE_ANGULAR_SPEED, scale_dimension
from math import sqrt, pi, radians, cos, sin, asin, degrees

class RotatingObstacle(Obstacle):
    def __init__(self, x: int, y: int, width: int, height: int, speed: int, spacing_mult: float, color: tuple[int, int, int], angular_speed: float = ROTATING_OBSTACLE_ANGULAR_SPEED, rotating_to_right: bool = True, initial_angle: int = 0):
        super().__init__(x, y, width, height, speed, spacing_mult, color)
        self._angular_speed = radians(angular_speed) * (1 if rotating_to_right else -1)
        self._circumscribed_circle_radius = sqrt(self._width ** 2 + self._height ** 2) / 2
        self._d_angle = 2 * asin((self._height / 2) / self._circumscribed_circle_radius)
        self._angle = radians(initial_angle) - self._d_angle / 2
        self._points = self._calculate_rotating_points(self._angle)
    
    def update(self, dt: float) -> None:
        self._y += self._speed * dt
        self._angle += self._angular_speed * dt

        self._points = self._calculate_rotating_points(self._angle)

        self._update_tracker(dt)
    
    def draw(self, screen: pg.Surface) -> None:
        self._draw_tracker(screen)

        pg.draw.polygon(screen, self._color, self._points)
        
        self._draw_ink_stains(screen)
    
    def check_collision(self, player: Player) -> tuple[bool, list[int]]:
        """Check Collision between the Player and the Obstacle.
        
            First, it'll rotate each position of the circles relative to the center of the rectangle, then calculate the nearest point and check the distance.
        """
        if sqrt((self._x - player.get_center()[0]) ** 2 + (self._y - player.get_center()[1]) ** 2) > player.get_distance() + player.get_radius() + self._circumscribed_circle_radius: 
            return (False, [])

        angle = self._angle + self._d_angle / 2
    
        for i in range(player.get_amount()):
            player_relative_center = player.get_positions()[i].copy()
            player_relative_center[0] -= self._x
            player_relative_center[1] -= self._y

            new_x = player_relative_center[0] * cos(-angle) - player_relative_center[1] * sin(-angle)
            new_y = player_relative_center[1] * cos(-angle) + player_relative_center[0] * sin(-angle)
            player_relative_center = [new_x, new_y]

            nearest_x = min(self._width / 2, max(-self._width / 2, player_relative_center[0]))
            nearest_y = min(self._height / 2, max(-self._height / 2, player_relative_center[1]))
            distance = sqrt((player_relative_center[0] - nearest_x) ** 2 + (player_relative_center[1] - nearest_y) ** 2)

            if distance < player.get_radius(): 
                self._has_ink_stain = True
                self._paint_new_stain((nearest_x, nearest_y), player.get_radius(), player.get_colors()[i])
                return (True, [i])
        
        return (False, [])

    def set_new_resolution(self, new_resolution: tuple[int, int], old_player_info: tuple[tuple[int, int], int], new_player_info: tuple[tuple[int, int], int], new_speed: float) -> None:
        self._speed = new_speed
        
        self._width = scale_dimension(self._base_width, new_resolution)
        self._height = scale_dimension(self._base_height, new_resolution)
        self._circumscribed_circle_radius = sqrt(self._width ** 2 + self._height ** 2) / 2
        # self._points = self._calculate_rotating_points(self._angle)

        y_ratio = (old_player_info[0][1] - self._y) / old_player_info[1]
        new_y = new_player_info[0][1] - y_ratio * new_player_info[1]
        self.set_y(new_y)

        x_ratio = (self._x - old_player_info[0][0]) / old_player_info[1]
        new_x = new_player_info[0][0] + x_ratio * new_player_info[1]
        self.set_x(new_x)

        for i in range(len(self._position_tracker)):
            time = self._position_tracker_lifetime - self._position_tracker_times[i]
            self._position_tracker[i] = self._calculate_rotating_points(self._angle - self._angular_speed * time)

    def _update_tracker(self, dt: float) -> None:
        for i in range(len(self._position_tracker_times)):
            self._position_tracker_times[i] -= dt
        
        self._position_tracker.append(self._points.copy())
        self._position_tracker_times.append(self._position_tracker_lifetime)

        remove_to = next((j for j, e in enumerate(self._position_tracker_times) if e > 0), len(self._position_tracker_times))
        for _ in range(remove_to):
            self._position_tracker.popleft()
            self._position_tracker_times.popleft()

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
    
    def _draw_ink_stains(self, screen: pg.Surface) -> None:
        if not self._has_ink_stain: return

        self._update_ink_stain()

        screen.blit(self._ink_stain_surface, self._ink_stain_surface.get_rect(center=(round(self._x), round(self._y))))
    
    def _paint_new_stain(self, pos: tuple[float, float], size: float, color: tuple[int, int, int]) -> None:
        ratio_pos = (
            round((pos[0] - (-self._width / 2)) / self._width * self._base_width),
            round((pos[1] - (-self._height / 2)) / self._height * self._base_height)
        )

        rad = round(size * self._base_width / self._width)

        generate_stain(self._base_ink_stain_surface, ratio_pos, rad, color, rad * 1.5)
    
    def _update_ink_stain(self) -> None:
        self._ink_stain_surface = pg.transform.scale(self._base_ink_stain_surface, (self._width, self._height))
        self._ink_stain_surface = pg.transform.rotate(self._ink_stain_surface, -degrees(self._angle + self._d_angle / 2))

    def _calculate_rotating_points(self, ang: float) -> tuple[tuple[float, float], tuple[float, float], tuple[float, float], tuple[float, float]]:
        return [
            [cos(ang) * self._circumscribed_circle_radius + self._x, sin(ang) * self._circumscribed_circle_radius + self._y], # topright
            [cos(ang + self._d_angle) * self._circumscribed_circle_radius + self._x, sin(ang + self._d_angle) * self._circumscribed_circle_radius + self._y], # bottomright
            [cos(ang + pi) * self._circumscribed_circle_radius + self._x, sin(ang + pi) * self._circumscribed_circle_radius + self._y],
            [cos(ang + self._d_angle + pi) * self._circumscribed_circle_radius + self._x, sin(ang + self._d_angle + pi) * self._circumscribed_circle_radius + self._y]
        ]
    
    def set_angle(self, angle: float) -> None:
        self._angle = radians(angle) - self._d_angle / 2
        self._points = self._calculate_rotating_points(self._angle)

    def set_x(self, new_x: float) -> None: 
        self._x = new_x
        self._points = self._calculate_rotating_points(self._angle)
    
    def set_y(self, new_y: float) -> None:
        self._y = new_y
        self._points = self._calculate_rotating_points(self._angle)
