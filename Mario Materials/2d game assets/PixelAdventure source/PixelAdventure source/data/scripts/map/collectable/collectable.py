import pygame

from data.engine.animation.sprite_animation.single_animation_controller import SingleAnimationController
from data.engine.entity.image_collideable_entity import ImageCollideableEntity
from data.engine.math.vector import Vector
from data.scripts.players.base_player import PLAYER_COLLECTABLE


class Collectable(ImageCollideableEntity):
    def __init__(self, collideable_group, center_position, animation_data, value=1):

        self.animation = SingleAnimationController(animation_data)
        image = self.animation.get_image()
        super().__init__(
            collideable_group,
            (
                center_position[0],
                center_position[1]
            ),
            image,
            layer=4
        )
        self.points = value

    def collected(self):
        data = {
            "collectable_type": type(self).__name__,
            "points": self.points,
            "color": self.get_color(),
            "position": self.get_position()
        }
        pygame.event.post(pygame.event.Event(PLAYER_COLLECTABLE, data))

    def get_position(self):
        return Vector(
            self.rectangle.centerx - self.image.get_width() // 2,
            self.rectangle.centery - self.image.get_height() // 2
        )

    def get_color(self):
        return "White"

    def update(self, **kwargs) -> None:
        self.animation.update(kwargs["dt"])
        self.image = self.animation.get_image()
        self.update_data()

    def draw(self, surface, offset=(0, 0)):
        surface.blit(
            self.image,
            (
                self.rectangle.x - offset[0],
                self.rectangle.y - offset[1]
            )
        )