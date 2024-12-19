import pygame as pg
from math import sin, cos, atan2, pi, radians, sqrt
from scripts.settings import *

class Player:
    def __init__(self, center: tuple[int, int], colors_circles: list[tuple[int, int, int]], border_color: tuple[int, int, int], radius: int, distance: int = 100, speed: float = PLAYER_ROTATION_VELOCITY) -> None:
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
        if key[pg.K_SPACE] and self.distance < SCREEN_SIZE[0]//3 or self.distance < 100 and not key[pg.K_LSHIFT]: # Change this Screen_Size after probably
            self.distance += self.speed
        elif self.distance > 100 and not key[pg.K_SPACE]:
            self.distance -= self.speed

        if key[pg.K_a]: self.angle -= self.speed
        if key[pg.K_d]: self.angle += self.speed
        self.angle %= 360

        self.__rotate_to_center()
        self.__update_tracker()
    
    def draw(self, screen: pg.Surface) -> None:
        if self.show_border:
            pg.draw.circle(screen, self.border_color, self.center, self.distance, self.border_size)

        if len(self.positions_tracker[0]) > 2:
            for i in range(self.amount):
                surf, topleft = self.__get_line_surface(self.positions_tracker[i], self.radius, self.colors[i], 127)

                screen.blit(surf, topleft)
        
        for i in range(self.amount):
            pg.draw.circle(screen, self.colors[i], self.positions[i], self.radius)

        self.__draw_intersection(screen)
    
    def update_by_event(self, event: pg.event.Event) -> None:
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_b:
                self.__toggle_border()
    
    def __toggle_border(self) -> None:
        self.show_border = not self.show_border

    def __rotate_to_center(self) -> None:
        for i in range(self.amount):
            self.positions[i][0] = int(self.distance * cos(radians(self.angle) + radians(self.d_angle * i)) + self.center[0])
            self.positions[i][1] = int(self.distance * sin(radians(self.angle) + radians(self.d_angle * i)) + self.center[1])

    def __update_tracker(self) -> None:
        for i in range(self.amount):
            for j in self.positions_tracker[i]:
                j[1] += self.speed
            
            self.positions_tracker[i].insert(0, self.positions[i].copy()) # Change to a Queue after

            while len(self.positions_tracker[i]) > self.max_tracker:
                self.positions_tracker[i].pop()
            
    def __draw_intersection(self, screen: pg.Surface) -> None:
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

    def __check_circles_collided(self) -> bool:
        return sqrt((self.positions[0][0] - self.positions[1][0]) ** 2 + (self.positions[0][1] - self.positions[1][1]) ** 2) < self.radius * 2
    
    def __get_diagonal_line(self, point1: tuple[int, int], radius1: int, point2: tuple[int, int], radius2: int) -> tuple[tuple[int, int], tuple[int, int], tuple[int, int], tuple[int, int]]:
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
    
    def __get_line_surface(self, points: list[tuple[int, int]], initial_radius: int, initial_color: tuple[int, int, int], initial_alpha: int) -> tuple[pg.Surface, tuple[int, int]]:
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

        points_offset = [[p[0] - point_tl[0], p[1] - point_tl[1]] for p in points]

        for i in range(len(points_offset) - 1, -1, -1):
            color = (*initial_color, int(-initial_alpha / len(points_offset) * i + initial_alpha))

            pg.draw.circle(surf, color, points_offset[i], radius[i])
            if i != 0:
                pg.draw.polygon(surf, color, self.__get_diagonal_line(points_offset[i-1], radius[i-1], points_offset[i], radius[i]))
        
        return (surf, point_tl)
