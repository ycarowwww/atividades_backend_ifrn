import pygame as pg

class MouseHandler:
    __current_cursor = None
    __cursor_modified = False

    @classmethod
    def update_cursor(self) -> None:
        if self.__current_cursor != None:
            pg.mouse.set_cursor(self.__current_cursor)
            self.__cursor_modified = True
            self.__current_cursor = None
        elif self.__cursor_modified:
            pg.mouse.set_cursor(pg.SYSTEM_CURSOR_ARROW)
            self.__cursor_modified = False
        
    @classmethod
    def change_cursor(self, cursor: int) -> None:
        self.__current_cursor = cursor
