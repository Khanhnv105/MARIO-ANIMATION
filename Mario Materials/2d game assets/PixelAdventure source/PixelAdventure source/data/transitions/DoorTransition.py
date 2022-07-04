import pygame
from data.engine.management.transition import Transition


class DoorTransition(Transition):
    def __init__(self, director, next_scene: str):
        super().__init__(director, next_scene)
        self.distance = 0
        self.mult = 1

    def on_update(self, dt: float, mouse: tuple) -> None:
        if self.activated:
            self.distance += 0.03 * dt * self.mult
            if self.distance >= 1.1 and self.mult == 1:
                self.mult = -1
                self.change_scene()

            elif self.distance < 0:
                self.on_quit()

    def on_draw(self, surface: pygame.Surface, mouse: tuple) -> None:
        width = int(self.director.DISPLAY_SIZE[0] * self.distance / 2)
        COLOR = (0, 0, 0)
        pygame.draw.rect(
            surface,
            COLOR,
            (
                0,
                0,
                width,
                self.director.DISPLAY_SIZE[1]
            )
        )
        pygame.draw.rect(
            surface,
            COLOR,
            (
                self.director.DISPLAY_SIZE[0] - width,
                0,
                width,
                self.director.DISPLAY_SIZE[1]
            )
        )

    def on_load(self):
        super().on_load()
        self.distance = 0
        self.mult = 1
