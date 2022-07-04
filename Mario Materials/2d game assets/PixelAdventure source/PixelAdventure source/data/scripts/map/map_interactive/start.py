import pygame

from data.engine.animation.sprite_animation.single_animation_controller import SingleAnimationController
from data.engine.entity.collideable_entity import CollideableEntity
from data.scripts.utils import dynamic_animation_creation


class Start(CollideableEntity):
    def __init__(self, group, position):
        self.animator = SingleAnimationController(
            dynamic_animation_creation(
                images_path="data/Assets/Free/Items/Checkpoints/Start/Start (Moving) (64x64)",
                images_scale=2
            )
        )
        self.image = self.animator.get_image()

        rectangle = pygame.Rect(
            position[0],
            position[1],
            self.image.get_width(),
            self.image.get_height()
        )

        super().__init__(group, rectangle, layer=1)

    def collision(self, other) -> None:
        pass

    def update(self, **kwargs) -> None:
        self.animator.update(kwargs["dt"])
        self.image = self.animator.get_image()

    def draw(self, surface, offset=(0, 0)):
        surface.blit(
            self.image,
            (
                self.rectangle.x - offset[0],
                self.rectangle.y - offset[1]
            )
        )
