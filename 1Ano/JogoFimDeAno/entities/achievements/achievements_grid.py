import pygame as pg
import pygame.freetype as pgft
from ..lines import GradientLine
from scripts import ACHIEVEMENTS, ACHIEVEMENTS_UNLOCKED, FONT, scale_dimension

class AchievementsGrid:
    def __init__(self, screen_size: tuple[int, int], base_color: tuple[int, int, int], locked_color: tuple[int, int, int], font_size: int, title_font_size_mult: float, gap: int, font: pgft.Font = FONT) -> None:
        self._achievements = ACHIEVEMENTS
        self._achievements_unlocked = ACHIEVEMENTS_UNLOCKED
        self._size = screen_size
        self._base_color = base_color
        self._locked_color = locked_color
        self._gap = gap
        self._font = font
        self._font_sizes = [ font_size, font_size * title_font_size_mult ]
        self._surface = self._create_surface()

        self._save_values = [ self._gap, self._font_sizes.copy() ]

    def _create_surface(self) -> pg.Surface:
        surf = pg.Surface(self._size)

        line = GradientLine([(0, 0, 0), self._base_color, (0, 0, 0)], (self._size[0] // 2, 0), (self._size[0] // 2, self._size[1]), self._gap // 2)
        line.draw(surf)
        surf.set_colorkey((0, 0, 0))

        max_width_achievement = round(self._size[0] / 2 - 2 * self._gap - self._gap / 2)
        amount_achievements = len(self._achievements)
        actual_heights = [ self._gap, self._gap ]

        for i in range(amount_achievements):
            x = self._gap if i % 2 == 0 else round(self._size[0] / 2 + self._gap + self._gap / 2)
            achievement_surf = self._draw_achievement_surface(max_width_achievement, i+1)
            surf.blit(achievement_surf, (x, actual_heights[i % 2]))
            actual_heights[i % 2] += achievement_surf.height + self._gap
        
        return surf
    
    def draw(self, screen: pg.Surface) -> None:
        screen.blit(self._surface)
    
    def resize(self, new_resolution: tuple[int, int]) -> None:
        self._size = new_resolution
        self._gap = scale_dimension(self._gap, new_resolution)
        self._font_sizes = [ scale_dimension(i, new_resolution) for i in self._save_values[1] ]
        self._surface = self._create_surface()

    def _draw_achievement_surface(self, max_width: int, achievement_id: int) -> pg.Surface:
        if self._gap * 3 >= max_width: raise ValueError("Achievements Grid Draw Individual Achievement Surface : Gap too big or Max Width too low.")

        img_size = round(max_width / 4)
        text_max_width = max_width - 3 * self._gap - img_size
        achievement_dict = self._achievements[str(achievement_id)]

        title_surf = self._draw_text(achievement_dict["title"], self._font, self._base_color, self._font_sizes[1], text_max_width, self._font_sizes[1] // 10) # Bug: It disapears when img_size is too small.
        description_surf = self._draw_text(achievement_dict["description"], self._font, self._base_color, self._font_sizes[0], text_max_width, self._font_sizes[0] // 10)

        print(title_surf.height)

        surf = pg.Surface((max_width, self._gap * 2 + max(title_surf.height + description_surf.height + self._gap, img_size)))

        r_img = pg.Rect((0, 0), (img_size, img_size))
        r_img.midleft = (self._gap, round(surf.height / 2))
        pg.draw.rect(surf, self._base_color, r_img, border_radius=(self._gap // 5))

        surf.blit(title_surf, (self._gap * 2 + img_size, self._gap))
        surf.blit(description_surf, (self._gap * 2 + img_size, self._gap * 2 + title_surf.height))

        return surf

    @staticmethod
    def _draw_text(text: str, font: pgft.Font, fgcolor: tuple[int, int, int], size: int, max_width: int, vertical_gap: int) -> pg.Surface:
        if len(text) <= 0: return
        if font.get_rect("---", size=size).width > max_width: raise ValueError("Max Width too Low for the font size.")
        
        if font.get_rect(text, size=size).width <= max_width:
            text_surf, text_rect = font.render(text, fgcolor, size=size)

            surf = pg.Surface(text_surf.size)
            surf.blit(text_surf, text_rect)
            return surf
        else:
            surf_group: list[tuple[pg.Surface, pg.Rect]] = []
            words = text.split(" ")
            actual_word = 0
            actual_width = 0
            actual_height = 0

            while actual_word < len(words):
                actual_text = words[actual_word]
                amount = 1

                while font.get_rect(actual_text, size=size).width < max_width:
                    if not actual_word + 1 < len(words): break
                    actual_word += 1
                    amount += 1
                    actual_text = f"{actual_text} {words[actual_word]}"
                else:
                    if amount == 1:
                        for i in range(1, len(actual_text)):
                            current_text_index = i
                            text = actual_text[:current_text_index] + "-"
                            if font.get_rect(text, size=size).width > max_width:
                                words.insert(actual_word+1, actual_text[current_text_index-1:])
                                actual_text = actual_text[:current_text_index-1] + "-"
                                break
                    else:
                        amount -= 1
                        actual_word -= 1
                        actual_text = " ".join(actual_text.split(" ")[:-1])
                
                text_surf, text_rect = font.render(actual_text, fgcolor, size=size)
                text_rect.topleft = (0, 0)
                surf_group.append((text_surf, text_rect))
                actual_height += text_surf.height + vertical_gap
                actual_width = max(text_surf.width, actual_width)

                actual_word += 1
            
            surf = pg.Surface((actual_width, actual_height))
            y_pos = 0
            
            for i in range(len(surf_group)):
                surf.blit(surf_group[i][0], surf_group[i][1])
                y_pos += surf_group[i][1].height + vertical_gap
                if i < len(surf_group) - 1:
                    surf_group[i+1][1].top = y_pos
            
            return surf
