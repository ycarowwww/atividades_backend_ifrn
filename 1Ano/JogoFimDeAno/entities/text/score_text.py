import pygame as pg
import pygame.freetype as pgft
from scripts import scale_dimension, scale_position, BASE_RESOLUTION

class ScoreText:
    def __init__(self, score: int, hidden_fgcolor: tuple[int, int, int], fgcolor: tuple[int, int, int], font: pgft.Font, font_size: int, position: tuple[int, int], pos_attr: str, min_number_zeros: int) -> None:
        """Creates a custom Text for the Score.
            
            score (int): current score
            hidden_fgcolor (tuple[int, int, int]): color of the 0s part
            fgcolor (tuple[int, int, int]): color of the real score
            font (pgft.Font): Font of the text
            font_size (int): Size of the Font
            position (tuple[int, int]): position of all the text
            pos_attr (str): position attribute of the text
            min_number_zeros (int): Number of 0s to the left
        """
        self._score = score
        self._colors = (
            fgcolor,
            hidden_fgcolor
        )
        self._font = font
        self._font_size = font_size
        self._position = position
        self._pos_attr = pos_attr
        self._num_0s = min_number_zeros
        self._surface, self._surface_rect = self._generate_surface()

        self._save_values = (self._font_size, self._position)

    def draw(self, screen: pg.Surface) -> None:
        screen.blit(self._surface, self._surface_rect)

    def resize(self, new_resolution: tuple[int, int]) -> None:
        self._position = scale_position(self._save_values[1], BASE_RESOLUTION, new_resolution)
        self._font_size = scale_dimension(self._save_values[0], new_resolution)
        self._surface, self._surface_rect = self._generate_surface()
    
    def set_score(self, new_score: int) -> None:
        self._score = max(0, new_score)
        self._surface, self._surface_rect = self._generate_surface()
    
    def _generate_surface(self) -> tuple[pg.Surface, pg.Rect]:
        len_0s = self._num_0s - len(str(self._score))

        if len_0s <= 0:
            text_surf, text_rect = self._font.render(str(self._score), self._colors[0], size=self._font_size)
            text_rect.topleft = (0, 0)
            surf = pg.Surface(text_rect.size)
            surf.blit(text_surf, text_rect)
        else:
            text_0_surf, text_0_rect = self._font.render("0" * len_0s, self._colors[1], size=self._font_size)
            score_surf, score_rect = self._font.render(str(self._score), self._colors[0], size=self._font_size)

            spacing_2_surfs = self._font.get_rect("0" + str(self._score)[0], size=self._font_size).width - self._font.get_rect("0", size=self._font_size).width - self._font.get_rect(str(self._score)[0], size=self._font_size).width

            width = text_0_rect.width + spacing_2_surfs + score_rect.width
            height = max(text_0_rect.height, score_rect.height)

            surf = pg.Surface((width, height))

            text_0_rect.topleft = (0, 0)
            score_rect.topleft = (width - score_rect.width, 0)
            surf.blit(text_0_surf, text_0_rect)
            surf.blit(score_surf, score_rect)

        surf.set_colorkey((0, 0, 0))

        surf_rect = surf.get_rect()
        setattr(surf_rect, self._pos_attr, self._position)

        return (surf, surf_rect)
