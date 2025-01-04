import pygame as pg

class Lines:
    def __init__(self, size: tuple[int, int], amount_lines: int, color: tuple[int, int, int]):
        self._amount = amount_lines # need to be even
        self._size = size
        self._actual_drop = 0
        self._max_drop = 2 / (self._amount - 1)
        self._velocity = self._max_drop
        self._times = [ i / (self._amount-1) for i in range(-2, self._amount-1) ]
        self._indexes = [ i for i in range(1, len(self._times) + 1, 2) ]
        self._points = [ [], [] ]
        self._color = color
    
    def update(self, dt: float) -> None:
        self._actual_drop += self._velocity * dt
        self._actual_drop %= self._max_drop
        self._calculate_points()
    
    def draw(self, screen: pg.Surface) -> None:
        for i in range(len(self._indexes)-1):
            self._draw_without_medium(screen, self._indexes[i])
        
        index_diagonals = round((self._amount - 1) / 2)
        self._draw_with_medium(screen, index_diagonals-1)
        self._draw_with_medium(screen, index_diagonals+1)
    
    def resize(self, new_size: tuple[int, int]) -> None:
        self._size = new_size
    
    def _calculate_points(self) -> None:
        self._points = [ [], [] ]
        for t in self._times:
            self._points[0].append((2 * min(0.5, t + self._actual_drop) * self._size[0], 
                                    2 * max(0, t + self._actual_drop - 0.5) * self._size[1]))
            
            self._points[1].append((2 * max(0, t + self._actual_drop - 0.5) * self._size[0], 
                                    2 * min(0.5, t + self._actual_drop) * self._size[1]))
    
    def _draw_without_medium(self, screen: pg.Surface, index: int) -> None:
        pg.draw.polygon(screen, self._color, (
            self._points[0][index],
            self._points[1][index],
            self._points[1][index+1],
            self._points[0][index+1]
        ))
    
    def _draw_with_medium(self, screen: pg.Surface, index: int) -> None:
        pg.draw.polygon(screen, self._color, (
            self._points[0][index],
            self._points[1][index],
            (self._points[1][index][0], self._points[1][index+1][1]),
            self._points[1][index+1],
            self._points[0][index+1],
            (self._points[0][index+1][0], self._points[0][index][1])
        ))
