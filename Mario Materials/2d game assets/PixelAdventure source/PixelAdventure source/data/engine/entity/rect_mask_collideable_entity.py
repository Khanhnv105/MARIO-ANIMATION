import pygame

from data.engine.entity.collideable_entity import CollideableEntity


class RectMaskCollideableEntity(CollideableEntity):
    """
    A diferencia de CollideableEntity esta clase permite
    a los rect tener una Mask, para que la deteccion de
    colisiones se realize entre dos Mask aunque una sea
    un rectangulo perfecto
    """

    def __init__(self, group, rectangle, layer=0, mode="dynamic", visible=True):
        super().__init__(group, rectangle, visible, layer, mode)
        self.mask = pygame.mask.from_surface(pygame.Surface(self.rectangle.size))
