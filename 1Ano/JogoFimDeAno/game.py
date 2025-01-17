import pygame as pg
import pygame.freetype as pgft
from entities import Player, ObstaclesManager, ButtonGroup, ImageButton, PauseButton, ReturnButton, TextButton, Text, Lines, CustomEventList, EventPauser
from scripts import BASE_RESOLUTION, FPS, FONT, COLORS, get_file_path
from enum import IntEnum, auto
from time import time

# More Backgrounds, Animations, Better dt (like a class)

class WindowsKeys(IntEnum):
    """Enum with the Windows Keys."""
    QUIT = auto()
    MAINMENU = auto()
    MAINGAME = auto()
    SETGAMEMODE = auto()
    SETLEVEL = auto()

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
        self.__current_window = WindowsKeys.MAINMENU
        self.__windows = { # An Enum will be better for the Keys
            WindowsKeys.MAINMENU : self.main_menu,
            WindowsKeys.MAINGAME : self.main_game,
            WindowsKeys.SETGAMEMODE : self.set_gamemode,
            WindowsKeys.SETLEVEL : self.set_level
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
        def game_bt_func(): self.__current_window = WindowsKeys.SETGAMEMODE
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
        player_background.resize(self.__screen.get_size())

        last_time = time() # Maybe a timer later

        while self.__current_window == WindowsKeys.MAINMENU:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.__current_window = WindowsKeys.QUIT
                
                if event.type == pg.KEYDOWN: # Change Later
                    if event.key == pg.K_RETURN:
                        self.__current_window = WindowsKeys.SETGAMEMODE # Open Selected Option
                
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
                self.__current_window = WindowsKeys.MAINMENU
        player = Player([i // 2 for i in BASE_RESOLUTION], 2, 20)
        player.set_circle_colors([COLORS["RED"], COLORS["BLUE"]])
        event_pauser = EventPauser()
        pause_button = PauseButton((50, 50), (BASE_RESOLUTION[0] - 10, 10), "topright", event_pauser.toggle_timers, (255, 255, 255), 15)
        return_menu_button = ReturnButton((50, 50), (BASE_RESOLUTION[0] - 70, 10), "topright", return_menu_func, (255, 255, 255))
        obstacle_manager = ObstaclesManager(player.get_center(), player.get_normal_distance(), player.get_angular_speed(), self.__is_level, self.__start_level)
        score, max_score = 0, 0
        score_text = Text("Score: 0", self.__FONT, (255, 255, 255), (10, 10), size=40)
        max_score_text = Text("Max: 0", self.__FONT, (0, 255, 0), (10, 45), size=20)
        collision_count = Text("Collisions: 0", self.__FONT, (255, 255, 255), (10, 65), size=20)
        fps_text = Text("FPS: ", self.__FONT, (100, 100, 100), (10, 85), size=15)
        background = Lines(self.__screen.get_size(), 30, COLORS["GRAY"])
        warn_text = Text("New Level: 0", self.__FONT, (255, 255, 255), (400, 200), "center", 30)
        show_warn = False
        player_collided = False

        pause_button.resize(self.__screen.get_size()) # Maybe try to find a better way later
        return_menu_button.resize(self.__screen.get_size())
        score_text.resize(self.__screen.get_size())
        max_score_text.resize(self.__screen.get_size())
        collision_count.resize(self.__screen.get_size())
        fps_text.resize(self.__screen.get_size())
        player.resize(self.__screen.get_size())
        obstacle_manager.resize(self.__screen.get_size(), player.get_center(), player.get_normal_distance())
        warn_text.resize(self.__screen.get_size())

        last_time = time()

        while self.__current_window == WindowsKeys.MAINGAME:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.__current_window = WindowsKeys.QUIT
                
                pause_button.update_by_event(event)
                return_menu_button.update_by_event(event)
                player.update_by_event(event)

                if event.type == pg.VIDEORESIZE:
                    obstacle_manager.resize(event.size, player.get_center(), player.get_normal_distance())
                    score_text.resize(event.size)
                    max_score_text.resize(event.size)
                    collision_count.resize(event.size)
                    fps_text.resize(event.size)
                    background.resize(event.size)
                    warn_text.resize(event.size)
                
                if event.type == CustomEventList.NEWLEVELWARNING:
                    warn_text.set_text(f"New Level: {event.level}")
                    pg.time.set_timer(CustomEventList.DISABLEWARNING, 1000, 1)
                    event_pauser.add_event(CustomEventList.DISABLEWARNING, 1000, 1) # Maybe we can get this better with the "EventHandler"
                    show_warn = True
                
                if event.type == CustomEventList.NEWGENERATIONWARNING:
                    warn_text.set_text("New Generated Obstacles")
                    pg.time.set_timer(CustomEventList.DISABLEWARNING, 1000, 1)
                    event_pauser.add_event(CustomEventList.DISABLEWARNING, 1000, 1)
                    show_warn = True
                
                if event.type == CustomEventList.DISABLEWARNING:
                    show_warn = False
                
                if event.type == CustomEventList.PLAYERCOLLISION: # Maybe handle this on the player's class
                    pg.time.set_timer(CustomEventList.RESETGAME, 500, 1)
                    event_pauser.add_event(CustomEventList.RESETGAME, 500, 1)
                    player_collided = True
                    player.add_lost_particles(event.indexes)
                
                if event.type == CustomEventList.RESETGAME:
                    player_collided = False
                    player.reset_movements()
                    obstacle_manager.reset()

            keys = pg.key.get_pressed()

            if keys[pg.K_LSHIFT] and keys[pg.K_ESCAPE]:
                self.__current_window = WindowsKeys.MAINMENU

            self.__clock.tick(self.__MAX_FPS)
            self.__screen.fill(COLORS["BLACK"])

            dt = time() - last_time
            last_time = time()

            event_pauser.update(dt)

            background.update(dt)
            background.draw(self.__screen)

            pause_button.draw(self.__screen)

            if pause_button.is_paused:
                player.draw(self.__screen)
                obstacle_manager.draw(self.__screen)
                return_menu_button.draw(self.__screen)
            else:
                if not player_collided:
                    player.update(dt)
                    obstacle_manager.update(dt)
                    obstacle_manager.check_collision(player)
                else:
                    player.update_lost_particles(dt)

                player.draw(self.__screen)
                obstacle_manager.draw(self.__screen)

                score = obstacle_manager.get_score()
                max_score = max(max_score, score)
                collisions = obstacle_manager.get_player_collision_count()
                
                score_text.set_text(f"Score: {score}")
                max_score_text.set_text(f"Max: {max_score}")
                collision_count.set_text(f"Collisions: {collisions}")

            score_text.draw(self.__screen)
            max_score_text.draw(self.__screen)
            collision_count.draw(self.__screen)

            if show_warn:
                warn_text.draw(self.__screen)

            fps_text.set_text(f"FPS: {(dt ** -1):.1f}")
            fps_text.draw(self.__screen)
            
            pg.display.flip()

    def set_gamemode(self) -> None:
        def game_bt_func(): 
            self.__is_level = False
            self.__current_window = WindowsKeys.MAINGAME
        def game_lvl_func(): 
            self.__is_level = True
            self.__current_window = WindowsKeys.SETLEVEL
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

        player_background.resize(self.__screen.get_size())
        fps_text.resize(self.__screen.get_size())
        buttongroup.resize(self.__screen.get_size())

        last_time = time()

        while self.__current_window == WindowsKeys.SETGAMEMODE:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.__current_window = WindowsKeys.QUIT
                
                if event.type == pg.KEYDOWN: # Change Later
                    if event.key == pg.K_ESCAPE:
                        self.__current_window = WindowsKeys.MAINMENU
                    
                    if event.key == pg.K_RETURN:
                        self.__current_window = WindowsKeys.MAINGAME # Open Selected Option
                
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
                self.__current_window = WindowsKeys.MAINGAME
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

        player_background.resize(self.__screen.get_size())
        fps_text.resize(self.__screen.get_size())
        buttongroup.resize(self.__screen.get_size())

        last_time = time()

        while self.__current_window == WindowsKeys.SETLEVEL:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.__current_window = WindowsKeys.QUIT
                
                if event.type == pg.KEYDOWN: # Change Later
                    if event.key == pg.K_ESCAPE:
                        self.__is_level = False
                        self.__current_window = WindowsKeys.SETGAMEMODE
                    
                    if event.key == pg.K_RETURN:
                        self.__current_window = WindowsKeys.MAINGAME # Open Selected Option
                
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
