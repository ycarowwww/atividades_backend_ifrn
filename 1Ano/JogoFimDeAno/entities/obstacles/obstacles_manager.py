import pygame as pg
from entities.player import Player
from entities.obstacles.obstacle import Obstacle
from entities.obstacles.stationary_obstacle import StationaryObstacle
from entities.obstacles.rotating_obstacle import RotatingObstacle
from entities.obstacles.obstacle_group import ObstacleGroup
from scripts.settings import OBSTACLES_HEIGHT, OBSTACLES_SPEED, SCREEN_SIZE, COLORS
from copy import deepcopy
from random import choice

class ObstaclesManager:
    """An Obstacle Manager that randomly generates certain obstacles."""
    def __init__(self) -> None:
        self._obstacles: list[Obstacle] = []
        self._centerx = SCREEN_SIZE[0] // 2
        self._speed = OBSTACLES_SPEED
        self._height = OBSTACLES_HEIGHT
        self._gap = 240 # Implement Better
        self._color = COLORS["WHITE"]
        self._possibles_obstacles = [ # Implement Better
            StationaryObstacle(self._centerx - 300, -self._height, 300, self._height, self._speed, self._color),
            StationaryObstacle(self._centerx, -self._height, 300, self._height, self._speed, self._color),
            StationaryObstacle(self._centerx - 100, -self._height, 200, self._height, self._speed, self._color),
            ObstacleGroup([StationaryObstacle(self._centerx - 300, -self._height, 200, self._height, self._speed, self._color), StationaryObstacle(self._centerx + 100, -self._height, 200, self._height, self._speed, self._color)]),
            RotatingObstacle(self._centerx, -self._height, 200, self._height, self._speed, self._color),
            RotatingObstacle(self._centerx, -self._height, 200, self._height, self._speed, self._color, rotating_to_right=False)
        ]
        self._obstacle_removed = False
    
    def _add_obstacle(self, obstacle: Obstacle) -> None: # Implement Better
        self._obstacles.append(obstacle)

    def _remove_obstacle(self, obstacle: Obstacle) -> None: # Implement Better
        self._obstacles.remove(obstacle)

    def update(self) -> None:
        obstacles_to_remove: list[Obstacle] = [] # Implement Better | Maybe use a queue
        self._obstacle_removed = False
        
        for obstacle in self._obstacles:
            obstacle.update()

            if obstacle.get_y() > SCREEN_SIZE[1]: # Implement Better
                obstacles_to_remove.append(obstacle)
                self._obstacle_removed = True
        
        for obstacle in obstacles_to_remove: # Implement Better
            self._remove_obstacle(obstacle)
        
        if len(self._obstacles) == 0 or len(self._obstacles) > 0 and self._obstacles[-1].get_y() > self._gap: # Implement Better
            self._add_obstacle(deepcopy(choice(self._possibles_obstacles))) # Implement Better

    def draw(self, screen: pg.Surface) -> None:
        for obstacle in self._obstacles:
            obstacle.draw(screen)

    def check_collision(self, player: Player) -> bool: # Implement Better
        for obstacle in self._obstacles:
            if obstacle.check_collision(player):
                return True
        
        return False

    def get_obstacle_removed(self) -> bool: return self._obstacle_removed
