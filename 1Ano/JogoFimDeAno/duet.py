import pygame as pg
import pygame.freetype as pgft
import colorsys
from math import cos, sin, radians, sqrt
from random import randint

PLAYER_ROTATION_VELOCITY: float = float(input("- Player's Rotation Velocity: "))

pg.init()

SCREEN_SIZE: tuple[int, int] = (800, 600)
SCREEN_CENTER: tuple[int, int] = (SCREEN_SIZE[0]//2, SCREEN_SIZE[1]//2)
screen: pg.Surface = pg.display.set_mode(SCREEN_SIZE)
pg.display.set_caption("Duet PFA")
clock: pg.time.Clock = pg.time.Clock()
FPS: float = 60.0
COLORS: dict[str, tuple[int, int, int]] = {
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
GAME_STATE: int = 1

def adjust_brightness(color: tuple[int, int, int], brightness_factor: float) -> tuple[int, int, int]:
    """
        Ajusta o brilho de uma cor RGB convertendo-a para HSV.

        Args:
            color (tuple): Cor RGB original.
            brightness_factor (float): Fator de Ajusta (1.0 = sem ajuste).

        Returns:
            tuple: cor RGB ajustada.
    """

    r, g, b = color
    h, s, v = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)

    v = min(1.0, max(0.0, v * brightness_factor))

    r, g, b = colorsys.hsv_to_rgb(h, s, v)

    return (int(r * 255), int(g * 255), int(b * 255))

def blit_text(screen: pg.Surface, message: str, color: tuple[int, int, int], topleft: tuple[int, int], font: pgft.Font) -> None:
    text_surface, text_rect = font.render(message, color)
    text_rect.topleft = topleft
    screen.blit(text_surface, text_rect)

def collision_circle_rect(circle_center: tuple[float, float], radius: float, rect: pg.Rect) -> bool:
    """
        Detecta a colisão de um círculo com um Retângulo.
    """
    closest_x: float = max(rect.left, min(circle_center[0], rect.right))
    closest_y: float = max(rect.top, min(circle_center[1], rect.bottom))

    distance: float = sqrt((circle_center[0] - closest_x) ** 2 + (circle_center[1] - closest_y) ** 2)

    return distance <= radius

def collision_circles(center1: tuple[int, int], center2: tuple[int, int], radius1: int, radius2: int) -> bool:
    return sqrt((center1[0] - center2[0]) ** 2 + (center1[1] - center2[1]) ** 2) < radius1 + radius2

def circles_intersection(screen: pg.Surface, player1: tuple[pg.Surface, tuple[int, int], int], player2: tuple[pg.Surface, tuple[int, int], int], color: tuple[int, int, int]) -> None:
    """
        Desenha a Intersecção de dois círculos na surface (*screen*) principal.
        
        Args:
            screen: Surface principal.
            players: Uma tupla com a surface do círculo, coordenadas do centro e o raio.
    """

    surf1 = player1[0]
    surf2 = player2[0]
    player1center = player1[1]
    player2center = player2[1]
    player1radius = player1[2]
    player2radius = player2[2]

    surf1.fill(COLORS["BLANK"])
    surf2.fill(COLORS["BLANK"])

    pg.draw.circle(surf1, color, (player1radius, player1radius), player1radius)
    pg.draw.circle(surf2, color, (player2radius, player2radius), player2radius)

    player1_topleft = (player1center[0] - player1radius, player1center[1] - player1radius)
    player2_topleft = (player2center[0] - player2radius, player2center[1] - player2radius)

    rel_pos_1_2 = (player2_topleft[0] - player1_topleft[0], player2_topleft[1] - player1_topleft[1])

    surf1.blit(surf2, rel_pos_1_2, special_flags=pg.BLEND_RGBA_MIN)

    if rel_pos_1_2[1] > 0:
        surf1.fill(COLORS["BLANK"], pg.Rect(0, 0, player1radius * 2, rel_pos_1_2[1]))
    if rel_pos_1_2[0] > 0:
        surf1.fill(COLORS["BLANK"], pg.Rect(0, rel_pos_1_2[1], rel_pos_1_2[0], player1radius * 2 - rel_pos_1_2[1]))
    if player1radius * 2 - (rel_pos_1_2[0] + player2radius * 2) > 0:
        surf1.fill(COLORS["BLANK"], pg.Rect(rel_pos_1_2[0] + player2radius * 2, rel_pos_1_2[1], player1radius * 2 - (rel_pos_1_2[0] + player2radius * 2), player1radius * 2 - rel_pos_1_2[1]))
    if player1radius * 2 - (rel_pos_1_2[1] + player2radius * 2) > 0:
        surf1.fill(COLORS["BLANK"], pg.Rect(rel_pos_1_2[0], rel_pos_1_2[1] + player2radius * 2, player2radius * 2, player1radius * 2 - (rel_pos_1_2[1] + player2radius * 2)))

    screen.blit(surf1, player1_topleft)

class Obstacle:
    def __init__(self, position: list[int], color: tuple[int, int, int], size: list[int]) -> None:
        self.position = position
        self.size = size
        self.color = color
        self.hitbox_rect = pg.Rect(self.position[0], self.position[1], self.size[0], self.size[1])
        self.speed = 270 / (180 / PLAYER_ROTATION_VELOCITY) # 200 (bigger" circle's radius) + 40 (balls' radois) + self.size = total height / time (180º / 5º) | Formula Temporary Removed
        self.positions_track: list[int] = []
        self.color_track = adjust_brightness(self.color, 0.5)
    
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
            line_color: list[int] = [-color / track_length * line + color for color in list(self.color_track)]
            pg.draw.line(screen, line_color, (self.hitbox_rect.centerx, self.positions_track[line-1]), (self.hitbox_rect.centerx, self.positions_track[line]), line_width)
        
        pg.draw.rect(screen, self.color, self.hitbox_rect)

class Player:
    def __init__(self, center: tuple[int, int], colors_circles: list[tuple[int, int, int]], border_color: tuple[int, int, int], radius: int, distance: int = 100, speed: float = 5) -> None:
        self.center = center
        self.colors = colors_circles
        self.radius = radius
        self.amount = len(self.colors)
        self.positions = [[0, 0] for _ in range(self.amount)]
        self.angle = 0
        self.d_angle = 360 // self.amount
        self.speed = speed
        self.distance = distance
        self.show_border = False
        self.border_size = 5
        self.border_color = border_color
        # Falta as linhas das posições, colisão e intersecção
        # self.positions_track: list[list[int]] = []
        # self.colors_track = [adjust_brightness(self.colors[i]) for i in range(len(self.colors) - 1)]
    
    def update(self) -> None:
        key: pg.key.ScancodeWrapper = pg.key.get_pressed()
        
        if key[pg.K_LSHIFT] and self.distance > 0:
            self.distance -= self.speed
        elif key[pg.K_SPACE] and self.distance < SCREEN_SIZE[0]//3 or self.distance < 100 and not key[pg.K_LSHIFT]:
            self.distance += self.speed
        elif self.distance > 100 and not key[pg.K_SPACE]:
            self.distance -= self.speed

        if key[pg.K_a]: self.angle -= self.speed
        if key[pg.K_d]: self.angle += self.speed
        self.angle %= 360

        self.rotate_to_center()
    
    def draw(self, screen: pg.Surface) -> None:
        if self.show_border:
            pg.draw.circle(screen, self.border_color, self.center, self.distance, self.border_size)
        
        # track_length: int = len(self.positions_track)
        # for line in range(track_length-1, 0, -1):
        #     line_width: int = int(-2 * self.radius / track_length * line + 2 * self.radius)
        #     line_color: list[int] = [-color / track_length * line + color for color in list(self.color_track)]
        #     pg.draw.line(screen, line_color, self.positions_track[line-1], self.positions_track[line], line_width)
        #     pg.draw.circle(screen, line_color, self.positions_track[line], line_width//2)
        
        for i in range(self.amount):
            pg.draw.circle(screen, self.colors[i], self.positions[i], self.radius)

    def rotate_to_center(self) -> None:
        for i in range(self.amount):
            self.positions[i][0] = int(self.distance * cos(radians(self.angle) + radians(self.d_angle * i)) + self.center[0])
            self.positions[i][1] = int(self.distance * sin(radians(self.angle) + radians(self.d_angle * i)) + self.center[1])

        # self.positions_track.insert(0, pos.copy()) # Usar uma Queue depois
        # if len(self.positions_track) >= 150 / self.speed:
        #     self.positions_track.pop(-1)

        # for line in range(1, len(self.positions_track)):
        #     self.positions_track[line][1] += self.speed
    
    def toggle_border(self) -> None:
        self.show_border = not self.show_border

def game() -> None:
    player: Player = Player(list(SCREEN_CENTER), [COLORS["BLUE"], COLORS["RED"]], COLORS["GRAY"], 20, speed=PLAYER_ROTATION_VELOCITY)
    # player1: Player = Player(list(SCREEN_CENTER), COLORS["BLUE"], 20, speed=PLAYER_ROTATION_VELOCITY)
    # player2: Player = Player(list(SCREEN_CENTER), COLORS["RED"], 20, 180, speed=PLAYER_ROTATION_VELOCITY)

    # surf_player1: pg.Surface = pg.Surface((player1.radius * 2, player1.radius * 2), pg.SRCALPHA)
    # surf_player2: pg.Surface = pg.Surface((player2.radius * 2, player2.radius * 2), pg.SRCALPHA)

    paused: bool = False
    pause_button_rect: pg.Rect = pg.Rect(0, 0, 50, 50)
    pause_button_rect.topright = (SCREEN_SIZE[0] - 10, 10)
    pause_button_triangle: list[tuple[int, int]] = (pause_button_rect.topleft, pause_button_rect.bottomleft, (pause_button_rect.right, pause_button_rect.centery))
    pause_button_rects: list[pg.Rect] = [pg.Rect(0, 0, 20, 50), pg.Rect(0, 0, 20, 50)]
    pause_button_rects[0].topright = pause_button_rect.topright
    pause_button_rects[1].topright = (pause_button_rects[0].right - 30, pause_button_rects[0].top)
    return_menu_button: pg.Rect = pg.Rect(0, 0, 50, 50)
    return_menu_button.topright = (pause_button_rect.left - 10, pause_button_rect.top)
    punctuation, max_score = 0, 0
    OBSTACLE_SIZE: int = 30
    obstacles_list: list[Obstacle] = [Obstacle([0, -OBSTACLE_SIZE], COLORS["WHITE"], [SCREEN_SIZE[0]//2, OBSTACLE_SIZE])]

    running: bool = True
    while running:
        key: pg.key.ScancodeWrapper = pg.key.get_pressed()

        if key[pg.K_LSHIFT] and key[pg.K_ESCAPE]:
            running = False

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
                global GAME_STATE
                GAME_STATE = 0

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    paused = not paused
                if event.key == pg.K_b:
                    player.toggle_border()

            if event.type == pg.MOUSEBUTTONDOWN:
                mx, my = event.pos

                if pause_button_rect.collidepoint(mx, my):
                    paused = not paused
                elif paused and return_menu_button.collidepoint(mx, my):
                    running = False

        clock.tick(FPS)
        screen.fill(COLORS["BLACK"])

        if paused:
            pg.draw.polygon(screen, COLORS["WHITE"], pause_button_triangle)
            pg.draw.polygon(screen, COLORS["WHITE"], (return_menu_button.topright, return_menu_button.bottomright, (return_menu_button.left, return_menu_button.centery)))

            player.draw(screen)
            # player1.draw(screen)
            # player2.draw(screen)

            # if collision_circles(player1.position, player2.position, player1.radius, player2.radius):
            #     circles_intersection(screen, (surf_player1, player1.position, player1.radius), (surf_player2, player2.position, player2.radius), COLORS["WHITE"])

            for rect in obstacles_list:
                rect.draw(screen)
            
            blit_text(screen, f"Score: {punctuation}", COLORS["WHITE"], (10, 10), GAME_FONT)
            blit_text(screen, f"Max: {max_score}", COLORS["GREEN"], (10, 40), MAX_SCORE_FONT)
            
            pg.display.flip()
            continue
        else:
            for rt in pause_button_rects:
                pg.draw.rect(screen, COLORS["WHITE"], rt)

        player.update()
        player.draw(screen)

        # if collision_circles(player1.position, player2.position, player1.radius, player2.radius):
        #     circles_intersection(screen, (surf_player1, player1.position, player1.radius), (surf_player2, player2.position, player2.radius), COLORS["WHITE"])

        for rect in obstacles_list:
            rect.movement_bottom()
            rect.draw(screen)
            # Check Collision with players
            # if collision_circle_rect(player1.position, player1.radius, rect.hitbox_rect) or collision_circle_rect(player2.position, player2.radius, rect.hitbox_rect):
            #     punctuation = 0

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
                case _: pass
            
            punctuation += 1
            max_score = max(max_score, punctuation)
        
        blit_text(screen, f"Score: {punctuation}", COLORS["WHITE"], (10, 10), GAME_FONT)
        blit_text(screen, f"Max: {max_score}", COLORS["GREEN"], (10, 40), MAX_SCORE_FONT)
        
        pg.display.flip()

def main_menu() -> None:
    title_surf, title_rect = GAME_FONT.render("DUET", COLORS["WHITE"], style=pgft.STYLE_STRONG)
    title_rect.center = (SCREEN_CENTER[0], 100)
    game_surf, game_rect = GAME_FONT.render("Game", COLORS["WHITE"], COLORS["BLUE"])
    game_rect.center = SCREEN_CENTER

    running: bool = True
    while running:
        if GAME_STATE == 0:
            running = False
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    # Abrir opção Selecionada
                    game()
            
            if event.type == pg.MOUSEBUTTONDOWN:
                mpos = event.pos
                
                if game_rect.collidepoint(mpos):
                    game()

        clock.tick(FPS)
        screen.fill(COLORS["BLACK"])

        screen.blit(title_surf, title_rect)
        screen.blit(game_surf, game_rect)
        
        pg.display.flip()

if __name__ == "__main__":
    main_menu()
