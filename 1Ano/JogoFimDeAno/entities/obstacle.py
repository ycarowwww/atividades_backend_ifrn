import pygame as pg
from scripts.settings import *

class Obstacle:
    def __init__(self, position: list[int], color: tuple[int, int, int], size: list[int]) -> None:
        self.position = position
        self.size = size
        self.color = color
        self.hitbox_rect = pg.Rect(self.position[0], self.position[1], self.size[0], self.size[1])
        self.speed = 270 / (180 / PLAYER_ROTATION_VELOCITY) # 200 (bigger" circle's radius) + 40 (balls' radois) + self.size = total height / time (180º / 5º) | Formula Temporary Removed
        self.positions_tracker: list[tuple[int, int]] = []
        self.max_amount_tracker = 5
    
    def movement_bottom(self) -> None:
        self.position[1] += self.speed
        self.hitbox_rect.y = self.position[1]

        self.positions_tracker.insert(0, self.hitbox_rect.topleft) # Change to a Queue after
        while len(self.positions_tracker) >= self.max_amount_tracker:
            self.positions_tracker.pop()
    
    def draw(self, screen: pg.Surface) -> None:
        self.__draw_tracker(50, screen)
        
        pg.draw.rect(screen, self.color, self.hitbox_rect)

    def __draw_tracker(self, initial_alpha: int, screen: pg.Surface) -> None:
        """Draw the Obstacle's tracker on the screen.

            Use another surface to draw the previous rectangles and blits it to the main surface.
        """
        if len(self.positions_tracker) <= 1: return
        
        size: tuple[int, int] = self.hitbox_rect.size
        ext_topleft, ext_bottomright = list(self.positions_tracker[0]), list(self.positions_tracker[0])

        for i in range(1, len(self.positions_tracker)): # Calculate the Extreme Points
            ext_topleft[0] = min(ext_topleft[0], self.positions_tracker[i][0])
            ext_topleft[1] = min(ext_topleft[1], self.positions_tracker[i][1])
            ext_bottomright[0] = max(ext_bottomright[0], self.positions_tracker[i][0])
            ext_bottomright[1] = max(ext_bottomright[1], self.positions_tracker[i][1])
        
        ext_bottomright = [ ext_bottomright[i] + size[i] for i in range(2) ]

        surf_size = (ext_bottomright[0] - ext_topleft[0], ext_bottomright[1] - ext_topleft[1])
        surf = pg.Surface(surf_size, flags=pg.SRCALPHA)
        surf.fill((0, 0, 0, 0))
        # Inverts the points and calculate the offset to won't draw previous tracks in the front of the new ones.
        offset_points: list[tuple[int, int]] = [ (self.positions_tracker[i][0] - ext_topleft[0], self.positions_tracker[i][1] - ext_topleft[1]) for i in range(len(self.positions_tracker) - 1, -1, -1) ]

        for i in range(len(offset_points)):
            col = (*self.color, int(initial_alpha / len(offset_points) * (i + 1)))
            rect = pg.Rect(offset_points[i][0], offset_points[i][1], size[0], size[1])

            pg.draw.rect(surf, col, rect)

            if i > 0: # Draw the "Connection lines" between the rects
                prev_rect = pg.Rect(offset_points[i-1][0], offset_points[i-1][1], size[0], size[1])
                pg.draw.polygon(surf, col, (prev_rect.topright, rect.topright, rect.topleft, prev_rect.topleft))
                pg.draw.polygon(surf, col, (prev_rect.topleft, rect.topleft, rect.bottomleft, prev_rect.bottomleft))
                pg.draw.polygon(surf, col, (prev_rect.topright, rect.topright, rect.bottomright, prev_rect.bottomright))
                pg.draw.polygon(surf, col, (prev_rect.bottomleft, rect.bottomleft, rect.bottomright, prev_rect.bottomright))

        screen.blit(surf, ext_topleft)
    