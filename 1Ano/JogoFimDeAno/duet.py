import pygame as pg
import pygame.freetype
from math import cos, sin, radians
from random import randint

pg.init()

SCREEN_SIZE: tuple[int, int] = (800, 600)
SCREEN_CENTER: tuple[int, int] = (SCREEN_SIZE[0]//2, SCREEN_SIZE[1]//2)
screen: pg.Surface = pg.display.set_mode(SCREEN_SIZE)
pg.display.set_caption("Duet PFA")
clock: pg.time.Clock = pg.time.Clock()
FPS: float = 60.0
COLORS: dict[str, tuple[int, int, int]] = {
    "BLACK" : (0, 0, 0),
    "GRAY" : (70, 70, 70),
    "WHITE" : (255, 255, 255),
    "RED" : (255, 0, 0),
    "GREEN" : (0, 255, 0),
    "BLUE" : (0, 0, 255)
}

class Player:
    def __init__(self, position: list[int], color: tuple[int, int, int], size: int, angle: int = 0) -> None:
        self.position = position
        self.color = color
        self.size = size
        self.angle = angle
        self.hitbox_rect = pg.Rect(0, 0, self.size, self.size)
        self.hitbox_rect.center = self.position
        self.positions_track = []
        self.distance = 100
    
    def update(self, screen: pg.Surface, point: tuple[int, int], key: pg.key.ScancodeWrapper) -> None:
        if key[pg.K_LSHIFT] and self.distance > 0:
            self.distance -= 5
        elif key[pg.K_SPACE] or self.distance < 100:
            self.distance += 5
        elif self.distance > 100:
            self.distance -= 5
        if key[pg.K_a]: self.angle -= 5
        if key[pg.K_d]: self.angle += 5
        self.angle %= 360

        self.rotate_to_center(point)
        self.draw(screen)
    
    def draw(self, screen: pg.Surface) -> None:
        track_length: int = len(self.positions_track)
        for line in range(track_length-1, 0, -1):
            line_width: int = int(-2 * self.size / track_length * line + 2 * self.size)
            line_color: list[int, int, int] = [-color / track_length * line + color for color in list(self.color)]
            pg.draw.line(screen, line_color, self.positions_track[line-1], self.positions_track[line], line_width)
            pg.draw.circle(screen, line_color, self.positions_track[line], line_width//2)
        
        pg.draw.circle(screen, self.color, self.position, self.size)

    def rotate_to_center(self, point: tuple[int, int]) -> None:
        self.position[0] = self.distance * cos(radians(self.angle)) + point[0]
        self.position[1] = self.distance * sin(radians(self.angle)) + point[1]
        self.hitbox_rect.center = self.position

        self.positions_track.insert(0, list(self.hitbox_rect.center)) # Usar uma Queue depois
        if len(self.positions_track) >= 30:
            self.positions_track.pop(-1)

        for line in range(1, len(self.positions_track)):
            self.positions_track[line][1] += 5

class Obstacle:
    def __init__(self, position: list[int], color: tuple[int, int, int], size: list[int]) -> None:
        self.position = position
        self.size = size
        self.color = color
        self.hitbox_rect = pg.Rect(self.position[0], self.position[1], self.size[0], self.size[1])
        self.speed = 270 / 36 # 200 (bigger" circle's radius) + 40 (balls' radois) + self.size = total height / time (180º / 5º) | Formula Temporary Removed
        self.positions_track = []
    
    def movement_bottom(self) -> None:
        self.position[1] += self.speed
        self.hitbox_rect.y = self.position[1]

        self.positions_track.insert(0, self.hitbox_rect.top) # Usar uma Queue depois
        if len(self.positions_track) >= 5:
            self.positions_track.pop(-1)
    
    def draw(self, screen: pg.Surface) -> None:
        track_length: int = len(self.positions_track)
        for line in range(track_length-1, 0, -1):
            line_width: int = self.size[0]
            line_color: list[int, int, int] = [-color / track_length * line + color for color in list(self.color)]
            pg.draw.line(screen, line_color, (self.hitbox_rect.centerx, self.positions_track[line-1]), (self.hitbox_rect.centerx, self.positions_track[line]), line_width)
        
        pg.draw.rect(screen, self.color, self.hitbox_rect)

def blit_text(screen: pg.Surface, message: str, color: tuple[int, int, int], topleft: tuple[int, int], font: pygame.freetype.Font) -> None:
    text_surface, text_rect = font.render(message, color)
    text_rect.topleft = topleft
    screen.blit(text_surface, text_rect)

player1: Player = Player(list(SCREEN_CENTER), COLORS["BLUE"], 20)
player2: Player = Player(list(SCREEN_CENTER), COLORS["RED"], 20, 180)

player_angle: int = 0
OBSTACLE_SIZE: int = 30
obstacles_list: list[Obstacle] = [Obstacle([0, -OBSTACLE_SIZE], COLORS["WHITE"], [SCREEN_SIZE[0]//2, OBSTACLE_SIZE])]
GAME_FONT: pygame.freetype.Font = pygame.freetype.SysFont("Arial", 30, True, False)
MAX_SCORE_FONT: pygame.freetype.Font = pygame.freetype.SysFont("Arial", 15, False, False)
punctuation: int = 0
max_score: int = 0

running: bool = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    clock.tick(FPS)
    screen.fill(COLORS["BLACK"])

    pg.draw.circle(screen, COLORS["GRAY"], SCREEN_CENTER, player1.distance, 5)

    key: pg.key.ScancodeWrapper = pg.key.get_pressed()

    player1.update(screen, SCREEN_CENTER, key)
    player2.update(screen, SCREEN_CENTER, key)

    for rect in obstacles_list:
        rect.movement_bottom()
        rect.draw(screen)
        
        if rect.hitbox_rect.collidelist([player1.hitbox_rect, player2.hitbox_rect]) != -1:
            punctuation = 0

    if obstacles_list[0].position[1] >= SCREEN_SIZE[1]:
        obstacles_list.pop(0)
        
    if len([rect for rect in obstacles_list if rect.position[1] >= 240]) - len(obstacles_list) >= 0:
        rnd_num: int = randint(1, 5)

        match rnd_num:
            case 1:
                obstacles_list.append(Obstacle([0, -OBSTACLE_SIZE], COLORS["WHITE"], [SCREEN_SIZE[0]//2, OBSTACLE_SIZE]))
            case 2:
                obstacles_list.append(Obstacle([SCREEN_CENTER[0], -OBSTACLE_SIZE], COLORS["WHITE"], [SCREEN_SIZE[0]//2, OBSTACLE_SIZE]))
            case 3:
                obstacles_list.append(Obstacle([SCREEN_CENTER[0], -SCREEN_CENTER[0]], COLORS["WHITE"], [OBSTACLE_SIZE, SCREEN_SIZE[0]//2]))
                obstacles_list[-1].hitbox_rect.centerx = SCREEN_CENTER[0]
            case 4:
                obstacles_list.append(Obstacle([SCREEN_CENTER[0] - SCREEN_SIZE[0]//8, -OBSTACLE_SIZE - 150], COLORS["WHITE"], [SCREEN_SIZE[0]//4, OBSTACLE_SIZE]))
            case 5:
                obstacles_list.append(Obstacle([0, -OBSTACLE_SIZE], COLORS["WHITE"], [SCREEN_SIZE[0]//2 - 100, OBSTACLE_SIZE]))
                obstacles_list.append(Obstacle([SCREEN_CENTER[0] + 100, -OBSTACLE_SIZE], COLORS["WHITE"], [SCREEN_SIZE[0]//2 - 100, OBSTACLE_SIZE]))
        
        punctuation += 1
        max_score = max(max_score, punctuation)
    
    blit_text(screen, f"Score: {punctuation}", COLORS["WHITE"], (10, 10), GAME_FONT)
    blit_text(screen, f"Max: {max_score}", COLORS["GREEN"], (10, 40), MAX_SCORE_FONT)
    
    pg.display.flip()

pg.quit()
