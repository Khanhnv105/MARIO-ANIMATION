import pygame

from .collideable_entity import CollideableEntity
from .rect_mask_collideable_entity import RectMaskCollideableEntity


class ImageCollideableEntity(CollideableEntity):
    """
    Es la clase mas avanzada de colisiones,
    agregando la funcionalidad de masks,
    de tal forma que se obtiene una precision
    de colisiones de perfeccion por pixel
    """

    def __init__(
            self,
            collideable_group,
            position,
            image,
            visible=True,
            layer=0,
            mode="dynamic"
    ):
        rectangle = pygame.Rect(
            position[0],
            position[1],
            image.get_width(),
            image.get_height()
        )
        super().__init__(
            group=collideable_group,
            rectangle=rectangle,
            visible=visible,
            layer=layer,
            mode=mode
        )
        self.image = image
        self.mask = None
        self.update_data()

    def update_mask(self):
        self.mask = pygame.mask.from_surface(self.image)

    def collides(self, other):

        rectangle_collision = super().collides(other)

        # Mask collision
        if issubclass(other.__class__, (ImageCollideableEntity, RectMaskCollideableEntity)):
            x_offset = other.rectangle[0] - self.rectangle[0]
            y_offset = other.rectangle[1] - self.rectangle[1]
            collision_point = self.mask.overlap(other.mask, (x_offset, y_offset))
            return collision_point is not None

        return rectangle_collision

    def update_data(self):
        """Actualiza la informacion basica necesaria """

        self.update_mask()
        self.rectangle.w = self.image.get_width()
        self.rectangle.h = self.image.get_height()

