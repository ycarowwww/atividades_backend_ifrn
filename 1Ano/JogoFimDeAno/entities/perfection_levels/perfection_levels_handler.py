from scripts import get_file_path, LEVELS_PERFECTION_UNLOCKED
from json import dump as json_dump

class PerfectionLevelsHandler:
    """Class with methods to handle the perfection level's logic."""
    @staticmethod
    def unlock_perfection(level: int) -> None:
        """Unlock and edit the json file keeping the player perfection levels progress."""
        if LEVELS_PERFECTION_UNLOCKED.get(str(level)) == None: # Level doesn't exist
            raise IndexError(f"PerfectionLevelsHandler: Unknown Level: {level}")
        elif LEVELS_PERFECTION_UNLOCKED[str(level)]: return # level already unlocked

        LEVELS_PERFECTION_UNLOCKED[str(level)] = True
        with open(get_file_path("../data/player_perfection_levels.json"), "w", encoding="utf-8") as file: # Modern way to write a file.
            json_dump(LEVELS_PERFECTION_UNLOCKED, file, ensure_ascii=False, indent=4)
