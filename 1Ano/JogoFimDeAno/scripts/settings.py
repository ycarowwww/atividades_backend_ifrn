import pygame as pg
import pygame.freetype as pgft

pg.init()

BASE_RSLT = (800, 600) # Base Resolution of the screen
PLAYER_ROTATION_VELOCITY: float = 5
SCREEN_SIZE: tuple[int, int] = BASE_RSLT
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

def scale_dimension(value: float, base_rslt: tuple[int, int], current_res: tuple[int, int]) -> int:
    width_factor = current_res[0] / base_rslt[0]
    height_factor = current_res[1] / base_rslt[1]
    return value * min(width_factor, height_factor)

def unscale_dimension(value: float, base_rslt: tuple[int, int], current_res: tuple[int, int]) -> int:
    width_factor = current_res[0] / base_rslt[0]
    height_factor = current_res[1] / base_rslt[1]
    return value * max(width_factor, height_factor)

def scale_position(pos: tuple[int, int], base_rslt: tuple[int, int], current_res: tuple[int, int]) -> tuple[int, int]:
    width_factor = current_res[0] / base_rslt[0]
    height_factor = current_res[1] / base_rslt[1]
    return (pos[0] * width_factor, pos[1] * height_factor)
