import pygame as pg
from ..eventhandler import CustomEventHandler, CustomEventList
from ..obstacles import Obstacle, RotatingObstacle, InvisibleObstacle, get_obstacle_list
from ..player import Player
from scripts import OBSTACLES_HEIGHT, COLORS, BASE_RESOLUTION
from typing import Callable

class BaseObstaclesManager:
    def __init__(self, player_center: tuple[int, int], player_normal_distance: int, player_angular_speed: float, obstacle_list: Callable[..., list[Obstacle]] = get_obstacle_list) -> None:
        self._obstacles: list[Obstacle] = []
        self._last_obstacle: Obstacle = None
        self._amount_obstacles: int = 0
        self._speed = player_normal_distance * 2 / (180 / player_angular_speed)
        self._height = OBSTACLES_HEIGHT
        self._color = COLORS["WHITE"]
        self._start_distance_mult = 8
        self._player_center = player_center
        self._player_normal_distance = player_normal_distance
        self._possibles_obstacles: list[Obstacle] = obstacle_list(self._player_center, self._player_normal_distance, player_angular_speed, self._height, self._speed, self._color)
        self._base_obstacles_attrs = (self._player_center, self._player_normal_distance, self._speed)
        self._actual_resolution = BASE_RESOLUTION
        self._player_count_collisions = 0
    
    def update(self, dt: float) -> None:
        for obstacle in self._obstacles:
            obstacle.update(dt)
        
        if self._last_obstacle == None or self._last_obstacle.get_y() - self._player_center[1] > self._player_normal_distance * 3: # Change this "3" later
            self._generate_obstacles()

    def draw(self, screen: pg.Surface) -> None:
        for obstacle in self._obstacles:
            if isinstance(obstacle, InvisibleObstacle): # Checkar a transparência do obstáculo invisível
                obstacle.check_distance(self._player_center, self._player_normal_distance)

            obstacle.draw(screen)

    def check_collision(self, player: Player) -> None: # Implement Better
        player_collided = False
        for obstacle in self._obstacles:
            detection, circles_indexes = obstacle.check_collision(player)
            if detection:
                player_collided = True
                CustomEventHandler.post_event(CustomEventList.PLAYERCOLLISION, { "indexes" : circles_indexes })
        
        if player_collided: self._increase_player_collision_count()
    
    def resize(self, new_resolution: tuple[int, int], player_center: tuple[int, int], player_normal_distance: int) -> None:
        self._speed = self._speed / self._player_normal_distance * player_normal_distance

        for obst in self._obstacles:
            obst.set_new_resolution(new_resolution, (self._player_center, self._player_normal_distance), (player_center, player_normal_distance), self._speed)
        
        self._player_center = player_center
        self._player_normal_distance = player_normal_distance
        self._actual_resolution = new_resolution

    def _generate_obstacles(self) -> None: ...
    
    def _increase_player_collision_count(self) -> None:
        self._player_count_collisions += 1
    
    def reset(self) -> None:
        self._set_base_y()

    def _set_base_y(self) -> None:
        for i in range(self._amount_obstacles):
            if i == 0: 
                new_y = self._player_center[1] - self._start_distance_mult * self._player_normal_distance
            else: 
                new_y = self._obstacles[i-1].get_y() - max(self._obstacles[i-1].get_spacing_mult(), self._obstacles[i].get_spacing_mult()) * self._player_normal_distance
            self._obstacles[i].set_y(new_y)

            if isinstance(self._obstacles[i], RotatingObstacle):
                ratiodist = (self._player_center[1] - new_y) / self._player_normal_distance
                self._obstacles[i].set_angle((ratiodist % 2) * 90)

    def set_new_color(self, color: tuple[int, int, int]) -> None:
        self._color = color
        
        for obst in self._possibles_obstacles:
            obst.set_color(color)

        for obst in self._obstacles:
            obst.set_color(color)

    def get_player_collision_count(self) -> int: return self._player_count_collisions
