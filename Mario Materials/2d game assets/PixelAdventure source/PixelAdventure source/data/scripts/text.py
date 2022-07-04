from data.engine.entity.collideable_entity import CollideableEntity
from data.engine.entity.entity import Entity


class Text(CollideableEntity):
    def __init__(self, group, position, image):
        super().__init__(
            group,
            (
                position[0], position[1],
                image.get_width(), image.get_height()
            ),
            True,
            mode="static"
        )
        self.position = position
        self.image = image

    def draw(self, surface, offset=(0, 0)):
        surface.blit(self.image, (self.position[0] - offset[0], self.position[1] - offset[1]))