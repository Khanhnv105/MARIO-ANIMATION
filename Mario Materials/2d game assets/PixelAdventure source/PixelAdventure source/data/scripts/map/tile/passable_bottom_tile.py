import pygame

from .static_tile import Tile, StaticTile


class PassableBottomTile(StaticTile):

    """
    Clase alternativa a Tile que permite atravesar
    al tile desde abajo, teniendo colisiones solamente
    con la parte superior del mismo
    """

    def __init__(self, group, top_left_position, image, layer=0):
        super().__init__(group, top_left_position, image, layer=layer)

    def draw(self, surface, offset=(0, 0)):
        super().draw(surface, offset)
        #pygame.draw.rect(surface, (0, 0, 0), (self.rectangle.x - offset[0], self.rectangle.y - offset[1], self.rectangle.w, self.rectangle.h), 2)
