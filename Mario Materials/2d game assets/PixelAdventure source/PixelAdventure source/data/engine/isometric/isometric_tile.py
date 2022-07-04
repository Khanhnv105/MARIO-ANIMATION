from typing import Tuple, List
import pygame
from engine.isometric.core import cartesian_to_isometric
from engine.tile.tile_set_loader import scale_image


class IsometricTile:
    def __init__(
            self,
            images: List[pygame.Surface],
            image_index: int,
            x_grid_pos: int,
            y_grid_pos: int,
            z_grid_pos: int,
            grid_size: tuple,
            zoom: float,
            scroll: tuple,
            display_rect=pygame.Rect,
            offset: int = 0
    ):
        """
        Clase que guarda la imagen y posicion del Tile
        """
        self.GRID_POSITION = x_grid_pos, y_grid_pos, z_grid_pos
        self.IMAGE_INDEX = image_index
        self.IMAGE_DIMENSIONS = images[image_index].get_size()

        # Offset es la variable que guarda cuanto se tiene
        # que hacer para arriba el tile en base a su dimension
        # esto es para que las imagenes mas grandes encajen
        self.offset = offset
        # if self.IMAGE_DIMENSIONS[1] > grid_size[0]:
        #    self.offset = self.IMAGE_DIMENSIONS[1] - grid_size[0]

        self.isometric_position = self.get_isometric_position(x_grid_pos, y_grid_pos)
        self.display_position = None
        self.rect = None
        self.visible = False
        self.already_saw = False

        self.IMAGE = images[image_index].copy()
        self.image = images[image_index].copy()
        self.camera_moved(scroll, zoom, display_rect)
        self.scale = 1

    def _set_visible(self, boolean):
        self.visible = boolean

    def is_visible(self, display_rect: pygame.Rect):
        return self.rect.colliderect(display_rect)

    def update(self, **kwargs) -> None:
        if self.scale < 1:
            self.scale += kwargs["dt"] * 0.02
            if self.scale > 1:
                self.scale = 1
            self.image = scale_image(self.IMAGE, self.scale).convert_alpha()

    def get_isometric_position(self, grid_x, grid_y) -> Tuple[float, float]:
        """Retorna la posición isometrica del tile"""
        isometric_grid_position = cartesian_to_isometric(grid_x, grid_y)
        return (
            isometric_grid_position[0] * self.IMAGE_DIMENSIONS[0] / 2,
            isometric_grid_position[1] * (self.IMAGE_DIMENSIONS[0] / 2) - (self.GRID_POSITION[2] * self.IMAGE_DIMENSIONS[1])
        )

    def camera_moved(self, scroll, zoom, display_rect):
        self.display_position = (
            int(self.isometric_position[0] * zoom - scroll[0]),
            int(self.isometric_position[1] * zoom - scroll[1] - self.offset * zoom)
        )
        self.rect = pygame.Rect(
            self.display_position[0],
            self.display_position[1],
            self.IMAGE_DIMENSIONS[0],
            self.IMAGE_DIMENSIONS[1]
        )
        visible = self.is_visible(display_rect)
        if not self.already_saw and visible != self.visible:
            self.scale = 0.1
            self.already_saw = True
        self.visible = visible

    def draw(self, surface):
        surface.blit(
            self.image,
            (
                int(self.display_position[0]),
                int(self.display_position[1])
            )
        )
