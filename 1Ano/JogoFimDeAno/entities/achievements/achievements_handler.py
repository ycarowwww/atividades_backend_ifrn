import pygame as pg
from ..eventhandler import CustomEventHandler, CustomEventList
from scripts import FONT, get_file_path, ACHIEVEMENTS, ACHIEVEMENTS_UNLOCKED
from json import dump as json_dump
from os.path import isfile
# Maybe we can add a dict[achiev_id : achiev_surf], a save_array and a method to draw it.
class AchievementsHandler:
    """Class with methods to handle the achievement's logic."""
    @staticmethod
    def unlock_achievement(achievement_id: int) -> None:
        """Unlock and edit the json file keeping the player achievements progress."""
        if ACHIEVEMENTS_UNLOCKED.get(str(achievement_id)) == None: # Achievement doesn't exist
            raise IndexError(f"AchievementsHandler: Unknown Achievement ID: {achievement_id}")
        elif ACHIEVEMENTS_UNLOCKED[str(achievement_id)]: return # Achievement already unlocked

        ACHIEVEMENTS_UNLOCKED[str(achievement_id)] = True
        with open(get_file_path("../data/player_achievements_unlocked.json"), "w", encoding="utf-8") as file: # Modern way to write a file.
            json_dump(ACHIEVEMENTS_UNLOCKED, file, ensure_ascii=False, indent=4)
        
        CustomEventHandler.post_event(CustomEventList.ACHIEVEMENTUNLOCKED, { "id" : achievement_id })
    
    @staticmethod
    def get_animation_unlock(achievement_id: int) -> pg.Surface: # Improve this later (add img and resizing, e.g.)
        title_surf, title_rect = FONT.render("Achievement Unlocked!", (255, 255, 255), size=20)
        text_surf, text_rect = FONT.render(ACHIEVEMENTS[str(achievement_id)]["title"], (255, 255, 255), size=15)
        gap = 5

        surf = pg.Surface((max(title_rect.width, text_rect.width) + gap * 2, title_rect.height + text_rect.height + gap * 3))
        pg.draw.rect(surf, (50, 50, 50), pg.Rect((0, 0), surf.size), border_radius=5)

        title_rect.topleft = (gap, gap)
        text_rect.topleft = (gap, gap * 2 + title_rect.height)

        surf.blit(title_surf, title_rect)
        surf.blit(text_surf, text_rect)

        return surf
    
    @staticmethod
    def get_achievement_image(achievement_id: int) -> pg.Surface | None:
        path = get_file_path(f"../images/achievements/{achievement_id}.svg")
        if not isfile(path): return None

        return pg.image.load(path)
