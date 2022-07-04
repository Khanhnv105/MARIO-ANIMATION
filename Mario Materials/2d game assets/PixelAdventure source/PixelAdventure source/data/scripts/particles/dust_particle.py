import math

import pygame

from data.engine.VFX.particle import Particle
from data.engine.math.vector import Vector
from data.engine.utils import draw_centered


class DustParticle(Particle):
    def __init__(self, manager, position, velocity_magnitude=1, direction=None):
        super().__init__(manager, position=position)
        self.image = pygame.image.load("data/Assets/Free/Other/Dust Particle.png").convert_alpha()
        if not direction:
            self.velocity = Vector.random(velocity_magnitude)
        else:
            self.velocity = Vector(math.cos(direction), math.sin(direction))
        self.life = 1

    def update(self, **kwargs):
        self.velocity.y += kwargs["dt"] * 0.1
        self.position += self.velocity * kwargs["dt"]
        self.life -= 0.05 * kwargs["dt"]
        if self.life < 0.1:
            self.destroy()

    def draw(self, surface, offset=(0, 0)):
        draw_centered(
            surface,
            pygame.transform.scale(
                surface, (int(self.life * self.image.get_width()), int(self.life * self.image.get_height()))),
            (
                self.position.x - offset[0],
                self.position.y - offset[1]
            )
        )
