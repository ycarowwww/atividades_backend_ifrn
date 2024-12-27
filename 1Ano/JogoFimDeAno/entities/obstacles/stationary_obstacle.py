import pygame as pg
from entities.player import Player
from entities.obstacles.obstacle import Obstacle
from math import sqrt

class StationaryObstacle(Obstacle):
    """An obstacle that just stands still and does not move or becomes invisible."""
    def __init__(self, x: int, y: int, width: int, height: int, speed: int, color: tuple[int, int, int]):
        super().__init__(x, y, width, height, speed, color)
        self._rect = pg.Rect(self._x, self._y, self._width, self._height)
    
    def update(self) -> None:
        self._y += self._speed
        self._rect.y = self._y

        self._position_tracker.append(list(self._rect.topleft))
        while len(self._position_tracker) >= self._max_positions_tracker:
            self._position_tracker.popleft()
    
    def draw(self, screen: pg.Surface) -> None:
        self._draw_tracker(screen)
        
        pg.draw.rect(screen, self._color, self._rect)
    
    def check_collision(self, player: Player) -> bool:
        if self._rect.bottom < player.get_center()[1] - player.get_distance() or self._rect.top > player.get_center()[1] + player.get_distance(): 
            return False
        
        for i in range(player.get_amount()):
            closest_x: float = max(self._rect.left, min(player.get_positions()[i][0], self._rect.right))
            closest_y: float = max(self._rect.top, min(player.get_positions()[i][1], self._rect.bottom))

            distance: float = sqrt((player.get_positions()[i][0] - closest_x) ** 2 + (player.get_positions()[i][1] - closest_y) ** 2)

            if distance < player.get_radius(): return True
        
        return False
    
    def _draw_tracker(self, screen: pg.Surface) -> None:
        """Draw the Obstacle's tracker on the screen.

            Use another surface to draw the previous rectangles and blits it to the main surface.
        """
        len_tracker: int = len(self._position_tracker)
        if len_tracker <= 1: return
        
        ext_topleft, ext_bottomright = list(self._position_tracker[0]), list(self._position_tracker[0])

        for i in range(1, len_tracker): # Calculate the Extreme Points
            ext_topleft[0] = min(ext_topleft[0], self._position_tracker[i][0])
            ext_topleft[1] = min(ext_topleft[1], self._position_tracker[i][1])
            ext_bottomright[0] = max(ext_bottomright[0], self._position_tracker[i][0])
            ext_bottomright[1] = max(ext_bottomright[1], self._position_tracker[i][1])
        
        ext_bottomright = [ ext_bottomright[i] + self._rect.size[i] for i in range(2) ]

        surf_size = (ext_bottomright[0] - ext_topleft[0], ext_bottomright[1] - ext_topleft[1])
        surf = pg.Surface(surf_size, flags=pg.SRCALPHA)
        surf.fill((0, 0, 0, 0)) # Fill the surface with "Blank" color
        # Inverts the points and calculate the offset to won't draw previous tracks in the front of the new ones.
        offset_points: list[tuple[int, int]] = [ (self._position_tracker[i][0] - ext_topleft[0], self._position_tracker[i][1] - ext_topleft[1]) for i in range(len_tracker) ]

        for i in range(len(offset_points)):
            col = (*self._color, int(self._initial_alpha_tracker / len(offset_points) * (i + 1)))
            rect = pg.Rect(offset_points[i][0], offset_points[i][1], self._width, self._height)

            pg.draw.rect(surf, col, rect)

            if i > 0: # Draw the "Connection lines" between the rects
                prev_rect = pg.Rect(offset_points[i-1][0], offset_points[i-1][1], self._width, self._height)
                pg.draw.polygon(surf, col, (prev_rect.topright, rect.topright, rect.topleft, prev_rect.topleft))
                pg.draw.polygon(surf, col, (prev_rect.topleft, rect.topleft, rect.bottomleft, prev_rect.bottomleft))
                pg.draw.polygon(surf, col, (prev_rect.topright, rect.topright, rect.bottomright, prev_rect.bottomright))
                pg.draw.polygon(surf, col, (prev_rect.bottomleft, rect.bottomleft, rect.bottomright, prev_rect.bottomright))

        screen.blit(surf, ext_topleft)
