import pygame
from pygame.locals import *
from .tiled_map import TiledMap
from ..management.scene import Scene
from data.engine.camera.old.camera import Camera


class Level(Scene):
    def __init__(self, director, tmx_path: str):
        super().__init__(director)
        self.tiled_level = TiledMap(tmx_path)
        self.camera = Camera(1, self.director.SIZE)

    def on_event(self, event) -> None:
        if event.type == MOUSEBUTTONDOWN:
            self.camera.start_scroll()
        elif event.type == MOUSEBUTTONUP:
            self.camera.stop_scroll()

        elif event.type == MOUSEWHEEL:
            if event.y > 0:
                self.camera.zoom("in")
            else:
                self.camera.zoom("out")

    def on_update(self, dt: float, mouse: tuple) -> None:
        self.camera.update(None, dt)
        scroll = self.camera.get_scroll()
        zoom = self.camera.get_zoom()

        if self.camera.moved():
            display_rect = pygame.Rect(0, 0, self.director.SIZE[0], self.director.SIZE[1])

            if self.camera.zoom_changed():
                self.tiled_level.zoom_changed(scroll, zoom, display_rect)
            if self.camera.scroll_changed():
                self.tiled_level.scroll_changed(scroll, zoom, display_rect)

        self.tiled_level.update(zoom, scroll)

    def on_draw(self, surface: pygame.Surface, mouse: tuple) -> None:
        surface.fill((200, 200, 200))
        self.tiled_level.draw(surface)
