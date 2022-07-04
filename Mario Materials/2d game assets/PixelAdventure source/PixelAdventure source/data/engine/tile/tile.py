""""from typing import List
import pygame


class Tile:
    def __init__(
            self,
            images: List[pygame.Surface],
            image_index: int,
            x_grid_pos: int,
            y_grid_pos: int
    ):
        self.IMAGE_INDEX = image_index
        self.IMAGE_DIMENSIONS = images[image_index].get_size()
        self.image_dimensions = self.IMAGE_DIMENSIONS
        self.GRID_POSITION = x_grid_pos, y_grid_pos

        self.POSITION = (
            self.GRID_POSITION[0] * self.IMAGE_DIMENSIONS[0],
            self.GRID_POSITION[1] * self.IMAGE_DIMENSIONS[1]
        )
        self.display_position = self.POSITION

        self.image = images[image_index]
        self.rect = self.get_rect()

    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(
            self.display_position[0],
            self.display_position[1],
            self.image_dimensions[0],
            self.image_dimensions[1]
        )

    def _set_visible(self, boolean):
        self.visible = boolean

    def is_visible(self, display_rect: pygame.Rect):
        return self.rect.colliderect(display_rect)

    def update(self, **kwargs) -> None:
        pass

    def camera_moved(self, scroll, zoom=1):
        self.display_position = (
            int(self.POSITION[0] * zoom - scroll[0]),
            int(self.POSITION[1] * zoom - scroll[1])
        )
        self.rect = pygame.Rect(
            self.display_position[0],
            self.display_position[1],
            self.IMAGE_DIMENSIONS[0],
            self.IMAGE_DIMENSIONS[1]
        )

    def draw(self, surface):
        surface.blit(
            self.image,
            self.display_position
        )
"""
import pygame

from data.engine.camera.functions import game_to_display
from data.engine.image.editor import scale_image


class Tile:
    def __init__(
            self,
            image: pygame.Surface,
            x_grid_pos: int,
            y_grid_pos: int
    ):
        self.IMAGE = image
        self.GRID_POSITION = x_grid_pos, y_grid_pos
        self.display_position = x_grid_pos * self.IMAGE.get_width(), y_grid_pos * self.IMAGE.get_height()
        self.image = self.IMAGE.copy()
        self.rect = self.get_rect()

    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(
            self.GRID_POSITION[0] * self.image.get_width(),
            self.GRID_POSITION[1] * self.image.get_height(),
            self.image.get_width(),
            self.image.get_height()
        )

    def update(self, **kwargs) -> None:
        pass

    def scroll_changed(self, scroll, zoom=1):
        self.display_position = game_to_display(self.rect.topleft, scroll, zoom)

    def zoom_changed(self, scroll, zoom):
        self.scroll_changed(scroll, zoom)
        self.image = scale_image(self.IMAGE, zoom).convert_alpha()

    def draw(self, surface):
        surface.blit(self.image, self.display_position)
