import pygame as pg
import pygame.freetype as pgft
from scripts import ACHIEVEMENTS, get_file_path, scale_dimension
from ..eventhandler import CustomEventList
from os.path import isfile

class AchievementsDrawer:
    def __init__(self, size: tuple[int, int], font: pgft.Font, warn_size: int, title_size: int, gap: int, fgcolor: tuple[int, int, int], bgcolor: tuple[int, int, int]) -> None:
        self._size = size
        self._achievements = ACHIEVEMENTS
        self._font = font
        self._font_sizes = ( warn_size, title_size )
        self._gap = gap
        self._colors = ( fgcolor, bgcolor )
        self._current_id = None
        self._current_remaining_time = 0
        self._current_surface = None
        self._current_surface_rect = None
        
        self._saves = ( self._font_sizes, self._gap )
    
    def update(self, dt: float) -> None:
        if self._current_id == None: return

        self._current_remaining_time -= dt

        if self._current_remaining_time <= 0:
            self._current_id = None
            self._current_remaining_time = 0
            self._current_surface = None
            self._current_surface_rect = None
    
    def draw(self, screen: pg.Surface) -> None:
        if self._current_surface == None: return

        screen.blit(self._current_surface, self._current_surface_rect)
    
    def update_by_event(self, event: pg.Event) -> None:
        if event.type == pg.VIDEORESIZE:
            self.resize(event.size)
        
        if event.type == CustomEventList.ACHIEVEMENTUNLOCKED:
            self._current_id = event.id
            self._current_remaining_time = 3
            self._create_surface()
        
    def resize(self, new_resolution: tuple[int, int]) -> None:
            self._size = new_resolution
            self._gap = scale_dimension(self._saves[1], new_resolution)
            self._font_sizes = tuple(scale_dimension(i, new_resolution) for i in self._saves[0])
            self._create_surface()
    
    def _create_surface(self) -> None:
        if self._current_id == None: return
        
        warn_surf, warn_rect = self._font.render("Conquista Desbloqueada!", self._colors[0], size=self._font_sizes[0])
        title_surf, title_rect = self._font.render(self._achievements[self._current_id]["title"], self._colors[0], size=self._font_sizes[1])
        img_size = warn_surf.height + title_surf.height + self._gap

        self._current_surface = pg.Surface((max(warn_surf.width, title_surf.width) + img_size + self._gap * 3, img_size + self._gap * 2), pg.SRCALPHA)
        self._current_surface.fill((0, 0, 0, 0))
        pg.draw.rect(self._current_surface, self._colors[1], self._current_surface.get_rect(topleft=(0, 0)), border_radius=img_size//10)
        
        if isfile(get_file_path(f"../images/achievements/achiev{self._current_id}.svg")): # Check if the achievement's image exist.
            achiev_img = pg.image.load(get_file_path(f"../images/achievements/achiev{self._current_id}.svg")).convert_alpha()
            achiev_img = pg.transform.scale(achiev_img, ( # Scale achievement's image to be inside the "img_rect".
                round(achiev_img.width * img_size / max(achiev_img.size)),
                round(achiev_img.height * img_size / max(achiev_img.size))
            ))
            self._current_surface.blit(achiev_img, achiev_img.get_rect(topleft=(self._gap, self._gap)))
        else:
            pg.draw.rect(self._current_surface, self._colors[1], pg.Rect((self._gap, self._gap), (img_size, img_size)), border_radius=img_size//10)

        warn_rect.topleft = (self._gap * 2 + img_size, self._gap)
        title_rect.topleft = (self._gap * 2 + img_size, self._gap * 2 + warn_surf.height)

        self._current_surface.blit(warn_surf, warn_rect)
        self._current_surface.blit(title_surf, title_rect)

        self._current_surface_rect = self._current_surface.get_rect(bottomright=(self._size[0] - self._gap, self._size[1] - self._gap))
