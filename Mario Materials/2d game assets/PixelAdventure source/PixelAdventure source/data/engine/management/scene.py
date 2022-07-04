import pygame


class Scene:
    """Clase de la cual heredan todas las escenas directamente"""

    def __init__(self, director):
        self.director = director

    def on_event(self, event) -> None:
        pass

    def on_update(self, dt: float, mouse: tuple) -> None:
        pass

    def on_draw(self, surface: pygame.Surface, mouse: tuple) -> None:
        pass

    def on_load(self):
        """Se llama cuando se va a usar la escena"""
        pass

    def on_quit(self):
        """Se llama cuando se abandona la escena"""
        pass

    def on_terminate(self):
        """
        Se llama cuando se va a finalizar el programa
        con el objetivo de guardar informacion en el
        caso de ser necesario
        """
        pass
