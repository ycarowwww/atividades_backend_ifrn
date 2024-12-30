import pygame as pg
from entities.player import Player
from entities.obstacles.obstacle import Obstacle

class ObstacleGroup:
    """A group of obstacles acting as one."""
    def __init__(self, obstacles: list[Obstacle] = []):
        self._amount = len(obstacles)
        self._obstacles = obstacles
        self._obstacles.sort(key=lambda obst: obst.get_y(), reverse=True)
        yobst0 = self._obstacles[0].get_y()
        for i in self._obstacles:
            i.set_y(i.get_y() - yobst0)

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
        centerx = self.get_x()
        ratio = new_x / centerx
        for i in range(self._amount):
            dist = self._obstacles[i].get_x() - centerx
            self._obstacles[i].set_x(dist * ratio)

    def set_y(self, new_y: float) -> None: 
        if self._amount <= 0: return
        dists = [self._obstacles[i-1].get_y() - self._obstacles[i].get_y() for i in range(1, self._amount)]
        self._obstacles[0].set_y(new_y)
        for i in range(1, self._amount):
            self._obstacles[i].set_y(self._obstacles[i-1].get_y() + dists[i-1])

    def set_speed(self, new_speed: float) -> None:
        for obst in self._obstacles:
            obst.set_speed(new_speed)

    def get_x(self) -> int: 
        if self._amount == 0: return -1

        return sum(obst.get_x() for obst in self._obstacles) / self._amount

    def get_y(self) -> int: 
        if self._amount == 0: return -1

        return self._obstacles[self._amount-1].get_y()

    def get_spacing_mult(self) -> float: 
        return max(self._obstacles, key=lambda obst: obst.get_spacing_mult()).get_spacing_mult()
