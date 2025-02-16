import pygame as pg
from scripts import ACHIEVEMENTS, ACHIEVEMENTS_UNLOCKED

class AchievementsGrid: # REALLY Incomplete
    def __init__(self, size: tuple[int, int]) -> None:
        self._achievements = ACHIEVEMENTS
        self._achievements_unlocked = ACHIEVEMENTS_UNLOCKED
