import pygame


class Transition:
    def __init__(self, director, next_scene: str):
        self.director = director
        self.next_scene = next_scene
        self.activated = False

    def change_scene(self):
        self.director.change_scene(self.next_scene)

    def on_update(self, dt: float, mouse: tuple) -> None:
        pass

    def on_draw(self, surface: pygame.Surface, mouse: tuple) -> None:
        pass

    def on_load(self):
        self.activated = True

    def on_quit(self):
        """Se llama cuando se abandona la escena"""
        self.activated = False
        self.director.stop_transition()

