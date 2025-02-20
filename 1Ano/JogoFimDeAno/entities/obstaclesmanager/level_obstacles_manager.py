from scripts import LEVELS
from . import BaseObstaclesManager
from ..achievements import AchievementsHandler
from ..eventhandler import CustomEventHandler, CustomEventList
from copy import deepcopy

class LevelObstaclesManager(BaseObstaclesManager):
    """An Obstacle Manager that generates pre-defined obstacles (levels)."""
    def __init__(self, player_center: tuple[int, int], player_normal_distance: int, player_angular_speed: float, actual_level: int = 1) -> None:
        super().__init__(player_center, player_normal_distance, player_angular_speed)
        self._actual_level = max(1, actual_level)
        self._post_event = self._actual_level == 1 # Maybe improve this later

    def _generate_obstacles(self) -> None:
        """Load Current Level Obstacles."""
        if self._post_event and self._actual_level != 1:
            AchievementsHandler.unlock_achievement(1)
            self._post_event = False

        self._obstacles.clear()
        # Basically to convert the "standard" obstacles to the new resolution
        self._speed = self._base_obstacles_attrs[2]
        actual_center = self._player_center
        actual_distance = self._player_normal_distance
        self._player_center = self._base_obstacles_attrs[0]
        self._player_normal_distance = self._base_obstacles_attrs[1]

        indexes_lvl = LEVELS.get(f"{self._actual_level}")

        if indexes_lvl is None:
            # Raise custom event
            self._actual_level = 1
            indexes_lvl = LEVELS.get(f"{self._actual_level}")

        CustomEventHandler.post_event(CustomEventList.NEWLEVELWARNING, {"level" : self._actual_level})
        self._actual_level += 1

        for i in indexes_lvl:
            self._obstacles.append(deepcopy(self._possibles_obstacles[i]))
        
        self._amount_obstacles = len(self._obstacles)
        self._set_base_y()
        self._last_obstacle = self._obstacles[self._amount_obstacles-1]
        self.resize(self._actual_resolution, actual_center, actual_distance)
