import pygame as pg
from typing import Any

class CustomEventHandler:
    @staticmethod
    def post_event(event: int, properties: dict[str, Any] = {}) -> None:
        pg.event.post(pg.event.Event(event, properties))
