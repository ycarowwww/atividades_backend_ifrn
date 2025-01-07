import pygame as pg
import pygame.freetype as pgft
from entities import Player, ObstaclesManager, ButtonGroup, ImageButton, PauseButton, ReturnButton, TextButton, Text, Lines
from scripts import BASE_RESOLUTION, FPS, FONT, COLORS, get_file_path
from time import time

# Ink stains (Preferably proceduraly), More Backgrounds, Animations (Death) + Particles, Better dt (like a class)

class Game:
    def __init__(self) -> None:
        pg.init()

        self.__screen: pg.Surface = pg.display.set_mode(BASE_RESOLUTION, pg.RESIZABLE)
        pg.display.set_caption("Duet")
        icon_img = pg.image.load(get_file_path("../images/icon.png")).convert_alpha()
        pg.display.set_icon(icon_img)
        self.__clock: pg.time.Clock = pg.time.Clock()
        self.__MAX_FPS = FPS
        self.__FONT = FONT
        self.__current_window = 1
        self.__windows = { # An Enum will be better for the Keys
            1 : self.main_menu,
            2 : self.main_game,
            3 : self.set_gamemode,
            4 : self.set_level
        }

        self.__is_level = False
        self.__start_level = 0

    def run(self) -> None:
        while self.__current_window != 0:
            window = self.__windows.get(self.__current_window)

            if window == None: break
            else: window()
        
        pg.quit()

    def main_menu(self) -> None:
        def game_bt_func(): self.__current_window = 3
        game_settings = ImageButton((70, 70), (300, 350), "center", lambda: None, get_file_path("../images/gear.svg"), 10, 3, 96, (255, 255, 255))
        game_start = ImageButton((50, 50), (500, 350), "center", game_bt_func, get_file_path("../images/triangle.svg"), 20, 3, 96, (255, 255, 255))
        game_title = Text("DUET", self.__FONT, (255, 255, 255), (400, 150), "center", 70)
        fps_text = Text("FPS: ", self.__FONT, (100, 100, 100), (10, 10), size=15)
        player_background = Player((400, 250), 2, 20)
        player_background.set_circle_colors([COLORS["RED"], COLORS["BLUE"]])
        player_background.toggle_gravity()
        player_background.toggle_control()
        background = Lines(self.__screen.get_size(), 30, COLORS["GRAY"])
        
        game_title.resize(self.__screen.get_size()) # Maybe try to find a better way later
        fps_text.resize(self.__screen.get_size())
        game_start.resize(self.__screen.get_size())
        game_settings.resize(self.__screen.get_size())
        player_background.set_new_resolution(self.__screen.get_size())

        last_time = time() # Maybe a timer later

        while self.__current_window == 1:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.__current_window = 0
                
                if event.type == pg.KEYDOWN: # Change Later
                    if event.key == pg.K_RETURN:
                        self.__current_window = 2 # Open Selected Option
                
                if event.type == pg.VIDEORESIZE:
                    game_title.resize(event.size)
                    fps_text.resize(event.size)
                    background.resize(event.size)

                game_start.update_by_event(event)
                game_settings.update_by_event(event)
                player_background.update_by_event(event)

            self.__clock.tick(self.__MAX_FPS)
            self.__screen.fill(COLORS["BLACK"])

            dt = time() - last_time
            last_time = time()

            background.update(dt)
            background.draw(self.__screen)

            player_background.update(dt)
            player_background.draw(self.__screen)

            game_title.draw(self.__screen)
            game_start.draw(self.__screen)
            game_settings.draw(self.__screen)

            fps_text.set_text(f"FPS: {(dt ** -1):.1f}")
            fps_text.draw(self.__screen)
            
            pg.display.flip()

    def main_game(self) -> None:
        def return_menu_func():
            if pause_button.is_paused:
                self.__current_window = 1
        player = Player([i // 2 for i in BASE_RESOLUTION], 2, 20)
        player.set_circle_colors([COLORS["RED"], COLORS["BLUE"]])
        pause_button = PauseButton((50, 50), (BASE_RESOLUTION[0] - 10, 10), "topright", lambda: None, (255, 255, 255), 15)
        return_menu_button = ReturnButton((50, 50), (BASE_RESOLUTION[0] - 70, 10), "topright", return_menu_func, (255, 255, 255))
        obstacle_manager = ObstaclesManager(player.get_center(), player.get_normal_distance(), player.get_angular_speed(), self.__is_level, self.__start_level)
        score, max_score = 0, 0
        score_text = Text("Score: 0", self.__FONT, (255, 255, 255), (10, 10), size=40)
        max_score_text = Text("Max: 0", self.__FONT, (0, 255, 0), (10, 45), size=20)
        fps_text = Text("FPS: ", self.__FONT, (100, 100, 100), (10, 65), size=15)
        background = Lines(self.__screen.get_size(), 30, COLORS["GRAY"])

        pause_button.resize(self.__screen.get_size()) # Maybe try to find a better way later
        return_menu_button.resize(self.__screen.get_size())
        score_text.resize(self.__screen.get_size())
        max_score_text.resize(self.__screen.get_size())
        fps_text.resize(self.__screen.get_size())
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
                    fps_text.resize(event.size)
                    background.resize(event.size)

            keys = pg.key.get_pressed()

            if keys[pg.K_LSHIFT] and keys[pg.K_ESCAPE]:
                self.__current_window = 1

            self.__clock.tick(self.__MAX_FPS)
            self.__screen.fill(COLORS["BLACK"])

            dt = time() - last_time
            last_time = time()

            background.update(dt)
            background.draw(self.__screen)

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
                obstacle_manager.check_collision(player)

                score = obstacle_manager.get_score()
                max_score = max(max_score, score)
                
                score_text.set_text(f"Score: {score}")
                max_score_text.set_text(f"Max: {max_score}")

            score_text.draw(self.__screen)
            max_score_text.draw(self.__screen)

            fps_text.set_text(f"FPS: {(dt ** -1):.1f}")
            fps_text.draw(self.__screen)
            
            pg.display.flip()

    def set_gamemode(self) -> None:
        def game_bt_func(): self.__current_window = 2
        def game_lvl_func(): 
            self.__is_level = True
            self.__current_window = 4
        player_background = Player((400, 300), 2, 20)
        player_background.set_circle_colors([COLORS["RED"], COLORS["BLUE"]])
        player_background.toggle_gravity()
        player_background.toggle_control()
        fps_text = Text("FPS: ", self.__FONT, (100, 100, 100), (10, 10), size=15)
        background = Lines(self.__screen.get_size(), 30, COLORS["GRAY"])
        buttongroup = ButtonGroup(
            (400, 300), 
            [
                TextButton((0, 0), "center", game_bt_func, "Random Generation", self.__FONT, (255, 255, 255), style=pgft.STYLE_STRONG, size_font=40),
                TextButton((0, 0), "center", game_lvl_func, "Levels", self.__FONT, (255, 255, 255), style=pgft.STYLE_STRONG, size_font=40)
            ],
            25,
            False
            )

        player_background.set_new_resolution(self.__screen.get_size())
        fps_text.resize(self.__screen.get_size())
        buttongroup.resize(self.__screen.get_size())

        last_time = time()

        while self.__current_window == 3:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.__current_window = 0
                
                if event.type == pg.KEYDOWN: # Change Later
                    if event.key == pg.K_RETURN:
                        self.__current_window = 2 # Open Selected Option
                
                if event.type == pg.VIDEORESIZE:
                    fps_text.resize(event.size)
                    background.resize(event.size)

                player_background.update_by_event(event)
                buttongroup.update_by_event(event)

            self.__clock.tick(self.__MAX_FPS)
            self.__screen.fill(COLORS["BLACK"])

            dt = time() - last_time
            last_time = time()

            background.update(dt)
            background.draw(self.__screen)

            player_background.update(dt)
            player_background.draw(self.__screen)

            buttongroup.draw(self.__screen)

            fps_text.set_text(f"FPS: {(dt ** -1):.1f}")
            fps_text.draw(self.__screen)
            
            pg.display.flip()

    def set_level(self) -> None:
        def set_level(n: int): 
            def set_start() -> None:
                self.__current_window = 2
                self.__start_level = n
            return set_start
        player_background = Player((400, 300), 2, 20)
        player_background.set_circle_colors([COLORS["RED"], COLORS["BLUE"]])
        player_background.toggle_gravity()
        player_background.toggle_control()
        fps_text = Text("FPS: ", self.__FONT, (100, 100, 100), (10, 10), size=15)
        background = Lines(self.__screen.get_size(), 30, COLORS["GRAY"])
        buttongroup = ButtonGroup(
            (400, 300), 
            [
                TextButton((0, 0), "center", set_level(1), "I", self.__FONT, (255, 255, 255), (60, 60, 60), pgft.STYLE_STRONG, size_font=40, padding_by_size=(80, 80)),
                TextButton((0, 0), "center", set_level(2), "II", self.__FONT, (255, 255, 255), (60, 60, 60), pgft.STYLE_STRONG, size_font=40, padding_by_size=(80, 80)),
                TextButton((0, 0), "center", set_level(3), "III", self.__FONT, (255, 255, 255), (60, 60, 60), pgft.STYLE_STRONG, size_font=40, padding_by_size=(80, 80))
            ],
            25,
            False
            )

        player_background.set_new_resolution(self.__screen.get_size())
        fps_text.resize(self.__screen.get_size())
        buttongroup.resize(self.__screen.get_size())

        last_time = time()

        while self.__current_window == 4:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.__current_window = 0
                
                if event.type == pg.KEYDOWN: # Change Later
                    if event.key == pg.K_RETURN:
                        self.__current_window = 2 # Open Selected Option
                
                if event.type == pg.VIDEORESIZE:
                    fps_text.resize(event.size)
                    background.resize(event.size)

                player_background.update_by_event(event)
                buttongroup.update_by_event(event)

            self.__clock.tick(self.__MAX_FPS)
            self.__screen.fill(COLORS["BLACK"])

            dt = time() - last_time
            last_time = time()

            background.update(dt)
            background.draw(self.__screen)

            player_background.update(dt)
            player_background.draw(self.__screen)

            buttongroup.draw(self.__screen)

            fps_text.set_text(f"FPS: {(dt ** -1):.1f}")
            fps_text.draw(self.__screen)
            
            pg.display.flip()

if __name__ == '__main__':
    Game().run()
