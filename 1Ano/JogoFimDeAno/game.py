import pygame as pg
import pygame.freetype as pgft
from entities.player import Player
from entities.buttons.pause_button import PauseButton
from entities.buttons.return_button import ReturnButton
from entities.buttons.text_button import TextButton
from entities.obstacles.obstacles_manager import ObstaclesManager
from scripts.settings import *

# Create Framerate Independence, Fix obstacles movement, Menu and Custom Screen Size

class Game:
    def __init__(self):
        pg.init()

        self.__SCREEN_SIZE = SCREEN_SIZE
        self.__screen: pg.Surface = pg.display.set_mode(self.__SCREEN_SIZE)
        pg.display.set_caption("Duet")
        self.__clock: pg.time.Clock = pg.time.Clock()
        self.__FPS = FPS
        self.__current_window = 1 # 1 : Menu | 2 : Game | Change to a dictionary/enum after
        self.__GAME_FONT = GAME_FONT
        self.__MAX_SCORE_FONT = MAX_SCORE_FONT

    def run(self):
        while self.__current_window != 0:
            match self.__current_window:
                case 1: self.main_menu()
                case 2: self.main_game()
        
        pg.quit()

    def main_menu(self):
        SCREEN_CENTER: tuple[int, int] = tuple([i // 2 for i in self.__SCREEN_SIZE])

        def game_bt_func(): self.__current_window = 2
        game_button = TextButton((0, 0), game_bt_func, "Game", self.__GAME_FONT, COLORS["WHITE"], COLORS["BLUE"], padding=15)
        game_button.set_position_attr("center", SCREEN_CENTER)

        while self.__current_window == 1:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.__current_window = 0
                
                if event.type == pg.KEYDOWN: # Change Later
                    if event.key == pg.K_RETURN:
                        self.__current_window = 2 # Open Selected Option

                game_button.update_by_event(event)

            self.__clock.tick(self.__FPS)
            self.__screen.fill(COLORS["BLACK"])

            game_button.draw(self.__screen)
            blit_text(self.__screen, "DUET", COLORS["WHITE"], self.__GAME_FONT, (SCREEN_CENTER[0], 100), "center", style=pgft.STYLE_STRONG)
            
            pg.display.flip()

    def main_game(self):
        def return_menu_func():
            if pause_button.is_paused:
                self.__current_window = 1
        player = Player([i // 2 for i in self.__SCREEN_SIZE], [COLORS["BLUE"], COLORS["RED"]], COLORS["GRAY"], 20)
        pause_button = PauseButton((50, 50), (SCREEN_SIZE[0] - 60, 10), lambda: None, (255, 255, 255), 15)
        return_menu_button = ReturnButton((50, 50), (SCREEN_SIZE[0] - 120, 10), return_menu_func, (255, 255, 255))
        punctuation, max_score = 0, 0
        obstacle_manager = ObstaclesManager()

        while self.__current_window == 2:
            key = pg.key.get_pressed()

            if key[pg.K_LSHIFT] and key[pg.K_ESCAPE]:
                self.__current_window = 1

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.__current_window = 0
                
                pause_button.update_by_event(event)
                player.update_by_event(event)
                return_menu_button.update_by_event(event)

            self.__clock.tick(self.__FPS)
            self.__screen.fill(COLORS["BLACK"])

            pause_button.draw(self.__screen)

            if pause_button.is_paused:
                player.draw(self.__screen)
                obstacle_manager.draw(self.__screen)
                return_menu_button.draw(self.__screen)
                
                blit_text(self.__screen, f"Score: {punctuation}", COLORS["WHITE"], self.__GAME_FONT, (10, 10), "topleft")
                blit_text(self.__screen, f"Max: {max_score}", COLORS["GREEN"], self.__MAX_SCORE_FONT, (10, 40), "topleft")
                
                pg.display.flip()
                continue

            player.update()
            player.draw(self.__screen)

            obstacle_manager.update()
            obstacle_manager.draw(self.__screen)
            
            if obstacle_manager.check_collision(player):
                punctuation = 0
            elif obstacle_manager.get_obstacle_removed():
                punctuation += 1
                max_score = max(max_score, punctuation)
            
            blit_text(self.__screen, f"Score: {punctuation}", COLORS["WHITE"], self.__GAME_FONT, (10, 10), "topleft")
            blit_text(self.__screen, f"Max: {max_score}", COLORS["GREEN"], self.__MAX_SCORE_FONT, (10, 40), "topleft")
            
            pg.display.flip()

if __name__ == '__main__':
    Game().run()
