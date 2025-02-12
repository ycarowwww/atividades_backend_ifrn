import pygame as pg

class EventPauser:
    """Pauses event timers when the game is paused."""
    _current_events: list[int] = []
    _current_times_remaining: list[float] = []
    _current_loops: list[int] = []
    _is_paused = False
    
    @classmethod
    def update(self, dt: float) -> None:
        """Updates the remaining time of each of the event timers. 'dt' needs to be in seconds."""
        if self._is_paused: return
        
        indexes_to_remove = []
        for i in range(len(self._current_times_remaining)):
            self._current_times_remaining[i] -= dt * 1000
            if self._current_times_remaining[i] <= 0:
                indexes_to_remove.insert(0, i)
        
        for i in indexes_to_remove:
            self._current_events.pop(i)
            self._current_times_remaining.pop(i)
            self._current_loops.pop(i)
    
    @classmethod
    def add_event(self, event: int, mills: int, loops: int = 0) -> None:
        self._current_events.append(event)
        self._current_times_remaining.append(mills)
        self._current_loops.append(loops)

    @classmethod
    def toggle_timers(self) -> None:
        """Updates the paused or unpaused status of events."""
        self._is_paused = not self._is_paused

        if self._is_paused:
            for event in self._current_events:
                pg.time.set_timer(event, 0, 0)
        else:
            for event, time, loops in zip(self._current_events, self._current_times_remaining, self._current_loops):
                pg.time.set_timer(event, round(time), loops)
