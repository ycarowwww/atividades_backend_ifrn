import pygame as pg
import pygame.freetype as pgft

pg.init()

BASE_RESOLUTION: tuple[int, int] = (800, 600) # Base Resolution of the screen
PLAYER_ROTATION_VELOCITY: float = 5
FPS: float = 60.0
COLORS: dict[str, tuple[int, int, int, int | None]] = {
    "BLACK" : (0, 0, 0),
    "GRAY" : (50, 50, 50),
    "WHITE" : (255, 255, 255),
    "RED" : (255, 0, 0),
    "GREEN" : (0, 255, 0),
    "BLUE" : (35, 172, 255),
    "BLANK" : (0, 0, 0, 0)
}
GAME_FONT: pgft.Font = pgft.SysFont("Arial", 30, True, False)
MAX_SCORE_FONT: pgft.Font = pgft.SysFont("Arial", 15, False, False)
OBSTACLES_HEIGHT: int = 30
OBSTACLES_SPEED: int = int((240 + OBSTACLES_HEIGHT * 2) / (180 / PLAYER_ROTATION_VELOCITY)) # 240 is the distance + radius of the balls
MAX_POSITIONS_TRACKER: int = 5
INITIAL_ALPHA_TRACKER: int = 50
ROTATING_OBSTACLE_ANGULAR_SPEED: float = 180 / (240 / OBSTACLES_SPEED) # Implement Better

def blit_text(screen: pg.Surface, text: str, color: tuple[int, int, int], font: pgft.Font, position: tuple[int, int], attr_pos: str, *args, **kwargs) -> None:
    text_surface, text_rect = font.render(text, color, **kwargs)
    setattr(text_rect, attr_pos, position)
    screen.blit(text_surface, text_rect)

def scale_position(position: tuple[int, int], actual_resolution: tuple[int, int], new_resolution: tuple[int, int]) -> tuple[int, int]:
    return (round(position[0] / actual_resolution[0] * new_resolution[0]), round(position[1] / actual_resolution[1] * new_resolution[1]))

def scale_dimension(original_dimension: int, new_resolution: tuple[int, int]) -> int:
    return round(original_dimension * min(new_resolution[0] / BASE_RESOLUTION[0], new_resolution[1] / BASE_RESOLUTION[1]))
