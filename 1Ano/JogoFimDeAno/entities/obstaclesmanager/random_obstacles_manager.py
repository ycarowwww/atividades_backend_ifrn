from . import BaseObstaclesManager
from ..eventhandler import CustomEventHandler, CustomEventList
from copy import deepcopy
from random import choice, randint

class RandomObstaclesManager(BaseObstaclesManager):
    """An Obstacle Manager that generates the obstacles with a random generation."""
    def __init__(self, player_center: tuple[int, int], player_normal_distance: int, player_angular_speed: float, lives: int) -> None:
        super().__init__(player_center, player_normal_distance, player_angular_speed)
        self._lives = lives
        self._actual_score = 0
        self._total_score = 0
        
    def _generate_obstacles(self) -> None:
        """Generate Random Obstacles."""
        self._calculate_actual_score()
        self._total_score += self._actual_score
        self._actual_score = 0
        self._obstacles.clear()
        # Basically to convert the "standard" obstacles to the new resolution
        self._speed = self._base_obstacles_attrs[2]
        actual_center = self._player_center
        actual_distance = self._player_normal_distance
        self._player_center = self._base_obstacles_attrs[0]
        self._player_normal_distance = self._base_obstacles_attrs[1]
        self._lives = min(3, self._lives + 1) # Maybe change this after

        self._amount_obstacles = randint(10, 20)
        self._obstacles.append(deepcopy(choice(self._possibles_obstacles)))

        for _ in range(1, self._amount_obstacles): # Maybe integrate with "_set_base_y()"
            new_obstacle = deepcopy(choice(self._possibles_obstacles))
            self._obstacles.append(new_obstacle)
        
        CustomEventHandler.post_event(CustomEventList.NEWGENERATIONWARNING)
        
        self._set_base_y()
        
        self._last_obstacle = self._obstacles[self._amount_obstacles-1]

        self.resize(self._actual_resolution, actual_center, actual_distance)

    def _calculate_actual_score(self) -> None:
        if len(self._obstacles) <= 0: self._actual_score = 0
        else: self._actual_score = round(self._start_distance_mult - (self._player_center[1] - self._obstacles[0].get_y()) / self._player_normal_distance)

    def _increase_player_collision_count(self) -> None:
        self._player_count_collisions += 1
        self._lives -= 1

    def check_player_lost(self) -> bool: 
        """Returns if the remaining lives are less than or equal to 0."""
        return self._lives <= 0

    def get_score(self) -> int: 
        self._calculate_actual_score()
        return self._total_score + self._actual_score

    def get_remaining_lives(self) -> int: return self._lives
