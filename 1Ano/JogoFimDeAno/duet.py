import pygame as pg
import pygame.freetype as pgft
import colorsys
from math import cos, sin, radians, atan2, pi, sqrt
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
    """Ajusta o brilho de uma cor RGB convertendo-a para HSV.

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

def get_diagonal_line(point1: tuple[int, int], radius1: int, point2: tuple[int, int], radius2: int) -> tuple[tuple[int, int], tuple[int, int], tuple[int, int], tuple[int, int]]:
    """Returns the 4 points of a 'quadrilateral' for a 'diagonal' line from circle1 to circle2

        Pygame can only draw lines with 90º ends, creating a 'shrinking' effect when drawing a line between two circles.
        This function returns 4 points between the circles to draw in the 'pg.draw.polygon' function for a line with a 'diagonal' ending.

        Args:
            point1 (tuple): Circle1's center.
            radius1 (tuple): Circle1's radius.
            point2 (int): Circle2's center.
            radius1 (int): Circle2's radius.

        Returns:
            tuple: A tuple with 4 points positions.
    """
    pos1: tuple[int, int] = (point1[0], -point1[1]) # Flipping the y-axis because of Pygame
    pos2: tuple[int, int] = (point2[0], -point2[1]) # Flipping the y-axis because of Pygame
    angle: float = atan2(point1[0] - point2[0], point1[1] - point2[1])

    def get_point(rad: int, ang: float, x: int, y: int) -> tuple[int, int]:
        """Returns the point position in the circle."""
        return (int(rad * cos(ang) + x), int(rad * sin(ang) + y))
    
    points = (get_point(radius1, angle, pos1[0], pos1[1]), 
              get_point(radius1, angle + pi, pos1[0], pos1[1]), 
              get_point(radius2, angle + pi, pos2[0], pos2[1]), 
              get_point(radius2, angle, pos2[0], pos2[1]))
    
    return tuple([(p[0], -p[1]) for p in points]) # Unflipping the y-axis because of Pygame

def get_line_surface(points: list[tuple[int, int]], initial_radius: int, initial_color: tuple[int, int, int], initial_alpha: int) -> tuple[pg.Surface, tuple[int, int]]:
    """Returns the line Surface and topleft position.

        Returns a Surface with a line of the circle's previous positions becoming increasingly transparent. 
        It also uses diagonal lines to connect the positions.

        Args:
            points (list[tuple]): Previous positions of the circle's center.
            initial_radius (int): Initial radius of the line.
            initial_color (tuple): Line color.
            initial_alpha (int): Initial alpha of the line.

        Returns:
            tuple: A tuple with the Surface and Topleft position.
        
        Raises:
            ValueError: If 'points' has less than 2 elements.
    """
    l = len(points)
    if l < 2: raise ValueError("At least 2 points are required.")
    
    radius: list[int] = [int(-initial_radius / l * i + initial_radius) for i in range(l)]
    
    point_tl = [points[0][0] - radius[0], points[0][1] - radius[0]]
    point_br = [points[0][0] + radius[0], points[0][1] + radius[0]]

    for i in range(1, len(points)):
        point_tl[0] = min(point_tl[0], points[i][0] - radius[i])
        point_tl[1] = min(point_tl[1], points[i][1] - radius[i])
        point_br[0] = max(point_br[0], points[i][0] + radius[i])
        point_br[1] = max(point_br[1], points[i][1] + radius[i])
    
    offset = (point_br[0] - point_tl[0], point_br[1] - point_tl[1])
    surf = pg.Surface(offset, flags=pg.SRCALPHA)
    surf2 = pg.Surface(offset, flags=pg.SRCALPHA) # Another surface to prevent a darker line from being on top of a lighter one.

    points_offset = [[p[0] - point_tl[0], p[1] - point_tl[1]] for p in points]

    for i in range(len(points_offset)):
        surf2.fill(COLORS["BLANK"])
        color = (*initial_color, int(-initial_alpha / len(points_offset) * i + initial_alpha))

        pg.draw.circle(surf2, color, points_offset[i], radius[i])
        if i != 0:
            pg.draw.polygon(surf2, color, get_diagonal_line(points_offset[i-1], radius[i-1], points_offset[i], radius[i]))

        surf.blit(surf2, (0, 0), special_flags=pg.BLEND_RGBA_MAX) # Pick the "strongest" color in the line
    
    return (surf, point_tl)

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

        self.positions_track.insert(0, self.hitbox_rect.top) # Change to a Queue after
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
        self.positions_tracker: list[list[tuple[int, int]]] = [[] for _ in range(self.amount)]
        self.max_tracker = 24
    
    def update(self) -> None:
        key: pg.key.ScancodeWrapper = pg.key.get_pressed()
        
        if key[pg.K_LSHIFT] and self.distance > 0:
            self.distance -= self.speed
        if key[pg.K_SPACE] and self.distance < SCREEN_SIZE[0]//3 or self.distance < 100 and not key[pg.K_LSHIFT]:
            self.distance += self.speed
        elif self.distance > 100 and not key[pg.K_SPACE]:
            self.distance -= self.speed

        if key[pg.K_a]: self.angle -= self.speed
        if key[pg.K_d]: self.angle += self.speed
        self.angle %= 360

        self.rotate_to_center()
        self.update_tracker()
    
    def draw(self, screen: pg.Surface) -> None:
        if self.show_border:
            pg.draw.circle(screen, self.border_color, self.center, self.distance, self.border_size)

        if len(self.positions_tracker[0]) > 2:
            for i in range(self.amount):
                surf, topleft = get_line_surface(self.positions_tracker[i], self.radius, self.colors[i], 127)

                screen.blit(surf, topleft)
        
        for i in range(self.amount):
            pg.draw.circle(screen, self.colors[i], self.positions[i], self.radius)

        self.draw_intersection(screen)

    def rotate_to_center(self) -> None:
        for i in range(self.amount):
            self.positions[i][0] = int(self.distance * cos(radians(self.angle) + radians(self.d_angle * i)) + self.center[0])
            self.positions[i][1] = int(self.distance * sin(radians(self.angle) + radians(self.d_angle * i)) + self.center[1])

    def update_tracker(self) -> None:
        for i in range(self.amount):
            for j in self.positions_tracker[i]:
                j[1] += self.speed
            
            self.positions_tracker[i].insert(0, self.positions[i].copy()) # Change to a Queue after

            while len(self.positions_tracker[i]) > self.max_tracker:
                self.positions_tracker[i].pop()
            
    def draw_intersection(self, screen: pg.Surface) -> None:
        if self.amount >= 2 and self.__check_circles_collided():
            surf_player = pg.Surface((self.distance * 2 + self.radius * 2, self.distance * 2 + self.radius * 2))
            surf_player.fill(COLORS["BLACK"])
            surf_player.set_colorkey(COLORS["BLACK"])

            topleft_offset = (self.center[0] - self.distance, self.center[1] - self.distance)
            offset_positions = [[i[0] - topleft_offset[0], i[1] - topleft_offset[1]] for i in self.positions]

            for i in range(self.amount):
                surf = pg.Surface((self.radius * 2, self.radius * 2))
                surf.fill(COLORS["BLACK"])
                pg.draw.circle(surf, self.colors[i], (self.radius, self.radius), self.radius)
                surf_player.blit(surf, offset_positions[i], special_flags=pg.BLEND_ADD)
            
            screen.blit(surf_player, (topleft_offset[0] - self.radius, topleft_offset[1] - self.radius))
    
    def toggle_border(self) -> None:
        self.show_border = not self.show_border
    
    def check_collision_rect(self, hitbox_rect: pg.Rect) -> bool:
        if hitbox_rect.bottom < self.center[1] - self.distance or hitbox_rect.top > self.center[1] + self.distance: 
            return False
        
        for i in range(self.amount):
            closest_x: float = max(hitbox_rect.left, min(self.positions[i][0], hitbox_rect.right))
            closest_y: float = max(hitbox_rect.top, min(self.positions[i][1], hitbox_rect.bottom))

            distance: float = sqrt((self.positions[i][0] - closest_x) ** 2 + (self.positions[i][1] - closest_y) ** 2)

            if distance <= self.radius: return True
        
        return False

    def __check_circles_collided(self) -> bool:
        return sqrt((self.positions[0][0] - self.positions[1][0]) ** 2 + (self.positions[0][1] - self.positions[1][1]) ** 2) < self.radius * 2

def game() -> None:
    player: Player = Player(list(SCREEN_CENTER), [COLORS["BLUE"], COLORS["RED"]], COLORS["GRAY"], 20, speed=PLAYER_ROTATION_VELOCITY)

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

        for rect in obstacles_list:
            rect.movement_bottom()
            rect.draw(screen)
            # Check Collision with players
            if player.check_collision_rect(rect.hitbox_rect):
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
                    obstacles_list.append(Obstacle([SCREEN_CENTER[0] - SCREEN_SIZE[0]//8, -OBSTACLE_SIZE], COLORS["WHITE"], [SCREEN_SIZE[0]//4, OBSTACLE_SIZE]))
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
