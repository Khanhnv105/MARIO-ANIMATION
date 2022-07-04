import pygame

from data.engine.animation.sprite_animation.animations_controller import AnimationsController
from data.engine.animation.sprite_animation.single_animation_controller import SingleAnimationController
from data.engine.entity.collideable_entity import CollideableEntity
from data.scripts.utils import dynamic_animation_creation


class Arrow(CollideableEntity):
    def __init__(self, group, position, arrow_type, side):
        animation = dynamic_animation_creation(
            images_path=f"data/Assets/Free/Traps/Arrow/{arrow_type}/{side}",
            delay=5,
            images_scale=2
        )
        self.animator = SingleAnimationController(animation)
        image = self.animator.get_image()
        rect = pygame.Rect(position[0], position[1], image.get_width(), image.get_height())
        super().__init__(group, rect, mode="static", layer=0)

    def update(self, **kwargs) -> None:
        self.animator.update(kwargs["dt"])

    def draw(self, surface, offset=(0, 0)):
        surface.blit(
            self.animator.get_image(),
            (
                self.rectangle.x - offset[0],
                self.rectangle.y - offset[1]
            )
        )
