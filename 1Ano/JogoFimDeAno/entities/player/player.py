import pygame as pg
from ..eventhandler import CustomEventList
from ..particles import ParticleManager
from scripts import scale_dimension, scale_position, BASE_RESOLUTION
from collections import deque
from enum import IntEnum
from math import sqrt, pi, radians, sin, cos, atan2

class Keys(IntEnum):
    """Enum with the Keyboard Keys to the Player's movements."""
    MOREDISTANCE = pg.K_SPACE
    LESSDISTANCE = pg.K_LSHIFT
    ROTATELEFT = pg.K_a
    ROTATERIGHT = pg.K_d
    TOGGLEBORDER = pg.K_b

class Player:
    def __init__(self, center: tuple[int, int], amount_circles: int, circle_radius: int, initial_angle: float = 0, angular_speed: float = 180, distance: float = 100, linear_speed: float = 100, max_distance_multiplier: float = 3, border_size: float = 5) -> None:
        self._center = center
        self._radius = circle_radius
        self._amount = amount_circles
        self._colors = [(255, 255, 255) for _ in range(self._amount)]
        self._angle = initial_angle
        self._d_angle = 360 / self._amount
        self._angular_speed = angular_speed
        self._normal_distance = distance
        self._distance = self._normal_distance
        self._max_distance_multiplier = max_distance_multiplier
        self._max_distance = self._normal_distance * self._max_distance_multiplier
        self._linear_speed = linear_speed
        self._positions = [[0, 0] for _ in range(self._amount)]
        self._rotate_to_center() # defines the starting positions
        self._show_border = True
        self._border_size = border_size
        self._border_color = (30, 30, 30)
        self._positions_tracker: list[deque[tuple[float, float]]] = [deque() for _ in range(self._amount)]
        self._positions_tracker_times: list[deque[float]] = [deque() for _ in range(self._amount)]
        self._positions_tracker_formulas: list[deque[list[float]]] = [deque() for _ in range(self._amount)] # Tuple with: angle, distance proportion and time
        self._positions_tracker_lifetime: float = 0.5 # seconds
        self._tracker_speed_multipler = 6 # radii of the circles
        self._tracker_speed = self._tracker_speed_multipler * self._radius / self._positions_tracker_lifetime
        self._initial_tracker_alpha = 127
        self._base_distance = self._normal_distance
        self._base_radius_distance_proportion = self._radius / self._base_distance
        self._base_border_size = self._border_size
        self._actual_resolution = BASE_RESOLUTION
        self._gravity = True
        self._enable_control = True
        self._indexes_particles: set[int] = set()
        self._particles: list[ParticleManager] = []
    
    def update(self, dt: float) -> None:
        key = pg.key.get_pressed()

        linear_speed = self._linear_speed * dt
        
        if self._enable_control:
            if key[Keys.LESSDISTANCE] or key[Keys.MOREDISTANCE]:
                if key[Keys.LESSDISTANCE]:
                    self._distance -= linear_speed
                if key[Keys.MOREDISTANCE]:
                    self._distance += linear_speed
            else:
                if abs(self._normal_distance - self._distance) <= linear_speed:
                    self._distance = self._normal_distance
                elif self._distance < self._normal_distance:
                    self._distance += linear_speed
                else:
                    self._distance -= linear_speed
                
            if self._distance > self._max_distance:
                self._distance = self._max_distance
            elif self._distance < 0:
                self._distance = 0

            if key[Keys.ROTATELEFT]: self._angle -= self._angular_speed * dt
            if key[Keys.ROTATERIGHT]: self._angle += self._angular_speed * dt

            if pg.mouse.get_pressed()[0]:
                mx = pg.mouse.get_pos()[0]

                if mx > self._center[0]: self._angle += self._angular_speed * dt
                else: self._angle -= self._angular_speed * dt
        else:
            self._angle += self._angular_speed * dt
        self._angle %= 360

        self._rotate_to_center()
        self._update_tracker(dt)
    
    def draw(self, screen: pg.Surface) -> None:
        if self._show_border:
            pg.draw.circle(screen, self._border_color, self._center, self._distance, round(self._border_size))

        self._draw_tracker(screen)
        
        for i in range(self._amount):
            if i in self._indexes_particles: 
                for j in self._particles:
                    j.draw(screen)
                continue

            pos = [ round(j) for j in self._positions[i] ]
            pg.draw.circle(screen, self._colors[i], pos, self._radius)

        self._draw_intersection(screen)
    
    def update_by_event(self, event: pg.event.Event) -> None:
        match event.type:
            case pg.KEYDOWN:
                if event.key == Keys.TOGGLEBORDER and self._enable_control:
                    self._toggle_border()

            case pg.VIDEORESIZE:
                self.resize(event.size)
            
            case CustomEventList.NEWLEVELWARNING | CustomEventList.NEWGENERATIONWARNING:
                self.reset_movements()
    
    def _toggle_border(self) -> None:
        self._show_border = not self._show_border

    def _rotate_to_center(self) -> None:
        for i in range(self._amount):
            self._positions[i][0] = self._distance * cos(radians(self._angle + self._d_angle * i)) + self._center[0]
            self._positions[i][1] = self._distance * sin(radians(self._angle + self._d_angle * i)) + self._center[1]

    def _update_tracker(self, dt: float) -> None:
        for i in range(self._amount):
            len_pos = len(self._positions_tracker[i])
            for j in range(len_pos):
                self._positions_tracker[i][j][1] += self._tracker_speed * dt if self._gravity else 0
                self._positions_tracker_times[i][j] -= dt
                self._positions_tracker_formulas[i][j][2] += dt
            
            self._positions_tracker[i].append(self._positions[i].copy())
            self._positions_tracker_times[i].append(self._positions_tracker_lifetime)
            self._positions_tracker_formulas[i].append([radians(self._angle + self._d_angle * i), self._distance / self._normal_distance, 0])
            
            remove_to = next((j for j, e in enumerate(self._positions_tracker_times[i]) if e > 0), len_pos)
            for _ in range(remove_to):
                self._positions_tracker[i].popleft()
                self._positions_tracker_times[i].popleft()
                self._positions_tracker_formulas[i].popleft()
        
    def _draw_tracker(self, screen: pg.Surface) -> None:
        """Draws the Tracker on the screen.

            Draws the Tracker on the screen with a line of the circle's previous positions becoming increasingly transparent. 
            It also uses diagonal lines to connect the positions.

            Args:
                points (list[tuple]): Previous positions of the circle's center.
                initial_radius (int): Initial radius of the line.
                initial_color (tuple): Line color.
                initial_alpha (int): Initial alpha of the line.
        """
        if len(self._positions_tracker[0]) < 2: return

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

            def rotate_point(rad: int, ang: float, x: int, y: int) -> tuple[int, int]:
                """Returns the point position in the circle."""
                return (int(rad * cos(ang) + x), int(rad * sin(ang) + y))
            
            points = (rotate_point(radius1, angle, pos1[0], pos1[1]), 
                      rotate_point(radius1, angle + pi, pos1[0], pos1[1]), 
                      rotate_point(radius2, angle + pi, pos2[0], pos2[1]), 
                      rotate_point(radius2, angle, pos2[0], pos2[1]))
        
            return tuple([(p[0], -p[1]) for p in points]) # Unflipping the y-axis because of Pygame

        for i in range(len(self._positions_tracker)):
            topleft_extreme = [0, 0]
            bottomright_extreme = [0, 0]
            for j, coords in zip(range(2), zip(*self._positions_tracker[i])):
                topleft_extreme[j] = round(min(coords) - self._radius)
                bottomright_extreme[j] = round(max(coords) + self._radius)

            offset = [ k - j for j, k in zip(topleft_extreme, bottomright_extreme) ]
            surf_tracker = pg.Surface(offset, flags=pg.SRCALPHA)

            points = [ (round(j[0] - topleft_extreme[0]), round(j[1] - topleft_extreme[1])) for j in self._positions_tracker[i] ]
            len_points = len(points)
            points_radii = [ round(self._radius / len_points * j) for j in range(len_points) ]
            
            for j in range(len_points):
                color_alpha = round(self._initial_tracker_alpha / len_points * j)
                color = (*self._colors[i], color_alpha)

                pg.draw.circle(surf_tracker, color, points[j], points_radii[j])
                if j != 0:
                    pg.draw.polygon(surf_tracker, color, get_diagonal_line(points[j-1], points_radii[j-1], points[j], points_radii[j]))
            
            screen.blit(surf_tracker, topleft_extreme)
            
    def _draw_intersection(self, screen: pg.Surface) -> None:
        if self._amount < 2 or not self._check_circles_collided(): return
        
        radius = round(self._radius)
        distance = round(self._distance)
        
        surf_player = pg.Surface([(distance + radius) * 2] * 2)
        surf_player.fill((0, 0, 0))
        surf_player.set_colorkey((0, 0, 0))

        topleft_offset = [ round(i - distance) for i in self._center ]
        offset_positions = [ [ round(i[j] - topleft_offset[j]) for j in range(2) ] for i in self._positions ]

        for i in range(self._amount):
            if i in self._indexes_particles: continue

            surf = pg.Surface([radius * 2] * 2)
            surf.fill((0, 0, 0))
            pg.draw.circle(surf, self._colors[i], (radius, radius), radius)
            surf_player.blit(surf, offset_positions[i], special_flags=pg.BLEND_ADD)
        
        screen.blit(surf_player, (topleft_offset[0] - radius, topleft_offset[1] - radius))

    def _check_circles_collided(self) -> bool:
        return sqrt((self._positions[0][0] - self._positions[1][0]) ** 2 + (self._positions[0][1] - self._positions[1][1]) ** 2) < self._radius * 2

    def resize(self, new_resolution: tuple[int, int]) -> None:
        particles_new_pos = [
            ((p.get_start_pos()[0] - self._center[0]) / self._normal_distance, 
             (p.get_start_pos()[1] - self._center[1]) / self._normal_distance)
            for p in self._particles
        ]

        self._center = scale_position(self._center, self._actual_resolution, new_resolution)
        self._distance /= self._normal_distance
        self._linear_speed /= self._normal_distance
        self._normal_distance = scale_dimension(self._base_distance, new_resolution)
        self._distance *= self._normal_distance
        self._max_distance = self._normal_distance * self._max_distance_multiplier
        self._radius = self._normal_distance * self._base_radius_distance_proportion
        self._linear_speed *= self._normal_distance
        self._tracker_speed = self._tracker_speed_multipler * self._radius / self._positions_tracker_lifetime
        self._border_size = scale_dimension(self._base_border_size, new_resolution)
        self._rotate_to_center()
        self._reposition_tracker()
        self._actual_resolution = new_resolution

        for i in range(len(particles_new_pos)):
            particles_new_pos[i] = (particles_new_pos[i][0] * self._normal_distance + self._center[0], particles_new_pos[i][1] * self._normal_distance + self._center[1])

        for p, pos in zip(self._particles, particles_new_pos):
            p.resize(pos, new_resolution)
    
    def _reposition_tracker(self) -> None:
        for i in range(self._amount):
            for j in range(len(self._positions_tracker[i])):
                ang = self._positions_tracker_formulas[i][j][0]
                dist = self._positions_tracker_formulas[i][j][1] * self._normal_distance
                dt = self._positions_tracker_formulas[i][j][2]
                self._positions_tracker[i][j][0] = round(dist * cos(ang) + self._center[0])
                self._positions_tracker[i][j][1] = round(dist * sin(ang) + self._center[1] + self._tracker_speed * dt)

    def add_lost_particles(self, indexes: list[int]) -> None:
        self._indexes_particles.update(indexes)
        for i in self._indexes_particles:
            self._particles.append(ParticleManager(self._positions[i], 20, self._linear_speed * 4, self.get_radius() / 10, self._colors[i], self._actual_resolution)) # Maybe change this 4 for something more logical

    def update_lost_particles(self, dt: float) -> None:
        for i in self._particles:
            i.update(dt)

    def set_circle_colors(self, new_colors: list[tuple[int, int, int]]) -> None:
        for i in range(min(len(new_colors), self._amount)):
            self._colors[i] = new_colors[i]
    
    def set_border_color(self, color: tuple[int, int, int]) -> None:
        self._border_color = color

    def get_amount(self) -> int: return self._amount
    
    def get_radius(self) -> int: return round(self._radius)

    def get_distance(self) -> int: return round(self._distance)

    def get_normal_distance(self) -> int: return round(self._normal_distance)

    def get_base_distance(self) -> int: return round(self._base_distance)

    def get_angular_speed(self) -> float: return self._angular_speed

    def get_center(self) -> tuple[int, int]: return (round(self._center[0]), round(self._center[1]))

    def get_positions(self) -> list[tuple[int, int]]: return self._positions

    def get_colors(self) -> list[tuple[int, int, int]]: return  self._colors

    def toggle_gravity(self) -> None: self._gravity = not self._gravity

    def toggle_control(self) -> None: self._enable_control = not self._enable_control

    def reset_movements(self) -> None: 
        self._angle = 180 if 90 < self._angle < 270 else 0
        self._distance = self._normal_distance
        self._indexes_particles.clear()
        self._particles.clear()
