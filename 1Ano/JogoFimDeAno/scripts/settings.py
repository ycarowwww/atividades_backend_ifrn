import pygame as pg
import pygame.freetype as pgft

pg.init()

PLAYER_ROTATION_VELOCITY: float = 5
SCREEN_SIZE: tuple[int, int] = (800, 600)
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

def blit_text(screen: pg.Surface, message: str, color: tuple[int, int, int], topleft: tuple[int, int], font: pgft.Font) -> None:
    text_surface, text_rect = font.render(message, color)
    text_rect.topleft = topleft
    screen.blit(text_surface, text_rect)
