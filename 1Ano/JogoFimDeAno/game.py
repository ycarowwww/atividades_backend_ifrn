import pygame as pg
import pygame.freetype as pgft
from entities.player import Player
from entities.obstacles.obstacles_manager import ObstaclesManager
from scripts.settings import *

# Create buttons classes and Framerate Independence

class Game:
    def __init__(self):
        pg.init()

        self.SCREEN_SIZE = SCREEN_SIZE
        self.screen: pg.Surface = pg.display.set_mode(self.SCREEN_SIZE)
        pg.display.set_caption("Pygame Game")
        self.clock: pg.time.Clock = pg.time.Clock()
        self.FPS = FPS
        self.current_window = 1 # 1 : Menu | 2 : Game | Change to a dictionary after
        self.GAME_FONT = GAME_FONT
        self.MAX_SCORE_FONT = MAX_SCORE_FONT
        self.player = Player([i // 2 for i in self.SCREEN_SIZE], [COLORS["BLUE"], COLORS["RED"]], COLORS["GRAY"], 20)

    def run(self):
        while self.current_window != 0:
            match self.current_window:
                case 1: self.main_menu()
                case 2: self.main_game()
        
        pg.quit()

    def main_menu(self):
        SCREEN_CENTER: tuple[int, int] = tuple([i // 2 for i in self.SCREEN_SIZE])
        title_surf, title_rect = self.GAME_FONT.render("DUET", COLORS["WHITE"], style=pgft.STYLE_STRONG)
        title_rect.center = (SCREEN_CENTER[0], 100)
        game_surf, game_rect = self.GAME_FONT.render("Game", COLORS["WHITE"], COLORS["BLUE"])
        game_rect.center = SCREEN_CENTER

        while self.current_window == 1:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.current_window = 0
                
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_RETURN:
                        self.current_window = 2 # Open Selected Option
                
                if event.type == pg.MOUSEBUTTONDOWN:
                    mpos = event.pos
                    
                    if game_rect.collidepoint(mpos):
                        self.current_window = 2

            self.clock.tick(self.FPS)
            self.screen.fill(COLORS["BLACK"])

            self.screen.blit(title_surf, title_rect)
            self.screen.blit(game_surf, game_rect)
            
            pg.display.flip()

    def main_game(self):
        paused: bool = False
        pause_button_rect: pg.Rect = pg.Rect(0, 0, 50, 50)
        pause_button_rect.topright = (SCREEN_SIZE[0] - 10, 10)
        pause_button_triangle: list[tuple[int, int]] = (pause_button_rect.topleft, pause_button_rect.bottomleft, (pause_button_rect.right, pause_button_rect.centery))
        pause_button_rects: list[pg.Rect] = [pg.Rect(0, 0, 20, 50), pg.Rect(0, 0, 20, 50)]
        pause_button_rects[0].topright = pause_button_rect.topright
        pause_button_rects[1].topright = (pause_button_rects[0].right - 30, pause_button_rects[0].top)
        return_menu_button: pg.Rect = pg.Rect(0, 0, 50, 50)
        return_menu_button.topright = (pause_button_rect.left - 10, pause_button_rect.top)
        punctuation, max_score = 0, 0
        obstacle_manager = ObstaclesManager()

        while self.current_window == 2:
            key = pg.key.get_pressed()

            if key[pg.K_LSHIFT] and key[pg.K_ESCAPE]:
                self.current_window = 1

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.current_window = 0

                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        paused = not paused
                    if event.key == pg.K_b:
                        self.player.toggle_border()

                if event.type == pg.MOUSEBUTTONDOWN:
                    mx, my = event.pos

                    if pause_button_rect.collidepoint(mx, my):
                        paused = not paused
                    elif paused and return_menu_button.collidepoint(mx, my):
                        self.current_window = 1

            self.clock.tick(FPS)
            self.screen.fill(COLORS["BLACK"])

            if paused:
                pg.draw.polygon(self.screen, COLORS["WHITE"], pause_button_triangle)
                pg.draw.polygon(self.screen, COLORS["WHITE"], (return_menu_button.topright, return_menu_button.bottomright, (return_menu_button.left, return_menu_button.centery)))

                self.player.draw(self.screen)

                obstacle_manager.draw(self.screen)
                
                blit_text(self.screen, f"Score: {punctuation}", COLORS["WHITE"], (10, 10), GAME_FONT)
                blit_text(self.screen, f"Max: {max_score}", COLORS["GREEN"], (10, 40), MAX_SCORE_FONT)
                
                pg.display.flip()
                continue
            else:
                for rt in pause_button_rects:
                    pg.draw.rect(self.screen, COLORS["WHITE"], rt)

            self.player.update()
            self.player.draw(self.screen)

            obstacle_manager.update()
            obstacle_manager.draw(self.screen)
            
            if obstacle_manager.check_collision(self.player):
                punctuation = 0
            elif obstacle_manager.get_obstacle_removed():
                punctuation += 1
                max_score = max(max_score, punctuation)
            
            blit_text(self.screen, f"Score: {punctuation}", COLORS["WHITE"], (10, 10), GAME_FONT)
            blit_text(self.screen, f"Max: {max_score}", COLORS["GREEN"], (10, 40), MAX_SCORE_FONT)
            
            pg.display.flip()

if __name__ == '__main__':
    Game().run()
