from math import sin

import pygame


class DynamicBackground:
    def __init__(self, c1, c2):
        self.c1 = pygame.Color(c1[0], c1[1], c1[2])
        self.c2 = pygame.Color(c2[0], c2[1], c2[2])
        self.size = 100
        self.inclination = 1

    def update(self, **kwargs):
        self.size = 100 + sin(kwargs["clock_ticks"] / 1000) * 30

    def draw(self, surface, offset):
        size = self.size
        display_width = surface.get_width()
        display_height = surface.get_height()
        for i, iteration in enumerate(range(int(display_width / size) + 0)):
            pygame.draw.polygon(
                surface,
                self.c1 if i % 2 == 0 else self.c2,
                [
                    [i * size, 0],
                    [(i + self.inclination) * size, 0],
                    [i * size, display_height],
                    [(i - self.inclination) * size, display_height]
                ]
            )
