import pygame as pg
import pygame.freetype as pgft
from entities.player import Player # Use Packages
from entities.buttons.pause_button import PauseButton
from entities.buttons.return_button import ReturnButton
from entities.buttons.text_button import TextButton
from entities.obstacles.obstacles_manager import ObstaclesManager
from entities.text.text import Text
from scripts.settings import *
from time import time

# Menu, Good Punctuation, Background
# Maybe use an Enum to the windows, FPS Viewer

class Game:
    def __init__(self):
        pg.init()

        self.__screen: pg.Surface = pg.display.set_mode(BASE_RESOLUTION, pg.RESIZABLE)
        pg.display.set_caption("Duet")
        icon_img = pg.image.load(get_file_path("../images/icon.png")).convert_alpha()
        pg.display.set_icon(icon_img)
        self.__clock: pg.time.Clock = pg.time.Clock()
        self.__MAX_FPS = FPS
        self.__current_window = 1 # 1 : Menu | 2 : Game | Change to a dictionary/enum after
        self.__FONT = FONT

    def run(self):
        while self.__current_window != 0:
            match self.__current_window:
                case 1: self.main_menu()
                case 2: self.main_game()
        
        pg.quit()

    def main_menu(self):
        def game_bt_func(): self.__current_window = 2
        game_button = TextButton((400, 300), "center", game_bt_func, "Game", self.__FONT, COLORS["WHITE"], COLORS["BLUE"], size_font=30, padding=15)
        game_title = Text("DUET", self.__FONT, (255, 255, 255), (400, 150), "center", 70)
        game_button.resize(self.__screen.get_size()) # Change later
        game_title.resize(self.__screen.get_size())

        while self.__current_window == 1:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.__current_window = 0
                
                if event.type == pg.KEYDOWN: # Change Later
                    if event.key == pg.K_RETURN:
                        self.__current_window = 2 # Open Selected Option
                
                if event.type == pg.VIDEORESIZE:
                    game_title.resize(event.size)

                game_button.update_by_event(event)

            self.__clock.tick(self.__MAX_FPS)
            self.__screen.fill(COLORS["BLACK"])

            game_button.draw(self.__screen)
            game_title.draw(self.__screen)
            
            pg.display.flip()

    def main_game(self):
        def return_menu_func():
            if pause_button.is_paused:
                self.__current_window = 1
        player = Player([i // 2 for i in BASE_RESOLUTION], 2, 20) # Player Tracker Decreasing Size - Bug:
        player.set_circle_colors([COLORS["RED"], COLORS["BLUE"]])
        pause_button = PauseButton((50, 50), (BASE_RESOLUTION[0] - 10, 10), "topright", lambda: None, (255, 255, 255), 15)
        return_menu_button = ReturnButton((50, 50), (BASE_RESOLUTION[0] - 70, 10), "topright", return_menu_func, (255, 255, 255))
        punctuation, max_score = 0, 0
        obstacle_manager = ObstaclesManager(player.get_center(), player.get_normal_distance(), player.get_angular_speed())
        score_text = Text("Score: 0", self.__FONT, (255, 255, 255), (10, 10), size=40)
        max_score_text = Text("Max: 0", self.__FONT, (0, 255, 0), (10, 45), size=20)

        pause_button.resize(self.__screen.get_size()) # Maybe try to find a better way later
        return_menu_button.resize(self.__screen.get_size())
        score_text.resize(self.__screen.get_size())
        max_score_text.resize(self.__screen.get_size())
        player.set_new_resolution(self.__screen.get_size())
        obstacle_manager.set_new_resolution(self.__screen.get_size(), player.get_center(), player.get_normal_distance())

        last_time = time()

        while self.__current_window == 2:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.__current_window = 0
                
                pause_button.update_by_event(event)
                return_menu_button.update_by_event(event)
                player.update_by_event(event)

                if event.type == pg.VIDEORESIZE:
                    obstacle_manager.set_new_resolution(event.size, player.get_center(), player.get_normal_distance())
                    score_text.resize(event.size)
                    max_score_text.resize(event.size)

            keys = pg.key.get_pressed()

            if keys[pg.K_LSHIFT] and keys[pg.K_ESCAPE]:
                self.__current_window = 1

            self.__clock.tick(self.__MAX_FPS)
            self.__screen.fill(COLORS["BLACK"])

            dt = time() - last_time
            last_time = time()

            pause_button.draw(self.__screen)

            if pause_button.is_paused:
                player.draw(self.__screen)
                obstacle_manager.draw(self.__screen)
                return_menu_button.draw(self.__screen)
            else:
                player.update(dt)
                player.draw(self.__screen)

                obstacle_manager.update(dt)
                obstacle_manager.draw(self.__screen)
                
                if obstacle_manager.check_collision(player):
                    punctuation = 0
                elif obstacle_manager.get_obstacles_passed() > 0:
                    punctuation += obstacle_manager.get_obstacles_passed()
                    max_score = max(max_score, punctuation)
                
                score_text.set_text(f"Score: {punctuation}")
                max_score_text.set_text(f"Max: {max_score}")

            score_text.draw(self.__screen)
            max_score_text.draw(self.__screen)
            
            pg.display.flip()

if __name__ == '__main__':
    Game().run()
