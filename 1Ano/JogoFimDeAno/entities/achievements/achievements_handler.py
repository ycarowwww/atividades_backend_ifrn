from ..eventhandler import CustomEventHandler, CustomEventList
from scripts import get_file_path, ACHIEVEMENTS_UNLOCKED
from json import dump as json_dump

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
        
        CustomEventHandler.post_event(CustomEventList.ACHIEVEMENTUNLOCKED, { "id" : str(achievement_id) })
