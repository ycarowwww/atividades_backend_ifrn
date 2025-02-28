import pygame as pg
from . import Obstacle
from ..player import Player
from ..stains import generate_stain
from scripts import scale_dimension
from math import sqrt

class HorizontalMovingObstacle(Obstacle):
    def __init__(self, first_x: float, second_x: float, y: float, width: float, height: float, speed: float, spacing_mult: float, color: tuple[int, int, int], player_center: tuple[int, int], player_normal_distance: float) -> None:
        super().__init__(first_x, y, width, height, speed, spacing_mult, color)
        self._positions_x = (first_x, second_x)
        self._rect = pg.Rect(self._x, self._y, self._width, self._height)
        self._rect.center = (self._x, self._y)
        self._player_attrs = (player_center, player_normal_distance)
        self._save_values = (self._positions_x, self._player_attrs)
    
    def update(self, dt: float) -> None:
        self._y += self._speed * dt
        self._rect.centery = round(self._y)

        self._check_current_x()

        self._update_tracker(dt)
    
    def draw(self, screen: pg.Surface) -> None:
        self._draw_tracker(screen)
        
        pg.draw.rect(screen, self._color, self._rect)

        self._draw_ink_stains(screen)
    
    def check_collision(self, player: Player) -> tuple[bool, list[int]]:
        if self._rect.bottom < player.get_center()[1] - player.get_distance() - player.get_radius() or self._rect.top > player.get_center()[1] + player.get_distance() + player.get_radius(): 
            return (False, [])
        
        for i in range(player.get_amount()):
            closest_x: float = max(self._rect.left, min(player.get_positions()[i][0], self._rect.right))
            closest_y: float = max(self._rect.top, min(player.get_positions()[i][1], self._rect.bottom))

            distance: float = sqrt((player.get_positions()[i][0] - closest_x) ** 2 + (player.get_positions()[i][1] - closest_y) ** 2)

            if distance < player.get_radius(): 
                self._has_ink_stain = True
                self._paint_new_stain((closest_x, closest_y), player.get_radius(), player.get_colors()[i])
                return (True, [i])
        
        return (False, [])

    def set_new_resolution(self, new_resolution: tuple[int, int], old_player_info: tuple[tuple[int, int], int], new_player_info: tuple[tuple[int, int], int], new_speed: float) -> None:
        self._speed = new_speed
        
        self._width = round(scale_dimension(self._base_width, new_resolution))
        self._height = round(scale_dimension(self._base_height, new_resolution))
        self._rect.width = self._width
        self._rect.height = self._height

        y_ratio = (old_player_info[0][1] - self._y) / old_player_info[1]
        new_y = new_player_info[0][1] - y_ratio * new_player_info[1]
        self.set_y(new_y)

        x_ratio = (self._x - old_player_info[0][0]) / old_player_info[1]
        new_x = new_player_info[0][0] + x_ratio * new_player_info[1]
        self.set_x(new_x)

        self._positions_x = tuple(
            (i - self._save_values[1][0][0]) / self._save_values[1][1] * new_player_info[1] + new_player_info[0][0]
            for i in self._save_values[0]
        )
        self._player_attrs = new_player_info

        for i in range(len(self._position_tracker)):
            time = self._position_tracker_lifetime - self._position_tracker_times[i]
            self._position_tracker[i] = (round(self._x), round(self._y - self._speed * time))
        
        self._ink_stain_surface = pg.transform.scale(self._base_ink_stain_surface, self._rect.size)

    def _check_current_x(self) -> None:
        if (self._player_attrs[0][1] - self._y + self._player_attrs[1]) % (4 * self._player_attrs[1]) < 2 * self._player_attrs[1]:
            self._x = self._positions_x[0]
        else:
            self._x = self._positions_x[1]

        start_animation = 0.25 * self._player_attrs[1] # Animation start at this distance to the mod formula
        t = (self._player_attrs[0][1] - self._y + self._player_attrs[1]) % (2 * self._player_attrs[1])
        if 0 < t < start_animation: # Interpolation between the two x's | 1 is the percentage to start the movement
            x1 = self._x # Bug: Weird Movement -> Fix Later
            x2 = self._positions_x[0] if self._x == self._positions_x[1] else self._positions_x[1]
            self._x = (x1 - x2) / (start_animation) * (t - start_animation) + x1
        
        self._rect.centerx = round(self._x)

    def _update_tracker(self, dt: float) -> None:
        for i in range(len(self._position_tracker_times)):
            self._position_tracker_times[i] -= dt
        
        self._position_tracker.append(self._rect.center)
        self._position_tracker_times.append(self._position_tracker_lifetime)

        remove_to = next((j for j, e in enumerate(self._position_tracker_times) if e > 0), len(self._position_tracker_times))
        for _ in range(remove_to):
            self._position_tracker.popleft()
            self._position_tracker_times.popleft()
    
    def _draw_tracker(self, screen: pg.Surface) -> None:
        """Draw the Obstacle's tracker on the screen.

            Use another surface to draw the previous rectangles and blits it to the main surface.
        """
        len_tracker: int = len(self._position_tracker)
        if len_tracker <= 1: return

        topleft_extreme, bottomright_extreme = [0, 0], [0, 0]
        for i, coords in zip(range(2), zip(*self._position_tracker)):
            topleft_extreme[i] = round(min(coords) - self._rect.size[i] / 2)
            bottomright_extreme[i] = round(max(coords) + self._rect.size[i] / 2)

        surf_size = (bottomright_extreme[0] - topleft_extreme[0], bottomright_extreme[1] - topleft_extreme[1])
        surf = pg.Surface(surf_size, flags=pg.SRCALPHA)
        surf.fill((0, 0, 0, 0)) # Fill the surface with "Blank" color
        # Inverts the points and calculate the offset to won't draw previous tracks in the front of the new ones.
        offset_points: list[tuple[int, int]] = [ [self._position_tracker[i][j] - topleft_extreme[j] for j in range(2)] for i in range(len_tracker) ]

        for i in range(len(offset_points)):
            col = (*self._color, int(self._initial_alpha_tracker / len(offset_points) * (i + 1)))
            rect = pg.Rect(0, 0, self._width, self._height)
            rect.center = (offset_points[i][0], offset_points[i][1])

            pg.draw.rect(surf, col, rect)

            if i > 0: # Draw the "Connection lines" between the rects
                prev_rect = pg.Rect(0, 0, self._width, self._height)
                prev_rect.center = (offset_points[i-1][0], offset_points[i-1][1])
                pg.draw.polygon(surf, col, (prev_rect.topright, rect.topright, rect.topleft, prev_rect.topleft))
                pg.draw.polygon(surf, col, (prev_rect.topleft, rect.topleft, rect.bottomleft, prev_rect.bottomleft))
                pg.draw.polygon(surf, col, (prev_rect.topright, rect.topright, rect.bottomright, prev_rect.bottomright))
                pg.draw.polygon(surf, col, (prev_rect.bottomleft, rect.bottomleft, rect.bottomright, prev_rect.bottomright))

        screen.blit(surf, topleft_extreme)

    def _draw_ink_stains(self, screen: pg.Surface) -> None:
        if not self._has_ink_stain: return

        screen.blit(self._ink_stain_surface, self._rect)

    def _paint_new_stain(self, pos: tuple[float, float], size: float, color: tuple[int, int, int]) -> None:
        ratio_pos = (
            (pos[0] - self._rect.x) / self._width * self._base_width,
            (pos[1] - self._rect.y) / self._height * self._base_height
        )

        rad = size * self._base_width / self._width

        generate_stain(self._base_ink_stain_surface, ratio_pos, rad, color, rad * 1.5)
        
        self._ink_stain_surface = pg.transform.scale(self._base_ink_stain_surface, self._rect.size)

    def set_x(self, new_x: float) -> None: 
        self._x = new_x
        self._rect.centerx = round(self._x)

    def set_y(self, new_y: float) -> None: 
        self._y = new_y
        self._rect.centery = round(self._y)
