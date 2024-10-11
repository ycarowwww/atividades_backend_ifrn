import pygame as pg
import pygame.freetype
from math import cos, sin, radians
from random import choice

pg.init()

COLORS: dict[str, tuple[int, int, int]] = {
    "BLACK" : (0, 0, 0),
    "WHITE" : (255, 255, 255),
    "RED" : (255, 0, 0),
    "GREEN" : (0, 255, 0),
    "BLUE" : (0, 0, 255)
}

SCREEN_SIZE: tuple[int, int] = (800, 600)
SCREEN_CENTER: tuple[int, int] = (SCREEN_SIZE[0]//2, SCREEN_SIZE[1]//2)
screen: pg.Surface = pg.display.set_mode(SCREEN_SIZE)
pg.display.set_caption("Duet PFA")
clock: pg.time.Clock = pg.time.Clock()
FPS: float = 60.0

class Player:
    def __init__(self, position: list[int], color: tuple[int, int, int], size: int, angle: int = 0) -> None:
        self.position = position
        self.color = color
        self.size = size
        self.angle = angle
        self.hitbox_rect = pg.Rect(0, 0, self.size, self.size)
        self.hitbox_rect.center = self.position
        self.positions_track = []
    
    def update(self, screen: pg.Surface, point: tuple[int, int], distance: int, key: pg.key.ScancodeWrapper) -> None:
        if key[pg.K_a]: self.angle -= 5
        if key[pg.K_d]: self.angle += 5
        self.angle %= 360

        self.rotate_to_center(point, distance)
        self.draw(screen)
    
    def draw(self, screen: pg.Surface) -> None:
        track_length: int = len(self.positions_track)
        for line in range(1, track_length):
            line_width: int = int(-2 * self.size / track_length * line + 2 * self.size)
            line_color: list[int, int, int] = [-color / track_length * line + color for color in list(self.color)]
            pg.draw.line(screen, line_color, self.positions_track[line-1], self.positions_track[line], line_width)
        
        pg.draw.circle(screen, self.color, self.position, self.size)

    def rotate_to_center(self, point: tuple[int, int], distance: int) -> None:
        self.position[0] = distance * cos(radians(self.angle)) + point[0]
        self.position[1] = distance * sin(radians(self.angle)) + point[1]
        self.hitbox_rect.center = self.position

        self.positions_track.insert(0, list(self.hitbox_rect.center))
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
    
    def movement_bottom(self) -> None:
        self.position[1] += 5
        self.hitbox_rect.y = self.position[1]
    
    def draw(self, screen: pg.Surface) -> None:
        pg.draw.rect(screen, self.color, self.hitbox_rect)

player1: Player = Player(list(SCREEN_CENTER), COLORS["BLUE"], 20)
player2: Player = Player(list(SCREEN_CENTER), COLORS["RED"], 20, 180)

player_angle: int = 0
OBSTACLE_SIZE: int = 30
possible_obstacles_x: list[int] = [0, SCREEN_CENTER[0]]
obstacles_list: list[Obstacle] = [Obstacle([choice(possible_obstacles_x), -OBSTACLE_SIZE], COLORS["WHITE"], [SCREEN_SIZE[0]//2, OBSTACLE_SIZE])]
GAME_FONT: pygame.freetype.Font = pygame.freetype.SysFont("Arial", 30, True, False)
punctuation: int = 0

running: bool = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    clock.tick(FPS)
    screen.fill(COLORS["BLACK"])

    key: pg.key.ScancodeWrapper = pg.key.get_pressed()

    player1.update(screen, SCREEN_CENTER, 100, key)
    player2.update(screen, SCREEN_CENTER, 100, key)

    for rect in obstacles_list:
        rect.movement_bottom()
        rect.draw(screen)
        if rect.hitbox_rect.collidelist([player1.hitbox_rect, player2.hitbox_rect]) != -1:
            punctuation = 0

    if obstacles_list[0].position[1] >= SCREEN_SIZE[1]:
        obstacles_list.pop(0)
        
    if len([rect for rect in obstacles_list if rect.position[1] >= 200]) - len(obstacles_list) >= 0:
        obstacles_list.append(Obstacle([choice(possible_obstacles_x), -OBSTACLE_SIZE], COLORS["WHITE"], [SCREEN_SIZE[0]//2, OBSTACLE_SIZE]))
        punctuation += 1
    
    GAME_FONT.render_to(screen, (SCREEN_SIZE[0]//2-15, SCREEN_SIZE[1]//2), f"{punctuation}", COLORS["WHITE"])
    
    pg.display.flip()

pg.quit()