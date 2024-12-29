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

    def update(self, dt: float) -> None:
        for obstacle in self._obstacles:
            obstacle.update(dt)

    def draw(self, screen: pg.Surface) -> None:
        for obstacle in self._obstacles:
            obstacle.draw(screen)
    
    def check_collision(self, player: Player) -> bool:
        for obstacle in self._obstacles:
            if obstacle.check_collision(player):
                return True
        
        return False

    def set_new_resolution(self, new_resolution: tuple[int, int]) -> None:
        for obstacle in self._obstacles:
            obstacle.set_new_resolution(new_resolution)

    def set_x(self, new_x: float) -> None: 
        if self._amount <= 0: return
        difference_xs = [self._obstacles[i-1].get_x() - self._obstacles[i].get_x() for i in range(1, self._amount)]
        self._obstacles[0].set_x(new_x)
        for i in range(1, self._amount):
            self._obstacles[i].set_x(new_x + difference_xs[i-1])

    def set_y(self, new_y: float) -> None: 
        if self._amount <= 0: return
        difference_ys = [self._obstacles[i-1].get_y() - self._obstacles[i].get_y() for i in range(1, self._amount)]
        self._obstacles[0].set_y(new_y)
        for i in range(1, self._amount):
            self._obstacles[i].set_y(new_y + difference_ys[i-1])

    def get_y(self) -> int: 
        if self._amount == 0: return -1

        return min(self._obstacles, key=lambda obst: obst.get_y()).get_y()

    def get_spacing_mult(self) -> float: 
        return max(self._obstacles, key=lambda obst: obst.get_spacing_mult()).get_spacing_mult()
