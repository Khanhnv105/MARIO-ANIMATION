import pygame
from data.engine.management.transition import Transition


class MainTransition(Transition):
    def __init__(self, director, next_scene: str):
        super().__init__(director, next_scene)
        self.image = pygame.transform.scale2x(
            pygame.image.load("data/Assets/Free/Other/Transition.png")).convert_alpha()
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
        rect = 0, 0, self.director.DISPLAY_SIZE[0] * self.distance, self.director.DISPLAY_SIZE[1]
        pygame.draw.rect(surface, self.image.get_at((44, 44)), rect)

    def on_load(self):
        super().on_load()
        self.distance = 0
        self.mult = 1
