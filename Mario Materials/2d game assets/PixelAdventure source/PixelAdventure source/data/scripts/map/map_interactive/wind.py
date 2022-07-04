from random import randint

import pygame

from data.engine.animation.sprite_animation.single_animation_controller import SingleAnimationController
from data.engine.entity.collideable_entity import CollideableEntity
from data.engine.entity.rect_mask_collideable_entity import RectMaskCollideableEntity
from data.engine.math.vector import Vector
from data.scripts.particles.wind_particle import WindParticle
from data.scripts.utils import dynamic_animation_creation


class Wind(RectMaskCollideableEntity):

    def __init__(self, group, rectangle):

        """
        Rect: Contiene toda el area en la que ejerce efecto
        """
        rect = pygame.Rect(
            rectangle[0],
            rectangle[1],
            rectangle[2],
            rectangle[3]
        )

        super().__init__(group, rect, mode="static")
        self.animator = SingleAnimationController(
            dynamic_animation_creation(
                delay=5,
                images_path="data/Assets/Free/Traps/Fan/On (24x8)",
                images_scale=2
            )
        )
        self.force = Vector(0, -.55)
        self.next_particle_time = 0
        self.image = self.animator.get_image()

    def collision(self, other) -> None:
        if other.__class__.__base__.__name__ == "BasePlayer":
            other.accelerate(self.force)

    def update(self, **kwargs) -> None:
        self.animator.update(kwargs['dt'])
        if self.next_particle_time < kwargs["clock_ticks"]:
            self.next_particle_time = kwargs["clock_ticks"] + 30
            WindParticle(
                manager=self.group.particles_manager,
                position=self._get_image_pos() + Vector(randint(0, self.image.get_width()), -self.image.get_height() // 3),
                direction_vector=Vector(0, -1),
                life_distance=self.rectangle.h
            )
        self.image = self.animator.get_image()

    def _get_image_pos(self):
        return Vector(
            self.rectangle.centerx - self.image.get_width() // 2,
            self.rectangle.bottom - self.image.get_height()
        )

    def draw(self, surface, offset=(0, 0)):

        surface.blit(self.image, self._get_image_pos() - offset)
        """"pygame.draw.rect(
            surface,
            (0, 0, 0),
            (
                self.rectangle.x - offset[0],
                self.rectangle.y - offset[1],
                self.rectangle.w,
                self.rectangle.h
            ),
            2

        )"""