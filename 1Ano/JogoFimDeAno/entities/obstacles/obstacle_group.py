import pygame as pg
from entities.player import Player
from entities.obstacles.obstacle import Obstacle

class ObstacleGroup:
    """A group of obstacles acting as one."""
    def __init__(self, start_obstacles: list[Obstacle] = []):
        self._amount = len(start_obstacles)
        self._obstacles = start_obstacles
    
    def add_obstacle(self, obstacle: Obstacle) -> None:
        self._amount += 1
        self._obstacles.append(obstacle)

    def update(self) -> None:
        for obstacle in self._obstacles:
            obstacle.update()

    def draw(self, screen: pg.Surface) -> None:
        for obstacle in self._obstacles:
            obstacle.draw(screen)
    
    def check_collision(self, player: Player) -> bool:
        for obstacle in self._obstacles:
            if obstacle.check_collision(player):
                return True
        
        return False

    def get_y(self) -> int: 
        if self._amount == 0: return -1
        return self._obstacles[0].get_y()
