import pygame


class Clock:
    def __init__(self):
        self.START_TIME = 0

        self.milliseconds = 0
        self.seconds = 0
        self.minutes = 0
        self.time_out = 0
        self.last_time = 0

    def resume(self):
        self.time_out += pygame.time.get_ticks() - self.last_time

    def restart(self):
        self.START_TIME = pygame.time.get_ticks()
        self.time_out = 0

    def update(self, **kwargs):
        self.last_time = kwargs["clock_ticks"]
        self.milliseconds = kwargs["clock_ticks"] - self.START_TIME - self.time_out
        self.seconds = self.milliseconds // 1000
        self.minutes = self.seconds // 60

        m, self.seconds = divmod(self.seconds, 60)
        h, self.minutes = divmod(m, 60)

    def get_seconds(self):
        return self.seconds

    def get_time(self):
        return f"{self.minutes}:{self.get_seconds()}"
