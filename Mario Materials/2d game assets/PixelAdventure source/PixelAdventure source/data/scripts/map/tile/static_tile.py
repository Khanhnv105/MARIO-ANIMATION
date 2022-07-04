import pygame

from data.engine.entity.collideable_entity import CollideableEntity
from data.scripts.map.tile.tile import Tile


class StaticTile(Tile, CollideableEntity):
    """
        Todos los tiles que hereden de esta clase van a ser
        estaticos, es decir que su posicion no deberia de cambiar
        """

    def __init__(self, group, position, image, layer=0):
        self.image = image

        rectangle = pygame.Rect(
            position[0],
            position[1],
            self.image.get_width(),
            self.image.get_height()
        )
        CollideableEntity.__init__(self, group, rectangle, layer=layer, mode="static")

    def draw(self, surface, offset=(0, 0)):
        surface.blit(
            self.image,
            (
                self.rectangle.x - offset[0],
                self.rectangle.y - offset[1]
            )
        )
