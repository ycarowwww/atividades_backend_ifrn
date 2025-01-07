import pygame as pg
from . import Obstacle
from ..player import Player
from scripts import scale_dimension
from math import sqrt

class StationaryObstacle(Obstacle):
    """An obstacle that just stands still and does not move or becomes invisible."""
    def __init__(self, x: int, y: int, width: int, height: int, speed: int, spacing_mult: float, color: tuple[int, int, int]):
        super().__init__(x, y, width, height, speed, spacing_mult, color)
        self._rect = pg.Rect(self._x, self._y, self._width, self._height)
        self._rect.center = (self._x, self._y)
    
    def update(self, dt: float) -> None:
        self._y += self._speed * dt
        self._rect.centery = round(self._y)

        self._update_tracker(dt)
    
    def draw(self, screen: pg.Surface) -> None:
        self._draw_tracker(screen)
        
        pg.draw.rect(screen, self._color, self._rect)
    
    def check_collision(self, player: Player) -> bool:
        if self._rect.bottom < player.get_center()[1] - player.get_distance() - player.get_radius() or self._rect.top > player.get_center()[1] + player.get_distance() + player.get_radius(): 
            return False
        
        for i in range(player.get_amount()):
            closest_x: float = max(self._rect.left, min(player.get_positions()[i][0], self._rect.right))
            closest_y: float = max(self._rect.top, min(player.get_positions()[i][1], self._rect.bottom))

            distance: float = sqrt((player.get_positions()[i][0] - closest_x) ** 2 + (player.get_positions()[i][1] - closest_y) ** 2)

            if distance < player.get_radius(): return True
        
        return False

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

        for i in range(len(self._position_tracker)):
            time = self._position_tracker_lifetime - self._position_tracker_times[i]
            self._position_tracker[i] = (round(self._x), round(self._y - self._speed * time))

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

    def set_x(self, new_x: float) -> None: 
        self._x = new_x
        self._rect.centerx = round(self._x)

    def set_y(self, new_y: float) -> None: 
        self._y = new_y
        self._rect.centery = round(self._y)
