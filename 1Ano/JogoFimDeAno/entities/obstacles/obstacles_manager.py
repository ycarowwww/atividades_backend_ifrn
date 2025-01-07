import pygame as pg
from .obstacle import Obstacle
from .rotating_obstacle import RotatingObstacle
from .standard_obstacles import get_obstacle_list
from ..player import Player
from ..eventhandler import *
from scripts import OBSTACLES_HEIGHT, COLORS, BASE_RESOLUTION, get_file_path
from copy import deepcopy
from json import load as json_load
from random import choice, randint

class ObstaclesManager:
    def __init__(self, player_center: tuple[int, int], player_normal_distance: int, player_angular_speed: float, load_level: bool = False, actual_level: int = 0) -> None:
        self._obstacles: list[Obstacle] = []
        self._last_obstacle: Obstacle = None
        self._amount_obstacles: int = 0
        self._speed = player_normal_distance * 2 / (180 / player_angular_speed)
        self._height = OBSTACLES_HEIGHT
        self._color = COLORS["WHITE"]
        self._start_distance_mult = 8
        self._player_center = player_center
        self._player_normal_distance = player_normal_distance
        self._possibles_obstacles: list[Obstacle] = get_obstacle_list(self._player_center, self._player_normal_distance, player_angular_speed, self._height, self._speed, self._color)
        self._base_obstacles_attrs = (self._player_center, self._player_normal_distance, self._speed)
        self._actual_resolution = BASE_RESOLUTION
        self._total_score = 0
        self._actual_score = 0
        self._load_level = load_level
        self._actual_level = actual_level - 1
    
    def update(self, dt: float) -> None:
        for obstacle in self._obstacles:
            obstacle.update(dt)
        
        if self._last_obstacle == None or self._last_obstacle.get_y() - self._player_center[1] > self._player_normal_distance * 3:
            self._generate_obstacles()

    def draw(self, screen: pg.Surface) -> None:
        for obstacle in self._obstacles:
            obstacle.draw(screen)

    def check_collision(self, player: Player) -> None: # Implement Better
        for obstacle in self._obstacles:
            if obstacle.check_collision(player):
                self._set_base_y()
                player.reset_rotation()
        
        self._calculate_actual_score()
    
    def set_new_resolution(self, new_resolution: tuple[int, int], player_center: tuple[int, int], player_normal_distance: int) -> None:
        self._speed = self._speed / self._player_normal_distance * player_normal_distance

        for obst in self._obstacles:
            obst.set_new_resolution(new_resolution, (self._player_center, self._player_normal_distance), (player_center, player_normal_distance), self._speed)
        
        self._player_center = player_center
        self._player_normal_distance = player_normal_distance
        self._actual_resolution = new_resolution

    def _generate_obstacles(self) -> None:
        self._total_score += self._actual_score
        self._actual_score = 0
        self._obstacles.clear()
        # Basically to convert the "standard" obstacles to the new resolution
        self._speed = self._base_obstacles_attrs[2]
        actual_center = self._player_center
        actual_distance = self._player_normal_distance
        self._player_center = self._base_obstacles_attrs[0]
        self._player_normal_distance = self._base_obstacles_attrs[1]

        if self._load_level:
            self._actual_level += 1

            with open(get_file_path("../data/levels.json")) as file:
                levels: dict[str, list[int]] = json_load(file)

            indexes_lvl = levels.get(f"{self._actual_level}")

            if indexes_lvl is None:
                # Raise custom event
                self._actual_level = 1
                indexes_lvl = levels.get(f"{self._actual_level}")

            for i in indexes_lvl:
                self._obstacles.append(deepcopy(self._possibles_obstacles[i]))
            
            self._amount_obstacles = len(self._obstacles)
            
            CustomEventHandler.post_event(CustomEventList.NEWLEVELWARNING, {"level" : self._actual_level})
        else:
            self._amount_obstacles = randint(10, 20)
            self._obstacles.append(deepcopy(choice(self._possibles_obstacles)))

            for _ in range(1, self._amount_obstacles): # Maybe integrate with "_set_base_y()"
                new_obstacle = deepcopy(choice(self._possibles_obstacles))
                self._obstacles.append(new_obstacle)
        
        self._set_base_y()
        
        self._last_obstacle = self._obstacles[self._amount_obstacles-1]

        self.set_new_resolution(self._actual_resolution, actual_center, actual_distance)
    
    def _calculate_actual_score(self) -> None:
        self._actual_score = round(self._start_distance_mult - (self._player_center[1] - self._obstacles[0].get_y()) / self._player_normal_distance)
    
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

    def get_score(self) -> int: return self._total_score + self._actual_score
